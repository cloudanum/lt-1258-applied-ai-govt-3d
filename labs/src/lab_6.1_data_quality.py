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
# # Lab 6.1 — Data Quality Assessment of Chicago 311
#
# *Chapter 6 — Data for AI: Collection, Quality, and Governance · 45 minutes
# · JupyterLab with pandas — no API key needed*
#
# A programme office wants to use 311 data to target service improvements.
# You have been asked whether the data supports that. Answer with numbers.
#
# Cells marked `# YOUR TURN` ask you to change a simple value and re-run.
# No API key is needed.

# %% [markdown]
# ## Objectives
#
# By the end of this lab, you will:
#
# - Assess a real dataset against all six quality dimensions.
# - Quantify each defect rather than describing it.
# - Produce a go / no-go recommendation with evidence.

# %% [markdown]
# ## Setup
#
# **Datasets and files** (all under `labs/data/`):
#
# - `chicago_311.csv` — 4,000 recent City of Chicago 311 service requests
#   (real, public; Socrata extract documented in `data/MANIFEST.json`).
#   Genuinely messy operational data: blank fields, inconsistent casing and
#   duplicate rows are present **on purpose** — they are the subject of the
#   lab.
#
# **Tools:** pandas only. No OpenAI key is required for any step.
#
# **Data rule:** this is genuinely public data, downloaded for offline
# classroom use. Treat it with the same care you would any operational
# extract: address fields in it belong to real residents.
#
# **How this notebook works:** every step is one provided cell — run it with
# Shift+Enter and read what it prints. Cells marked `# YOUR TURN` ask you to
# change a simple value (like the blank-rate limit that flags a column) and
# re-run the cell. Everything runs as shipped, so you can never get stuck.

# %%
# ▶ Setup — run this cell first (click it, then Shift+Enter).
# It loads the course helper functions used by every step below.
from lab_helpers import *

# %% [markdown]
# ## Steps
#
# 1. Load the file. (3 min)
# 2. **Completeness:** null rate per column; flag anything above 20%. (6 min)
# 3. **Uniqueness:** duplicate `sr_number` count; inspect a duplicate pair.
#    (6 min)
# 4. **Consistency:** case and whitespace variants in categorical columns.
#    (6 min)
# 5. **Validity:** dates outside a plausible range; closed-before-created
#    rows. (6 min)
# 6. **Timeliness:** distribution of `created_date`; how current is it?
#    (5 min)
# 7. **Accuracy:** pick one column and say honestly how you would even test
#    it. (5 min)
# 8. Build a one-table scorecard: dimension, metric, value, pass/fail.
#    (5 min)
# 9. Write a go / no-go recommendation with the two numbers that drive it.
#    (3 min)

# %% [markdown]
# ### Step 1 — Load (3 min, provided)
#
# `data/chicago_311.csv` is a genuine operational extract — 4,000 recent
# service requests, warts included on purpose. Run this cell to load it.

# %%
df = load_311_data()

# %% [markdown]
# ### Step 2 — Completeness (6 min)
#
# Run this cell for the blank rate per column; it flags anything above 20%.
# Watch for columns that are blank for a *reason* (a `closed_date` on an open
# request is not a defect — the cell checks that too). Then try a stricter or
# looser limit.

# %%
NULL_LIMIT = 20   # ← YOUR TURN: the % of blanks that flags a column — try 10 or 50 and re-run this cell
completeness = completeness_report(df, NULL_LIMIT)

# %% [markdown]
# ### Step 3 — Uniqueness (6 min, provided)
#
# Run this cell for the duplicate `sr_number` count and a duplicate pair to
# inspect. Then look at the city's own `duplicate` flag — do the two stories
# agree?

# %%
uniqueness = uniqueness_report(df)

# %% [markdown]
# ### Step 4 — Consistency (6 min, provided)
#
# Run this cell for the case and whitespace variants in the categorical
# columns — `city`, `state` — and the way `zip_code` is stored: a ZIP is an
# identifier, not a quantity.

# %%
consistency_report(df)

# %% [markdown]
# ### Step 5 — Validity (6 min, provided)
#
# Run this cell for dates outside a plausible range and requests closed
# before they were created. A zero here is a *pass* — record it as one, with
# the check that proved it.

# %%
validity = validity_report(df)

# %% [markdown]
# ### Step 6 — Timeliness (5 min, provided)
#
# Run this cell for the `created_date` coverage: how current is the extract,
# and how wide is its window? Currency and coverage are different claims —
# assess both.

# %%
timeliness = timeliness_report(df)

# %% [markdown]
# ### Step 7 — Accuracy (5 min)
#
# Pick one column and say honestly how you would *even test* its accuracy.
# This is the dimension the data cannot grade itself on — write your answer
# in the markdown cell below.
#
# #### Your answer (write here)
#
# *Column chosen, and the test you would run (against what ground truth,
# obtained how, at what cost):*
#
# -

# %% [markdown]
# ### Step 8 — The scorecard (5 min, provided)
#
# Run this cell for the one-table scorecard: dimension, metric, value,
# pass/fail, filled from the numbers above. The thresholds baked in are a
# defensible starting point — if you defend different ones, say so in your
# recommendation.

# %%
scorecard = quality_scorecard(df, completeness, uniqueness, validity, timeliness)

# %% [markdown]
# ### Step 9 — Go / no-go recommendation (3 min, write here)
#
# *One paragraph: can the programme office use this file to target service
# improvements? Name the two numbers that drive your answer.*
#
# -

# %% [markdown]
# ## Deliverable
# 1. The six dimension measurements.
# 2. The scorecard table.
# 3. Your go / no-go recommendation with its two driving numbers.

# %% [markdown]
# ## Reflection
# 1. Which dimension could you *not* assess from the data alone?
# 2. What is the single cheapest fix at the point of collection?
# 3. Would you sign the recommendation you just wrote?

# %% [markdown]
# ## Debrief (instructor-led)
#
# - **Compare verdicts.** Who said go, who said no-go? Put the two driving
#   numbers side by side — did the same number drive opposite verdicts?
# - **Thresholds are policy.** The 20% null threshold: who set it, and is it
#   the right one for targeting service improvements?
# - **Bridge to Lab 6.2.** Which defect class from your scorecard is the
#   best candidate for GenAI-assisted cleaning — and which is not?

# %% [markdown]
# ## Troubleshooting
#
# - **A red error mentioning `chicago_311.csv` or "No such file".** The
#   course data pack is missing or incomplete — tell your instructor; run the
#   Day-0 healthcheck to confirm.
# - **A warning about mixed column types on load.** Expected on this file
#   (mixed types in operational columns) — the provided load already handles
#   it.
# - **A dimension shows zero defects.** That is a pass, not a bug. Record it
#   in the scorecard with the check that proved it (Step 5 shows how).
# - **`zip_code` prints with a decimal point (60618.0).** That *is* the
#   consistency defect Step 4 asks you to find, not a display error.
# - **Your numbers differ from a neighbour's.** They should not — every
#   number is computed from the same file. Re-run the notebook in order
#   (Kernel → Restart & Run All).

# %% [markdown]
# ---
# *Curious about the Python behind these steps? The full code-forward version
# of this lab lives in the `For_Python_Programmers/` folder.*
