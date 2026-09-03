#!/usr/bin/env python3
"""Poll GCS for task completions and collect results into the manifest."""

import argparse
import json
import sys
import time

from gcs_utils import gcs_list, gcs_read_json, gcs_write_json


def check_task_completion(task: dict, bucket: str, wave_id: str) -> dict:
    """Check if a task has completed by looking for result.json in GCS."""
    if task["status"] == "completed":
        return task

    task_id = task["id"]
    base = f"{bucket}/waves/{wave_id}/outputs/{task_id}"
    result = gcs_read_json(f"{base}/result.json")

    if result is None:
        return task

    exit_code = result.get("exit_code", -1)
    is_error = bool(result.get("is_error", False))
    task["result"] = {
        "exit_code": exit_code,
        "is_error": is_error,
        "cost_usd": result.get("total_cost_usd"),
        "duration_seconds": result.get("duration_seconds"),
        "output_path": f"{base}/result.json",
        "stdout_path": f"{base}/stdout.log",
        "stderr_path": f"{base}/stderr.log",
        "artifacts": gcs_list(f"{base}/artifacts/"),
        "error": result.get("error") if exit_code != 0 else None,
    }
    task["status"] = "completed" if exit_code == 0 and not is_error else "failed"
    return task


def update_metrics(manifest: dict) -> dict:
    completed = sum(1 for t in manifest["tasks"] if t["status"] == "completed")
    failed = sum(1 for t in manifest["tasks"] if t["status"] == "failed")
    pending = sum(1 for t in manifest["tasks"] if t["status"] in ("pending", "running"))
    manifest["metrics"]["completed"] = completed
    manifest["metrics"]["failed"] = failed
    manifest["metrics"]["pending"] = pending
    return manifest


def determine_wave_status(manifest: dict) -> str:
    statuses = {t["status"] for t in manifest["tasks"]}
    if statuses == {"completed"}:
        return "completed"
    if "pending" in statuses or "running" in statuses:
        return "running"
    if "failed" in statuses and "completed" in statuses:
        return "partial_failure"
    if statuses == {"failed"}:
        return "failed"
    return "running"


def collect(manifest: dict, bucket: str, timeout: int, poll_interval: int = 10) -> dict:
    wave_id = manifest["wave_id"]
    start = time.time()
    total = manifest["metrics"]["total_tasks"]

    print(f"Collecting results for wave {wave_id} ({total} tasks)", file=sys.stderr)

    while True:
        for i, task in enumerate(manifest["tasks"]):
            if task["status"] not in ("pending", "running"):
                continue
            manifest["tasks"][i] = check_task_completion(task, bucket, wave_id)

        manifest = update_metrics(manifest)
        status = determine_wave_status(manifest)
        manifest["status"] = status

        completed = manifest["metrics"]["completed"]
        failed = manifest["metrics"]["failed"]
        pending = manifest["metrics"]["pending"]
        elapsed = int(time.time() - start)

        print(f"  [{elapsed}s] {completed}/{total} completed, {failed} failed, {pending} pending",
              file=sys.stderr)

        if status in ("completed", "partial_failure", "failed"):
            break

        if time.time() - start > timeout:
            print(f"Timeout after {timeout}s: {pending} tasks still pending", file=sys.stderr)
            manifest["status"] = "partial_failure" if completed > 0 else "failed"
            break

        time.sleep(poll_interval)

    manifest["metrics"]["wall_clock_seconds"] = round(time.time() - start, 2)

    durations = [t["result"]["duration_seconds"] for t in manifest["tasks"]
                 if t.get("result") and t["result"].get("duration_seconds")]
    manifest["metrics"]["total_cpu_seconds"] = round(sum(durations), 2) if durations else None
    costs = [t["result"]["cost_usd"] for t in manifest["tasks"]
             if t.get("result") and t["result"].get("cost_usd") is not None]
    manifest["metrics"]["total_cost_usd"] = round(sum(costs), 4) if costs else None

    gcs_write_json(f"{bucket}/waves/{wave_id}/manifest.json", manifest)

    return manifest


def print_summary(manifest: dict) -> None:
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"Wave: {manifest['wave_id']}", file=sys.stderr)
    print(f"Status: {manifest['status']}", file=sys.stderr)
    m = manifest["metrics"]
    print(f"Tasks: {m['completed']}/{m['total_tasks']} completed, {m['failed']} failed", file=sys.stderr)
    if m.get("wall_clock_seconds"):
        print(f"Wall clock: {m['wall_clock_seconds']}s", file=sys.stderr)
    if m.get("total_cpu_seconds"):
        print(f"Total CPU time: {m['total_cpu_seconds']}s", file=sys.stderr)
    if m.get("total_cost_usd") is not None:
        print(f"Claude spend: ${m['total_cost_usd']}", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)

    for task in manifest["tasks"]:
        icon = {"completed": "+", "failed": "!", "pending": "?", "running": "~"}.get(task["status"], "?")
        line = f"  [{icon}] {task['id']}: {task['status']}"
        if task.get("result"):
            r = task["result"]
            if r.get("duration_seconds"):
                line += f" ({r['duration_seconds']}s)"
            if r.get("error"):
                line += f": {r['error']}"
        print(line, file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Collect wave results from GCS")
    parser.add_argument("--manifest", required=True, help="Path to wave manifest JSON")
    parser.add_argument("--bucket", default=None, help="Override GCS bucket")
    parser.add_argument("--timeout", type=int, default=900, help="Max seconds to poll (default: 900)")
    parser.add_argument("--poll-interval", type=int, default=10, help="Seconds between polls (default: 10)")
    parser.add_argument("--json", action="store_true", help="Output full manifest as JSON to stdout")
    args = parser.parse_args()

    with open(args.manifest) as f:
        manifest = json.load(f)

    bucket = args.bucket or manifest["config"]["bucket"]

    manifest = collect(manifest, bucket, args.timeout, args.poll_interval)
    print_summary(manifest)

    with open(args.manifest, "w") as f:
        json.dump(manifest, f, indent=2)

    if args.json:
        print(json.dumps(manifest, indent=2))

    failed = manifest["metrics"]["failed"]
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
