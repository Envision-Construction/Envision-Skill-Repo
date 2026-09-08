---
name: insurance-specialist
description: "Forensic insurance-industry research orchestrator with nested specialist agents covering captive formation, IRC 831(b) vs 831(a) elections and micro-captive enforcement (T.D. 10029 listed transactions and their current vacatur posture, Notice 2016-66 history, Avrahami and Reserve Mechanical case law), cell and rent-a-captive structures, captive domicile selection, coverage lapse and cancellation-notice law, and premium finance mechanics. Use this skill aggressively whenever the user mentions captives, 831(b), micro-captive, cell captive, protected cell, segregated portfolio, rent-a-captive, sponsored captive, captive domicile, captive feasibility, indication report, Atlas Insurance captive work, IRS captive enforcement or settlement, premium finance, IPFS, coverage lapse, policy cancellation, reinstatement, cancellation notice, certificate of insurance, or asks any insurance statute, regulation, or carrier-vs-finance-company question, even when they never say the word insurance. This skill owns the forensic research: deep 831(b) enforcement and case law, cell and domicile comparison, coverage-lapse timelines, premium finance. Captive formation, licensing, and ongoing captive regulatory compliance as a doctrine question go to legal-captive; entity and transactional tax goes to legal-tax."
---

# insurance-specialist: forensic research orchestrator

> **Freshness:** class=`legislation` verified=2026-07-04 sources=primary statute and regulation text, Federal Register and Treasury Decisions, IRS Rev. Procs. and guidance, court opinions (the ladder in workflows/legislation-refresh.md)

Binding contract: [`../_shared/zero-fabrication.md`](../_shared/zero-fabrication.md) and [`../_shared/posture.md`](../_shared/posture.md).
Never fabricate an authority: a fabricated citation that reaches a filed document
is a sanctionable event, and "not found" is an acceptable answer. Anything
unverifiable is labeled "ASSUMPTION (unverified)", never asserted.

This skill DOES bind to [`../_shared/output-format.md`](../_shared/output-format.md),
including its work-product disclaimer. The two contracts are compatible and were
briefly read as conflicting: output-format forbids only *generic* "consult an
attorney" hedging, which is not what a named escalation line is. This skill
additionally requires a per-deliverable escalation line naming the specific
professional and the specific step (election filing, opinion letter, regulator
submission, actuarial pricing). Where one deliverable mixes an insurance section
with a `legal-*` section, the shared disclaimer appears once at the end and the
named escalation line stays with the insurance section. A generic "consult an
attorney" sentence belongs in neither.

The disclaimer is not optional on an insurance-only deliverable. Dropping it
would ship analysis with no statement that licensed counsel must review it
before reliance, which is the one line that keeps work-product augmentation from
reading as advice.

## Purpose and framing contract

This skill produces **compliance-risk analysis** of insurance structures,
statutes, and broker proposals. Two commitments bind every output:

1. **Abuse patterns are documented so structures avoid them.** When analyzing IRC
   § 831(b) micro-captive exposure, the deliverable states how the IRS attacks a
   pattern and what a defensible structure shows instead, never "how to get away
   with it."
2. **Decision support, not legal or tax advice.** Every deliverable ends with an
   escalation line naming what requires licensed counsel or a credentialed
   actuary (election filings, opinion letters, regulator submissions, live
   disputes).

## Freshness and figures

`class` in the header above selects the staleness threshold from the central
table in
[`scripts/check_authority_freshness.py`](../../../scripts/check_authority_freshness.py);
the number is not written here so that changing it is one edit and no two files
can disagree about it. For this skill that threshold is the **90 days** already
governing `references/current-legislation.md`, which is where this convention
started. Past the threshold, or whenever the question concerns "current / latest"
legislation, treat the snapshot as a lead rather than an authority: re-run
[`workflows/legislation-refresh.md`](workflows/legislation-refresh.md) before
relying on it, label what you could not verify "ASSUMPTION (unverified)", and
record the stale header and its date in LIMITATIONS. The changelog at the bottom
of the snapshot persists across refreshes. Update `verified` only after actually
re-verifying against a live source: a date nobody earned is upstream of every
fabricated citation this suite exists to prevent, because it is what stops the
next reader from checking. `python3 scripts/check_authority_freshness.py` reports
the whole suite.

