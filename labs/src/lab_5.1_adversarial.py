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
# # Lab 5.1 — Adversarial Examples and Model Robustness
#
# *Chapter 5 — AI Security, Risks, and Responsible AI · 40 minutes (flex —
# your instructor may skip this) · JupyterLab with pandas, scikit-learn and
# matplotlib — no API key needed*
#
# You are testing a classifier before it goes anywhere near a decision. Your
# job is to break it on purpose, in a sandbox, and report honestly.
#
# Cells marked `# YOUR TURN` ask you to change a simple value and re-run.
# No API key is needed.

# %% [markdown]
# ## Objectives
#
# By the end of this lab, you will:
#
# - Craft inputs that flip a model's prediction.
# - Measure how much perturbation it actually takes.
# - Name the defences that would have helped.

# %% [markdown]
# ## Setup
#
# **Datasets and files** (all under `labs/data/`):
#
# - `epa_aqi_by_county.csv` — EPA Annual Air Quality Index by county, 2024
#   (real, public; see `data/MANIFEST.json`)
#
# **Tools:** pandas, scikit-learn (logistic regression), matplotlib. This lab
# is fully self-contained — no OpenAI key is required.
#
# **Data rule:** the dataset is genuinely public US government data. The
# attack you build runs against a throwaway model in this sandbox — never
# point these techniques at a system you do not own.
#
# **How this notebook works:** every step is one provided cell — run it with
# Shift+Enter and read what it prints. Cells marked `# YOUR TURN` ask you to
# change a simple value (like which sample county to attack) and re-run the
# cell. Everything runs as shipped, so you can never get stuck.

# %%
# ▶ Setup — run this cell first (click it, then Shift+Enter).
# It loads the course helper functions used by every step below.
from lab_helpers import *

# %% [markdown]
# ## Steps
#
# 1. Train the small classifier provided. (6 min)
# 2. Record its baseline accuracy on the held-out set. (5 min)
# 3. Perturb one feature at a time and find the smallest change that flips a
#    prediction. (8 min)
# 4. Plot flip rate against perturbation size. (8 min)
# 5. Apply one defence from the chapter and re-measure. (8 min)
# 6. Write what you would tell a system owner in three sentences. (5 min)

# %% [markdown]
# ### Step 1 — Train the small classifier (6 min, provided)
#
# The model: predict whether a county had **any** Unhealthy-or-worse air days
# in 2024 (`poor_air`), from its day-count profile. A logistic regression —
# small, inspectable, and easy to attack honestly. Run this cell to load the
# data and train it.

# %%
model = train_air_risk_model()

# %% [markdown]
# ### Step 2 — Baseline accuracy (5 min, provided)
#
# Run this cell to record the model's accuracy on the held-out set *before*
# anyone attacks it. Also read the coefficients: which feature does the model
# trust most?

# %%
show_baseline_accuracy(model)

# %% [markdown]
# ### Step 3 — The smallest change that flips one prediction (8 min)
#
# This cell takes one correctly-classified county and perturbs **one feature
# at a time** — how many extra `Unhealthy for Sensitive Groups Days` does it
# take before the model changes its mind? (This is FGSM's question, asked of
# a model simple enough that you can watch it happen.) Run it, then try
# another county by changing `SAMPLE_ROW`.

# %%
SAMPLE_ROW = 5   # ← YOUR TURN: pick another test county (0, 1, 2, …) and see if it breaks as easily, then re-run this cell
find_smallest_flip(model, SAMPLE_ROW)

# %% [markdown]
# ### Step 4 — Flip rate vs. perturbation size (8 min, provided)
#
# One flip is an anecdote; a rate is a measurement. Run this cell: for every
# test county it pushes the most sensitive feature by ε (up for clean
# counties, down for poor-air ones — the direction that aims at the wrong
# answer) and counts how many flip, then plots the curve.

# %%
rates = attack_strength_sweep(model)

# %% [markdown]
# ### Step 5 — Apply one defence and re-measure (8 min, provided)
#
# Defence: **adversarial retraining**. Run this cell — it augments the
# training set with perturbed copies that keep their *true* labels, retrains,
# and re-runs the same attack. The model learns that "a few extra USG days"
# is not, by itself, the signal.

# %%
retrain_with_defence(model, rates)

# %% [markdown]
# ### Step 6 — Three sentences to the system owner (5 min, write here)
#
# *How breakable the model is, what it costs to break it, and what you did
# about it:*
#
# -
# -
# -

# %% [markdown]
# ## Deliverable
# 1. Baseline accuracy and the smallest successful perturbation.
# 2. The flip-rate curve.
# 3. Before/after flip rates under your defence.
# 4. Your three sentences to the system owner.

# %% [markdown]
# ## Reflection
# 1. How small was the smallest successful perturbation?
# 2. Would the defence have survived an attacker who *knew about it*?
# 3. Which MITRE ATLAS tactic does this exercise correspond to?

# %% [markdown]
# ## Debrief (instructor-led)
#
# - **Compare smallest flips.** How many days did it take around the room?
#   What does a "small" perturbation mean when the unit is days of bad air?
# - **Defence economics.** Adversarial retraining cost you nothing but
#   compute — why isn't it done by default? What attack would defeat it?
# - **ATLAS mapping.** Which MITRE ATLAS tactic did you just execute, and
#   where in your agency's ML lifecycle would you run this exercise?

# %% [markdown]
# ## Troubleshooting
#
# - **A red error mentioning `epa_aqi_by_county.csv` or "No such file".** The
#   course data pack is missing or incomplete — tell your instructor; run the
#   Day-0 healthcheck to confirm.
# - **A `ConvergenceWarning` appears.** Harmless here; the model is tiny and
#   the features are scaled, so the fit has already converged well enough.
# - **The plot is empty or missing.** Run the cells in order — Kernel →
#   Restart & Run All.
# - **Step 3 says no flip was found.** With the shipped value that cannot
#   happen; if you changed `SAMPLE_ROW`, that county may simply be harder to
#   flip — try another number, or put `SAMPLE_ROW` back to 5.
# - **Numbers differ from a neighbour's.** They should not — the train/test
#   split is seeded, so everyone gets the same counties. A difference means a
#   value was edited or a cell was run out of order — Kernel → Restart & Run
#   All.

# %% [markdown]
# ---
# *Curious about the Python behind these steps? The full code-forward version
# of this lab lives in the `For_Python_Programmers/` folder.*
