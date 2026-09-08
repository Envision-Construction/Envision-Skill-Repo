# general-counsel plugin

Envision/Prometheus legal intelligence as a Claude Code plugin: 11 skills
(9 `legal-<area>` specialists + `gc-consult` + the `insurance-specialist`
forensic research orchestrator) and 14 agents (9 specialists + the 4-agent
`insurance-*` suite + the `general-counsel` supervisor), all bound by the
zero-fabrication contract in `skills/_shared/`.

## Install (this machine)

```
/plugin marketplace add Envision-Construction/Envision-Skill-Repo
/plugin install general-counsel@envision-skill-repo
```

Skills invoke namespaced: `/general-counsel:gc-consult`,
`/general-counsel:legal-cre`, … Agents dispatch as
`general-counsel:legal-<area>`.

## Update flow

This plugin is distributed through the org registry, not from this repo
directly. The installed copy is `general-counsel@envision-skill-repo`, pulled
from GitHub (`Envision-Construction/Envision-Skill-Repo`, marketplace entry
`./plugins/legal/general-counsel`) into `~/.claude/plugins/cache/`. An edit
here reaches a session only after all four steps:

1. Mirror this tree into the registry clone:
   `rsync -a --delete --exclude __pycache__ plugin/ ~/GitHub/Envision-Skill-Repo/plugins/legal/general-counsel/`
2. Bump the version in BOTH `plugin/.claude-plugin/plugin.json` and the
   registry's `.claude-plugin/marketplace.json` general-counsel entry. They
   must agree: `claude plugin validate ~/GitHub/Envision-Skill-Repo`.
3. Commit and push the registry.
4. `claude plugin marketplace update envision-skill-repo`, then
   `claude plugin update general-counsel@envision-skill-repo`, then restart.

The registry copy went stale from 2026-07-25 to 2026-09-08 because step 1 was
skipped; sessions ran six-week-old prompts while this tree moved on. For
iteration without the registry round-trip, `claude --plugin-dir ./plugin`
loads this tree directly. The 2026-07-04 `gc-marketplace` local-path install
that resolved `${CLAUDE_PLUGIN_ROOT}` to this repo live was removed on
2026-07-25 and no longer exists.

## The three-consumer contract

`plugin/skills/` is the single source of truth for:

1. **The deployed Cloud Run service** — `app/agents/prompts.py` assembles
   production prompts from `_shared/*.md` + `legal-*/references/domain.md` at
   import. **Editing those files edits PRODUCTION prompts** — run
   `python scripts/snapshot_prompts.py` + `pytest tests/test_prompt_fidelity.py`
   after intentional changes.
2. **This plugin** (org-wide sessions) — SKILL.md wrappers + agents read the
   same references at runtime.
3. **In-repo sessions** — matter-lifecycle skills (`gc-new-matter`,
   `gc-redteam`, `gc-authorities-log`, `gc-file-and-serve`) stay repo-local in
   `../skills/` next to privileged `matters/` work product, which is never
   distributed with this plugin.

`_shared/posture.md` (house posture) is a fourth snapshot-gated shared block, beside `zero-fabrication.md`, `output-format.md`, and `supervisor.md`; every prompt surface above inherits it.

## Consult routing (deterministic)

`gc-consult` is a fixed 4-step pathway: (1) jurisdiction/posture, (2) the
`legal_consult` gateway tool — the deployed `/consult-legal` service — with an
explicit outcome table, (3) on outage or interactive work, dispatch the
`general-counsel:general-counsel` supervisor agent, which routes 3–5 specialist
lenses from `_shared/supervisor.md` and taps the bundled `insurance-*` agents
for captive/coverage/premium-finance questions, (4) deliver (matter repo →
privileged CONSULT file; elsewhere → in-response memo). Single-lens doc review
goes straight to the matching `legal-<area>` agent.

## Insurance suite provenance

`skills/insurance-specialist/` + `agents/insurance-*.md` were bundled
2026-07-21 (v1.2.0) from `claude-code-memory/global/{skills,agents}` so the
supervisor's insurance tap works on every machine the plugin reaches, not just
this one. **The plugin copy is canonical from v1.2.0 on** (paths rewritten to
`${CLAUDE_PLUGIN_ROOT}`, dispatch names namespaced `general-counsel:`); retire
or freeze the claude-code-memory copy rather than editing both.
