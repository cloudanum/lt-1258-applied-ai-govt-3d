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
# with pandas and the OpenAI API via the course helpers (canned offline
# fallback)*
#
# This is the consolidation lab, and it is a ladder: four rungs, each one
# change to the prompt — **zero-shot → few-shot → role + format contract →
# reasoning-model comparison** — every output scored against the same rubric.
# The finding is not the four outputs; it is which single rung bought the most
# quality. Prompting spine: rung **P4**.
#
# Cells marked `# YOUR TURN` ask you to edit the prompt text and re-run.
# Offline, every call returns a realistic canned answer so you can keep
# working.

# %% [markdown]
# ## Objectives
#
# By the end of this lab, you will:
#
# - Measurably improve an output by iterating your prompt.
# - Apply zero-shot, few-shot, role + format, and reasoning-model techniques.
# - Score outputs against a rubric.

# %% [markdown]
# ## Setup
#
# **Datasets and files** (all under `labs/data/`):
#
# - `gov_memo.txt` — the **policy memo**: a synthetic CDO memorandum giving
#   interim guidance on generative AI for constituent services. Five lettered
#   rules in section 3. Substrate for rungs 1–3.
# - `constituent_feedback.csv` — the **constituent-feedback set**: fifteen
#   synthetic messages of mixed urgency. Substrate for rung 4.
# - `MANIFEST.json` — the **dataset description**: provenance for every file
#   in `data/`, public and synthetic.
# - `chicago_311.csv`, `corpus/ai_acceptable_use_policy.md` — used by the
#   stretch section.
#
# **Tools:** the OpenAI chat API through the course helpers — offline these
# return canned stand-ins, so the notebook never hard-fails on a keyless
# machine.
#
# **Data rule:** every file above is either genuinely public US government
# data (documented in `data/MANIFEST.json`) or synthetic material written for
# this course. Never paste real agency data containing PII into these
# notebooks — or into any AI tool.
#
# **How this notebook works:** every step is one provided cell — run it with
# Shift+Enter and read what it prints. Cells marked `# YOUR TURN` ask you to
# edit the prompt text (ordinary quoted text — no code) and re-run the cell.
# Everything runs as shipped, so you can never get stuck.

# %%
# ▶ Setup — run this cell first (click it, then Shift+Enter).
# It loads the course helper functions used by every step below.
from lab_helpers import *
lab_status()

# %% [markdown]
# ### The substrate (provided)
#
# The workbook source pack: the policy memo, the constituent-feedback set, and
# the dataset description in `MANIFEST.json` — plus the two files the stretch
# section uses. Run this cell to load them.

# %%
materials = load_prompt_studio_materials()

# %% [markdown]
# ## Steps
#
# The prompt ladder — four rungs, each one change to the prompt, each scored
# against the same rubric. The point is not the four outputs; it is seeing which
# single change bought the most quality.
#
# 1. **Zero-shot.** Ask the assistant to "summarize the policy memo." Score it.
#    ✓ You have a baseline output and a rubric score.
# 2. **Few-shot.** Give two examples of the summary style you want, then ask
#    again. ✓ You can see how examples changed the output.
# 3. **Role + format contract.** *"You are a policy analyst. Summarize the memo
#    as a 5-row table: rule | who it affects | effective date | source line."*
#    Score it. ✓ You have a structured, role-shaped output.
# 4. **Reasoning-model comparison.** Run the hardest task — classify each
#    constituent complaint by theme and urgency — on a standard model and on a
#    reasoning model. Compare. ✓ You can describe when the reasoning model
#    helped.
#
# Score every output 1–5 per rubric dimension and record it in the scorecard
# below.

# %% [markdown]
# ### The course rubric — score every output 1–5 per dimension
#
# | Dimension | 1 | 3 | 5 |
# |---|---|---|---|
# | **Accuracy** | invented or wrong claims | minor overstatement | every claim supported |
# | **Completeness** | misses the point | covers it thinly | covers it, no padding |
# | **Format** | ignores instructions | mostly follows them | exactly what was asked |
# | **Tone** | wrong register | uneven | right for the audience |
#
# #### My scorecard (write here — it drives Stretch B: improve the weakest)
#
# | output | accuracy | completeness | format | tone |
# |---|---|---|---|---|
# | zero-shot | | | | |
# | few-shot | | | | |
# | role + format | | | | |
# | reasoning comparison | | | | |

