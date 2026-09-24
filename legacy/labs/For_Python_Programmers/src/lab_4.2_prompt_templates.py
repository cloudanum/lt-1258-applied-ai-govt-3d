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
# # Lab 4.2 — Build a Reusable Prompt Template Library
#
# *Chapter 4 — Modern GenAI and Prompt Engineering · 30 minutes (flex — your
# instructor may skip this) · JupyterLab with pandas and the OpenAI API via
# `lab_common` (canned offline fallback)*
#
# A prompt that works once is a trick. A template that works on inputs you
# have not seen is a tool.
#
# Cells marked `# YOUR CODE` are for you. Offline, calls return realistic
# canned answers built from your actual inputs.

# %% [markdown]
# ## Objectives
#
# By the end of this lab, you will:
#
# - Turn one-off prompts into parameterised templates.
# - Test a template against inputs it was not written for.
# - Ship something your team can adopt.

# %% [markdown]
# ## Setup
#
# **Datasets and files** (all under `labs/data/`):
#
# - `federal_ai_use_cases.csv` — the OMB 2025 Federal Agency AI Use Case
#   Inventory (real, public; see `data/MANIFEST.json`). Real data with real
#   gaps: blank stages and problem statements — which is exactly what will
#   break your first template.
#
# **Tools:** pandas, plus the OpenAI chat API through `lab_common.chat()` /
# `lab_common.chat_json()` — offline these return canned stand-ins built from
# your actual inputs.
#
# **Prerequisite:** your Prompt Card from Lab 4.1 (or any prompt you like).
#
# **Data rule:** use only the public course data above. Never paste real
# agency data containing PII into these notebooks — or into any AI tool.

# %%
# API key status — lab_common loads OPENAI_API_KEY from the environment
# (classroom VM) or the course .env file at import. The key is never printed.
# With no key, every AI call below falls back to a realistic canned output.
import lab_common as lc

if lc.online():
    print(f"OpenAI API key found — live mode (model: {lc.CHAT_MODEL}).")
else:
    print("No API key found — offline mode: AI calls return realistic canned "
          "outputs, so every step still runs.\nAsk your instructor if you "
          "expected a key on this machine.")

# %% [markdown]
# ## Steps
#
# 1. Open `lab_4.2_prompt_templates.ipynb` and run the Setup cells.
# 2. Take your best prompt from Lab 4.1 and replace the specifics with
#    `[BRACKETED]` slots. (5 min)
# 3. Write it as a Python function taking those slots as arguments. (6 min)
# 4. Run it over five different rows of `federal_ai_use_cases.csv`. (6 min)
# 5. Find the input that breaks it and fix the template, not the input.
#    (7 min)
# 6. Add a second template for a different pattern and test it the same way.
#    (4 min)
# 7. Export both to `my_prompt_library.md`. (2 min)

# %% [markdown]
# ### Steps 2–3 — From prompt to template
#
# Take the zero-shot summarizer from Lab 4.1 (or your best prompt from that
# lab) and replace the specifics with `[BRACKETED]` slots. Then write it as a
# Python function whose arguments are the slots. The substrate: rows of
# `federal_ai_use_cases.csv`.

# %%
import pandas as pd
from lab_common import chat, chat_json

uc = pd.read_csv("data/federal_ai_use_cases.csv", encoding="utf-8-sig")
cols = ["agency_name", "use_case_name", "development_stage",
        "is_high_impact", "problem_solved"]
print(uc[cols].head(3).to_string())

# %%
def use_case_brief(agency, name, stage, problem, audience="a non-technical executive"):
    """Template v1 — YOUR CODE: replace the body with your own parameterized
    version of your Lab 4.1 prompt. The reference version below fills the
    slots into a briefing prompt; yours should too (or better)."""
    prompt = (f"In two sentences for {audience}, summarize this federal AI "
              f"use case.\nAgency: {agency}\nUse case: {name}\n"
              f"Stage: {stage}\nProblem it solves: {problem}")
    canned = (f"[offline example for: {name[:60]}] {agency} is applying AI "
              f"({stage}) to {str(problem)[:80]}. The system, '{name}', is "
              f"intended to turn that manual work into an automated pipeline.")
    return chat([{"role": "user", "content": prompt}], offline=canned)

