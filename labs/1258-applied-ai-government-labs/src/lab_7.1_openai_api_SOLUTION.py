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
import os
from openai import OpenAI

client = OpenAI()                                   # reads OPENAI_API_KEY from the environment
MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")     # one place to change the model
print("Using model:", MODEL)

# %% [markdown]
# ## Exercise 1 — Your first chat call
#
# The Chat Completions API takes a list of *messages*. Each message has a `role`
# (`system`, `user`, or `assistant`) and `content`.

# %%
resp = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a concise assistant for U.S. government IT staff."},
        {"role": "user", "content": "In two sentences, what is the Freedom of Information Act?"},
    ],
)
print(resp.choices[0].message.content)

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
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": persona},
            {"role": "user", "content": "How quickly must an agency respond to a FOIA request?"},
        ],
    )
    print(f"\n--- persona: {persona[:40]}... ---")
    print(resp.choices[0].message.content)

# %% [markdown]
# ## Exercise 3 — Temperature
#
# `temperature` controls randomness. Low (0–0.3) = focused and repeatable; high
# (0.8–1.2) = varied and creative. Run this twice and compare.

# %%
for temp in [0.0, 1.0]:
    resp = client.chat.completions.create(
        model=MODEL,
        temperature=temp,
        messages=[{"role": "user",
                   "content": "Suggest a title for a one-page guide on using AI responsibly in government."}],
    )
    print(f"temperature={temp}: {resp.choices[0].message.content.strip()}")

# %% [markdown]
# ## Exercise 4 — Structured output (JSON) from a real document
#
# Programs need structured data, not prose. We ask the model to extract fields
# from the interim-guidance memo as JSON, and enforce it with
# `response_format={"type": "json_object"}`.

# %%
import json
memo = open("data/gov_memo.txt").read()

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
data = json.loads(resp.choices[0].message.content)
print(json.dumps(data, indent=2))
assert "subject" in data and "key_rules" in data, "expected keys present"

# %% [markdown]
# ## Exercise 5 — Token usage and cost
#
# Every response reports token usage. This is how you estimate what a workload
# costs before you scale it to an agency.

# %%
usage = resp.usage
print(f"prompt tokens:     {usage.prompt_tokens}")
print(f"completion tokens: {usage.completion_tokens}")
print(f"total tokens:      {usage.total_tokens}")

# Illustrative pricing — confirm current rates for your pinned model.
PRICE_IN_PER_1K, PRICE_OUT_PER_1K = 0.00015, 0.0006
cost = usage.prompt_tokens/1000*PRICE_IN_PER_1K + usage.completion_tokens/1000*PRICE_OUT_PER_1K
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
