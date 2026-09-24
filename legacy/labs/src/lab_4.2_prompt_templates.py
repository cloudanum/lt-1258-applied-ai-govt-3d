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
# the course helpers (canned offline fallback)*
#
# A prompt that works once is a trick. A template that works on inputs you
# have not seen is a tool.
#
# Cells marked `# YOUR TURN` ask you to edit the template text and re-run.
# Offline, calls return realistic canned answers built from your actual
# inputs.

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
# **Tools:** the OpenAI chat API through the course helpers — offline these
# return canned stand-ins built from your actual inputs.
#
# **Prerequisite:** your Prompt Card from Lab 4.1 (or any prompt you like).
#
# **Data rule:** use only the public course data above. Never paste real
# agency data containing PII into these notebooks — or into any AI tool.
#
# **How this notebook works:** every step is one provided cell — run it with
# Shift+Enter and read what it prints. Cells marked `# YOUR TURN` ask you to
# edit the template text (ordinary quoted text with `[BRACKETED]` slots — no
# code) and re-run the cell. Everything runs as shipped, so you can never get
# stuck.

# %%
# ▶ Setup — run this cell first (click it, then Shift+Enter).
# It loads the course helper functions used by every step below.
from lab_helpers import *
lab_status()

# %% [markdown]
# ## Steps
#
# 1. Run the Setup cell and load the inventory. (2 min)
# 2. Take your best prompt from Lab 4.1 and replace the specifics with
#    `[BRACKETED]` slots. (5 min)
# 3. Fill the slots into a template you can re-use. (6 min)
# 4. Run it over five different rows of `federal_ai_use_cases.csv`. (6 min)
# 5. Find the input that breaks it and fix the template, not the input.
#    (7 min)
# 6. Add a second template for a different pattern and test it the same way.
#    (4 min)
# 7. Export both to `my_prompt_library.md`. (2 min)

# %% [markdown]
# ### Step 1 — Load the inventory (provided)
#
# The substrate: rows of `federal_ai_use_cases.csv`. Run the cell and read the
# preview — these are the fields your templates will fill their slots from.

# %%
uc = load_use_case_inventory()

# %% [markdown]
# ### Steps 2–3 — From prompt to template
#
# Take the zero-shot summarizer from Lab 4.1 (or your best prompt from that
# lab) and replace the specifics with `[BRACKETED]` slots. The template below
# is a working starting point — **edit the text** so it says what *you* want,
# keeping the slots: `[AGENCY]`, `[NAME]`, `[STAGE]`, `[PROBLEM]`,
# `[AUDIENCE]`. The helper fills the slots from each inventory row and sends
# the result to the model.

# %%
MY_TEMPLATE = """In two sentences for [AUDIENCE], summarize this federal AI use case.
Agency: [AGENCY]
Use case: [NAME]
Stage: [STAGE]
Problem it solves: [PROBLEM]"""   # ← YOUR TURN: edit the template text (keep the [SLOTS]), then re-run this cell — the next cell runs it on real rows

# %% [markdown]
# ### Step 4 — Test on five rows it was not written for
#
# Run your template over five different rows. Score each output on the course
# rubric (accuracy / completeness / format / tone, 1–5) — at least mentally —
# and watch for the row where it breaks.

# %%
test_template_on_rows(uc, MY_TEMPLATE)

# %% [markdown]
# ### Step 5 — Find the input that breaks it
#
# The inventory is real data: 223 rows have a blank `development_stage` and
# 297 have a blank `problem_solved`. The first cell feeds your template one of
# those rows — read what comes out. Then fix **the template, not the input** —
# the next unseen row will have the same defect.

# %%
show_breaking_row(uc, MY_TEMPLATE)

# %%
MY_FIXED_TEMPLATE = """In two sentences for [AUDIENCE], summarize this federal AI use case. If a field says 'not reported', do not invent it — say the inventory does not report it.
Agency: [AGENCY]
Use case: [NAME]
Stage: [STAGE]
Problem it solves: [PROBLEM]"""   # ← YOUR TURN: your fixed template — it must tell the model what to do when a field is "not reported"

show_fixed_brief(uc, MY_FIXED_TEMPLATE)

# %% [markdown]
# ### Step 6 — A second template, a different pattern
#
# Briefings are generation; now try a template for a **different** pattern —
# structured triage: given a use case, return JSON with
# `{plain_english, risk_flag, one_question_to_ask}`. The template below is a
# working version — edit it, then the same three test rows are run through it.

# %%
TRIAGE_TEMPLATE = """Return JSON with keys plain_english, risk_flag (low|review), one_question_to_ask for this use case.
Agency: [AGENCY]
Use case: [NAME]
Stage: [STAGE]
High-impact: [IS_HIGH_IMPACT]"""   # ← YOUR TURN: edit the triage template, then re-run this cell

triage_use_cases(uc, TRIAGE_TEMPLATE)

# %% [markdown]
# ### Step 7 — Export the library
#
# Ship it: write both templates to `my_prompt_library.md` with a usage note
# and the known-limitation you discovered in Step 5. The text below is a
# working version — replace it with documentation of *your* two templates
# (name, slots, the prompt text, when to use, known limitations).

# %%
MY_LIBRARY = """# My Prompt Library

## use_case_brief(agency, name, stage, problem, audience)
Two-sentence executive briefing of a federal AI use case.
**Known limitation:** inventory rows may lack stage or problem; v2 omits the clause rather than inventing content.

## triage_use_case(agency, name, stage, is_high_impact)
Structured JSON triage: plain_english, risk_flag, one_question_to_ask.
**Known limitation:** risk_flag keys only off the high-impact label; it is triage, not assessment.
"""   # ← YOUR TURN: document YOUR two templates, then re-run this cell

save_to_prompt_library(MY_LIBRARY)

# %% [markdown]
# ## Deliverable
# 1. Your briefing template v1, the broken output, and the fixed v2.
# 2. Your triage template tested on three rows.
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
# - **`ModuleNotFoundError: lab_helpers`** — the kernel's working directory is
#   not `labs/`. Restart the kernel from the `labs/` folder and Run All.
# - **A red error mentioning `federal_ai_use_cases`** — the data file is not
#   where the notebook expects it. Restart the kernel from the `labs/` folder
#   and Run All; if it persists, tell your instructor.
# - **"nan" appears in an output** — that is Step 5 doing its job: a blank
#   field reached the prompt unfilled. Fix the template text (see the v2
#   template's "not reported" wording), not the row.
# - **Every AI call prints "[offline example ...]"** — you are on the canned
#   path (no key on this machine). The canned replies are built from the real
#   row values, so the mechanics of the lab are unaffected.
# - **`my_prompt_library.md` did not change** — edit the `MY_LIBRARY` text
#   first, then re-run the export cell.

# %% [markdown]
# ---
# *Curious about the Python behind these steps? The full code-forward version
# of this lab lives in the `For_Python_Programmers/` folder.*
