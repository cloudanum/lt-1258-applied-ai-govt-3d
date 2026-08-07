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
# On the classroom VM, `OPENAI_API_KEY` and `OPENAI_MODEL` are already set. We just
# create a client and pin the model in one place. If you ever move this code to
# Azure OpenAI or Amazon Bedrock in production, only this cell changes.

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

# %%
import os
from lab_common import (get_client, CHAT_MODEL, TEMPERATURE_MODEL,
                        note_api_failure)

# The instructor copy runs in the offline smoke test too, so the client may be
# absent. `call()` keeps every exercise below reading like a plain SDK call
# while still producing the transcript when there is no key.
client = get_client()                               # reads OPENAI_API_KEY from the environment
MODEL = CHAT_MODEL                                  # one place to change the model
print("Using model:", MODEL)
if client is None:
    print("(offline — canned instructor answers below; live runs differ in "
          "wording, not in the verified numbers)")


def call(canned, model=None, **kwargs):
    """One chat completion, or the canned instructor answer when offline.

    `model` defaults to MODEL; Exercise 3 overrides it because varying
    temperature needs a model that accepts temperature at all.
    """
    if client is None:
        return canned
    try:
        return client.chat.completions.create(
            model=model or MODEL, **kwargs).choices[0].message.content
    except Exception as e:
        print(f"({type(e).__name__} — call failed; canned answer)")
        return canned

# %% [markdown]
# ## Exercise 1 — Your first chat call
#
# The Chat Completions API takes a list of *messages*. Each message has a `role`
# (`system`, `user`, or `assistant`) and `content`.

# %%
print(call(
    "The Freedom of Information Act (FOIA) gives any person the right to request "
    "records from U.S. executive-branch agencies. Agencies must generally respond "
    "within 20 business days, releasing records unless one of nine exemptions applies.",
    messages=[
        {"role": "system", "content": "You are a concise assistant for U.S. government IT staff."},
        {"role": "user", "content": "In two sentences, what is the Freedom of Information Act?"},
    ],
))

# %% [markdown]
# ## Exercise 2 — The system prompt changes the voice
#
# Same question, different `system` message. Notice how the persona shifts the
# tone without changing the facts.

# %%
for persona in [
    "You are a policy analyst. Answer formally, citing the 20-business-day response rule.",
    "You are explaining to a brand-new employee. Answer in plain, friendly language.",
]:
    canned = (
        "Under the Freedom of Information Act (5 U.S.C. § 552), an agency must "
        "determine whether to comply within twenty (20) business days of receipt. "
        "In unusual circumstances it may extend by up to ten additional business "
        "days, provided it notifies the requester in writing."
        if "policy analyst" in persona else
        "Think of it as a 20-working-day clock: once your FOIA request arrives, the "
        "agency has about four weeks of business days to get back to you. If things "
        "get complicated it can take a bit longer, but it has to tell you first.")
    print(f"\n--- persona: {persona[:40]}... ---")
    print(call(canned, messages=[
        {"role": "system", "content": persona},
        {"role": "user", "content": "How quickly must an agency respond to a FOIA request?"},
    ]))

# %% [markdown]
# ## Exercise 3 — Temperature
#
# `temperature` controls randomness. Low (0–0.3) = focused and repeatable; high
# (0.8–1.2) = varied and creative. Run this twice and compare.
#
# Note the model on the first line: reasoning models such as the gpt-5 family
# accept only the default temperature and reject anything else, so this one
# exercise pins a temperature-capable model. That is itself worth knowing —
# "which knobs exist" is a property of the model, not of the API.

# %%
print("Exercise 3 uses:", TEMPERATURE_MODEL, f"(the rest of this lab uses {MODEL})")
for temp in [0.0, 1.0]:
    canned = ("Responsible AI in Government: A One-Page Guide" if temp == 0.0
              else "AI With Guardrails: A Field Guide for Public Servants")
    out = call(canned, model=TEMPERATURE_MODEL, temperature=temp,
               messages=[{"role": "user",
                          "content": "Suggest a title for a one-page guide on using AI responsibly in government."}])
    print(f"temperature={temp}: {out.strip()}")

# %% [markdown]
# ## Exercise 4 — Structured output (JSON) from a real document
#
# Programs need structured data, not prose. We ask the model to extract fields
# from the interim-guidance memo as JSON, and enforce it with
# `response_format={"type": "json_object"}`.

# %%
import json
memo = open("data/gov_memo.txt").read()

CANNED_JSON = json.dumps({
    "subject": "Interim Guidance on Generative AI for Constituent Services",
    "effective_date": "2026-03-14",
    "key_rules": [
        "Every AI-assisted work product must be reviewed by a responsible employee before release.",
        "Only public information may be entered into public AI tools; PII never.",
        "Internal information must use the approved enterprise assistant.",
        "AI-assisted correspondence is a federal record and must be retained.",
        "AI assistance must be disclosed in the reply and the reviewer logged.",
    ],
}, indent=2)

data = json.loads(call(
    CANNED_JSON,
    response_format={"type": "json_object"},
    messages=[
        {"role": "system",
         "content": "Extract fields from the memo. Reply ONLY with JSON having keys: "
                    "subject (string), effective_date (string), key_rules (array of short strings)."},
        {"role": "user", "content": memo},
    ],
))
print(json.dumps(data, indent=2))
assert "subject" in data and "key_rules" in data, "expected keys present"

# %% [markdown]
# ## Exercise 5 — Token usage and cost
#
# Every response reports token usage. This is how you estimate what a workload
# costs before you scale it to an agency.

# %%
# Re-run the Exercise 4 extraction and keep the whole response, so we can read
# `usage` off it. Offline, the numbers below are the ones captured from a live
# instructor run — the arithmetic is what students must reproduce.
prompt_tokens = completion_tokens = None
if client is not None:
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system",
                 "content": "Extract fields from the memo. Reply ONLY with JSON having keys: "
                            "subject (string), effective_date (string), key_rules (array of short strings)."},
                {"role": "user", "content": memo},
            ],
        )
        prompt_tokens = resp.usage.prompt_tokens
        completion_tokens = resp.usage.completion_tokens
    except Exception as e:
        # A live key with no credits still lands here; the captured numbers
        # keep the cost arithmetic — the actual point of this exercise — intact.
        note_api_failure(e)
if prompt_tokens is None:
    prompt_tokens, completion_tokens = 631, 174   # captured from a live run

total_tokens = prompt_tokens + completion_tokens
print(f"prompt tokens:     {prompt_tokens}")
print(f"completion tokens: {completion_tokens}")
print(f"total tokens:      {total_tokens}")

# Illustrative pricing — confirm current rates for your pinned model.
PRICE_IN_PER_1K, PRICE_OUT_PER_1K = 0.00015, 0.0006
cost = prompt_tokens/1000*PRICE_IN_PER_1K + completion_tokens/1000*PRICE_OUT_PER_1K
print(f"\nthis call ≈ ${cost:.5f}")
print(f"1,000 similar calls ≈ ${cost*1000:.2f}")

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