# %% [markdown]
# ### Step 4 — Test on five rows it was not written for
#
# Run your template over five different rows. Score each output on the course
# rubric (accuracy / completeness / format / tone, 1–5) — at least mentally —
# and watch for the row where it breaks.

# %%
test_rows = uc[cols].dropna(subset=["use_case_name"]).sample(5, random_state=11)
outputs = {}
for i, row in test_rows.iterrows():
    outputs[i] = use_case_brief(row["agency_name"], row["use_case_name"],
                                row["development_stage"], row["problem_solved"])
    print(f"--- {row['use_case_name'][:70]}")
    print(outputs[i], "\n")

# %% [markdown]
# ### Step 5 — Find the input that breaks it
#
# The inventory is real data: 223 rows have a blank `development_stage` and
# 297 have a blank `problem_solved`. Feed your template one of those rows and
# read what comes out. Then fix **the template, not the input** — the next
# unseen row will have the same defect.

# %%
breaking_row = uc[uc["problem_solved"].isna()][cols].iloc[0]
print(breaking_row.to_string(), "\n")
broken = use_case_brief(breaking_row["agency_name"], breaking_row["use_case_name"],
                        breaking_row["development_stage"], breaking_row["problem_solved"])
print("BROKEN OUTPUT:\n", broken)

# %%
def use_case_brief_v2(agency, name, stage, problem, audience="a non-technical executive"):
    # YOUR CODE: the fixed template. Handle missing stage/problem gracefully
    # (omit the clause, or say "stage not reported" — but never print "nan").
    return None


def reference_brief_v2(agency, name, stage, problem, audience="a non-technical executive"):
    """Provided fallback so later cells run. Peek only if stuck!"""
    stage_txt = f"Stage: {stage}" if pd.notna(stage) else "Stage: not reported"
    prob_txt = (f"Problem it solves: {problem}" if pd.notna(problem)
                else "Problem statement: not reported in the inventory")
    prompt = (f"In two sentences for {audience}, summarize this federal AI "
              f"use case. If a field says 'not reported', do not invent it — "
              f"say the inventory does not report it.\nAgency: {agency}\n"
              f"Use case: {name}\n{stage_txt}\n{prob_txt}")
    canned = (f"[offline example for: {name[:60]}] {agency} reports an AI use "
              f"case, '{name[:60]}'"
              + (f", currently {str(stage).lower()}" if pd.notna(stage) else
                 ", though the inventory does not report its stage")
              + ". Details beyond that are not reported in the inventory.")
    return chat([{"role": "user", "content": prompt}], offline=canned)


fixed = use_case_brief_v2(breaking_row["agency_name"], breaking_row["use_case_name"],
                          breaking_row["development_stage"], breaking_row["problem_solved"])
if fixed is None:
    fixed = reference_brief_v2(breaking_row["agency_name"], breaking_row["use_case_name"],
                               breaking_row["development_stage"],
                               breaking_row["problem_solved"])
    print("(reference fix applied — replace with your own use_case_brief_v2)\n")
print("FIXED OUTPUT:\n", fixed)

# %% [markdown]
# ### Step 6 — A second template, a different pattern
#
# Briefings are generation; now write a template for a **different** pattern —
# e.g. structured triage: given a use case, return JSON with
# `{plain_english, risk_flag, one_question_to_ask}`. Test it the same way.

# %%
def triage_use_case(agency, name, stage, is_high_impact):
    # YOUR CODE: chat_json() template returning
    # {"plain_english": str, "risk_flag": "low"|"review", "one_question_to_ask": str}
    # Pass a canned offline object built from the arguments.
    return None


