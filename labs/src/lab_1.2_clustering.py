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
# this) · CloudShare VM (JupyterLab) · pandas + scikit-learn — no API key
# needed*
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
# - **Tools:** pandas, scikit-learn (`StandardScaler`, `KMeans`), matplotlib.
#   Run from the `labs/` folder.
# - **No API key is needed** — this lab never calls a model.
# - **The one rule that never changes:** public or synthetic data only.
# - Cells marked `# YOUR CODE` are for you to complete. Each has a reference
#   fallback that runs if you leave it blank — replace it with your own line
#   when you can.

# %% [markdown]
# ## Steps
#
# 1. **(3 min)** Open `lab_1.2_clustering.ipynb` and load
#    `epa_aqi_by_county.csv`.
# 2. **(4 min)** Select the numeric day-count columns and scale them.
# 3. **(5 min)** Fit K-Means with k=3. Print each cluster's size and column
#    means.
# 4. **(3 min)** Name each cluster in plain English from those means.
# 5. **(6 min)** Sweep k from 2 to 8, plot inertia, and choose a k you can
#    defend.
# 6. **(5 min)** List the counties in the worst cluster and sanity-check
#    against the raw rows.
# 7. **(4 min)** Write two sentences a programme director could act on.

# %% [markdown]
# ### Step 1 — Load the EPA annual summary (provided)
#
# `data/epa_aqi_by_county.csv` has one row per county for 2024: how many days
# the county spent at each AQI level, plus summary statistics.

# %%
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

epa = pd.read_csv("data/epa_aqi_by_county.csv")
print("shape:", epa.shape, "| states/territories:", epa["State"].nunique())
print("columns:", list(epa.columns))
epa.head(3)

# %% [markdown]
# ### Step 2 — Select and scale the features
#
# The features are the six **day-count columns**: how many days each county
# spent at each AQI category, from `Good Days` to `Hazardous Days`. K-Means is
# a distance algorithm — with unscaled features, the big counts (hundreds of
# good days) would crush the small ones (a handful of hazardous days).

# %%
FEATURES = ["Good Days", "Moderate Days", "Unhealthy for Sensitive Groups Days",
            "Unhealthy Days", "Very Unhealthy Days", "Hazardous Days"]

X = None
# YOUR CODE: fit a StandardScaler on epa[FEATURES] and store the transformed
# array in X (one line: StandardScaler().fit_transform(...)).

if X is None:
    X = StandardScaler().fit_transform(epa[FEATURES])
    print("(reference scaling applied — replace with your own line above)")
print("scaled feature matrix:", X.shape)

# %% [markdown]
# ### Step 3 — Fit k=3 and read the clusters
#
# Fit K-Means with k=3, then print each cluster's size and its column means
# (back in *original* units, so they read as days per year).

# %%
km3 = KMeans(n_clusters=3, n_init=10, random_state=42).fit(X)
epa["cluster_k3"] = km3.labels_

means = epa.groupby("cluster_k3")[FEATURES + ["Median AQI"]].mean().round(1)
means["counties"] = epa["cluster_k3"].value_counts()
print(means.to_string())

# %% [markdown]
# ### Step 4 — Name each cluster in plain English (write here)
#
# *One short name per cluster, from the means above — e.g. "the clean
# majority", "the moderate middle", ...:*
#
# - cluster 0:
# - cluster 1:
# - cluster 2:

# %% [markdown]
# ### Step 5 — Choose k deliberately: the elbow method
#
# Sweep k from 2 to 8, record each model's **inertia** (sum of squared
# distances to cluster centres), and plot it. The elbow — where adding another
# cluster stops paying off — is your candidate k.

# %%
inertias = []
# YOUR CODE: fit KMeans for k = 2..8 on X (n_init=10, random_state=42),
# appending each model's .inertia_ to `inertias`.

if not inertias:
    for k in range(2, 9):
        inertias.append(KMeans(n_clusters=k, n_init=10, random_state=42).fit(X).inertia_)
    print("(reference sweep applied — replace with your own loop above)\n")
for k, i in zip(range(2, 9), inertias):
    print(f"k={k}  inertia={i:,.0f}")

plt.figure(figsize=(6, 3.5))
plt.plot(range(2, 9), inertias, marker="o")
plt.xlabel("k (number of clusters)")
plt.ylabel("inertia")
plt.title("Elbow method — where does the curve stop paying off?")
plt.show()

# %% [markdown]
# ### Step 6 — Fit your chosen k and find the worst cluster
#
# Pick the k you can defend from the elbow plot, refit, and list the counties
# in the worst-air cluster. Sanity-check them against the raw rows — do the
# day counts match the story the means told?

# %%
K = None  # YOUR CODE: the k you chose from the elbow plot

if K is None:
    K = 4
    print("(reference K=4 applied — choose your own from the elbow plot)\n")

km = KMeans(n_clusters=K, n_init=10, random_state=42).fit(X)
epa["cluster"] = km.labels_
epa["unhealthy_total"] = (epa["Unhealthy Days"] + epa["Very Unhealthy Days"]
                          + epa["Hazardous Days"])

summary = epa.groupby("cluster")[FEATURES + ["Median AQI"]].mean().round(1)
summary["counties"] = epa["cluster"].value_counts()
print(summary.to_string())

worst = epa.groupby("cluster")["unhealthy_total"].mean().idxmax()
print(f"\nworst cluster: {worst}")
print(epa[epa["cluster"] == worst]
      .sort_values("unhealthy_total", ascending=False)
      [["State", "County", "unhealthy_total", "Max AQI", "Median AQI"]]
      .head(15).to_string(index=False))

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
#   from the *means*, not the row list — point out any that just describe one
#   famous county.
# - Compare chosen k values: k=3 and k=4 are both defensible; ask a defender
#   of each what they optimized for (simplicity vs separating the
#   extreme-event counties).
# - Land the unsupervised punchline: there is no "correct" answer to check
#   against — the test is whether the grouping is *useful and stable* (does it
#   survive a different `random_state`?).

# %% [markdown]
# ## Troubleshooting
#
# - **`ModuleNotFoundError: sklearn` (or matplotlib).** The VM image is missing
#   a package — tell your instructor; run the Day-0 healthcheck to confirm.
# - **Your cluster numbers don't match your neighbour's names.** Cluster
#   *labels* are arbitrary — cluster 0 in your run can be cluster 2 in theirs.
#   Compare the means and county lists, not the numbers.
# - **`ConvergenceWarning` from KMeans.** Harmless at this size; `n_init=10`
#   already re-runs the fit ten times and keeps the best.
# - **The elbow plot didn't appear.** Re-run the cell; if it still doesn't,
#   Kernel → Restart & Run All.
# - **Different results after a kernel restart.** You changed `random_state`
#   or edited the feature list — reset both to the provided values and re-run.
