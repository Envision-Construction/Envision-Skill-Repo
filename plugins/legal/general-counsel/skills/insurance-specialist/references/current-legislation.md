# Current Captive Legislation Snapshot

> As of: 2026-07-04 — methodology: deep-research harness (104 agents, fan-out search → source fetch → 3-vote adversarial verification per claim; only claims surviving verification appear as VERIFIED). Supplemented by same-day specialist passes against primary statute text (labeled [specialist pass]). Full verified-findings JSON archived at `memory/private/atlas-captive-sources/deep_research_legislation_2026_07_04.json`. Coverage gaps are stated explicitly — absence means NOT VERIFIED THIS PASS, never "nothing happened." (That archive path is a claude-code-memory location, not a path in this repo; do not go looking for it here. Future refreshes archive inside the matter folder they were run for, per ../workflows/legislation-refresh.md.)

> **Freshness:** class=`legislation` verified=2026-07-04 sources=primary statute and regulation text, Federal Register and Treasury Decisions, IRS Rev. Procs. and guidance, court opinions (the ladder in ../workflows/legislation-refresh.md)

`class` selects the threshold from the central table in
`scripts/check_authority_freshness.py`; the number is not written here so that
changing it is one edit. Past the threshold this snapshot is a lead, not an
authority: re-run [`../workflows/legislation-refresh.md`](../workflows/legislation-refresh.md),
label what you could not verify "ASSUMPTION (unverified)", and record the stale
header and its date in LIMITATIONS. Bump `verified` only after re-verifying;
partial re-verification appends a changelog entry and leaves the date alone.

## Federal (VERIFIED, 3-0 votes unless noted)

**T.D. 10029 (90 FR 3534, published & effective Jan. 14, 2025)** — the operative micro-captive reporting framework; applies only to § 831(b)-electing captives:
- **Listed transaction (§ 1.6011-10 — VACATED, see litigation)**: 831(b) election + 20% Relationship Test (≥20% of captive assets/vote/value held by an Insured/Owner/related persons) + **BOTH** the Financing Factor **AND** loss ratio **below 30%** computed over the captive's **ten most recent taxable years**. A captive with fewer than ten taxable years **cannot** be a listed transaction. (Refuted detail: a "5-year Financing Computation Period pinned at § 1.6011-10(b)(2)" failed verification 1-2 — confirm period length against reg text before quoting.)
- **Transaction of interest (§ 1.6011-11 — IN FORCE)**: same Relationship Test + election, plus **EITHER** the Financing Factor **OR** loss ratio **below 60%** over ten years (threshold lowered from proposed 65%; period extended from nine). Disclosure duties under §§ 6011/6111/6112 for participants and material advisors, penalties for failure.
- Sources: federalregister.gov/documents/2025/01/14/2025-00393; eCFR/Cornell LII reg text.

**Litigation — live three-court split** (a Sixth Circuit merits ruling plausibly lands within 12 months):
- *Drake Plastics Ltd. Co. v. IRS*, No. 4:25-cv-02570 (S.D. Tex., Rosenthal, J., Apr. 15, 2026): **vacated § 1.6011-10** (listed) for lack of required § 6707A findings; **upheld § 1.6011-11** (TOI); vacatur stayed to May 1, 2026 — stay lapsed, **vacatur operative as of 2026-07-04**; remand leaves Treasury free to re-promulgate with proper findings. (Opinion text verified via FindLaw/Tax Notes.) **CITE CONFLICT, unresolved as of 2026-07-25:** `captive-formation-831b.md` § 4 carries this case as No. H-25-2570 decided Apr. 16, 2026. The docket sheet has not been re-pulled. Both forms may name the same Houston-division docket, but the two decision dates cannot both be right. Pull the docket sheet and reconcile before citing this case in anything filed or served; a case cited two ways with two dates is a cite-check failure.
- *CIC Services, LLC v. IRS*, No. 3:25-cv-00146 (E.D. Tenn., McDonough, J., Mar. 5, 2026): **upheld T.D. 10029 in full**; CIC's Sixth Circuit appellant brief filed June 11, 2026.
- *Ryan, LLC v. IRS*, No. 3:25-cv-78 (N.D. Tex.): arbitrary-and-capricious challenge to both designations **proceeded past dismissal** [verified]; trade press dated 2026-07-01 additionally reports a merits ruling upholding § 1.6011-11 [single-source — verify against opinion text before external citation].
- Practical posture: **assume TOI disclosure (Form 8886/8918) binds**; the nationwide-vs-party scope of the Drake vacatur is a contested remedial question — conservative advisors may treat listed-tier disclosure as prudent even while vacated.

**§ 831(b) premium cap, tax years beginning in 2026: $2,900,000** — Rev. Proc. 2025-32 (irs.gov/pub/irs-drop/rp-25-32.pdf); 2025 was $2,850,000 (Rev. Proc. 2024-40). Pinpoint reported as § 3.36 (direct extraction) and § 4.36 (verification pass) — dollar figure confirmed twice; reconfirm the section number before external citation. Rev. Proc. 2025-32 reflects OBBBA (P.L. 119-21, enacted 2025-07-04); whether OBBBA changed § 831(b) beyond indexing was NOT separately verified.

**§ 6700 promoter enforcement ACTIVE**: IR-2025-68 (June 16, 2025) — Bruce Molnar (Alta Holdings / U.S. Risk / Newport Re; the *Syzygy* program) paid § 6700 promoter penalties; IRS states it "will vigorously pursue managers, advisors and participants." Bears directly on captive-manager selection.

