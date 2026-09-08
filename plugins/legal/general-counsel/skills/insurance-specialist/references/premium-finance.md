# Premium Finance Mechanics — PFAs, POA Cancellation, Unearned Premium, State Acts

> Evergreen reference for the insurance-specialist skill.
>
> **Freshness:** class=`legislation` verified=2026-07-04 sources=O.C.G.A. Title 33 ch. 22 text via the Justia 2024 Code mirror with its currency year recorded, FindLaw as the second independent source for § 33-22-13, SEC EDGAR and the company site for corporate identity

`class` selects the threshold from the central table in
`scripts/check_authority_freshness.py`; the number is not written here so that
changing it is one edit. Past the threshold this file is a lead, not an
authority: re-verify the specific fact you need against the governing state's
current statute text, label what you cannot verify "ASSUMPTION (unverified)", and
record the stale header and its date in LIMITATIONS. Bump `verified` only after
re-verifying this file's own scope. The cross-reference to
[`current-legislation.md`](current-legislation.md) locates statute currency; it
does not transfer that file's freshness to this one.

Two at-use rules override the header. Service-charge caps, delinquency and NSF
fees, and de minimis refund thresholds are periodically amended: re-pull them
from the current section text at each use. Cure deadlines and cancellation
effective dates are computed from the governing state's text pulled that day,
never from this file; the ten-day count below is Georgia's and does not port.

Decision support for forensic insurance research — not legal or tax advice. Abuse and failure patterns are documented so structures and disputes AVOID them.

## 1. What premium finance is — and THE canonical misidentification

Premium finance is a **loan**: a licensed finance company advances the annual (or multi-year) premium to the insurance carrier up front; the insured repays the finance company in installments plus a finance charge. The collateral is the policy's **unearned premium** — the refundable portion of prepaid premium if the policy cancels mid-term.

