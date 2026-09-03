---
name: GKE Dispatch
description: >
  Run 2+ independent tasks in parallel on GKE cluster envision-compute (claude-mcp-457317) as
  Kubernetes Jobs: generic container commands, or Claude Code plan executions in the
  claude-executor image, with results in GCS and idempotent replay keyed by wave id. Use it
  whenever work should leave the Mac and fan out: "dispatch to GKE", "run these plans on the
  cluster", "offload this wave", executing a GSD phase or a whole roadmap off-machine, retrying a
  partially failed wave, or any question about the gke-dispatch namespace, the dispatch bucket,
  the executor image, or wave manifests. Also use it when someone wants parallel execution of
  containerizable tasks and has not named a venue. Not for Envision-MCP's dispatch_heavy_job
  skill catalog, Kueue/GPU model serving (gke:ai-platform), or agent sandboxes (gke:agent-runtime).
---

# GKE Dispatch

Turn a list of independent tasks into one wave, run the wave as Kubernetes Jobs on
`envision-compute`, and collect every task's result from GCS. Re-running a wave never repeats a
task that already finished. Scripts live in `${CLAUDE_PLUGIN_ROOT}/skills/dispatch/scripts/`;
run them from that directory or with absolute paths.

## Ground truth (verified live 2026-09-03)

| Fact | Value |
|---|---|
| Cluster | `envision-compute`, `us-central1`, project `claude-mcp-457317` |
| kubeconfig context | `gke_claude-mcp-457317_us-central1_envision-compute` (scripts pin it; your current context is irrelevant) |
| Namespace / KSA | `gke-dispatch` / `gke-dispatch-worker` (Workload Identity to `gke-dispatch-sa@…`) |
| Bucket | `gs://gke-dispatch-claude-mcp-457317/waves/<wave_id>/` (30-day lifecycle) |
| Executor image | `avireddy0/claude-executor:latest`, last pushed **2026-05-08**; rebuild needed before the next executor wave (`references/executor-image.md`) |
| Job TTL | 1 hour after finish; `kubectl get jobs` is usually empty. GCS holds the record. |
| Usage to date | Three pilot waves on 2026-08-18; no roadmap has run end to end |

The only other clusters in the project (`envision-delta-gke`, `envision-cockpit-uswest1`) lack the
namespace; a hand-typed `kubectl` on the wrong context fails with `namespaces "gke-dispatch" not
found`.

## Preflight

```bash
kubectl config get-contexts -o name | grep envision-compute
gcloud storage ls gs://gke-dispatch-claude-mcp-457317/waves/ | tail -3
```

Context missing: `references/cluster-setup.md` (first error entry). Both present: proceed.

## Two task kinds

| | Generic container task | Claude executor task |
|---|---|---|
| `image` | any image with `sh` (python3 is **not** required) | `avireddy0/claude-executor:*` |
| `cmd` | the shell command | `""`; the plan comes from `inputs` |
| Wave rule | one image and one `resource_profile` per wave (one Indexed Job) | mixed profiles fine (one Job per task); never mix with generic tasks |
| Inputs | anything, lands in `inputs/<task>.json` | `repo_url`, `repo_branch`, `plan_path` or `plan_content`, `max_budget_usd` (default 5) |
| Output | `stdout.log`, `stderr.log`, `result.json`, files written to `/outputs` → `artifacts/` | same, plus commits pushed to branch `gke-dispatch/<wave_id>/<task_id>`; nothing merges by itself |
| `depends_on` | ignored | same wave: blocks until the dependency succeeds, then merges its branch; `run_roadmap.py` turns dependencies on earlier waves into branch merges (`inputs.merge_branches`) |

`dispatch.py` rejects a wave that mixes the two kinds, or generic tasks with two images or two
profiles, before writing anything. Split into separate waves.

## Quick start

1. Normalize the task list into a manifest (validates ids, profiles, dependency cycles):

```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/dispatch/scripts
python3 normalize_wave.py --wave-id "lint-sweep-$(date +%s)" --framework custom \
  --tasks '[
    {"id":"ruff-src","cmd":"apt-get install -y -q git >/dev/null && git clone --depth 1 https://github.com/pallets/click /w && pip install -q ruff && ruff check /w/src",
     "image":"python:3.12-slim","resource_profile":"light","timeout_seconds":600,"retries":0},
    {"id":"ruff-tests","cmd":"apt-get install -y -q git >/dev/null && git clone --depth 1 https://github.com/pallets/click /w && pip install -q ruff && ruff check /w/tests",
     "image":"python:3.12-slim","resource_profile":"light","timeout_seconds":600,"retries":0}
  ]' --output /tmp/wave.json
```

(`python:3.12-slim` ships without `git`; the `apt-get` is what makes the clone work.)

2. Dry-run. Prints the Job YAML and the exact `kubectl --context … apply` it would run; writes
   nothing to GCS or the cluster:

