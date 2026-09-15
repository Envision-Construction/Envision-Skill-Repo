---
last_updated: "2026-09-14"
update_cadence: quarterly
next_review: "2026-12-14"
data_vintage: "Q3 2026"
sources:
  - "FRED / ICE BofA indices"
  - "PitchBook LCD (via ABF Journal, Yahoo Finance)"
  - "ZCG credit briefing, PGIM, Trepp"
  - "Lincoln International, SPP (via Kadenwood Credit Terms Monitor)"
  - "CBRE"
  - "Internal estimates (expected loss, liquidity, duration, protection columns)"
---

# Cross-Asset Relative Value Benchmarks

Use this file for current cross-asset benchmark inputs and market snapshots. For the normalization methodology, structural assessment framework, and decision workflow, see `skills/portfolio-investment-process/references/cross-asset-relative-value-framework.md`.

## Current Benchmark Matrix

### Current Spread/Yield Landscape (Q3 2026, spreads as of August 31 to September 11, 2026)

Spread column refreshed in the 2026-09-14 pass; bracketed numbers resolve in the Source Key. Expected Loss, Liquidity, Duration, and Structural Protection are internal structural assumptions carried from Q1 2026, not market data, and were not re-verified. Loss-Adjusted Spread is recomputed as spread minus expected loss.

| Asset Class | Typical Spread (bps) | Expected Loss (bps/yr) | Loss-Adjusted Spread | Liquidity | Duration (yrs) | Structural Protection |
|---|---|---|---|---|---|---|
| IG Corporate (BBB) | 97 [1] (index 80 [2]) | 5-10 | 87-92 | High | 5-7 | Incurrence covenants |
| HY Bond (BB) | 150 [3] | 30-60 | 90-120 | Medium-High | 4-6 | Incurrence covenants |
| Leveraged Loan (B) | 428-470 index level [4][5]; single-B not found | 80-150 | 278-390 | Medium | 3-5 (floating) | Mostly cov-lite |
| CLO AAA | 128 [4]; marketing inside 120 [6] | <1 | 127-128 | Medium | 3-5 (floating) | Subordination + OC/IC |
| CLO BBB | 274 [4] | 20-50 | 224-254 | Low-Medium | 5-7 (floating) | Subordination |
| CLO BB | 575 [4] | 100-200 | 375-475 | Low | 6-8 (floating) | Thin subordination |
| Private Credit (1st lien, sponsored core MM) | 500-509 [7][8] | 100-175 | 325-409 | Very Low | 5-7 (floating) | Maintenance covenants |
| Private Credit (unitranche) | 500-549 core MM [8]; 550-750 lower MM [9] | 125-225 | 275-625 | Very Low | 5-7 (floating) | Maintenance covenants |
| CRE Senior (stabilized, perm over UST) | 204 commercial / 162 multifamily [10] | 15-40 | 122-189 | Low | 5-10 | LTV/DSCR covenants |
| CRE Bridge/Transitional (over SOFR) | 350-500 institutional / 500-700 debt fund [11] (low confidence) | 75-175 | 175-625 | Very Low | 2-3 (floating) | Reserves, milestones |
| CMBS AAA (conduit, secondary) | mid 70s [6] | <5 | 65-80 | Medium-High | 4-6 | Subordination + reserves |
| ABS AAA (auto prime, 3-yr) | 40 [12] | <1 | 39-40 | High | 1-2 | Subordination + excess spread |

### Spread Moves Since Q1 2026

| Asset Class | Q1 2026 | Q3 2026 | As of | Confidence |
|---|---|---|---|---|
| IG Corporate (BBB) | 120-150 | 97 | 9/11 | two-source [1][2] (index ~70 in June [13]) |
| HY Bond (BB) | 250-325 | 150 | 9/11 | official [3]; index-level corroboration only |
| Leveraged Loan (B) | 350-450 | 428-470 (index) | 5/31; 9/11 | medium (two indices, two dates) |
| CLO AAA | 130-150 | 128 | 8/31 | two-source [4][6] |
| CLO BBB | 350-425 | 274 | 8/31 | single [4] |
| CLO BB | 600-750 | 575 | 8/31 | single [4] |
| Private Credit (1st lien) | 550-700 | 500-509 | Q2 to Aug | two-source [7][8] |
| Private Credit (unitranche) | 625-800 | 500-549 / 550-750 | Q2; Jul | medium [8][9] |
| CRE Senior (stabilized) | 200-300 | 204 / 162 | Q2 | single [10] (CBRE); Trepp: at most 3 bps of movement in August [14] |
| CRE Bridge/Transitional | 400-600 | 350-500 / 500-700 | May | low [11] (lender marketing); CRE CLO AAA +130-140 as funding proxy [6] |
| CMBS AAA | 100-130 | mid 70s | 8/24 | single [6]; Trepp: AAA in 2-4 bps in August [14] |
| ABS AAA (auto) | 60-80 | 40 | 8/6 | single [12]; PGIM ABS index 85 bps, 35 over corporates [6] |

**Reading the move.** Quality bifurcation dominates: BB and IG tightened 100-175 bps while CCC widened about 350 bps (see `references/market-benchmarks.md`, section 3). Securitized paper (CMBS AAA, auto ABS AAA, CLO mezz) tightened the most. Private credit repriced wider on the spread line even as the syndicated market tightened, so the private-credit premium over broadly syndicated loans (162 bps on new issue) is now measurable rather than assumed. Base rates fell 75 bps while the curve rose 70-80 bps, so compare all-in yields, not spreads alone.

*Note: Ranges reflect market conditions as of data vintage. Consult `references/market-benchmarks.md` for current levels, the full source key, and the list of metrics not re-verified in the Q3 pass.*

## Source Key

[1] https://fred.stlouisfed.org/series/BAMLC0A4CBBB
[2] https://streetstats.finance/rates/corporates
[3] https://fred.stlouisfed.org/series/BAMLH0A1HYBB
[4] https://www.zcg.com/briefing (Global Economic & Credit Market Briefing, week ending September 11, 2026)
[5] https://www.polencapital.com/sites/default/files/2026%20High%20Yield%20and%20Leveraged%20Loan%20Mid-Year%20Review%20and%20Outlook_Opportunity%20Beneath%20the%20Surface.pdf (Morningstar LSTA 428 bps, 5/31)
[6] https://www.pgim.com/us/en/intermediary/insights/featured/weekly-view-from-the-desk (August 24, 2026)
[7] https://finance.yahoo.com/markets/stocks/articles/q2-us-private-credit-wrap-213115638.html (PitchBook LCD Q2 wrap)
[8] https://www.abfjournal.com/middle-market-debt-weekly-odds-of-a-fed-hike-push-past-85/ (PitchBook LCD data)
[9] https://kadenwoodgroup.com/perspectives/credit-terms-monitor (SPP Jul-2026, Lincoln 5/1/2026)
[10] https://www.cbre.com/insights/figures/q2-2026-us-capital-markets-report
[11] https://avanacapital.com/business-loans/commercial-bridge-loan-guide/
[12] https://x.com/AutoFinanceNews/status/2087668130864656866 (J.P. Morgan data)
[13] https://www.chicagoatlantic.com/private-credit-markets-q2-2026-update/
[14] https://www.trepp.com/trepptalk/august-2026-rates-and-spreads
