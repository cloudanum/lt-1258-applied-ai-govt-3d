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
# then read the four checks below. Every check should print a green **PASS**
# (check 3 may print a yellow **SKIP** if you are not on the class VM). If any
# prints a red **FAIL**, raise your hand — your instructor has a fix for each
# one.
#
# You do **not** need to edit anything in this notebook.

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
#   `.env` file via `lab_common.load_dotenv()` — never paste a key into a
#   notebook, and this notebook never prints one (only its last four
#   characters). With no key the check reports **SKIP**, not an error.
# - **The one rule that never changes:** public or synthetic data only. Never
#   paste real agency, personal or sensitive data into any assistant during
#   this class.

# %%
# Setup cell (run it and forget it): locate the labs/ folder — where
# lab_common.py and data/ live — no matter where Jupyter was started from.
# Importing lab_common runs its .env loader: it reads the course .env file (or
# uses the key already in the environment) without ever printing the key.
import os, sys, importlib, json
from pathlib import Path

for _cand in (Path.cwd(), *Path.cwd().parents):
    if (_cand / "lab_common.py").is_file():
        os.chdir(_cand)
        if str(_cand) not in sys.path:
            sys.path.insert(0, str(_cand))
        break

import lab_common as lc

DATA = lc.DATA_DIR

GREEN, YELLOW, RED, RESET = "\033[92m", "\033[93m", "\033[91m", "\033[0m"
def result(ok, label, detail=""):
    tag = f"{GREEN}PASS{RESET}" if ok else f"{RED}FAIL{RESET}"
    print(f"[{tag}] {label}" + (f" — {detail}" if detail else ""))
    return ok

def skip(label, detail=""):
    print(f"[{YELLOW}SKIP{RESET}] {label}" + (f" — {detail}" if detail else ""))

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
# The packages the week's notebooks import. If anything is missing, the VM
# image is wrong — tell your instructor now rather than mid-lab.

# %%
needed = ["openai", "pandas", "requests", "matplotlib", "sklearn"]
missing = [m for m in needed if importlib.util.find_spec(m) is None]
result(not missing,
       "Python packages installed",
       "all present" if not missing else f"missing: {', '.join(missing)}")
import openai
print("      openai SDK version:", openai.__version__, "(need >= 1.0)")

# %% [markdown]
# ### Check 2 — Lab data files present
#
# The six public datasets from `data/MANIFEST.json` plus the supporting files
# later labs use. Everything the week needs ships on the VM, downloaded ahead
# of class because classroom networks are unreliable.

# %%
manifest = json.loads((DATA / "MANIFEST.json").read_text())
expected = [ds["file"] for ds in manifest["datasets"]] + [
    "cached_datagov.json", "citizen_records.json", "gov_memo.txt", "corpus"]
missing_files = [f for f in expected if not (DATA / f).exists()]
result(not missing_files,
       "Lab data files present",
       f"all {len(expected)} found ({len(manifest['datasets'])} datasets "
       f"+ {len(expected) - len(manifest['datasets'])} support files)"
       if not missing_files else f"missing: {', '.join(missing_files)}")

# %% [markdown]
# ### Check 3 — OpenAI API key configured and reachable
#
# On the classroom VM the key is provided for you as an environment variable.
# This check makes one tiny call to confirm it works. It prints only the *last
# four characters* of the key — never the whole key. With no key at all it
# reports **SKIP**: the week's AI cells fall back to canned replies, but on the
# class VM a SKIP means something is wrong — tell your instructor.

# %%
key = os.getenv("OPENAI_API_KEY")
model = lc.CHAT_MODEL
if not key:
    skip("OpenAI API key configured",
         "OPENAI_API_KEY is not set — on the class VM, tell your instructor; "
         "otherwise the AI cells will use canned fallbacks")
else:
    print(f"      key ends in ...{key[-4:]}   model = {model}")
    try:
        from openai import OpenAI
        client = OpenAI()
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Reply with the single word: ready"}],
        )
        result(True, "OpenAI API reachable", f"model replied: {resp.choices[0].message.content.strip()!r}")
    except Exception as e:
        result(False, "OpenAI API reachable", f"{type(e).__name__}: {e}")

# %% [markdown]
# ### Check 4 — data.gov reachable (used in Labs 2.1 / 7.2 / 7.3)
#
# This is a convenience check only. Whatever it says, the labs still work: they
# fall back to a bundled cached copy of the data. It never blocks the class.

# %%
try:
    import requests
    r = requests.get("https://catalog.data.gov/", timeout=8,
                     headers={"User-Agent": "lt-1258-lab"})
    # Any HTTP response means the host is reachable; the labs use the live API
    # when possible and the cached copy otherwise.
    result(True, "data.gov reachable", f"host responded (HTTP {r.status_code})")
except Exception as e:
    result(True, "data.gov reachable",
           f"offline ({type(e).__name__}) — labs will use the bundled cached copy")

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
#   `.env`, read by `lab_common` — so a notebook can be shared or screenshotted
#   without leaking it.)
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
# - **Check 2 FAIL (missing data files).** Confirm the notebook is running from
#   the `labs/` folder (the setup cell prints where it landed). If files are
#   genuinely missing, tell your instructor — the data pack is re-copyable.
# - **Check 3 SKIP / FAIL on the class VM.** The key injection failed — tell
#   your instructor. The week's AI cells have canned fallbacks, so nothing is
#   blocked while it is fixed.
# - **A check stopped with a Python error instead of printing.** Kernel →
#   Restart & Run All; if it repeats, call the instructor.
