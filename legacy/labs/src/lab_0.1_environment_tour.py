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
# # Lab 0.1 — Course Environment and Data Tour
#
# *Course 1258 — Applied AI for Government IT Professionals · Ch00 Course
# Launch and Lab Environment · 20 minutes · CloudShare VM (JupyterLab) ·
# OpenAI API via the course helpers (canned fallback when no key)*
#
# You have a working VM. Before the course leans on it, take a few minutes to
# learn the room: where the notebooks are, where the data is, and how a
# notebook reaches the model.

# %% [markdown]
# ## Objectives
#
# By the end of this lab, you will:
#
# - Navigate JupyterLab confidently: cells, run order, kernel restart.
# - Confirm the six shipped datasets load, and know what each one is for.
# - Make one successful call to the OpenAI API using the key from `.env`.

# %% [markdown]
# ## Setup
#
# - **Datasets:** all six course datasets in `data/` (provenance in
#   `data/MANIFEST.json`); this lab touches `federal_ai_use_cases.csv` and
#   `chicago_311.csv` directly.
# - **API key:** the setup cell below loads the course helpers, which read
#   `OPENAI_API_KEY` from the environment (classroom VM) or from the course
#   `.env` file. The key is **never printed**. With no key, the model cell
#   uses a realistic canned reply, so the tour completes either way.
# - **The one rule that never changes:** public or synthetic data only. Never
#   paste real agency, personal or sensitive data into any assistant.
# - **Every step below is one provided cell** — there is nothing to type.
#   Run the cells in order (Shift+Enter) and read what they print.

# %%
# ▶ Setup — run this cell first (click it, then Shift+Enter).
# It loads the course helper functions used by every step below.
from lab_helpers import *

# %% [markdown]
# ## Steps
#
# 1. **(1 min)** Open `lab_0.1_environment_tour.ipynb` — you are here. Run
#    cells top to bottom (Shift+Enter), or **Run → Run All Cells** now and
#    read along.
# 2. **(3 min)** Run the **environment** cell. Confirm it prints the `.env`
#    path it loaded and the model alias — but never the key itself.
# 3. **(3 min)** Run the **data inventory** cell: it reads
#    `data/MANIFEST.json` and prints each dataset with its row count and
#    one-line description.
# 4. **(3 min)** Load the federal AI use case inventory and look at its shape
#    and columns.
# 5. **(2 min)** Answer in the notebook: how many use cases are flagged
#    `is_high_impact`?
# 6. **(3 min)** Look at the five most common `sr_type` values in the Chicago
#    311 data.
# 7. **(3 min)** Run the **first API call** cell: a one-sentence prompt,
#    printing the reply and the token counts.
# 8. **(2 min)** Deliberately break something: restart the kernel, re-run only
#    the last cell, and read the error. Then **Run All** to recover.

# %% [markdown]
# ### Step 2 — The environment cell (provided)
#
# This cell prints where the key came from and which models the course uses —
# **never the key itself**. On the VM the key is injected for you; off the VM,
# the helpers read it from a `.env` file at the course root.

# %%
tour_environment()

# %% [markdown]
# ### Step 3 — Data inventory (provided)
#
# `data/MANIFEST.json` says where each dataset came from and what it is for.
# This cell prints each file with its row count and one-line description.

# %%
tour_data_inventory()

# %% [markdown]
# ### Step 4 — Load the federal AI use case inventory (provided)
#
# This CSV is the course's own subject matter as data: every AI use case the
# agencies reported to OMB. This cell loads it and prints its shape and
# columns.

# %%
uc = load_use_cases()

# %% [markdown]
# ### Step 5 — How many use cases are flagged high-impact? (provided)
#
# The `is_high_impact` column answers OMB's risk question. This cell counts
# how many use cases are flagged `High-impact` — and shows what *other* values
# the column contains while it is at it.

# %%
count_high_impact(uc)

# %% [markdown]
# ### Step 6 — Chicago 311: the five most common request types (provided)
#
# `chicago_311.csv` is a recent extract of the City's 311 service requests —
# deliberately real and messy. You will meet it again in Labs 5.2, 6.1 and 6.2.

# %%
top_311_requests()

# %% [markdown]
# ### Step 7 — Your first API call (provided)
#
# One sentence in, one sentence out, and read the token counts — the unit you
# pay in. If no key is configured you get a canned reply so the tour still
# works; the token line tells you it is offline.

# %%
first_api_call()

# %% [markdown]
# ### Step 8 — Break it on purpose
#
# 1. **Kernel menu → Restart Kernel** (the circular arrow). This wipes every
#    variable and every loaded helper.
# 2. Re-run *only* this cell. Read the `NameError`: `kernel_state_check` no
#    longer exists because the setup cell above has not run in the new kernel.
# 3. **Run menu → Run All Cells** to recover.
#
# This is the single most common notebook confusion in class — make it happen
# now, on purpose, when nothing is at stake.

# %%
kernel_state_check(uc)

# %% [markdown]
# ## Deliverable
#
# A fully run notebook (Run All, top to bottom, no errors) with:
# 1. The data inventory printed in Step 3.
# 2. The high-impact count from Step 5.
# 3. The top-5 request types from Step 6.
# 4. The model's reply and token counts from Step 7 (or the offline note).

# %% [markdown]
# ## Reflection
#
# 1. Why did the last cell fail after a kernel restart?
# 2. Which of the six datasets would you reach for to answer "which agencies
#    use AI for document processing"?
# 3. What did the token counts suggest about cost at agency scale?

# %% [markdown]
# ## Debrief (instructor-led)
#
# - Show of hands: who hit the `NameError` in Step 8 before Run All fixed it?
#   Say it aloud: kernel state lives in memory, not in the file — "Restart &
#   Run All" is the notebook's clean build.
# - Look at the `is_high_impact` value counts together: what on earth is
#   `Presumed High-Impact, but Not High-impact`? (Matched OMB's checklist on
#   paper; the agency judged it not actually high-impact. Real government data
#   has labels like this.)
# - One minute on the token counts: ~40 tokens for a sentence. What does a
#   50,000-document month do to that number? (Preview of Lab 7.1's cost
#   exercise.)

# %% [markdown]
# ## Troubleshooting
#
# - **`NameError: name 'kernel_state_check' is not defined`.** You restarted
#   the kernel or ran a cell out of order — **Run → Run All Cells**.
# - **Step 7 prints the canned reply.** No key is configured — on the class VM,
#   tell your instructor; off the VM this is expected and the lab still works.
# - **The data-inventory cell is slow.** It reads all six CSVs end to end to
#   count rows — 20–30 seconds is normal on the VM.

# %% [markdown]
# ---
# *Curious about the Python behind these steps? The full code-forward version
# of this lab lives in the `For_Python_Programmers/` folder.*
