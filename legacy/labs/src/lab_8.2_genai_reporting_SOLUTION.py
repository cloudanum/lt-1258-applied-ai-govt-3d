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
# # Lab 8.2 — GenAI-Assisted Analysis and Briefing  *(SOLUTION / instructor copy)*
#
# **Chapter 8 — AI Operations and Reporting in Government** · 35 minutes *(flex)*
#
# **Objectives**
# 1. Use GenAI to accelerate analysis without outsourcing judgement.
# 2. Verify every generated figure against the source.
# 3. Produce a briefing you would put your name on.

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
# ## Step 1 — Profile, then five candidate findings

# %%
epa = load_epa_for_briefing()

# %%
profile_txt = show_epa_profile(epa)

# %% [markdown]
# **Worked prompt + the canned findings.** Note the profile explicitly says
# "Single year only: 2024" — watch whether the model still offers a trend
# claim. (The canned set does, deliberately: finding 5.)

# %%
FINDINGS_PROMPT = (
    "You are an analyst's assistant. From the dataset profile below, propose "
    "five candidate findings for a briefing on U.S. county air quality. "
    "Return JSON under key \"findings\" (five strings). Each finding must be "
    "checkable against the dataset described — no external knowledge."
)

findings = propose_findings(profile_txt, FINDINGS_PROMPT)

# %% [markdown]
# ## Step 2 — Pick the three most decision-relevant
#
# **Expected:** 1, 2, 4 (distribution, concentration, where-to-act). Finding
# 3 is trivia without the others; finding 5 is a trend claim on a single-year
# file — discard on sight.

# %%
MY_THREE = [1, 2, 4]

# %% [markdown]
# ## Step 3 — Recompute every finding in pandas
#
# **Expected verdicts:** 1 confirmed (838/997 = 84%), 2 confirmed (317 >
# 71+62+60+26 = 219), 3 **wrong** (8 states, not 15), 4 confirmed (61, 60,
# 46), 5 **unverifiable** (file contains only 2024). Typical live-model hit
# rate in this exercise: 3 of 5. That is why the recompute step exists.

# %%
verify_findings(epa)

# %%
VERDICTS = {1: "confirmed", 2: "confirmed", 3: "wrong",
            4: "confirmed", 5: "unverifiable"}
show_verdicts(VERDICTS)

# %% [markdown]
# ## Step 4 — Draft the briefing from confirmed findings only
#
# **Worked prompt** below. Two instructive failure modes to narrate in class:
# if you forget to forbid outside claims, the model re-introduces the
# discarded findings (it "remembers" them from the conversation); if you
# paste the whole file instead of findings, it drafts from unverified numbers.

# %%
BRIEFING_PROMPT = (
    "Draft a one-page briefing for a deputy director using ONLY the verified "
    "findings below. Do not add any number, claim, or comparison that is not "
    "in this list. Structure: headline, three short paragraphs, one-line "
    "recommendation."
)

briefing = draft_briefing(findings, VERDICTS, BRIEFING_PROMPT)

# %% [markdown]
# ## Step 5 — Edit log (worked)
#
# - Corrected "more than the next four states combined" — kept, but verified
#   against the recompute (317 > 219) before letting it stand.
# - Removed the draft's hedge "appears to be concentrated" — after
#   verification the claim is not an appearance; unsupported hedging is its
#   own accuracy problem.
# - Removed "record-low" from an earlier draft line — superlatives need a
#   time series this file does not contain (finding 5's failure mode).
# - Tone: cut "alarmingly" — the numbers carry the alarm; adjectives are not
#   evidence.
#
# ## Reflection (expected answers)
# 1. Three of five: two confirmed-and-used, one wrong (8 states ≠ 15), one
#    unverifiable (single-year file). Both failures looked equally confident
#    in prose.
# 2. Drafting speed and structure — the first pass of candidate findings and
#    the briefing skeleton. Verification time did not shrink; it moved
#    earlier, to the findings stage, where it is cheaper.
# 3. The briefing would have shipped "15 states with hazardous days" and a
#    trend claim the file cannot support — signed by you. The model's error
#    becomes your error at the moment you stop checking.
