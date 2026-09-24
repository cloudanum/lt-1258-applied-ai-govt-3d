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
# # Lab 7.1 — First Calls with the OpenAI API
#
# *Chapter 7 — Building with LLMs: APIs, RAG, and Agents · 30 minutes · JupyterLab + the OpenAI Python SDK*
#
# Everything the chat box did all course was an API call. Now you make the calls
# yourself: a first call, a system prompt that fixes the register, temperature,
# structured JSON out of a government memo, and the token math behind "what will
# this cost?".
#
# Cells marked `# YOUR CODE` are yours to write. Every cell runs as shipped —
# until you write yours, a labelled canned reply keeps the lab moving, and with
# no API key the whole notebook still runs (offline mode).

# %% [markdown]
# ## Objectives
#
# By the end of this lab, you will:
#
# - Make working chat calls from Python with the current SDK.
# - Control behaviour with system prompts and temperature.
# - Get structured JSON out of a real government memo and read the cost.

# %% [markdown]
# ## Setup
#
# - **Data:** `data/gov_memo.txt` — a *synthetic* training memo from the Office of
#   the Chief Data Officer. Course rule: public or synthetic data only — never
#   paste real constituent records into a prompt.
# - **Key:** `OPENAI_API_KEY` is injected on the classroom VM. The first cell
#   below loads it (falling back to the course `.env` file) and never prints it.
# - **Model:** pinned once via `OPENAI_MODEL` (default `gpt-5-mini`) — one line
#   to change when a model retires.

# %%
# API key: uses OPENAI_API_KEY from the environment (classroom VM); when run on
# the author's machine it falls back to the course .env file found by walking up
# from the notebook directory. The key is never printed.
import os, pathlib
def _load_api_key():
    if os.getenv("OPENAI_API_KEY") is not None:
        return  # environment wins — an explicitly empty value forces offline mode
    for p in [pathlib.Path.cwd(), *pathlib.Path.cwd().parents]:
        env = p / ".env"
        if env.is_file():
            for line in env.read_text().splitlines():
                k, _, v = line.partition("=")
                if k.strip() == "OPENAI_API_KEY" and v.strip():
                    os.environ["OPENAI_API_KEY"] = v.strip()
                    return
_load_api_key()
if not os.getenv("OPENAI_API_KEY"):
    print("OPENAI_API_KEY not set - ask your instructor, or the AI steps will be skipped/mocked.")

# %%
import json
from openai import OpenAI

ONLINE = bool(os.getenv("OPENAI_API_KEY"))
client = OpenAI() if ONLINE else None               # reads OPENAI_API_KEY from the environment
MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")     # one place to change the model
print("key loaded:", "yes (value never shown)" if ONLINE else "no — OFFLINE mode, canned replies below")
print("model:", MODEL)

# Canned replies from the instructor transcript — used only where labelled, so
# the lab never hard-fails on a keyless machine.
CANNED = {
    "first_call": (
        "The Freedom of Information Act (FOIA) is a federal law that gives any person "
        "the right to request records from U.S. executive-branch agencies. Agencies "
        "must generally respond within 20 business days, releasing records unless one "
        "of nine exemptions applies — for example personal privacy, law-enforcement "
        "sensitivity, or national security."),
    "personas": (
        "Under the Freedom of Information Act (5 U.S.C. § 552), an agency must determine "
        "whether to comply with a request within twenty (20) business days of receipt. "
        "In unusual circumstances the agency may extend this period by up to ten "
        "additional business days, provided it notifies the requester in writing.",
        "Think of it as a 20-working-day clock: once your FOIA request arrives, the "
        "agency has about four weeks of business days to get back to you. If things "
        "get complicated it can take a bit longer, but it has to tell you first."),
    "temperature": {
        "0.0": ["Responsible AI in Government: A One-Page Guide",
                "Responsible AI in Government: A One-Page Guide",
                "Responsible AI in Government: A One-Page Guide"],
        "1.0": ["AI With Guardrails: A Field Guide for Public Servants",
                "Your Agency, Your Algorithm: Responsible AI in One Page",
                "Trustworthy Bots, Transparent Government: A Starter Guide"],
    },
    "memo_json": {
        "title": "Interim Guidance on Generative AI for Constituent Services",
        "date": "2026-03-14",
        "decision": ("Interim rules for generative AI in constituent services: every "
                     "AI-assisted work product is human-reviewed before release, only "
                     "public information goes into public tools, internal work uses "
                     "approved enterprise tools, and AI-assisted correspondence is "
                     "kept as a federal record."),
        "owner": "Office of the Chief Data Officer",
    },
    "usage": {"prompt_tokens": 574, "completion_tokens": 88, "total_tokens": 662},
}

