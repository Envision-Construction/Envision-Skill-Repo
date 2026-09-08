# Coverage Lapse & Cancellation-Notice Law

> Evergreen reference for the insurance-specialist skill.
>
> **Freshness:** class=`deadline-rule` verified=2026-07-04 sources=O.C.G.A. Title 33 text via the Justia 2024 Code mirror with its currency year recorded, the 2025 enrolled session law (SB 35 PDF), Georgia appellate opinions, Ga. Comp. R. and Regs.

`class` selects the threshold from the central table in
`scripts/check_authority_freshness.py`; the number is not written here so that
changing it is one edit. Past the threshold this file is a lead, not an
authority: re-verify the specific fact you need against the governing state's
current statute text, label what you cannot verify "ASSUMPTION (unverified)", and
record the stale header and its date in LIMITATIONS. Bump `verified` only after
re-verifying this file's own scope. The cross-reference to
[`current-legislation.md`](current-legislation.md) locates statute currency; it
does not transfer that file's freshness to this one.

Every day count below is a notice or cure period a party will rely on. Pull the
governing state's current section text the day you compute a date from it: a
missed cancellation, cure, or tail-election deadline cannot be un-missed, and the
Georgia counts here do not port to another state.

Scope: how policies terminate, what makes a termination legally effective, and how to forensically reconstruct a lapse. Georgia (O.C.G.A. Title 33) is the worked example; every state has an analogous scheme with different day counts and grounds. This is decision support, not legal advice — for a live dispute, pull the current statute text and controlling case law in the governing state.

## 1. Definitions — use these terms precisely

| Term | What it is | Coverage effect | Key forensic question |
|---|---|---|---|
| **Cancellation** | Insurer (or premium finance company via power of attorney) terminates mid-term | Coverage ends on the stated effective date — IF notice was statutorily compliant | Was every notice element satisfied? Defective notice = policy still in force |
| **Nonrenewal** | Insurer declines to issue a successor policy at expiration | Coverage runs to natural expiry, then stops | Was advance notice given within the statutory window? Late notice can extend coverage or expose the insurer |
| **Lapse** | Coverage gap from any cause — cancellation, nonrenewal without replacement, expiry, nonpayment | No coverage during the gap | Who bore the risk each day, and was the gap avoidable/curable? |
| **Rescission** | Insurer unwinds the policy for material misrepresentation in the application; treats it as never having existed | Retroactive to inception — claims already paid may be clawed back; premium typically returned | Was the misrepresentation material and (where required) intentional? Rescission is an affirmative defense the insurer must plead and prove |
| **Void ab initio** | Contract never formed — e.g., total failure of consideration (premium check bounced at inception), no insurable interest | Never any coverage; no cancellation notice required | Georgia codifies this: O.C.G.A. § 33-24-44(d.1) — notice requirements "shall not apply in any case where a binder or contract of insurance is void ab initio for failure of consideration" (verified 2026-07-04) |

Distinctions that matter in disputes: cancellation and nonrenewal are **prospective** and notice-gated; rescission and void-ab-initio are **retroactive** and notice-exempt. An insurer that wants retroactive effect will try to characterize a termination as rescission/void; an insured/claimant defends by forcing it into the cancellation box, where strict notice compliance applies.

## 2. Cancellation-notice statutes — Georgia worked example

All pinpoint cites below verified 2026-07-04 against the 2024 Georgia Code (Justia) plus 2025 session law. The structure — different notice periods by ground, mailing-proof rules, strict construction against the insurer — generalizes to essentially every state. **Do not port Georgia's day counts to another state**; the full state matrix belongs in current-legislation.md refreshes.

### 2.1 The general cancellation statute — O.C.G.A. § 33-24-44

- **Default (underwriting reasons)**: written notice ≥ **30 days** before effective date, delivered in person, electronically per § 33-24-14(d), or by first-class mail to the insured's last address of record and any lienholder, with the insurer "receiving the receipt provided by the United States Postal Service or such other evidence of mailing" — § 33-24-44(b).
- **Nonpayment of premium, or any policy in effect < 60 days**: notice may be cut to ≥ **10 days** — § 33-24-44(d).
- **Audit noncompliance**: if the insured refuses a policy-required premium audit, insurer may cancel on ≥ 10 days' notice by certified mail/statutory overnight, but only after **two documented notification efforts**, and no cancellation notice may be mailed within 20 days of the first effort — § 33-24-44(d.2).
- **Unearned premium**: pro-rata refund due by the cancellation date; if premiums are financed, unearned premium goes **to the premium finance company within 10 working days** of cancellation; audit-pending refunds due within 30 days after the audit — § 33-24-44(c)(1)-(2). Late refund penalty: 25% of the refund plus 18%/yr interest, capped at 50% of the refund — § 33-24-44(c)(3).
- **PFC cancellation carve-out**: when a premium finance company cancels under a power of attorney, the *insurer* owes the insured no § 33-24-44 notice — the PFC's own notice duties under § 33-22-13 govern instead, and the insurer must still notify governmental agencies/mortgagees/third parties — § 33-24-44(e). This carve-out is the single most exploited seam in lapse disputes; see § 4 and references/premium-finance.md.

