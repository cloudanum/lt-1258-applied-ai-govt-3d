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
# # Lab 1.1 — Exploring the Federal AI Use Case Inventory
#
# *Course 1258 — Applied AI for Government IT Professionals · Ch01 AI and ML
# Foundations for Government · 30 minutes · CloudShare VM (JupyterLab) ·
# pandas only — no API key needed*
#
# You have been asked to brief your CIO on what other agencies are actually
# doing with AI. The OMB inventory is public and sitting on your VM. No AI is
# needed for this lab — this is the data literacy underneath it.

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
# - **Datasets:** `data/federal_ai_use_cases.csv` (the individually-reported
#   portion of OMB's 2025 Federal Agency AI Use Case Inventory — capped
#   extract) and `data/federal_ai_cots.csv` (its commercial off-the-shelf
#   companion). Provenance in `data/MANIFEST.json`.
# - **No API key is needed** — this lab never calls a model.
# - **The one rule that never changes:** public or synthetic data only.
# - **How this notebook works:** every step is one provided cell — run it with
#   Shift+Enter and read what it prints. Cells marked `# YOUR TURN` ask you to
#   change a simple value and re-run the cell. Everything runs as shipped, so
#   you can never get stuck.

# %%
# ▶ Setup — run this cell first (click it, then Shift+Enter).
# It loads the course helper functions used by every step below.
from lab_helpers import *

# %% [markdown]
# ## Steps
#
# 1. **(3 min)** Run the setup cell above, then load the inventory.
# 2. **(3 min)** Print the shape and columns. How many use cases, how many
#    agencies?
# 3. **(4 min)** Produce the top 10 agencies by use-case count.
# 4. **(4 min)** Break the inventory down by development stage. What share is
#    actually in production?
# 5. **(4 min)** Which agencies report the most high-impact AI?
# 6. **(4 min)** Cross-tabulate `topic_area` against `development_stage` and
#    read one row aloud.
# 7. **(4 min)** Which commercial tools appear most often?
# 8. **(4 min)** Write three findings in the notebook, each with the step that
#    produced it.

# %% [markdown]
# ### Step 1 — Load the inventory (provided)
#
# Run this cell. It loads `data/federal_ai_use_cases.csv` — the
# individually-reported portion of OMB's 2025 inventory (capped extract — see
# `data/MANIFEST.json` for provenance).

# %%
uc = load_ai_inventory()

# %% [markdown]
# ### Step 2 — First look: shape, columns, agencies (provided)
#
# Run this cell to print the shape and columns. **How many use cases, and how
# many agencies?**

# %%
inventory_overview(uc)

# %% [markdown]
# ### Step 3 — Top 10 agencies by use-case count
#
# Run this cell to rank agencies by how many use cases they reported. Then
# change `TOP_N` below and re-run — what changes?

# %%
TOP_N = 10   # ← YOUR TURN: how many agencies to show — try 3 or 20, then re-run this cell
top_ai_agencies(uc, top_n=TOP_N)

# %% [markdown]
# ### Step 4 — What share is actually in production? (provided)
#
# Run this cell to break the inventory down by `development_stage`. What share
# of use cases is `Deployed`? The cell prints the share two ways — blanks
# excluded, and blanks counted in the total. Decide for yourself which you
# would quote — and be ready to defend it.

# %%
show_deployed_share(uc)

# %% [markdown]
# ### Step 5 — Who reports the most high-impact AI? (provided)
#
# Run this cell to keep only the rows flagged `is_high_impact == "High-impact"`
# and rank agencies. (Lab 0.1 already showed this column has more than two
# values — the cell filters deliberately, it does not just count non-blanks.)

# %%
high_impact_agencies(uc)

# %% [markdown]
# ### Step 6 — Topic area × development stage (provided)
#
# Run this cell to cross-tabulate `topic_area` against `development_stage`,
# then read one row aloud to your neighbour: what does it tell you about where
# that topic's AI actually is?

# %%
topic_stage_crosstab(uc)

# %% [markdown]
# ### Step 7 — The commercial tools underneath (provided)
#
# `federal_ai_cots.csv` is the companion file: consolidated commercial
# off-the-shelf AI use. Run this cell to see which commercial products appear
# most often. Notice the near-duplicates in the product names while you read —
# a preview of Lab 6.2.

# %%
top_commercial_tools()

# %% [markdown]
# ### Step 8 — Three findings, each with the step that produced it
#
# Write three findings for your CIO in the markdown cell below. Each must be
# one sentence *plus* the step above that produced the number. A finding is
# something a decision-maker could act on, not a restated table.

# %% [markdown]
# **Your findings (write here):**
#
# 1.
# 2.
# 3.

# %% [markdown]
# ## Deliverable
#
# 1. The top-10 agency table, the deployed share, the high-impact ranking.
# 2. The topic × stage cross-tab with one row read aloud.
# 3. Your three findings, each with the step that produced it.

# %% [markdown]
# ## Reflection
#
# 1. Which single number would most change your CIO's mind?
# 2. What does this dataset *not* tell you about how well any of it works?
# 3. Where would a chart have been clearer than a table?

# %% [markdown]
# ## Debrief (instructor-led)
#
# - Compare deployed shares across the room: who included the 223 blanks in
#   the denominator, who excluded them, and who can defend their choice? Both
#   are defensible if stated — the blanks themselves are a finding about the
#   inventory's completeness.
# - Contrast the two rankings on the board: most AI by volume vs most
#   *high-impact* AI. They are not the same agencies — which number belongs in
#   the CIO briefing?
# - Only six agencies appear in this capped extract (the full inventory is
#   56). Ask what the cap does to any "top 10" claim before anyone quotes one.

# %% [markdown]
# ## Troubleshooting
#
# - **A red error mentioning a data file.** The course data pack is incomplete
#   — tell your instructor; run the Day-0 healthcheck to confirm.
# - **The counts in a step don't add up to the row count.** Blank values are
#   left out of most counts by default — Step 4's table shows them as `NaN`.
# - **Your numbers differ from your neighbour's.** Check you are both on the
#   same shipped extract; this file is capped (see `data/MANIFEST.json`), not
#   the full 56-agency inventory.
# - **Out-of-order errors after experimenting.** Kernel → Restart & Run All.

# %% [markdown]
# ---
# *Curious about the Python behind these steps? The full code-forward version
# of this lab lives in the `For_Python_Programmers/` folder.*
