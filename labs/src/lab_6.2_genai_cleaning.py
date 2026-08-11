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
# # Lab 6.2 — GenAI-Assisted Cleaning with Structured Outputs
#
# *Chapter 6 — Data for AI: Collection, Quality, and Governance · 35 minutes
# · JupyterLab with pandas and the OpenAI API via the course helpers (canned
# offline fallback)*
#
# Lab 6.1 found the defects. Now fix a class of them with GenAI — and then
# check the fixer, because schema-correct is not the same as correct.
#
# Cells marked `# YOUR TURN` ask you to edit the prompt text (or a count) and
# re-run. Offline, a realistic canned mapping stands in for the model so every
# step still runs.

# %% [markdown]
# ## Objectives
#
# By the end of this lab, you will:
#
# - Use a model to normalise messy categorical data at volume.
# - Enforce a schema so the output is machine-usable.
# - Audit the model's work and measure what it got wrong.

# %% [markdown]
# ## Setup
#
# **Datasets and files** (all under `labs/data/`):
#
# - `chicago_311.csv` — the same 4,000-request extract you assessed in
#   Lab 6.1 (real, public; see `data/MANIFEST.json`). Target column:
#   `sr_type`, 68 free-typed request labels.
#
# **Tools:** pandas, plus the OpenAI chat API in JSON mode through the course
# helpers. Offline, a keyword-rule canned mapping stands in for the model so
# every step still runs.
#
# **Data rule:** the extract is genuinely public data. The values sent to
#   the model are service-request labels only — never send resident-level
#   fields (addresses, names) to an external API.
#
# **How this notebook works:** every step is one provided cell — run it with
# Shift+Enter and read what it prints. Cells marked `# YOUR TURN` ask you to
# edit the prompt text (ordinary quoted text — no code) or a count, and
# re-run the cell. Everything runs as shipped, so you can never get stuck.

# %%
# ▶ Setup — run this cell first (click it, then Shift+Enter).
# It loads the course helper functions used by every step below.
from lab_helpers import *
lab_status()

# %% [markdown]
# ## Steps
#
# 1. Run the Setup cell. (1 min)
# 2. Extract 60 raw values from a messy categorical column. (4 min)
# 3. Call the model with a **strict JSON schema**:
#    `{raw, canonical, confidence}`. (6 min)
# 4. Parse the response; fail loudly if it does not validate. (5 min)
# 5. Sample 20 mappings and check them by hand. Record the error rate.
#    (7 min)
# 6. Find one high-confidence wrong mapping and explain what misled it.
#    (5 min)
# 7. Re-run the failures with a tightened prompt and compare. (5 min)
# 8. State the human-review rate you would require in production. (3 min)

# %% [markdown]
# ### Step 2 — Extract 60 raw values (4 min, provided)
#
# The target: `sr_type` in the 311 extract — 68 free-typed request labels.
# The goal: map each to a **controlled vocabulary** of service categories a
# dashboard can group by.

# %%
raw_values = extract_messy_labels()

# %% [markdown]
# ### Step 3 — Call the model with a strict JSON schema (6 min)
#
# Ask for one object per raw value: `{raw, canonical, confidence}` —
# `canonical` restricted to the controlled vocabulary, `confidence` 0–1.
# JSON mode makes the answer machine-usable; the schema makes it *checkable*.
#
# The prompt below is a working version — it (a) gives the controlled
# vocabulary, (b) demands JSON `{"mappings": [{raw, canonical, confidence},
# ...]}` with one object per input value, and (c) tells the model to use
# "Other" with low confidence rather than force a fit. **Edit the text** and
# re-run to see the mapping change.

# %%
MAPPING_PROMPT = """You are normalizing Chicago 311 request-type labels into a controlled vocabulary for a city dashboard.
VOCABULARY: Noise, Information & 311 Services, Water & Drainage, Urban Forestry, Graffiti & Property Damage, Streets & Transportation, Sanitation & Waste, Pest & Animal Control, Buildings & Housing, Code Enforcement & Violations, Other.
Return JSON only: {"mappings": [{"raw": ..., "canonical": ..., "confidence": 0-1}, ...]} with exactly one object per input value. If no category fits well, use "Other" with confidence <= 0.5 rather than forcing a fit."""   # ← YOUR TURN: edit the mapping prompt, then re-run this cell

mapped = clean_labels_with_ai(raw_values, MAPPING_PROMPT)

