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
# # Lab 4.1 — Prompt Engineering Studio
#
# *Chapter 4 — Modern GenAI and Prompt Engineering · 45 minutes · JupyterLab
# with pandas and the OpenAI API via `lab_common` (canned offline fallback)*
#
# This is the consolidation lab. You have already climbed rungs P0–P3, so the
# ladder here names skills you have been using since Day 1: **zero-shot,
# few-shot, reasoning, iteration, role, structured output, grounding.**
# Prompting spine: rung **P4**.
#
# Cells marked `# YOUR CODE` are for you. Offline, every call returns a
# realistic canned answer so you can keep working.

# %% [markdown]
# ## Objectives
#
# By the end of this lab, you will:
#
# - Apply the seven prompt patterns to real government material.
# - Score every output against the rubric and improve the weakest.
# - Leave with a personal, tested prompt library.

# %% [markdown]
# ## Setup
#
# **Datasets and files** (all under `labs/data/`):
#
# - `gov_memo.txt` — GAO-style CDO memorandum: interim guidance on generative
#   AI for constituent services (substrate for the zero-shot, reasoning, and
#   structured-output patterns)
# - `chicago_311.csv` — 4,000 real Chicago 311 service requests (few-shot
#   classification labels)
# - `corpus/ai_acceptable_use_policy.md` — agency AI acceptable-use policy
#   (role and grounding patterns)
#
# **Tools:** pandas, plus the OpenAI chat API through `lab_common.chat()` /
# `lab_common.chat_json()` — offline these return canned stand-ins, so the
# notebook never hard-fails on a keyless machine.
#
# **Data rule:** every file above is either genuinely public US government
# data (documented in `data/MANIFEST.json`) or synthetic material written for
# this course. Never paste real agency data containing PII into these
# notebooks — or into any AI tool.

# %%
# API key status — lab_common loads OPENAI_API_KEY from the environment
# (classroom VM) or the course .env file at import. The key is never printed.
# With no key, every AI call below falls back to a realistic canned output.
import lab_common as lc

if lc.online():
    print(f"OpenAI API key found — live mode (model: {lc.CHAT_MODEL}).")
else:
    print("No API key found — offline mode: AI calls return realistic canned "
          "outputs, so every step still runs.\nAsk your instructor if you "
          "expected a key on this machine.")

# %% [markdown]
# ### The substrate (provided)
#
# Three real course documents: a CDO memo on generative AI, Chicago 311
# request types, and the agency's acceptable-use policy.

# %%
from lab_common import chat, chat_json

memo = open("data/gov_memo.txt").read()
policy = open("data/corpus/ai_acceptable_use_policy.md").read()

import pandas as pd
c311 = pd.read_csv("data/chicago_311.csv", low_memory=False)
sr_types = c311["sr_type"].dropna().unique().tolist()

print(f"memo: {len(memo)} chars | policy: {len(policy)} chars | "
      f"{len(sr_types)} distinct 311 request types")

# %% [markdown]
# ## Steps
#
# 1. Open `lab_4.1_prompt_studio.ipynb` and run the Setup cells.
# 2. **Zero-shot:** summarise the GAO-style memo. Score it. (5 min)
# 3. **Few-shot:** add two exemplars to a 311 classification. Score it. (5 min)
# 4. **Reasoning:** run the hardest item on a reasoning model, no CoT
#    instruction. (5 min)
# 5. **Iterate:** take your worst output and improve it in three rounds,
#    keeping each version. (6 min)
# 6. **Role:** 'You are a FOIA officer...' on the acceptable-use policy. (5 min)
# 7. **Structured output:** extract the memo's key entities into a table.
#    (6 min)
# 8. **Grounding:** answer only from the policy, with the quoted sentence.
#    (6 min)
# 9. Copy your best prompt from each pattern onto your Prompt Card. (7 min)
#
# Each step below is one pattern. Score every output 1–5 per rubric dimension
# and record it in the `scorecard` dict — it drives Step 5.

