# Wave Manifest Schema

The wave manifest is the single source of truth for a dispatch cycle. `normalize_wave.py` creates
it, `dispatch.py` uploads it to `gs://<bucket>/waves/<wave_id>/manifest.json`, and `collect.py`
updates it as tasks finish.

## Schema

```json
{
  "wave_id": "string (required, unique, idempotency key)",
  "created_at": "ISO8601 timestamp",
  "git_sha": "string (optional, pins reproducibility)",
  "source_framework": "string (gsd | ralph | bmad | taskmaster | custom)",
  "status": "pending | dispatching | running | completed | partial_failure | failed",
  "tasks": [
    {
      "id": "string (required, unique within wave; becomes part of the Job name and branch name)",
      "index": "integer (auto-assigned, maps to JOB_COMPLETION_INDEX)",
      "cmd": "string (required; '' for executor tasks that run a plan)",
      "image": "string (required; 'claude-executor' in the name selects the executor path)",
      "inputs": {
        "repo_url": "executor: repo to clone",
        "repo_branch": "executor: branch (default main)",
        "git_sha": "executor: pin the checkout",
        "plan_path": "executor: PLAN.md path inside the clone",
        "plan_content": "executor: inline plan text (wins over plan_path)",
        "max_budget_usd": "executor: --max-budget-usd (default 5; below ~2 fails on the context floor)",
        "merge_branches": ["executor: branches fetched and merged before the plan runs; run_roadmap.py fills this from depends_on on earlier waves"],
        "...": "anything else, uploaded as inputs/<task_id>.json"
      },
      "outputs_pattern": "string (informational; everything under /outputs is collected)",
      "resource_profile": "light | standard | heavy | gpu | gpu_high",
      "timeout_seconds": "integer (default 600; Job activeDeadlineSeconds = timeout + 60)",
      "retries": "integer (default 2; executor: the Job's backoffLimit; indexed: backoffLimitPerIndex, so one task's failures never terminate its siblings)",
      "depends_on": ["task_id (same wave only; see below)"],
      "status": "pending | running | completed | failed | skipped",
      "result": {
        "exit_code": "integer",
        "is_error": "boolean (executor envelope; forces failed even on exit 0)",
        "cost_usd": "float | null (executor total_cost_usd)",
        "duration_seconds": "float",
        "output_path": "gs:// path to result.json",
        "stdout_path": "gs:// path to stdout.log",
        "stderr_path": "gs:// path to stderr.log",
        "artifacts": ["gs:// paths under outputs/<task_id>/artifacts/"],
        "error": "string (if failed)"
      }
    }
  ],
  "config": {
    "mode": "indexed-job | auto (pod-pool is accepted and ignored: not implemented)",
    "parallelism_cap": "integer | null (null = one pod per task)",
    "bucket": "gs://gke-dispatch-claude-mcp-457317",
    "namespace": "gke-dispatch",
    "cluster": "kubeconfig context; default gke_claude-mcp-457317_us-central1_envision-compute; null (pre-2026-09-03 manifests) falls back to that default; the literal \"current\" uses kubectl's current context",
    "node_pool": "unused",
    "service_account": "gke-dispatch-worker"
  },
  "metrics": {
    "total_tasks": "integer",
    "completed": "integer",
    "failed": "integer",
    "pending": "integer",
    "wall_clock_seconds": "float",
    "total_cpu_seconds": "float (sum of task durations)",
    "total_cost_usd": "float | null (sum of executor spend)"
  }
}
```

## Validation rules

`normalize_wave.py` enforces 1–6; `job_templates.build_job_yaml` enforces 7 (so `dispatch.py`
rejects the manifest before any GCS write).

1. `wave_id` unique across all dispatches: `{framework}-{phase}-{wave}-{timestamp}`.
2. `tasks[].id` unique within the wave. Lowercase, `[a-z0-9.-]`: it is embedded in a DNS-1123 Job
   name (`gke-dispatch-<wave_id>-<task_id>`, truncated to 63 chars) and in the push branch.
