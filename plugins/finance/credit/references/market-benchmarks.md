---
last_updated: "2026-09-14"
update_cadence: quarterly
next_review: "2026-12-14"
data_vintage: "Q3 2026"
sources:
  - "FRED / ICE BofA indices"
  - "NY Fed, CME Term SOFR, US Treasury"
  - "PitchBook LCD (via Voya, ABF Journal, Yahoo Finance)"
  - "Fitch Ratings, Federal Reserve FEDS Notes"
  - "Guggenheim / J.P. Morgan structured credit"
  - "Lincoln International, SPP, Houlihan Lokey (via Kadenwood Credit Terms Monitor)"
  - "CBRE, Trepp, PGIM, ZCG credit briefing"
  - "SIFMA"
---

# Market Benchmarks Reference

**Last Updated:** September 14, 2026 (data as of September 11, 2026 unless a row says otherwise)
**Update Cadence:** Quarterly
**Next Review:** December 2026

**How to read this file.** Every figure carries a bracketed source number that resolves in the Source Key at the end. Confidence tags: **two-source** (two independent publishers agree), **official** (one primary data source such as FRED, Treasury, or CME), **single** (one secondary publisher), **stale** (Q1 2026 value, not re-verified in the Q3 pass). Never cite a stale row as current; say "Q1 2026 vintage" or go find the number.

---

## 1. Base Rate Environment

| Metric | Current Level | As of | Confidence | Q1 2026 file |
|--------|---------------|-------|------------|--------------|
| SOFR (Overnight) | 3.62% | 9/11 | two-source [1][2] | 4.25-4.35% |
| Term SOFR 1-Month | 3.82% (CME); 3.77-3.79% (ZCG) | 9/11 | two-source [3][4] | 4.30% |
| Term SOFR 3-Month | 3.89% (CME); 3.84-3.86% (ZCG) | 9/11 | two-source [3][4] | 4.35% |
| Term SOFR 6-Month | 4.04% (CME); 3.97-3.99% (ZCG) | 9/11 | two-source [3][4] | 4.40% |
| Term SOFR 12-Month | 4.28% | 9/11 | official [3] | 4.45% |
| Fed Funds Target | 3.50-3.75% (EFFR 3.63%) | 9/14 | two-source [5][6][4] | 4.25-4.50% |
| 2-Year Treasury | 4.63% (4.56% on 9/10) | 9/11 | two-source [7][8] | 3.85-4.00% |
| 10-Year Treasury | 4.96% (4.95% on 9/10) | 9/11 | two-source [7][9][4] | 4.10-4.25% |
| 30-Year Treasury | 5.35% | 9/11 | two-source [7][4] | not tracked |

**Context:** The Fed has cut 75 bps since Q1 (target now 3.50-3.75%), yet the curve sold off: the 2-year and 10-year sit 70-80 bps above the Q1 file, and CME FedWatch priced roughly 85% odds of a 25 bp hike at the September 16 FOMC [6]. Term SOFR slopes upward from 3.82% (1M) to 4.28% (12M). Do not underwrite to "gradual moderation"; model a flat-to-higher policy path with a steeper curve.

---

## 2. Leveraged Loan Spreads

### First Lien Term Loan B (TLB) by Rating

Rating-level new-issue spread, OID, and bid-ask were **not found** in the Q3 pass (the LCD Relative Value Snapshot is paywalled). The table below is **stale Q1 2026 vintage**; use the verified reference points that follow it.

| Rating | Bid-Ask Spread | OID Range | New-Issue Coupon | Status |
|--------|---|---|---|---|
| BB | 325-375 bps | 2.0-3.5% | SOFR+350-400 | stale |
| B | 400-475 bps | 3.5-5.0% | SOFR+425-500 | stale |
| B- | 475-550 bps | 4.5-6.0% | SOFR+500-575 | stale |
| CCC | 600-725 bps | 6.5-8.5% | SOFR+625-750 | stale |

