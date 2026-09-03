# Multi-Phase Milestone Pattern

When a milestone spans several phases that must run in order with verification gates between
them, author one roadmap JSON and run it with `scripts/run_roadmap.py`. Phases run in sequential
batches; waves inside a phase run in parallel on GKE; one command runs the whole milestone.

## Roadmap JSON vs `--planning-dir` vs a single wave

| Use roadmap JSON | Use `--planning-dir .planning` | Use a single-wave manifest |
|---|---|---|
| Phases need a real `verification.cmd` gate | Plans already exist as `*-PLAN.md` with gsd-core frontmatter | One batch of independent tasks |
| Tasks are heterogeneous (shell + executor + GPU) | Every task is a Claude executor run of one plan | Ad-hoc task list |
| You want resume + dry-run for the whole milestone | You want the same, without authoring JSON | One-shot dispatch |

`--planning-dir` mode reads each plan's frontmatter: `wave:` decides the wave (plans in one
declared wave that share `files_modified` are split into sequential sub-waves, gsd-core's own
rule), `files_modified:` feeds phase batching, `depends_on:` drives branch merges (next section).
It has **no verification gate**: PLAN.md carries no verification command, so every phase's gate is
`{"cmd": null, "required": false}` and the run prints a warning saying so. Phases with a
`SUMMARY.md` are skipped as already done. Decimal phase directories (`91.1-...`) are supported.

## How phase ordering works

`run_roadmap.py` does not walk `phases[]` strictly in order. `group_phases_into_batches`
partitions phases into sequential batches; phases inside a batch run concurrently because their
`files_modified` sets are disjoint. Greedy, from `phases[0]`:

1. Start a batch with the next remaining phase; its files become the batch's claimed set.
2. Add each later remaining phase whose `files_modified` is disjoint from the claimed set.
3. Close the batch when nothing else fits; start the next one.
4. Batches run sequentially. The next batch waits for every phase in the prior batch to complete
   and for each required `verification.cmd` to pass.

`files_modified` is therefore load-bearing. A task without it claims nothing, so a phase of
such tasks is parallel-eligible with everything; forget it everywhere and all phases collapse into
one parallel batch. Declare it on every task of a multi-phase manifest.

## `depends_on`: same wave polls, earlier waves merge

`run_roadmap.py` resolves every executor task's `depends_on` before the wave is normalized:

- A dependency in the **same wave** stays a dependency. The `wait-deps` init container polls its
  `result.json`, fails the task if the dependency failed, and records its branch.
- A dependency in an **earlier wave or phase** becomes `inputs.merge_branches`: the branch
  `gke-dispatch/<that wave_id>/<task_id>` is written to the same file without polling, because
  that wave already finished.
- Either way the executor merges every recorded branch into its clone before the plan runs. That
  merge is the only automatic hand-off of code between tasks; without a dependency, a wave-2 pod
  works on the tree pinned at kickoff.
- A dependency on a task in the **same or a later wave** that is not in this wave is rejected
  with the offending id, and so is an unknown name. Dependencies must point backwards.

`depends_on` values may be task ids (`phase-41-01`) or bare plan numbers (`41-01`), matching
gsd-core plan frontmatter. Generic (Indexed Job) tasks ignore `depends_on` entirely. A manifest
you hand to `normalize_wave.py` yourself has no roadmap context, so there dependencies must be
same-wave ids; `dispatch.py` re-validates and rejects anything else.

## Annotated skeleton (3 phases)

```json
{
  "roadmap_id": "example-milestone",
  "phases": [
    {
      "id": "phase-A-bootstrap",
      "title": "Bootstrap shared infrastructure",
      "waves": [
        [
          {
            "id": "a-01",
            "cmd": "",
            "image": "avireddy0/claude-executor:latest",
            "resource_profile": "standard",
            "timeout_seconds": 1800,
            "inputs": {
              "repo_url": "https://github.com/Envision-Construction/Envision-MCP.git",
              "repo_branch": "main",
              "plan_path": ".planning/phases/A/A-01-PLAN.md",
              "max_budget_usd": "15"
            },
            "files_modified": ["config/settings.py"]
          }
        ]
      ],
      "verification": {"cmd": "cd repos/Envision-MCP && pytest tests/config -q", "required": true}
    },
    {
      "id": "phase-B-parallel-refactor",
      "title": "Per-service refactors, then the aggregator that depends on them",
      "waves": [
        [
          {"id": "b-01", "cmd": "", "image": "avireddy0/claude-executor:latest",
           "resource_profile": "standard", "timeout_seconds": 1800,
           "inputs": {"plan_path": ".planning/phases/B/B-01-PLAN.md",
                      "repo_url": "https://github.com/Envision-Construction/Envision-MCP.git",
                      "repo_branch": "main", "max_budget_usd": "15"},
           "files_modified": ["gateway/integrations/svc_a.py"]},
          {"id": "b-02", "cmd": "", "image": "avireddy0/claude-executor:latest",
           "resource_profile": "standard", "timeout_seconds": 1800,
           "inputs": {"plan_path": ".planning/phases/B/B-02-PLAN.md",
                      "repo_url": "https://github.com/Envision-Construction/Envision-MCP.git",
                      "repo_branch": "main", "max_budget_usd": "15"},
           "files_modified": ["gateway/integrations/svc_b.py"]},
          {"id": "b-03", "cmd": "", "image": "avireddy0/claude-executor:latest",
           "resource_profile": "standard", "timeout_seconds": 3600,
           "inputs": {"plan_path": ".planning/phases/B/B-03-PLAN.md",
                      "repo_url": "https://github.com/Envision-Construction/Envision-MCP.git",
                      "repo_branch": "main", "max_budget_usd": "20"},
           "depends_on": ["b-01", "b-02"],
           "files_modified": ["gateway/routers/aggregated.py"]}
        ]
      ],
      "verification": {"cmd": "cd repos/Envision-MCP && pytest tests/integrations -q", "required": true}
    },
    {
      "id": "phase-C-ml-retrain",
      "title": "Retrain intent classifier on new schema",
      "waves": [
        [
          {"id": "c-01", "cmd": "python retrain.py --epochs 20",
           "image": "avireddy0/intent-trainer:latest",
           "resource_profile": "gpu",
           "timeout_seconds": 3600,
           "inputs": {"dataset_uri": "gs://gke-dispatch-claude-mcp-457317/datasets/intent-v3.parquet"},
           "files_modified": ["models/intent/"]}
        ]
      ],
      "verification": {"cmd": "python verify_model.py --min-f1 0.85", "required": true}
    }
  ]
}
```