### 2.2 Line-specific overlays

- **Personal auto — O.C.G.A. § 33-24-45**: grounds-limited cancellation regime for auto policies; incorporates § 33-24-44's mailing/delivery mechanics ("No notice of cancellation of a policy to which this Code section applies shall be effective unless mailed or delivered as prescribed in Code Section 33-24-44"). Statute at issue in *Reynolds* (§ 2.3). Day counts and permitted grounds: confirm against current text before relying.
- **Residential property (homeowners/fire) — O.C.G.A. § 33-24-46**: after 60 days in force, cancellation only for (A) nonpayment, (B) fraud/concealment/material misrepresentation, (C) substantial increase in hazard, or (D) violation of material policy terms — § 33-24-46(c)(2). Nonrenewal requires written notice — **60 days** effective 2026-01-01 (raised from 30 by 2025 Ga. SB 35 / Act 277, signed 2025-05-14; enrolled text strikes "30" for "60" in § 33-24-46(d)(1); verified against the enrolled bill PDF). Reduction-in-coverage: separate 30-day all-caps notice — § 33-24-46(d)(2). Cancellation for other-than-nonpayment and all nonrenewals must include Georgia FAIR Plan eligibility notice — § 33-24-46(e). Prohibited nonrenewal grounds include ≤ 2 non-fault claims in 36 months — § 33-24-46(j)(3). Trap for insureds: § 33-24-46(l) bars a wrongful-nonrenewal claim unless the insured filed a written objection with the insurer *before* the nonrenewal took effect.
- **Commercial P&C (liability lines; not personal auto/personal P&C) — O.C.G.A. § 33-24-47**: **45 days'** notice of cancellation, nonrenewal, or premium increase > 15% — § 33-24-47(b). Nonpayment cancellations and policies in force < 60 days revert to § 33-24-44 (i.e., 10 days) — § 33-24-47(a). **Workers' compensation: 75 days**, by § 33-24-14(d) electronic delivery or certified mail/statutory overnight, return receipt requested — § 33-24-47(f). Reduction in coverage: 45-day all-caps notice — § 33-24-47(g). Remedy for defective notice is weak on this statute: the policyholder may *purchase* up to 30 extra days at the same terms by tendering pro-rata premium before termination — § 33-24-47(c) — rather than the cancellation being void.
- **Notice content regulation**: Ga. Comp. R. & Regs. 120-2-53 prescribes cancellation/nonrenewal notice contents, including language advising the insured of a 15-day window to request Commissioner review.

### 2.3 Strict-compliance doctrine — defective notice = no cancellation

Georgia (and the majority rule nationally): cancellation-notice statutes are construed **strictly against the insurer**, and the insurer bears the burden of proving compliant cancellation.

- *Reynolds v. Infinity Gen. Ins. Co.*, 287 Ga. 86, 694 S.E.2d 337 (2010) (Ga. Supreme Court, construing §§ 33-24-44 and 33-24-45(c)(1)): the statute "is to be strictly construed against the insurer, inasmuch as the methods adopted by the General Assembly are mandatory and intended to assure that the insured has actual notice of cancellation"; the notice there was held **ineffective**. (verified 2026-07-04)
- *Perry & Co. v. New South Ins. Brokers*, 182 Ga. App. 84, 354 S.E.2d 852 (1987): "The notice requirements of the statutes regarding cancellation of insurance policies are mandatory and require strict compliance and failure to adhere to the requirements results in noncancellation of the policy." (verified 2026-07-04)

Practical consequences: if the notice was short by one day, sent to a stale address when a current one was of record, missing the statutory reason, missing the FAIR Plan paragraph, or the insurer cannot produce mailing evidence — the policy is treated as **still in force** at the loss date. This is the claimant's strongest lever and the insurer's largest silent liability.

### 2.4 Proof-of-mailing rules

