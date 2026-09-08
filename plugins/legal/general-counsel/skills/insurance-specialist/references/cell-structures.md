# Cell Captive Structures — PCCs, SPCs, SACs, Series Captives

> Evergreen reference for the insurance-specialist skill.
>
> **Freshness:** class=`legislation` verified=2026-07-04 sources=domicile captive-statute text (official legislature sites, Justia mirrors with their currency year recorded), BMA and CIMA published law, IRS revenue rulings and the Federal Register, court opinion PDFs

`class` selects the threshold from the central table in
`scripts/check_authority_freshness.py`; the number is not written here so that
changing it is one edit. Past the threshold this file is a lead, not an
authority: re-verify the specific fact you need per
[`../workflows/legislation-refresh.md`](../workflows/legislation-refresh.md),
label what you cannot verify "ASSUMPTION (unverified)", and record the stale
header and its date in LIMITATIONS. Bump `verified` only after re-verifying this
file's own scope. The cross-reference to [`current-legislation.md`](current-legislation.md)
locates statute currency; it does not transfer that file's freshness to this one.
Minimum-capital figures and premium-tax rates are periodically amended and are
re-pulled from the domicile statute at each use, however fresh this header looks.

Decision-support reference for evaluating cell captive structures, rent-a-captive programs, and pooling arrangements. Compliance-risk framing throughout: abuse patterns are documented so structures avoid them. Not legal or tax advice.

## 1. Taxonomy — precise definitions

All of these are variations on one idea: a single licensed insurance company (the "core" or "sponsor") whose statute lets it wall off assets and liabilities into internally segregated compartments ("cells"), each typically serving a different participant. Terminology is jurisdiction-specific — do not use the terms interchangeably in filed documents.

| Term | Jurisdiction(s) | Legal personality of the cell |
|---|---|---|
| **Protected cell company (PCC)** | US states (VT, DC, MT, NV, GA, TN, SC, etc.), Guernsey (originator, 1997), Malta, Gibraltar | Unincorporated cell: NO separate legal personality by default; segregation is statutory, within one legal entity |
| **Incorporated cell company (ICC) / incorporated protected cell (IPC)** | Guernsey, Jersey; US states that added it (VT § 6034a, GA Art. 2 of ch. 41, TN, others) | Each cell IS a separately incorporated entity; the cell company is an umbrella. Strongest wall of the family |
| **Segregated accounts company (SAC)** | Bermuda — Segregated Accounts Companies Act 2000 (SAC Act); Incorporated Segregated Accounts Companies Act 2019 (ISAC) adds the incorporated variant | Segregated account is NOT a separate legal person (SAC Act § 17); statutory linkage of assets/liabilities to the account. Requires a Bermuda segregated account representative |
| **Segregated portfolio company (SPC)** | Cayman Islands — Companies Act (Revised), Part XIV; insurance SPCs licensed under the Insurance Act. "Portfolio insurance companies" (PICs) let an SPC incorporate a cell as a separate company (Insurance (Portfolio Insurance Companies) Regulations, 2015) | Segregated portfolio is not a separate legal person; a PIC is |
| **Series LLC captive** | Delaware, and a minority of US captive statutes that permit captives formed as series (DE explicitly; check domicile) | Series generally treated as separate under state LLC law for internal liability; federal tax entity status governed by the still-proposed 2010 regs (§ 4 below) |

Usage rules:
- "PCC" is the generic US/European term; "SPC" is Cayman; "SAC" is Bermuda; "sponsored captive with protected cells" is the phrasing in most US captive statutes (Vermont model). Match the domicile's statutory term in any formal document.
- "Cell captive," "rent-a-captive," and "sponsored captive" describe overlapping commercial arrangements, not distinct legal forms — the legal form is whichever chassis above the sponsor licensed.
- Incorporated cells can typically contract with each other and with the core; unincorporated cells of the same PCC generally cannot contract with each other (no separate personality) — a real constraint when structuring intercell reinsurance.

## 2. Rent-a-captive and sponsored-captive mechanics

A rent-a-captive lets a business get captive-like economics (underwriting profit and investment income on its own risk) without forming, capitalizing, and licensing its own insurer. The modern regulated form is the sponsored captive/PCC; the cell is the "rented" compartment.