Notes:

- `phase-A`: one wave, one task; the minimum viable phase.
- `phase-B`: all three tasks in **one wave**. `b-01` and `b-02` start immediately; `b-03`'s pod
  waits in `wait-deps` until both have `exit_code: 0`, merges their branches, then runs. Putting
  `b-03` in a second wave with the same `depends_on` also works under `run_roadmap.py`: the
  dependencies resolve to branch merges and no polling is needed. Without `depends_on`, a
  second-wave `b-03` would run on the pre-`b-01` tree.
- Per-task `timeout_seconds`, `retries`, `resource_profile`, and nested `inputs`
  (`max_budget_usd`, `repo_url`, …) all pass through; omitted values default to 1800 s, 2 retries,
  `standard`, 15 USD.
- `phase-C`: a generic container task on `gpu` (one L4, spot). `gpu_high` is the H100 spot pool
  (quota 3 in us-central1); there is no A100 pool. Check quotas with `gcq us-central1 claude-mcp-457317 gpu`.
- `verification.cmd` runs in the dispatcher's working directory after the phase's last wave.
  `required: false` makes it advisory; `true` blocks the next batch on failure.
- Task ids are lowercase because they become Job names and branch names.

## Invocation matrix

```bash
# Dry run: print phase/wave/task plan, dispatch nothing, write nothing
python3 scripts/run_roadmap.py --roadmap roadmap.json --dry-run

# Interactive: pause between batches, "n" stops and saves resume state
python3 scripts/run_roadmap.py --roadmap roadmap.json

# Autonomous: no prompts, run to completion
python3 scripts/run_roadmap.py --roadmap roadmap.json --auto

# From a GSD planning dir (executor tasks only, no gates)
python3 scripts/run_roadmap.py --planning-dir .planning --dry-run
python3 scripts/run_roadmap.py --planning-dir .planning --auto

# Resume after interrupt or partial failure
python3 scripts/run_roadmap.py \
  --resume gs://gke-dispatch-claude-mcp-457317/roadmaps/<roadmap_id>/state.json
```

`--bucket` and `--namespace` default to the live values. `--resume` reuses each wave's `wave_id`
as its idempotency key: completed tasks skip, failed tasks reset to pending and re-dispatch.

## Prior example

`~/GitHub/central-command/.planning/milestones/v25.0-roadmap.json` (8 phases, 31 plans, 21 waves)
is the largest roadmap authored for this dispatcher. Its phase batching per `--dry-run`: phases
124, 125, 126 parallel (disjoint files), then 127 through 131 serial (all touch `gateway/`). 14 of
its 20 `depends_on` edges point at a task in an earlier wave; `run_roadmap.py` resolves those to
branch merges, so the file dispatches as written. The same JSON handed to `normalize_wave.py`
wave by wave would be rejected, because a lone wave has no roadmap context for the other ids.

## Anti-patterns

- **Forward `depends_on`** (a task in the same batch's later wave, or a later phase): rejected.
  Dependencies point backwards; ordering forwards comes from `wave:` and `files_modified`.
- **Tasks without `files_modified`**: every phase becomes parallel-eligible.
- **One giant wave with every task**: loses the gate between logical units.
- **`verification.required: false` everywhere**: the gate is ornamental; run the check or drop it.
- **`gpu` or `gpu_high` on non-GPU work**: ties up GPU spot capacity; `standard` already lands on
  a spot node.
- **Budgets under 2 USD on executor tasks**: the headless context floor eats them
  (`executor-image.md`).
- **`latest` image tags on a reproducibility-critical wave**: pin a digest.
