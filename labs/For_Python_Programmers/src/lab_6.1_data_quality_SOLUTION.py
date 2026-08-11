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
# # Lab 6.1 — Data Quality Assessment of Chicago 311  *(SOLUTION / instructor copy)*
#
# **Chapter 6 — Data for AI: Collection, Quality, and Governance** · 45 minutes
#
# **Objectives**
# 1. Assess a real dataset against all six quality dimensions.
# 2. Quantify each defect rather than describing it.
# 3. Produce a go / no-go recommendation with evidence.

# %%
# Instructor copies live in solutions/, one level below labs/ — find labs/
# (where lab_common.py and data/ are) and run from there.
import os, sys
from pathlib import Path

for _cand in (Path.cwd(), Path.cwd().parent):
    if (_cand / "lab_common.py").is_file():
        os.chdir(_cand)
        if str(_cand) not in sys.path:
            sys.path.insert(0, str(_cand))
        break

# %% [markdown]
# ## Step 1 — Load

# %%
import pandas as pd

pd.set_option("display.width", 220)
pd.set_option("display.max_columns", 45)

df = pd.read_csv("data/chicago_311.csv", low_memory=False)
print("shape:", df.shape)
print("columns:", list(df.columns))

# %% [markdown]
# ## Step 2 — Completeness
#
# **Expected:** 7 columns over 20% null, two of them 100% (`legacy_sr_number`,
# `sanitation_division_days`) and `created_department` ~69%. Debrief point:
# `closed_date` (~35% null) correlates exactly with `status == "Open"` — a
# null that is *structure*, not defect. Distinguish "missing" from
# "not applicable".

# %%
completeness = (df.isna().mean() * 100).round(1).sort_values(ascending=False)
print(completeness[completeness > 0].to_string())
flagged = completeness[completeness > 20]
print(f"\ncolumns above 20% null: {len(flagged)}")
print("closed_date null == open requests?",
      int(df["closed_date"].isna().sum()), "==",
      int((df["status"] == "Open").sum()))

# %% [markdown]
# ## Step 3 — Uniqueness
#
# **Expected:** `sr_number` is perfectly unique (0 dups) — the *key* passes.
# But the city flags 220 rows (5.5%) as duplicates of an earlier request, and
# 19 rows share type + address + timestamp down to the second (true double
# submissions). Lesson: test uniqueness at the grain of the *event*, not just
# the key.

# %%
dup_sr = int(df["sr_number"].duplicated().sum())
flagged_dups = int(df["duplicate"].sum())
print(f"duplicated sr_number values: {dup_sr}")
print(f"rows flagged duplicate=True by the city: {flagged_dups}")

key_dups = int(df.duplicated(subset=["sr_type", "street_address", "created_date"]).sum())
print(f"same type + address + timestamp (likely double submissions): {key_dups}")
print(df[df.duplicated(subset=["sr_type", "street_address", "created_date"], keep=False)]
      [["sr_number", "sr_type", "street_address", "created_date"]]
      .sort_values(["street_address", "created_date"]).head(4).to_string(index=False))

# %% [markdown]
# ## Step 4 — Consistency
#
# **Expected:** `Chicago` ×3,428 vs `CHICAGO` ×1; `Illinois` ×3,426 vs `IL`
# ×3; `zip_code` stored as float64 (`60666.0`) — an identifier treated as a
# quantity, and 571 rows have no city/state/zip at all. Small counts, but
# each one breaks a naive `GROUP BY`.

# %%
consistency = {
    "city": df["city"].value_counts(dropna=False).head(5).to_dict(),
    "state": df["state"].value_counts(dropna=False).head(5).to_dict(),
    "zip_dtype": str(df["zip_code"].dtype),
    "zip_sample": df["zip_code"].dropna().head(3).tolist(),
}
for k, v in consistency.items():
    print(f"{k}: {v}")

# %% [markdown]
# ## Step 5 — Validity
#
# **Expected:** 0 unparseable dates, 0 closed-before-created, range
# 2026-07-31 → 2026-08-01. A clean pass — record it *with* the query, because
# "we checked and it passed" is evidence; "looks fine" is not.

# %%
created = pd.to_datetime(df["created_date"], errors="coerce")
closed = pd.to_datetime(df["closed_date"], errors="coerce")

validity = {
    "created_unparseable": int(created.isna().sum()),
    "closed_before_created": int((closed < created).sum()),
    "range": f"{created.min()} -> {created.max()}",
}
print(validity)

# %% [markdown]
# ## Step 6 — Timeliness
#
# **Expected:** the extract is current to within hours but covers only a
# ~19-hour window across 2 calendar days. Current ≠ sufficient: no season,
# no trend, no weekend/weekday contrast. Any "target service improvements"
# plan needs a longer pull.

# %%
timeliness = {
    "newest": str(created.max()),
    "oldest": str(created.min()),
    "calendar_days": int(created.dt.date.nunique()),
    "window_hours": round((created.max() - created.min()).total_seconds() / 3600, 1),
}
print(timeliness)

# %% [markdown]
# ## Step 7 — Accuracy (expected answer)
#
# *Column chosen:* `street_address`. *Test:* accuracy needs ground truth the
# file does not contain — sample N requests and verify the address against
# the city's address master file (or geocode and check the point falls inside
# the stated community area, which the file *does* provide as a cross-check:
# rows where latitude/longitude disagree with `community_area` are accuracy
# suspects). Cost: an address-master join plus a spot sample — cheap as a
# sample, expensive as a census. The honest sentence: "accuracy is estimated
# by audit, not computed."

# %% [markdown]
# ## Step 8 — The scorecard (worked)

# %%
scorecard = pd.DataFrame([
    {"dimension": "Completeness", "metric": "columns >20% null",
     "value": f"{len(flagged)} of {df.shape[1]} (2 entirely empty)", "passes": False},
    {"dimension": "Uniqueness", "metric": "duplicate sr_number",
     "value": dup_sr, "passes": True},
    {"dimension": "Uniqueness", "metric": "city-flagged duplicates",
     "value": f"{flagged_dups} (5.5%)", "passes": False},
    {"dimension": "Consistency", "metric": "city/state variants + zip dtype",
     "value": "Chicago/CHICAGO, Illinois/IL, zip as float64", "passes": False},
    {"dimension": "Validity", "metric": "closed-before-created / bad dates",
     "value": "0 / 0", "passes": True},
    {"dimension": "Timeliness", "metric": "window covered",
     "value": f"{timeliness['window_hours']}h, {timeliness['calendar_days']} calendar days",
     "passes": False},
    {"dimension": "Accuracy", "metric": "testable from data alone?",
     "value": "no — needs address-master audit", "passes": None},
])
print(scorecard.to_string(index=False))

# %% [markdown]
# ### Go / no-go recommendation (worked)
#
# "**Conditional go.** The file is structurally sound — unique keys, valid
# dates, current to within hours — and usable for operational questions about
# *this* window. But 5.5% of rows are flagged duplicates and the extract
# covers only ~19 hours: any citywide targeting decision needs the duplicate
# flag honoured and at least a full-year pull first. The two numbers that
# drive this: **220 flagged duplicates** and **2 calendar days of coverage**."
#
# ## Reflection (expected answers)
# 1. Accuracy — every other dimension grades the file against itself;
#    accuracy grades it against the world.
# 2. Constrain `city`/`state` to a dropdown (or store ZIP as text) at the
#    intake form — the cheapest defect is the one never typed.
# 3. If the recommendation names its evidence and its conditions, yes —
#    a conditional go with numbers is signable; an unconditional one would
#    not be.
