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
# # Lab 0.1 — Course Environment and Data Tour  *(SOLUTION / instructor copy)*
#
# *Course 1258 — Applied AI for Government IT Professionals · Ch00 Course
# Launch and Lab Environment · 20 minutes · CloudShare VM (JupyterLab) ·
# OpenAI API via the course helpers (canned fallback when no key)*

# %% [markdown]
# ## Objectives
#
# By the end of this lab, you will:
#
# - Navigate JupyterLab confidently: cells, run order, kernel restart.
# - Confirm the six shipped datasets load, and know what each one is for.
# - Make one successful call to the OpenAI API using the key from `.env`.

# %% [markdown]
# ## Setup
#
# - **Datasets:** all six course datasets in `data/` (provenance in
#   `data/MANIFEST.json`); this lab touches `federal_ai_use_cases.csv` and
#   `chicago_311.csv` directly.
# - **API key:** the course helpers load `OPENAI_API_KEY` from the
#   environment or the course `.env` — never printed. No key → canned reply.
# - Instructor copies live in `solutions/`, one level below `labs/` — the
#   first cell finds `labs/` (where `lab_common.py` / `lab_helpers.py` and
#   `data/` are) and runs from there.

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
# ## Steps
#
# 1. **(1 min)** Open the notebook.
# 2. **(3 min)** Run the **environment** cell — prints the `.env` path and
#    model alias, never the key.
# 3. **(3 min)** Run the **data inventory** cell — each dataset with row
#    count and description.
# 4. **(3 min)** Load the federal AI use case inventory; shape and columns.
# 5. **(2 min)** Count the `is_high_impact` use cases.
# 6. **(3 min)** Five most common `sr_type` values in `chicago_311.csv`.
# 7. **(3 min)** First API call: reply + token counts.
# 8. **(2 min)** Break it on purpose: restart kernel, re-run the last cell,
#    read the error, Run All to recover.

# %% [markdown]
# ### Step 2 — The environment cell

# %%
tour_environment()

# %% [markdown]
# ### Step 3 — Data inventory

# %%
tour_data_inventory()

# %% [markdown]
# ### Step 4 — Load the federal AI use case inventory

# %%
uc = load_use_cases()

# %% [markdown]
# ### Step 5 — How many use cases are flagged high-impact?
#
# **Expected answer:** 143 flagged `High-impact` (of 1,200 rows). Point out the
# third value — `Presumed High-Impact, but Not High-impact` (79) — a genuinely
# confusing label worth 30 seconds of class discussion: it means the use case
# matched the OMB checklist on paper but the agency determined it was not
# actually high-impact. And 223 rows leave the question blank.

# %%
count_high_impact(uc)

# %% [markdown]
# ### Step 6 — Chicago 311: the five most common request types
#
# **Expected answer:** Aircraft Noise Complaint dominates (~1,547 of 4,000) —
# an automated feed, not residents typing complaints. That single observation
# previews Lab 1.2's clustering story.

# %%
top_311_requests()

# %% [markdown]
# ### Step 7 — Your first API call

# %%
first_api_call()

# %% [markdown]
# ### Step 8 — Break it on purpose
#
# Instructor notes for the restart exercise:
# - The `NameError: name 'kernel_state_check' is not defined` is the *point*:
#   kernel state is not saved with the notebook, only code and outputs are.
# - If a student's Run All fails partway, it is almost always a cell they
#   edited out of order — re-run from the top.
# - Worth saying aloud: "Restart & Run All" is the notebook equivalent of
#   a clean build. Do it before you trust any output.

# %%
kernel_state_check(uc)

# %% [markdown]
# ## Deliverable
#
# A fully run notebook with the inventory, the high-impact count (143), the
# top-5 request types, and the model reply + token counts (or the offline
# note).

# %% [markdown]
# ## Reflection (expected answers)
#
# 1. Kernel restart wipes all variables and loaded helpers; the last cell
#    referenced names defined by earlier cells that had not re-run yet.
# 2. `federal_ai_use_cases.csv` — filter `topic_area` / search `use_case_name`
#    and `problem_solved` for document processing (Lab 1.1 does exactly this).
# 3. A one-sentence exchange is ~40 tokens; at published per-1K-token prices
#    that is fractions of a cent per call — but 50,000 documents a month
#    (Lab 7.1's scenario) turns fractions into a budget line.

# %% [markdown]
# ## Debrief (instructor-led)
#
# - Show of hands: who hit the `NameError` in Step 8 before Run All fixed it?
#   Kernel state lives in memory, not in the file.
# - Discuss the `Presumed High-Impact, but Not High-impact` label (Step 5
#   notes) — real government data has labels like this.
# - One minute on token counts: ~40 tokens a sentence; what does a
#   50,000-document month do to that? (Preview of Lab 7.1.)

# %% [markdown]
# ## Troubleshooting
#
# - **`NameError: name 'kernel_state_check' is not defined`.** Kernel restart /
#   out-of-order run — Run All.
# - **Canned reply in Step 7.** No key configured — expected off the VM; on
#   the VM, have the student tell you so the key injection can be fixed.
# - **Slow inventory cell.** It reads all six CSVs end to end — 20–30 seconds
#   on the VM is normal.
