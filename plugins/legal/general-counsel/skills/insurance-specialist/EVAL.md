# insurance-specialist — Quantitative Evaluation (2026-07-04)

> Method: 12 keyed prompts (3 fabricated-authority traps, 3 stale-figure/currency traps, 3 domain-depth, 3 judgment) × 2 configs (with skill / without) × 3 repeat runs = 72 runs. Independent scorer agents graded 210 keyed-fact checks against an answer sheet derived from an adversarially verified corpus (deep-research, 104 agents, 3-vote verification), web-verified 350 extracted citations, and 24 blind order-swapped A/B judgments (judges never told which config produced which answer, instructed not to reward length). Workflow `wf_49589e16-c45`; full per-run data in the session workspace.

> **Results valid as of 2026-07-04**, the verification date of the corpus these
> answer keys derive from. The keys are not evergreen: they encode the legal state
> recorded in [`references/current-legislation.md`](references/current-legislation.md)
> on that date, including the vacatur posture that p05 turns on. Re-derive them
> from that file after each legislation refresh before reusing this harness. A
> scored run against stale keys measures the keys, not the skill. One blocker
> first: the *Drake Plastics* docket-number and decision-date conflict recorded in
> both reference files is unresolved as of 2026-07-25, so any key that turns on
> the docket needs it reconciled before the run.

## Results

| Metric | With skill (36 runs) | Without skill (36 runs) |
|---|---|---|
| Keyed-fact pass rate | **100%** (105/105) | 92.4% (97/105) |
| Trap pass rate | **100%** (18/18) | 83.3% (15/18) |
| Fabrication rate (invented authority) | 0% | 0% |
| Citation validity (web-verified) | **100%** (180/180) | 98.8% (168/170) |
| Blind A/B wins | **20** | 4 (0 ties) |

## Reading the numbers honestly

- **Where the skill's edge concentrates: legal currency and regulation-content precision.** Every baseline trap failure was the same prompt (p05): all three baseline runs were unaware of the 2026 *Drake Plastics* vacatur of the listed-transaction reg — one asserted T.D. 10029 "remains in effect" and warned against relying on "a future vacatur." Both invalid baseline citations were content misstatements of the T.D. 10029 factor structure (stating either/or where the listed tier requires BOTH financing and sub-30% loss ratio). The skill's dated snapshot + never-quote-indexed-figures-from-memory rule eliminated this class entirely, 36/36.
- **What the skill does NOT add: gross-fabrication protection.** A frontier model with web access refused all three pure fabrication baits in both configs (0% fabrication everywhere). The skill's value is currency, precision, and consistency — not preventing invented statutes.
- **Blind preference 20–4** (binomial p ≈ 0.0008 vs. chance) on correctness/currency/usefulness criteria with length explicitly not rewarded.
- **Cost**: with-skill runs average roughly +90% wall-clock and +15% tokens (reference reading + verification passes). Iteration-1 smoke data: ~788s vs ~406s, ~171K vs ~150K tokens per run.

## Description-trigger optimization — attempted, instrument mismatch (2026-07-04)

The skill-creator trigger optimizer (20 realistic queries, 3 runs each, 12/8 train-test split) was run once and its measurement discarded as invalid for this estate: it probes bare headless `claude -p` where the description competes against ~900 installed skills with no semantic-routing layer, and measured 0% recall even on "what's the current 831(b) premium cap for 2026" (its improve loop also requires an env API key this machine doesn't expose). Production triggering here is mediated by the [SKILL-AUTO] gemini-embedding hook, where this description surfaced at cosine 0.64–0.79 on every insurance-adjacent prompt across the authoring session — including contextual triggers that never said "insurance" — and all 36 with-skill eval runs followed the skill correctly when routed. Re-run the optimizer only inside an isolated single-skill config if bare-triggering ever matters (e.g., distribution to estates without semantic skill routing).

## Provenance

Prompt set and answer keys derive from primary sources verified 2026-07-04 (Rev. Proc. 2025-32; T.D. 10029 / 90 FR 3534; Drake Plastics No. 4:25-cv-02570; CIC Services No. 3:25-cv-00146; NC S.L. 2024-29; O.C.G.A. 33-22-13; 8 V.S.A. 6004/6014/6034c; Rev. Proc. 2003-47). Keys age with the law — re-derive from `references/current-legislation.md` after each refresh before reusing this harness.
