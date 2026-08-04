# My Prompt Library

## use_case_brief(agency, name, stage, problem, audience)
Two-sentence executive briefing of a federal AI use case.
**Known limitation:** inventory rows may lack stage or problem; v2 omits the clause rather than inventing content.

## triage_use_case(agency, name, stage, is_high_impact)
Structured JSON triage: plain_english, risk_flag, one_question_to_ask.
**Known limitation:** risk_flag keys only off the high-impact label; it is triage, not assessment.
