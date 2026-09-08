# Legislation Refresh: canonical deep-research question and staleness rule

## When to refresh

- [`../references/current-legislation.md`](../references/current-legislation.md)
  is past its `legislation` threshold (the central table in
  `scripts/check_authority_freshness.py`; **90 days**, the rule this convention
  started from), OR
- the user asks about "current / latest / this year's" captive legislation, OR
- a specialist hits a fact the snapshot dates before a known pending change.

`python3 scripts/check_authority_freshness.py` reports the snapshot's age along
with every other dated file in the suite; `--quiet` prints only breaches, which
is the form a scheduled run should use. A breach is not a stop: it downgrades the
snapshot from authority to lead until the specific fact you need is re-verified.

## How

Invoke `Skill(deep-research)` with the canonical question below (adjust the
trailing year window to the run date). Distill the verified findings into
[`../references/current-legislation.md`](../references/current-legislation.md).
Do **not** paste the full research dump; keep the snapshot under ~450 lines.
Archive the full report inside the matter folder it was run for
(`matters/<slug>/`, untracked and excluded from Cloud Build) rather than in a
`memory/` tree, which does not exist in this repo. Append a dated entry to the
snapshot's changelog: what changed, and what was checked and found unchanged. The
changelog persists across snapshot replacements.

Update the header's `verified` date only for what you actually re-verified
against a live source. A partial pass appends a changelog entry and leaves
`verified` alone. A date nobody earned is upstream of every fabricated citation
this suite exists to prevent, because it is what stops the next reader from
checking.

## Canonical question

> As of [RUN DATE], what is the current state of captive-insurance law and enforcement relevant to a US middle-market operating group evaluating captive formation? Cover, with primary-source citations and effective dates:
> 1. **Federal**: status and any litigation/amendment of the micro-captive final regulations (T.D. 10029, Jan 2025), current listed-transaction and transaction-of-interest definitions (loss-ratio thresholds, financing factors, computation periods), disclosure duties under sections 6011/6111/6112, and section 6700 promoter-penalty enforcement; the current inflation-indexed section 831(b) premium cap (cite the Rev. Proc.); any 831(b)/831(a) statutory amendments enacted or pending in the current Congress; IRS settlement-initiative status; significant Tax Court / appellate captive decisions in the last 24 months.
> 2. **State domiciles**, Georgia (O.C.G.A. Title 33 Ch. 41), Vermont, Tennessee, South Carolina, North Carolina, Delaware, Utah: captive-statute amendments in the last 24 months (new cell provisions, capital requirements, premium-tax changes, redomestication rules), plus each domicile's current minimum capital for pure and cell captives.
> 3. **Offshore**, Bermuda and Cayman: regulatory changes affecting US-owned captives (BMA / CIMA rules, economic-substance requirements), and the current mechanics/considerations of the IRC 953(d) election.
> 4. **Premium finance**: any recent state or federal changes to premium-finance-company regulation that affect captive or conventional program funding.
> Rank findings by relevance to a formation decision being made now; flag anything effective within the next 12 months.

## Snapshot format contract

`../references/current-legislation.md` must keep:

- Line 1 header, then the `> As of: YYYY-MM-DD` methodology line.
- The parsable freshness line, within the first 25 lines, carrying the three
  fields the checker reads in order: `class` (here, `legislation`), `verified`,
  and `sources` last. Copy its exact shape from the live file rather than
  retyping it. `verified` is the date a source was actually looked at, not the
  date the file was edited; `sources` names what was checked, concretely enough
  to repeat. A future date is reported as MALFORMED, on purpose: it is the
  obvious way to silence the check forever.
- Sections: Federal / per-domicile (GA, VT, TN, SC, NC, DE, UT) / Offshore
  (Bermuda, Cayman, 953(d)) / Premium finance.
- Every claim: pinpoint cite plus canonical URL plus verified-on date.
- Absence stated explicitly. A gap is written as NOT VERIFIED THIS PASS, never
  left silent, because silence reads as "nothing happened".
- `## Re-audit changelog` at the bottom, append-only, dated entries.

## Carried into the next refresh

The 2026-07-04 pass left these open, and they are the first things a refresh
should close: TN / SC / DE / UT amendments and capital minima, Cayman (CIMA Class
B(i) capital and licensing), premium-finance regulatory changes, pending federal
831(b) bills, IRS settlement-initiative status, and the Sixth Circuit posture in
*CIC Services*. There is also one unresolved cite conflict, recorded in both
files: *Drake Plastics* appears as No. 4:25-cv-02570 decided Apr. 15, 2026 in the
snapshot and as No. H-25-2570 decided Apr. 16, 2026 in
[`../references/captive-formation-831b.md`](../references/captive-formation-831b.md).
Pull the docket sheet and reconcile it in the same pass.