def reference_triage(agency, name, stage, is_high_impact):
    flag = "review" if is_high_impact == "High-impact" else "low"
    canned = {"plain_english": f"{name} — an AI use case reported by {agency}.",
              "risk_flag": flag,
              "one_question_to_ask":
                  "What human review exists before this system's output reaches a decision?"}
    prompt = (f"Return JSON with keys plain_english, risk_flag (low|review), "
              f"one_question_to_ask for this use case.\nAgency: {agency}\n"
              f"Use case: {name}\nStage: {stage}\nHigh-impact: {is_high_impact}")
    return chat_json([{"role": "user", "content": prompt}], offline=canned)


for i, row in test_rows.head(3).iterrows():
    out = triage_use_case(row["agency_name"], row["use_case_name"],
                          row["development_stage"], row["is_high_impact"])
    if out is None:
        out = reference_triage(row["agency_name"], row["use_case_name"],
                               row["development_stage"], row["is_high_impact"])
        if i == test_rows.index[0]:
            print("(reference triage applied — replace with your own)\n")
    print(out)

# %% [markdown]
# ### Step 7 — Export the library
#
# Ship it: write both templates to `my_prompt_library.md` with a usage note
# and the known-limitation you discovered in Step 5.

# %%
library_md = None
# YOUR CODE: build a markdown string documenting both templates (name, slots,
# the prompt text, when to use, known limitations) and write it to
# my_prompt_library.md.

if library_md is None:
    library_md = (
        "# My Prompt Library\n\n"
        "## use_case_brief(agency, name, stage, problem, audience)\n"
        "Two-sentence executive briefing of a federal AI use case.\n"
        "**Known limitation:** inventory rows may lack stage or problem; "
        "v2 omits the clause rather than inventing content.\n\n"
        "## triage_use_case(agency, name, stage, is_high_impact)\n"
        "Structured JSON triage: plain_english, risk_flag, one_question_to_ask.\n"
        "**Known limitation:** risk_flag keys only off the high-impact label; "
        "it is triage, not assessment.\n"
    )
    with open("my_prompt_library.md", "w") as f:
        f.write(library_md)
    print("(reference library exported — replace with your own)\n")
print(open("my_prompt_library.md").read())

# %% [markdown]
# ## Deliverable
# 1. `use_case_brief` v1, the broken output, and the fixed v2.
# 2. `triage_use_case` tested on three rows.
# 3. `my_prompt_library.md`.

# %% [markdown]
# ## Reflection
# 1. What broke first when the input varied?
# 2. Which slot turned out to matter most?
# 3. What would you need to add before handing this to your team?

# %% [markdown]
# ## Debrief (instructor-led)
#
# - **Show of breaks.** Who found a row that broke their template? Collect
#   the failure modes on the board — missing fields, odd lengths, unexpected
#   values.
# - **Template vs prompt.** What did you gain by parameterizing, and what did
#   you lose?
# - **Adoption.** What would a team need around `my_prompt_library.md`
#   (ownership, versioning, review) before it becomes shared infrastructure?

# %% [markdown]
# ## Troubleshooting
#
# - **`UnicodeDecodeError` reading the CSV** — the inventory ships with a
#   BOM; the notebook already reads it with `encoding="utf-8-sig"`. Keep that
#   argument if you rewrite the cell.
# - **`KeyError` on a column name** — print `list(uc.columns)`; the OMB file
#   uses snake_case names exactly as in `cols`.
# - **"nan" appears in an output** — that is Step 5 doing its job: a blank
#   field reached the prompt unfilled. Fix the template (see
#   `reference_brief_v2`), not the row.
# - **Every AI call prints "(reference ...)" or "[offline example ...]"** —
#   you are on the canned path (no key, or the YOUR-CODE function still
#   returns `None`). The mechanics of the lab are unaffected.
# - **`my_prompt_library.md` did not update** — the reference exporter only
#   writes when `library_md` is `None`; assign your own string first.
