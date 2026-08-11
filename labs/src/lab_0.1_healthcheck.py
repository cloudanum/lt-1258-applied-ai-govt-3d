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
# # Lab 0.1 — Environment Healthcheck
#
# *Course 1258 — Applied AI for Government IT Professionals · Ch00 Course
# Launch and Lab Environment · DO NOW 0.1 · 15 minutes · CloudShare VM
# (JupyterLab)*
#
# Nothing else in the week works until this is green, so it is the first thing
# you do. Run this notebook first, before Chapter 1: **Run → Run All Cells**,
# then read the four checks below. **Checks 1–3 should read PASS** — that is
# what "ready" looks like. **Check 4 is informational** and prints `INFO`
# whatever it finds. If any of checks 1–3 prints a red **FAIL**, or a yellow
# **SKIP** on the class VM, raise your hand — your instructor has a fix for each
# one. (Off the class VM, a SKIP on check 3 is expected: there is no key, and
# the AI cells fall back to canned replies.)
#
# You do **not** need to edit anything in this notebook — just run it.

# %% [markdown]
# ## Objectives
#
# By the end of this activity, you will:
#
# - Reach a running JupyterLab in your CloudShare VM.
# - Prove packages, data files, the API key and network are all ready.

# %% [markdown]
# ## Setup
#
# - **Files checked:** the six course datasets listed in `data/MANIFEST.json`,
#   plus the supporting files later labs use (`cached_datagov.json`,
#   `citizen_records.json`, `gov_memo.txt`, `corpus/`).
# - **API key:** read from the environment (classroom VM) or from the course
#   `.env` file — never paste a key into a notebook, and this notebook never
#   prints one (only its last four characters). With no key the check reports
#   **SKIP**, not an error.
# - **The one rule that never changes:** public or synthetic data only. Never
#   paste real agency, personal or sensitive data into any assistant during
#   this class.

# %%
# ▶ Setup — run this cell first (click it, then Shift+Enter).
# It loads the course helper functions the checks below use.
from lab_helpers import *

# %% [markdown]
# ## Steps
#
# 1. **(5 min, before this notebook)** Sign in to **My Learning Tree**, open
#    the course page, click **Launch Lab**, then the **in-browser Viewer** (not
#    RDP — it errors). Firefox opens JupyterLab automatically; if not,
#    double-click **Start Labs** (password `pw` if asked).
# 2. **(2 min)** Open `lab_0.1_healthcheck.ipynb` (this file) and choose
#    **Run → Run All Cells**.
# 3. **(8 min)** Read the four checks below. Checks 1–3 should read **PASS** —
#    that is what "ready" looks like. Check 4 (network) is informational: a
#    cached copy of every dataset ships on the VM, so the labs work either way.

# %% [markdown]
# ### Check 1 — Python packages
#
# The packages the week's notebooks need. If anything is missing, the VM
# image is wrong — tell your instructor now rather than mid-lab.

# %%
check_python_packages()

# %% [markdown]
# ### Check 2 — Lab data files present
#
# The six public datasets from `data/MANIFEST.json` plus the supporting files
# later labs use. Everything the week needs ships on the VM, downloaded ahead
# of class because classroom networks are unreliable.

# %%
check_data_files()

# %% [markdown]
# ### Check 3 — OpenAI API key configured and reachable
#
# On the classroom VM the key is provided for you as an environment variable.
# This check makes one tiny call to confirm it works. It prints only the *last
# four characters* of the key — never the whole key. With no key at all it
# reports **SKIP**: the week's AI cells fall back to canned replies, but on the
# class VM a SKIP means something is wrong — tell your instructor.

# %%
check_api_key()

# %% [markdown]
# ### Check 4 — data.gov reachable (used in Labs 2.1 / 7.2 / 7.3)
#
# This is a convenience check only. Whatever it says, the labs still work: they
# fall back to a bundled cached copy of the data. It never blocks the class.

# %%
check_datagov_reachable()

# %% [markdown]
# ## Deliverable
#
# A fully run notebook (Run All, top to bottom) with checks 1–3 showing **PASS**
# — leave it on screen for your instructor, or raise your hand on any **FAIL**
# or unexpected **SKIP**. Check 4 may say the cached copy will be used; that is
# fine.

# %% [markdown]
# ## Reflection
#
# 1. Which check proves the OpenAI key is readable from `.env` / the environment?
# 2. If check 2 failed, what would you look at first?

# %% [markdown]
# ## Debrief (instructor-led)
#
# - Poll the room: who is all-green? Anyone with a FAIL — which check? Fix the
#   stragglers now; nothing later waits for this.
# - Ask: where does the key live, and why not in the notebook? (Environment /
#   `.env`, loaded by the course helpers — so a notebook can be shared or
#   screenshotted without leaking it.)
# - Ask: which check would fail first if the network were down? (Check 3 — the
#   only one that needs to leave the VM. Check 4 only *reports* the outage.)

# %% [markdown]
# ## Troubleshooting
#
# - **The RDP button errors.** Use the **in-browser Viewer** instead.
# - **JupyterLab did not open.** Double-click **Start Labs** on the desktop;
#   the password is `pw` if asked.
# - **Check 1 FAIL (missing packages).** The VM image is incomplete — tell your
#   instructor; do not try to `pip install` mid-class.
# - **Check 2 FAIL (missing data files).** The data pack may not have copied —
#   tell your instructor; it is re-copyable.
# - **Check 3 SKIP / FAIL on the class VM.** The key injection failed — tell
#   your instructor. The week's AI cells have canned fallbacks, so nothing is
#   blocked while it is fixed.
# - **A check stopped with a Python error instead of printing.** Kernel →
#   Restart & Run All; if it repeats, call the instructor.

# %% [markdown]
# ---
# *Curious about the Python behind these checks? The full code-forward version
# of this lab lives in the `For_Python_Programmers/` folder.*
