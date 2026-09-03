#!/usr/bin/env python3
"""Dispatch a wave manifest to GKE.

Order of operations:
1. merge with the manifest already in GCS (completed tasks stay completed);
2. reset failed tasks to pending (retry semantics hold for a local-only manifest too);
3. re-validate depends_on (hand-edited manifests bypass normalize_wave.py);
4. reconcile against result files in GCS: adopt a prior exit-0 result as completed, archive a
   prior failed result so the in-pod guard and collect.py do not read it as the new outcome;
5. `kubectl apply` on the cluster named in config.cluster (default envision-compute).
`--dry-run` stops after step 4's read-only part and prints the YAML; it writes nothing.
"""

import argparse
import json
import sys
import tempfile
import time
from pathlib import Path

from gcs_utils import DEFAULT_CONFIG, gcs_read_json, gcs_write_json, run
from job_templates import build_job_yaml, _is_executor
from normalize_wave import check_dependency_cycles

CLUSTER_SETUP_HINT = "See references/cluster-setup.md for the error-driven fix."


def upload_inputs(manifest: dict, bucket: str) -> None:
    wave_id = manifest["wave_id"]
    for task in manifest["tasks"]:
        if task["status"] != "pending" or not task.get("inputs"):
            continue
        path = f"{bucket}/waves/{wave_id}/inputs/{task['id']}.json"
        gcs_write_json(path, task["inputs"])


def recount(manifest: dict) -> None:
    m = manifest["metrics"]
    m["completed"] = sum(1 for t in manifest["tasks"] if t["status"] == "completed")
    m["failed"] = sum(1 for t in manifest["tasks"] if t["status"] == "failed")
    m["pending"] = sum(1 for t in manifest["tasks"] if t["status"] == "pending")


def merge_with_existing(manifest: dict, bucket: str) -> dict:
    """Idempotent replay against the GCS manifest: keep completed tasks, reset failed ones."""
    wave_id = manifest["wave_id"]
    existing = gcs_read_json(f"{bucket}/waves/{wave_id}/manifest.json")
    if not existing:
        return manifest

    existing_status = {t["id"]: t for t in existing["tasks"]}
    for task in manifest["tasks"]:
        prior = existing_status.get(task["id"])
        if prior and prior["status"] == "completed":
            task["status"] = "completed"
            task["result"] = prior["result"]
        elif prior and prior["status"] == "failed":
            task["status"] = "pending"
    recount(manifest)
    print(f"Idempotent merge: {manifest['metrics']['completed']} already completed, "
          f"{manifest['metrics']['pending']} to dispatch", file=sys.stderr)
    return manifest


def reset_failed(manifest: dict) -> int:
    """A failed task in the manifest you hand dispatch.py is a retry request."""
    n = 0
    for task in manifest["tasks"]:
        if task["status"] == "failed":
            task["status"] = "pending"
            task["result"] = None
            n += 1
    if n:
        recount(manifest)
        print(f"Retrying {n} failed task(s)", file=sys.stderr)
    return n


def reconcile_with_results(manifest: dict, bucket: str, dry_run: bool) -> dict:
    """Look at outputs/<task>/result.json for every pending task.

    exit 0 there means the work is done (a Job that finished after collect.py timed out, or a
    resume): adopt it as completed. Anything else is a stale failure: move it aside, because the
    in-pod idempotent guard and collect.py both key off that file.
    """
    wave_id = manifest["wave_id"]
    adopted, archived = [], []
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    for task in manifest["tasks"]:
        if task["status"] != "pending":
            continue
        base = f"{bucket}/waves/{wave_id}/outputs/{task['id']}"
        prior = gcs_read_json(f"{base}/result.json")
        if prior is None:
            continue
        if prior.get("exit_code") == 0 and not prior.get("is_error"):
            task["status"] = "completed"
            task["result"] = {
                "exit_code": 0, "is_error": False, "cost_usd": prior.get("total_cost_usd"),
                "duration_seconds": prior.get("duration_seconds"),
                "output_path": f"{base}/result.json", "stdout_path": f"{base}/stdout.log",
                "stderr_path": f"{base}/stderr.log", "artifacts": [], "error": None,
            }
            adopted.append(task["id"])
        else:
            if not dry_run:
                run(["gsutil", "mv", f"{base}/result.json", f"{base}/result.prev-{stamp}.json"])
            archived.append(task["id"])
    if adopted:
        print(f"Adopted prior successful results for: {', '.join(adopted)}", file=sys.stderr)
    if archived:
        verb = "Would archive" if dry_run else "Archived"
        print(f"{verb} stale failed result.json for: {', '.join(archived)}", file=sys.stderr)
    recount(manifest)
    return {"adopted": adopted, "archived": archived}


