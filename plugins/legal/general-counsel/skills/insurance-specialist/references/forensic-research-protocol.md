# Forensic Research Protocol

> Evergreen reference for the insurance-specialist skill.
>
> **Freshness:** class=`method` verified=2026-07-04 sources=n/a, method only: this file asserts no dated legal fact of its own, and its dated items are locators re-found at use (see the note below)

`class=method` is a positive claim that nothing here goes stale on a clock, so it
carries no threshold. It is true only because of one rule: **the dated items in
this file are locators, never load-bearing content.** The URL patterns in § 2 were
confirmed to resolve on the date shown; if one 404s, re-search rather than
guessing a sibling (§ 2 says so). The Rev. Proc. numbers named in § 6 are worked
examples of the procedure, not the figure: § 6's instruction is to locate the
current annual inflation-adjustment Rev. Proc. and scrape it, which stays correct
after a new one supersedes the ones named. Anything in this file that starts
asserting a dated legal fact instead of locating one has left `method`, and the
class has to change with it. Statute currency lives in
[`current-legislation.md`](current-legislation.md), which carries its own header.

This file is METHOD. It governs how every other reference in this skill gets researched, verified, and cited. Follow it before asserting any legal, regulatory, or tax fact. This is decision support, not legal or tax advice — the protocol exists so structures can be evaluated against what the law actually says, not what a promoter claims it enables.

## 1. Source hierarchy (highest to lowest)

Resolve conflicts by picking the higher layer. A lower layer NEVER overrides a higher one.

| Rank | Source class | Examples | Load-bearing? |
|---|---|---|---|
| 1 | Official statute/regulation text | State legislature codification sites, govinfo.gov, uscode.house.gov, ecfr.gov | Yes — the anchor |
| 2 | Final rules / Treasury Decisions in the Federal Register | federalregister.gov, govinfo.gov FR collection | Yes |
| 3 | IRS subregulatory guidance | Notices, Rev. Procs., Rev. Ruls. in the Internal Revenue Bulletin (irs.gov/irb, irs.gov/pub/irs-drop) | Yes, within its authority tier — note it binds the IRS less than a T.D. |
| 4 | Court opinions | Official reporters / court-issued PDFs (ustaxcourt.gov, uscourts.gov, state supreme court sites) | Yes — cite the official PDF, not a blog's summary |
| 5 | Agency releases | Insurance-department bulletins, BMA/CIMA guidance notes, IRS news releases (IR-XXXX-XX) | Contextual — confirm against layers 1–4 |
| 6 | Secondary analysis | Law-firm client alerts, treatises, bar journal articles | Lead-generation only — use to FIND the primary source, then cite the primary |
| 7 | Broker / promoter / captive-manager marketing | Vendor sites, "831(b) plan" promoters, VAR pages | NEVER load-bearing. Treat every claim as an allegation to verify against layers 1–4 |

Two hard corollaries:
- A law-firm alert that says "the statute provides X" is a pointer, not proof. Scrape the statute.
- Promoter marketing is itself evidence in the compliance-risk analysis (what the market is being told), but never evidence of what the law says.

## 2. Retrieval sequence

Standard loop: `firecrawl_search` to LOCATE → `firecrawl_scrape` the OFFICIAL source → pin the citation (section, URL, verified date). Never cite from the search snippet alone; snippets truncate operative language ("shall not" becomes "shall"). Never quote WebFetch output — it is a model summary, not raw text; use firecrawl_scrape when the exact words matter.

For PDFs (session laws, Rev. Procs., court opinions), scrape with `parsers: ["pdf"]`. For statute pages that render via JS, add `waitFor`.

### Canonical URL patterns per jurisdiction (all verified live 2026-07-04)

**Federal**
- IRC (official): `https://uscode.house.gov/browse/prelim@title26&edition=prelim` (OLRC) and `https://www.govinfo.gov` USCODE collection. Cornell LII (`law.cornell.edu/uscode/text/26/...`) is a reliable unofficial mirror — fine for locating, cite the official for load-bearing text.
- Treasury regs (current): `https://www.ecfr.gov/current/title-26` — pinpoint pattern `ecfr.gov/current/title-26/chapter-I/...`. eCFR is continuously updated but unofficial; the annually published CFR on govinfo.gov is official. For load-bearing reg text, note the eCFR "as of" date shown on the page.
- Federal Register (T.D.s, proposed rules, listed-transaction notices): `https://www.federalregister.gov` (search by T.D. number or docket); official PDF also in the govinfo.gov FR collection.
- IRS guidance: Rev. Procs./Notices as released at `https://www.irs.gov/pub/irs-drop/rp-YY-NN.pdf` (e.g., `rp-25-32.pdf`); as published at `https://www.irs.gov/irb/YYYY-WW_IRB` (e.g., `irs.gov/irb/2025-45_IRB`). The IRB version is the citable one.
- Tax Court: `https://www.ustaxcourt.gov` — use DAWSON (Docket search / Opinion search) for official opinion PDFs. Cite by official reporter (T.C., T.C. Memo.) plus the DAWSON PDF link.

