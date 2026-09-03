#!/usr/bin/env python3
"""Execute an entire ROADMAP sequentially: waves parallel on GKE, phases sequential.

Reads a roadmap definition (JSON or parsed from ROADMAP.md), executes each phase's
waves in order, gates on verification between phases, and supports checkpoint resume.

Usage:
    python3 run_roadmap.py --roadmap roadmap.json --bucket gs://gke-dispatch-claude-mcp-457317
    python3 run_roadmap.py --planning-dir .planning --bucket gs://gke-dispatch-claude-mcp-457317
    python3 run_roadmap.py --resume gs://gke-dispatch-claude-mcp-457317/roadmaps/my-roadmap/state.json
"""

import argparse
import json
import re
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

from gcs_utils import gcs_read_json, gcs_write_json, run

SCRIPTS_DIR = Path(__file__).parent


def run_script(script: str, args: list[str]) -> subprocess.CompletedProcess:
    # sys.executable, not the literal "python3": PATH shims (uv, pyenv, the modern-python plugin)
    # can intercept a bare python3 and refuse to run a script path.
    script_path = SCRIPTS_DIR / script
    return run([sys.executable, str(script_path)] + args, check=False)


# --- Roadmap Parsing ---

def parse_roadmap_json(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def detect_repo_info(planning_dir: str) -> dict:
    """Detect git repo URL, branch, and SHA from the repo containing the planning dir."""
    try:
        result = run(["git", "-C", str(Path(planning_dir).resolve()), "rev-parse", "--show-toplevel"], check=False)
        if result.returncode != 0:
            return {}
        repo_root = Path(result.stdout.strip())
    except Exception:
        return {}

    info: dict[str, str] = {"_repo_root": str(repo_root)}
    try:
        result = run(["git", "-C", str(repo_root), "remote", "get-url", "origin"], check=False)
        if result.returncode == 0:
            url = result.stdout.strip()
            if url.startswith("git@github.com:"):
                url = "https://github.com/" + url[len("git@github.com:"):]
            if url.endswith(".git"):
                url = url[:-4]
            info["repo_url"] = url
    except Exception:
        pass
    try:
        result = run(["git", "-C", str(repo_root), "rev-parse", "--abbrev-ref", "HEAD"], check=False)
        if result.returncode == 0:
            info["repo_branch"] = result.stdout.strip()
    except Exception:
        pass
    try:
        result = run(["git", "-C", str(repo_root), "rev-parse", "HEAD"], check=False)
        if result.returncode == 0:
            info["git_sha"] = result.stdout.strip()
    except Exception:
        pass
    return info


def parse_planning_dir(planning_dir: str) -> dict:
    """Build a roadmap definition from a GSD .planning/ directory structure."""
    planning = Path(planning_dir)
    roadmap_md = planning / "ROADMAP.md"
    state_md = planning / "STATE.md"

    if not roadmap_md.exists():
        print(f"No ROADMAP.md found in {planning_dir}", file=sys.stderr)
        sys.exit(1)

    repo_info = detect_repo_info(planning_dir)
    repo_root = repo_info.pop("_repo_root", None)
    if repo_info.get("repo_url"):
        print(f"Detected repo: {repo_info['repo_url']} @ {repo_info.get('repo_branch', 'main')}", file=sys.stderr)
    else:
        print("WARNING: Could not detect git remote: pods will not clone a repo", file=sys.stderr)

    roadmap_text = roadmap_md.read_text()
    phases = []

    phase_dirs = sorted(planning.glob("phase-*"))
    if not phase_dirs:
        phases_subdir = planning / "phases"
        if phases_subdir.is_dir():
            phase_dirs = sorted(
                d for d in phases_subdir.iterdir()
                if d.is_dir() and re.match(r"\d+", d.name) and d.name != "_archive"
            )
    for phase_dir in phase_dirs:
        if not phase_dir.is_dir():
            continue

        phase_num = re.match(r"(\d+(?:\.\d+)?)", phase_dir.name)
        if not phase_num:
            continue
        phase_num = phase_num.group(1)

        if (phase_dir / "SUMMARY.md").exists():
            continue

        plan_files = sorted(phase_dir.glob("*PLAN*.md"))

        plans = []
        for plan_file in plan_files:
            plan_text = plan_file.read_text()
            stem = plan_file.stem.lower()
            plan_name = re.sub(r"^(\d+(?:\.\d+)?-\d+)-plan$", r"phase-\1", stem)
            if plan_name == stem:
                plan_name = stem.replace("plan-", "").replace("plan", f"phase-{phase_num}")

            fm = parse_frontmatter(plan_text)
            files_modified = list(fm.get("files_modified") or []) or extract_files_modified(plan_text)

            if repo_root:
                rel_plan_path = str(plan_file.resolve().relative_to(repo_root))
            else:
                rel_plan_path = str(plan_file)

            plans.append({
                "id": plan_name,
                "plan_path": rel_plan_path,
                "plan_content": plan_text,
                "cmd": "",
                "files_modified": files_modified,
                "wave": fm.get("wave"),
                "depends_on": list(fm.get("depends_on") or []),
                "image": "avireddy0/claude-executor:latest",
                "resource_profile": "standard",
                "repo_url": repo_info.get("repo_url", ""),
                "repo_branch": repo_info.get("repo_branch", "main"),
                "git_sha": repo_info.get("git_sha", ""),
            })

        waves = group_by_declared_waves(plans) or group_into_waves(plans)

        phase_title = extract_phase_title(roadmap_text, phase_num)
        phases.append({
            "id": f"phase-{phase_num}",
            "title": phase_title or f"Phase {phase_num}",
            "waves": waves,
            # PLAN.md carries no verification command, so planning-dir mode has no gate.
            # Author a roadmap JSON (references/multi-phase-milestone.md) when phases must gate.
            "verification": {"cmd": None, "required": False},
        })

    if phases:
        print("WARNING: planning-dir mode runs phases WITHOUT a verification gate "
              "(PLAN.md has no verification.cmd). Use --roadmap JSON to gate phases.", file=sys.stderr)

    return {
        "roadmap_id": f"roadmap-{int(time.time())}",
        "source": str(planning_dir),
        "git_sha": repo_info.get("git_sha"),
        "phases": phases,
    }


def _scalar(v: str):
    v = v.strip().strip('"').strip("'")
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    return v


def parse_frontmatter(text: str) -> dict:
    """Read the YAML frontmatter keys gsd-core plans carry (wave, depends_on, files_modified).

    Scalars, inline lists, and block lists at the top level; nested mappings are skipped.
    No PyYAML dependency so the dispatcher runs on a bare python3.
    """
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    data: dict = {}
    current_key = None
    for raw in text[3:end].split("\n"):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw[0] in " \t":
            item = raw.strip()
            if item.startswith("- ") and current_key is not None and isinstance(data.get(current_key), list):
                data[current_key].append(_scalar(item[2:]))
            else:
                current_key = None  # nested mapping: its items belong to it, not to the top-level key
            continue
        key, sep, value = raw.partition(":")
        if not sep:
            continue
        key, value = key.strip(), value.strip()
        current_key = key
        if value == "":
            data[key] = []
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [_scalar(v) for v in inner.split(",")] if inner else []
        else:
            data[key] = _scalar(value)
    return data


def group_by_declared_waves(plans: list[dict]) -> list[list[dict]] | None:
    """Honor gsd-core's `wave:` frontmatter when every plan declares it.

    Within one declared wave, plans that share files_modified are split into sequential
    sub-waves (the same rule gsd-core's execute-phase applies). Returns None when any plan
    lacks `wave`, so the caller falls back to overlap grouping.
    """
    if not plans or any(p.get("wave") is None for p in plans):
        return None
    waves: list[list[dict]] = []
    for w in sorted({p["wave"] for p in plans}):
        waves.extend(group_into_waves([p for p in plans if p["wave"] == w]))
    return waves


def extract_files_modified(plan_text: str) -> list[str]:
    files = []
    in_section = False
    for line in plan_text.split("\n"):
        if re.match(r"#+\s*(files.modified|files_modified|files to modify)", line, re.IGNORECASE):
            in_section = True
            continue
        if in_section:
            if line.startswith("#"):
                break
            match = re.match(r"\s*[-*]\s*`?([^`\s]+)`?", line)
            if match:
                files.append(match.group(1))
    return files


def extract_phase_title(roadmap_text: str, phase_num: str) -> str | None:
    pattern = rf"#+\s*Phase\s+{phase_num}\b[:\s\u2014\u2013-]*(.*)"  # colon, dash, en/em dash
    match = re.search(pattern, roadmap_text, re.IGNORECASE)
    if match:
        return match.group(1).strip().rstrip("|").strip() or f"Phase {phase_num}"
    return None


def group_into_waves(plans: list[dict]) -> list[list[dict]]:
    """Group plans into waves based on files_modified overlap."""
    if not plans:
        return []

    remaining = list(plans)
    waves = []

    while remaining:
        wave = []
        wave_files: set[str] = set()

        for plan in list(remaining):
            plan_files = set(plan.get("files_modified", []))
            if not plan_files & wave_files:
                wave.append(plan)
                wave_files |= plan_files
                remaining.remove(plan)

        if not wave:
            wave = [remaining.pop(0)]

        waves.append(wave)

    return waves


# --- Roadmap State ---

def create_roadmap_state(roadmap: dict, bucket: str) -> dict:
    total_tasks = sum(
        len(task)
        for phase in roadmap["phases"]
        for task in phase["waves"]
    )
    return {
        "roadmap_id": roadmap["roadmap_id"],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "pending",
        "current_phase_index": 0,
        "current_wave_index": 0,
        "bucket": bucket,
        "phases": [
            {
                "id": phase["id"],
                "title": phase["title"],
                "status": "pending",
                "waves": [
                    {
                        "wave_index": wi,
                        "status": "pending",
                        "wave_id": f"{roadmap['roadmap_id']}-{phase['id']}-w{wi}",
                        "task_count": len(wave),
                        "manifest_path": None,
                    }
                    for wi, wave in enumerate(phase["waves"])
                ],
            }
            for phase in roadmap["phases"]
        ],
        "metrics": {
            "total_phases": len(roadmap["phases"]),
            "completed_phases": 0,
            "total_tasks": total_tasks,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "wall_clock_seconds": None,
        },
    }


def save_state(state: dict, bucket: str, dry_run: bool = False) -> None:
    if dry_run:
        return
    path = f"{bucket}/roadmaps/{state['roadmap_id']}/state.json"
    gcs_write_json(path, state)
    print(f"  State saved to {path}", file=sys.stderr)


# --- Execution ---

def execute_wave(wave_tasks: list[dict], wave_id: str, bucket: str,
                 namespace: str, dry_run: bool = False) -> dict:
    """Normalize, dispatch, and collect a single wave."""
    tasks_json = json.dumps([
        {
            "id": t["id"],
            "cmd": t["cmd"],
            "image": t["image"],
            "resource_profile": t.get("resource_profile", "standard"),
            "inputs": {
                "plan_path": t.get("plan_path", ""),
                "plan_content": t.get("plan_content", ""),
                "repo_url": t.get("repo_url", ""),
                "repo_branch": t.get("repo_branch", "main"),
                "git_sha": t.get("git_sha", ""),
                "max_budget_usd": str(t.get("max_budget_usd", 5)),
            },
        }
        for t in wave_tasks
    ])

    import tempfile
    manifest_file = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
    manifest_path = manifest_file.name
    manifest_file.close()

    result = run_script("normalize_wave.py", [
        "--wave-id", wave_id,
        "--tasks", tasks_json,
        "--framework", "gsd",
        "--output", manifest_path,
    ])
    if result.returncode != 0:
        print(f"  Normalize failed: {result.stderr}", file=sys.stderr)
        return {"status": "failed", "error": result.stderr}

    if dry_run:
        print(f"  [dry-run] Would dispatch {len(wave_tasks)} tasks", file=sys.stderr)
        Path(manifest_path).unlink(missing_ok=True)
        return {"status": "dry_run"}

    dispatch_args = [
        "--manifest", manifest_path,
        "--bucket", bucket,
        "--namespace", namespace,
        "--mode", "auto",
    ]

    result = run_script("dispatch.py", dispatch_args)
    if result.returncode != 0:
        print(f"  Dispatch failed: {result.stderr}", file=sys.stderr)
        return {"status": "failed", "error": result.stderr}

    result = run_script("collect.py", [
        "--manifest", manifest_path,
        "--bucket", bucket,
        "--timeout", "1800",
    ])

    with open(manifest_path) as f:
        manifest = json.load(f)

    Path(manifest_path).unlink(missing_ok=True)
    return manifest


def run_verification(phase: dict) -> bool:
    """Run phase verification command. Returns True if passed."""
    verification = phase.get("verification", {})
    cmd = verification.get("cmd")
    if not cmd:
        return True

    required = verification.get("required", True)
    print(f"  Running verification: {cmd}", file=sys.stderr)
    result = run(["sh", "-c", cmd], check=False)

    if result.returncode != 0:
        print(f"  Verification {'FAILED' if required else 'warned'}: {result.stderr[:500]}", file=sys.stderr)
        return not required

    print(f"  Verification passed", file=sys.stderr)
    return True


def get_phase_files(phase: dict) -> set[str]:
    """Collect all files_modified across all waves in a phase."""
    files: set[str] = set()
    for wave in phase.get("waves", []):
        for task in wave:
            files.update(task.get("files_modified", []))
    return files


def group_phases_into_batches(phases: list[dict], start_index: int = 0) -> list[list[int]]:
    """Group phases into parallel batches based on file overlap.

    Phases with no overlapping files_modified can run concurrently.
    Returns list of batches, each batch is a list of phase indices.
    """
    remaining = list(range(start_index, len(phases)))
    batches = []

    while remaining:
        batch = []
        batch_files: set[str] = set()

        for pi in list(remaining):
            phase_files = get_phase_files(phases[pi])
            if not phase_files & batch_files:
                batch.append(pi)
                batch_files |= phase_files
                remaining.remove(pi)

        if not batch:
            batch = [remaining.pop(0)]

        batches.append(batch)

    return batches


_metrics_lock = threading.Lock()


def execute_phase(phase: dict, phase_state: dict, state: dict, pi: int,
                  total_phases: int, bucket: str, namespace: str,
                  dry_run: bool) -> bool:
    """Execute a single phase. Returns True on success, False on failure."""
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"Phase {pi+1}/{total_phases}: {phase['title']}", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)

    phase_state["status"] = "running"
    total_waves = len(phase["waves"])

    for wi in range(total_waves):
        wave_tasks = phase["waves"][wi]
        wave_state = phase_state["waves"][wi]

        if wave_state["status"] == "completed":
            print(f"  Wave {wi+1}/{total_waves}: already completed, skipping", file=sys.stderr)
            continue

        print(f"\n  Wave {wi+1}/{total_waves}: {len(wave_tasks)} tasks", file=sys.stderr)
        wave_state["status"] = "running"

        wave_result = execute_wave(
            wave_tasks, wave_state["wave_id"], bucket, namespace, dry_run
        )

        if dry_run:
            wave_state["status"] = "dry_run"
            continue

        if isinstance(wave_result, dict) and wave_result.get("status") == "failed":
            wave_state["status"] = "failed"
            with _metrics_lock:
                state["metrics"]["failed_tasks"] += wave_state["task_count"]
            print(f"  Wave {wi+1} FAILED: halting phase", file=sys.stderr)
            return False

        wave_manifest_status = wave_result.get("status", "unknown")
        completed = wave_result.get("metrics", {}).get("completed", 0)
        failed = wave_result.get("metrics", {}).get("failed", 0)

        with _metrics_lock:
            state["metrics"]["completed_tasks"] += completed
            state["metrics"]["failed_tasks"] += failed

        if wave_manifest_status == "completed":
            wave_state["status"] = "completed"
            print(f"  Wave {wi+1} completed: {completed} tasks", file=sys.stderr)
        elif wave_manifest_status == "partial_failure":
            wave_state["status"] = "partial_failure"
            print(f"  Wave {wi+1} partial failure: {completed} ok, {failed} failed", file=sys.stderr)
            return False
        else:
            wave_state["status"] = "failed"
            print(f"  Wave {wi+1} failed", file=sys.stderr)
            return False

    if not dry_run:
        if not run_verification(phase):
            phase_state["status"] = "verification_failed"
            return False

    phase_state["status"] = "completed"
    with _metrics_lock:
        state["metrics"]["completed_phases"] += 1
    print(f"\nPhase {phase['id']} completed", file=sys.stderr)
    return True