def select_mode(manifest: dict) -> str:
    """Only indexed-job exists. `auto` and `pod-pool` both resolve here; pod-pool is unbuilt."""
    mode = manifest["config"].get("mode", "auto")
    if mode == "pod-pool":
        print("pod-pool mode is not implemented; using indexed-job", file=sys.stderr)
    return "indexed-job"


def kubectl_args(manifest: dict) -> list[str]:
    """kubectl prefix pinned to a context. A null `config.cluster` (every manifest written before
    2026-09-03) falls back to the envision-compute default, the only cluster with the namespace;
    the literal "current" opts into whatever context kubectl has selected."""
    cluster = manifest["config"].get("cluster") or DEFAULT_CONFIG["cluster"]
    if cluster == "current":
        return ["kubectl"]
    return ["kubectl", "--context", cluster]


def apply_yaml(manifest: dict, yaml_content: str) -> None:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(yaml_content)
        yaml_path = f.name
    try:
        result = run(kubectl_args(manifest) + ["apply", "-f", yaml_path], check=False)
        if result.returncode != 0:
            print(result.stderr.strip(), file=sys.stderr)
            print(f"kubectl apply failed ({' '.join(kubectl_args(manifest))}). "
                  f"{CLUSTER_SETUP_HINT}", file=sys.stderr)
            sys.exit(1)
        print(result.stdout, file=sys.stderr)
    finally:
        Path(yaml_path).unlink()


def main():
    parser = argparse.ArgumentParser(description="Dispatch wave to GKE")
    parser.add_argument("--manifest", required=True, help="Path to wave manifest JSON")
    parser.add_argument("--bucket", default=None, help="Override GCS bucket")
    parser.add_argument("--namespace", default=None, help="Override K8s namespace")
    parser.add_argument("--cluster", default=None,
                        help="Override kubeconfig context (default: envision-compute)")
    parser.add_argument("--mode", default=None, help="Override compute mode (only indexed-job exists)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print Job YAML and the apply command; no GCS writes, no kubectl")
    args = parser.parse_args()

    with open(args.manifest) as f:
        manifest = json.load(f)

    if args.bucket:
        manifest["config"]["bucket"] = args.bucket
    if args.namespace:
        manifest["config"]["namespace"] = args.namespace
    if args.cluster:
        manifest["config"]["cluster"] = args.cluster
    if args.mode:
        manifest["config"]["mode"] = args.mode

    bucket = manifest["config"]["bucket"]

    manifest = merge_with_existing(manifest, bucket)
    reset_failed(manifest)

    dep_errors = check_dependency_cycles(manifest["tasks"])
    if dep_errors:
        print("Manifest rejected: depends_on must name tasks in this wave "
              "(run_roadmap.py turns cross-wave dependencies into branch merges):", file=sys.stderr)
        for e in dep_errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    reconcile_with_results(manifest, bucket, args.dry_run)

    pending = [t for t in manifest["tasks"] if t["status"] == "pending"]
    if not pending:
        print("All tasks already completed. Nothing to dispatch.", file=sys.stderr)
        sys.exit(0)

    select_mode(manifest)
    mode = "executor-jobs (one Job per task)" if _is_executor(pending[0]) else "indexed-job"

    try:
        yaml_content = build_job_yaml(manifest)
    except ValueError as e:
        print(f"Manifest rejected: {e}", file=sys.stderr)
        sys.exit(1)

    if args.dry_run:
        print(yaml_content)
        apply_cmd = " ".join(kubectl_args(manifest) + ["apply", "-f", "<generated>.yaml"])
        print(f"[dry-run] {len(pending)} task(s) via {mode}; would run: {apply_cmd}", file=sys.stderr)
        print(f"[dry-run] no GCS writes; manifest would land at {bucket}/waves/{manifest['wave_id']}/manifest.json",
              file=sys.stderr)
        sys.exit(0)

    manifest["status"] = "dispatching"
    gcs_write_json(f"{bucket}/waves/{manifest['wave_id']}/manifest.json", manifest)
    upload_inputs(manifest, bucket)

    print(f"Dispatching {len(pending)} tasks via {mode}", file=sys.stderr)
    apply_yaml(manifest, yaml_content)

    manifest["status"] = "running"
    gcs_write_json(f"{bucket}/waves/{manifest['wave_id']}/manifest.json", manifest)

    with open(args.manifest, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"Wave {manifest['wave_id']} dispatched: {len(pending)} tasks running", file=sys.stderr)


if __name__ == "__main__":
    main()
