# My Prompt Library

Two tested templates from Course 1258 Labs 4.1–4.2. Each lists its slots, the
prompt text, and the limitations the tests exposed. Offline runs return canned
outputs; on the VM they call the enterprise assistant.

## 1. use_case_brief(agency, name, stage, problem, audience="a non-technical executive")

Two-sentence executive briefing of a federal AI use case.

```
Template v2 — missing data is a prompt case, not an accident.
Prompt: "In two sentences for [AUDIENCE], summarize this federal AI use case.
If a field says 'not reported', do not invent it — say the inventory does not
report it. Agency: [AGENCY] / Use case: [NAME] / Stage: [STAGE] / Problem: [PROBLEM]"
```

**Known limitation:** inventory rows may lack stage or problem; v2 omits the
clause and says "not reported" rather than inventing content.

## 2. triage_use_case(agency, name, stage, is_high_impact)

Structured JSON triage: `plain_english`, `risk_flag` (low|review),
`one_question_to_ask`.

**Known limitation:** risk_flag keys only off the reported high-impact label;
it is triage, not assessment. Missing stage handled as "not reported".