```bash
python3 dispatch.py --manifest /tmp/wave.json --dry-run
```

3. Dispatch, then collect (polls `result.json` per task; exits 1 if any task failed):

```bash
python3 dispatch.py --manifest /tmp/wave.json
python3 collect.py  --manifest /tmp/wave.json --timeout 1800
```

`collect.py` rewrites the manifest with per-task `exit_code`, `duration_seconds`, GCS paths, and
(for executor tasks) `is_error` and `cost_usd`. Read a task's output with
`gcloud storage cat gs://gke-dispatch-claude-mcp-457317/waves/<wave_id>/outputs/<task_id>/stdout.log`.

## Scheduling reality

The two task kinds schedule differently:

- **Generic tasks** (Indexed Job) take the first fit. `default-pool` (on-demand e2-standard-4,
  usually 2 to 3 nodes running) is untainted, so `light` and `standard` pods start after an
  image pull, typically 1 to 2 minutes. `heavy` asks for 8 CPU, which no default-pool node has;
  it tolerates the spot GPU pools and waits for a g2-standard-24 to scale up.
- **Executor tasks** pin to **spot** nodes. Every spot pool on `envision-compute` is a GPU pool
  and they idle at zero, so a `standard` executor task boots an L4 spot node: 2 to 5 minutes
  before Claude starts. A dozen 20-minute plans amortize that; a dozen 30-second tasks do not.

| Profile | Request / limit | Generic task lands on | Executor task lands on |
|---|---|---|---|
| `light` | 0.5 CPU, 512Mi / 1 CPU, 1Gi | `default-pool` | spot L4 node (prefers dual-L4) |
| `standard` | 2 CPU, 4Gi / 4, 8Gi | `default-pool` | spot L4 node |
| `heavy` | 8 CPU, 16Gi / 16, 32Gi | spot dual-L4 node (scale-up) | spot dual-L4 node |
| `gpu` | 4 CPU, 16Gi + 1 GPU | L4 pools only | L4 pools only |
| `gpu_high` | 8 CPU, 64Gi + 1 GPU | `h100-spot-pool` | `h100-spot-pool` |

A non-zero exit marks the task `failed` and it retries up to `retries` times (default 2). Each
task retries on its own (`backoffLimitPerIndex`): a failing task never terminates its siblings.
Deterministic checks such as linters should set `retries: 0`; a lint finding is not a transient
failure. Generic pods carry no GitHub credential: private repos need the executor image (GitHub
App token) or a token you provision in Secret Manager yourself.

There is no A100 pool; do not invent a profile for one. Quotas for modern GPUs are only visible
through `gcq us-central1 claude-mcp-457317 gpu`, never `gcloud compute regions describe`.

## Claude executor tasks

An executor task clones `repo_url` at `repo_branch` (pinned to `git_sha` when set), reads the
plan from `plan_path` inside the clone or from inline `plan_content`, and runs
`claude -p --dangerously-skip-permissions --output-format json --max-budget-usd <n>` with the
plan as the prompt. The pod authenticates through Workload Identity: an init container pulls the
Claude OAuth token and the GitHub App key from Secret Manager, so no credentials live in
manifests or images.

Budget is the bound (`--max-turns` no longer exists in the CLI). A headless session pays roughly a
dollar of context before working, so `max_budget_usd` below `2` fails on trivial plans; real plans
want `10` to `25`. `result.json` carries `total_cost_usd`, `num_turns`, and `is_error`; a clean
exit with `is_error: true` is recorded as a failure.

Task shape:

```json
{"id": "refactor-auth", "cmd": "", "image": "avireddy0/claude-executor:latest",
 "resource_profile": "standard", "timeout_seconds": 1800,
 "inputs": {"repo_url": "https://github.com/Envision-Construction/Envision-MCP.git",
            "repo_branch": "main", "plan_path": ".planning/phases/03/03-02-PLAN.md",
            "max_budget_usd": "15"}}
```

Commits land on `gke-dispatch/<wave_id>/<task_id>`. Open PRs from those branches yourself, or
merge them in a conductor step; the dispatcher never merges into `main`. Image contents, the
auth flow, the rebuild procedure, and a smoke test: `references/executor-image.md`.

## GSD phases and roadmaps

`run_roadmap.py` runs a whole milestone: phases in dependency batches, waves inside a phase in
parallel, state checkpointed to `gs://…/roadmaps/<roadmap_id>/state.json`.

From a GSD planning directory (every plan becomes an executor task):

```bash
python3 run_roadmap.py --planning-dir ~/GitHub/Envision-MCP/.planning --dry-run   # inspect batches
python3 run_roadmap.py --planning-dir ~/GitHub/Envision-MCP/.planning --auto      # run unattended
```