# %% [markdown]
# ### Rung 1 — Zero-shot (8 min)
#
# Ask the assistant to "summarize the policy memo" with no examples, no role, no
# scaffolding — the baseline everything else is measured against. The cell below
# carries a working prompt; **edit the text** to make it yours, re-run, and
# score the output.

# %%
MY_PROMPT = """Summarize this memorandum for a division director in one short paragraph."""   # ← YOUR TURN: edit this prompt text, then re-run this cell

zero_shot = ask_about_memo(materials, MY_PROMPT)

# %% [markdown]
# ### Rung 2 — Few-shot (10 min)
#
# Same memo, same request — but first show the model **two examples of the
# summary style you want**. Nothing else changes. The cell below carries two
# exemplars in the house style you would actually send: one line per rule, the
# affected group named, no throat-clearing. **Edit them into your own style**
# and re-run.

# %%
MY_EXAMPLES = """Human review — every division: no AI-assisted product reaches a constituent or the public record until a named employee has approved it.
Data handling — every employee: public information only in public tools; suspected exposure is reported within one business day."""   # ← YOUR TURN: replace with YOUR two exemplars, then re-run this cell

few_shot = ask_with_examples(materials, MY_EXAMPLES)

# %% [markdown]
# ### Rung 3 — Role + format contract (12 min)
#
# Two changes at once, because they work as a pair: give the model a **role**
# and a **format contract**. The role sets what it optimises for; the contract
# says exactly what shape to return.
#
# > *"You are a policy analyst. Summarize the memo as a 5-row table:
# > rule | who it affects | effective date | source line."*
#
# The memo has five lettered rules in section 3 — one row each. The `source
# line` column is the one that keeps it honest: it forces the model to point at
# the clause it used, so you can check it.

# %%
MY_ROLE = "You are a policy analyst."   # ← YOUR TURN: change the role, then re-run this cell

MY_ASK = """Summarize the memo as a 5-row markdown table with exactly these columns: rule | who it affects | effective date | source line. One row per lettered rule in section 3. The source line column must quote the clause you used."""   # ← YOUR TURN: change the format contract too, if you like

role_format = ask_with_role(materials, MY_ROLE, MY_ASK)

# %% [markdown]
# ### Rung 4 — Reasoning-model comparison (15 min)
#
# The hardest task in the lab: classify **every** constituent message by
# **theme** and **urgency**. Fifteen messages, mixed — two are live safety
# emergencies, one is a compliment, several are routine records requests. Run it
# on the standard model and on a reasoning model, then compare. Both cells are
# provided — run them and read.
#
# Urgency is where they diverge. Getting theme right is pattern-matching;
# getting urgency right needs the model to notice that "flood water is coming up
# through the drain" outranks "I would like copies of the grant awards" even
# though both are politely worded.

# %%
standard, reasoning = compare_models_on_triage(materials)

# %%
show_urgency_disagreements(materials, standard, reasoning)

# %% [markdown]
# ## Stretch (not timed)
#
# The workbook page ends at rung 4. Everything below is optional — the other
# three patterns from the a2 lab, kept because they are useful, and the Prompt
# Card that Lab 4.2 builds on.

# %% [markdown]
# ### Stretch A — A harder single-model question
#
# Give the model the hardest item you have — a multi-constraint question on the
# memo — with **no** chain-of-thought instruction. Modern reasoning models do the
# work internally; your job is to ask the hard thing clearly. A working question
# is provided — edit it, or ask your own.

# %%
HARD_QUESTION = """A division wants to use a free public chatbot to draft reply letters that quote from constituent case files, and to skip review for 'routine' replies. Under the memo, which specific clauses does this violate, and what is the smallest change that would make the plan compliant?"""   # ← YOUR TURN: edit the hard question, then re-run this cell

