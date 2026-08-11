# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Lab 4.2 — Build a Reusable Prompt Template Library  *(SOLUTION / instructor copy)*
#
# **Chapter 4 — Modern GenAI and Prompt Engineering** · 30 minutes *(flex)*
#
# **Objectives**
# 1. Turn one-off prompts into parameterised templates.
# 2. Test a template against inputs it was not written for.
# 3. Ship something your team can adopt.

# %%
# Instructor copies live in solutions/, one level below labs/ — find labs/
# (where lab_common.py, lab_helpers.py and data/ are) and run from there.
import os, sys
from pathlib import Path

for _cand in (Path.cwd(), *Path.cwd().parents):
    if (_cand / "lab_common.py").is_file():
        os.chdir(_cand)
        if str(_cand) not in sys.path:
            sys.path.insert(0, str(_cand))
        break

from lab_helpers import *

# %% [markdown]
# ## Step 1 — From prompt to template
#
# **Worked v1:** the Lab 4.1 zero-shot summarizer with four slots. Note the
# deliberate flaw left in: v1 trusts that `stage` and `problem` exist.

# %%
uc = load_use_case_inventory()

# %%
TEMPLATE_V1 = """In two sentences for [AUDIENCE], summarize this federal AI use case.
Agency: [AGENCY]
Use case: [NAME]
Stage: [STAGE]
Problem it solves: [PROBLEM]"""

# %% [markdown]
# ## Step 2 — Test on five rows it was not written for
#
# **Expected:** v1 reads fine on complete rows (rubric ~4s). Watch for long
# use-case names (one Commerce row is a 227-character sentence) — the output
# parrots the whole name — and for the blank fields Step 3 targets.

# %%
test_template_on_rows(uc, TEMPLATE_V1)

# %% [markdown]
# ## Step 3 — The breaking input, and fixing the template
#
# **Expected break:** "Automated Data Annotation" (DHS) has no
# `problem_solved` and no `development_stage`. v1 prints `Stage: nan /
# Problem it solves: nan` — and online, the model will either echo "nan" or,
# worse, invent a plausible problem. Both are template failures: the fix is
# to make missing data a first-class case in the prompt, and to instruct the
# model to say "not reported" rather than guess.
#
# **Which slot mattered most (reflection 2):** `problem` — it carries the
# sentence's meaning; `stage` can be dropped without the output collapsing.

# %%
show_breaking_row(uc, TEMPLATE_V1)

# %%
TEMPLATE_V2 = """In two sentences for [AUDIENCE], summarize this federal AI use case. If a field says 'not reported', do not invent it — say the inventory does not report it.
Agency: [AGENCY]
Use case: [NAME]
Stage: [STAGE]
Problem it solves: [PROBLEM]"""

show_fixed_brief(uc, TEMPLATE_V2)

# %% [markdown]
# ## Step 4 — A second template, a different pattern
#
# **Worked:** structured triage (JSON), the Lab 4.1 structured-output pattern
# templatized. `risk_flag` keys only off the reported high-impact label — the
# output says triage, not assessment.

# %%
TRIAGE_TEMPLATE = """Return JSON with keys plain_english, risk_flag (low|review), one_question_to_ask for this use case.
Agency: [AGENCY]
Use case: [NAME]
Stage: [STAGE]
High-impact: [IS_HIGH_IMPACT]"""

triage_use_cases(uc, TRIAGE_TEMPLATE)

# %% [markdown]
# ## Step 5 — Export the library

# %%
LIBRARY_MD = """# My Prompt Library

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
"""

save_to_prompt_library(LIBRARY_MD)

# %% [markdown]
# ## Reflection (expected answers)
# 1. Missing data broke it first — blanks in `development_stage` (223 rows)
#    and `problem_solved` (297 rows). Second was over-long use-case names
#    swamping the summary.
# 2. `problem` — it carries the sentence's meaning. The template must say
#    what to do when it is absent, because absent is common.
# 3. Before a team handoff: a version note and owner, test cases (the
#    breaking row becomes a regression test), a cost/latency note, and the
#    data-category rule — which of these fields may leave the boundary at all
#    (Lab 5.2's question).
