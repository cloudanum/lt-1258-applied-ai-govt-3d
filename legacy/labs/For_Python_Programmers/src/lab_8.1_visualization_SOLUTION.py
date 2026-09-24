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
# # Lab 8.1 — Visualization and Reporting from EPA Data  *(SOLUTION / instructor copy)*
#
# **Chapter 8 — AI Operations and Reporting in Government** · 40 minutes
#
# **Objectives**
# 1. Build charts that answer a stated question.
# 2. Apply the visualization guidelines deliberately.
# 3. Turn three charts into a one-page briefing.

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
import matplotlib.pyplot as plt

epa = pd.read_csv("data/epa_aqi_by_county.csv")
epa["unhealthy_total"] = (epa["Unhealthy Days"] + epa["Very Unhealthy Days"]
                          + epa["Hazardous Days"])
print("shape:", epa.shape)
epa[["State", "County", "unhealthy_total", "Median AQI", "Max AQI"]].head(3)

# %% [markdown]
# ## Step 2 — Chart 1: the 15 worst counties
#
# **Expected finding 1:** "San Bernardino County recorded 88 days at
# Unhealthy or worse in 2024 — nearly three months — followed by Riverside
# (67) and Los Angeles (55), with every other county below 35. Four of the
# five worst counties are in California. The problem is concentrated, not
# diffuse: the top three counties alone account for 210 of the state's 317
# unhealthy county-days."

# %%
top15 = epa.nlargest(15, "unhealthy_total").iloc[::-1].copy()
top15["label"] = top15["County"] + ", " + top15["State"]

fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(top15["label"], top15["unhealthy_total"])
ax.set_xlabel("days at Unhealthy or worse, 2024")
ax.set_ylabel("")
ax.set_title("Which counties had the most unhealthy air days in 2024?")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Step 3 — Chart 2: how widespread is the problem?
#
# **Expected finding 2:** "The national median county saw a median AQI of 40
# — solidly in the Good band — and 92.7% of counties had a median at or below
# 50. Bad air is therefore a *local* condition, not a national one, on a
# typical day. The right tail, not the middle, is where the policy problem
# lives."

# %%
fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(epa["Median AQI"], bins=30)
ax.axvline(50, color="grey", linestyle="--", linewidth=1)
ax.text(51, ax.get_ylim()[1] * 0.8, "Good/Moderate boundary (50)", fontsize=9)
ax.set_xlabel("county's median AQI, 2024")
ax.set_ylabel("number of counties")
ax.set_title("Most counties breathe Good air most of the year")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Step 4 — Chart 3: California against the nation
#
# **Expected finding 3:** "Two-thirds of California's 52 counties (35 of 52)
# sit above the national median median-AQI of 40. California's own median
# (46.5) is in the Good band but much closer to the boundary than the
# nation's. The state's air-quality problem is broad, not just three famous
# counties."

# %%
STATE = "California"
state_df = epa[epa["State"] == STATE].sort_values("Median AQI", ascending=False)
national_median = epa["Median AQI"].median()

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(state_df["County"], state_df["Median AQI"])
ax.axhline(national_median, color="grey", linestyle="--", linewidth=1)
ax.text(0, national_median + 1, f"national median = {national_median:.0f}", fontsize=9)
ax.set_ylabel("median AQI, 2024")
ax.set_title(f"{STATE} counties vs. the national median")
ax.set_xticks(range(len(state_df)))
ax.set_xticklabels(state_df["County"], rotation=90, fontsize=6)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Step 5 — Guideline checklist (audited)
#
# - [x] Bars sorted by value (chart 1 descending; chart 3 descending)
# - [x] Axes labelled with units ("days", "AQI, 2024"); titles state the
#       question or the answer
# - [x] No chartjunk — single-series bars, no legend, no gridlines, no colour
#       games
# - [x] Honest scale — all bar charts start at zero (check this if students
#       trimmed the y-axis "to see the differences": that is the a3 CTA
#       chart's mistake)
#
# ## Step 6 — Assemble the one-page briefing

# %%
fig, axes = plt.subplots(3, 1, figsize=(9, 12))
fig.suptitle("U.S. county air quality, 2024: where should EPA focus outreach?",
             fontsize=13, fontweight="bold")

axes[0].barh(top15["label"], top15["unhealthy_total"])
axes[0].set_title("1. The worst air is concentrated in a few counties", fontsize=10)
axes[0].set_xlabel("days at Unhealthy or worse")

axes[1].hist(epa["Median AQI"], bins=30)
axes[1].axvline(50, color="grey", linestyle="--", linewidth=1)
axes[1].set_title("2. Most counties are in the Good band most of the year", fontsize=10)
axes[1].set_xlabel("county median AQI")

axes[2].bar(state_df["County"], state_df["Median AQI"])
axes[2].axhline(national_median, color="grey", linestyle="--", linewidth=1)
axes[2].set_title(f"3. {STATE} sits mostly above the national median", fontsize=10)
axes[2].set_ylabel("median AQI")
axes[2].set_xticks(range(len(state_df)))
axes[2].set_xticklabels(state_df["County"], rotation=90, fontsize=6)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("epa_briefing.png", dpi=120)
plt.show()
print("saved epa_briefing.png")

# %% [markdown]
# ### Recommendation (worked)
#
# "Focus chronic-exposure outreach on the three Southern California counties
# that logged 46+ Unhealthy days each in 2024, and treat the remaining
# outliers — a handful of counties with rare but hazardous smoke and dust
# events — as an emergency-communication problem, not a chronic one."
#
# ## Reflection (expected answers)
# 1. Chart 1 — sorted bars, meaningful labels, and a title that is the
#    question; it stands alone. Chart 3 without its median line caption is
#    the weakest.
# 2. Sorting turns a list into a ranking: the reader's eye goes straight to
#    San Bernardino instead of hunting; unsorted, the same data says nothing
#    in the first two seconds.
# 3. `Max AQI` was left out: a single-day spike (Essex County, MA hit 1513 —
#    a wildfire-smoke event) would dominate any scale and describe one bad
#    day, not air quality. Choosing the honest aggregate is a chart decision.