Each `references/*.md` carries its own header and its own class. A pointer from
one reference to another locates statute currency; it does not transfer freshness.

Two rules hold no matter how fresh a header is:

- **Indexed figures are never quoted from memory or from a reference file.** The
  831(b) premium cap, penalty amounts, premium-tax rates, and minimum-capital
  figures are re-verified from the current official publication on each use.
  Canonical procedure: `references/forensic-research-protocol.md` § 6.
- **Never compute a controlling date from a snapshot.** Any date a party will
  rely on (cure deadline, cancellation effective date, disclosure due date) comes
  from the statute or rule text pulled that day. A missed deadline cannot be
  un-missed.

## Nested specialists: dispatch map

Dispatch via the Agent tool. Each specialist reads its own reference file(s)
before answering; pass **local file paths, never pasted payloads**.

| Question type | Dispatch to | Reference base |
|---|---|---|
| Federal captive tax: 831(a)/(b) election, listed-transaction exposure, IRS enforcement, case law, 953(d) | `general-counsel:insurance-captive-tax` | `references/captive-formation-831b.md` |
| Entity structure: pure vs cell (PCC/ICC/SAC/SPC), rent-a-captive, sponsored, series LLC; domicile comparison | `general-counsel:insurance-captive-structures` | `references/cell-structures.md` |
| Coverage lapse, cancellation/reinstatement, notice statutes, premium finance, IPFS, COI questions | `general-counsel:insurance-coverage-counsel` | `references/coverage-lapse-law.md` + `references/premium-finance.md` |
| "Verify this cite / is this still good law / find the current statute text" | `general-counsel:insurance-statute-researcher` | `references/forensic-research-protocol.md` |
| Strategy, value creation, EBITDA/cash impact, exit posture | **main session** invokes `Skill(pe-executive:pe-executive-mindset)`, never delegated to a specialist | see the PE framing note below |

All four specialists are pinned `model: opus`. Each one's work is open-ended
enough (federal tax synthesis, cross-domicile comparison, coverage-position
analysis, adversarial cite verification) that it must not degrade when this skill
is dispatched from a lighter session.

`legal_consult` (envision-mcp) may second-read a legal conclusion when available.
Treat it as a cross-check, not a dependency; if it is unreachable, say so in
LIMITATIONS and continue.

### PE-executive framing

Strategy questions are framed as a PE-executive decision, on the same terms the
rest of this suite uses. The canonical statement of the four pressures, the six
decision lenses, and the invocation is
[`gc-consult`, STEP 4](../gc-consult/SKILL.md); do not restate it here, because a
second copy is how the two drift apart. Three constraints carry into any
insurance deliverable:

- If the `pe-executive` plugin is absent, apply the framing from the pressures
  and lenses named in `gc-consult` and record the degradation in LIMITATIONS.
  Degrade, do not skip.
- **Illustrative only.** This skill holds no financial data on Envision. Every
  PE-framed statement opens with the literal token `illustrative:` and is
  framework-typical, never asserted as an Envision-specific figure.
- **No legal citation inside the frame.** Authority belongs in the analysis. The
  lens frames the recommendation; it never changes a conclusion about what the
  law says, and where the two point different directions the legal conclusion
  governs and the tension is stated.

## Forensic research protocol (digest)

Full method: [`references/forensic-research-protocol.md`](references/forensic-research-protocol.md).
Non-negotiables:

- Source hierarchy: official statute/reg text, then T.D.s and the Federal
  Register, then IRS guidance, then court opinions, then secondary analysis.
  Broker and promoter marketing is never load-bearing.
- Two independent sources for every load-bearing claim. Pinpoint cite plus
  canonical URL plus verified-on date, every time.
- Never fabricate: "not found" is the answer when a source does not exist.
  Distinguish repealed vs not-yet-effective vs not-found.