3. `tasks[].image` pullable from the cluster (Docker Hub, gcr.io, Artifact Registry).
4. `tasks[].depends_on` resolve to task ids **in the same wave**; no cycles. `dispatch.py`
   re-checks this, so a hand-edited manifest cannot smuggle in a dependency the pod would poll for
   forever. `run_roadmap.py` converts dependencies on earlier waves into `inputs.merge_branches`
   before normalizing, which is how cross-wave dependencies work through the roadmap runner.
5. `resource_profile` is one of the five above. `timeout_seconds` ≥ 1, `retries` ≥ 0.
6. `config.bucket` writable by `gke-dispatch-sa`.
7. **Wave homogeneity.** A wave is either all `claude-executor` tasks (one Job per task; each keeps
   its own timeout/retries/profile) or all generic tasks sharing **one image and one
   `resource_profile`** (one Indexed Job). Mixed waves are rejected with a message naming the split.

## Idempotency contract

`wave_id` is the idempotency key. When `dispatch.py` sees an existing
`waves/<wave_id>/manifest.json`:

1. Tasks `completed` there stay completed (result copied over); nothing re-runs.
2. Tasks `failed` there, or in the manifest you pass, reset to `pending`.
3. Each pending task's `outputs/<task_id>/result.json` is reconciled: exit 0 without `is_error`
   is adopted as completed; anything else is moved to `result.prev-<timestamp>.json` so the pod
   guard and `collect.py` cannot read a stale failure as the new outcome.
4. Only `pending` tasks become Job pods. In the pod, the guard (indexed: `idempotent-check` init
   container; executor: the entrypoint, before cloning) skips when `result.json` already shows
   exit 0.

Re-running `dispatch.py` with the same manifest is always safe. Re-running while the previous
Job is still active re-applies identical YAML (`unchanged`); it does not spawn a second copy.
`--dry-run` performs steps 1 to 3 read-only (it reports what it would archive) and prints the YAML.

## `depends_on` semantics

Only executor tasks honor it, and only within one wave (same `wave_id`):

- The `wait-deps` init container polls `outputs/<dep>/result.json` every 15 s and exits 1 if any
  dependency finished with a non-zero `exit_code` (the task then fails without running).
- On success it records `gke-dispatch/<wave_id>/<dep>` for each dependency, and the entrypoint
  fetches and merges those branches into the clone before the plan runs.

A hand-built single-wave manifest that needs another task's *code* must put both tasks in the
**same wave** with `depends_on`; waves are sequential but a wave-2 pod clones the tree pinned at
kickoff, not wave 1's branches. Under `run_roadmap.py` the same need is expressed the gsd-core
way: `depends_on` naming a task in an earlier wave or phase becomes `inputs.merge_branches`, and
the `wait-deps` init container writes those branches without polling (their waves already
finished). Forward references (same or later wave) are rejected. Generic (Indexed Job) tasks
ignore `depends_on`.

## Status transitions

```
Task:  pending → running → completed
                        → failed (retries exhausted, non-zero exit, or is_error=true)

Wave:  pending → dispatching → running → completed        (all tasks completed)
                                       → partial_failure  (some failed or collect timed out with progress)
                                       → failed           (all failed, or timed out with none completed)
```

`collect.py --timeout` marks still-pending tasks by wall clock; the pods may still be running.
Re-run `collect.py` later with the same manifest to pick them up.

## wave_id conventions

| Framework | Format | Example |
|---|---|---|
| GSD (`run_roadmap.py`) | `<roadmap_id>-<phase_id>-w<n>` | `roadmap-1787033210-phase-91.1-w0` |
| GSD (manual) | `gsd-p<phase>-w<wave>-<timestamp>` | `gsd-p3-w2-1717900800` |
| Ralph | `ralph-<loop>-i<iteration>-<timestamp>` | `ralph-abc123-i5-1717900800` |
| Custom | `<framework>-<identifier>-<timestamp>` | `gke-pilot-shell-reads-1787035524` |
