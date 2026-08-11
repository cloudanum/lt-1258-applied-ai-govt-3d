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
# # Lab 2.1 — Public Data Expedition: Profile an Agency Dataset
#
# *Course 1258 — Applied AI for Government IT Professionals · Ch02 AI
# Applications Across Government and Public Data · 30 minutes · CloudShare VM
# (JupyterLab) · pandas — no API key needed (data.gov search has a cached
# fallback)*
#
# A programme office hands you a dataset and asks "can we use this?". That
# question is answered by profiling, not by opinion. You will do it three
# times, quickly, on three real datasets.

# %% [markdown]
# ## Objectives
#
# By the end of this lab, you will:
#
# - Profile an unfamiliar public dataset from scratch.
# - Read metadata critically and state what the data cannot answer.
# - Produce a one-paragraph dataset briefing another analyst could use.

# %% [markdown]
# ## Setup
#
# - **Datasets:** `data/cdc_flu_wastewater.csv`, `data/nyc_air_quality.csv`,
#   `data/chicago_311.csv` — all public US government data, downloaded ahead
#   of class (provenance in `data/MANIFEST.json`).
# - **No API key is needed.** The data.gov search in Step 1 tries the live
#   catalogue and falls back to a cached snapshot, so it works offline.
# - **The one rule that never changes:** public or synthetic data only. Never
#   paste real agency, personal or sensitive data into any assistant.
# - **How this notebook works:** every step is one provided cell — run it with
#   Shift+Enter and read what it prints. Cells marked `# YOUR TURN` ask you to
#   change a simple value and re-run the cell. Everything runs as shipped, so
#   you can never get stuck.

# %%
# ▶ Setup — run this cell first (click it, then Shift+Enter).
# It loads the course helper functions used by every step below.
from lab_helpers import *

# %% [markdown]
# ## Steps
#
# 1. **(4 min)** Run the warm-up: how you would *find* a dataset like these
#    before profiling it.
# 2. **(4 min)** For **each** of the three datasets: load it and print shape,
#    columns, column types.
# 3. **(6 min)** Report per column: blank count, distinct count, and an
#    example value.
# 4. **(4 min)** Identify the grain — what does one row actually represent?
# 5. **(4 min)** Identify the time column and print the date range.
# 6. **(4 min)** Name one question the dataset answers well and one it cannot
#    answer.
# 7. **(4 min)** Write a four-sentence briefing for the CDC wastewater file,
#    including its grain, coverage, and one caveat.

# %% [markdown]
# ### Step 1 — Warm-up: finding the data in the first place
#
# data.gov retired its JSON API, so this search tries the live catalogue and
# falls back to a cached snapshot. Either way, this is how you would *find* a
# dataset like the three below before profiling it. Watch which source it
# reports. Then change `KEYWORD` to a topic your agency cares about and
# re-run.

# %%
KEYWORD = "air quality"   # ← YOUR TURN: search for any topic, then re-run this cell
search_gov_datasets(KEYWORD)

# %% [markdown]
# ### Step 2 — Load all three datasets (provided)
#
# Run this cell to load each CSV and print its shape, columns, and column
# types. Just the first look — the detailed per-column profile is Step 3.

# %%
frames = load_expedition_datasets()

# %% [markdown]
# ### Step 3 — A profile of each dataset (provided)
#
# Run this cell. For each of the three datasets it prints one row per column:
# the column's type, how many values are blank, how many are distinct, and
# one example value. This table is the reusable first look at any unfamiliar
# dataset — read it the same way all three times.

# %%
profile_datasets(frames)

# %% [markdown]
# ### Step 4 — The grain: what is one row?
#
# For each dataset, state the grain in one sentence — what does a single row
# actually represent? (Hint: they are three different kinds of thing. Look at
# the CDC `sample_id` / `site` columns, the NYC `geo_place_name` /
# `time_period` pair, and the 311 `sr_number`.)
#
# **Your answers (write here):**
#
# - cdc_flu_wastewater:
# - nyc_air_quality:
# - chicago_311:

# %% [markdown]
# ### Step 5 — The time dimension (provided)
#
# Every dataset here has a time column (or something playing that role). Run
# this cell — it finds each one and prints the range it covers. (NYC's is not
# a full date — compare the range with the `time_period` values it prints and
# decide which is honest.)

# %%
show_time_ranges(frames)

# %% [markdown]
# ### Step 6 — What each dataset can and cannot answer
#
# For each dataset, name one question it answers well and one it *cannot*
# answer. Write them below — then check your "cannot" claims against the
# column list. The discipline is the point.
#
# **Your answers (write here):**
#
# - cdc_flu_wastewater — answers well: / cannot answer:
# - nyc_air_quality — answers well: / cannot answer:
# - chicago_311 — answers well: / cannot answer:

# %% [markdown]
# ### Step 7 — Four-sentence briefing: CDC wastewater
#
# Write a four-sentence briefing on `cdc_flu_wastewater.csv` that another
# analyst could act on. It must include: the **grain**, the **coverage**
# (sites, states, dates), one **strength**, and one **caveat**.
#
# **Your briefing (write here):**
#
# *
# *
# *
# *

# %% [markdown]
# ## Deliverable
#
# 1. The profiler output for all three datasets.
# 2. Grain, time range, and can/cannot-answer pairs for each.
# 3. Your four-sentence CDC briefing.

# %% [markdown]
# ## Reflection
#
# 1. Which dataset was hardest to establish a grain for?
# 2. What would you ask the data owner before using any of these in a decision?
# 3. The Ch02 slides describe wastewater surveillance as an early-warning
#    system. Does this file support that claim on its own?

# %% [markdown]
# ## Debrief (instructor-led)
#
# - Start with the time ranges: who noticed the Chicago 311 extract covers
#   about a day? Ask what that does to any trend claim built on it.
# - Take the NYC grain apart together — it is a long/tidy table ("which
#   pollutant" and "which period" are data, not columns), the one most rooms
#   misread as "one row per neighbourhood".
# - Hear two or three CDC briefings aloud. Score them against the checklist:
#   grain, coverage, one strength, one caveat — and did anyone promise case
#   counts the file cannot deliver?

# %% [markdown]
# ## Troubleshooting
#
# - **Step 1 prints `source: cached`.** Expected — data.gov's API is gone and
#   the classroom network may be filtered. The snapshot is the lesson.
# - **A warning about mixed column types.** Real government CSVs do this; the
#   provided load already handles it by reading each file in one pass.
# - **A date range looks wrong or a date column shows blanks.** Some rows have
#   unparseable or blank dates — the time-range step skips them honestly;
#   note how many rows that costs before quoting a range.
# - **Out-of-order errors after experimenting.** Kernel → Restart & Run All.

# %% [markdown]
# ---
# *Curious about the Python behind these steps? The full code-forward version
# of this lab lives in the `For_Python_Programmers/` folder.*
