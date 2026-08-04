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
# Cells marked `# YOUR CODE` are for you. Offline — or until you write your own
# prompt — every call returns a labelled canned answer, so the whole notebook
# always runs.

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

# %%
# API key: uses OPENAI_API_KEY from the environment (classroom VM); when run on
# the author's machine it falls back to the course .env file found by walking up
# from the notebook directory. The key is never printed.
import os, pathlib
def _load_api_key():
    if os.getenv("OPENAI_API_KEY") is not None:
        return  # environment wins — an explicitly empty value forces offline mode
    for p in [pathlib.Path.cwd(), *pathlib.Path.cwd().parents]:
        env = p / ".env"
        if env.is_file():
            for line in env.read_text().splitlines():
                k, _, v = line.partition("=")
                if k.strip() == "OPENAI_API_KEY" and v.strip():
                    os.environ["OPENAI_API_KEY"] = v.strip()
                    return
_load_api_key()
if not os.getenv("OPENAI_API_KEY"):
    print("OPENAI_API_KEY not set - ask your instructor, or the AI steps will be skipped/mocked.")

# %% [markdown]
# ## Steps
#
# ### Step 1 — Open the notebook
#
# You are here. Run the Setup loader cell above first.
#
# ### Step 2 — Profile, then five candidate findings (6 min)
#
# Send the model a *profile* of the EPA data (not the whole file) and ask for
# five candidate findings. The profile is provided — read it; it is all the
# model ever sees.

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

# %%
CANNED_FINDINGS = {"findings": [
    "838 of 997 counties (84%) recorded zero days at Unhealthy or worse in 2024.",
    "California accounts for 317 unhealthy-or-worse county-days — more than the next four states combined.",
    "Hazardous-level air days were recorded in 15 states in 2024.",
    "Three Southern California counties (San Bernardino, Riverside, Los Angeles) each logged more than 45 Unhealthy days.",
    "Air quality improved in most counties relative to 2023.",
]}

FINDINGS_PROMPT = None
# YOUR CODE: prompt for five candidate findings from profile_txt as JSON
# under key "findings". Pass offline=CANNED_FINDINGS.

findings = None
if FINDINGS_PROMPT:
    findings = chat_json([{"role": "user", "content":
                           FINDINGS_PROMPT + "\n\nPROFILE:\n" + profile_txt}],
                         offline=CANNED_FINDINGS)
if findings is None:
    findings = CANNED_FINDINGS
    print("(canned findings applied — write FINDINGS_PROMPT above to run your own)\n")
for i, f in enumerate(findings["findings"], 1):
    print(f"{i}. {f}")

# %% [markdown]
# ### Step 3 — Pick the three most decision-relevant (3 min)
#
# Which three would a deputy director act on? Write your picks (by number) —
# then verify *all five* anyway, because the ones you discarded still teach
# you about the model's error pattern.

# %%
my_three = [1, 2, 4]  # YOUR CODE: your three picks by finding number

# %% [markdown]
# ### Step 4 — Recompute every finding in pandas (8 min)
#
# The cell below recomputes all five. Run it, then mark each finding
# **confirmed / wrong / unverifiable** in the verdicts dict. A finding is
# unverifiable when the *file itself* cannot answer it — that is a different
# failure from being wrong.

# %%
# verification code (provided — read it; this is the skill the lab exists to teach)
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
verdicts = {}
# YOUR CODE: {1: "confirmed"|"wrong"|"unverifiable", ...} for all five,
# from the recomputed numbers above.

if not verdicts:
    verdicts = {1: "confirmed", 2: "confirmed", 3: "wrong",
                4: "confirmed", 5: "unverifiable"}
    print("(reference verdicts applied — check them against the numbers above)\n")
for i, v in verdicts.items():
    print(f"finding {i}: {v}")

# %% [markdown]
# ### Step 5 — Draft the briefing from confirmed findings only (5 min)
#
# Now the assistant earns its keep: draft the one-page briefing using **only
# the confirmed findings**. Feeding it verified facts, not its own claims,
# is the whole workflow in one line.

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

BRIEFING_PROMPT = None
# YOUR CODE: prompt for a one-page briefing using ONLY the confirmed findings
# (join `confirmed` into the prompt). Forbid any claim not in the list.
# Pass offline=CANNED_BRIEFING.

briefing = None
if BRIEFING_PROMPT:
    briefing = chat([{"role": "user", "content": BRIEFING_PROMPT}],
                    offline=CANNED_BRIEFING)
if briefing is None:
    briefing = CANNED_BRIEFING
    print("(canned briefing applied — write BRIEFING_PROMPT above to run your own)\n")
print(briefing)

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
# influenza wastewater surveillance — messier and time-based. Build a profile
# below, then repeat Steps 2–7 on it. Notice how much more can go wrong when
# the file has dates, sites and text fields.

# %%
cdc = pd.read_csv("data/cdc_flu_wastewater.csv")
print("shape:", cdc.shape)
print("columns:", ", ".join(cdc.columns[:12]), "...")
print("states/territories:", cdc["state_territory"].nunique())
print("sample dates:", cdc["sample_collect_date"].min(), "->", cdc["sample_collect_date"].max())
# YOUR CODE: profile it properly (per-site counts, missing values, date spans),
# then run the five-findings -> verify -> briefing workflow on that profile.

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
# - **"(canned findings applied...)" prints** — expected until you write
#   `FINDINGS_PROMPT` (or when running without a key). The canned set is
#   deliberate: two of its five findings fail verification.
# - **`chat_json` returns `None` or your prompt errors** — ask explicitly for a
#   JSON object with the key `"findings"`; the helper already sets
#   `response_format={"type": "json_object"}`.
# - **Your recomputed number differs from a finding** — that IS the exercise,
#   not a bug in the data. Mark the verdict and keep the receipt (the code).
# - **`KeyError` on a CDC column in the stretch** — you guessed a column name;
#   print `cdc.columns` first. Never guess schema.
# - **The briefing invents a number not in `confirmed`** — tighten
#   `BRIEFING_PROMPT`: "use only the findings below; every number must appear
#   in them".
