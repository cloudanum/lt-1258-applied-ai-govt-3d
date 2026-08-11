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
# Cells marked `# YOUR TURN` ask you to edit ordinary text (a question, an
# instruction, a persona) and re-run the cell. Every cell runs as shipped, and
# with no API key the whole notebook still runs — a labelled canned reply from
# the instructor transcript keeps the lab moving (offline mode).

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
# - **Key:** `OPENAI_API_KEY` is injected on the classroom VM. The setup cell
#   below loads it (falling back to the course `.env` file) and never prints it.
# - **Model:** pinned once via `OPENAI_MODEL` (default `gpt-5-mini`) — one line
#   to change when a model retires.
# - **How this notebook works:** every step is one provided cell — run it with
#   Shift+Enter and read what it prints. Cells marked `# YOUR TURN` ask you to
#   edit the text (ordinary quoted text — no code) and re-run the cell.
#   Everything runs as shipped, so you can never get stuck.

# %%
# ▶ Setup — run this cell first (click it, then Shift+Enter).
# It loads the course helper functions used by every step below.
from lab_helpers import *
lab_status()

# %% [markdown]
# ## Steps
#
# 1. Run the setup cell — confirm it prints the model name.
#    ✓ *"chat model alias: …"* prints.
# 2. **Exercise 2**: the same question with two different system prompts.
#    ✓ Two answers in different voices, same facts.
# 3. **Exercise 3**: the same prompt at temperature 0.0 and 1.0.
#    ✓ You can see focused vs. varied output.
# 4. **Exercise 4**: extract `subject`, `effective_date`, `key_rules`
#    from the memo as JSON. ✓ The extraction prints and the keys are present.
# 5. **Exercise 5**: read the token usage and estimate the cost of 1,000
#    calls. ✓ You have a dollar estimate.
#
# Step 1 is already done if the Setup cell above reported the key loaded
# **without printing it** (`API key configured: yes`) and the pinned model. If
# it says OFFLINE, tell your instructor — the lab still works, with canned
# replies.

# %% [markdown]
# ### Exercise 1 — Your first chat call (4 min)
#
# A chat call takes a *question* and returns a *reply*. (Under the hood it is a
# list of *messages*, each with a `role` — `system`, `user`, `assistant` — and
# `content`; this one has a user message only, the pattern for everything else
# in the lab.) Run the cell and read the reply.

# %%
QUESTION = "In two sentences, what is the Freedom of Information Act?"   # ← YOUR TURN: edit the question, then re-run this cell

first_foia_call(QUESTION)

# %% [markdown]
# ### Exercise 2 — The system prompt changes the voice (5 min)
#
# Same question, two different *system* messages. The system message sets the
# register the user message cannot. The cell asks *"How quickly must an agency
# respond to a FOIA request?"* twice — once under each persona — so you can
# compare. Edit the persona text and re-run.

# %%
FOIA_QUESTION = "How quickly must an agency respond to a FOIA request?"

FORMAL_PERSONA = "You are a policy analyst. Answer formally, citing the 20-business-day response rule."   # ← YOUR TURN: edit the formal persona, then re-run this cell

PLAIN_PERSONA = "You are explaining to a brand-new employee. Answer in plain, friendly language."   # ← YOUR TURN: edit the plain-language persona too

compare_foia_voices(FOIA_QUESTION, FORMAL_PERSONA, PLAIN_PERSONA)

# %% [markdown]
# ### Exercise 3 — Temperature (5 min)
#
# `temperature` controls variance. Low (0) = repeatable; high (1.0+) = varied.
# The cell sends the **same** prompt once at `temperature=0.0` and once at
# `temperature=1.0`, so you can compare focused against varied output.
#
# This one exercise uses a different, temperature-capable model: reasoning
# models (the gpt-5 family the rest of the lab uses) reject every temperature
# except the default, so the call would fail. Which knobs a model exposes is a
# property of the model, not of the API — worth remembering when you pick one.

# %%
TITLE_PROMPT = "Suggest a title for a one-page guide on using AI responsibly in government."   # ← YOUR TURN: edit the prompt, then re-run this cell

try_temperature_titles(TITLE_PROMPT)

# %% [markdown]
# ### Exercise 4 — Structured output (JSON) from a real document (6 min)
#
# Programs need structured data, not prose. The cell loads `data/gov_memo.txt`
# and extracts **`subject`, `effective_date`, `key_rules`** as JSON — the JSON
# format is enforced, so a program can rely on it. Your job is the instruction
# text: name the keys and their shapes. Edit it and re-run.

# %%
EXTRACTION_INSTRUCTIONS = """Extract fields from the memo. Reply ONLY with JSON having exactly these keys: subject (string), effective_date (string, YYYY-MM-DD), key_rules (array of short strings)."""   # ← YOUR TURN: edit the extraction instructions, then re-run this cell

extraction = extract_memo_json_71(EXTRACTION_INSTRUCTIONS)

# %% [markdown]
# ### Exercise 5 — Token usage and cost (3 min)
#
# Every response carries a token count: prompt, completion and total tokens.
# The cell re-runs the Exercise 4 extraction, keeps the counts, and multiplies
# out to agency scale. Run it and read the dollar estimate.

# %%
show_token_cost()

# %% [markdown]
# ## Stretch (not timed)
#
# The workbook page ends at Exercise 5. Everything below is optional — work it
# if you finish early or want to go further after class.

# %% [markdown]
# ### Stretch A — Tighten the prompt until it validates every time
#
# One successful parse proves nothing. The cell re-runs your Exercise 4
# extraction three times and validates keys *and* types each time. If any run
# fails, tighten `EXTRACTION_INSTRUCTIONS` above — name the keys, show an
# example, forbid extra text — until it is 3/3.

# %%
validate_extraction_runs(EXTRACTION_INSTRUCTIONS)

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
# - **The Setup cell prints `API key configured: no — OFFLINE mode`.** The key
#   is not in the environment. Re-run the Setup cell; on the VM, ask your
#   instructor. (OFFLINE mode with canned replies is the intended fallback, not
#   a bug.)
# - **The Exercise 4 reply is prose, not JSON, on a live run** — the model
#   wrapped the JSON in prose. Keep the JSON-only enforcement (the helper
#   applies it) and say "reply ONLY with JSON" in your instructions.
# - **Validation keeps failing on `effective_date`** — ask for the format
#   explicitly: "date as an ISO YYYY-MM-DD string".
# - **A rate-limit error on a live run** — the shared classroom key is busy;
#   wait 20 seconds and re-run the cell.
# - **A not-found error naming the model on a live run** — `OPENAI_MODEL`
#   points at a retired model; delete the override and use the default.
# - **Three identical titles at temperature 1.0 on a live run** — coincidence
#   is possible but suspicious; tell your instructor.

# %% [markdown]
# ---
# *Curious about the Python behind these steps? The full code-forward version
# of this lab lives in the `For_Python_Programmers/` folder.*