# %% [markdown]
# ## Steps
#
# ### Step 1 — Setup and key check (3 min)
#
# You just did it: run the two Setup cells above and confirm the output reports
# the key loaded **without printing it** (`key loaded: yes`). If it says OFFLINE,
# tell your instructor — the lab still works, with canned replies.

# %% [markdown]
# ### Step 2 — Your first call: user message only (4 min)
#
# A chat call takes a list of *messages*, each with a `role` (`system`, `user`,
# `assistant`) and `content`. This one has a user message only — the pattern for
# everything else in the lab. Run it and print the reply.

# %%
messages = [{"role": "user",
             "content": "In two sentences, what is the Freedom of Information Act?"}]

if client is not None:
    try:
        resp = client.chat.completions.create(model=MODEL, messages=messages)
        print(resp.choices[0].message.content)
    except Exception as e:
        print(f"({type(e).__name__} — the call failed; canned reply from the transcript:)\n")
        print(CANNED["first_call"])
else:
    print("(offline) canned reply from the instructor transcript:\n")
    print(CANNED["first_call"])

# %% [markdown]
# ### Step 3 — Add a system message that fixes the register (5 min)
#
# Same question, two different `system` messages. The system message sets the
# register the user message cannot. Ask *"How quickly must an agency respond to
# a FOIA request?"* twice and compare.

# %%
question = "How quickly must an agency respond to a FOIA request?"
system_formal = ("You are a policy analyst. Answer formally, citing the "
                 "20-business-day response rule.")
system_plain = ("You are explaining to a brand-new employee. Answer in plain, "
                "friendly language.")

replies = None
# YOUR CODE: two calls — same `question`, once with system_formal and once with
# system_plain as the system message. Set replies = (formal_text, plain_text),
# modelled on Step 2.
if replies is None:
    replies = CANNED["personas"]
    print("(canned replies applied — write your two calls above)\n")
print("FORMAL REGISTER:\n", replies[0])
print("\nPLAIN-LANGUAGE REGISTER:\n", replies[1])

# %% [markdown]
# ### Step 4 — Temperature: three runs at 0, three at 1.0 (5 min)
#
# `temperature` controls variance. Low (0) = repeatable; high (1.0+) = varied.
# Run the **same** prompt three times at `temperature=0.0`, then three times at
# `temperature=1.0`, and compare.

# %%
prompt = [{"role": "user",
           "content": "Suggest a title for a one-page guide on using AI responsibly in government."}]

runs = None
# YOUR CODE: send `prompt` three times with temperature=0.0 and three times with
# temperature=1.0. Set runs = {"0.0": [three strings], "1.0": [three strings]}.
if runs is None:
    runs = CANNED["temperature"]
    print("(canned runs applied — write your loop above)\n")
for temp, titles in runs.items():
    print(f"temperature={temp}:")
    for t in titles:
        print("  -", t)
    print("  all three identical?", len(set(titles)) == 1, "\n")

# %% [markdown]
# ### Step 5 — Structured JSON out of a real memo (6 min)
#
# Programs need structured data, not prose. Load `data/gov_memo.txt` and extract
# **`title`, `date`, `decision`, `owner`** as JSON, enforced with
# `response_format={"type": "json_object"}`.

# %%
memo = open("data/gov_memo.txt").read()

extraction = None
# YOUR CODE: call with response_format={"type": "json_object"} and a system
# message asking for JSON with exactly the keys title, date, decision, owner
# (all strings; date as YYYY-MM-DD). Parse with json.loads into `extraction`.
if extraction is None:
    extraction = CANNED["memo_json"]
    print("(canned extraction applied — write your call above)\n")
print(json.dumps(extraction, indent=2))

