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
# # Lab 2.1 — Public Data Expedition: Profile an Agency Dataset  *(SOLUTION / instructor copy)*
#
# *Course 1258 — Applied AI for Government IT Professionals · Ch02 AI
# Applications Across Government and Public Data · 30 minutes · CloudShare VM
# (JupyterLab) · pandas — no API key needed (data.gov search has a cached
# fallback)*

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
#   `data/chicago_311.csv` — provenance in `data/MANIFEST.json`.
# - **Tools:** pandas + the course data.gov search helper (cached snapshot
#   fallback) — no API key needed.
# - Instructor copies live in `solutions/`, one level below `labs/` — the
#   first cell finds `labs/` (where `lab_common.py` / `lab_helpers.py` and
#   `data/` are) and runs from there.

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
# ## Steps
#
# 1. **(4 min)** Run the finding-data warm-up.
# 2. **(4 min)** Load each of the three datasets; print shape, columns,
#    column types.
# 3. **(6 min)** Per column: blank count, distinct count, an example value.
# 4. **(4 min)** Identify the grain of each dataset.
# 5. **(4 min)** Identify the time column; print the date range.
# 6. **(4 min)** One question each dataset answers well; one it cannot.
# 7. **(4 min)** Four-sentence briefing for the CDC wastewater file.

# %% [markdown]
# ### Step 1 — Warm-up: finding the data in the first place

# %%
KEYWORD = "air quality"   # the reference search topic
search_gov_datasets(KEYWORD)

# %% [markdown]
# ### Step 2 — Load all three datasets

# %%
frames = load_expedition_datasets()

# %% [markdown]
# ### Step 3 — A profile of each dataset

# %%
profile_datasets(frames)

# %% [markdown]
# ### Step 4 — The grain: what is one row? (expected answers)
#
# - **cdc_flu_wastewater:** one PCR measurement of one sample collected at one
#   wastewater site on one date — a *measurement*, not a place or a day (the
#   same site appears many times).
# - **nyc_air_quality:** one indicator value for one geography in one time
#   period — a long/tidy table where "which pollutant" and "which period" are
#   data, not columns. Hardest grain of the three; students often misread it
#   as "one row per neighbourhood".
# - **chicago_311:** one service request, keyed by `sr_number`.

# %% [markdown]
# ### Step 5 — The time dimension
#
# **Expected:** CDC `sample_collect_date` spans 2022-08-09 → 2026-07-28. NYC's
# `time_period` is the year (2021–2024 annual averages) — so the honest unit
# is a year, and `start_date` (2021-01-01 → 2024-01-01) just restates it at
# day precision; do not quote sub-annual freshness from it. Chicago
# `created_date` covers just 2026-07-31 → 2026-08-01 (~19 hours) — students
# should notice how *thin* that window is before anyone trends it.

# %%
show_time_ranges(frames)

# %% [markdown]
# ### Step 6 — What each dataset can and cannot answer (expected examples)
#
# - **cdc_flu_wastewater** — answers well: "Is flu-A signal rising at site X
#   this month?" / cannot answer: "How many people have flu?" (concentration
#   is not case counts; population_served is a catchment estimate).
# - **nyc_air_quality** — answers well: "Which neighbourhoods had the highest
#   PM2.5 in 2024?" / cannot answer: "Is today's air safe?" (periods are
#   annual averages, not current readings).
# - **chicago_311** — answers well: "What share of requests close same-day?"
#   / cannot answer: "Which problems matter most to residents?" (request
#   counts reflect reporting behaviour and automated feeds — 39% of this
#   extract is aircraft noise — not resident priorities).

# %% [markdown]
# ### Step 7 — Four-sentence briefing (worked example)
#
# "Each row of this file is one PCR measurement of Influenza A in a wastewater
# sample, drawn from 518 sites across 41 states and territories between August
# 2022 and July 2026. Its strength is lead time: it tracks community flu
# signal independent of whether anyone seeks a test or a doctor. Its main
# caveat is that concentration is not case counts — `population_served` is a
# catchment estimate and lab methods vary by site, so compare a site to its
# own history, not to other sites. Suitable for early-warning trend monitoring;
# not suitable for estimating how many people are sick."

# %% [markdown]
# ## Deliverable
#
# 1. The profiler output for all three datasets.
# 2. Grain, time range, and can/cannot-answer pairs for each.
# 3. The four-sentence CDC briefing.

# %% [markdown]
# ## Reflection (expected answers)
#
# 1. NYC air quality — the long format hides the grain until you read
#    `name`, `geo_type_name` and `time_period` together.
# 2. How is the population denominator estimated? What QC flags were applied?
#    Is anything suppressed for privacy? How fresh is the extract?
# 3. Not on its own: early warning is a *trend over time at one site*, so the
#    claim needs the time series plus a link to clinical data. The file is
#    consistent with the claim; it does not prove it.

# %% [markdown]
# ## Debrief (instructor-led)
#
# - Start with the time ranges: who noticed the Chicago 311 extract covers
#   about a day? Ask what that does to any trend claim built on it.
# - Take the NYC grain apart together (Step 4 notes) — the long format is the
#   one most rooms misread.
# - Hear two or three CDC briefings aloud; score against the checklist —
#   grain, coverage, strength, caveat — and flag any that promise case counts
#   the file cannot deliver.

# %% [markdown]
# ## Troubleshooting
#
# - **`source: cached` in Step 1.** Expected — the snapshot is the lesson.
# - **A mixed-types warning.** Real CSVs do this; the provided load handles
#   it.
# - **Blank dates / a surprising range.** Unparseable or blank dates are
#   skipped honestly — count the cost before quoting a range.
# - **NYC grain confusion.** Read `name`, `geo_type_name`, `time_period`
#   together — it is long/tidy, not one row per neighbourhood.
# - **Out-of-order errors.** Kernel → Restart & Run All.