def execute_roadmap(roadmap: dict, state: dict, bucket: str,
                    namespace: str, dry_run: bool = False,
                    auto: bool = False) -> dict:
    """Execute phases with maximum parallelism: independent phases run concurrently."""
    start_time = time.time()
    state["status"] = "running"
    save_state(state, bucket, dry_run)

    start_phase = state["current_phase_index"]
    total_phases = len(roadmap["phases"])

    batches = group_phases_into_batches(roadmap["phases"], start_phase)
    print(f"Phase parallelism: {len(batches)} sequential batches from {total_phases} phases", file=sys.stderr)
    for bi, batch in enumerate(batches):
        titles = [roadmap["phases"][pi]["title"] for pi in batch]
        print(f"  Batch {bi+1}: {titles} {'(parallel)' if len(batch) > 1 else ''}", file=sys.stderr)

    for bi, batch in enumerate(batches):
        skip_all = True
        for pi in batch:
            if state["phases"][pi]["status"] != "completed":
                skip_all = False
                break
        if skip_all:
            continue

        if len(batch) == 1:
            pi = batch[0]
            phase = roadmap["phases"][pi]
            phase_state = state["phases"][pi]

            if phase_state["status"] == "completed":
                continue

            success = execute_phase(phase, phase_state, state, pi, total_phases,
                                     bucket, namespace, dry_run)
            save_state(state, bucket, dry_run)

            if not success and not dry_run:
                state["status"] = "partial_failure"
                save_state(state, bucket, dry_run)
                print(f"\nPhase {phase['id']} FAILED: roadmap halted", file=sys.stderr)
                print(f"Resume with: python3 run_roadmap.py --resume {bucket}/roadmaps/{state['roadmap_id']}/state.json",
                      file=sys.stderr)
                break
        else:
            from concurrent.futures import ThreadPoolExecutor, as_completed

            print(f"\n{'='*60}", file=sys.stderr)
            print(f"Parallel batch: {len(batch)} phases launching concurrently", file=sys.stderr)
            print(f"{'='*60}", file=sys.stderr)

            def run_phase(pi: int) -> tuple[int, bool]:
                phase = roadmap["phases"][pi]
                phase_state = state["phases"][pi]
                if phase_state["status"] == "completed":
                    return pi, True
                success = execute_phase(phase, phase_state, state, pi, total_phases,
                                         bucket, namespace, dry_run)
                return pi, success

            batch_failed = False
            with ThreadPoolExecutor(max_workers=len(batch)) as pool:
                futures = {pool.submit(run_phase, pi): pi for pi in batch}
                for future in as_completed(futures):
                    pi, success = future.result()
                    phase_title = roadmap["phases"][pi]["title"]
                    if success:
                        print(f"  [parallel] Phase {pi+1} ({phase_title}) completed", file=sys.stderr)
                    else:
                        print(f"  [parallel] Phase {pi+1} ({phase_title}) FAILED", file=sys.stderr)
                        batch_failed = True

            save_state(state, bucket, dry_run)

            if batch_failed and not dry_run:
                state["status"] = "partial_failure"
                save_state(state, bucket, dry_run)
                print(f"\nParallel batch failed: roadmap halted", file=sys.stderr)
                break

        if not dry_run and not auto:
            next_batches = batches[bi+1:]
            if next_batches:
                next_titles = [roadmap["phases"][pi]["title"] for pi in next_batches[0]]
                print(f"\nNext batch: {next_titles}", file=sys.stderr)
                try:
                    answer = input("Continue? [Y/n] ").strip().lower()
                    if answer in ("n", "no"):
                        print("Paused. Resume with --resume flag.", file=sys.stderr)
                        state["status"] = "paused"
                        save_state(state, bucket, dry_run)
                        break
                except (EOFError, KeyboardInterrupt):
                    print("\nPaused. Resume with --resume flag.", file=sys.stderr)
                    state["status"] = "paused"
                    save_state(state, bucket, dry_run)
                    break

    all_completed = all(p["status"] == "completed" for p in state["phases"])
    if all_completed:
        state["status"] = "completed"

    state["metrics"]["wall_clock_seconds"] = round(time.time() - start_time, 2)
    save_state(state, bucket, dry_run)
    return state


