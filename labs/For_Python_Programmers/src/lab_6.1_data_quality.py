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
# Cells marked `# YOUR CODE` are for you to complete. No API key is needed.

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

# %% [markdown]
# ## Steps
#
# 1. Open `lab_6.1_data_quality.ipynb` and load the file. (3 min)
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
# service requests, warts included on purpose.

# %%
import pandas as pd

pd.set_option("display.width", 220)
pd.set_option("display.max_columns", 45)

df = pd.read_csv("data/chicago_311.csv", low_memory=False)
print("shape:", df.shape)
print("columns:", list(df.columns))

# %% [markdown]
# ### Step 2 — Completeness (6 min)
#
# Null rate per column; flag anything above 20%. Watch for columns that are
# null for a *reason* (a `closed_date` on an open request is not a defect).

# %%
completeness = None
# YOUR CODE: null percentage per column, sorted descending; flag columns > 20%.

if completeness is None:
    completeness = (df.isna().mean() * 100).round(1).sort_values(ascending=False)
    print("(reference answer applied)\n")
print(completeness[completeness > 0].to_string())
flagged = completeness[completeness > 20]
print(f"\ncolumns above 20% null: {len(flagged)}")

# %% [markdown]
# ### Step 3 — Uniqueness (6 min)
#
# Duplicate `sr_number` count; inspect a duplicate pair. Then look at the
# city's own `duplicate` flag — do the two stories agree?

# %%
dup_sr = None
flagged_dups = None
# YOUR CODE: dup_sr = number of duplicated sr_number values;
# flagged_dups = rows where the duplicate flag is True. Inspect both.

if dup_sr is None:
    dup_sr = int(df["sr_number"].duplicated().sum())
    flagged_dups = int(df["duplicate"].sum())
    print("(reference answers applied)\n")
print(f"duplicated sr_number values: {dup_sr}")
print(f"rows flagged duplicate=True by the city: {flagged_dups}")

# near-duplicates the key alone can't see:
key_dups = int(df.duplicated(subset=["sr_type", "street_address", "created_date"]).sum())
print(f"same type + address + timestamp (likely double submissions): {key_dups}")

# %% [markdown]
# ### Step 4 — Consistency (6 min)
#
# Case and whitespace variants in categorical columns. Check `city`, `state`,
# and the dtype of `zip_code` — a ZIP is an identifier, not a quantity.

# %%
consistency = None
# YOUR CODE: distinct raw values of city and state (with counts), and the
# dtype + a sample of zip_code.

if consistency is None:
    consistency = {
        "city": df["city"].value_counts(dropna=False).head(5).to_dict(),
        "state": df["state"].value_counts(dropna=False).head(5).to_dict(),
        "zip_dtype": str(df["zip_code"].dtype),
        "zip_sample": df["zip_code"].dropna().head(3).tolist(),
    }
    print("(reference answer applied)\n")
for k, v in consistency.items():
    print(f"{k}: {v}")

# %% [markdown]
# ### Step 5 — Validity (6 min)
#
# Dates outside a plausible range; requests closed before they were created.
# A zero here is a *pass* — record it as one, with the query that proved it.

# %%
created = pd.to_datetime(df["created_date"], errors="coerce")
closed = pd.to_datetime(df["closed_date"], errors="coerce")

validity = None
# YOUR CODE: count unparseable created dates, closed-before-created rows,
# and print the date range.

if validity is None:
    validity = {
        "created_unparseable": int(created.isna().sum()),
        "closed_before_created": int((closed < created).sum()),
        "range": f"{created.min()} -> {created.max()}",
    }
    print("(reference answer applied)\n")
print(validity)

# %% [markdown]
# ### Step 6 — Timeliness (5 min)
#
# The distribution of `created_date`: how current is the extract, and how
# wide is its window? Currency and coverage are different claims — assess
# both.

# %%
timeliness = None
# YOUR CODE: min/max of created_date and the number of distinct calendar
# days covered.

if timeliness is None:
    timeliness = {
        "newest": str(created.max()),
        "oldest": str(created.min()),
        "calendar_days": int(created.dt.date.nunique()),
        "window_hours": round((created.max() - created.min()).total_seconds() / 3600, 1),
    }
    print("(reference answer applied)\n")
print(timeliness)

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
# ### Step 8 — The scorecard (5 min)
#
# One table: dimension, metric, value, pass/fail. Fill it from the numbers
# above — the thresholds are yours to defend.

# %%
scorecard = None
# YOUR CODE: a DataFrame with columns [dimension, metric, value, passes]
# covering all six dimensions.

if scorecard is None:
    scorecard = pd.DataFrame([
        {"dimension": "Completeness", "metric": "columns >20% null",
         "value": f"{len(flagged)} of {df.shape[1]}", "passes": False},
        {"dimension": "Uniqueness", "metric": "duplicate sr_number",
         "value": dup_sr, "passes": dup_sr == 0},
        {"dimension": "Uniqueness", "metric": "city-flagged duplicates",
         "value": flagged_dups, "passes": False},
        {"dimension": "Consistency", "metric": "city/state case variants + zip dtype",
         "value": "Chicago/CHICAGO, Illinois/IL, zip as float", "passes": False},
        {"dimension": "Validity", "metric": "closed-before-created",
         "value": validity["closed_before_created"], "passes": True},
        {"dimension": "Timeliness", "metric": "window covered",
         "value": f"{timeliness['window_hours']}h, {timeliness['calendar_days']} days",
         "passes": False},
        {"dimension": "Accuracy", "metric": "testable from data alone?",
         "value": "no", "passes": None},
    ])
    print("(reference scorecard applied — adjust thresholds and defend your own)\n")
print(scorecard.to_string(index=False))

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
# - **`FileNotFoundError: data/chicago_311.csv`** — the kernel's working
#   directory is not `labs/`. Restart the kernel from the `labs/` folder and
#   Run All.
# - **`DtypeWarning` on load** — expected on this file (mixed types in
#   operational columns); `low_memory=False` in the load cell silences it.
# - **A dimension shows zero defects** — that is a pass, not a bug. Record it
#   in the scorecard with the query that proved it (Step 5 shows how).
# - **`zip_code` prints as float (60618.0)** — that *is* the consistency
#   defect Step 4 asks you to find, not a display error.
# - **Your scorecard values differ from a neighbour's** — the reference
#   scorecard is a starting point; if you measured the dimensions yourself,
#   defend your numbers. Only the load cell is shared state.
