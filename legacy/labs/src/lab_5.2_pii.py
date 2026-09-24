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
# # Lab 5.2 — Detect and Mask PII in Citizen Records
#
# *Chapter 5 — AI Security, Risks, and Responsible AI · 40 minutes ·
# JupyterLab with pandas and regex (Presidio on the VM, regex fallback
# elsewhere) — no API key needed*
#
# Before any dataset leaves your boundary — to a vendor, a portal, or a
# model — someone has to find the PII. Today that is you. **All records here
# are synthetic.**
#
# Cells marked `# YOUR TURN` ask you to change a simple value and re-run.
# No API key is needed (on the VM, the masking helper uses Presidio;
# elsewhere it falls back to regex).

# %% [markdown]
# ## Objectives
#
# By the end of this lab, you will:
#
# - Find PII in structured and free-text government data.
# - Mask it without destroying the record's analytic value.
# - Measure what your detector misses.

# %% [markdown]
# ## Setup
#
# **Datasets and files** (all under `labs/data/`):
#
# - `citizen_records.json` — five **synthetic** constituent cases. Every
#   name, SSN, email, phone and address is fabricated for training (the
#   injection payload in case C-1005 is intentional — part of the exercise)
# - `chicago_311.csv` — 4,000 real Chicago 311 service requests, for the
#   free-text scan (real, public; see `data/MANIFEST.json`)
#
# **Tools:** pandas, the course's regex patterns, and the course masking
# helper. No OpenAI key is required for any step.
#
# **Data rule:** the citizen records are synthetic precisely so this lab can
# show real PII patterns safely. Outside class, never load real citizen PII
# into an unapproved environment — that is the boundary this lab rehearses.
#
# **How this notebook works:** every step is one provided cell — run it with
# Shift+Enter and read what it prints. Cells marked `# YOUR TURN` ask you to
# change a simple value and re-run the cell. Everything runs as shipped, so
# you can never get stuck.

# %%
# ▶ Setup — run this cell first (click it, then Shift+Enter).
# It loads the course helper functions used by every step below.
from lab_helpers import *

# %% [markdown]
# ## Steps
#
# 1. Run the Setup cell above.
# 2. Run the regex detector over `citizen_records.json`. Record hits by type.
#    (7 min)
# 3. Run it over the free-text fields of `chicago_311.csv`. (5 min)
# 4. Find three items it **missed** by reading rows yourself. (7 min)
# 5. Improve one pattern and re-run; confirm you did not create false
#    positives. (8 min)
# 6. Mask rather than delete, keeping the field analysable. (8 min)
# 7. Write the residual risk you would report. (5 min)

# %% [markdown]
# ### Step 2 — The regex detector over citizen records (7 min, provided)
#
# `data/citizen_records.json` holds five synthetic constituent cases. The
# course ships ready-made patterns for SSN, email, and phone. Run the next
# two cells: the first loads the records, the second runs the detector over
# the whole file and prints the hits by type.

# %%
records = load_pii_records()

# %%
scan_records_for_pii(records)

# %% [markdown]
# #### ✓ Checkpoint
# There are 5 records with one SSN, one email, and one phone each — so why
# does one of the counts come back as **6**? Read record C-1005's `summary`
# field before you answer.

# %% [markdown]
# ### Step 3 — The same detector over Chicago 311 free text (5 min, provided)
#
# Run this cell to point the same detector at the free-text-ish fields of a
# real operational dataset. What does zero hits mean — and what does it
# *not* mean?

# %%
scan_311_for_pii()

# %% [markdown]
# ### Step 4 — Find three items the detector missed (7 min)
#
# Run the cell, read the records with your own eyes, and list three pieces of
# information the regex walked straight past. (Hint: only one of the three
# has a digit in it.)

# %%
show_records_for_review(records)

# %% [markdown]
# #### Three misses (write here)
#
# 1.
# 2.
# 3.

# %% [markdown]
# ### Step 5 — Improve one pattern (8 min)
#
# The cell below carries a pattern (a piece of search text) that catches US
# street addresses like "418 Maple Court, Springfield, VA 22150". Run it: it
# checks the pattern against every record's address — and, to prove it
# creates no false positives, against the summaries, which contain no
# addresses and must stay silent. Then try improving it.

# %%
ADDRESS_PATTERN = r"\b\d+\s+[\w ]+\s+(Street|St|Avenue|Ave|Lane|Court|Way|Road|Rd|Boulevard|Blvd|Drive|Dr)\b"   # ← YOUR TURN: edit this search text to catch more (or fewer) address styles, then re-run — the false-positive check must still print "none"
test_address_pattern(records, ADDRESS_PATTERN)

# %% [markdown]
# ### Step 6 — Mask, don't delete (8 min, provided)
#
# Deleting the PII fields would also delete the record's usefulness. Run this
# cell to mask instead (using your pattern from Step 5), and show that the
# masked file still answers an analytic question: how many open cases per
# topic?

# %%
masked_records = mask_records_pii(records, ADDRESS_PATTERN)

# %% [markdown]
# ### Step 7 — Residual risk (5 min)
#
# Masking SSN/email/phone/address still leaves `name` (regex cannot reliably
# find names — Presidio can, on the VM) and the *combination* of topic +
# address-general-area can re-identify a household. And note what masking did
# **not** do to C-1005: the injection payload is still there, still an
# instruction — redaction is not sanitisation.
#
# #### Residual risk you would report (write here)
#
# *
# *

# %% [markdown]
# ## Deliverable
# 1. Hit counts by type for both datasets.
# 2. Your three missed items and your improved pattern with its
#    false-positive check.
# 3. The masked records + the analytic query that still works.
# 4. Your residual-risk statement.

# %% [markdown]
# ## Reflection
# 1. What did the detector miss, and why is that class hard for regex?
# 2. What did masking cost you analytically?
# 3. Would you certify this file as safe to share? On what basis?

# %% [markdown]
# ## Debrief (instructor-led)
#
# - **The count of 6.** Who figured out why one PII type over-counted? What
#   does that say about "hits" as a metric?
# - **Recall vs precision.** Your improved pattern — did anyone create a
#   false positive proving the trade-off? Which error is worse before a
#   release?
# - **C-1005.** Masking left the injection payload untouched. What control —
#   other than redaction — would catch it?

# %% [markdown]
# ## Troubleshooting
#
# - **A red error mentioning `citizen_records.json` or "No such file".** The
#   course data pack is missing or incomplete — tell your instructor; run the
#   Day-0 healthcheck to confirm.
# - **A red error after you edited `ADDRESS_PATTERN`.** The search text is no
#   longer valid — undo your edit (the shipped value above always works) and
#   change it more carefully, one piece at a time.
# - **Names are masked on the classroom VM but not on your own machine (or
#   vice versa).** Expected: the VM uses a smarter name-aware masker
#   (Presidio); elsewhere the helper falls back to simpler pattern-matching
#   automatically. That gap is one of the teaching points.
# - **Your improved pattern finds nothing.** Put the shipped value back,
#   confirm it catches all five addresses, then change one piece at a time.
# - **False positives on summaries.** Your pattern is too broad (usually a
#   bare number or a too-greedy word run). Tighten it until the check prints
#   `none`.

# %% [markdown]
# ---
# *Curious about the Python behind these steps? The full code-forward version
# of this lab lives in the `For_Python_Programmers/` folder.*