# %% [markdown]
# ### The course rubric — score every output 1–5 per dimension
#
# | Dimension | 1 | 3 | 5 |
# |---|---|---|---|
# | **Accuracy** | invented or wrong claims | minor overstatement | every claim supported |
# | **Completeness** | misses the point | covers it thinly | covers it, no padding |
# | **Format** | ignores instructions | mostly follows them | exactly what was asked |
# | **Tone** | wrong register | uneven | right for the audience |

# %%
scorecard = {}  # {pattern_name: {"accuracy": n, "completeness": n, "format": n, "tone": n}}
# You will fill this in as you go — it drives Step 5 (improve the weakest).

# %% [markdown]
# ### Step 2 — Zero-shot (5 min)
#
# *Pattern 1.* Summarize the CDO memo with no examples, no role, no
# scaffolding — the baseline everything else is measured against.

# %%
CANNED_ZEROSHOT = (
    "The memo gives divisions interim rules for using generative AI in "
    "constituent services: a human must review every AI-assisted product "
    "before release, only public information may go into public AI tools, "
    "internal work must use the approved enterprise assistant, and AI-drafted "
    "correspondence is a federal record that must be retained. It is "
    "effective immediately until a final policy is issued."
)

zero_shot = None
# YOUR CODE: chat() with a one-line user message asking for a summary of
# `memo`. Pass offline=CANNED_ZEROSHOT.

if zero_shot is None:
    zero_shot = CANNED_ZEROSHOT
    print("(canned zero-shot summary — write your prompt above to run your own)\n")
print(zero_shot)

# %% [markdown]
# ### Step 3 — Few-shot (5 min)
#
# *Pattern 2.* Classify 311 request types into service categories. Give the
# model **two exemplars** first, then ask it to classify three new types.

# %%
CANNED_FEWSHOT = (
    "Graffiti Removal Request -> Property & Streets\n"
    "Tree Emergency -> Urban Forestry\n"
    "Water On Street Complaint -> Water & Drainage"
)

few_shot = None
# YOUR CODE: build a user message with two exemplar classifications of your
# own (e.g. "Aircraft Noise Complaint -> Noise", "311 INFORMATION ONLY CALL
# -> Information"), then three types from `sr_types` to classify. chat() with
# offline=CANNED_FEWSHOT.

if few_shot is None:
    few_shot = CANNED_FEWSHOT
    print("(canned few-shot output — write your exemplars above to run your own)\n")
print(few_shot)

# %% [markdown]
# ### Step 4 — Reasoning (5 min)
#
# *Pattern 3.* Give the model the hardest item you have — a multi-constraint
# question on the memo — with **no** chain-of-thought instruction. Modern
# reasoning models do the work internally; your job is to ask the hard thing
# clearly.

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

reasoning = None
# YOUR CODE: chat() with HARD_ITEM + the memo text. Pass offline=CANNED_REASONING.

if reasoning is None:
    reasoning = CANNED_REASONING
    print("(canned reasoning output — write your call above to run your own)\n")
print(reasoning)

# %% [markdown]
# ### Step 5 — Iterate on your weakest output (6 min)
#
# *Pattern 4.* Look at your scorecard. Take the **worst-scoring** output so
# far and improve it in three rounds, keeping each version. Write what you
# changed each round.

# %%
iterations = []
# YOUR CODE: three rounds. Append (prompt, output) tuples to `iterations`.
# Change ONE thing per round (specificity? format constraint? audience?) so
# you can see what actually moved the score.

if not iterations:
    print("(no iterations yet — this step is yours; see the solution copy "
          "for a worked example)")

# %% [markdown]
# #### Iteration log (write here)
#
# - Round 1 — changed: / score before → after:
# - Round 2 — changed: / score before → after:
# - Round 3 — changed: / score before → after:

# %% [markdown]
# ### Step 6 — Role (5 min)
#
# *Pattern 5.* "You are a FOIA officer..." — set a role, then apply it to the
# acceptable-use policy.

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

role_out = None
# YOUR CODE: system message "You are a FOIA officer reviewing a draft
# acceptable-use policy..." + the policy text. Pass offline=CANNED_ROLE.

if role_out is None:
    role_out = CANNED_ROLE
    print("(canned role output — write your role prompt above to run your own)\n")
print(role_out)

