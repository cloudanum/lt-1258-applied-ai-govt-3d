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
# # Lab 8.2 — GenAI-Assisted Analysis and Briefing
#
# *Chapter 8 — AI Operations and Reporting in Government · 30 minutes (flex — your instructor may skip this) · JupyterLab + OpenAI API*
#
# Same deliverable as Lab 8.1, but with an assistant. The difference is the
# verification step, which is now yours.
#
# Cells marked `# YOUR TURN` ask you to edit the prompt text (or a pick) and
# re-run. Offline, every call returns a labelled canned answer, so the whole
# notebook always runs.

# %% [markdown]
# ## Objectives
#
# By the end of this lab, you will:
#
# - Use GenAI to accelerate analysis without outsourcing judgement.
# - Verify every generated figure against the source.
# - Produce a briefing you would put your name on.

# %% [markdown]
# ## Setup
#
# - **Data:**
#   - `data/epa_aqi_by_county.csv` — EPA Annual AQI by county, 2024 (public).
#   - `data/cdc_flu_wastewater.csv` — CDC influenza wastewater surveillance
#     (public) — the stretch step at the end.
#   - Provenance for both: `data/MANIFEST.json`. Public or synthetic data only.
# - **Key:** `OPENAI_API_KEY` from the environment / course `.env`, never printed.
# - **Boundary:** the model only ever sees the *profile* you send — never the raw
#   CSV. That is the pattern to copy when the data is not public.
# - **How this notebook works:** every step is one provided cell — run it with
#   Shift+Enter and read what it prints. Cells marked `# YOUR TURN` ask you to
#   edit the prompt text (ordinary quoted text — no code) or a pick from a
#   list, and re-run the cell. Everything runs as shipped, so you can never
#   get stuck.

# %%
# ▶ Setup — run this cell first (click it, then Shift+Enter).
# It loads the course helper functions used by every step below.
from lab_helpers import *
lab_status()

# %% [markdown]
# ## Steps
#
# ### Step 1 — Open the notebook
#
# You are here. Run the Setup cell above first.
#
# ### Step 2 — Profile, then five candidate findings (6 min)
#
# Send the model a *profile* of the EPA data (not the whole file) and ask for
# five candidate findings. The profile is provided — run the next cell and
# read it; it is all the model ever sees.

# %%
epa = load_epa_for_briefing()

# %%
profile = show_epa_profile(epa)

# %% [markdown]
# Now ask for the five candidate findings. The prompt below is a working
# version — **edit the text** and re-run to ask for different findings.

# %%
FINDINGS_PROMPT = """You are an analyst's assistant. From the dataset profile below, propose five candidate findings for a briefing on U.S. county air quality. Return JSON under key "findings" (five strings). Each finding must be checkable against the dataset described — no external knowledge."""   # ← YOUR TURN: edit the findings prompt, then re-run this cell

findings = propose_findings(profile, FINDINGS_PROMPT)

# %% [markdown]
# ### Step 3 — Pick the three most decision-relevant (3 min)
#
# Which three would a deputy director act on? Write your picks (by number) —
# then verify *all five* anyway, because the ones you discarded still teach
# you about the model's error pattern.

# %%
MY_THREE = [1, 2, 4]   # ← YOUR TURN: your three picks by finding number, then re-run this cell

# %% [markdown]
# ### Step 4 — Recompute every finding (8 min)
#
# The first cell below recomputes all five findings from the file itself.
# Run it, then mark each finding **confirmed / wrong / unverifiable** in the
# second cell. A finding is unverifiable when the *file itself* cannot answer
# it — that is a different failure from being wrong.

# %%
verify_findings(epa)

# %%
MY_VERDICTS = {1: "confirmed", 2: "confirmed", 3: "wrong", 4: "confirmed", 5: "unverifiable"}   # ← YOUR TURN: your verdict for each finding ("confirmed" / "wrong" / "unverifiable"), from the recomputed numbers above

show_verdicts(MY_VERDICTS)

# %% [markdown]
# ### Step 5 — Draft the briefing from confirmed findings only (5 min)
#
# Now the assistant earns its keep: draft the one-page briefing using **only
# the confirmed findings**. Feeding it verified facts, not its own claims,
# is the whole workflow in one line. The prompt below is a working version —
# note how it forbids any claim not in the verified list.

# %%
BRIEFING_PROMPT = """Draft a one-page briefing for a deputy director using ONLY the verified findings below. Do not add any number, claim, or comparison that is not in this list. Structure: headline, three short paragraphs, one-line recommendation."""   # ← YOUR TURN: edit the briefing prompt, then re-run this cell

briefing = draft_briefing(findings, MY_VERDICTS, BRIEFING_PROMPT)

# %% [markdown]
# ### Step 6 — Edit like you mean it (5 min)
#
# Edit the draft for accuracy and tone; remove every hedge you cannot
# support. Then record what you changed.
#
# ### Step 7 — Note which figures you had to correct (3 min)
#
# *Figures corrected, hedges removed, tone changes:*
#
# -
# -

# %% [markdown]
# ## Stretch — same game, harder file (optional)
#
# The workbook also lists `data/cdc_flu_wastewater.csv`: 3,000 rows of CDC
# influenza wastewater surveillance — messier and time-based. Run the cell
# below for a first look, then repeat Steps 2–7 on it (build a profile, ask
# for findings, verify, brief). Notice how much more can go wrong when the
# file has dates, sites and text fields.

# %%
profile_cdc_wastewater()

# %% [markdown]
# ## Deliverable
#
# 1. The five candidate findings with your verified verdicts.
# 2. The briefing drafted from confirmed findings only.
# 3. Your edit log (Step 7).

# %% [markdown]
# ## Reflection
#
# 1. How many of the five candidate findings survived verification?
# 2. Where did the assistant save you real time?
# 3. What would have happened if you had skipped the recompute step?

# %% [markdown]
# ## Debrief (instructor-led)
#
# 1. Which of the five findings would have reached the deputy director if you
#    had trusted the draft unread? What kind of wrong was each?
# 2. Where did verification cost you more time than the assistant saved — and
#    where was it clearly worth it?
# 3. What changes when the assistant runs inside a FedRAMP boundary instead of
#    a public chatbot — what may you then send that you may not send today?

# %% [markdown]
# ## Troubleshooting
#
# - **Every AI cell prints "(offline canned ...)"** — no API key is visible on
#   this machine. The canned set is deliberate: two of its five findings fail
#   verification. The lab is fully usable either way.
# - **The findings step returns prose, not a list (live run)** — ask
#   explicitly for a JSON object with the key `"findings"`; the helper already
#   forces JSON mode.
# - **Your recomputed number differs from a finding** — that IS the exercise,
#   not a bug in the data. Mark the verdict and keep the receipt (the
#   recomputed numbers above it).
# - **The briefing invents a number not in the confirmed list** — tighten
#   `BRIEFING_PROMPT`: "use only the findings below; every number must appear
#   in them".

# %% [markdown]
# ---
# *Curious about the Python behind these steps? The full code-forward version
# of this lab lives in the `For_Python_Programmers/` folder.*
