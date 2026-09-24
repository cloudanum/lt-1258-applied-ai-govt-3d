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
# # Lab 7.1 — First Calls with the OpenAI API  *(SOLUTION / instructor copy)*
#
# **Chapter 7 — Building with LLMs: APIs, RAG & Agents**
#
# This is the rewrite of the former Lab 6.3. It uses the current OpenAI Python SDK
# (v1.x+), reads the API key from the environment (already set up for you on the
# VM — there is no key to paste), and pins the model through a single variable so
# the lab keeps working as models change.
#
# **Objectives**
# 1. Make a working chat completion call from Python.
# 2. See how the *system* prompt and *temperature* change the output.
# 3. Get **structured (JSON) output** you can use in a program.
# 4. Read the token usage and estimate cost at agency scale.

# %% [markdown]
# ## Setup — no key to paste
#
# On the classroom VM, `OPENAI_API_KEY` and `OPENAI_MODEL` are already set — the
# helpers create the client and pin the model in one place. If you ever move this
# pattern to Azure OpenAI or Amazon Bedrock in production, only the setup
# changes.

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
# ## Exercise 1 — Your first chat call
#
# The Chat Completions API takes a list of *messages*. Each message has a `role`
# (`system`, `user`, or `assistant`) and `content` — the helper sends the
# student's question as the single user message.

# %%
QUESTION = "In two sentences, what is the Freedom of Information Act?"

first_foia_call(QUESTION)

# %% [markdown]
# ## Exercise 2 — The system prompt changes the voice
#
# Same question, different `system` message. Notice how the persona shifts the
# tone without changing the facts.

# %%
FOIA_QUESTION = "How quickly must an agency respond to a FOIA request?"

FORMAL_PERSONA = "You are a policy analyst. Answer formally, citing the 20-business-day response rule."

PLAIN_PERSONA = "You are explaining to a brand-new employee. Answer in plain, friendly language."

compare_foia_voices(FOIA_QUESTION, FORMAL_PERSONA, PLAIN_PERSONA)

# %% [markdown]
# ## Exercise 3 — Temperature
#
# `temperature` controls randomness. Low (0–0.3) = focused and repeatable; high
# (0.8–1.2) = varied and creative. Run this twice and compare.
#
# Note the model: reasoning models such as the gpt-5 family accept only the
# default temperature and reject anything else, so this one exercise pins a
# temperature-capable model. That is itself worth knowing — "which knobs exist"
# is a property of the model, not of the API.

# %%
TITLE_PROMPT = "Suggest a title for a one-page guide on using AI responsibly in government."

try_temperature_titles(TITLE_PROMPT)

# %% [markdown]
# ## Exercise 4 — Structured output (JSON) from a real document
#
# Programs need structured data, not prose. We ask the model to extract fields
# from the interim-guidance memo as JSON, and enforce it with
# `response_format={"type": "json_object"}` (the helper applies it).
#
# **Worked instruction text** below — the elements that make it reliable:
# naming the keys, giving each a type, and saying "ONLY".

# %%
EXTRACTION_INSTRUCTIONS = (
    "Extract fields from the memo. Reply ONLY with JSON having keys: "
    "subject (string), effective_date (string, YYYY-MM-DD), "
    "key_rules (array of short strings)."
)

extraction = extract_memo_json_71(EXTRACTION_INSTRUCTIONS)

# %% [markdown]
# ## Exercise 5 — Token usage and cost
#
# Every response reports token usage. This is how you estimate what a workload
# costs before you scale it to an agency. Offline, the numbers below are the
# ones captured from a live instructor run — the arithmetic is what students
# must reproduce.
#
# **Expected:** prompt 631 + completion 174 = 805 tokens → ≈ $0.00020 per call,
# ≈ $0.20 per 1,000 calls at the illustrative rates.

# %%
show_token_cost()

# %% [markdown]
# ## Stretch A — Tighten the prompt until it validates every time
#
# **Expected:** 3/3 VALID with the worked instructions above. When a student's
# instructions validate only intermittently, the fix is almost always naming
# the keys explicitly and forbidding extra text.

# %%
validate_extraction_runs(EXTRACTION_INSTRUCTIONS)

# %% [markdown]
# ## Debrief
# 1. Which changed the output more — the system prompt or the temperature? Why?
# 2. Why is JSON output (Exercise 4) more useful in a real system than prose?
# 3. Your agency wants to summarize 50,000 documents a month. Using the cost from
#    Exercise 5, roughly what would that cost — and what would change if you ran it
#    on Azure OpenAI (FedRAMP) instead?
#
# **What changed from the old lab:** the retired `openai.Completion.create(...)`
# call and the `text-davinci-003` model are gone, and there is no `api_key =
# "your_api_key_here"` line — the key comes from the environment.
