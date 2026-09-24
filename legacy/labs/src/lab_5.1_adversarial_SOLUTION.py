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
# # Lab 5.1 — Adversarial Examples and Model Robustness  *(SOLUTION / instructor copy)*
#
# **Chapter 5 — AI Security, Risks, and Responsible AI** · 40 minutes *(flex)*
#
# **Objectives**
# 1. Craft inputs that flip a model's prediction.
# 2. Measure how much perturbation it actually takes.
# 3. Name the defences that would have helped.

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
# ## Step 1 — Train the small classifier

# %%
model = train_air_risk_model()

# %% [markdown]
# ## Step 2 — Baseline accuracy
#
# **Expected:** ~86.8%. The model leans hardest on
# `Unhealthy for Sensitive Groups Days` (coefficient ≈ +1.8) — which tells the
# attacker exactly where to push. Model transparency cuts both ways.

# %%
show_baseline_accuracy(model)

# %% [markdown]
# ## Step 3 — The smallest change that flips one prediction
#
# **Expected:** for the reference sample (a clean county), just **+19 USG
# days** flips it to "poor air" — the model never asks whether 19 extra days
# is plausible given the county's other counts. Smaller than students expect;
# that is the lesson.

# %%
SAMPLE_ROW = 5   # the reference sample
find_smallest_flip(model, SAMPLE_ROW)

# %% [markdown]
# ## Step 4 — Flip rate vs. perturbation size
#
# **Expected curve:** ~1% at ε=1, ~26% at ε=10, ~84% at ε=20, plateau ~85%.
# The remaining ~15% are counties whose other features dominate — no single-
# feature attack moves them. State it plainly: a 20-day edit flips five out
# of six predictions while baseline accuracy stays a marketing number.

# %%
rates = attack_strength_sweep(model)

# %% [markdown]
# ## Step 5 — Defence: adversarial retraining
#
# **Expected:** flip rate collapses to ~0% at every ε tested, with accuracy
# unchanged (~86.8%). Then the honest caveat: this defence covers *this*
# attack. An attacker who knows we retrained on USG-day perturbations will
# perturb `Good Days` downward or `Moderate Days` instead — re-measure and
# some flips return. Defence is a moving target, not a checkbox.
#
# (A second defence worth mentioning in debrief: a **consistency check** —
# day counts that sum above `Days with AQI` are physically impossible, so the
# application layer should reject them before the model ever sees them.)

# %%
retrain_with_defence(model, rates)

# %% [markdown]
# ### Three sentences to the system owner (worked)
#
# "Before any mitigation, editing a single input field by about twenty days
# flipped five out of six of the model's predictions while its headline
# accuracy stayed 87% — so accuracy alone is not evidence of robustness. We
# retrained the model on perturbed examples and the same attack now flips
# effectively nothing, at no cost to accuracy. The remaining exposure is an
# attacker who adapts to the defence, so input validation at the application
# layer and periodic re-testing need to be part of operating this model, not
# one-time fixes."
#
# ## Reflection (expected answers)
# 1. +19 days on one feature for the reference county — single-feature edits
#    in the tens, not thousands.
# 2. Not fully: retraining covers the attack it was shown. An adaptive
#    attacker perturbs a different feature (try it: `Good Days` downward) —
#    which is why red-teaming is iterative.
# 3. Evasion — crafting adversarial data to defeat a model at inference time
#    (ATLAS tactic AML.TA0015 *Evade ML Model*, technique family *Craft
#    Adversarial Data*).
