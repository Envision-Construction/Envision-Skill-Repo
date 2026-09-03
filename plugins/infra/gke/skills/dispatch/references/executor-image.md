# Claude Executor Image

`us-central1-docker.pkg.dev/claude-mcp-457317/envision/claude-executor:20260903` runs one GSD plan (or one shell command) per pod as a headless
Claude Code session, then pushes the resulting commits to a branch. Read this before dispatching
executor tasks, before touching `docker/`, or when an executor pod fails at startup.

## Contents (`docker/Dockerfile`)

- `node:20-slim` base; `git`, `curl`, `jq`, `openssh-client`, `python3` + `PyJWT`/`cryptography`,
  Google Cloud CLI (`gsutil`, `gcloud`).
- Claude Code CLI installed at **build time** via `claude.ai/install.sh`. The CLI version is
  frozen into the image; so is `entrypoint.sh`. Editing `docker/` in this repo changes nothing on
  the cluster until the image is rebuilt and pushed.
- Non-root user `executor` (uid 1001), workdir `/workspace`.

## Current image (built and smoke-tested 2026-09-03)

`us-central1-docker.pkg.dev/claude-mcp-457317/envision/claude-executor:20260903` was built by Cloud Build
(build `9d6f9bee`, 3m55s) from this `docker/` directory and carries the entrypoint described here.
The cluster's node service account pulls it through its `artifactregistry.reader` role; no image
pull secret exists or is needed. Docker Hub `us-central1-docker.pkg.dev/claude-mcp-457317/envision/claude-executor:20260903` (pushed 2026-05-08)
is the previous build: it still passes `--max-turns`, which the CLI rejects, and writes no
`is_error`/cost fields. Do not use it.

## Auth flow (what actually runs)

1. Init container `fetch-secrets` (`google/cloud-sdk:slim`) runs
   `gcloud secrets versions access latest --secret=gsd-claude-oauth-token` and
   `--secret=gsd-github-app-private-key` in project `claude-mcp-457317`, writing them into an
   `emptyDir` at `/var/secrets/`. It authenticates through Workload Identity: KSA
   `gke-dispatch-worker` (namespace `gke-dispatch`, cluster `envision-compute`) is bound to GSA
   `gke-dispatch-sa@claude-mcp-457317.iam.gserviceaccount.com`.
2. `entrypoint.sh` exports `CLAUDE_CODE_OAUTH_TOKEN` from `/var/secrets/claude-oauth-token`.
3. `generate_github_token.py` mints a 10-minute JWT for GitHub App **3604031**, exchanges it for an
   installation token on org `Envision-Construction`, and configures `git` to use it for
   `https://github.com/` URLs. Multi-repo push works without a PAT.

The SecretProviderClass `gke-dispatch-secrets` still exists in the namespace from the earlier CSI
design. Nothing mounts it; the init-container path above is the live mechanism.

Secret Manager inventory: `gsd-claude-oauth-token` (from `claude setup-token`, a one-year
`sk-ant-oat01` token), `gsd-github-app-private-key`, `gsd-github-app-id` (unused; the ID is a
constant in `job_templates.py`).

## Input contract

Env set by `job_templates.build_executor_job`:

| Env | Source | Meaning |
|---|---|---|
| `WAVE_ID`, `TASK_ID`, `GCS_BUCKET` | dispatcher | Locate `inputs/<task>.json` and `outputs/<task>/` |
| `REPO_URL`, `REPO_BRANCH`, `GIT_SHA` | `inputs.repo_url` etc. | Clone target; `GIT_SHA` pins the checkout |
| `PLAN_PATH` | `inputs.plan_path` | Path inside the cloned repo |
| `TASK_CMD` | `task.cmd` | Shell fallback when no plan resolves |
| `MAX_BUDGET_USD` | `inputs.max_budget_usd` (default `5`) | `--max-budget-usd` for the headless session |
| `DEP_BRANCHES_FILE` | fixed | Written by `wait-deps` from same-wave `depends_on` (polled) and `inputs.merge_branches` (earlier waves, written directly) |

Before cloning, the entrypoint checks `outputs/<task_id>/result.json`; a prior exit-0 result means
the task already ran (a re-applied Job, or a resume after `collect.py` timed out) and the pod
exits 0 without spending budget. `dispatch.py` archives failed results before re-dispatching, so
this guard never blocks a retry.

Prompt resolution order: `PLAN_PATH` file in the clone; `plan_content` from `inputs/<task>.json`;
`plan_path` from that JSON; else `TASK_CMD` (or `cmd` from the JSON) runs via `eval`. With no
resolvable work the pod exits 1 with `FATAL: No task command resolved`.

