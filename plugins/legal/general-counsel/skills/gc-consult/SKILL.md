---
name: gc-consult
description: "Run a grounded GC consult: jurisdiction and posture first, 3+ specialist lenses, every load-bearing authority verified against a live primary source, then a conclusion-first memo under the house posture with verdict, ranked ANGLES, priced exposure, PE-framed next actions with a fallback ladder, and an authority index. Use before any hearing, deadline, filing decision, or strategy call. Triggers on 'run a consult', 'GC consult on X', 'what's our strategy for the hearing', 'what are our options before <deadline>', 'analyze our position in <matter>', 'we just got a letter from their lawyer', 'forensic consult'. Not for attacking a consult that already exists: that is gc-redteam, which runs after this one and before anyone acts on it."
---

# gc-consult: the deterministic consult pathway

> **Freshness:** class=`tool-surface` verified=2026-07-25 sources=live envision-mcp tool registry (`legal_consult` present, parameters question + jurisdictions; the gateway search/get_schema discovery layer does not index it)

Binding contracts: [`../_shared/zero-fabrication.md`](../_shared/zero-fabrication.md),
[`../_shared/posture.md`](../_shared/posture.md) (the house posture: deal counsel to
a sponsor, ANGLES after the holding, every exposure priced, four-item floor
surfaced only in LIMITATIONS), and
[`../_shared/output-format.md`](../_shared/output-format.md). Never fabricate
an authority: a fabricated citation that reaches a filed document is a
sanctionable event, and "not found" is an acceptable answer. Anything
unverifiable is labeled "ASSUMPTION (unverified)", never asserted.

Execute the four steps below in order. Each step's outcome dictates the next, so
there are no sequencing judgment calls.


## STEP 0 — matter workspace gate (uniform across the lifecycle)

Before anything else: if this work concerns a matter and no
`matters/<slug>-<docket>/` workspace exists for it, STOP and run
`gc-new-matter` first (same folder contract, same privilege headers, same
PENDING/Matters Dropbox placement — one cadence for the whole chain). When
the workspace exists, append this skill's artifact path to `lifecycle.consults` in the matter's `matter.json` (schema `gc-matter/v1`,
emitted by gc-new-matter) in the same edit that writes the artifact.

## Freshness

`class` selects the staleness threshold from the central table in
[`scripts/check_authority_freshness.py`](../../../scripts/check_authority_freshness.py);
the number is deliberately not written here, so changing it is one edit and no
two files can disagree about it. Past the threshold, treat the header as a lead
rather than an authority: re-verify the gateway contract before relying on it,
and record the stale header and its date in LIMITATIONS. Update `verified` only
after an actual check against the live source. A date nobody earned is upstream
of every fabricated citation this suite exists to prevent, because it is what
stops the next reader from checking. Run
`python3 scripts/check_authority_freshness.py` from the general-counsel repo for
the whole suite's status; the script and the link to it above live in that repo,
not in an installed copy of the plugin.

Two rules hold no matter how fresh the header is:

- Never compute a controlling date from a snapshot. Any date a party will rely
  on (answer due, notice served by, deadline to file) comes from the statute or
  rule text pulled that day. A missed deadline cannot be un-missed.
- Never quote an indexed or periodically adjusted figure (filing fees, statutory
  interest, penalty amounts, dollar caps) from memory or from a reference file.
  A snapshot value can be wrong while every sentence around it is right, so pull
  the current official publication at each use.

## STEP 1: jurisdiction and posture

Establish forum, governing law, procedural posture, and controlling dates before
any substantive work. No silent defaults. In a matter repo, read the matter's
`00-*` anchor doc first. Carry these four facts into every later step.

Controlling dates come from the current statute or rule text pulled that day,
and the pull is recorded next to the date.

Facts drawn from correspondence (email, Slack, Drive, meeting transcripts) carry
their provenance at the point of use: message id, date, sender. A quoted email
with no id is an unverified assertion, not evidence. Retrieve when the question
needs the record; do not sweep a mailbox because the tools are there.

## STEP 2: call the deployed service (`/consult-legal` path)

Call the `legal_consult` gateway tool (envision-mcp) with the question verbatim
plus the jurisdictions from STEP 1. This is the deployed General Counsel
service, the productionized descendant of the org `/consult-legal` skill
(prompts ported 2026-06-10), running classify, then 9-specialist fan-out, then
Opus synthesis with deterministic authority validation.

### `legal_consult` outcome table (exactly one row applies)

| Gateway result | Next action |
|---|---|
| Structured answer (200) | Go to STEP 4 with the returned `{answer, authorities, jurisdictions, assumptions, limitations}`. Re-verify the authorities the recommendation actually rests on before delivering. If `answer` carries no ANGLES section after the holding, the deployed image predates the house posture: record that in LIMITATIONS and supply the angles from an in-session dispatch (STEP 3) before delivering, never by patching the service's memo by hand. |
| "unknown tool" / "unknown parameter" | Skill staleness: the gateway contract changed under this file. Surface the error to the user verbatim and stop. A silent fallback hides that this skill is out of date, so the next session repeats the failure. |
| 503 or `GC_BACKEND_UNAVAILABLE` | Service outage (capacity gating; general-counsel repo `docs/INFERENCE-RUNBOOK.md`). Go to STEP 3. |
| Call denied or blocked before it reaches the service (local permission mode, MCP server not connected) | Record "gateway unreachable in this environment" in LIMITATIONS. Go to STEP 3. |
| User asked for in-session, interactive, or document-review work | Skip the gateway and go to STEP 3. |