# %% [markdown]
# ### Step 6 — Tighten the prompt until it validates every time (4 min)
#
# One successful parse proves nothing. The validator below checks keys *and*
# types. Re-run your extraction three times; if any run fails, tighten the
# prompt — name the keys, show an example, forbid extra text — until it is 3/3.

# %%
REQUIRED = {"title": str, "date": str, "decision": str, "owner": str}

def validate(obj):
    """Return a list of problems; an empty list means valid."""
    if not isinstance(obj, dict):
        return ["not a JSON object"]
    return [f"'{k}' missing or not a {t.__name__}" for k, t in REQUIRED.items()
            if not isinstance(obj.get(k), t)]

n_runs, passes = 3, 0
for i in range(n_runs):
    result = None
    # YOUR CODE: re-run your Step 5 extraction into `result` (paste your call,
    # with the tightened prompt).
    if result is None:
        result = CANNED["memo_json"]   # canned stands in so you can see the mechanics
    problems = validate(result)
    passes += not problems
    print(f"run {i + 1}: {'VALID' if not problems else 'INVALID: ' + '; '.join(problems)}")
print(f"\n{passes}/{n_runs} valid — keep tightening until it is {n_runs}/{n_runs}.")

# %% [markdown]
# ### Step 7 — Tokens and the cost of 1,000 memos (3 min)
#
# Every response carries a `usage` object: prompt, completion and total tokens.
# Capture it from your Step 5 call and multiply out to agency scale.

# %%
usage = None
# YOUR CODE: capture resp.usage from your Step 5/6 call as
# usage = {"prompt_tokens": ..., "completion_tokens": ..., "total_tokens": ...}
if usage is None:
    usage = CANNED["usage"]
    print("(illustrative usage applied — capture resp.usage from your own call above)\n")

PRICE_IN_PER_1K, PRICE_OUT_PER_1K = 0.00015, 0.0006   # illustrative — check current rates for your pinned model
per_call = (usage["prompt_tokens"] / 1000 * PRICE_IN_PER_1K
            + usage["completion_tokens"] / 1000 * PRICE_OUT_PER_1K)
print(f"prompt {usage['prompt_tokens']} + completion {usage['completion_tokens']} "
      f"= {usage['total_tokens']} tokens")
print(f"≈ ${per_call:.5f} per memo  →  ${per_call * 1000:.2f} per 1,000 memos")

# %% [markdown]
# ## Deliverable
#
# 1. The validated `{title, date, decision, owner}` JSON extracted from
#    `gov_memo.txt` (3/3 validation runs).
# 2. Your token counts and the estimated cost per 1,000 memos.

# %% [markdown]
# ## Reflection
#
# 1. What did the system message change that the user message could not?
# 2. Where would temperature 0 still not give you identical output?
# 3. What is the first thing you would log if this ran in production?

# %% [markdown]
# ## Debrief (instructor-led)
#
# 1. Which changed the output more — the system prompt or the temperature? Why?
# 2. Why is JSON output (Step 5) more useful in a real system than prose?
# 3. Your agency wants to summarize 50,000 documents a month. Using Step 7,
#    roughly what would that cost — and what changes if you run it on Azure
#    OpenAI (FedRAMP) instead?

# %% [markdown]
# ## Troubleshooting
#
# - **`OpenAIError: The api_key client option must be set`** — the key is not in
#   the environment. Re-run both Setup cells; on the VM, ask your instructor.
#   (OFFLINE mode with canned replies is the intended fallback, not a bug.)
# - **`json.JSONDecodeError` in Step 5/6** — the model wrapped the JSON in prose.
#   Keep `response_format={"type": "json_object"}` and say "reply ONLY with JSON".
# - **Validation keeps failing on `date`** — ask for the format explicitly:
#   "date as an ISO YYYY-MM-DD string".
# - **`RateLimitError`** — the shared classroom key is busy; wait 20 seconds and
#   re-run the cell.
# - **`NotFoundError` naming the model** — `OPENAI_MODEL` points at a retired
#   model; delete the override and use the default in Setup.
# - **Three identical titles at temperature 1.0** — coincidence is possible but
#   suspicious; check you passed `temperature` to the call, not the messages.