- Georgia requires not just first-class mailing but the insurer "receiving the receipt provided by the United States Postal Service or such other evidence of mailing as prescribed or accepted by the United States Postal Service" — § 33-24-44(b). In practice: USPS Certificate of Mailing (PS Form 3817/3877 firm book) or Intelligent Mail barcode records. Actual receipt by the insured is generally NOT required if statutory mailing is proven — the statute shifts risk of non-receipt to the insured once the insurer proves compliant dispatch.
- Workers' comp is stricter: certified mail / statutory overnight, return receipt requested, receipt retained — § 33-24-47(f).
- Lienholder notice irregularities do not invalidate an otherwise-valid cancellation *as to the insured* (§ 33-24-44(b), (d)) — but can create separate insurer liability to the lienholder.
- Forensic move: subpoena/request the insurer's mailing manifest and the USPS receipt for the *specific* notice. A generic declaration of "ordinary business practice" without the statutory receipt is attackable under strict compliance.

## 3. Reinstatement law

- **No statutory right to reinstatement** for lapsed P&C policies in Georgia (unlike life insurance, where policies commonly carry contractual reinstatement clauses). Reinstatement is discretionary with the carrier — typically conditioned on payment of all past-due premium, a no-loss letter (insured warrants no known losses during the gap), and sometimes re-underwriting.
- **The gap is generally NOT covered.** Standard reinstatement is effective from the reinstatement date forward; a "no lapse in coverage" reinstatement (rescinding the cancellation as if it never happened) exists but requires the carrier's explicit agreement and is the exception. Never assume gap coverage from the word "reinstated" — read the reinstatement notice for the effective date and any lapse-in-coverage language.
- **Premium-finance context**: under O.C.G.A. § 33-22-13(c)(1), the PFC's notice to the insured must state that payment received *after* the cancellation notice went to the insurer "will not reinstate the policy"; the PFC may only *request* reinstatement from the carrier. (verified 2026-07-04)
- **Claims-made policies — a gap is catastrophic**, not merely a hole:
  - A lapse breaks continuity; the replacement policy's **retroactive date** typically resets to the new inception, wiping out prior-acts coverage for every wrongful act before that date.
  - Claims first made during the gap are covered by nothing, and an **extended reporting period (ERP/tail)** usually must be elected within 30–60 days of termination (policy-specific) — miss the election window and the tail is gone too.
  - Forensic check on any claims-made lapse: compare the old policy's retro date to the new policy's retro date; if they differ, quantify the prior-acts exposure that vanished, and check whether a tail was offered/elected.
- **Occurrence policies**: a gap only forfeits coverage for bodily injury/property damage *occurring during* the gap — prior occurrence-period coverage survives. For latent/continuous injury (construction defect), a gap can still splinter the coverage block across trigger theories.

## 4. Gap-exposure taxonomy and remedies

### How gaps actually happen (in observed frequency order)

1. **Premium-finance-company cancellation — the dominant source.** The insured financed the premium (agent-arranged PFA, e.g., IPFS — a finance company, NOT the carrier; see references/premium-finance.md), missed an installment, and the PFC exercised its power of attorney: 10-day cure notice (§ 33-22-13(b)), then cancellation request to the insurer, which the insurer may treat under a **conclusive presumption** of PFC compliance (§ 33-22-13(c)(2)) — the insurer bears no liability even if the PFC botched its notices; the insured's recourse is against the PFC. The insured often learns of the lapse only at claim time. Insurer must still notify mortgagees/government/third parties within 2 business days — § 33-22-13(d).
2. **Audit-premium nonpayment.** Auditable policies (GL, workers' comp) generate additional premium at audit; nonpayment of the audit bill is premium nonpayment → 10-day cancellation path (§ 33-24-44(d)), or audit-refusal cancellation (§ 33-24-44(d.2)). Contractors with payroll swings are the classic victims.
3. **Carrier insolvency.** Liquidation order typically cancels all policies by operation of law within a statutory window fixed by the governing state's liquidation and guaranty-association acts. **UNVERIFIED as to any day count: none is stated here, deliberately.** No state's act was pulled for this file, and a notice window asserted without a source is the defect this skill exists to prevent. Pull the governing state's act (state guaranty-association acts govern — confirm the state's window before relying). Guaranty-fund coverage is capped and excludes some lines/claimants. A gap opens between liquidation and replacement placement.
4. Also seen: nonrenewal notice missed by the insured (mail to old address); agent E&O (failure to remit or to place renewal); mid-term cancellation for misrepresentation discovered at claim.

### Remedies against a bad lapse