# --- Summary ---

def print_summary(state: dict) -> None:
    m = state["metrics"]
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"Roadmap: {state['roadmap_id']}", file=sys.stderr)
    print(f"Status: {state['status']}", file=sys.stderr)
    print(f"Phases: {m['completed_phases']}/{m['total_phases']}", file=sys.stderr)
    print(f"Tasks: {m['completed_tasks']}/{m['total_tasks']} completed, {m['failed_tasks']} failed", file=sys.stderr)
    if m.get("wall_clock_seconds"):
        mins = m["wall_clock_seconds"] / 60
        print(f"Wall clock: {mins:.1f} minutes", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)

    for phase in state["phases"]:
        icon = {"completed": "+", "failed": "!", "running": "~", "pending": " ",
                "verification_failed": "V"}.get(phase["status"], "?")
        print(f"  [{icon}] {phase['id']}: {phase['title']}: {phase['status']}", file=sys.stderr)
        for wave in phase["waves"]:
            wi_icon = {"completed": "+", "failed": "!", "pending": " "}.get(wave["status"], "?")
            print(f"      [{wi_icon}] wave-{wave['wave_index']}: {wave['task_count']} tasks: {wave['status']}",
                  file=sys.stderr)


# --- Main ---

def main():
    parser = argparse.ArgumentParser(description="Execute a full roadmap on GKE")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--roadmap", help="Path to roadmap JSON file")
    source.add_argument("--planning-dir", help="Path to GSD .planning/ directory")
    source.add_argument("--resume", help="GCS path to state.json for checkpoint resume")

    parser.add_argument("--bucket", default="gs://gke-dispatch-claude-mcp-457317",
                        help="GCS bucket for wave data")
    parser.add_argument("--namespace", default="gke-dispatch", help="K8s namespace")
    parser.add_argument("--dry-run", action="store_true", help="Parse and plan without dispatching")
    parser.add_argument("--auto", action="store_true",
                        help="Run without confirmation prompts between phases")
    parser.add_argument("--json", action="store_true", help="Output final state as JSON to stdout")
    args = parser.parse_args()

    if args.resume:
        print(f"Resuming from checkpoint: {args.resume}", file=sys.stderr)
        state = gcs_read_json(args.resume)
        if not state:
            print(f"Failed to read state from {args.resume}", file=sys.stderr)
            sys.exit(1)

        roadmap_source = state.get("_roadmap_snapshot")
        if not roadmap_source:
            print("State file missing _roadmap_snapshot: cannot resume without roadmap definition", file=sys.stderr)
            sys.exit(1)

        roadmap = roadmap_source
        bucket = state["bucket"]
    elif args.roadmap:
        roadmap = parse_roadmap_json(args.roadmap)
        bucket = args.bucket
        state = create_roadmap_state(roadmap, bucket)
    else:
        roadmap = parse_planning_dir(args.planning_dir)
        bucket = args.bucket
        state = create_roadmap_state(roadmap, bucket)

    if not args.resume:
        state["_roadmap_snapshot"] = roadmap

    total_phases = len(roadmap["phases"])
    total_waves = sum(len(p["waves"]) for p in roadmap["phases"])
    total_tasks = sum(len(t) for p in roadmap["phases"] for t in p["waves"])
    print(f"Roadmap: {roadmap['roadmap_id']}", file=sys.stderr)
    print(f"  {total_phases} phases, {total_waves} waves, {total_tasks} tasks", file=sys.stderr)

    if args.dry_run:
        print(f"\n[DRY RUN] Would execute:", file=sys.stderr)
        for pi, phase in enumerate(roadmap["phases"]):
            print(f"  Phase {pi+1}: {phase['title']}", file=sys.stderr)
            for wi, wave in enumerate(phase["waves"]):
                task_ids = [t["id"] for t in wave]
                print(f"    Wave {wi+1}: {task_ids}", file=sys.stderr)

    state = execute_roadmap(roadmap, state, bucket, args.namespace, args.dry_run, args.auto)
    print_summary(state)

    if args.json:
        clean_state = {k: v for k, v in state.items() if k != "_roadmap_snapshot"}
        print(json.dumps(clean_state, indent=2))

    if state["status"] not in ("completed", "dry_run", "paused"):
        sys.exit(1)


if __name__ == "__main__":
    main()