### Verified Loan Market Reference Points (Q3 2026)

| Metric | Current | As of | Confidence |
|---|---|---|---|
| Loan index discounted spread / yield | 470 bps / 9.17% (CS Leveraged Loan Index, swap-adjusted) [4]; 428 bps / 8.09% (Morningstar LSTA, 5/31) [10]; index yield ~8.1% (Aug) [11] | 9/11; 5/31 | medium (different indices and dates) |
| Syndicated new-issue clearing spread | ~S+340 implied (private-credit new-issue S+502 less the 162 bp premium) [6]; Fed staff median S+400 on 2025 issuance [12] | 3 months to 8/31 | medium |
| Average secondary bid | 95.58 (8/31) [13]; 95.80 (9/8) [14] | Aug-Sep | two-source |
| CCC loan cohort | S&P CCC loan index S+1,794 (+323 bps YTD) [4]; CCC loans carry an 800+ bp yield premium over CCC HY [10] | 8/31; 5/31 | medium |
| Single-B loans vs single-B HY | B loans yield ~95 bps over B HY (B HY effective yield 7.49%) [10] | 5/31 | single |
| Repricing tape | GMR $2.9B TLB repriced S+325 to S+275; Sophos $1.67B refi talk S+500-525 at 97 OID [6] | 9/11 | anecdotal |

### Second Lien / Unitranche Pricing

| Product | Spread Range | As of | Confidence | Q1 2026 file |
|---------|---|---|---|---|
| Second Lien ($15-40M EBITDA) | SOFR+725-825 | 5/1 | single [17] (Lincoln) | SOFR+550-700 |
| Unitranche, sponsored core middle market | SOFR+500-509 average (Q2 sponsored LBO S+509 vs S+474 in Q1; plain-vanilla S+500, up from S+450 late 2025) | Q2; Aug | two-source [18][6] | SOFR+425-525 |
| Unitranche, lower middle market (<$10M EBITDA) | SOFR+550-750 | Jul 2026 | single [17] (SPP) | SOFR+525-650 |

**Clearing Spreads:** ~S+340 implied (TLB) [6]; S+725-825 (2L) [17]
**Market Size:** ~$1.4T leveraged loans outstanding, end-2025 [12] (single); YTD issuance $269B ex-repricing through August, down 12% YoY [13]; Q2 gross ~$220B, net $73B [15][16] (two-source on gross)

---

## 3. High Yield Bond Spreads

### Option-Adjusted Spread (OAS) by Rating (ICE BofA via FRED)

| Rating | Current OAS | As of | Confidence | Q1 2026 file |
|--------|---|---|---|---|
| BB | 150 bps | 9/11 | official [19]; index-level corroboration: ICE HY 267 [20], 270 on 8/17 [21], 274 on 5/31 [10] | 285-335 bps |
| B | 273 bps | 9/11 | official [22] | 420-480 bps |
| CCC | 1,076 bps | 9/11 | official [23]; ICE CCC 1,018 on 8/17 [21] | 650-800 bps |

52-week ranges by rating: **not found**. The HY index traded 274-328 bps over 2026 through May [10].

**Quality bifurcation:** BB and B are roughly 150-175 bps tighter than the Q1 file while CCC is roughly 350 bps wider. Index-level HY spreads misprice CCC names badly; use the rating-level series.

### New-Issue Coupon Ranges

Rating-level new-issue coupons were **not found**. ICE index effective yields (secondary market) are the proxy; the Q1 coupon column is stale.

| Rating | Index Effective Yield (proxy) | As of | Confidence | Q1 2026 coupon range (stale) |
|--------|---|---|---|---|
| BB | 6.28% | 9/11 | official [24]; HY index YTW 7.16% [20], 7.58% swap-adjusted [4] | 5.50-6.75% |
| B | 7.49% | 9/11 | official [25]; BondBloxx B-rated ETF 30-day SEC yield 6.93% (8/31) [26] | 7.00-8.50% |
| CCC | 15.44% | 9/11 | official [27] | 10.00-12.50% |