## STEP 3: dispatch the general-counsel orchestrator

Dispatch one agent: `general-counsel:general-counsel` (this plugin's supervisor).
Its prompt carries, in this order: (a) the question verbatim, (b) jurisdictions,
(c) procedural posture and controlling dates from STEP 1, (d) any matter-file
facts the specialists need, each with its provenance.

The supervisor's STEP 4 is the other half of this handoff: it relays (a) through
(d) onward to each specialist unchanged and appends its own return instruction.
It does not re-derive them, so the two lists stay in the same order. Anything you
omit here reaches no specialist.

The supervisor selects 3 to 5 specialist lenses from the routing table, taps this
plugin's bundled insurance-specialist agents when captive, coverage, or
premium-finance issues are present, fans out in parallel, synthesizes, and
returns the full memo (VERDICT, ANGLES merged across lenses and ranked,
per-lens analysis, PRICED EXPOSURE, NEXT ACTIONS as the sequenced play closing
with the fallback ladder, LIMITATIONS, AUTHORITY INDEX) opening with the method
line. Do not re-run its work. Verify its method-line counts are real
numbers before delivering: a consult that claims verification it did not do is
the failure this pathway exists to prevent.

For single-lens document review or interactive drafting, dispatch the one
matching `general-counsel:legal-<area>` agent directly instead of the supervisor.

## STEP 4: frame the recommendation, then deliver

### House posture, then PE-executive framing (every consult)

The house posture (`../_shared/posture.md`) governs everything downstream of the
verdict: angles, exposure pricing, recommendation, sequence. Before delivering,
confirm the memo carries it: ANGLES ranked right after the holding, every
exposure priced with its survival structure, no banned hedge, any floor hit as
one line in LIMITATIONS only. A memo missing any of those goes back to STEP 3,
not to the user.

Then frame the recommendation and NEXT ACTIONS as a PE-executive decision. This
is standing, not reserved for business or transactional questions: the reader
runs a portfolio company and decides under the same pressures every time,
whether the question is a lien deadline or an entity election.

Invoke `Skill(pe-executive:pe-executive-mindset)` for the lens vocabulary. If
that plugin is not installed, apply the pressures and lenses named here and
record "PE framing applied without the pe-executive plugin" in LIMITATIONS.
Degrade, do not skip.

- **The four pressures**: exit clock, equity incentive, leverage constraint,
  replacement threat.
- **The decision lenses**: EBITDA impact, time to value, cash-flow effect,
  measurability, risk to the base, exit narrative.

Two guardrails, both load-bearing:

- **Illustrative only.** The GC holds no financial data on Envision. Every
  PE-framed statement opens with the literal token `illustrative:` and is
  framework-typical, never asserted as an Envision-specific figure. That token is
  what the deployed service's `pe_lens` already enforces, so the in-session frame
  and the service frame read the same way.
- **No legal citation inside the frame.** Authority belongs in the analysis and
  the AUTHORITY INDEX. A case or statute quoted inside the PE frame reads as
  legal grounding for a business judgment, which is the confusion the split
  exists to prevent.

The verdict is the law as verified and is never bent to fit either frame.
Neither the posture nor the PE frame is the reason to do something the verified
analysis says is unavailable; when they point at a closed door, the memo names
the adjacent open one and proceeds through it.

### Deliver

- **In a matter repo** (a repo with a `matters/` tree): write the memo as
  `CONSULT-<YYYY-MM-DD>.md` in the matter folder with the matter's privilege
  header, then surface the VERDICT in the response.
- **Anywhere else**: deliver the memo in the response, or to a path the user
  names.

Every delivery opens with the method line, with real counts, or it is not done:

> Method: multi-specialist consult (GC service pattern: grounding →
> N specialists → adversarial verification). **N findings verified against live
> primary sources** (name the source classes); **N load-bearing claims
> adversarially checked; N corrected.** Not legal advice; for review by
> retained counsel.

## Matter lifecycle

The chain runs in this order: `gc-new-matter` scaffolds, this skill runs the
consult, `gc-redteam` attacks the result before anyone acts on it, anything that
will be filed or served goes through `gc-authorities-log`, then
`gc-file-and-serve` executes. A memo that reaches a matter folder without a
`gc-redteam` pass has skipped the only adversarial check in the chain.

This skill ships with the plugin and loads wherever the plugin is installed. The
other four are repo-local to the general-counsel repo, where the privileged
`matters/` tree lives. Outside that repo those four do not load and matter
artifacts are out of scope: say so rather than improvising a folder.

Retrieved correspondence is privileged work product. It lives in the matter tree,
which is untracked, and never in git-backed memory, a commit message, or any
tracked file.

Matter packages exported out of the repo follow one mandatory placement rule,
organized by law firm. Read it at its canonical location and do not restate it
here, because a second copy is how the rule drifts:
[`skills/gc-new-matter/SKILL.md`, section "Dropbox export placement"](../../../skills/gc-new-matter/SKILL.md#dropbox-export-placement-mandatory)
(that relative path resolves inside the general-counsel repo).
