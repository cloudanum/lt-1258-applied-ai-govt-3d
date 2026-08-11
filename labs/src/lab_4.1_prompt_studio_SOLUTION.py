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
# # Lab 4.1 — Prompt Engineering Studio  *(SOLUTION / instructor copy)*
#
# **Chapter 4 — Modern GenAI and Prompt Engineering** · 45 minutes · rung **P4**
#
# **Objectives**
# 1. Apply the seven prompt patterns to real government material.
# 2. Score every output against the rubric and improve the weakest.
# 3. Leave with a personal, tested prompt library.

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
# ## Setup — the substrate

# %%
materials = load_prompt_studio_materials()

# %% [markdown]
# ## Pattern 1 — Zero-shot
#
# **Worked prompt + expected rubric:** accurate but generic — it names the
# four rules yet misses the *why* (the two pilot risks in §2). Typical scores:
# accuracy 5, completeness 3, format 4, tone 4.

# %%
ZERO_SHOT_PROMPT = "Summarize this memorandum for a division director in one short paragraph."
zero_shot = ask_about_memo(materials, ZERO_SHOT_PROMPT)

# %% [markdown]
# ## Pattern 2 — Few-shot
#
# **Worked prompt + expected:** two exemplars fix both the category vocabulary
# and the output format — the model stops inventing category names. Scores:
# 5/4/5/4. Teaching point: exemplars beat instructions for *format*.

# %%
FEW_SHOT_PROMPT = """Classify 311 request types into service categories, following the pattern of the examples.

Aircraft Noise Complaint -> Noise
311 INFORMATION ONLY CALL -> Information

Graffiti Removal Request ->
Tree Emergency ->
Water On Street Complaint ->"""

few_shot = classify_311_with_examples(FEW_SHOT_PROMPT)

# %% [markdown]
# ## Pattern 3 — Reasoning
#
# **Worked prompt + expected:** the multi-constraint question is where a
# reasoning model earns its cost — it must cross-reference three clauses, not
# retrieve one. Scores: 5/5/4/4. No CoT instruction: the model reasons
# internally; asking it to "think step by step" adds tokens, not accuracy.

# %%
HARD_ITEM = (
    "A division wants to use a free public chatbot to draft reply letters that "
    "quote from constituent case files, and to skip review for 'routine' "
    "replies. Under the memo, which specific clauses does this violate, and "
    "what is the smallest change that would make the plan compliant?"
)
reasoning = ask_hard_question(materials, HARD_ITEM)

# %% [markdown]
# ## Pattern 4 — Iterate on the weakest (worked example)
#
# Weakest above: **zero_shot** (completeness 3 — it dropped the memo's
# rationale). Three one-change rounds:
#
# - **Round 1 — add what to keep:** "…include why the guidance was issued."
#  Completeness 3 → 4 (mentions pilots but vaguely).
# - **Round 2 — name the content explicitly:** "…include the two recurring
#  risks the pilots surfaced." Completeness 4 → 5.
# - **Round 3 — constrain the shape:** "Exactly four sentences: purpose, the
#  two risks, the four rules, effective date." Format 4 → 5.
#
# What actually moved the score: naming the missing content (round 2), not
# asking harder (round 1).

# %%
ROUND_1 = "Summarize this memorandum for a division director in one short paragraph; include why the guidance was issued."
ROUND_2 = "Summarize this memorandum for a division director; include the two recurring risks the pilots surfaced."
ROUND_3 = "Summarize this memorandum in exactly four sentences: purpose, the two risks, the four rules, effective date."

iterate_on_prompt(materials, [ROUND_1, ROUND_2, ROUND_3])

# %% [markdown]
# ## Pattern 5 — Role
#
# **Worked prompt + expected:** the role changes *what the model notices* —
# a FOIA officer spots records and Exemption 6 alignment, not productivity.
# Scores: 5/4/4/5.

# %%
FOIA_ROLE = ("You are a FOIA officer reviewing a draft acceptable-use policy "
             "before commenting to the Chief Data Officer.")
role_out = ask_policy_with_role(materials, FOIA_ROLE)

# %% [markdown]
# ## Pattern 6 — Structured output
#
# **Worked prompt + expected:** JSON mode plus an explicit schema gives
# machine-usable output; the table below is the proof. Scores: 5/5/5/4.

# %%
entities = extract_memo_fields(materials)

# %% [markdown]
# ## Pattern 7 — Grounding
#
# **Worked prompt + expected:** the answer quotes the policy verbatim, and the
# mechanical check below proves the quote is real — the grounding pattern made
# the claim *auditable*. Scores: 5/5/5/5.

# %%
QUESTION = ("What happens if an employee pastes a constituent's record into "
            "a public chatbot?")
grounded = ask_policy_only(materials, QUESTION)

# %%
SCORECARD = {
    "zero_shot": {"accuracy": 5, "completeness": 3, "format": 4, "tone": 4},
    "few_shot": {"accuracy": 5, "completeness": 4, "format": 5, "tone": 4},
    "reasoning": {"accuracy": 5, "completeness": 5, "format": 4, "tone": 4},
    "role": {"accuracy": 5, "completeness": 4, "format": 4, "tone": 5},
    "structured": {"accuracy": 5, "completeness": 5, "format": 5, "tone": 4},
    "grounded": {"accuracy": 5, "completeness": 5, "format": 5, "tone": 5},
}
show_scorecard_totals(SCORECARD)

# %% [markdown]
# ## Step 8 — Prompt Card (worked)
#
# The seven prompts above, in order, are the card. The two worth handing to a
# colleague unchanged: **structured output** (schema + JSON mode transfers to
# any document) and **grounding** (answer-only-from-source + quote is the
# pattern every agency Q&A needs).
#
# ## Reflection (expected answers)
# 1. Grounding usually gives the biggest jump — it converts "sounds right"
#    into "checkably right", which is worth more than eloquence in government
#    work.
# 2. Naming the missing content beats asking harder; format constraints are
#    the cheapest score gains.
# 3. The structured-output and grounding prompts — they are the two that
#    generalize without the author's taste.