- **Strict-compliance attack** (§ 2.3): defective notice → policy still in force. First and best argument.
- **Waiver**: insurer conduct inconsistent with cancellation — accepting/retaining premium after the purported cancellation date, issuing endorsements, defending a claim — can waive the cancellation.
- **Estoppel**: insured detrimentally relied on insurer/agent representations that coverage continued (e.g., agent said "you're covered, ignore the notice"). Requires reasonable reliance; weaker where the statutory notice was clear.
- **Wrongful cancellation / breach of contract**: damages = what the policy would have paid, plus consequential damages where recoverable.
- **Bad faith**: in Georgia, first-party bad faith runs through O.C.G.A. § 33-4-6 (50% penalty + fees on frivolous claim refusal, 60-day demand prerequisite) — a wrongful-cancellation denial can qualify. UNVERIFIED beyond the section number's general subject — confirm current § 33-4-6 text before relying.
- **Agent/broker E&O**: failure to forward notices, remit premium, or procure replacement coverage.
- Compliance-risk framing: carriers and PFCs lose these fights on process, not substance. A defensible cancellation file shows: correct statutory ground identified, correct day count for that ground, notice to the current address of record, statutory mailing evidence retained, lienholder/third-party notices logged, unearned premium refunded on time.

## 5. Certificates of insurance are NOT coverage

- A COI (ACORD 25) is an **information-only snapshot** as of its issue date. Standard ACORD language: it confers no rights on the holder, does not amend/extend/alter the policy, and — since ACORD 25 (2010) — the certificate does not even promise notice of cancellation to the holder beyond what the policy/endorsements provide. Many states (Georgia included, O.C.G.A. § 33-24-19.1 — UNVERIFIED pinpoint, confirm before citing) statutorily prohibit certificates that purport to alter policy terms.
- **Additional-insured status lives in the policy endorsement, not the COI.** If the underlying policy lapses, every AI's coverage dies with it — the GC/owner holding a clean COI dated three months ago has nothing. AI status is also only as good as the endorsement's scope (ongoing vs. completed operations; "when required by written contract" triggers).
- **Construction-contract implications**: subcontract insurance exhibits typically require maintained coverage + AI status + waiver of subrogation + primary/non-contributory, with a COI as *evidence*. A lapse puts the sub in breach of contract independent of any claim, and shifts the loss to (a) the sub directly, (b) the GC's own program, or (c) contractual indemnity — which may itself be uninsured once the CGL is gone.
- Forensic rule: **never treat a COI as proof coverage existed on the loss date.** Verify against carrier records: policy declarations, endorsement list, and the cancellation/reinstatement history. The COI's issue date only proves what an agent asserted on that day; agents issue COIs from stale data, and fraudulent COIs over lapsed policies are a recurring pattern in subcontractor defaults.

## 6. Construction-specific continuity

- **Contract-required coverages** (typical subcontract exhibit): CGL (per-project aggregate, completed ops through the statute of repose), auto, WC/EL, umbrella, sometimes pollution/professional. Continuity requirements often extend *years past* substantial completion (completed-operations AI). A lapse during the completed-ops tail is invisible day-to-day and surfaces only at a defect claim.
- **OCIP/CCIP wrap interplay**: wrap-enrolled subs get GL/WC (program-defined) through the wrap *for enrolled operations at the wrap site only*. Lapse traps: (1) the sub's own practice policies usually carry a wrap exclusion — if wrap enrollment lapses or the sub was never actually enrolled (enrollment paperwork ≠ confirmation), the wrap exclusion on the practice policy can leave zero coverage; (2) off-site work (fabrication, yard, transit) is outside the wrap and rides the practice program — a practice-policy lapse is unprotected by the wrap; (3) wrap termination at project completion vs. completed-ops tail length must be checked against the repose period.
- **Subcontractor default exposure**: a sub's coverage lapse is a leading indicator of financial distress (premium finance default precedes payroll default). GC controls: certified copies of endorsements (not just COIs) for critical subs, contractual right to procure replacement coverage and back-charge, subguard (SDI) as backstop, and joint-check or direct-pay arrangements for premium on distressed subs.
- Downstream: owner's lender typically requires uninterrupted builder's risk + GL evidence; a lapse can trigger loan-covenant default and force-placed coverage at penalty rates.

## 7. Forensic lapse timeline-reconstruction checklist

Goal: a day-by-day ledger of who bore the risk, from which every legal argument falls out.