reasoning_answer = ask_hard_question(materials, HARD_QUESTION)

# %% [markdown]
# ### Stretch B — Iterate on your weakest output
#
# Look at your scorecard. Take the **worst-scoring** output so
# far and improve it in three rounds, keeping each version. Write what you
# changed each round. The cell below carries a worked three-round improvement
# of the rung-1 summary — **replace the three prompts with your own rounds**:
# change ONE thing per round (specificity? format constraint? audience?) so
# you can see what actually moved the score.

# %%
ROUND_1_PROMPT = """Summarize this memorandum for a division director in one short paragraph; include why the guidance was issued."""   # ← YOUR TURN: your round-1 prompt
ROUND_2_PROMPT = """Summarize this memorandum for a division director; include the two recurring risks the pilots surfaced."""   # ← YOUR TURN: your round-2 prompt (one more change)
ROUND_3_PROMPT = """Summarize this memorandum in exactly four sentences: purpose, the two risks, the four rules, effective date."""   # ← YOUR TURN: your round-3 prompt (one more change)

iterate_on_prompt(materials, [ROUND_1_PROMPT, ROUND_2_PROMPT, ROUND_3_PROMPT])

# %% [markdown]
# #### Iteration log (write here)
#
# - Round 1 — changed: / score before → after:
# - Round 2 — changed: / score before → after:
# - Round 3 — changed: / score before → after:

# %% [markdown]
# ### Stretch C — Role: a FOIA officer on the acceptable-use policy
#
# "You are a FOIA officer..." — set a role, then apply it to the
# acceptable-use policy.

# %%
MY_POLICY_ROLE = "You are a FOIA officer reviewing a draft acceptable-use policy before commenting to the Chief Data Officer."   # ← YOUR TURN: try a different role (an auditor? a union rep?), then re-run this cell

role_out = ask_policy_with_role(materials, MY_POLICY_ROLE)

# %% [markdown]
# ### Stretch D — Structured output: entities as JSON
#
# Extract the memo's key entities into a table a program can
# use. JSON mode forces machine-readable output — this is the pattern that
# feeds downstream systems. Provided — run it and read the table.

# %%
entities = extract_memo_fields(materials)

# %% [markdown]
# ### Stretch E — Grounding: answer only from the policy
#
# Answer **only** from the acceptable-use policy, and require the
# model to quote the sentence it relied on. Grounding is the difference
# between "plausible" and "defensible". The cell also checks the quote
# mechanically against the policy text.

# %%
MY_QUESTION = "What happens if an employee pastes a constituent's record into a public chatbot?"   # ← YOUR TURN: ask a different question about the policy, then re-run this cell

grounded = ask_policy_only(materials, MY_QUESTION)

# %% [markdown]
# ### Stretch F — Your Prompt Card (Lab 4.2 builds on this)
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
#
# One **before/after prompt pair** with its two rubric scores, and a one-line
# note on **which rung of the ladder bought the most quality**.
#
# (Keep the full scorecard too — it is the evidence behind that one line.)

# %% [markdown]
# ## Reflection
# 1. Where did the model sound confident but get a fact wrong? How did you catch
#    it?
# 2. When would you stop iterating and switch approach (RAG? a different tool)?

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
# - **`ModuleNotFoundError: lab_helpers`** — the kernel's working directory is
#   not `labs/`. Restart the kernel from the `labs/` folder and Run All.
# - **Every AI cell prints "(offline canned ...)"** — no API key is visible. On
#   the classroom VM the key is injected; on your own machine it comes from the
#   course `.env`. The lab is fully usable either way.
# - **API errors (rate limit, authentication)** — re-run the cell once; if it
#   persists, the canned path keeps you moving. Tell your instructor.
# - **`quote verified in policy: False`** — the quoted sentence is not in the
#   policy. That is the grounding lesson: require the quote, then check it
#   mechanically before you trust the answer.

# %% [markdown]
# ---
# *Curious about the Python behind these steps? The full code-forward version
# of this lab lives in the `For_Python_Programmers/` folder.*
