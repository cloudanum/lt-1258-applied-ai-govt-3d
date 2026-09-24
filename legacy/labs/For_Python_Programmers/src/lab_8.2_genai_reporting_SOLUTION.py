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
# (where lab_common.py and data/ are) and run from there.
import os, sys
from pathlib import Path

for _cand in (Path.cwd(), Path.cwd().parent):
    if (_cand / "lab_common.py").is_file():
        os.chdir(_cand)
        if str(_cand) not in sys.path:
            sys.path.insert(0, str(_cand))
        break

# %% [markdown]
# ## Step 1 — Profile, then five candidate findings

# %%
import pandas as pd
from lab_common import chat, chat_json

epa = pd.read_csv("data/epa_aqi_by_county.csv")
epa["unhealthy_total"] = (epa["Unhealthy Days"] + epa["Very Unhealthy Days"]
                          + epa["Hazardous Days"])

profile_txt = f"""EPA Annual AQI by county, 2024. {len(epa)} counties, {epa['State'].nunique()} states/territories.
Columns: State, County, Year, Days with AQI, Good/Moderate/USG/Unhealthy/Very Unhealthy/Hazardous Days,
Max AQI, 90th Percentile AQI, Median AQI, pollutant day counts (CO, NO2, Ozone, PM2.5, PM10).
Median of county Median AQI: {epa['Median AQI'].median()}.
Single year only: 2024."""

print(profile_txt)

# %% [markdown]
# **Worked prompt + the canned findings.** Note the profile explicitly says
# "Single year only: 2024" — watch whether the model still offers a trend
# claim. (The canned set does, deliberately: finding 5.)

# %%
CANNED_FINDINGS = {"findings": [
    "838 of 997 counties (84%) recorded zero days at Unhealthy or worse in 2024.",
    "California accounts for 317 unhealthy-or-worse county-days — more than the next four states combined.",
    "Hazardous-level air days were recorded in 15 states in 2024.",
    "Three Southern California counties (San Bernardino, Riverside, Los Angeles) each logged more than 45 Unhealthy days.",
    "Air quality improved in most counties relative to 2023.",
]}

FINDINGS_PROMPT = (
    "You are an analyst's assistant. From the dataset profile below, propose "
    "five candidate findings for a briefing on U.S. county air quality. "
    "Return JSON under key \"findings\" (five strings). Each finding must be "
    "checkable against the dataset described — no external knowledge."
)

findings = chat_json([{"role": "user", "content":
                       FINDINGS_PROMPT + "\n\nPROFILE:\n" + profile_txt}],
                     offline=CANNED_FINDINGS)
for i, f in enumerate(findings["findings"], 1):
    print(f"{i}. {f}")

# %% [markdown]
# ## Step 2 — Pick the three most decision-relevant
#
# **Expected:** 1, 2, 4 (distribution, concentration, where-to-act). Finding
# 3 is trivia without the others; finding 5 is a trend claim on a single-year
# file — discard on sight.

# %%
my_three = [1, 2, 4]

# %% [markdown]
# ## Step 3 — Recompute every finding in pandas
#
# **Expected verdicts:** 1 confirmed (838/997 = 84%), 2 confirmed (317 >
# 71+62+60+26 = 219), 3 **wrong** (8 states, not 15), 4 confirmed (61, 60,
# 46), 5 **unverifiable** (file contains only 2024). Typical live-model hit
# rate in this exercise: 3 of 5. That is why the recompute step exists.

# %%
zero_unhealthy = int((epa["unhealthy_total"] == 0).sum())
print(f"[1] counties with zero unhealthy-or-worse days: {zero_unhealthy} of {len(epa)}")

ca_days = int(epa.loc[epa["State"] == "California", "unhealthy_total"].sum())
by_state = (epa.groupby("State")["unhealthy_total"].sum()
            .sort_values(ascending=False))
next4 = int(by_state.iloc[1:5].sum())
print(f"[2] California: {ca_days} | next four states combined: {next4}")

hz_states = int(epa.loc[epa["Hazardous Days"] > 0, "State"].nunique())
print(f"[3] states with any Hazardous days: {hz_states}")

socal = epa[epa["County"].isin(["San Bernardino", "Riverside", "Los Angeles"])
            & (epa["State"] == "California")]
print("[4] SoCal Unhealthy days:", socal.set_index("County")["Unhealthy Days"].to_dict())

print(f"[5] years present in file: {sorted(epa['Year'].unique())}")

# %%
verdicts = {1: "confirmed", 2: "confirmed", 3: "wrong",
            4: "confirmed", 5: "unverifiable"}
for i, v in verdicts.items():
    print(f"finding {i}: {v}")

# %% [markdown]
# ## Step 4 — Draft the briefing from confirmed findings only
#
# **Worked prompt** below. Two instructive failure modes to narrate in class:
# if you forget to forbid outside claims, the model re-introduces the
# discarded findings (it "remembers" them from the conversation); if you
# paste the whole file instead of findings, it drafts from unverified numbers.

# %%
confirmed = [findings["findings"][i - 1] for i, v in verdicts.items() if v == "confirmed"]

CANNED_BRIEFING = (
    "COUNTY AIR QUALITY, 2024 — BRIEFING FOR THE DEPUTY DIRECTOR\n\n"
    "Bad air in 2024 was a local, not national, condition: 84% of U.S. "
    "counties (838 of 997) recorded zero days at Unhealthy or worse. "
    "California is the outlier, accounting for 317 unhealthy-or-worse "
    "county-days — more than the next four states combined. The exposure is "
    "concentrated further still: San Bernardino, Riverside, and Los Angeles "
    "counties each logged more than 45 Unhealthy days.\n\n"
    "RECOMMENDATION: focus chronic-exposure outreach on the three Southern "
    "California counties; treat remaining hotspots as event-driven."
)

BRIEFING_PROMPT = (
    "Draft a one-page briefing for a deputy director using ONLY the verified "
    "findings below. Do not add any number, claim, or comparison that is not "
    "in this list. Structure: headline, three short paragraphs, one-line "
    "recommendation.\n\nVERIFIED FINDINGS:\n- " + "\n- ".join(confirmed)
)

briefing = chat([{"role": "user", "content": BRIEFING_PROMPT}],
                offline=CANNED_BRIEFING)
print(briefing)

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
