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
# # Lab 1.1 — Exploring the Federal AI Use Case Inventory  *(SOLUTION / instructor copy)*
#
# *Course 1258 — Applied AI for Government IT Professionals · Ch01 AI and ML
# Foundations for Government · 30 minutes · CloudShare VM (JupyterLab) ·
# pandas only — no API key needed*

# %% [markdown]
# ## Objectives
#
# By the end of this lab, you will:
#
# - Load, filter, group and summarise a real federal dataset.
# - Answer substantive questions about federal AI adoption from evidence.
# - Practise the analysis habits every later lab depends on.

# %% [markdown]
# ## Setup
#
# - **Datasets:** `data/federal_ai_use_cases.csv` (capped extract of OMB's
#   2025 inventory) and `data/federal_ai_cots.csv`. Provenance in
#   `data/MANIFEST.json`.
# - **Tools:** pandas only — no API key needed.
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
# 1. **(3 min)** Run the setup cell, then load the inventory.
# 2. **(3 min)** Shape and columns — how many use cases, how many agencies?
# 3. **(4 min)** Top 10 agencies by use-case count.
# 4. **(4 min)** Share actually in production (`development_stage`).
# 5. **(4 min)** Most high-impact AI by agency.
# 6. **(4 min)** `topic_area` × `development_stage` cross-tab; read a row
#    aloud.
# 7. **(4 min)** COTS file — most common commercial tools.
# 8. **(4 min)** Three findings, each with the step that produced it.

# %% [markdown]
# ### Step 1 — Load the inventory

# %%
uc = load_ai_inventory()

# %% [markdown]
# ### Step 2 — First look: shape, columns, agencies
#
# **Expected:** 1,200 rows × 36 columns, 6 agencies. The full OMB inventory is
# 3,611 use cases across 56 agencies; this extract is capped (see MANIFEST) —
# worth saying so no one over-generalizes from six agencies.

# %%
inventory_overview(uc)

# %% [markdown]
# ### Step 3 — Top 10 agencies by use-case count
#
# **Expected:** DoE (340), Interior (247), DHS (238), Commerce (223), DoJ
# (149), CFTC (3). Only six agencies in this capped extract, so the "top 10"
# is a top 6 — a good moment to ask what the file's cap does to any ranking.

# %%
TOP_N = 10   # how many agencies to show
top_ai_agencies(uc, top_n=TOP_N)

# %% [markdown]
# ### Step 4 — What share is actually in production?
#
# **Expected:** 347 Deployed of 977 non-blank = **35.5%** (28.9% if the 223
# blanks are counted in the denominator — either is defensible if stated).
# The 223 blank stage values are themselves a finding: the inventory's
# completeness problem.

# %%
show_deployed_share(uc)

# %% [markdown]
# ### Step 5 — Who reports the most high-impact AI?
#
# **Expected:** DoJ 59, DHS 55, DoE 29 (143 total). The ranking flips the
# volume ranking — DoE reports the most AI; DoJ and DHS report the most
# *consequential* AI. That contrast is the CIO headline.

# %%
high_impact_agencies(uc)

# %% [markdown]
# ### Step 6 — Topic area × development stage
#
# **Expected read:** Science leads in volume (254) but most of it is
# pre-deployment; IT is the most *operational* topic (66 deployed vs 39
# pre-deployment). Reading one row aloud forces the "so what".

# %%
topic_stage_crosstab(uc)

# %% [markdown]
# ### Step 7 — The commercial tools underneath
#
# **Expected:** Microsoft Copilot variants dominate — and they are split across
# `Microsoft Copilot` (51), `Microsoft M365 Copilot AI` (20), `M365 Copilot`
# (10). The fragmented labels understate the true leader: a real preview of
# the canonicalization problem Lab 6.2 fixes with GenAI.

# %%
top_commercial_tools()

# %% [markdown]
# ### Step 8 — Three findings (worked examples)
#
# 1. **Only about a third of reported federal AI is actually deployed** —
#    347 of 977 non-blank stage values say `Deployed`.
#    (Step 4 — `show_deployed_share(uc)`)
# 2. **The highest-volume agency is not the highest-stakes one** — DoE leads
#    on count (340) but DoJ and DHS lead on high-impact systems (59 and 55).
#    (Steps 3 and 5 — `top_ai_agencies(uc)` and `high_impact_agencies(uc)`)
# 3. **One vendor's assistant dominates the commercial layer under three
#    different names** — Copilot variants appear in 96 of 900 COTS rows.
#    (Step 7 — `top_commercial_tools()`)

# %% [markdown]
# ## Deliverable
#
# 1. The top-10 agency table, the deployed share, the high-impact ranking.
# 2. The topic × stage cross-tab with one row read aloud.
# 3. Three findings, each with the step that produced it.

# %% [markdown]
# ## Reflection (expected answers)
#
# 1. Defensible answers: the 35.5% deployed share (ambition vs reality) or the
#    DoJ/DHS high-impact lead (where the risk management budget should go).
# 2. Nothing about performance, accuracy, uptake, or outcomes — the inventory
#    records existence and intent, not results.
# 3. The topic × stage cross-tab and the high-impact ranking both compress
#    better as sorted bar charts — that is Lab 8.1's job.

# %% [markdown]
# ## Debrief (instructor-led)
#
# - Compare deployed-share denominators across the room (Step 4 notes): both
#   answers defensible if stated; the 223 blanks are themselves a finding.
# - Board the two rankings side by side — volume vs high-impact — and ask
#   which number belongs in the CIO briefing.
# - Remind the room this extract shows 6 of 56 agencies; ask what the cap
#   does to any "top 10" claim before it gets quoted.

# %% [markdown]
# ## Troubleshooting
#
# - **A red error mentioning a data file.** The data pack is incomplete — have
#   the student run the Day-0 healthcheck and flag it to you.
# - **Counts don't add to the row total.** Blanks are left out of most counts
#   by default — Step 4's table shows them as `NaN`.
# - **Numbers differ from a neighbour's.** Same shipped extract? It is capped
#   (see `data/MANIFEST.json`), not the full inventory.
# - **Out-of-order errors.** Kernel → Restart & Run All.
