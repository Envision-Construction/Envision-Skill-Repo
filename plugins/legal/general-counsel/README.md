# general-counsel plugin

Envision/Prometheus legal intelligence as a Claude Code plugin: 11 skills
(9 `legal-<area>` specialists + `gc-consult` + the `insurance-specialist`
forensic research orchestrator) and 14 agents (9 specialists + the 4-agent
`insurance-*` suite + the `general-counsel` supervisor), all bound by the
zero-fabrication contract in `skills/_shared/`.

## Install (this machine)

```
/plugin marketplace add /Users/avireddy/GitHub/general-counsel
/plugin install general-counsel@gc-marketplace
```

Skills invoke namespaced: `/general-counsel:gc-consult`,
`/general-counsel:legal-cre`, … Agents dispatch as
`general-counsel:legal-<area>`.

## Update flow

Local-path marketplace installs (this machine) resolve `${CLAUDE_PLUGIN_ROOT}`
to THIS repo's `plugin/` at runtime — skill/agent edits propagate live to new
sessions (verified 2026-07-04: a dispatched agent read
`~/GitHub/general-counsel/plugin/skills/.../references/domain.md`, not the
cache copy). A cache copy also exists under `~/.claude/plugins/cache/`; after
structural changes (new skills/agents, manifest edits) refresh it:

```
/plugin marketplace update gc-marketplace
/plugin update general-counsel@gc-marketplace
```

Git-sourced installs (other machines) ARE cached copies and always need that
update flow. For one-off iteration: `claude --plugin-dir ./plugin`.

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