Pricing conventions (par to 101 for BB, par to 102 for B, 98-102 for CCC) are Q1 vintage and structural; treat as guidance, not data.

**Primary volume:** 13 deals / $12.0B priced in the week to 9/11 [4]; $1.7B / 4 deals in the week of 8/21 [28] (two-source on the tape).
**Market Size:** ~$1.5T face value outstanding (low confidence, single [29]; the Q1 file's $2.0T is not corroborated); issuance $189B YTD through early July, up 20% YoY [11] (single). SIFMA total corporate issuance $1,899.8B through August, up 29.8%, not split IG/HY [30].

---

## 4. CLO Market Data

### Issuance & AUM
- **2025 CLO Issuance:** ~$208B across 429 deals [31] (single; Q1 file said $175-190B)
- **2026 YTD Issuance:** $112.1B through 9/3, down 21% YoY (PitchBook LCD) [13]; H1 $55B, down 22% (J.P. Morgan via Guggenheim) [32]; Q2 $23B, the lowest quarter in about 2.5 years, August $19B across 40 deals [16]. Provider counts differ; cite the provider with any figure you use.
- **Resets / Refis:** Q2 $49B resets, $41B refis [16] (single)
- **US CLO Outstanding:** ~$977B (FSB) [33]; "about $1 trillion" (Nuveen) [34] (medium). Global figure **not found**; the Q1 file's $825B global / $600B US is stale.
- **CLO ETF AUM:** above $50B (7/2) [35]; JAAA alone above $30B (8/13) (two-source)

### Tranche Pricing (New-Issue Spreads, 8/31)

| Tranche | Spread to SOFR | Confidence | Q1 2026 file | Indicative yield (3M term SOFR 3.89% + spread) |
|---------|---|---|---|---|
| AAA | SOFR+128 [4]; deals marketing inside S+120 in late August [28] | two-source | SOFR+90-120 | ~5.1-5.2% |
| AA | SOFR+158 [4] | single | SOFR+150-200 | ~5.5% |
| A | SOFR+184 [4] | single | SOFR+220-280 | ~5.7% |
| BBB | SOFR+274 [4]; Carlyle: BBB/BB still wider than YTD tights [16] | single | SOFR+350-425 | ~6.6% |
| BB | SOFR+575, in from S+645 in July [4] | single | SOFR+550-675 | ~9.6% |
| B | not found | — | SOFR+900-1150 (stale) | — |
| Equity | no market-wide figure; CCIF's Q2 new equity purchases at 13% GAAP yield, ~20% cash-on-cash [16] | fund-level | 12-16% | — |

The indicative yield column is computed here (3M term SOFR [3] plus spread); it is not a sourced figure.

**Arbitrage:** no bps figure found; managers describe the arbitrage as challenged with excess spread narrowing [16][13]. The Q1 file's 200-280 bps is stale. Mezz has tightened sharply (BBB from 350-425 to 274) while AAA is flat to slightly wider (90-120 to 128), which is what a compressed arbitrage looks like from the liability side.

---

## 5. Private Credit Spreads

### Direct Lending (Unitranche Equivalent)

| Borrower Quality | SOFR Spread | Total Yield | As of | Confidence | Q1 2026 file |
|---|---|---|---|---|---|
| Sponsor-backed, EBITDA >$20M | +500-509 [18][6] | Houlihan Lokey Private Performing Credit Index 9.97% (spread 576) Q2 [17]; Sixth Street Lending Partners weighted-average spread 620 bps, total yield 10.2% Q2 [36] | Q2; 3 months to 8/31 | two-source on spread | +425-525 / 8.65-9.60% |
| Mid-market, EBITDA $10-20M | not found; bracketed by S+500-549 (core, 52% of sponsor deals [6]) and S+550-750 (lower MM) | not found | — | stale | +525-650 / 9.60-10.85% |
| Lower mid-market, <$10M EBITDA | unitranche +550-750; senior bank +350-425; new-issue OID 98-99 (<$20M EBITDA) | not found | Jul 2026; 4/30 | single [17] (SPP; Houlihan Lokey on OID) | +675-850 / 11.15-12.85% |

### Secondary / Mezzanine / Junior Capital
- **Subordinated debt, $15-40M EBITDA:** 11.0-13.5% all-in (Lincoln, 5/1) [17]; **junior / mezz, <$10M EBITDA:** 13.0-16.0% all-in (SPP, Jul) [17] (medium: two segments, one aggregator). Q1 file: SOFR+750-1000 (8.75-12.00%).
- **Preferred equity, $40-100M EBITDA:** 13.5-16.5% (Lincoln, 5/1) [17] (single). Q1 file's sub-debt row (SOFR+1000-1500+) is stale.
- **Private credit premium over broadly syndicated loans:** 162 bps on new issue, 3 months to 8/31 [6]; Blue Owl cites a 200-250 bp trailing three-year yield premium [37] (medium).
- **Defaults (Q2):** Proskauer PCDI 2.51%; KBRA 3.3%; Fitch middle-market 4.9% (record); Blue Owl portfolio ~1.0% [17][37]. Definitions differ; name the index when quoting.

**Market Size:** AUM ~$1.7T global at start-2026 (Preqin) [38]; ~$2T (S&P); ~$1.4T US corporate private credit outstanding, end-2025 (Federal Reserve) [12] (medium; definitional spread). Q1 file: $1.8T.
**Deployment:** direct-lending volume $107B in H1 ($74.1B Q1 + $32.9B Q2) [18]; direct-lending LBO volume $30.2B YTD, down 21% [39] (two-source). **Fundraising:** H1 2026 $190B, up 53% YoY (With Intelligence via [40], single).

---

## 6. Market Size & Volume Summary

| Segment | Total Outstanding | 2026 Issuance / Volume to Date | Confidence |
|---------|---|---|---|
| Leveraged Loans | ~$1.4T (end-2025) [12] | $269B YTD Aug ex-repricing, -12% YoY [13] | single / medium |
| High Yield Bonds | ~$1.5T face (weak) [29] | $189B YTD early July, +20% YoY [11] | low / single |
| CLOs | ~$977B-$1T US [33][34]; global not found | $112B YTD 9/3, -21% YoY [13] | medium |
| Private Credit | $1.7-2.0T global [38]; $1.4T US corporate [12] | direct-lending volume $107B H1 [18] | medium |
| Structured (ABS / CMBS / RMBS) | see Structured Finance section | H1: ABS $137B (+22%), CMBS $99B (+33%), RMBS $82B (+22%), CLO $55B (-22%) [32]; ABS YTD Aug $356.3B, +2.3% (SIFMA, broader definition) [41] | two-source on direction |

No total is given. The outstanding figures mix face value, AUM, and scopes (US versus global, corporate versus all private credit), so a sum would be a false number.

---

## 7. SOFR Floor Conventions

**SOFR Floor Conventions:** See `references/typical-deal-parameters.md` for SOFR floor conventions by loan type and market segment.

---

## 8. Pricing Grid Conventions

### Typical Leverage-Based Step-Downs (Loan Pricing)

| Leverage Metric | Spread Adjustment |
|---|---|
| Total Debt/EBITDA > 5.0x | SOFR + Base Spread |
| Total Debt/EBITDA 4.0-5.0x | SOFR + Base - 25 bps |
| Total Debt/EBITDA 3.0-4.0x | SOFR + Base - 50 bps |
| Total Debt/EBITDA < 3.0x | SOFR + Base - 75 bps |

### Interest Coverage Step-Ups

| EBITDA/Interest | Spread Adjustment |
|---|---|
| < 2.0x | +25 bps step-up |
| 2.0-2.5x | No adjustment |
| > 2.5x | -25 bps step-down |

---

## Notes for Analysts

- **Rates:** policy down 75 bps since Q1, curve up 70-80 bps, market pricing a hike. Floating-rate coupons fell with SOFR; fixed-rate refinancing got more expensive. Model both.
- **Quality bifurcation:** BB/B OAS ~150-175 bps tighter than Q1, CCC ~350 bps wider; CCC loans at S+1,794. Never apply an index-level HY or loan spread to a CCC credit.
- **Private credit repriced wider:** unitranche from S+425-525 to ~S+500-509, second lien to S+725-825, mezz to 11-16% all-in, with a 162 bp premium over syndicated. The Q1 "private credit is cheap" framing no longer holds.
- **CLO liabilities:** mezz much tighter, AAA flat to wider, arbitrage described as challenged; issuance down about a fifth YoY.
- **Regional Variation:** European direct lending spreads typically 50-100 bps tighter than US equivalents (structural, not re-verified)
- **Covenant Trends:** Continued loosening; most sponsor-backed deals "cov-lite" in the SOFR+400-500 range (structural)
- **Liquidity Premium:** Wider spreads on smaller <$50M facilities; tighter on institutional scale (structural)
- **Cross-Border:** SOFR-based deals 95%+ of new US issuance; sterling SONIA alternatives declining (structural)

---

## 9. Commercial Real Estate Market Benchmarks

### Verified CRE Debt Reference Points (Q3 2026)

| Metric | Value | As of | Confidence |
|---|---|---|---|
| Permanent loan spread over UST, commercial (5-10 yr fixed) | 204 bps | Q2 | single [45] (CBRE) |
| Permanent loan spread over UST, multifamily (5-10 yr fixed) | 162 bps | Q2 | single [45] |
| Average mortgage rate / LTV / DSCR | 5.7% / 59.6% commercial, 63.3% multifamily / 1.43x | Q2 | single [45] |
| All-property cap rate | 6.3% | Q2 | single [45] |
| Balance-sheet lender spreads | "tight"; moved at most 3 bps in August | Aug | direction only [46] (Trepp) |
| Bridge / transitional | SOFR+350-500 institutional; SOFR+500-700 debt fund | May 2026 | low [47] (lender marketing, not a data provider) |
| CRE CLO AAA new issue (bridge funding proxy) | +130-140 | 8/24 | single [28] (PGIM) |

### Cap Rate Ranges by Property Type (stale: Q1 2026 vintage)

CBRE's Q2 2026 all-property cap rate is 6.3% [45]. The property-type ranges below were not re-verified in the Q3 pass.

| Property Type | Cap Rate Range | Notes |
|---|---|---|
| Multifamily | 4.5–6.5% | Most competitive; cap rates tighten for stabilized assets |
| Industrial | 5.0–7.0% | Benefited by e-commerce logistics demand |
| Office — CBD | 6.5–8.5% | Elevated due to remote work headwinds |
| Office — Suburban | 7.0–9.5% | Higher caps reflect greater uncertainty |
| Retail — Anchored | 6.0–8.0% | Stable cash flows; lower caps for grocery-anchored |
| Retail — Unanchored | 7.5–10.0% | Wider range; tenant credit dependent |
| Hospitality — Select Service | 7.5–9.5% | Operational risk premium factored in |
| Self-Storage | 5.5–7.5% | Resilient asset class; steady occupancy |
| Medical Office | 5.5–7.0% | Steady demand from healthcare users |
| Data Center | 5.0–6.5% | Low-cap due to long-term lease stability |

### CRE Mortgage Spreads by Lender Type (stale: Q1 2026 vintage)

Use the CBRE perm spreads (204 / 162 bps over UST) and the bridge ranges above for current levels. This lender-type grid was not re-verified.

| Lender Type | Spread Range | Typical Coupon | LTV | DSCR |
|---|---|---|---|---|
| Agency (GSE-eligible) | T+140–200 bps | 5.40–6.00% | 60–75% | ≥1.25x |
| CMBS Conduit | T+160–250 bps | 5.50–6.50% | 65–80% | ≥1.20x |
| Life Company | T+130–180 bps | 5.30–5.80% | 60–75% | ≥1.30x |
| Bank Portfolio | SOFR+175–300 bps | 5.75–6.65% | 65–80% | ≥1.15x |
| Bridge/Debt Fund | SOFR+300–550 bps | 7.25–9.75% | 70–85% | ≥1.10x (interest-only) |

### CMBS Market Snapshot

| Metric | Value | As of | Confidence |
|--------|-------|-------|------------|
| H1 2026 CMBS issuance | $99B, up 33% YoY | H1 | single [32] (J.P. Morgan via Guggenheim) |
| 2025 issuance (stale) | $85–95B | — | Q1 vintage |
| SASB vs. Conduit mix (stale) | 35% SASB / 65% Conduit | — | Q1 vintage |

**CRE Delinquency Rates:** See `references/default-recovery-rates.md` (CRE Default & Recovery section) for current delinquency rates by property type.

**Update Cadence:** Quarterly (track rate environment, delinquency trends, property-type performance)

---

## Structured Finance Market Benchmarks

Current market conditions for asset-backed securities, project finance, and securitized credit markets (data as of August-September 2026 where marked; otherwise Q1 2026 vintage, stale).

### ABS Spreads by Sector (New-Issue)

| Sector | AAA Spread | Tranche Spread Range | Status |
|--------|-----------|---------------------|--------|
| Auto Prime | +40 bps (3-yr prime AAA, 8/6) [48] (J.P. Morgan data via Auto Finance News) | AAA to BBB: T+40 to T+350 (stale) | AAA verified, single; rest stale (Q1: T+40-60) |
| Auto Subprime | T+80–120 bps | AAA to B: T+80 to T+800 | stale |
| Credit Card | T+35–55 bps | AAA to A: T+35 to T+200 | stale |
| Student Loan | T+50–80 bps | AAA to BBB: T+50 to T+300 | stale |
| Equipment | T+50–75 bps | AAA to A: T+50 to T+250 | stale |
| RV Loans | T+75–110 bps | AAA to BBB: T+75 to T+400 | stale |

**Context:** PGIM puts the ABS index at 85 bps, about 35 bps over corporates (8/24) [28]. Auto prime remains the tightest sector. Subprime and credit-card default commentary in the Q1 file (5-7% and 0.5-1%) was not re-verified.

### RMBS Spreads (stale: Q1 2026 vintage)

| Product | AAA Spread | Notes |
|---------|-----------|-------|
| Agency MBS (Current Coupon) | T+80–140 bps | Implicit government backing; liquid |
| Non-Agency Prime Jumbo AAA | T+100–160 bps | Higher default risk vs. agency |
| Non-Agency Alt-A AAA | T+150–220 bps | Legacy; lower credit quality |

**Market Snapshot:** RMBS issuance $82B in H1 2026, up 22% YoY [32] (single, J.P. Morgan via Guggenheim). Agency MBS outstanding (~$12T) is Q1 vintage.

### CMBS Spreads

| Product | Spread | As of | Confidence | Q1 2026 file |
|---------|--------|-------|------------|--------------|
| Conduit AAA | mid +70s (secondary) | 8/24 | single [28]; Trepp: AAA in 2-4 bps in August [46] | T+90–140 bps |
| SASB AAA (floating) | +120–130 | 8/24 | single [28] | T+80–130 bps |
| Conduit BBB- | ~+400 | 8/24 | single [28]; Trepp: BBB/BBB-/A in ~30 bps in August [46] | not tracked |

**Delinquency Context:** See `references/default-recovery-rates.md` (CRE Default & Recovery section) for current CMBS delinquency rates by property type.

### Securitized Issuance Volume

| Product | 2026 to Date | Confidence | Q1 2026 estimate (stale) |
|---------|--------------|------------|--------------------------|
| ABS (J.P. Morgan definition) | $137B H1, +22% YoY [32] | single | ~$310–350B full year |
| ABS (SIFMA definition, broader) | $356.3B YTD Aug, +2.3% YoY [41] | official | — |
| CMBS | $99B H1, +33% YoY [32] | single | ~$80–100B full year |
| RMBS | $82B H1, +22% YoY [32] | single | non-agency ~$90–110B full year |
| CLO | $55B H1, -22% YoY [32]; $112B YTD 9/3 (LCD) [13] | two-source on direction | 180–210B full year |

The two ABS figures differ by definition, not by error; name the provider whenever you quote one. Auto ABS, credit card ABS, equipment ABS, and agency RMBS sub-totals were not re-verified.

### Project Finance Spreads (Infrastructure Debt) (stale: Q1 2026 vintage, not researched in the Q3 pass)

| Rating | BBB Project Bond Spread | BB Project Bond Spread |
|--------|--------------------------|----------------------|
| Investment-Grade Infrastructure | T+150–220 bps | N/A (IG category) |
| BB-Rated Infrastructure | T+250–350 bps | N/A (below BBB) |
| Typical Senior Leverage | 70–75% | Range for projects |

**Examples** (illustrative, Q1 vintage):
- Motorway concession (toll revenue, 25-year): BBB, T+180 bps
- Wind farm (PPA-backed, strong offtake): BBB, T+150 bps
- Water treatment (municipal revenue-backed): BBB, T+200 bps
- Port expansion (traffic-dependent): BB, T+300 bps

**Market Size** (Q1 vintage): Global infrastructure debt market ~$200–250B annual issuance; US/Europe dominant. Asian/EM infrastructure growing 15–20% annually.

---

## Not Re-Verified in the Q3 2026 Pass

Treat every item below as Q1 2026 vintage. Find a current source before citing.

- TLB new-issue spread, OID, and bid-ask by rating (BB / B / B- / CCC)
- HY new-issue coupon ranges by rating; HY 52-week OAS ranges by rating
- CLO single-B tranche spread; market-wide CLO equity return; arbitrage in bps; global CLO AUM
- Direct lending at the $10-20M EBITDA cut; a second source for HY issuance, loan outstanding, and 12M term SOFR
- CRE cap rates by property type; the lender-type mortgage grid; CRE bridge spreads from a data provider (only lender marketing found)
- ABS sectors other than auto prime AAA; RMBS spreads; project finance spreads and examples

---

## Source Key

Research pass 2026-09-14 via Firecrawl search and scrape; [4] was read locally with pdftotext after the PDF parser timed out.

[1] https://fred.stlouisfed.org/series/SOFR
[2] https://www.newyorkfed.org/markets/reference-rates/sofr
[3] https://www.cmegroup.com/market-data/cme-group-benchmark-administration/term-sofr.html
[4] https://www.zcg.com/briefing (Global Economic & Credit Market Briefing, week ending September 11, 2026, PDF)
[5] https://fred.stlouisfed.org/series/DFEDTARU and /DFEDTARL
[6] https://www.abfjournal.com/middle-market-debt-weekly-odds-of-a-fed-hike-push-past-85/
[7] https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202609
[8] https://fred.stlouisfed.org/series/DGS2
[9] https://fred.stlouisfed.org/series/DGS10
[10] https://www.polencapital.com/sites/default/files/2026%20High%20Yield%20and%20Leveraged%20Loan%20Mid-Year%20Review%20and%20Outlook_Opportunity%20Beneath%20the%20Surface.pdf
[11] https://www.kkr.com/insights/high-yield-second-act
[12] https://www.federalreserve.gov/econres/notes/feds-notes/private-credit-and-leveraged-loan-markets-similarities-differences-and-substitution-20260811.html
[13] https://individuals.voya.com/insights/market-outlook/senior-loan-talking-points
[14] https://theleadpc.com/bloomberg-leveraged-lending-insights-9-7-2026/
[15] https://www.fitchratings.com/research/corporate-finance/us-levfin-markets-steady-in-2q26-credit-quality-divide-widens-31-07-2026
[16] https://www.marketbeat.com/earnings/reports/2026-8-19-carlyle-credit-income-fund-stock-2/
[17] https://kadenwoodgroup.com/perspectives/credit-terms-monitor (aggregates SPP Jul-2026, Lincoln 5/1/2026, Houlihan Lokey Q2 and 4/30/2026, KBRA, Proskauer)
[18] https://finance.yahoo.com/markets/stocks/articles/q2-us-private-credit-wrap-213115638.html (PitchBook LCD Q2 wrap)
[19] https://fred.stlouisfed.org/series/BAMLH0A1HYBB
[20] https://www.wsj.com/market-data/bonds/benchmarks
[21] https://www.abfjournal.com/middle-market-debt-weekly-refinancing-rush-meets-rate-realities/
[22] https://fred.stlouisfed.org/series/BAMLH0A2HYB
[23] https://fred.stlouisfed.org/series/BAMLH0A3HYC
[24] https://fred.stlouisfed.org/series/BAMLH0A1HYBBEY
[25] https://fred.stlouisfed.org/series/BAMLH0A2HYBEY
[26] https://bondbloxxetf.com/bondbloxx-b-rated-usd-high-yield-corporate-bond-etf/
[27] https://fred.stlouisfed.org/series/BAMLH0A3HYCEY
[28] https://www.pgim.com/us/en/intermediary/insights/featured/weekly-view-from-the-desk (August 24, 2026)
[29] https://www.linkedin.com/posts/bruce-richards-6035771a9_the-high-yield-bond-market-is-very-different-activity-7465371272051400704-zD_V
[30] https://www.sifma.org/research/statistics/us-corporate-bonds-statistics
[31] https://www.invesco.com/apac/en/institutional/insights/fixed-income/quarterly-case-for-senior-loans.html
[32] https://www.guggenheiminvestments.com/perspectives/sector-views/third-quarter-2026-structured-credit-outlook/
[33] https://www.fsb.org/uploads/P060526.pdf
[34] https://www.nuveen.com/global/investment-capabilities/fixed-income/a-closer-look-at-clo?type=us
[35] https://pitchbook.com/news/articles/bofa-us-clo-etfs-surge-past-50b-in-aum-inflows-total-10b-ytd
[36] https://sixthstreetlendingpartners.gcs-web.com/static-files/9d2f64fb-ae93-4a76-a6db-9f812b71f74e
[37] https://www.blueowl.com/insights/2026-mid-year-focus
[38] https://ctacquisitions.com/private-credit-market-2026/ (cites Preqin 2026 Global Alternatives Report)
[39] https://www.capstonepartners.com/insights/middle-market-leveraged-finance-report/
[40] https://angelinvestorsnetwork.com/market-analysis/private-credit-illiquidity-premium-spread-compression-2026
[41] https://www.sifma.org/research/statistics/us-asset-backed-securities-statistics
[42] https://fred.stlouisfed.org/series/BAMLC0A4CBBB
[43] https://streetstats.finance/rates/corporates
[44] https://www.chicagoatlantic.com/private-credit-markets-q2-2026-update/
[45] https://www.cbre.com/insights/figures/q2-2026-us-capital-markets-report
[46] https://www.trepp.com/trepptalk/august-2026-rates-and-spreads
[47] https://avanacapital.com/business-loans/commercial-bridge-loan-guide/
[48] https://x.com/AutoFinanceNews/status/2087668130864656866