**NOT VERIFIED THIS PASS (federal)**: current IRS settlement-initiative availability (last formal initiatives were 2019/2020); pending 831(a)/(b) bills in the current Congress; Tax Court/appellate captive merits decisions within the last 24 months.

## State domiciles

- **North Carolina (VERIFIED)**: latest amendment S.L. 2024-29 (S.B. 319 — NC DOI page mislabels it "H.B. 319"), eff. July 2, 2024; no captive amendment enacted through 2026-07-04. Its redomestication premium-tax holiday (G.S. 105-228.4A(g)) **expired for taxable years beginning on/after Jan. 1, 2026**. Minimum capital & surplus (G.S. 58-10-370, 58-10-575): **$250K** pure/protected-cell/special-purpose/SPFC (Commissioner may set other amounts); **$500K** association/industrial-insured.
- **Vermont [specialist pass, primary text 2026-07-04]**: sponsored-captive core minimum **$100K, funded by the sponsor** (8 V.S.A. § 6004(a)(6)); cell participants fund regulator-set cell capital/collateral (no flat per-cell statutory minimum); premium tax 0.38% first $20M (§ 6014(a)), $7,500 minimum at sponsored-captive level with **cells exempt** (§ 6014(c)(2)); § 6034c cell-to-standalone conversion is a "deemed continuation"; § 6006b express two-way redomestication. 707 active captives YE2025 (ACCD release).
- **Georgia [specialist pass, primary text 2026-07-04]**: pure captive minimum surplus **$250K, client-funded** (O.C.G.A. § 33-41-8(a)(1), Commissioner may require more); premium tax 0.4% first $20M, $100K max, no statutory minimum (§ 33-41-22); inbound redomestication program (Ga. Reg. 120-2-45-.17, 45-day decision); **no express outbound redomestication provision found in Ch. 41 Art. 1** — outbound runs through receiving-state law + GA dissolution. ~56 captives (trade-reported; official OCI count not located). Code currency caveat: verified via 2024 Justia mirror (amendments through 2019 Ga. Laws 186 shown).
- **TN / SC / DE / UT: NOT VERIFIED THIS PASS** — chapter-level cites only (Tenn. Code Ann. tit. 56 ch. 13; S.C. Code § 38-90; N.C.G.S. ch. 58 art. 10 [NC verified above]; 18 Del. C. ch. 69; Utah Code § 31A-37). Verify amendments + capital minima before relying.

## Offshore

- **Bermuda (VERIFIED)**: Insurance Amendment (No. 2) Act 2025 operative Jan. 7, 2026 — expands BMA group-supervision criteria, creates "designated insurance holding companies" regime (Bermuda-incorporated entities only), notification/no-objection for material changes. Typical US-owned pure captive (Class 1–3) unlikely to be directly affected; matters for larger/commercial-class structures. (BMA Q4-2025 Regulatory Update.)
- **IRC 953(d) (VERIFIED)**: Rev. Proc. 2003-47 remains the operative election procedure (2025-26 PLRs still apply it). Electing insurer meeting the **Office Test** (US office) and **Asset Test** (US-situs assets ≥10% of base-year gross income, directly or via US consolidated affiliate) is exempt from the security requirement; failing both → closing agreement + letter of credit = 10% of gross income, **floor $75,000 / cap $10,000,000**, election not approved until security posted. Election trades § 884 branch-profits and § 4371 FET exposure for worldwide US taxation; FET returns if election terminates.
- **Cayman: NOT VERIFIED THIS PASS** — no CIMA rule-change or economic-substance findings survived verification. (A same-day engagement pass on CIMA Class B(i) capital/licensing is in progress; fold results into the next refresh.)

## Premium finance

**NOT VERIFIED THIS PASS** — zero verified findings on recent state/federal premium-finance-company regulatory changes. Georgia's operative framework (O.C.G.A. § 33-22-13 notice/cure mechanics) verified current 2026-07-04 by specialist pass — see `coverage-lapse-law.md` / `premium-finance.md`.

## Re-audit changelog

- 2026-07-04 — First full refresh (deep-research wf_b97d42f0-44a, 104 agents + specialist passes). Federal split documented (Drake vacatur / CIC upheld+appeal / Ryan pending-merits); $2.9M 2026 cap; § 6700 Molnar settlement; NC verified; VT/GA folded from specialist passes; Bermuda 2025 Act; Rev. Proc. 2003-47 mechanics. REFUTED: 5-yr financing-period pin. GAPS: TN/SC/DE/UT, Cayman, premium-finance changes, pending federal bills, settlement-initiative status.
- 2026-07-04: stub created with the skill, no legal content at that point. SUPERSEDED the same day by the full-refresh entry above; do not read this line as the state of the file.
- 2026-07-25: freshness audit only, no legal re-verification and no content change. Snapshot is 21 days old against a 90-day `legislation` threshold, so it is current and was NOT refreshed; nothing here was re-pulled and the `verified` date was deliberately not bumped. Added the parsable freshness header. Recorded the unresolved Drake Plastics docket/date conflict against `captive-formation-831b.md`. Carried forward for the next refresh, unchanged since 2026-07-04: TN / SC / DE / UT capital minima and amendments, Cayman (CIMA Class B(i) pass was in progress), premium-finance regulatory changes, pending federal 831(b) bills, IRS settlement-initiative status, Tax Court and appellate captive merits decisions in the last 24 months, and the Sixth Circuit posture in CIC Services (appellant brief filed 2026-06-11, a merits ruling plausibly lands inside this snapshot's remaining life).