**Core vs. cell ownership and capital:**
- The **sponsor/core** owns the licensed insurance company, contributes the core (statutory minimum) capital, holds the license, and is the regulated person. Sponsors are typically insurers, reinsurers, or captive managers; many statutes restrict who may sponsor.
- The **cell participant** contributes cell-level capital/collateral and receives the cell's underwriting results by contract. In an unincorporated-cell PCC the participant usually does NOT own the cell (there is nothing to own — it's an account); it holds contractual rights via a participation agreement, sometimes evidenced by non-voting preference shares of the core linked to the cell. In an ICC/IPC or Cayman PIC, the participant can own actual shares of the incorporated cell.
- Cell capital norms are set per-domicile and per-program by the regulator based on the cell's business plan — expect the regulator to require capital sufficient for the cell's retained risk, not just a flat minimum.

**Participation agreement** — the central document. Verify it addresses: which liabilities attach to the cell vs. the core; premium and claims flows; collateral obligations and top-up triggers; dividend/profit distribution; recourse (or non-recourse) between core and cell; exit/termination and runoff; governing law matching the domicile's cell statute.

**Fronting and collateral:**
- Where the insured needs admitted paper (workers' comp, auto liability, contractual COI requirements), a licensed **fronting carrier** issues the policy and reinsures the cell. The front takes credit risk on the cell and demands **collateral** — letter of credit, reinsurance trust (Reg. 114-type trust), or funds withheld — typically sized at or above expected ultimate losses within the cell's retention.
- Direct-placement cell programs (no front) write surplus-lines-style or direct where the domicile and the insured's home-state law permit — this is exactly where unlicensed-insurer problems arise (see Talisman, § 3).

**Live example the user has encountered:** Talisman Casualty Insurance Company LLC (Las Vegas) is a Nevada-domiciled protected-cell captive selling specialty coverage (contractors, surety-like products) through cells to third-party insureds. Treat it as a worked example of both the mechanics and the risk: on 2025-07-09 the Florida Office of Insurance Regulation entered a consent order requiring Talisman to cease and desist acting as a captive insurer in Florida without a license or certificate of authority (floir.gov consent order, verified 2026-07-04). Lesson: a cell captive licensed in Domicile A that sells to insureds in State B is exposed to State B's unauthorized-insurer regime; the cell wall does nothing for that problem.

## 3. Strength of cell walls

**What the statute gives you:** ring-fencing — assets of cell X are not chargeable with liabilities of cell Y or of the core's other business (e.g., 8 V.S.A. § 6034(3); SAC Act 2000). Within the domicile, this is settled statutory law.

**What litigation has actually tested (thin):**
- *Pac Re 5-AT v. AmTrust N.A.*, No. 1:14-cv-00131-CSO (D. Mont. May 13, 2015): an unincorporated Montana protected cell was held NOT a separate legal entity; absent statutory language to the contrary, the PCC core was the proper party and was held liable for obligations incurred in the cell's name. Follow-on: *AmTrust N.A. v. Pacific Re*, No. 15-cv-7505 (S.D.N.Y. Mar. 25, 2016) confirmed the arbitration award against the core, not merely the cell. (govinfo.gov opinion PDF, verified 2026-07-04.)
- Takeaway: the wall protects cell assets from other cells' creditors, but it does not automatically shield the CORE from liabilities a cell incurs — that depends on the statute's exact recourse language and the participation agreement. Draft non-recourse language explicitly; do not assume it.
- Beyond Pac Re and a handful of insolvency matters, US courts have rarely tested cell segregation in a core-insolvency scenario. Treat ring-fencing as statutorily strong but litigation-thin — price that uncertainty in any structure where a single cell's blowup could exceed core capital.

**Cross-jurisdiction recognition risk:** the segregation is a creature of the domicile's statute. A claimant suing in a forum state with no cell statute (or a bankruptcy court applying federal law) may not respect the wall — there is no controlling US authority requiring a non-domicile forum to honor another state's (or Bermuda's/Cayman's) cell segregation. Risk is highest when: (a) the cell writes third-party business in non-domicile states (Talisman pattern), (b) the core becomes insolvent, or (c) the claim sounds in tort/fraud rather than contract. Incorporated cells (ICC/IPC/PIC) largely moot this — separate incorporation travels across borders the way ordinary corporate separateness does — which is the main reason to pay the extra cost of incorporation for cells with outside-domicile exposure.

## 4. Federal tax treatment of cells

**Rev. Rul. 2008-8, 2008-5 I.R.B. 340** (irs.gov/pub/irs-drop/rr-08-08.pdf, verified 2026-07-04): insurance status is tested **cell by cell**. The arrangement between an individual cell and its owner is analyzed under the same risk-shifting / risk-distribution / insurance-in-the-commonly-accepted-sense standards that apply to a standalone captive (the ruling maps the classic brother-sister and parent-sub fact patterns onto cells). Consequence: a PCC is not "an insurance company" wholesale — each cell must independently earn insurance treatment. Companion **Notice 2008-19** (same I.R.B.) requested comments on cell entity status and foreshadowed the proposed regs.

**831(b) elections apply per cell.** A cell that (i) is treated as a separate entity for federal tax purposes, (ii) qualifies as an insurance company, and (iii) meets the premium and diversification tests can make its own § 831(b) election. The net-written-premium ceiling is inflation-indexed: **$2,900,000 for taxable years beginning in 2026** (Rev. Proc. 2025-32 § 3, irs.gov/pub/irs-drop/rp-25-32.pdf, verified 2026-07-04; up from $2.85M in 2025 per Rev. Proc. 2024-40 — confirm the 2025 figure in current-legislation.md before citing it). The § 831(b)(2)(B) diversification requirements (20% single-policyholder limit or the ownership test) are tested at the electing cell, not the PCC — a cell whose premium all comes back from one promoter pool needs the pool to supply genuine risk distribution (see § 7).

**Series/cell entity-classification regs — STILL PROPOSED.** Prop. Reg. § 301.7701-1(a)(5), REG-119921-09, 75 Fed. Reg. 55699 (Sept. 14, 2010) (federalregister.gov/documents/2010/09/14/2010-22793, verified 2026-07-04) would treat each domestic series/cell as an entity formed under local law, then classify it under the normal check-the-box rules. As of 2026-07-04 these have **never been finalized** (multiple 2025–2026 practitioner sources confirm; verified 2026-07-04). Note: under the proposed regs and existing IRS practice, a cell that conducts an insurance business is treated as a separate entity in any event — so insurance cells have the clearest (if still non-final) path to separate-entity status. Foreign cells (Bermuda SAC accounts, Cayman SPs) raise additional issues (per-cell 953(d) elections, CFC status) — take those questions to a specialist; do not extrapolate.

**Enforcement overlay:** final regulations designating certain micro-captive transactions as listed transactions / transactions of interest were published Jan. 14, 2025 (**T.D. 10029**, 90 Fed. Reg. — federalregister.gov/documents/2025/01/14/2025-00393, verified 2026-07-04), and apply to cell arrangements the same as standalone captives (the regs' definitions expressly reach cells). District-court litigation over these regs produced conflicting 2025–2026 outcomes (one court upheld them; another vacated the listed-transaction designation at least in part) — the regime's current enforceability is genuinely unsettled; check references/current-legislation.md before advising on disclosure obligations.

## 5. Cell provisions per domicile (one line each — currency in current-legislation.md)

- **Georgia** — O.C.G.A. Title 33, Ch. 41 (Captive Insurance Company Act, enacted 1988, modernized 2021–22); Article 2 adds protected cells and **incorporated** protected cells (IPCs count as captives under § 33-41-2); rules at Ga. Comp. R. & Regs. 120-2-45. (justia/oci.georgia.gov, verified 2026-07-04)
- **Vermont** — 8 V.S.A. ch. 141, subch. 2 (sponsored captives): § 6034 protected cells (statutory ring-fence), § 6034a incorporated protected cells, § 6034c sponsored-captive mechanics; 2024 amendments eased cell-to-standalone conversion. (legislature.vermont.gov, verified 2026-07-04)
- **Tennessee** — Revised Captive Insurance Act, Tenn. Code Ann. tit. 56, ch. 13 (protected-cell / ICC provisions in the 2011 rewrite and later amendments — confirm pinpoint in current-legislation.md).
- **South Carolina** — S.C. Code Ann. ch. 38-90 (captives incl. sponsored captives and cells — confirm pinpoint).
- **North Carolina** — N.C. Captive Insurance Act (2013), N.C. Gen. Stat. ch. 58, art. 10 (protected-cell captives — confirm pinpoint).
- **Delaware** — 18 Del. C. ch. 69 (sponsored captives; Delaware also permits **series** captive structures — the series-LLC/cell overlap is most acute here; confirm pinpoint).
- **Utah** — Utah Code tit. 31A, ch. 37 (captives; sponsored-captive/cell part — confirm pinpoint).
- **Bermuda** — Segregated Accounts Companies Act 2000 (registration of SACs; § 17 no-separate-personality; segregated account representative required) + Incorporated Segregated Accounts Companies Act 2019; insurance licensing under the Insurance Act 1978. (BMA-published Act text, verified 2026-07-04)
- **Cayman** — Companies Act (Revised) Part XIV (SPCs) + Insurance Act (Revised) for licensed insurer SPCs + Insurance (Portfolio Insurance Companies) Regulations, 2015 (PICs). (Chapter-level cite; confirm revision year in current-legislation.md.)

## 6. Capitalization, fronting, collateral; exiting into a standalone captive

**Capital norms (directional, regulator-negotiated — not statutory constants):**
- Core capital: fixed by the domicile's own statute, and the regulator can and does require more than the floor. The only sponsored-captive core minimum verified in this skill's source set is Vermont's: **$100K, funded by the sponsor** (8 V.S.A. § 6004(a)(6), verified 2026-07-04, recorded in [`current-legislation.md`](current-legislation.md)). Do not generalize that figure into a range, and do not attach a range to a named state whose statute has not been pulled. Quote a number only after reading the governing domicile's section text.
- Cell capital: sized to the cell's business plan — retention, line of business, premium volume. Regulators look for cell assets ≥ a conservative estimate of ultimate retained losses; promoter decks that quote "no capital required" are describing collateral posted to a front, not an absence of capital.
- Collateral to fronts: LOC or reinsurance trust, typically 100%+ of expected ultimate losses in the cell's layer, adjusted annually with loss development. Funds-withheld structures trade collateral for credit exposure to the front.

**Exiting a cell into a standalone captive (redomestication basics):**
1. Feasibility first — a cell graduating usually has premium/surplus that now justifies standalone frictional costs (own audit, actuary, board, capital).
2. Mechanics: most cell statutes now allow **conversion** of a cell (especially an incorporated cell) into a standalone captive in the same domicile (e.g., Vermont's conversion provisions, streamlined 2024); moving domiciles is a **redomestication** under the receiving state's captive statute — the new domicile licenses the entity, the old one releases it, and the entity's corporate existence continues (no assumption-reinsurance novation needed if continuity is preserved).
3. Unincorporated cells are harder — there may be no "entity" to redomesticate; the practical path is: incorporate the cell (if the statute allows), or form the new captive and move the book via novation or loss-portfolio-transfer reinsurance, then run off / terminate the participation agreement.
4. Diligence items: trapped collateral at the fronting carrier (LOCs often outlive the participation), unearned premium and IBNR allocation between cell and core, exit fees in the participation agreement, tax continuity (an entity-status change can be a deemed liquidation — model it before moving).

## 7. Red flags in cell/pool promotions — and what defensible looks like

The two controlling micro-captive cases both ran through promoter-operated quota-share pools, and both are directly applicable to cell programs:

- ***Avrahami v. Commissioner*, 149 T.C. No. 7 (2017):** captive's risk distribution rested on Pan American Reinsurance — a promoter-linked "terrorism" pool charging ~$360K/yr premiums for remote risk, with **circular cash flow** (pool premiums out ≈ reinsurance premiums back in) and premiums not actuarially derived. Court: not insurance. (EY summary + Ryan case note, verified 2026-07-04)
- ***Reserve Mechanical Corp. v. Commissioner*, T.C. Memo. 2018-86, aff'd 34 F.4th 881 (10th Cir. May 13, 2022):** risk distribution claimed through PoolRe, a Capstone-managed stop-loss pool of ~50 captives; quota-share premiums were reciprocal and engineered so each participant got back roughly what it paid in. Both courts: the quota-share policies were not bona fide insurance; no risk distribution. (10th Cir. slip op. at ca10.uscourts.gov, verified 2026-07-04)

**Red flags the IRS attacks (a defensible structure shows the opposite):**

| Red flag (IRS attack vector) | What defensible looks like |
|---|---|
| Promoter-controlled pool where the promoter also manages every participant's captive/cell | Independent pool or fronting arrangement; unaffiliated risk actually at stake; participant can audit pool underwriting |
| Circular/reciprocal cash flow — each cell's pool premium ≈ its reinsurance recovery of premium | Net risk transfer: pool losses can exceed any participant's premium; cash flows track loss experience, not contributions |
| Premiums not actuarially derived (priced to hit the 831(b) ceiling, flat across insureds, or backed into from a tax target) | Independent actuarial pricing memo per coverage, exposure-rated, re-priced annually against loss experience |
| Implausible coverages (terrorism on a jewelry store, remote-risk policies never claimed on) | Coverages map to documented, quantified exposures the insured actually faces and previously retained or bought commercially |
| No claims ever filed / claims discouraged | Real claims history; claims handled at arm's length with documentation |
| Cell capital and premium routed back to the owner via loans, side agreements | Cell assets stay in the cell, invested conservatively, no loan-backs to insureds/owners |
| Diversification test "met" solely by the promoter's pool | Risk distribution defensible without the pool, or pool participation survives Reserve Mechanical scrutiny (genuine heterogeneous risks, real pool-level losses) |
| Sales pitch leads with tax savings, estate planning, or "deductible wealth transfer" | Feasibility study leads with risk management need; tax treatment is a consequence, not the purpose |

Cell-specific additions: verify the cell (not just the core) can meet insurance status under Rev. Rul. 2008-8 on its own facts; verify T.D. 10029 disclosure analysis was done per electing cell (subject to the litigation caveat in § 4); verify the participation agreement doesn't quietly make the arrangement a deposit/experience-account (no real risk transfer to anyone).

## Sources verified

- https://www.irs.gov/pub/irs-drop/rr-08-08.pdf — Rev. Rul. 2008-8 text: cell-by-cell insurance-status analysis, statutory protection of cell assets. (verified 2026-07-04)
- https://www.irs.gov/irb/2008-05_IRB — I.R.B. 2008-5 carrying Rev. Rul. 2008-8 and Notice 2008-19. (verified 2026-07-04)
- https://www.irs.gov/pub/irs-drop/rp-25-32.pdf — Rev. Proc. 2025-32: 2026 inflation adjustments incl. § 831(b) $2.9M limit (corroborated by captivereview.com and MarksNelson notes). (verified 2026-07-04)
- https://www.federalregister.gov/documents/2010/09/14/2010-22793/series-llcs-and-cell-companies — REG-119921-09 proposed series/cell classification regs, 75 FR 55699; multiple 2025–2026 practitioner sources confirm never finalized. (verified 2026-07-04)
- https://www.federalregister.gov/documents/2025/01/14/2025-00393/micro-captive-listed-transactions-and-micro-captive-transactions-of-interest — T.D. 10029 final micro-captive listed-transaction regs, effective Jan. 14, 2025; JofA (July 2026) and Parker Tax notes confirm split district-court outcomes in ensuing litigation. (verified 2026-07-04)
- https://www.ca10.uscourts.gov/sites/ca10/files/opinions/010110683986.pdf — Reserve Mechanical 10th Cir. affirmance (May 13, 2022): PoolRe quota-share not bona fide insurance. (verified 2026-07-04)
- https://taxnews.ey.com/news/2017-1382-tax-court-holds-microcaptive-insurance-company-was-not-bona-fide-insurer and https://ryan.com/avrahami-v.-commissioner/ — Avrahami, 149 T.C. No. 7: Pan American pool, circular cash flow, non-actuarial premiums. (verified 2026-07-04)
- https://www.govinfo.gov/content/pkg/USCOURTS-mtd-1_14-cv-00131/pdf/USCOURTS-mtd-1_14-cv-00131-0.pdf — Pac Re 5-AT v. AmTrust, No. 1:14-cv-00131 (D. Mont. May 13, 2015): unincorporated cell not a separate legal entity. (verified 2026-07-04)
- https://legislature.vermont.gov/statutes/section/08/141/06034 (+ § 6034a, § 6034c) — Vermont protected-cell and incorporated-protected-cell statutes. (verified 2026-07-04)
- https://oci.georgia.gov/regulatory-filings/captives, https://law.justia.com/codes/georgia/title-33/chapter-41/ and Ga. R. & Regs. 120-2-45 — Georgia Captive Act O.C.G.A. 33-41 incl. incorporated protected cells (Art. 2). (verified 2026-07-04)
- https://cdn.bma.bm/documents/2023-11-14-09-27-09-Segregated-Accounts-Companies-Act-2000.pdf — Bermuda SAC Act 2000 text (BMA-hosted). (verified 2026-07-04)
- https://floir.gov/docs-sf/default-source/orders/property-and-casualty/2025/talisman-casualty-insurance-company-consent-order-(07-09-2025).pdf — Florida OIR consent order (2025-07-09): Talisman Casualty cease-and-desist, unlicensed captive activity in Florida. (verified 2026-07-04)