# %% [markdown]
# ### Step 4 — Fail loudly if it does not validate (5 min, provided)
#
# A schema you never check is a hope, not a contract. This cell validates
# every item and stops at the first violation — then corrupts one entry on
# purpose to prove the check bites.

# %%
validate_cleaning(mapped)

# %% [markdown]
# ### Step 5 — Audit: sample 20 and check by hand (7 min)
#
# The model's schema passed; now grade its *judgement*. Run the first cell to
# draw 20 sampled mappings, read each one, decide how many are wrong, put
# your count in the second cell, and re-run it.

# %%
audit_sample = show_cleaning_sample(mapped)

# %%
ERRORS_FOUND = 1   # ← YOUR TURN: read the 20 rows above, then replace 1 with YOUR count of wrong mappings and re-run this cell
show_error_rate(ERRORS_FOUND)

# %% [markdown]
# #### Which were wrong, and why (write here)
#
# -
# -

# %% [markdown]
# ### Step 6 — The high-confidence wrong mapping (5 min, provided)
#
# This cell filters to confidence ≥ 0.85 — find one mapping that is
# *confidently* wrong. What in the label text misled the model?

# %%
show_confident_mappings(mapped)

# %% [markdown]
# #### Your pick and explanation (write here)
#
# *Mapping, what it should be, and what in the text misled the model:*
#
# -

# %% [markdown]
# ### Step 7 — Tighten the prompt, re-run the failures (5 min)
#
# One sentence of domain knowledge in the prompt fixes a whole error class.
# The cell below carries a working tightening sentence — edit it (or write
# your own), then re-run: only the failures go back to the model, with your
# prompt plus the tightening sentence. Compare the new mappings with what
# Step 5 showed.

# %%
TIGHTENER = """
IMPORTANT: distinguish service delivery from enforcement — labels containing 'Violation' are code-enforcement actions (Code Enforcement & Violations), not service requests, even when the enforcing department sounds like a service (e.g. Sanitation)."""   # ← YOUR TURN: edit the tightening sentence, then re-run this cell

rerun_with_tighter_prompt(mapped, MAPPING_PROMPT, TIGHTENER)

# %% [markdown]
# ### Step 8 — State the human-review rate (3 min)
#
# Given your measured error rate, what share of mappings would you route to a
# human in production — all, a sample, or only low-confidence ones? Write it
# as an operational rule with a number.
#
# #### Your rule (write here)
#
# -

# %% [markdown]
# ## Deliverable
# 1. The mapping table with validation passing (and the deliberate failure).
# 2. Your audited error rate and the high-confidence wrong mapping explained.
# 3. The tightened-prompt re-run.
# 4. Your human-review rule.

# %% [markdown]
# ## Reflection
# 1. What error rate would you accept, and who decides?
# 2. Did confidence correlate with correctness?
# 3. Which defects from Lab 6.1 can GenAI *not* fix?

# %% [markdown]
# ## Debrief (instructor-led)
#
# - **Compare error rates.** What did different auditors count as "wrong"?
#   Did the disagreement itself reveal an ambiguity in the controlled
#   vocabulary?
# - **Confidence as a routing signal.** Would routing only low-confidence
#   mappings to humans have caught your high-confidence wrong one?
# - **Cost of the loop.** Each tightened prompt is a re-run and a re-audit.
#   At what fleet size does that stop being worth it versus a lookup table
#   curated by hand?

# %% [markdown]
# ## Troubleshooting
#
# - **`ModuleNotFoundError: lab_helpers`** — the kernel's working directory is
#   not `labs/`. Restart the kernel from the `labs/` folder and Run All.
# - **The mapping step prints "(offline canned mapping ...)"** — no API key is
#   visible on this machine; keyword rules stand in for the model. The lab is
#   fully usable either way.
# - **The model's answer is not usable JSON (live run)** — your prompt asked
#   for prose around the JSON. Demand "JSON only" and re-run the cell.
# - **The validator rejects a mapping** — if it comes from the corruption
#   demo in Step 4, the validator is working (read the printed message). If
#   it comes from your own prompt's output, the model broke the schema
#   contract: fail loudly is the correct behavior, not a bug.
# - **Your error rate looks like a guess** — it is, until you read the 20
#   sampled rows. The audit only counts if *you* set `ERRORS_FOUND` yourself.

# %% [markdown]
# ---
# *Curious about the Python behind these steps? The full code-forward version
# of this lab lives in the `For_Python_Programmers/` folder.*
