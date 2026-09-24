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
# - **Tools:** pandas, plus `lab_common.search_datasets` for the finding-data
#   warm-up. **No API key is needed.** The data.gov search tries the live
#   catalogue and falls back to a cached snapshot, so it works offline.
# - **The one rule that never changes:** public or synthetic data only. Never
#   paste real agency, personal or sensitive data into any assistant.
# - Cells marked `# YOUR CODE` are for you to complete. Each has a reference
#   fallback that runs if you leave it blank — replace it with your own code
#   when you can.

# %% [markdown]
# ## Steps
#
# 1. **(4 min)** Open `lab_2.1_data_expedition.ipynb` and run the warm-up:
#    how you would *find* a dataset like these before profiling it.
# 2. **(4 min)** For **each** of the three datasets: load it and print shape,
#    columns, dtypes.
# 3. **(6 min)** Report per column: null count, distinct count, and an
#    example value.
# 4. **(4 min)** Identify the grain — what does one row actually represent?
# 5. **(4 min)** Identify the time column and print the date range.
# 6. **(4 min)** Name one question the dataset answers well and one it cannot
#    answer.
# 7. **(4 min)** Write a four-sentence briefing for the CDC wastewater file,
#    including its grain, coverage, and one caveat.

# %% [markdown]
# ### Step 1 — Warm-up: finding the data in the first place (provided)
#
# data.gov retired its JSON API, so `lab_common.search_datasets` tries the live
# catalogue and falls back to a cached snapshot. Either way, this is how you
# would *find* a dataset like the three below before profiling it. Watch which
# source it reports.

# %%
# Locate the labs/ folder no matter where Jupyter was started from.
import os, sys
from pathlib import Path

for _cand in (Path.cwd(), *Path.cwd().parents):
    if (_cand / "lab_common.py").is_file():
        os.chdir(_cand)
        if str(_cand) not in sys.path:
            sys.path.insert(0, str(_cand))
        break

import pandas as pd
from lab_common import search_datasets

pd.set_option("display.width", 200)

hits = search_datasets("air quality", rows=3)
print(f"source: {hits['source']}\n")
for h in hits["results"]:
    print(f"- {h['title']}  ({h['organization']})")
    print(f"  tags: {', '.join(h['tags'])}\n")

# %% [markdown]
# ### Step 2 — Load all three datasets
#
# Load each CSV and print its shape, columns, and dtypes. Just the first
# look — the detailed per-column profile is Step 3.

# %%
DATASETS = {
    "cdc_flu_wastewater": "data/cdc_flu_wastewater.csv",
    "nyc_air_quality": "data/nyc_air_quality.csv",
    "chicago_311": "data/chicago_311.csv",
}
frames = {name: pd.read_csv(path, low_memory=False)
          for name, path in DATASETS.items()}

for name, frame in frames.items():
    print(f"=== {name}: {frame.shape[0]:,} rows x {frame.shape[1]} columns ===")
    print("columns:", list(frame.columns))
    print(frame.dtypes.value_counts().to_string(), "\n")

# %% [markdown]
# ### Step 3 — A profiler you can reuse
#
# Write `profile(df, name)`: per column, print the null count, distinct
# count, and one example value. You will run it on all three datasets, so
# write it once.

# %%
def profile(df, name):
    # YOUR CODE: print the dataset name and shape, then a table with one row
    # per column: dtype, nulls, nunique, and an example non-null value.
    return None


def reference_profile(df, name):
    """Provided fallback so later cells run. Peek only if stuck!"""
    print(f"=== {name}: {df.shape[0]:,} rows x {df.shape[1]} columns ===")
    rows = []
    for col in df.columns:
        example = df[col].dropna().iloc[0] if df[col].notna().any() else None
        rows.append({"column": col, "dtype": str(df[col].dtype),
                     "nulls": int(df[col].isna().sum()),
                     "distinct": int(df[col].nunique()),
                     "example": str(example)[:40]})
    print(pd.DataFrame(rows).to_string(index=False))
    print()


for name, frame in frames.items():
    fn = profile(frame, name)
    if fn is None:
        reference_profile(frame, name)

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
# ### Step 5 — The time dimension
#
# Every dataset here has a time column (or something playing that role). Find
# it and print the range it covers.

# %%
time_ranges = {}
# YOUR CODE: for each frame, identify the time column, parse it, and store
# (min, max) in time_ranges[name]. (NYC's is not a full date — look at
# time_period and start_date and decide which is honest.)

if not time_ranges:
    cdc_dates = pd.to_datetime(frames["cdc_flu_wastewater"]["sample_collect_date"],
                               errors="coerce")
    nyc_dates = pd.to_datetime(frames["nyc_air_quality"]["start_date"], errors="coerce")
    c311_dates = pd.to_datetime(frames["chicago_311"]["created_date"], errors="coerce")
    time_ranges = {
        "cdc_flu_wastewater": (cdc_dates.min(), cdc_dates.max()),
        "nyc_air_quality": (nyc_dates.min(), nyc_dates.max()),
        "chicago_311": (c311_dates.min(), c311_dates.max()),
    }
    print("(reference answer applied — replace with your own code above)\n")
for name, (lo, hi) in time_ranges.items():
    print(f"{name:22s} {lo}  ->  {hi}")

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
# - **`DtypeWarning: Columns (n) have mixed types`.** Real government CSVs do
#   this; `low_memory=False` in the provided load silences it by reading the
#   file in one pass.
# - **`pd.to_datetime` produced `NaT` values.** Some rows have unparseable or
#   blank dates — `errors="coerce"` is the honest fix; note how many rows it
#   cost before quoting a range.
# - **The profiler cell prints the reference version, not yours.** Your
#   `profile()` must *return something* (even `True`) once it prints — a bare
#   `return None` keeps the fallback engaged.
# - **Out-of-order errors after experimenting.** Kernel → Restart & Run All.
