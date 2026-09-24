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
# # Lab 1.3 — Decision Tree Classifier  *(SOLUTION / instructor copy)*
#
# **Course 1258 · Ch01 AI and ML Foundations** · 30 minutes (flex) · no API
# key needed
#
# **Objectives**
# 1. Train a decision tree on the EPA county AQI dataset.
# 2. Visualize the tree and read its rules in plain English.
# 3. Measure accuracy honestly (train/test split).
# 4. Show overfitting as depth grows; pick a defensible depth.
# 5. Explain feature leakage.

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
# ## Steps 1–2 — Data, label, features
#
# **Instructor note.** 997 county rows, 151 positive (15%) — the
# always-say-no baseline is 85%, so quote that *before* anyone celebrates
# an 86% test score. Leakage columns to name on the board: `Unhealthy
# Days` (the label itself), `Very Unhealthy Days`, `Hazardous Days`,
# `Max AQI`, `90th Percentile AQI` (all tail statistics of the same
# distribution).

# %%
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text
from sklearn.metrics import ConfusionMatrixDisplay

aqi = pd.read_csv("data/epa_aqi_by_county.csv")
aqi["has_unhealthy"] = (aqi["Unhealthy Days"] > 0).astype(int)

counts = aqi["has_unhealthy"].value_counts().sort_index()
print(f"{len(aqi)} counties | {counts[1]} with unhealthy days "
      f"({counts[1] / len(aqi):.0%})")

counts.rename({0: "no unhealthy days", 1: "unhealthy days"}) \
      .plot.bar(color=["#4c9f70", "#c0504d"], rot=0,
                ylabel="counties", title="Class balance — EPA counties 2024")
plt.tight_layout(); plt.show()

FEATURES = ["Days with AQI", "Good Days", "Moderate Days", "Median AQI",
            "Days CO", "Days NO2", "Days Ozone", "Days PM2.5", "Days PM10"]
X = aqi[FEATURES]
y = aqi["has_unhealthy"]

# %% [markdown]
# ## Steps 3–4 — Split, fit, score
#
# **Expected result (seed 42):** depth-3 tree → train ≈ 0.886, test ≈
# 0.860, 7 leaves. Beats the 85% baseline by only a few points — a good,
# honest number to interrogate with the confusion matrix: the tree catches
# most unhealthy counties but still misses some (false negatives).

# %%
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

tree = DecisionTreeClassifier(max_depth=3, random_state=42)
tree.fit(X_train, y_train)
print(f"train accuracy: {tree.score(X_train, y_train):.3f}")
print(f"test  accuracy: {tree.score(X_test, y_test):.3f} "
      f"| depth {tree.get_depth()}, {tree.get_n_leaves()} leaves")

ConfusionMatrixDisplay.from_estimator(
    tree, X_test, y_test, cmap="Blues", colorbar=False,
    display_labels=["no unhealthy", "unhealthy"])
plt.title("Confusion matrix — depth-3 tree (test set)")
plt.tight_layout(); plt.show()

# %% [markdown]
# ## Step 5 — The tree figure
#
# **Reading:** root split is `Median AQI <= 53.5` — typical-day air
# quality, not the tail. The right branch (median > 53.5) is where the
# unhealthy counties live; the tree then separates them on `Days PM2.5`
# and `Days CO`. One rule path to read aloud: *median AQI > 53.5, PM2.5
# days ≤ 281, CO days > 1 → no unhealthy days* (a county with dirty
# typical air dominated by traffic/CO rather than smoke).

# %%
fig, ax = plt.subplots(figsize=(24, 10))
plot_tree(tree, ax=ax, feature_names=FEATURES,
          class_names=["no unhealthy days", "unhealthy days"],
          filled=True, rounded=True, fontsize=10, proportion=False)
plt.title("Decision tree — which counties record unhealthy air days?",
          fontsize=14)
plt.tight_layout(); plt.show()

# %% [markdown]
# ## Step 6 — Importances and rules
#
# **Expected:** `Median AQI` dominates (~0.66 of total importance), then
# `Days with AQI` (~0.10) and `Days PM2.5` (~0.10). Nice audit point:
# `Days with AQI` enters because counties with more measured days have
# more chances to log a bad one — a *data-collection* feature, not an
# air-quality feature. Worth a sentence in any model documentation.

# %%
importances = pd.Series(tree.feature_importances_, index=FEATURES) \
    .sort_values()
importances[importances > 0].plot.barh(
    color="#2e6f8e", title="Feature importances — depth-3 tree",
    xlabel="importance")
plt.tight_layout(); plt.show()

print(export_text(tree, feature_names=FEATURES))

# %% [markdown]
# ## Step 7 — worked: the uncapped tree
#
# **Expected result:** train = 1.000, test ≈ 0.848, ~106 leaves. The tree
# memorized every training county and got *worse* on unseen ones — the
# overfitting gap in three numbers.

# %%
full_tree = DecisionTreeClassifier(max_depth=None, random_state=42)
full_tree.fit(X_train, y_train)
print(f"full tree: train={full_tree.score(X_train, y_train):.3f} "
      f"test={full_tree.score(X_test, y_test):.3f} "
      f"leaves={full_tree.get_n_leaves()}")

# %% [markdown]
# ## Step 8 — worked: the depth sweep
#
# **Expected shape:** train accuracy climbs to 1.0 as depth grows; test
# accuracy flattens around depth 2–4 and wobbles downward after.
# Reference pick: depth 3 — at/near the test peak, still drawable on one
# slide. Accept any answer in 2–4 with that reasoning.

# %%
depths = list(range(1, 13))
train_acc, test_acc = [], []
for d in depths:
    t = DecisionTreeClassifier(max_depth=d, random_state=42)
    t.fit(X_train, y_train)
    train_acc.append(t.score(X_train, y_train))
    test_acc.append(t.score(X_test, y_test))

plt.figure(figsize=(8, 4.5))
plt.plot(depths, train_acc, "o-", label="train")
plt.plot(depths, test_acc, "s-", label="test")
plt.xlabel("max_depth"); plt.ylabel("accuracy")
plt.title("Overfitting curve — deeper memorizes, not generalizes")
plt.xticks(depths); plt.legend(); plt.grid(alpha=0.3)
plt.tight_layout(); plt.show()

best_depth = 3
print(f"chosen depth: {best_depth} — test accuracy at/near peak, "
      f"tree still fits on one slide and reads as ~7 rules")

# %% [markdown]
# ## Grading notes
#
# - **Rule path:** any valid root-to-leaf path read correctly (feature,
#   threshold, direction, leaf class).
# - **Uncapped tree:** must show train ≈ 1.0 with test *lower* than the
#   depth-3 tree, and the sentence must name overfitting (or
#   memorization/generalization).
# - **best_depth:** 2–4 accepted when justified by the test curve or by
#   "simplest tree that captures the pattern". Reject picks > 6 unless
#   the student can defend them with the curve.
# - **Leakage question (Reflection 1):** the median summarizes the
#   *typical* day, which is knowable before any bad day happens; Max AQI
#   is itself the worst day of the year — it is the label in disguise.
