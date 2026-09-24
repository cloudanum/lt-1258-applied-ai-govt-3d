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
# Cells marked `# YOUR CODE` are for you to complete. No API key is needed
# (on the VM, `mask_pii` uses Presidio; elsewhere it falls back to regex).

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
# **Tools:** pandas, Python `re`, and `lab_common` (regex patterns +
# `mask_pii`). No OpenAI key is required for any step.
#
# **Data rule:** the citizen records are synthetic precisely so this lab can
# show real PII patterns safely. Outside class, never load real citizen PII
# into an unapproved environment — that is the boundary this lab rehearses.

# %% [markdown]
# ## Steps
#
# 1. Open `lab_5.2_pii.ipynb` and run the Setup cells.
# 2. Run the regex detector over `citizen_records.json`. Record hits by type.
#    (7 min)
# 3. Run it over the free-text fields of `chicago_311.csv`. (5 min)
# 4. Find three items it **missed** by reading rows yourself. (7 min)
# 5. Improve one pattern and re-run; confirm you did not create false
#    positives. (8 min)
# 6. Mask rather than delete, keeping the field analysable. (8 min)
# 7. Write the residual risk you would report. (5 min)

# %% [markdown]
# ### Step 2 — The regex detector over citizen records (7 min)
#
# `data/citizen_records.json` holds five synthetic constituent cases.
# `lab_common` ships the course's regex patterns for SSN, email, and phone.
# Run the detector over the whole file and record hits by type.

# %%
import json
import pandas as pd
import lab_common as lc

records = lc.load_citizen_records()
blob = json.dumps(records)

hits = None
# YOUR CODE: count hits per PII type using lc._SSN, lc._EMAIL, lc._PHONE
# over `blob`. Store {"ssn": n, "email": n, "phone": n} in hits.

if hits is None:
    hits = {"ssn": len(lc._SSN.findall(blob)),
            "email": len(lc._EMAIL.findall(blob)),
            "phone": len(lc._PHONE.findall(blob))}
    print("(reference counts applied)\n")
print(hits)
print("\nrecord keys:", list(records[0].keys()))

# %% [markdown]
# #### ✓ Checkpoint
# There are 5 records with one SSN, one email, and one phone each — so why
# does one of the counts come back as **6**? Read record C-1005's `summary`
# field before you answer.

# %% [markdown]
# ### Step 3 — The same detector over Chicago 311 free text (5 min)
#
# Now point it at the free-text-ish fields of a real operational dataset.
# What does zero hits mean — and what does it *not* mean?

# %%
c311 = pd.read_csv("data/chicago_311.csv", low_memory=False)

hits_311 = None
# YOUR CODE: count SSN/email/phone hits across the street_address, city and
# state columns of c311.

if hits_311 is None:
    text = "\n".join(c311[["street_address", "city", "state"]]
                     .fillna("").agg(" ".join, axis=1))
    hits_311 = {"ssn": len(lc._SSN.findall(text)),
                "email": len(lc._EMAIL.findall(text)),
                "phone": len(lc._PHONE.findall(text))}
    print("(reference counts applied)\n")
print(hits_311)

# %% [markdown]
# ### Step 4 — Find three items the detector missed (7 min)
#
# Run the cell, read the records with your own eyes, and list three pieces of
# information the regex walked straight past. (Hint: only one of the three
# has a digit in it.)

# %%
for r in records:
    print(f"\n{r['case_id']} — {r['name']}")
    print("  address:", r["address"])
    print("  summary:", r["summary"][:110])

# %% [markdown]
# #### Three misses (write here)
#
# 1.
# 2.
# 3.

# %% [markdown]
# ### Step 5 — Improve one pattern (8 min)
#
# Pick one miss class and write a pattern for it. Then prove you did not
# create false positives: run your new pattern over text that should **not**
# match.

# %%
ADDRESS = re_pattern = None
# YOUR CODE: a compiled regex that catches US street addresses like
# "418 Maple Court, Springfield, VA 22150" (number + words + street type is
# enough — perfection is not the goal). Store it in ADDRESS.

if ADDRESS is None:
    import re
    ADDRESS = re.compile(r"\b\d+\s+[\w ]+\s+"
                         r"(Street|St|Avenue|Ave|Lane|Court|Way|Road|Rd|Boulevard|Blvd|Drive|Dr)\b")
    print("(reference pattern applied)\n")

# does it catch the record addresses?
for r in records:
    m = ADDRESS.search(r["address"])
    print(f"{r['case_id']}: {'HIT -> ' + m.group(0) if m else 'miss'}")

# false-positive check: summaries contain no addresses — it must stay silent
fp = [r["case_id"] for r in records if ADDRESS.search(r["summary"])]
print("\nfalse positives on summaries:", fp or "none")

# %% [markdown]
# ### Step 6 — Mask, don't delete (8 min)
#
# Deleting the PII fields would also delete the record's usefulness. Mask
# instead, and show that the masked file still answers an analytic question:
# how many open cases per topic?

# %%
masked_records = None
# YOUR CODE: a copy of `records` with lc.mask_pii() applied to every string
# field (and your ADDRESS pattern applied to the address field if you want
# full marks). Keep case_id, topic, status usable.

if masked_records is None:
    def _mask_value(v):
        return ADDRESS.sub("[REDACTED-ADDRESS]", lc.mask_pii(str(v)))
    masked_records = [{k: _mask_value(v) for k, v in r.items()} for r in records]
    print("(reference masking applied)\n")

print(json.dumps(masked_records[0], indent=2))

mdf = pd.DataFrame(masked_records)
print("\nstill analysable — open cases by topic:")
print(mdf[mdf["status"] == "open"]["topic"].value_counts().to_string())

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
# - **`FileNotFoundError: data/citizen_records.json`** — the kernel's working
#   directory is not `labs/`. Restart the kernel from the `labs/` folder and
#   Run All.
# - **`NameError: name 're' is not defined`** — the reference pattern imports
#   `re` inside its fallback block; if you write your own `ADDRESS` first,
#   add `import re` at the top of your cell.
# - **Presidio `ImportError` on your own machine** — expected: `mask_pii`
#   falls back to regex automatically. Only the classroom VM image has
#   Presidio.
# - **Your improved pattern finds nothing** — test it on one string directly
#   (`ADDRESS.search(records[0]['address'])`) and build it up token by token.
# - **False positives on summaries** — your pattern is too broad (usually a
#   bare `\d+` or a too-greedy `[\w ]+`). Tighten it until the check prints
#   `none`.
