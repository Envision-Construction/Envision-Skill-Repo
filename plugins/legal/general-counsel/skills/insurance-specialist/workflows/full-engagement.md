# Full Engagement Playbook: materials review / feasibility / indication-report critique

Use when the ask spans multiple specialist domains (e.g. "review these broker
captive materials", "critique the indication report", "should we form, rent a
cell, or stay conventional").

## 1. Gather (orchestrating session leads)

- Retrieve source materials via envision-mcp (Gmail, Drive, Slack, meeting
  transcripts) **in the main session**. The specialists now hold the same
  gateway, but the corpus is assembled once and passed as pointers: four agents
  each re-running the same retrieval is how the context budget goes. A
  specialist uses its own access to close a gap in the record it is analyzing,
  not to re-gather what the manifest already lists.
- Save raw documents inside the matter folder that `gc-new-matter` scaffolds
  (`matters/<slug>/`). That whole tree is untracked (`.gitignore`) and excluded
  from Cloud Build (`.gcloudignore`), which is the property that makes it the
  right home for privileged material. There is no `memory/` tree in this repo.
- Keep a manifest as a numbered file at the matter root listing, per document:
  filename, origin id (Gmail message id / Drive file id), date, sender where the
  document is correspondence, one-line description, fetch status. Every fact
  later drawn from one of these carries that provenance at the point of use; a
  quoted email with no id is an unverified assertion, not evidence.
- Gotcha: `parse_document_on_demand` accepts only `gs://` URIs. The reliable path
  for email attachments is `gmail_get_attachment`, save locally, then native
  `Read` (PDF supported, use `pages`).
- Fold in internal context (prior memos, tax-counsel opinions) by path.
- If a gateway surface is unreachable (server not connected, permission denied),
  record it in LIMITATIONS and continue. Never fill the hole from memory.

## 2. Analyze (one parallel dispatch)

Dispatch all relevant specialists in a single message. **Synchronization
contract** (a 2026-07-04 eval run hit this race): specialists may finish Writing
their section files after their return message arrives, or return before the
Write lands. Before synthesizing, the orchestrator verifies each expected section
file EXISTS on disk (ls/Glob) and re-checks once after a short wait for any
missing file. Never conclude a section "never landed" from return-message timing
alone. Each prompt carries:

- The section assignment (e.g. tax agent to Regulatory; structures agent to
  Legal-structural plus domicile matrix; coverage-counsel to program mechanics
  and premium-finance exposure).
- **Pointers**: manifest path plus the specific local file paths it must Read.
  Never paste document bodies into prompts, and never paste raw PII into a
  prompt, a section file, or a return.
- An output path to Write its full section, and an instruction to return a
  distilled summary under 500 words.
- The reminder: two-source rule, pinpoint plus URL plus verified-on citations,
  indexed figures re-verified at use, controlling dates pulled the day they are
  computed, not-found is an answer.

## 3. Synthesize (main session)

- Read the section files, reconcile conflicts (note where specialists disagree
  and why).
- Run `Skill(pe-executive:pe-executive-mindset)` for the Strategy section: value
  creation, cash and EBITDA impact, risk-adjusted comparison of the structural
  options, negotiation leverage with brokers. The framing guardrails are in
  [`../SKILL.md`](../SKILL.md) (illustrative only, no legal citation inside the
  frame, the lens never changes a legal conclusion). If the plugin is absent,
  apply the framing and record the degradation in LIMITATIONS.
- Author the recommendation memo: cites all sections plus
  [`../references/current-legislation.md`](../references/current-legislation.md);
  separates Regulatory / Legal / Strategy; ends with the counsel and actuary
  escalation line naming the specific step.
- The memo is a matter artifact. It routes through the lifecycle: `gc-redteam`
  attacks it before anyone acts on it, and anything that will be filed or served
  goes through `gc-authorities-log` first. A memo that lands in a matter folder
  without a `gc-redteam` pass has skipped the only adversarial check in the
  chain. Placement, privilege header, and the by-law-firm Dropbox export rule
  belong to `gc-new-matter`; see [`../SKILL.md`](../SKILL.md) for the links.