**States** (each verified to resolve to the captive chapter, 2026-07-04)
- **GA**: Official O.C.G.A. free public access is via the Code Revision Commission's LexisNexis portal, `https://www.lexisnexis.com/hottopics/gacode/` (linked from `https://www.legis.ga.gov` → "Georgia Code"). The Lexis portal is session-tokened and hostile to scraping — use Justia's mirror `https://law.justia.com/codes/georgia/title-33/chapter-41/` (captive chapter, O.C.G.A. §§ 33-41-1 to 33-41-106) to read, then cite the O.C.G.A. section number and note the mirror year (Justia currently mirrors the 2024 Code).
- **VT**: `https://legislature.vermont.gov/statutes/chapter/08/141` (8 V.S.A. ch. 141, Captive Insurance Companies); per-section pattern `legislature.vermont.gov/statutes/section/08/141/0NNNN` (e.g., `/06001` for 8 V.S.A. § 6001). This IS the official Vermont Statutes Online.
- **TN**: Revised Tennessee Captive Insurance Act = Tenn. Code Ann. §§ 56-13-101 to 56-13-418. Official free access to T.C.A. is via the Secretary of State's Lexis arrangement; practical mirrors: `https://law.justia.com/codes/tennessee/title-56/chapter-13/`. Regulator's law page: `https://www.tn.gov/commerce/insurance/captive/rules-and-laws.html`. Session laws (public chapters, official PDFs): `https://publications.tnsosfiles.com/acts/{GA}/pub/pcNNNN.pdf`.
- **SC**: `https://www.scstatehouse.gov/code/t38c090.php` — S.C. Code Title 38, ch. 90 (Captive Insurance Companies), whole chapter on one official page. Title index: `scstatehouse.gov/code/title38.php`.
- **NC**: `https://www.ncleg.gov/Laws/GeneralStatuteSections/Chapter58` — N.C.G.S. ch. 58; captive provisions in Article 10 (N.C.G.S. § 58-10-340 et seq.). Session laws: `ncleg.gov/EnactedLegislation/SessionLaws/HTML/{biennium}/SLYYYY-NN.html`.
- **DE**: `https://delcode.delaware.gov/title18/c069/` — 18 Del. C. ch. 69 (Captive Insurance Companies), official Delaware Code Online with an "Authenticated PDF" link per chapter — prefer the authenticated PDF for load-bearing quotes.
- **UT**: `https://le.utah.gov/xcode/Title31A/Chapter37/31a-37.html` — Utah Code Ann. ch. 31A-37 (Captive Insurance Companies Act); per-section pattern `le.utah.gov/xcode/Title31A/Chapter37/31A-37-SNNN.html`. Official; each section page shows its effective date.

**Offshore**
- **Bermuda**: consolidated laws at `https://www.bermudalaws.bm` — pattern `bermudalaws.bm/Laws/Consolidated%20Law/{year}/{Act Name}` (e.g., `/1978/Insurance%20Act%201978`). Regulator: `https://www.bma.bm` (registers, guidance notes, Statements of Principles as PDFs under `bma.bm/viewPDF/documents/...`).
- **Cayman**: consolidated legislation index at `https://legislation.gov.ky` (primary Acts alphabetical; subordinate legislation PDFs under `legislation.gov.ky/cms/images/LEGISLATION/...`). Regulator: `https://www.cima.ky/insurance` (Insurance Act overview, rules, statements of guidance). Cayman renamed "Laws" to "Acts" in 2020 — search both forms.

If a pattern above 404s, do NOT guess a sibling URL into a citation — re-search, or use `firecrawl_map` on the domain to find the moved page.

## 3. Verification rules