Budget floor: the container has no CLAUDE.md, rules, or MCP servers, so the per-turn context is
small; the 2026-09-03 smoke test (one turn, no repo) cost 0.048 USD. The ~1 USD floor measured in
local headless sessions (2026-06-28, ~76K input tokens of system prompt and tool definitions) does
not apply. A budget that runs out ends the run with `subtype: error_max_budget_usd`; default `5`
is fine for smoke tests and small fixes, real plans usually want `10` to `25`.

## Output contract

Uploaded to `gs://<bucket>/waves/<wave_id>/outputs/<task_id>/`:

- `result.json`: `exit_code`, `duration_seconds`, `timestamp`, `git_commits` (last 10 subjects),
  `repo_branch`, `head_sha`, and from the Claude envelope `is_error`, `claude_subtype`,
  `total_cost_usd`, `num_turns`, `session_id`. `exit_code` is forced to 1 when the CLI exited 0
  but reported `is_error: true` (budget exhausted, refusal, tool failure).
- `stdout.log`: Claude's final `result` text only. `stderr.log`: CLI stderr.
- `artifacts/claude.json`: the raw `--output-format json` envelope, for forensics.

Git: uncommitted changes are auto-committed as `[gke-dispatch] <wave>/<task>: auto-commit remaining
changes`, then the branch `gke-dispatch/<wave_id>/<task_id>` is pushed with `--force-with-lease`.
**Nothing merges automatically.** Open PRs from those branches, or merge them in a conductor step.
Dependencies are the one automatic merge: for same-wave `depends_on`, `wait-deps` blocks until
each dependency's `result.json` shows `exit_code: 0`; for `inputs.merge_branches` (earlier waves,
resolved by `run_roadmap.py`) it writes the branches immediately. The entrypoint then fetches and
merges every recorded `origin/gke-dispatch/<wave_id>/<task_id>` before the plan runs; a merge
conflict is fatal for that task.

## Rebuilding

The image is `linux/amd64`. On this Mac `docker` is a shim over Apple `container`, so a local
build needs `--arch amd64`; Cloud Build avoids the cross-arch step entirely. The Cloud Build path
produced the current image on 2026-09-03; the local path has not been exercised.

Cloud Build into Artifact Registry (preferred, no local Docker Hub login):

```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/dispatch/docker
gcloud builds submit --project claude-mcp-457317 --region us-central1 \
  --tag us-central1-docker.pkg.dev/claude-mcp-457317/envision/claude-executor:$(date +%Y%m%d) .
```

Then point tasks at the new reference: the default in `run_roadmap.py`, the ground-truth row in
`SKILL.md`, and the examples in `multi-phase-milestone.md`. Pin by digest for any wave that must
be reproducible.

Local via Apple `container` (pushes to Docker Hub; only if Cloud Build is unavailable):

```bash
container build --arch amd64 -t avireddy0/claude-executor:$(date +%Y%m%d) docker/
container image push avireddy0/claude-executor:$(date +%Y%m%d)
```

## Smoke test after a rebuild

One task, tiny budget, no repo. The plan body must look like a plan: the entrypoint prefixes every
prompt with "Execute this plan precisely. Commit each change atomically. Do not skip any step.",
and on 2026-09-03 a one-line body ("Reply with exactly: EXECUTOR OK. Do nothing else.") came back
as "No plan was included in your message" with exit 0 and `is_error: false`. The pod, the
envelope parsing, and `collect.py` all reported success; only `stdout.log` showed the miss.

```bash
python3 scripts/normalize_wave.py --wave-id "executor-smoke-$(date +%s)" --framework custom \
  --tasks '[{"id":"smoke","cmd":"","image":"<new image ref>","timeout_seconds":900,
            "inputs":{"plan_content":"# Plan: executor smoke test\n\nThere is no repository and nothing to commit.\n\n## Step 1\nReply with exactly this text and nothing else: EXECUTOR OK","max_budget_usd":"3"}}]' \
  --output /tmp/smoke.json
python3 scripts/dispatch.py --manifest /tmp/smoke.json
python3 scripts/collect.py --manifest /tmp/smoke.json --timeout 900
```

Pass criteria, all three: `result.json` has `is_error: false` and a numeric `total_cost_usd`, AND
`stdout.log` (Claude's final text; the full envelope is `artifacts/claude.json`) contains
`EXECUTOR OK`. The first two alone are not proof (see above). Verified 2026-09-03 on the current
image: `EXECUTOR OK`, 0.021 USD, one turn, 4 s in the pod, 70 s from apply to result with a spot
node already warm; a cold scale-up adds 2 to 5 minutes (executor pods pin to spot nodes; see
`cluster-setup.md`).
