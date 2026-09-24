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
# # Lab 1.2 — Clustering Counties by Air Quality (K-Means)
#
# *Course 1258 — Applied AI for Government IT Professionals · Ch01 AI and ML
# Foundations for Government · 30 minutes (flex — your instructor may skip
# this) · CloudShare VM (JupyterLab) · no API key needed*
#
# EPA publishes an annual air-quality summary for every county. Nobody has
# labelled them. You want to find the natural groupings so a programme office
# can target outreach.

# %% [markdown]
# ## Objectives
#
# By the end of this lab, you will:
#
# - Run K-Means on a real EPA dataset and interpret the clusters.
# - Choose k deliberately rather than by default.
# - Explain an unsupervised result to a non-technical stakeholder.

# %% [markdown]
# ## Setup
#
# - **Dataset:** `data/epa_aqi_by_county.csv` — EPA annual Air Quality Index
#   by county, 2024: one row per county, with the number of days spent at each
#   AQI level plus summary statistics. Provenance in `data/MANIFEST.json`.
# - **No API key is needed** — this lab never calls a model.
# - **The one rule that never changes:** public or synthetic data only.
# - **How this notebook works:** every step is one provided cell — run it with
#   Shift+Enter and read what it prints. Cells marked `# YOUR TURN` ask you to
#   change a simple value (like the number of clusters) and re-run the cell.
#   Everything runs as shipped, so you can never get stuck.

# %%
# ▶ Setup — run this cell first (click it, then Shift+Enter).
# It loads the course helper functions used by every step below.
from lab_helpers import *

# %% [markdown]
# ## Steps
#
# 1. **(3 min)** Load `epa_aqi_by_county.csv`.
# 2. **(4 min)** Scale the numeric day-count columns.
# 3. **(5 min)** Group the counties into 3 clusters. Read each cluster's size
#    and averages.
# 4. **(3 min)** Name each cluster in plain English from those averages.
# 5. **(6 min)** Try 2 to 8 clusters, look at the "elbow" plot, and choose a
#    number of clusters you can defend.
# 6. **(5 min)** List the counties in the worst cluster and sanity-check
#    against the raw rows.
# 7. **(4 min)** Write two sentences a programme director could act on.

# %% [markdown]
# ### Step 1 — Load the EPA annual summary (provided)
#
# `data/epa_aqi_by_county.csv` has one row per county for 2024: how many days
# the county spent at each AQI level, plus summary statistics.

# %%
epa = load_epa_data()

# %% [markdown]
# ### Step 2 — Scale the features (provided)
#
# The features are the six **day-count columns**: how many days each county
# spent at each AQI category, from `Good Days` to `Hazardous Days`. K-Means is
# a distance algorithm — with unscaled features, the big counts (hundreds of
# good days) would crush the small ones (a handful of hazardous days). This
# cell gives every feature equal weight.

# %%
X = scale_day_counts(epa)

# %% [markdown]
# ### Step 3 — Group into 3 clusters and read them (provided)
#
# This cell groups the counties into 3 clusters, then prints each cluster's
# size and its column averages (back in *original* units, so they read as days
# per year).

# %%
show_clusters(epa, X, k=3)

# %% [markdown]
# ### Step 4 — Name each cluster in plain English (write here)
#
# *One short name per cluster, from the averages above — e.g. "the clean
# majority", "the moderate middle", ...:*
#
# - cluster 0:
# - cluster 1:
# - cluster 2:

# %% [markdown]
# ### Step 5 — Choose the number of clusters deliberately: the elbow method
# (provided)
#
# This cell tries 2 to 8 clusters, records each grouping's **inertia** (how
# spread out the clusters are — lower is tighter), and plots it. The elbow —
# where adding another cluster stops paying off — is your candidate k.

# %%
elbow_plot(X)

# %% [markdown]
# ### Step 6 — Fit your chosen k and find the worst cluster
#
# Pick the k you can defend from the elbow plot, put it in the cell below, and
# run it. The cell lists the counties in the worst-air cluster. Sanity-check
# them against the raw rows — do the day counts match the story the averages
# told?

# %%
K = 4   # ← YOUR TURN: replace 4 with the k you chose from the elbow plot, then re-run this cell
show_worst_counties(epa, X, k=K)

# %% [markdown]
# ### Step 7 — Two sentences for the programme director (write here)
#
# *What the clusters are, and which counties the outreach programme should
# start with:*
#
# -
# -

# %% [markdown]
# ## Deliverable
#
# 1. The elbow plot and your chosen k (one sentence justifying it).
# 2. The cluster summary table with your plain-English name for each cluster.
# 3. The worst-cluster county list, sanity-checked against raw rows.
# 4. Your two sentences for the programme director.

# %% [markdown]
# ## Reflection
#
# 1. What changed when you changed k?
# 2. Why did scaling matter here?
# 3. What would you tell someone who asked "is this cluster *correct*?"

# %% [markdown]
# ## Debrief (instructor-led)
#
# - Collect the cluster names the room invented in Step 4. The best ones come
#   from the *averages*, not the row list — point out any that just describe
#   one famous county.
# - Compare chosen k values: k=3 and k=4 are both defensible; ask a defender
#   of each what they optimized for (simplicity vs separating the
#   extreme-event counties).
# - Land the unsupervised punchline: there is no "correct" answer to check
#   against — the test is whether the grouping is *useful and stable* (does it
#   survive a re-run of the steps?).

# %% [markdown]
# ## Troubleshooting
#
# - **A red error mentioning `sklearn` or `matplotlib`.** The VM image is
#   missing a package — tell your instructor; run the Day-0 healthcheck to
#   confirm.
# - **Your cluster numbers don't match your neighbour's names.** Cluster
#   *numbers* are arbitrary — cluster 0 in your run can be cluster 2 in theirs.
#   Compare the averages and county lists, not the numbers.
# - **A `ConvergenceWarning` appears.** Harmless at this size — the grouping
#   step already re-runs the fit ten times and keeps the best.
# - **The elbow plot didn't appear.** Re-run the cell; if it still doesn't,
#   Kernel → Restart & Run All.
# - **Different results after a kernel restart.** You edited `K` — reset it to
#   your chosen value and re-run the cell.

# %% [markdown]
# ---
# *Curious about the Python behind these steps? The full code-forward version
# of this lab lives in the `For_Python_Programmers/` folder.*
