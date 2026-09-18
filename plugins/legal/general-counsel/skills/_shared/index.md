---
type: index
title: General Counsel shared contracts
description: Map of the five contract files every GC surface (deployed service, plugin skills, specialist agents) binds to.
resource: plugin/skills/_shared/
tags: [legal, contracts, zero-fabrication, house-posture]
timestamp: 2026-09-16
---

# _shared/ — binding contracts (OKF-style index)

| Doc | type | What it binds |
|---|---|---|
| [zero-fabrication.md](zero-fabrication.md) | policy | No fabricated authorities, docket numbers, or rule text — ever. Unverifiable ⇒ "ASSUMPTION (unverified)". |
| [posture.md](posture.md) | policy | The house posture: deal counsel to a sponsor. ANGLES after the holding, every exposure priced with its survival structure, banned hedges, four-item floor surfaced only in LIMITATIONS. Rendered into supervisor.md at its marker and appended to every specialist prompt. |
| [output-format.md](output-format.md) | policy | Conclusion-first, angles-second memo shape: holding, ANGLES, badged citations, PRICED EXPOSURE/CONFIDENCE, sequenced NEXT ACTIONS, limitations. |
| [ontology.md](ontology.md) | reference | Business-dimension layer (first-principles / PE lens) and its grounding rules. |
| [supervisor.md](supervisor.md) | prompt | The GENERAL_COUNSEL supervisor: house-posture section (posture.md rendered at `<!-- posture:full -->`), routing table with angle-coverage rules, synthesis duties, JSON envelope. |
| [pe-precedent.md](pe-precedent.md) | reference | Verified snapshot of benchmark cases and statutes where a private-equity sponsor or portfolio company is plaintiff or defendant (Delaware, federal, Texas). Orientation for every lens under the house posture; not loaded into prompts. |
| [texas-recent-legislation.md](texas-recent-legislation.md) | reference | Verified enactment index for the 89th Texas Legislature (2025) and the November 2025 constitutional amendments, tagged by practice area; each `legal-*/references/texas.md` links here. Not loaded into prompts. |
| [jurisdiction-coverage.md](jurisdiction-coverage.md) | reference | Per-state matrix of what the suite can ground (statute text tool, bill tool, weekly cron, doctrine file) and the primary-source facts behind it. Not loaded into prompts. |

The first five files are read by `app/agents/prompts.py` at import — they ARE the
production prompts. The three `reference` rows below them are read at runtime by
agents and skills only. This index is inert to the loader (it reads only the five
named files) and exists so knowledge consumers (Claude Code, OKF-compatible
catalogs) can discover the contracts. Frontmatter follows Google's Open
Knowledge Format v0.1 draft (type/title/description/resource) — compatible,
not dependent.
