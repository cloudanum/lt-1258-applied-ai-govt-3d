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
# OpenAI API via `lab_common` (canned fallback when no key)*
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
# - **API key:** the environment cell below imports `lab_common`, whose loader
#   reads `OPENAI_API_KEY` from the environment (classroom VM) or from the
#   course `.env` file. It prints the `.env` path and model alias — **never
#   the key**. With no key, the model cell uses a realistic canned reply, so
#   the tour completes either way.
# - **The one rule that never changes:** public or synthetic data only. Never
#   paste real agency, personal or sensitive data into any assistant.
# - Cells marked `# YOUR CODE` are for you to complete. Each has a reference
#   fallback that runs if you leave it blank, so the notebook never gets stuck
#   — replace the fallback with your own line when you can.

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
# 4. **(3 min)** Load `federal_ai_use_cases.csv` with pandas. Print `.shape`
#    and `.columns`.
# 5. **(2 min)** Answer in the notebook: how many use cases are flagged
#    `is_high_impact`?
# 6. **(3 min)** Load `chicago_311.csv` and print the five most common
#    `sr_type` values.
# 7. **(3 min)** Run the **first API call** cell: a one-sentence prompt,
#    printing the reply and the token counts.
# 8. **(2 min)** Deliberately break something: restart the kernel, re-run only
#    the last cell, and read the error. Then **Run All** to recover.

# %% [markdown]
# ### Step 2 — The environment cell (provided)
#
# This cell finds the `labs/` folder, imports `lab_common` (which loads the
# `.env` file), and prints where the key came from — **never the key itself**.
# On the VM the key is injected for you; off the VM, `lab_common` reads it from
# a `.env` file at the course root.

# %%
# Locate the labs/ folder no matter where Jupyter was started from.
import os, sys
from pathlib import Path

for _cand in (Path.cwd(), *Path.cwd().parents):
    if (_cand / "lab_common.py").is_file():
        os.chdir(_cand)
        if str(_cand) not in sys.path:
            sys.path.insert(0, str(_cand))
        break

import lab_common as lc

print(".env loaded from:", lc.DOTENV_PATH or "(none — relying on environment variables)")
print("chat model alias  :", lc.CHAT_MODEL)
print("embedding model   :", lc.EMBED_MODEL)
print("API key configured:", bool(lc.get_client()))
print("data directory    :", lc.DATA_DIR)

# %% [markdown]
# ### Step 3 — Data inventory (provided)
#
# `data/MANIFEST.json` says where each dataset came from and what it is for.
# This cell prints each file with its row count and one-line description.

# %%
import json
import pandas as pd

manifest = json.loads((lc.DATA_DIR / "MANIFEST.json").read_text())
print(f"data pack retrieved: {manifest['retrieved']}\n")
for ds in manifest["datasets"]:
    n = len(pd.read_csv(lc.DATA_DIR / ds["file"], low_memory=False))
    print(f"{ds['file']:28s} {n:>6,} rows — {ds['description']}")

# %% [markdown]
# ### Step 4 — Load the federal AI use case inventory
#
# This CSV is the course's own subject matter as data: every AI use case the
# agencies reported to OMB. Load it and print its shape and columns.

# %%
uc = None
# YOUR CODE: read data/federal_ai_use_cases.csv into `uc` with pd.read_csv
# (lc.DATA_DIR points at the data/ folder; use encoding="utf-8-sig" — the file
# starts with a byte-order mark). Then print uc.shape and list(uc.columns).

if uc is None:
    uc = pd.read_csv(lc.DATA_DIR / "federal_ai_use_cases.csv", encoding="utf-8-sig")
    print("(reference load applied — replace with your own line above)\n")
print("shape:", uc.shape)
print("columns:", list(uc.columns))

# %% [markdown]
# ### Step 5 — How many use cases are flagged high-impact?
#
# The `is_high_impact` column answers OMB's risk question. Count how many use
# cases are flagged `High-impact` — and notice what *other* values the column
# contains while you are at it.

# %%
high_impact_count = None
# YOUR CODE: count rows where uc["is_high_impact"] == "High-impact".

if high_impact_count is None:
    high_impact_count = int((uc["is_high_impact"] == "High-impact").sum())
    print("(reference count applied)\n")
print(uc["is_high_impact"].value_counts().to_string())
print(f"\nflagged High-impact: {high_impact_count} of {len(uc)}")

# %% [markdown]
# ### Step 6 — Chicago 311: the five most common request types
#
# `chicago_311.csv` is a recent extract of the City's 311 service requests —
# deliberately real and messy. You will meet it again in Labs 5.2, 6.1 and 6.2.

# %%
top5 = None
# YOUR CODE: load data/chicago_311.csv (low_memory=False) and store the five
# most common values of the "sr_type" column in `top5`.

if top5 is None:
    _c311 = pd.read_csv(lc.DATA_DIR / "chicago_311.csv", low_memory=False)
    top5 = _c311["sr_type"].value_counts().head(5)
    print("(reference load applied)\n")
print(top5.to_string())

# %% [markdown]
# ### Step 7 — Your first API call
#
# One sentence in, one sentence out, and read the token counts — the unit you
# pay in. If no key is configured you get a canned reply so the tour still
# works; the token line tells you it is offline.

# %%
CANNED_REPLY = (
    "The OMB AI use case inventory tracks how federal agencies are using "
    "artificial intelligence — each reported system's purpose, development "
    "stage, and whether it is high-impact."
)

client = lc.get_client()
if client is not None:
    resp = client.chat.completions.create(
        model=lc.CHAT_MODEL,
        messages=[{"role": "user", "content":
                   "In one sentence, what does the OMB federal AI use case "
                   "inventory track?"}],
    )
    print(resp.choices[0].message.content)
    print(f"\ntokens — prompt: {resp.usage.prompt_tokens}, "
          f"completion: {resp.usage.completion_tokens}, "
          f"total: {resp.usage.total_tokens}")
else:
    print(lc.chat([{"role": "user", "content": "..."}], offline=CANNED_REPLY))
    print("\n(offline canned reply — token counts need a live call; "
          "a call this size is typically ~40 tokens total)")

# %% [markdown]
# ### Step 8 — Break it on purpose
#
# 1. **Kernel menu → Restart Kernel** (the circular arrow). This wipes every
#    variable.
# 2. Re-run *only* this cell. Read the `NameError`: `lc` no longer exists
#    because the import cell above has not run in the new kernel.
# 3. **Run menu → Run All Cells** to recover.
#
# This is the single most common notebook confusion in class — make it happen
# now, on purpose, when nothing is at stake.

# %%
print("lc is still defined:", "lc" in dir(), "| uc rows:", len(uc))

# %% [markdown]
# ## Deliverable
#
# A fully run notebook (Run All, top to bottom, no errors) with:
# 1. The data inventory printed in Step 3.
# 2. Your high-impact count from Step 5.
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
# - **`NameError: name 'lc' is not defined`.** You restarted the kernel or ran
#   a cell out of order — **Run → Run All Cells**.
# - **`FileNotFoundError: data/...`.** You are not running from the `labs/`
#   folder; the Step 2 setup cell should have fixed this — re-run from the top.
# - **`UnicodeDecodeError` or a column named `\ufeff...`.** The federal CSV has
#   a byte-order mark; load it with `encoding="utf-8-sig"`.
# - **Step 7 prints the canned reply.** No key is configured — on the class VM,
#   tell your instructor; off the VM this is expected and the lab still works.
# - **The data-inventory cell is slow.** It reads all six CSVs end to end to
#   count rows — 20–30 seconds is normal on the VM.
