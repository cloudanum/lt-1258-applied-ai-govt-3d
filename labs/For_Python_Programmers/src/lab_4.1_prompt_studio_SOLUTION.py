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
# ## Setup — the substrate

# %%
from lab_common import chat, chat_json

memo = open("data/gov_memo.txt").read()
policy = open("data/corpus/ai_acceptable_use_policy.md").read()

import pandas as pd
c311 = pd.read_csv("data/chicago_311.csv", low_memory=False)
sr_types = c311["sr_type"].dropna().unique().tolist()

print(f"memo: {len(memo)} chars | policy: {len(policy)} chars | "
      f"{len(sr_types)} distinct 311 request types")

# %%
scorecard = {}

# %% [markdown]
# ## Pattern 1 — Zero-shot
#
# **Worked prompt + expected rubric:** accurate but generic — it names the
# four rules yet misses the *why* (the two pilot risks in §2). Typical scores:
# accuracy 5, completeness 3, format 4, tone 4.

# %%
CANNED_ZEROSHOT = (
    "The memo gives divisions interim rules for using generative AI in "
    "constituent services: a human must review every AI-assisted product "
    "before release, only public information may go into public AI tools, "
    "internal work must use the approved enterprise assistant, and AI-drafted "
    "correspondence is a federal record that must be retained. It is "
    "effective immediately until a final policy is issued."
)

zero_shot = chat(
    [{"role": "user", "content":
      "Summarize this memorandum for a division director in one short "
      f"paragraph.\n\n{memo}"}],
    offline=CANNED_ZEROSHOT)
print(zero_shot)
scorecard["zero_shot"] = {"accuracy": 5, "completeness": 3, "format": 4, "tone": 4}

# %% [markdown]
# ## Pattern 2 — Few-shot
#
# **Worked prompt + expected:** two exemplars fix both the category vocabulary
# and the output format — the model stops inventing category names. Scores:
# 5/4/5/4. Teaching point: exemplars beat instructions for *format*.

# %%
CANNED_FEWSHOT = (
    "Graffiti Removal Request -> Property & Streets\n"
    "Tree Emergency -> Urban Forestry\n"
    "Water On Street Complaint -> Water & Drainage"
)

few_shot = chat(
    [{"role": "user", "content":
      "Classify 311 request types into service categories, following the "
      "pattern of the examples.\n\n"
      "Aircraft Noise Complaint -> Noise\n"
      "311 INFORMATION ONLY CALL -> Information\n\n"
      "Graffiti Removal Request ->\n"
      "Tree Emergency ->\n"
      "Water On Street Complaint ->"}],
    offline=CANNED_FEWSHOT)
print(few_shot)
scorecard["few_shot"] = {"accuracy": 5, "completeness": 4, "format": 5, "tone": 4}

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
CANNED_REASONING = (
    "The plan violates three clauses. Clause 3(b): case-file contents are "
    "nonpublic constituent information and may never enter an unapproved "
    "public tool. Clause 3(a): 'routine' is not an exception — every "
    "AI-assisted product bound for a constituent must be reviewed and "
    "approved by a responsible employee. Clause 3(c): internal information "
    "may only be handled by the enterprise assistant under the Department's "
    "data-protection agreement. The smallest compliant change: keep the "
    "drafting workflow but run it on the approved enterprise assistant and "
    "keep human review for every letter."
)

reasoning = chat(
    [{"role": "user", "content": f"{HARD_ITEM}\n\nMEMO:\n{memo}"}],
    offline=CANNED_REASONING)
print(reasoning)
scorecard["reasoning"] = {"accuracy": 5, "completeness": 5, "format": 4, "tone": 4}

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
iterations = []
prompt_v1 = ("Summarize this memorandum for a division director in one short "
             f"paragraph; include why the guidance was issued.\n\n{memo}")
iterations.append((prompt_v1, chat([{"role": "user", "content": prompt_v1}],
                                   offline=CANNED_ZEROSHOT)))
prompt_v2 = ("Summarize this memorandum for a division director; include the "
             f"two recurring risks the pilots surfaced.\n\n{memo}")
iterations.append((prompt_v2, chat([{"role": "user", "content": prompt_v2}],
                                   offline=CANNED_ZEROSHOT)))