**The canonical misidentification: IPFS Corporation / Imperial PFS is a premium FINANCE company, NOT the insurance carrier.** IPFS describes itself as "North America's largest premium finance company," privately held since 1977, headquartered in Kansas City, MO (1055 Broadway Blvd), operating across the US, Puerto Rico, and Canada (ipfs.com homepage, https://www.ipfs.com/, verified 2026-07-04). SEC filings independently confirm the corporate identity: IPFS Corporation reports on "the ongoing sale and servicing of premium finance receivables" (SEC EDGAR, https://www.sec.gov/Archives/edgar/data/1541492/000110465915069994/a15-20554_1ex99d1.htm, verified 2026-07-04). IPFS issues **loans**, not policies.

Why the distinction is load-bearing in any dispute or forensic timeline:

| Question | Wrong answer (misidentified) | Right answer |
|---|---|---|
| Who owes the coverage / must pay the claim? | "IPFS" | The **carrier** named on the dec page |
| Who must receive notice of claim / suit? | IPFS | Carrier (and agent per policy conditions) |
| Who do you sue for wrongful denial? | IPFS | Carrier (bad faith, breach of contract) |
| Who do you sue for wrongful cancellation via defective POA notice? | Carrier alone | Finance company (statutory notice defect) and/or carrier (processing failure) — see §3 |
| Who receives the unearned premium on cancellation? | Insured | Finance company first, insured only the surplus — see §4 |
| Who do you pay to CURE a default? | Carrier or agent | The **finance company**, by its stated deadline |

When an "IPFS notice" appears in a document set, the first classification step is: this is a **lender communication about a loan secured by a policy**, and the policy's carrier is a different entity that must be identified from the notice body or the underlying dec page.

## 2. Premium finance agreement (PFA) anatomy

A PFA is a consumer-credit-adjacent installment loan contract. Standard components:

- **Down payment** — typically 10–25% of total premium collected at inception (varies by line and credit; UNVERIFIED as to any statutory minimum — confirm per state before relying). Paid to the agent/broker, who remits with the financed balance to the carrier.
- **Amount financed** — total premium(s) plus taxes/fees, minus down payment. One PFA can finance multiple policies (schedule of policies listed in the agreement).
- **Installment schedule** — usually 9–10 monthly installments on an annual policy, front-loaded so the loan balance amortizes faster than premium earns (keeps the unearned-premium collateral above the loan balance — the lender's core underwriting equation).
- **Finance charge / APR** — disclosed as dollar finance charge and annual percentage rate. State premium finance acts cap or regulate service charges (Georgia: O.C.G.A. § 33-22-9 "Service charges"; delinquency and NSF fees at § 33-22-10 — section titles verified via 2024 GA Code chapter index, https://law.justia.com/codes/georgia/title-33/chapter-22/, verified 2026-07-04; confirm current charge caps before quoting figures).
- **Security interest / assignment** — insured assigns unearned premiums (and often loss payments to the extent of the balance) to the finance company.
- **Power of attorney (POA) clause** — the decisive clause: on default, the finance company is appointed attorney-in-fact to **cancel the listed policies in the insured's name** and collect the unearned premium. This is what converts a missed installment into a coverage lapse.

Form, contents, execution, and delivery of the PFA are themselves regulated (Georgia: O.C.G.A. § 33-22-8; the finance company must also notify the insured of the POA's existence and provide a copy of the agreement, § 33-22-12.1 — titles verified via chapter index, verified 2026-07-04).

## 3. POA cancellation flow, step by step

Statutory chain (Georgia model — O.C.G.A. § 33-22-13, 2024 Code, amended eff. 7/1/2014; full text verified at https://law.justia.com/codes/georgia/title-33/chapter-22/section-33-22-13/, 2026-07-04). Most states follow the same skeleton with different day counts.

1. **Default** — insured misses an installment (or check bounces).
2. **Notice of intent to cancel** — finance company must give **not less than ten days' written notice** to the insured (delivered, sent electronically, or mailed to the address in the agreement) of intent to cancel "unless the default is cured within such ten-day period." A copy must also go to the **agent or broker** on the PFA. § 33-22-13(b).
3. **Cure window** — payment of the stated cure amount within the ten days stops the cancellation.
4. **Cancellation request to carrier** — after the ten days expire, the finance company may "in the name of the insured" cancel by mailing/delivering a **notice of cancellation** to the insurer — treated "as if the notice of cancellation had been submitted by the insured." Simultaneously it must mail the insured a notice stating the date and time of cancellation (which must be after the mailing date) and warning that **payment received after the cancellation request will NOT reinstate the policy** (it may say the finance company will request reinstatement). Plain-language standard applies; first-class mail with USPS proof of mailing. § 33-22-13(c)(1).
5. **Carrier cancels** — the insurer's receipt of the finance company's cancellation notice creates a **conclusive presumption** that the finance company complied with the statute and that the insured authorized the cancellation; the insurer bears **no liability** for the insured's non-receipt of notice or the finance company's non-compliance. § 33-22-13(c)(2).
6. **Third-party notices** — statutory/contractual notices to government agencies, mortgagees, or other third parties still apply; the **insurer** must send those on or before the **second business day** after receiving the cancellation notice and set the effective date accordingly. § 33-22-13(d).
7. **Unearned premium flows back** — insurer returns unearned premium to the finance company for the insured's account (see §4).

### Where the chain breaks, and who bears the gap

- **Defective notice by the finance company** (short day count, wrong address vs the address "shown in the agreement," no copy to agent, missing cure amount, cancellation date before mailing date): under § 33-22-13(a) the policy "shall not be canceled" unless the statute is followed — a wrongful-cancellation claim runs against the **finance company**. But under the § 33-22-13(c)(2) conclusive presumption, the **carrier is shielded** once it receives the cancellation notice — so in Georgia the insured's remedy for a notice defect is against the finance company, and arguing the policy never validly canceled as against the carrier is an uphill fight. Forensically: demand the finance company's proof-of-mailing artifacts (USPS receipt or accepted equivalent) — the statute makes them mandatory.
- **Carrier processing lag**: cancellation is effective per the notice, not per the carrier's data entry. A claim occurring between the stated effective date and the carrier's booking date is outside coverage; conversely, a carrier that books cancellation EARLIER than the noticed date has cut coverage the statute preserved. Compare the finance company's noticed effective date/time against the carrier's cancellation endorsement date line by line.
- **Payment-in-flight**: money received by the finance company after it has already mailed the carrier cancellation does not reinstate (statutory text). Payments received **within** the ten-day cure window that the finance company failed to apply are a classic wrongful-cancellation fact pattern — pull bank/ACH timestamps.
- **Third-party notice failure** (mortgagee, certificate holders, state filings): duty sits with the **insurer** post-receipt (§ 33-22-13(d)); a mortgagee not noticed may retain rights under its standard mortgage clause even after the insured's coverage dies.

## 4. Unearned-premium math

- **Pro-rata return**: unearned premium = annual premium × (unexpired days ÷ policy days). Used when the **finance company cancels via POA** — the cancellation is statutorily treated as the insured's own notice, but market practice and most policy forms apply pro-rata to finance-company cancellations; some forms still apply short-rate to any insured-initiated cancellation. **Check the policy's cancellation condition — do not assume.** (UNVERIFIED as a universal rule — confirm per policy form and state.)
- **Short-rate return**: pro-rata minus a penalty set by the policy's own short-rate table or cancellation condition. Applies to voluntary insured cancellations under many forms. (UNVERIFIED as to any typical percentage: no source in this file supports one, so read the penalty off the applicable form rather than carrying a rule-of-thumb figure into a computation.)
- **Audit-premium interaction**: on auditable lines (GL, WC), the "premium" at inception is a **deposit**. Cancellation triggers a short-term audit; earned premium is recomputed on actual exposure. The audit can **wipe out or invert** the expected unearned return — the finance company may be undersecured and the insured can owe additional premium to the carrier ON TOP of the loan deficiency to the finance company. In a forensic reconstruction, never treat "unearned premium per dec page math" as the actual refund on an audited line; get the cancellation audit.
- **Who gets what** (Georgia, O.C.G.A. § 33-22-14, 2024 Code, verified https://law.justia.com/codes/georgia/title-33/chapter-22/section-33-22-14/, 2026-07-04):
  - Insurer, once notified of the PFA (§ 33-22-12), must return unearned premiums **to the finance company** for the insured's account; paying anyone else leaves the insurer **directly liable** to the finance company. § 33-22-14(a).
  - Finance company applies the return premium to the loan balance. Only a **surplus** goes to the insured — refunded via the agent/broker within **ten working days** of receipt; no refund required if the excess is under **$5.00**. § 33-22-14(b)(1).
  - Late refund penalty on the finance company: **25% of the refund plus 18% per annum interest**, capped at 50% of the refund. § 33-22-14(b)(2). Agent must pass the refund to the insured within **ten working days** of receiving it. § 33-22-14(b)(3).
  - Failure to refund does **not** invalidate an otherwise-proper cancellation. § 33-22-14(c).
  - Sibling provision: Georgia's general cancellation statute requires unearned premiums financed through a premium finance company to be tendered **to the finance company within ten working days** (O.C.G.A. § 33-24-44, text excerpt verified via Fastcase snippet, https://public.fastcase.com/, verified 2026-07-04 — pull full section text before citing in a filing).
- **Practical answer to "what does the insured get back?"**: usually nothing until the finance balance clears. Because the loan amortizes slower than a late-term cancellation's return premium in the tail months, a mid-to-late-term finance cancellation frequently returns $0 to the insured and may leave a deficiency.

## 5. State premium finance acts — Georgia worked example

Every state regulates premium finance companies under an insurance-code chapter (or banking law, e.g., New York). Common architecture: licensing, form/charge regulation, PFA filing or insurer-notification, POA cancellation procedure, unearned-premium disposition. Georgia — O.C.G.A. Title 33, Chapter 22, "Insurance Premium Finance Companies" (§§ 33-22-1 — 33-22-16; chapter structure verified at https://law.justia.com/codes/georgia/title-33/chapter-22/, 2026-07-04):

| Provision | Cite (2024 GA Code) | Content |
|---|---|---|
| Licensing | § 33-22-3 | No person may finance insurance premiums in Georgia without a Commissioner-issued license; annual renewal each **March 1**; unlicensed operation is a misdemeanor-level offense, fine up to **$1,000** on conviction. Full text verified 2026-07-04. |
| Applicant vetting / denial | § 33-22-4 | Investigation, hearing, grounds (title verified via chapter index) |
| Minimum capital / bond | § 33-22-5 | (title verified via chapter index; figures not verified — confirm) |
| Revocation / fines | § 33-22-6 | (title verified via chapter index) |
| PFA form & delivery | § 33-22-8 | (title verified via chapter index) |
| Service charges | § 33-22-9 | (title verified via chapter index; caps not verified — confirm current text) |
| Delinquency / NSF fees | § 33-22-10 | (title verified via chapter index) |
| Notify insurer of PFA | § 33-22-12 | Predicate for § 33-22-14(a) direct-liability rule |
| Notice of POA to insured | § 33-22-12.1 | Copy of PFA + notice that POA exists (title verified) |
| **POA cancellation procedure** | **§ 33-22-13** | **≥10 days' written notice of intent + cure window; then cancellation in insured's name; conclusive presumption shields insurer; insurer sends third-party notices within 2 business days.** Full text verified 2026-07-04. |
| **Unearned premium disposition** | **§ 33-22-14** | **Return to finance company; surplus to insured in 10 working days; $5 de minimis; 25% + 18%/yr penalty capped at 50%.** Full text verified 2026-07-04. |
| Rules authority / scope | §§ 33-22-15, -16 | Commissioner rulemaking; applicability (titles verified) |

Wrongful-cancellation liability in Georgia flows from § 33-22-13(a)'s command that the policy "shall not be canceled" absent compliance — but remember the (c)(2) presumption reroutes the claim toward the finance company and away from the insurer. Other states differ: some make the carrier verify notice compliance (no conclusive presumption), and day counts vary (10 days is common; several states use longer periods for personal lines — confirm per state in current-legislation.md before asserting a number).

## 6. Interaction with lapse law

Finance-driven cancellation is the **dominant source of mid-term coverage gaps** in commercial books: the insured pays "the insurance" (i.e., the loan) late, and a ten-day statutory fuse burns down to a POA cancellation — often without the insured connecting the lender notice to the policy at all. Cross-ref: **references/coverage-lapse-law.md** for carrier-initiated cancellation/nonrenewal notice law; this file governs the finance-company-initiated path, which follows the PFA statute, not the carrier-cancellation statute (though third-party notice duties merge at § 33-22-13(d)).

Reinstatement path after a finance default:
1. **Inside the cure window** (before the carrier notice is mailed): pay the cure amount to the finance company — the policy never cancels.
2. **After cancellation request is mailed**: by statute, payment does not reinstate; the finance company **may** request reinstatement from the carrier (§ 33-22-13(c)(1) permits the notice to say so). Reinstatement is then a **carrier underwriting decision**, usually conditioned on a no-loss letter for the gap period and full payment. The gap between the cancellation effective date and any reinstatement endorsement is typically **uncovered unless the carrier reinstates without lapse** — read the reinstatement endorsement's effective-date language exactly.
3. **Forensic timeline discipline**: for any claimed loss near a finance default, build the sequence — installment due date → default → intent-to-cancel mailing date → cure deadline → cancellation-request mailing date → carrier effective date/time → reinstatement request → reinstatement effective date — and place the date of loss against it. The controlling documents are the finance company's notices and USPS proofs, not the parties' recollections.

## 7. Reading an IPFS notice, field by field

Real IPFS notices from 2021–23 exist in the user's Gmail as exemplars; the anatomy below is generic — never reproduce personal data from them into work product.

- **Parties block**: (1) **Borrower/insured** — the named insured on the PFA (watch for named-insured mismatches vs the dec page: an entity-name discrepancy between loan and policy is a red flag for who actually holds coverage); (2) **Finance company** — IPFS Corporation (or regional entity), with a loan/account number; (3) **Insurance company / carrier** — the entity that actually owes coverage; on multi-policy PFAs, one carrier per scheduled policy; (4) **Agent/broker** — the producer of record, statutorily entitled to a copy of the intent-to-cancel notice.
- **Account / loan number** vs **policy number(s)**: distinct identifiers. The loan number keys IPFS's records; the policy numbers key the carriers'. A cancellation notice lists every scheduled policy being cancelled — check whether ALL policies on the PFA are named or only some.
- **Notice type**: distinguish (a) *Notice of Intent to Cancel* (the ten-day/cure-window letter) from (b) *Notice of Cancellation* (the post-window letter stating the deed is done). Only (a) carries a cure right.
- **Cure amount and deadline**: the dollar figure that stops cancellation and the date/time by which the finance company must **receive** it (receipt, not mailing). Late fees and returned-check fees may be folded in.
- **Cancellation effective date and time**: on the type-(b) notice — this is the coverage cut line. Statutorily it must postdate the mailing of that notice.
- **POA invocation language**: wording to the effect that the finance company is exercising the power of attorney granted in the PFA to cancel the listed policies **in the insured's name**. This clause is what makes the carrier treat the request as insured-authorized (Georgia: § 33-22-13(c)).
- **No-reinstatement-by-payment warning**: statutory language that payments after the cancellation request will not reinstate, possibly with a statement that reinstatement may be requested. Georgia requires this content in the notice (§ 33-22-13(c)(1)).
- **Forensic checks on any notice**: mailing date vs stated effective date (must satisfy the statutory minimum day count for the governing state), address used vs address in the PFA, whether the agent was copied, arithmetic of the cure amount vs the installment schedule, and whether a payment (bank records) landed inside the cure window.

## Sources verified

- https://www.ipfs.com/ — IPFS is "North America's largest premium finance company," privately held since 1977, Kansas City-based, US/PR/Canada footprint; a finance company, not a carrier (verified 2026-07-04).
- https://www.sec.gov/Archives/edgar/data/1541492/000110465915069994/a15-20554_1ex99d1.htm — IPFS Corporation as servicer of premium finance receivables (independent confirmation of corporate identity/business, verified 2026-07-04).
- https://www.trustpilot.com/review/ipfs.com — corroborates Kansas City HQ address, 1055 Broadway Blvd 64105 (third-party aggregator layer; verified 2026-07-04).
- https://law.justia.com/codes/georgia/title-33/chapter-22/ — chapter structure and section titles, O.C.G.A. §§ 33-22-1 — 33-22-16 (2024 Code, verified 2026-07-04).
- https://law.justia.com/codes/georgia/title-33/chapter-22/section-33-22-13/ — full text of § 33-22-13: ten-day notice/cure, POA cancellation in insured's name, conclusive presumption, two-business-day third-party notices (verified 2026-07-04).
- https://law.justia.com/codes/georgia/title-33/chapter-22/section-33-22-14/ — full text of § 33-22-14: unearned premium to finance company, ten-working-day surplus refund, $5 de minimis, 25%/18% penalty capped at 50% (verified 2026-07-04).
- https://law.justia.com/codes/georgia/title-33/chapter-22/section-33-22-3/ — full text of § 33-22-3: license requirement, March 1 renewal, $1,000 fine (verified 2026-07-04).
- https://codes.findlaw.com/ga/title-33-insurance/ga-code-sect-33-22-13/ — second independent source for the § 33-22-13 ten-day notice language (search-result text match, verified 2026-07-04).
- https://public.fastcase.com/ (O.C.G.A. § 33-24-44 excerpt) — financed unearned premiums tendered to the premium finance company within ten working days (snippet-level; pull full text before filing use; verified 2026-07-04).