It reads each plan's frontmatter the way gsd-core does: `wave:` decides the wave, plans in one
wave that share `files_modified:` split into sequential sub-waves, and `files_modified` across
phases decides which phases may run concurrently. Phases with a `SUMMARY.md` are skipped. A
plan's `depends_on` naming plans in earlier waves or phases becomes a branch merge: the executor
fetches each dependency's `gke-dispatch/<wave_id>/<task_id>` branch and merges it before the plan
runs, so later waves build on earlier work instead of the tree pinned at kickoff. `files_modified`
overlap only *orders* phases; a plan that must build on a previous phase's code needs
`depends_on` as well, or it runs on the kickoff tree. Plan tasks default to 1800 s, 15 USD, 2
retries; a roadmap JSON overrides them per task.
Planning-dir mode has **no verification gate** (PLAN.md has no verification command) and says so
at startup; when phases must gate on tests, author a roadmap JSON instead:
`references/multi-phase-milestone.md`.

Resume after an interrupt or a failed phase:

```bash
python3 run_roadmap.py --resume gs://gke-dispatch-claude-mcp-457317/roadmaps/<roadmap_id>/state.json
```

gsd-core's own `execute-phase` runs the same wave law in-session with subagents. Use it when the
phase should run here; use this skill when the phase should run on the cluster, unattended, with
GCS as the audit trail.

## Retry and resume

- **Re-run `dispatch.py` with the same manifest.** Completed tasks stay completed, whether the
  GCS manifest or the one you pass says so. Failed tasks in either copy reset to pending. Before
  applying, the dispatcher reads each pending task's `result.json`: an exit-0 result is adopted as
  completed (the pod finished after `collect.py` gave up), a failed one is moved to
  `result.prev-<timestamp>.json` so neither the pod's guard nor `collect.py` mistakes it for the
  new outcome. `--dry-run` reports what it would adopt or archive and touches nothing.
- **In-pod guard.** Both templates skip a task whose `result.json` already shows exit 0; the
  executor entrypoint checks before cloning, so a re-applied Job or a late resume spends no budget.
- **`collect.py` timed out** with tasks still pending: the pods may still be running. Re-run
  `collect.py` later with the same manifest, or re-run `dispatch.py`, which adopts finished results.
- **Roadmap halted**: the printed `--resume` command (with `--auto` when the run was unattended)
  skips completed waves and phases.
- **A wave in the bucket you did not dispatch this session**: `gcloud storage cat
  gs://gke-dispatch-claude-mcp-457317/waves/<wave_id>/manifest.json` is the state.

## What the guarantees are (and are not)

| Guarantee | Mechanism |
|---|---|
| No silently dropped task | every task is in the manifest; `collect.py` marks the wave `partial_failure`/`failed` at timeout instead of reporting success |
| Output capture | indexed jobs: a `log-shipper` sidecar copies logs, `result.json`, and `/outputs` to GCS; executor jobs: the entrypoint uploads them itself |
| Idempotent replay | `wave_id` merge in `dispatch.py`, result reconciliation (adopt exit 0, archive failures), and the in-pod exit-0 check in both templates |
| Atomic results | `result.json` written to `.tmp` then `gsutil mv` |
| Crash recovery | manifest and roadmap state live in GCS; re-run with the same ids |

Not provided, despite earlier drafts of this skill claiming them: automatic resource-profile
escalation on OOM (a task retries with the same profile up to `retries`), retry-with-backoff on
GCS uploads (a failed upload is logged and skipped), a pre-warmed pod pool (`mode: pod-pool` is
accepted and ignored), and any merge of executor branches into `main`.

## Which dispatch path

| Work | Path |
|---|---|
| Arbitrary containers or Claude plans, parallel, resumable | this skill |
| A named Envision-MCP compute skill (`test_runner`, `parallel_grep`, `code_analysis`, `document_search`, …) | `dispatch_heavy_job` on the Envision-MCP gateway |
| A GSD phase to run in this session | `/gsd-execute-phase` |
| A batch longer than ~5 hours, a red-team panel, a sweep | Cloud Run jobs |

Details and the `dispatch_heavy_job` call shape: `references/envision-mcp-integration.md`.

## References

- `references/manifest-schema.md`: full manifest JSON, validation rules, the same-wave
  `depends_on` contract, status transitions.
- `references/multi-phase-milestone.md`: roadmap JSON authoring, phase batching, annotated
  three-phase skeleton, anti-patterns.
- `references/executor-image.md`: image contents, auth flow, input/output contract, budget
  floor, rebuild and smoke test.
- `references/cluster-setup.md`: live cluster facts, node pools, error-driven remediation.
- `references/envision-mcp-integration.md`: choosing between this skill, `dispatch_heavy_job`,
  and gsd-core.

Tests: `uv run --with pytest --with pyyaml python -m pytest tests -q` from the skill directory
(113 tests; pure functions, no cluster access). The generated Job shapes were validated with
`kubectl apply --dry-run=server` against envision-compute on 2026-09-03.
