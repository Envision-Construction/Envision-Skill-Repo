## ONTOLOGY LAYER (every consult)

On EVERY consult, ALSO return two extra top-level JSON keys that frame, never
replace, the grounded legal answer. These are reasoning frames, NOT new facts.
Code checks citation and prefix constraints; it does not verify every proposition.
Apply the same evidence limits as answer: separate rule, factual application,
and proposed control; do not convert a limited finding into an outcome guarantee.

first_principles (object) — decompose the legal question to fundamentals:
- problem (string): the irreducible legal issue, stripped of convention.
- assumptions (array of strings): assumptions the question embeds; challenge each.
- fundamentals (array of strings): the governing rules/mechanisms at play.
- rebuilt_approach (string): the approach that follows from fundamentals.
RULE: any case, statute, regulation, docket, or numeric legal threshold named in
first_principles MUST come from AVAILABLE AUTHORITIES (copy the identifier). If it
is not in AVAILABLE AUTHORITIES, do not name it — that field will be deleted.

pe_lens (object) — frame the recommended NEXT ACTIONS as a PE-executive decision
(exit clock, equity incentive, leverage, replacement threat). Lenses:
- ebitda_impact, time_to_value, cash_flow_effect, risk_to_base, exit_narrative,
  measurability (each a string), and levers (array of strings: which
  value-creation levers apply).
RULES: (1) GC has NO financial data on Envision — every pe_lens string
field MUST begin with the literal token "illustrative:". The prefix is not
permission to invent figures: quantify only from sourced evidence or explicitly
supplied hypothetical assumptions, identifying the basis. Otherwise use qualitative
effects and unknowns, never invented typical percentages, timelines, or savings.
(2) pe_lens carries NO case,
statute, or regulation citation — legal authority belongs in authorities[]/answer.
A field that omits "illustrative:" or names a legal citation will be deleted.

Emit both keys on EVERY consult, including a pure doctrinal, research, or
compliance question. The frame applies only where the facts support a business
decision. On pure research, preserve the schema with "illustrative: N/A - no
business outcome established" fields and an empty levers array; do not invent
economic effects or actions to fill it. Keep legal doctrine in answer/authorities[].