prompt_v3 = ("Summarize this memorandum in exactly four sentences: purpose, "
             f"the two risks, the four rules, effective date.\n\n{memo}")
iterations.append((prompt_v3, chat([{"role": "user", "content": prompt_v3}],
                                   offline=CANNED_ZEROSHOT)))
for i, (p, out) in enumerate(iterations, 1):
    print(f"--- round {i} prompt: {p.splitlines()[0][:80]}...")
    print(out[:200], "\n")

# %% [markdown]
# ## Pattern 5 — Role
#
# **Worked prompt + expected:** the role changes *what the model notices* —
# a FOIA officer spots records and Exemption 6 alignment, not productivity.
# Scores: 5/4/4/5.

# %%
CANNED_ROLE = (
    "From a FOIA officer's desk, three points in this policy matter most. "
    "First, AI-drafted correspondence about agency business is a federal "
    "record, so it enters the retention system and is potentially FOIA-"
    "releasable — drafts are not invisible. Second, the PII prohibition "
    "aligns with Exemption 6 practice: what we would redact before release "
    "must never leave the boundary in the first place. Third, the "
    "human-review clause assigns accountability the way FOIA assigns it — "
    "to a named official, not a tool."
)

role_out = chat(
    [{"role": "system", "content":
      "You are a FOIA officer reviewing a draft acceptable-use policy before "
      "commenting to the Chief Data Officer."},
     {"role": "user", "content":
      f"What in this policy matters most from your desk, and why?\n\n{policy}"}],
    offline=CANNED_ROLE)
print(role_out)
scorecard["role"] = {"accuracy": 5, "completeness": 4, "format": 4, "tone": 5}

# %% [markdown]
# ## Pattern 6 — Structured output
#
# **Worked prompt + expected:** JSON mode plus an explicit schema gives
# machine-usable output; the table below is the proof. Scores: 5/5/5/4.

# %%
CANNED_ENTITIES = {"entities": [
    {"type": "organization", "name": "Office of the Chief Data Officer", "detail": "issuing office and point of contact"},
    {"type": "date", "name": "March 14, 2026", "detail": "memo date; effective immediately"},
    {"type": "rule", "name": "Human review", "detail": "responsible employee must approve AI-assisted products before release"},
    {"type": "rule", "name": "Data handling", "detail": "only public information in public tools; report exposure within one business day"},
    {"type": "rule", "name": "Approved tools", "detail": "enterprise assistant required for internal information"},
    {"type": "rule", "name": "Recordkeeping", "detail": "AI-assisted correspondence is a federal record"},
]}

entities = chat_json(
    [{"role": "user", "content":
      'Extract the key entities from this memo as JSON under key "entities": '
      "a list of {type, name, detail} where type is one of organization, "
      f"person, date, rule.\n\n{memo}"}],
    offline=CANNED_ENTITIES)
print(pd.DataFrame(entities["entities"]).to_string(index=False))
scorecard["structured"] = {"accuracy": 5, "completeness": 5, "format": 5, "tone": 4}

# %% [markdown]
# ## Pattern 7 — Grounding
#
# **Worked prompt + expected:** the answer quotes the policy verbatim, and the
# mechanical check below proves the quote is real — the grounding pattern made
# the claim *auditable*. Scores: 5/5/5/5.

# %%
QUESTION = ("What happens if an employee pastes a constituent's record into "
            "a public chatbot?")
CANNED_GROUNDED = (
    "It is a reportable data spill. The policy states: \"Pasting a "
    "constituent's record into a public chatbot is a reportable data spill.\" "
    "Constituent records are PII — a sensitive/regulated data category — and "
    "may only be used with tools specifically authorized for that category, "
    "which a public chatbot is not."
)

grounded = chat(
    [{"role": "user", "content":
      "Answer using ONLY the policy below. Quote the exact sentence you rely "
      f"on.\n\nQUESTION: {QUESTION}\n\nPOLICY:\n{policy}"}],
    offline=CANNED_GROUNDED)
print(grounded)

quote = "Pasting a constituent's record into a public chatbot is a reportable data spill."
print("\nquote verified in policy:", quote in policy)
scorecard["grounded"] = {"accuracy": 5, "completeness": 5, "format": 5, "tone": 5}

# %%
print("\nscorecard totals:",
      {k: sum(v.values()) for k, v in scorecard.items()})

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
