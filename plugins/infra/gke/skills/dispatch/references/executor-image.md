# Claude Executor Image

`avireddy0/claude-executor:latest` runs one GSD plan (or one shell command) per pod as a headless
Claude Code session, then pushes the resulting commits to a branch. Read this before dispatching
executor tasks, before touching `docker/`, or when an executor pod fails at startup.

## Contents (`docker/Dockerfile`)

- `node:20-slim` base; `git`, `curl`, `jq`, `openssh-client`, `python3` + `PyJWT`/`cryptography`,
  Google Cloud CLI (`gsutil`, `gcloud`).
- Claude Code CLI installed at **build time** via `claude.ai/install.sh`. The CLI version is
  frozen into the image; so is `entrypoint.sh`. Editing `docker/` in this repo changes nothing on
  the cluster until the image is rebuilt and pushed.
- Non-root user `executor` (uid 1001), workdir `/workspace`.

## Image staleness (verified 2026-09-03)

Docker Hub `avireddy0/claude-executor:latest` was last pushed **2026-05-08**. It carries the May
entrypoint (`claude -p --max-turns`) and a May CLI. The entrypoint in this repo now uses
`--max-budget-usd` and `--output-format json`, so the next executor wave needs a rebuild first.
Until then, executor tasks run the old contract: no `is_error`/cost fields in `result.json`, and
`MAX_BUDGET_USD` is ignored.

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
| `DEP_BRANCHES_FILE` | fixed | Written by `wait-deps` when `depends_on` is set |

Prompt resolution order: `PLAN_PATH` file in the clone; `plan_content` from `inputs/<task>.json`;
`plan_path` from that JSON; else `TASK_CMD` (or `cmd` from the JSON) runs via `eval`. With no
resolvable work the pod exits 1 with `FATAL: No task command resolved`.

Budget floor: a headless session inherits the full system prompt and MCP tool definitions, which
costs on the order of a dollar before any work happens (measured 2026-06-28, ~76K input tokens).
Budgets under `2` fail on trivial plans with `subtype: error_max_budget_usd`. Default `5` is the
minimum sensible; real plans usually want `10`–`25`.

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
Same-wave `depends_on` is the one automatic merge: `wait-deps` blocks until each dependency's
`result.json` shows `exit_code: 0`, then the entrypoint fetches and merges
`origin/gke-dispatch/<wave_id>/<dep_id>` before the plan runs.

## Rebuilding

The image is `linux/amd64`. On this Mac `docker` is a shim over Apple `container`, so a local
build needs `--arch amd64`; Cloud Build avoids the cross-arch step entirely. Neither path was
exercised in the 2026-09-03 upgrade; treat the commands as the shape, not as verified output.

Cloud Build into Artifact Registry (preferred, no local Docker Hub login):

```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/dispatch/docker
gcloud builds submit --project claude-mcp-457317 \
  --tag us-central1-docker.pkg.dev/claude-mcp-457317/<ar-repo>/claude-executor:$(date +%Y%m%d) .
```

Then point tasks at the new reference (and update the default in `run_roadmap.py`). Pin by digest
for any wave that must be reproducible.

Local via Apple `container` (needs a Docker Hub login):

```bash
container build --arch amd64 -t avireddy0/claude-executor:$(date +%Y%m%d) docker/
container image push avireddy0/claude-executor:$(date +%Y%m%d)
```

## Smoke test after a rebuild

One task, tiny budget, no repo:

```bash
python3 scripts/normalize_wave.py --wave-id "executor-smoke-$(date +%s)" --framework custom \
  --tasks '[{"id":"smoke","cmd":"","image":"<new image ref>","timeout_seconds":900,
            "inputs":{"plan_content":"Reply with exactly: EXECUTOR OK. Do nothing else.","max_budget_usd":"3"}}]' \
  --output /tmp/smoke.json
python3 scripts/dispatch.py --manifest /tmp/smoke.json
python3 scripts/collect.py --manifest /tmp/smoke.json --timeout 900
```

Pass criteria: `result.json` has `is_error: false` and a numeric `total_cost_usd`; `stdout.log`
contains `EXECUTOR OK`. Expect a few minutes of node scale-up before the pod starts (executor pods
pin to spot nodes; see `cluster-setup.md`).