- **Two independent sources for every load-bearing claim.** Independent means different provenance — the official statute page plus a court opinion applying it counts; two law-firm alerts citing each other does not. For statute text, official source + one mirror (Justia/FindLaw/Cornell) agreeing is sufficient.
- **Effective-date discipline.** A codified section is the statute *as amended* — it silently absorbs session laws. When the question is "what did the law say on date D" (audit years, policy inception), pull the session law history (every official codification lists amending acts) and reconstruct the version in force on D. The current code page answers "what is the law today," nothing more.
- **Regs: applicability date ≠ publication date.** A T.D. published in the Federal Register may apply only to tax years beginning after a later date, or retroactively per the APPLICABILITY/DATES section of the preamble. Cite the applicability date, not the FR publication date, when the question is whether a rule governs a given year.
- **Pending-change sweep.** Before treating an answer as settled, run one search for pending legislation (state legislature bill trackers, congress.gov), proposed regs (federalregister.gov proposed-rule search), and live litigation (a circuit split or pending Tax Court docket can flip the answer). If something pending could change the answer, say so explicitly in the output and log it in references/current-legislation.md.
- **Regulator bulletins can move faster than statutes.** Check the state insurance department / BMA / CIMA page for bulletins interpreting the captive statute — a statute unchanged since 2019 may carry a 2025 bulletin that changes filing practice.

## 4. Citation discipline

Every load-bearing legal assertion carries all three, every time:
1. **Pinpoint cite** — section/subsection, not the chapter: `8 V.S.A. § 6002(a)(2)`, `Treas. Reg. § 1.831-3`, `Rev. Proc. 2025-32, § 3.__`, `Avrahami v. Commissioner, 149 T.C. 144 (2017)`.
2. **Canonical URL** — the official source actually scraped (per § 2 patterns), not a search-result URL or aggregator.
3. **Verified-on date** — `(verified YYYY-MM-DD)`. This is the date the URL was scraped and the text read, not the date the law passed.

Status labels — distinguish precisely, never blur:
- **Repealed** — was law, no longer is. Cite the repealing act and its effective date.
- **Not yet effective** — enacted but with a future effective date. Cite the session law and the effective date; do not describe it as current law.
- **Amended pending codification** — session law passed, code page not yet updated. Cite the session law; flag that the code page lags.
- **Not found** — searched, does not exist at the expected location. Say exactly that (see § 5).
- **UNVERIFIED — confirm before relying** — asserted but not confirmed against an official source in this pass.

## 5. Never-fabricate rules

- **"Not found" is a complete, correct answer.** If the statute, ruling, or case cannot be located at official sources, write "not found" — never "it likely exists," never a plausible-sounding cite.
- **Never assume a document exists because a claim references it.** Promoter decks routinely cite "IRS approval letters," "safe-harbor rulings," and cases that do not say what is claimed — or do not exist. A reference to a document is a search instruction, not evidence.
- **Never construct a citation from a pattern.** URL patterns in § 2 locate documents; they do not prove a specific section number exists. Confirm the section renders with the expected text before citing it.
- **Distinguish three different things in every write-up:** what the statute SAYS (quoted, pinpoint-cited) / what it arguably ENABLES (analysis, labeled as analysis) / what a promoter CLAIMS it enables (layer-7 allegation, attributed and unverified). Collapsing these three is the core fabrication failure mode in this domain — and the pattern the IRS attacks in promoted-transaction cases. A defensible research product keeps the three visibly separate.
- **Never quote a legal holding from memory.** Model memory of case outcomes and dollar thresholds drifts. Scrape the opinion; quote the scraped text.

## 6. Indexed-figure currency rule

Inflation-indexed figures are NEVER quoted from model memory or from a prior year's reference file. This includes, at minimum:
- the § 831(b)(2)(A)(i) net/direct written premium cap (indexed annually per § 831(b)(2)(D));
- § 6662/§ 6707A-family penalty amounts and any indexed reporting thresholds;
- state captive premium-tax brackets and minimum-capital figures when the state indexes or periodically amends them.

