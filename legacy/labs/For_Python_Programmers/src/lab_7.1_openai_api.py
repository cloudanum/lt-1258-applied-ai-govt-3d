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
MODEL = os.getenv("OPENAI_MODEL") or "gpt-5-mini"   # one place to change the model
# Exercise 3 only. Reasoning models (the gpt-5 family) accept just the default
# temperature and reject any other value, so the temperature exercise needs a
# model that actually has the knob.
TEMPERATURE_MODEL = os.getenv("OPENAI_TEMPERATURE_MODEL") or "gpt-4.1-mini"
print("key loaded:", "yes (value never shown)" if ONLINE else "no — OFFLINE mode, canned replies below")
print("Using model:", MODEL, f"(Exercise 3 uses {TEMPERATURE_MODEL})")

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
        "subject": "Interim Guidance on Generative AI for Constituent Services",
        "effective_date": "2026-03-14",
        "key_rules": [
            "Every AI-assisted work product must be reviewed by a responsible "
            "employee before release; the employee, not the tool, is accountable.",
            "Only public information may be entered into public AI tools; PII must "
            "never be entered into an unapproved tool, and exposure is reported "
            "within one business day.",
            "Tasks involving internal information must use the enterprise assistant "
            "on the approved-tools list maintained by the CIO.",
            "AI-assisted correspondence documenting agency business is a federal "
            "record and must be retained on the applicable schedule.",
            "Correspondence drafted with AI assistance must disclose that in a "
            "closing line, and the tool and reviewer are logged in the case system.",
        ],
    },
    "usage": {"prompt_tokens": 631, "completion_tokens": 174, "total_tokens": 805},
}

# %% [markdown]
# ## Steps
#
# 1. Run the setup cell — confirm it prints the model name.
#    ✓ *"Using model: …"* prints.
# 2. Complete **Exercise 2**: two calls with different system prompts, same
#    question. ✓ Two answers in different voices, same facts.
# 3. Complete **Exercise 3**: the same prompt at temperature 0.0 and 1.0.
#    ✓ You can see focused vs. varied output.
# 4. Complete **Exercise 4**: extract `subject`, `effective_date`, `key_rules`
#    from the memo as JSON with `response_format={"type":"json_object"}`.
#    ✓ `json.loads` succeeds and the keys are present.
# 5. Complete **Exercise 5**: print token usage and estimate the cost of 1,000
#    calls. ✓ You have a dollar estimate.
#
# Step 1 is already done: you ran the two Setup cells above and the output
# reported the key loaded **without printing it** (`key loaded: yes`) and the
# pinned model. If it says OFFLINE, tell your instructor — the lab still works,
# with canned replies.

# %% [markdown]
# ### Exercise 1 — Your first chat call (4 min)
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
# ### Exercise 2 — The system prompt changes the voice (5 min)
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
# ### Exercise 3 — Temperature (5 min)
#
# `temperature` controls variance. Low (0) = repeatable; high (1.0+) = varied.
# Send the **same** prompt once at `temperature=0.0` and once at
# `temperature=1.0`, and compare focused against varied output.
#
# Use `model=TEMPERATURE_MODEL` for these two calls, not `MODEL`: reasoning
# models reject every temperature except the default, so the call would fail
# with `unsupported_value`. Which knobs a model exposes is a property of the
# model, not of the API — worth remembering when you pick one.

# %%
prompt = [{"role": "user",
           "content": "Suggest a title for a one-page guide on using AI responsibly in government."}]

runs = None
# YOUR CODE: send `prompt` once with temperature=0.0 and once with
# temperature=1.0, passing model=TEMPERATURE_MODEL to both.
# Set runs = {"0.0": "<title>", "1.0": "<title>"}.
if runs is None:
    runs = {t: titles[0] for t, titles in CANNED["temperature"].items()}
    print("(canned runs applied — write your two calls above)\n")
for temp, title in runs.items():
    print(f"temperature={temp}: {title}")
print("\nRun the cell again. At 0.0 the title should barely move; at 1.0 it should.")

# %% [markdown]
# ### Exercise 4 — Structured output (JSON) from a real document (6 min)
#
# Programs need structured data, not prose. Load `data/gov_memo.txt` and extract
# **`subject`, `effective_date`, `key_rules`** as JSON, enforced with
# `response_format={"type": "json_object"}`.

# %%
memo = open("data/gov_memo.txt").read()

extraction = None
# YOUR CODE: call with response_format={"type": "json_object"} and a system
# message asking for JSON with exactly the keys subject (string),
# effective_date (string, YYYY-MM-DD) and key_rules (array of short strings).
# Parse with json.loads into `extraction`.
if extraction is None:
    extraction = CANNED["memo_json"]
    print("(canned extraction applied — write your call above)\n")
print(json.dumps(extraction, indent=2))

# ✓ json.loads succeeded and the keys are present:
assert isinstance(extraction, dict), "extraction should be a dict from json.loads"
for _k in ("subject", "effective_date", "key_rules"):
    assert _k in extraction, f"expected key {_k!r} in the extraction"
print(f"\n✓ all three keys present; key_rules has {len(extraction['key_rules'])} entries")

# %% [markdown]
# ### Exercise 5 — Token usage and cost (3 min)
#
# Every response carries a `usage` object: prompt, completion and total tokens.
# Capture it from your Exercise 4 call and multiply out to agency scale.

# %%
usage = None
# YOUR CODE: capture resp.usage from your Exercise 4 call as
# usage = {"prompt_tokens": ..., "completion_tokens": ..., "total_tokens": ...}
if usage is None:
    usage = CANNED["usage"]
    print("(illustrative usage applied — capture resp.usage from your own call above)\n")

PRICE_IN_PER_1K, PRICE_OUT_PER_1K = 0.00015, 0.0006   # illustrative — check current rates for your pinned model
per_call = (usage["prompt_tokens"] / 1000 * PRICE_IN_PER_1K
            + usage["completion_tokens"] / 1000 * PRICE_OUT_PER_1K)
print(f"prompt {usage['prompt_tokens']} + completion {usage['completion_tokens']} "
      f"= {usage['total_tokens']} tokens")
print(f"≈ ${per_call:.5f} per call  →  ${per_call * 1000:.2f} per 1,000 calls")

# %% [markdown]
# ## Stretch (not timed)
#
# The workbook page ends at Exercise 5. Everything below is optional — work it
# if you finish early or want to go further after class.

# %% [markdown]
# ### Stretch A — Tighten the prompt until it validates every time
#
# One successful parse proves nothing. The validator below checks keys *and*
# types. Re-run your extraction three times; if any run fails, tighten the
# prompt — name the keys, show an example, forbid extra text — until it is 3/3.

# %%
REQUIRED = {"subject": str, "effective_date": str, "key_rules": list}

def validate(obj):
    """Return a list of problems; an empty list means valid."""
    if not isinstance(obj, dict):
        return ["not a JSON object"]
    return [f"'{k}' missing or not a {t.__name__}" for k, t in REQUIRED.items()
            if not isinstance(obj.get(k), t)]

n_runs, passes = 3, 0
for i in range(n_runs):
    result = None
    # YOUR CODE: re-run your Exercise 4 extraction into `result` (paste your
    # call, with the tightened prompt).
    if result is None:
        result = CANNED["memo_json"]   # canned stands in so you can see the mechanics
    problems = validate(result)
    passes += not problems
    print(f"run {i + 1}: {'VALID' if not problems else 'INVALID: ' + '; '.join(problems)}")
print(f"\n{passes}/{n_runs} valid — keep tightening until it is {n_runs}/{n_runs}.")

# %% [markdown]

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