- Separate what a statute SAYS, what a structure DOES, and what a promoter
  CLAIMS. Collapsing the three is the core fabrication failure mode here.

One standing party-identification rule, because misidentifying it changes who
owes coverage and who gets sued: a premium finance company (IPFS / Imperial PFS
is the one in this record) lends the premium and holds a power of attorney to
cancel. It is not the carrier. Details and the party map:
[`references/premium-finance.md`](references/premium-finance.md).

## Correspondence and discovery

The specialists hold `mcp__envision-mcp__*` and `mcp__personal-context__*` for
email, Slack, Drive documents, meeting transcripts, ClickUp, and people context.
That is a change from the earlier design, in which retrieval was the orchestrating
session's job alone, and the split it replaces is worth stating: the orchestrating
session still gathers the corpus and passes **pointers**, because pasting payloads
into four prompts is what blows the context budget. The specialists' own access
exists so a specialist can close a gap in the record it is analyzing instead of
reasoning around it.

Four rules bound that access, because widening reach into privileged material is
where this goes wrong:

- **Provenance at the point of use.** Every retrieved fact carries its source:
  message id, date, and sender for correspondence; filename for attachments. A
  quoted email with no id is an unverified assertion and cannot carry a
  conclusion. Same standard as the anchor-doc rule in
  [`gc-new-matter`](../../../skills/gc-new-matter/SKILL.md).
- **Just in time, not speculative.** Query when the question needs the record. Do
  not sweep a mailbox because the tools are there. personal-context is ACL-gated
  and audited.
- **Retrieved correspondence is privileged work product.** It belongs in the
  matter tree, which is untracked. It never goes into git-backed memory, a commit
  message, or any tracked file, and raw PII payloads are never pasted anywhere,
  including into a section file or a return.
- **Graceful absence.** A tool that is unavailable (server not connected,
  permission denied) is a LIMITATIONS entry, not a hole to fill from memory.

## Full engagement (materials review, feasibility, indication-report critique)

Follow [`workflows/full-engagement.md`](workflows/full-engagement.md): gather
source materials to local paths first, then one parallel dispatch of the relevant
specialists with per-section assignments, each specialist Writes its section file
and returns a short summary, then synthesize and run the strategy lens.

## Matter lifecycle

Anything that becomes a matter artifact (a feasibility memo, an indication-report
critique, a lapse-exposure analysis, a coverage position) routes through the
lifecycle skills instead of being written straight into `matters/`:
`gc-new-matter` scaffolds, `gc-consult` runs the consult, `gc-redteam` attacks it
before anyone acts on it, `gc-authorities-log` cite-checks anything that will be
filed or served, then `gc-file-and-serve` executes. A memo that reaches a matter
folder without a `gc-redteam` pass has skipped the only adversarial check in the
chain.

`gc-consult` ships with this plugin and loads wherever the plugin is installed.
The other four are repo-local to the general-counsel repo, where the privileged
`matters/` tree lives. Outside that repo those four do not load and matter
artifacts are out of scope; say so rather than improvising a folder. There is no
`memory/` tree in this repo.

Matter packages exported out of the repo follow one mandatory placement rule,
organized by law firm. Read it at its canonical location and do not restate it
here, because a second copy is how the rule drifts:
[`skills/gc-new-matter/SKILL.md`, section "Dropbox export placement"](../../../skills/gc-new-matter/SKILL.md#dropbox-export-placement-mandatory)
(that relative path resolves inside the general-counsel repo).

## Output discipline

- Cited analysis in complete sentences; tables only for enumerable comparisons
  (domicile matrices, notice-day counts).
- Separate what a statute SAYS, what a structure DOES, and what a promoter
  CLAIMS. Label each.
- Mandatory closing escalation line in every deliverable, naming the specific
  professional and the specific step.

## Evaluation

[`EVAL.md`](EVAL.md) records the measured effect of this skill (12 keyed prompts,
72 runs, 2026-07-04). Its answer keys are derived from the same primary sources
as `references/current-legislation.md` and age with them: re-derive the keys
after each legislation refresh before reusing the harness, and read the results
as valid as of the snapshot date recorded in that file.