Procedure on EVERY use: locate the current annual inflation-adjustment revenue procedure (search `site:irs.gov "Rev. Proc." inflation adjustments {year}`; for tax years beginning in 2026 that is **Rev. Proc. 2025-32**, https://www.irs.gov/pub/irs-drop/rp-25-32.pdf, published in I.R.B. 2025-45, https://www.irs.gov/irb/2025-45_IRB (verified 2026-07-04); for tax years beginning in 2025 it was Rev. Proc. 2024-40, https://www.irs.gov/pub/irs-drop/rp-24-40.pdf (verified 2026-07-04)) → scrape it → quote the figure with the Rev. Proc. pinpoint section → cite Rev. Proc. number + URL + verified date. If the current-year Rev. Proc. is not yet released for the year in question, say so and use the latest released one, labeled with its applicable tax year.

## 7. Escalation criteria — stop and require licensed professionals

Research output from this skill is decision support. The following are OUTSIDE its lane; when the task touches one, deliver the research memo and state plainly that a licensed professional must own the next step:

- **Anything filed with the IRS or a regulator** — a § 831(b) election, Form 8886/8918 reportable-transaction disclosures, a captive license application, annual statutory filings. Research can describe requirements; a licensed practitioner signs and files.
- **Tax opinion letters / penalty-protection reliance** — only counsel can render an opinion a taxpayer may rely on; never draft text intended to function as one.
- **Actuarial work** — premium pricing, loss reserving, feasibility studies. Pricing defensibility is exactly what the IRS attacks (arm's-length premiums, actuarially determined); a credentialed actuary's signed work is the defense, not a research memo.
- **Live disputes** — an open IRS exam, appeals, docketed litigation, or a regulator inquiry. Research may support counsel; it must not go to the adversary directly.
- **Formation/restructuring decisions at the commitment point** — jurisdiction selection and structure design can be researched and compared here, but the decision to form, dissolve, or restructure requires counsel and (usually) a licensed captive manager in the domicile.

The escalation line in one sentence: **when the work product would be filed, relied on for penalty protection, or shown to a regulator or court, it must come from a licensed professional — this skill prepares the briefing that makes their work faster.**

## Sources verified

All URLs scraped or search-confirmed 2026-07-04:

- https://law.justia.com/codes/georgia/title-33/chapter-41/ — GA captive chapter mirror (O.C.G.A. §§ 33-41-1 to 33-41-106; 2024 Code)
- https://www.lexisnexis.com/hottopics/gacode/ + https://www.legis.ga.gov — official O.C.G.A. public-access portal and legislature site
- https://legislature.vermont.gov/statutes/chapter/08/141 — Vermont Statutes Online, 8 V.S.A. ch. 141 (captives); section pattern /statutes/section/08/141/06001
- https://law.justia.com/codes/tennessee/title-56/chapter-13/ — Revised Tennessee Captive Insurance Act mirror (T.C.A. §§ 56-13-101 to 56-13-418)
- https://www.tn.gov/commerce/insurance/captive/rules-and-laws.html — TN regulator's captive law page
- https://publications.tnsosfiles.com/acts/109/pub/pc1018.pdf — TN session-law (public chapter) PDF pattern
- https://www.scstatehouse.gov/code/t38c090.php — S.C. Code Title 38, ch. 90 (captives), official
- https://www.ncleg.gov/Laws/GeneralStatuteSections/Chapter58 — N.C.G.S. ch. 58 incl. Art. 10 captive sections, official; session-law pattern confirmed via SL2015-99
- https://delcode.delaware.gov/title18/c069/ — 18 Del. C. ch. 69 (captives), official, with Authenticated PDF
- https://le.utah.gov/xcode/Title31A/Chapter37/31a-37.html — Utah Code ch. 31A-37 (Captive Insurance Companies Act), official; section pattern 31A-37-SNNN.html
- https://www.bermudalaws.bm/Laws/Consolidated%20Law/1978/Insurance%20Act%201978 — Bermuda consolidated Insurance Act 1978
- https://www.bma.bm — Bermuda Monetary Authority (guidance PDFs under /viewPDF/documents/)
- https://legislation.gov.ky — Cayman Islands consolidated legislation portal
- https://www.cima.ky/insurance — CIMA insurance regulatory page (Insurance Act oversight)
- https://www.irs.gov/pub/irs-drop/rp-25-32.pdf + https://www.irs.gov/irb/2025-45_IRB — Rev. Proc. 2025-32 (2026 inflation adjustments), release + IRB publication
- https://www.irs.gov/pub/irs-drop/rp-24-40.pdf — Rev. Proc. 2024-40 (2025 inflation adjustments incl. § 831(b)(2)(A)(i) premium limit)
- https://www.ecfr.gov/current/title-26 — eCFR Title 26 (Treasury regs, current unofficial compilation)
- https://uscode.house.gov/browse/prelim@title26&edition=prelim — OLRC official U.S. Code Title 26
- https://www.govinfo.gov — official USCODE/CFR/FR collections (bulkdata path confirmed for ECFR title-26)
- https://www.ustaxcourt.gov — U.S. Tax Court (DAWSON opinion/docket search)
