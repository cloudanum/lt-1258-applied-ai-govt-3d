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
# (where lab_common.py and data/ are) and run from there.
import os, sys
from pathlib import Path

for _cand in (Path.cwd(), Path.cwd().parent):
    if (_cand / "lab_common.py").is_file():
        os.chdir(_cand)
        if str(_cand) not in sys.path:
            sys.path.insert(0, str(_cand))
        break

# %% [markdown]
# ## Step 1 — From prompt to template
#
# **Worked v1:** the Lab 4.1 zero-shot summarizer with four slots. Note the
# deliberate flaw left in: v1 trusts that `stage` and `problem` exist.

# %%
import pandas as pd
from lab_common import chat, chat_json

uc = pd.read_csv("data/federal_ai_use_cases.csv", encoding="utf-8-sig")
cols = ["agency_name", "use_case_name", "development_stage",
        "is_high_impact", "problem_solved"]
print(uc[cols].head(3).to_string())

# %%
def use_case_brief(agency, name, stage, problem, audience="a non-technical executive"):
    """Template v1 — slots: agency, name, stage, problem, audience."""
    prompt = (f"In two sentences for {audience}, summarize this federal AI "
              f"use case.\nAgency: {agency}\nUse case: {name}\n"
              f"Stage: {stage}\nProblem it solves: {problem}")
    canned = (f"[offline example for: {name[:60]}] {agency} is applying AI "
              f"({stage}) to {str(problem)[:80]}. The system, '{name}', is "
              f"intended to turn that manual work into an automated pipeline.")
    return chat([{"role": "user", "content": prompt}], offline=canned)

# %% [markdown]
# ## Step 2 — Test on five rows it was not written for
#
# **Expected:** v1 reads fine on complete rows (rubric ~4s). Watch for long
# use-case names (one Commerce row is a 227-character sentence) — the output
# parrots the whole name — and for the blank fields Step 3 targets.

# %%
test_rows = uc[cols].dropna(subset=["use_case_name"]).sample(5, random_state=11)
outputs = {}
for i, row in test_rows.iterrows():
    outputs[i] = use_case_brief(row["agency_name"], row["use_case_name"],
                                row["development_stage"], row["problem_solved"])
    print(f"--- {row['use_case_name'][:70]}")
    print(outputs[i], "\n")

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
breaking_row = uc[uc["problem_solved"].isna()][cols].iloc[0]
print(breaking_row.to_string(), "\n")
broken = use_case_brief(breaking_row["agency_name"], breaking_row["use_case_name"],
                        breaking_row["development_stage"], breaking_row["problem_solved"])
print("BROKEN OUTPUT:\n", broken)

# %%
def use_case_brief_v2(agency, name, stage, problem, audience="a non-technical executive"):
    """Template v2 — missing data is a prompt case, not an accident."""
    stage_txt = f"Stage: {stage}" if pd.notna(stage) else "Stage: not reported"
    prob_txt = (f"Problem it solves: {problem}" if pd.notna(problem)
                else "Problem statement: not reported in the inventory")
    prompt = (f"In two sentences for {audience}, summarize this federal AI "
              f"use case. If a field says 'not reported', do not invent it — "
              f"say the inventory does not report it.\nAgency: {agency}\n"
              f"Use case: {name}\n{stage_txt}\n{prob_txt}")
    canned = (f"[offline example for: {name[:60]}] {agency} reports an AI use "
              f"case, '{name[:60]}'"
              + (f", currently {str(stage).lower()}" if pd.notna(stage) else
                 ", though the inventory does not report its stage")
              + ". Details beyond that are not reported in the inventory.")
    return chat([{"role": "user", "content": prompt}], offline=canned)


fixed = use_case_brief_v2(breaking_row["agency_name"], breaking_row["use_case_name"],
                          breaking_row["development_stage"], breaking_row["problem_solved"])
print("FIXED OUTPUT:\n", fixed)

# %% [markdown]
# ## Step 4 — A second template, a different pattern
#
# **Worked:** structured triage (JSON), the Lab 4.1 structured-output pattern
# templatized. `risk_flag` keys only off the reported high-impact label — the
# output says triage, not assessment.

# %%
def triage_use_case(agency, name, stage, is_high_impact):
    prompt = (f"Return JSON with keys plain_english, risk_flag (low|review), "
              f"one_question_to_ask for this use case.\nAgency: {agency}\n"
              f"Use case: {name}\nStage: {stage}\nHigh-impact: {is_high_impact}")
    canned = {"plain_english": f"{name} — an AI use case reported by {agency}.",
              "risk_flag": "review" if is_high_impact == "High-impact" else "low",
              "one_question_to_ask":
                  "What human review exists before this system's output reaches a decision?"}
    return chat_json([{"role": "user", "content": prompt}], offline=canned)


for i, row in test_rows.head(3).iterrows():
    print(triage_use_case(row["agency_name"], row["use_case_name"],
                          row["development_stage"], row["is_high_impact"]))

# %% [markdown]
# ## Step 5 — Export the library

# %%
library_md = f"""# My Prompt Library

Two tested templates from Course 1258 Labs 4.1–4.2. Each lists its slots, the
prompt text, and the limitations the tests exposed. Offline runs return canned
outputs; on the VM they call the enterprise assistant.

## 1. use_case_brief(agency, name, stage, problem, audience="a non-technical executive")

Two-sentence executive briefing of a federal AI use case.

```
{use_case_brief_v2.__doc__}
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
with open("my_prompt_library.md", "w") as f:
    f.write(library_md)
print(open("my_prompt_library.md").read())

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
