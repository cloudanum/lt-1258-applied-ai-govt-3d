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
# # Lab 6.2 — GenAI-Assisted Cleaning with Structured Outputs  *(SOLUTION / instructor copy)*
#
# **Chapter 6 — Data for AI: Collection, Quality, and Governance** · 35 minutes
#
# **Objectives**
# 1. Use a model to normalise messy categorical data at volume.
# 2. Enforce a schema so the output is machine-usable.
# 3. Audit the model's work and measure what it got wrong.

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
# ## Step 1 — Extract 60 raw values

# %%
raw_values = extract_messy_labels()

# %% [markdown]
# ## Step 2 — Call the model with a strict JSON schema
#
# **Worked prompt** below. Offline, the canned mapping plays the model's
# part — including its characteristic mistake (next steps).

# %%
MAPPING_PROMPT = """You are normalizing Chicago 311 request-type labels into a controlled vocabulary for a city dashboard.
VOCABULARY: Noise, Information & 311 Services, Water & Drainage, Urban Forestry, Graffiti & Property Damage, Streets & Transportation, Sanitation & Waste, Pest & Animal Control, Buildings & Housing, Code Enforcement & Violations, Other.
Return JSON only: {"mappings": [{"raw": ..., "canonical": ..., "confidence": 0-1}, ...]} with exactly one object per input value. If no category fits well, use "Other" with confidence <= 0.5 rather than forcing a fit."""

mapped = clean_labels_with_ai(raw_values, MAPPING_PROMPT)

# %% [markdown]
# ## Step 3 — Fail loudly if it does not validate

# %%
validate_cleaning(mapped)

# %% [markdown]
# ## Step 4 — Audit: sample 20 and check by hand
#
# **Expected errors in this sample (seed 7):** `Sanitation Code Violation`
# is the systematic one — mapped to *Sanitation & Waste* at 0.9 confidence
# when it is a code-enforcement action. Depending on the draw, students may
# also flag `Water Lead Test Kit Request` (a health-testing programme, not
# drainage) and `Finance Parking Code Enforcement Review` (revenue
# enforcement, not transportation). Expected error rate: **1–3 of 20
# (5–15%)**.

# %%
audit_sample = show_cleaning_sample(mapped)

# %%
ERRORS_FOUND = count_audit_errors(audit_sample)
show_error_rate(ERRORS_FOUND, detail=True)

# %% [markdown]
# ## Step 5 — The high-confidence wrong mapping
#
# **Expected pick:** `Sanitation Code Violation -> Sanitation & Waste`,
# confidence 0.9. The word "Sanitation" is a *department name*, not a service
# description — the model matched the surface token and never saw the
# enforcement semantics. This is the canonical GenAI-cleaning failure mode:
# the label is lexically close to the wrong category and the model's
# confidence reflects lexical match strength, not judgement.

# %%
show_confident_mappings(mapped, highlight="Sanitation Code Violation")

# %% [markdown]
# ## Step 6 — Tighten the prompt, re-run the failures
#
# **Expected:** all five 'Violation' labels move to
# `Code Enforcement & Violations`. One sentence of domain knowledge fixed a
# whole error class — cheaper than more data, faster than a bigger model.
# And the audit question repeats: did the fix break anything that was right?
# (Re-run the validator and eyeball the full table again — it did not.)

# %%
TIGHTENER = ("\nIMPORTANT: distinguish service delivery from enforcement — "
             "labels containing 'Violation' are code-enforcement actions "
             "(Code Enforcement & Violations), not service requests, even "
             "when the enforcing department sounds like a service (e.g. "
             "Sanitation).")

rerun_with_tighter_prompt(mapped, MAPPING_PROMPT, TIGHTENER, check=True)

# %% [markdown]
# ## Step 7 — Human-review rule (worked)
#
# "Route to human review: (a) every mapping with confidence < 0.8, (b) 100%
# of mappings for any *new* vocabulary category in its first month, and (c)
# a 5% random audit of the remainder — with the measured 5–15% base error
# rate, unaudited automation is not defensible for anything feeding a public
# dashboard."
#
# ## Reflection (expected answers)
# 1. For a public dashboard: near zero on high-volume categories — and the
#    decision belongs to the data owner and the accountability chain (the
#    official who signs the dashboard), not the person who wrote the prompt.
# 2. Weakly — confidence tracks lexical match strength, so the most
#    dangerous errors are the *confident* ones (Sanitation Code Violation at
#    0.9). Confidence is useful for triage order, not for trust.
# 3. GenAI cannot fix missing values (the 100%-null columns), cannot detect
#    duplicates, and cannot judge accuracy against the real world — those
#    need collection changes, keys, and audits respectively.
