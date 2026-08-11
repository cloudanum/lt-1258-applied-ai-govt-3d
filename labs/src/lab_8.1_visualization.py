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
# # Lab 8.1 — Visualization and Reporting from EPA Data
#
# *Chapter 8 — AI Operations and Reporting in Government · 30 minutes · JupyterLab + pandas/matplotlib (no API key needed)*
#
# A deputy director asks: which counties have the worst air quality, is it
# getting better, and where should we focus? Answer in one page.
#
# Cells marked `# YOUR TURN` ask you to change a simple value and re-run —
# everything runs as shipped, so you can never get stuck.

# %% [markdown]
# ## Objectives
#
# By the end of this lab, you will:
#
# - Build charts that answer a stated question.
# - Apply the visualization guidelines deliberately.
# - Turn three charts into a one-page briefing.

# %% [markdown]
# ## Setup
#
# - **Data:** `data/epa_aqi_by_county.csv` — EPA Annual Air Quality Index by
#   county, 2024 (public data; see `data/MANIFEST.json` for the source URL).
#   Course rule: public or synthetic data only.
# - **Tools:** pandas + matplotlib only — this lab needs no API key.
# - **Output:** the one-page briefing is saved to `epa_briefing.png` in Step 7.
# - **How this notebook works:** every step is one provided cell — run it with
#   Shift+Enter and read what it prints (or look at the chart it draws).
#   Cells marked `# YOUR TURN` ask you to change a simple value (like which
#   state to chart) and re-run the cell.

# %%
# ▶ Setup — run this cell first (click it, then Shift+Enter).
# It loads the course helper functions used by every step below.
from lab_helpers import *

# %% [markdown]
# ## Steps
#
# ### Step 1 — Load the EPA file (2 min, provided)
#
# One row per county per year. The load adds `unhealthy_total` = Unhealthy +
# Very Unhealthy + Hazardous days — the exposure the deputy director cares
# about. Run this cell.

# %%
epa = load_epa_county_data()

# %% [markdown]
# ### Step 2 — Chart 1: the 15 worst counties (5 min, provided)
#
# Question: *which counties have the worst air quality?* Run this cell to
# rank counties by unhealthy-day count and chart the top 15 as a horizontal
# bar chart — sorted, labelled, no decoration.

# %%
top15 = plot_worst_counties(epa)

# %% [markdown]
# ### Finding 1 (three sentences, write here)
#
# -
# -
# -

# %% [markdown]
# ### Step 3 — Chart 2: the distribution of Median AQI (4 min, provided)
#
# Question: *is bad air a national condition or a local one?* Run this cell
# to chart the distribution of `Median AQI` across all 997 counties, with the
# Good/Moderate boundary (AQI 50) marked.

# %%
plot_aqi_distribution(epa)

# %% [markdown]
# ### Finding 2 (three sentences, write here)
#
# -
# -
# -

# %% [markdown]
# ### Step 4 — Chart 3: one state against the national median (5 min)
#
# Question: *how does California compare?* Run this cell to chart each
# California county's `Median AQI` against the national median. (California
# has the most counties in the file; swap in your own state if you prefer.)

# %%
STATE = "California"   # ← YOUR TURN: swap in your own state (spell it exactly as in the data) and re-run this cell
state_chart = plot_state_comparison(epa, STATE)

# %% [markdown]
# ### Finding 3 (three sentences, write here)
#
# -
# -
# -

# %% [markdown]
# ### Step 5 — The guideline checklist (4 min)
#
# Before assembling the page, audit your three charts against the course
# guidelines and fix what fails:
#
# - [ ] Bars sorted by value (not alphabetically, not arbitrarily)
# - [ ] Axes labelled with units; title states the question or the answer
# - [ ] No chartjunk: no 3-D, no gradients, no gridline noise, no legend for
#       a single series
# - [ ] Honest scale: bar charts start at zero; any truncation is flagged in
#       the title

# %% [markdown]
# ### Step 6 — Three-sentence findings (5 min)
#
# You drafted Finding 1–3 as you went. Revisit them now with the checklist in
# hand: each finding should say what the chart shows, why it matters, and what
# it does *not* show.

# %% [markdown]
# ### Step 7 — Assemble the one-page briefing (5 min, provided)
#
# Question, three charts, recommendation — one figure, saved to
# `epa_briefing.png`. Run this cell to stack your three charts into the page.

# %%
assemble_briefing_page(epa, top15, state_chart)

# %% [markdown]
# ### Recommendation (write here — one sentence the deputy director can act on)
#
# -

# %% [markdown]
# ## Deliverable
#
# 1. Three charts, each with its three-sentence finding.
# 2. The completed guideline checklist.
# 3. `epa_briefing.png` with your one-sentence recommendation.

# %% [markdown]
# ## Reflection
#
# 1. Which chart would survive being screenshotted without its caption?
# 2. What did sorting change about the reader's conclusion?
# 3. What did you choose *not* to plot, and why?

# %% [markdown]
# ## Debrief (instructor-led)
#
# 1. Which chart would you hand a reporter, and which an inspector general?
#    What changes between the two?
# 2. The one-pager answers "where should we focus" — what does it deliberately
#    leave out, and who might object?
# 3. If this briefing ran every month, what would you automate — and what must
#    stay human?

# %% [markdown]
# ## Troubleshooting
#
# - **The state chart's county labels are hard to read.** Expected — they are
#   printed small and sideways so a whole state fits; a state with many
#   counties will always be crowded.
# - **`epa_briefing.png` is blank or missing.** Re-run Step 7 — the briefing
#   cell saves the file first, then shows it. If it is still missing, Kernel
#   → Restart & Run All.
# - **A red error mentioning `Median AQI` or `unhealthy_total`.** Step 1 was
#   not run — run the notebook in order (Kernel → Restart & Run All).
# - **The state chart says no counties were found.** The state name does not
#   match the data — check the spelling (and capitalization) against the
#   preview in Step 1.
# - **A red error mentioning `epa_aqi_by_county.csv` or "No such file".** The
#   course data pack is missing or incomplete — tell your instructor; run the
#   Day-0 healthcheck to confirm.

# %% [markdown]
# ---
# *Curious about the Python behind these steps? The full code-forward version
# of this lab lives in the `For_Python_Programmers/` folder.*