**Gather (all of):**
1. Premium finance agreement (PFA) + payment schedule + PFC ledger (every installment: due date, received date, NSF events).
2. Every notice, both directions: PFC 10-day intent-to-cancel, PFC cancellation request to insurer, insurer cancellation/nonrenewal notices, reinstatement notices/offers, agent correspondence. Capture envelopes/mailing metadata where available.
3. Carrier records: policy dec pages + all endorsements, cancellation transaction history, unearned-premium refund ledger (amount, payee, date — was it tendered to the PFC within 10 working days per § 33-24-44(c)(2)?), reinstatement effective dates.
4. Insured's payment records: bank statements, cancelled checks/ACH traces vs. the PFC ledger.
5. Agent/broker file: COIs issued (with dates), placement correspondence, any representations about coverage status.
6. Mailing proof: USPS receipts/certificates of mailing, certified-mail return receipts, firm mailing books, address-of-record history.

**Build:**
7. Day-by-day timeline from first missed payment through replacement placement (or loss date). For each notice, log: date mailed, method, address used, statutory days given, effective date claimed.
8. For each notice, **test against the statute**: right ground? right day count for that ground (GA: 10 nonpayment / 30 general / 45 commercial / 75 WC / 60 homeowners nonrenewal from 2026)? right address (last of record)? statutory mailing evidence in hand? required content (reason, FAIR Plan paragraph, all-caps reduction headers, Commissioner-review language)? lienholder/third-party notices sent? Flag every deviation — each one is a potential "cancellation never happened."
9. Mark the claimed lapse window; then mark the *defensible* lapse window after striking non-compliant cancellations. The difference is the dispute.
10. For each day in the residual gap, identify the risk-bearer: insured (compliant cancellation), insurer (defective notice → still on risk), PFC (botched § 33-22-13 process — insured's recourse target given the insurer's conclusive presumption), agent (E&O), or guaranty fund (insolvency).
11. If claims-made: overlay retro dates and tail-election windows (§ 3) on the same timeline.
12. Cross-check the loss date(s) against the final ledger and write the exposure conclusion per party.

## Sources verified (2026-07-04)

- https://law.justia.com/codes/georgia/title-33/chapter-24/article-1/section-33-24-44/ — O.C.G.A. § 33-24-44 full text (2024 Code): 30-day general / 10-day nonpayment & <60-day notice, mailing-receipt rule, void-ab-initio carve-out (d.1), audit-refusal path (d.2), unearned-premium timing and 25%+18% penalty, PFC carve-out (e).
- https://law.justia.com/codes/georgia/title-33/chapter-24/article-1/section-33-24-46/ — O.C.G.A. § 33-24-46 full text (2024 Code): residential-property grounds after 60 days, 30-day nonrenewal (pre-2026), FAIR Plan notice, prohibited nonrenewal grounds, pre-suit objection requirement (l).
- https://law.justia.com/codes/georgia/title-33/chapter-24/article-1/section-33-24-47/ — O.C.G.A. § 33-24-47 full text (2024 Code): 45-day commercial notice, >15% premium-increase notice, WC 75-day certified mail (f), 30-day purchase remedy (c), 45-day reduction notice (g).
- https://www.legis.ga.gov/api/legislation/document/20252026/236504 — SB 35 enrolled text (PDF): strikes "30" for "60" days in § 33-24-46(d)(1) nonrenewal notice.
- https://legiscan.com/GA/bill/SB35/2025 — SB 35 status: passed, Act 277, signed 2025-05-14, effective 2026-01-01. Corroborated by https://gov.georgia.gov/document/2025-signed-legislation/sb-35/download.
- https://law.justia.com/codes/georgia/title-33/chapter-22/section-33-22-13/ — O.C.G.A. § 33-22-13 full text (2024 Code): PFC 10-day cure notice, cancellation-in-name-of-insured mechanics, no-reinstatement-by-late-payment language, conclusive presumption protecting insurer, 2-business-day third-party notice.
- https://caselaw.findlaw.com/court/ga-supreme-court/1510248.html — Reynolds v. Infinity Gen. Ins. Co. (Ga. 2010): strict construction against insurer; notice held ineffective. Reporter cite 287 Ga. 86, 694 S.E.2d 337 corroborated by https://law.justia.com/cases/georgia/court-of-appeals/2011/a11a0087.html (Burnside v. GEICO, quoting it).
- https://law.justia.com/cases/georgia/court-of-appeals/1987/73905-0.html — Perry & Co. v. New South Ins. Brokers, 182 Ga. App. 84, 354 S.E.2d 852 (1987): strict-compliance quote.
- https://rules.sos.ga.gov/gac/120-2-53 — Ga. Comp. R. & Regs. 120-2-53: cancellation/nonrenewal notice content requirements incl. 15-day Commissioner-review language (title/summary level).
