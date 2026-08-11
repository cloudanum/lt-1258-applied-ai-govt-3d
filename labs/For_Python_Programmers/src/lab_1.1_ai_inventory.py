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
# - Load, filter, group and summarise a real federal dataset with pandas.
# - Answer substantive questions about federal AI adoption from evidence.
# - Practise the analysis habits every later lab depends on.

# %% [markdown]
# ## Setup
#
# - **Datasets:** `data/federal_ai_use_cases.csv` (the individually-reported
#   portion of OMB's 2025 Federal Agency AI Use Case Inventory — capped
#   extract) and `data/federal_ai_cots.csv` (its commercial off-the-shelf
#   companion). Provenance in `data/MANIFEST.json`.
# - **Tools:** pandas. Run from the `labs/` folder (the VM's **Start Labs**
#   shortcut puts you there); both files load with `encoding="utf-8-sig"`.
# - **No API key is needed** — this lab never calls a model.
# - **The one rule that never changes:** public or synthetic data only.
# - Cells marked `# YOUR CODE` are for you to complete. Each has a reference
#   fallback that runs if you leave it blank — replace it with your own line
#   when you can.

# %% [markdown]
# ## Steps
#
# 1. **(3 min)** Open `lab_1.1_ai_inventory.ipynb` and run the setup cell.
# 2. **(3 min)** Print the shape and columns. How many use cases, how many
#    agencies?
# 3. **(4 min)** Group by `agency_name` and produce the top 10 agencies by
#    use-case count.
# 4. **(4 min)** Group by `development_stage`. What share is actually in
#    production?
# 5. **(4 min)** Filter `is_high_impact`. Which agencies report the most
#    high-impact AI?
# 6. **(4 min)** Cross-tabulate `topic_area` against `development_stage` and
#    read one row aloud.
# 7. **(4 min)** Join the COTS file. Which commercial tools appear most often?
# 8. **(4 min)** Write three findings in the notebook, each with the line of
#    code that produced it.

# %% [markdown]
# ### Step 1 — Setup and load
#
# Run this cell. It imports pandas and loads
# `data/federal_ai_use_cases.csv` — the individually-reported portion of OMB's
# 2025 inventory (capped extract — see `data/MANIFEST.json` for provenance).

# %%
import pandas as pd

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 40)

uc = None
# YOUR CODE: load data/federal_ai_use_cases.csv into `uc` with pd.read_csv
# (use encoding="utf-8-sig" — the file starts with a byte-order mark).

if uc is None:
    uc = pd.read_csv("data/federal_ai_use_cases.csv", encoding="utf-8-sig")
    print("(reference load applied — replace with your own line above)")

# %% [markdown]
# ### Step 2 — First look: shape, columns, agencies
#
# Print the shape and columns. **How many use cases, and how many agencies?**

# %%
print("shape:", uc.shape, "| agencies:", uc["agency_name"].nunique())
print("columns:", list(uc.columns))

# %% [markdown]
# ### Step 3 — Top 10 agencies by use-case count
#
# Group by `agency_name` and produce the ten agencies reporting the most use
# cases.

# %%
top_agencies = None
# YOUR CODE: value_counts (or groupby().size()) on agency_name, top 10.

if top_agencies is None:
    top_agencies = uc["agency_name"].value_counts().head(10)
    print("(reference answer applied)\n")
print(top_agencies.to_string())

# %% [markdown]
# ### Step 4 — What share is actually in production?
#
# Group by `development_stage`. What share of use cases is `Deployed`? Decide
# for yourself what to do with blank values — and be ready to defend it.

# %%
deployed_share = None
# YOUR CODE: the percentage of use cases with development_stage == "Deployed".
# (Hint: value_counts with dropna=False first, then decide your denominator.)

if deployed_share is None:
    stage = uc["development_stage"]
    deployed_share = round((stage == "Deployed").sum() / stage.notna().sum() * 100, 1)
    print("(reference answer applied — blanks excluded from the denominator)\n")
print(uc["development_stage"].value_counts(dropna=False).to_string())
print(f"\nDeployed share: {deployed_share}%")

# %% [markdown]
# ### Step 5 — Who reports the most high-impact AI?
#
# Filter to rows flagged `is_high_impact == "High-impact"` and rank agencies.
# (Lab 0.1 already showed this column has more than two values — filter
# deliberately, don't just count non-blanks.)

# %%
high_impact_by_agency = None
# YOUR CODE: filter to High-impact rows, then rank agencies by count.

if high_impact_by_agency is None:
    high_impact_by_agency = (uc[uc["is_high_impact"] == "High-impact"]
                             ["agency_name"].value_counts())
    print("(reference answer applied)\n")
print(high_impact_by_agency.to_string())

# %% [markdown]
# ### Step 6 — Topic area × development stage
#
# Cross-tabulate `topic_area` against `development_stage` and read one row
# aloud to your neighbour: what does it tell you about where that topic's AI
# actually is?

# %%
xtab = None
# YOUR CODE: pd.crosstab(uc["topic_area"], uc["development_stage"])

if xtab is None:
    xtab = pd.crosstab(uc["topic_area"], uc["development_stage"])
    print("(reference answer applied)\n")
print(xtab.to_string())

# %% [markdown]
# ### Step 7 — The commercial tools underneath
#
# `federal_ai_cots.csv` is the companion file: consolidated commercial
# off-the-shelf AI use. Which commercial products appear most often? Notice the
# near-duplicates in the product names while you count — a preview of Lab 6.2.

# %%
top_tools = None
# YOUR CODE: load data/federal_ai_cots.csv (encoding="utf-8-sig") and count
# the 10 most frequent values of "Name of Commercial Product or Service Used".

if top_tools is None:
    cots = pd.read_csv("data/federal_ai_cots.csv", encoding="utf-8-sig")
    top_tools = (cots["Name of Commercial Product or Service Used"]
                 .value_counts().head(10))
    print("(reference answer applied)\n")
print(top_tools.to_string())

# %% [markdown]
# ### Step 8 — Three findings, each with the code that produced it
#
# Write three findings for your CIO in the markdown cell below. Each must be
# one sentence *plus* the line of code that produced the number. A finding is
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
# 3. Your three findings, each with its line of code.

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
# - **`FileNotFoundError: data/federal_ai_use_cases.csv`.** You are not running
#   from the `labs/` folder — close the notebook, open it from the file
#   browser in JupyterLab, and Run All.
# - **`KeyError: 'agency_name'` or a weird first column name.** The file's
#   byte-order mark got into the header — reload with `encoding="utf-8-sig"`.
# - **Your value counts don't add up to the row count.** Blank values are
#   dropped by default — use `value_counts(dropna=False)` to see them.
# - **Your numbers differ from your neighbour's.** Check you are both on the
#   same shipped extract; this file is capped (see `data/MANIFEST.json`), not
#   the full 56-agency inventory.