# %% [markdown]
# ### Step 7 — Structured output (6 min)
#
# *Pattern 6.* Extract the memo's key entities into a table a program can
# use. Force JSON and parse it — this is the pattern that feeds downstream
# systems.

# %%
CANNED_ENTITIES = {"entities": [
    {"type": "organization", "name": "Office of the Chief Data Officer", "detail": "issuing office and point of contact"},
    {"type": "date", "name": "March 14, 2026", "detail": "memo date; effective immediately"},
    {"type": "rule", "name": "Human review", "detail": "responsible employee must approve AI-assisted products before release"},
    {"type": "rule", "name": "Data handling", "detail": "only public information in public tools; report exposure within one business day"},
    {"type": "rule", "name": "Approved tools", "detail": "enterprise assistant required for internal information"},
    {"type": "rule", "name": "Recordkeeping", "detail": "AI-assisted correspondence is a federal record"},
]}

entities = None
# YOUR CODE: chat_json() asking for the memo's entities under key "entities",
# each with {type, name, detail}. Pass offline=CANNED_ENTITIES.

if entities is None:
    entities = CANNED_ENTITIES
    print("(canned entities — write your chat_json call above to run your own)\n")
print(pd.DataFrame(entities["entities"]).to_string(index=False))

# %% [markdown]
# ### Step 8 — Grounding (6 min)
#
# *Pattern 7.* Answer **only** from the acceptable-use policy, and require the
# model to quote the sentence it relied on. Grounding is the difference
# between "plausible" and "defensible".

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

grounded = None
# YOUR CODE: chat() with QUESTION + the policy text; instruct the model to
# answer only from the policy and to quote the supporting sentence.
# Pass offline=CANNED_GROUNDED.

if grounded is None:
    grounded = CANNED_GROUNDED
    print("(canned grounded answer — write your call above to run your own)\n")
print(grounded)

# check the quote really is in the policy (grounding, verified mechanically):
quote = "Pasting a constituent's record into a public chatbot is a reportable data spill."
print("\nquote verified in policy:", quote in policy)

# %% [markdown]
# ### Step 9 — Your Prompt Card (7 min)
#
# Copy your best prompt from each pattern into the markdown cell below. This
# is the seed of the template library you build in Lab 4.2.
#
# #### My Prompt Card (write here)
#
# - Zero-shot:
# - Few-shot:
# - Reasoning:
# - Iteration (final version):
# - Role:
# - Structured output:
# - Grounding:

# %% [markdown]
# ## Deliverable
# 1. All seven pattern outputs with rubric scores in `scorecard`.
# 2. The three-round iteration log for your weakest output.
# 3. Your completed Prompt Card.

# %% [markdown]
# ## Reflection
# 1. Which pattern gave the biggest jump in rubric score?
# 2. Which of your three iteration rounds actually helped, and why?
# 3. Which prompt would you hand to a colleague unchanged?

# %% [markdown]
# ## Debrief (instructor-led)
#
# - **Compare Prompt Cards.** Which pattern showed the most divergence
#   between students' prompts — and what does that tell you about the
#   pattern?
# - **Live vs canned.** If anyone ran offline, re-run one cell with the key
#   present and compare: did the rubric score change?
# - **Bridge to Lab 4.2.** Which of your seven prompts is the best candidate
#   to templatize, and which slots would it need?

# %% [markdown]
# ## Troubleshooting
#
# - **`FileNotFoundError: data/gov_memo.txt`** — the kernel's working
#   directory is not `labs/`. Restart the kernel from the `labs/` folder and
#   Run All.
# - **`ModuleNotFoundError: lab_common`** — same cause: the notebook must run
#   with `labs/` as its working directory.
# - **Every AI cell prints "(canned ...)"** — no API key is visible. On the
#   classroom VM the key is injected; on your own machine it comes from the
#   course `.env`. The lab is fully usable either way.
# - **API errors (rate limit, authentication)** — re-run the cell once; if it
#   persists, the canned path keeps you moving. Tell your instructor.
# - **`quote verified in policy: False`** — the quoted sentence is not in the
#   policy. That is the grounding lesson: require the quote, then check it
#   mechanically before you trust the answer.
