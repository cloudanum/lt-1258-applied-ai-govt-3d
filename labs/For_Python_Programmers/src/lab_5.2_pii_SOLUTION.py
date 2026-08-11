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
# # Lab 5.2 — Detect and Mask PII in Citizen Records  *(SOLUTION / instructor copy)*
#
# **Chapter 5 — AI Security, Risks, and Responsible AI** · 40 minutes
#
# **Objectives**
# 1. Find PII in structured and free-text government data.
# 2. Mask it without destroying the record's analytic value.
# 3. Measure what your detector misses.

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
# ## Step 1 — The regex detector over citizen records
#
# **Expected:** `{"ssn": 5, "email": 6, "phone": 5}`. The sixth email is the
# payoff of the checkpoint: C-1005's `summary` is a prompt-injection payload
# containing `external-audit@not-a-real-domain.example`. The detector counts
# it — but only the human notices it is an *exfiltration instruction*, not a
# constituent's contact details. Detection is not understanding.

# %%
import json
import re
import pandas as pd
import lab_common as lc

records = lc.load_citizen_records()
blob = json.dumps(records)

hits = {"ssn": len(lc._SSN.findall(blob)),
        "email": len(lc._EMAIL.findall(blob)),
        "phone": len(lc._PHONE.findall(blob))}
print(hits)
print("\nrecord keys:", list(records[0].keys()))

# %% [markdown]
# ## Step 2 — The same detector over Chicago 311 free text
#
# **Expected:** zero hits of all three types. Zero means *this detector found
# none of these three patterns* — it does not mean "no PII": a 311 address
# plus a request type ("dead animal pick-up") can point at a specific
# household, and free-text fields can carry names a regex has no pattern for.

# %%
c311 = pd.read_csv("data/chicago_311.csv", low_memory=False)

text = "\n".join(c311[["street_address", "city", "state"]]
                 .fillna("").agg(" ".join, axis=1))
hits_311 = {"ssn": len(lc._SSN.findall(text)),
            "email": len(lc._EMAIL.findall(text)),
            "phone": len(lc._PHONE.findall(text))}
print(hits_311)

# %% [markdown]
# ## Step 3 — Three items the detector missed (expected)
#
# 1. **Names** ("Jordan Alvarez", …) — no character pattern separates a
#    person's name from any other capitalized words; this is what NER
#    (Presidio/spaCy) exists for.
# 2. **Street addresses** ("418 Maple Court, Springfield, VA 22150") —
#    structured but pattern-light, and trivially re-identifying combined with
#    a name.
# 3. **The intent in C-1005's summary** — the regex counts the attacker's
#    email but cannot flag that the sentence is an instruction to exfiltrate.
#    (Accept "the external email is a *different kind* of hit" as a variant.)

# %%
for r in records:
    print(f"\n{r['case_id']} — {r['name']}")
    print("  address:", r["address"])
    print("  summary:", r["summary"][:110])

# %% [markdown]
# ## Step 4 — Improve one pattern
#
# **Expected:** the address pattern catches all five record addresses and
# stays silent on the summaries (no false positives). Note for debrief: run
# the same pattern over 311 `street_address` and it fires on *every row* —
# correct there too, which is exactly why "detect → mask everything" needs a
# policy decision about what counts as PII in context, not just a pattern.

# %%
ADDRESS = re.compile(r"\b\d+\s+[\w ]+\s+"
                     r"(Street|St|Avenue|Ave|Lane|Court|Way|Road|Rd|Boulevard|Blvd|Drive|Dr)\b")

for r in records:
    m = ADDRESS.search(r["address"])
    print(f"{r['case_id']}: {'HIT -> ' + m.group(0) if m else 'miss'}")

fp = [r["case_id"] for r in records if ADDRESS.search(r["summary"])]
print("\nfalse positives on summaries:", fp or "none")

# %% [markdown]
# ## Step 5 — Mask, don't delete
#
# **Expected:** masked records keep `case_id`, `topic`, `status`, and the
# analytic query (open cases by topic: air quality 2, others 1 each) still
# works. The regex fallback leaves `name` intact — on the VM, Presidio's NER
# catches names too; that gap *is* the teaching point.

# %%
def _mask_value(v):
    return ADDRESS.sub("[REDACTED-ADDRESS]", lc.mask_pii(str(v)))

masked_records = [{k: _mask_value(v) for k, v in r.items()} for r in records]
print(json.dumps(masked_records[0], indent=2))

mdf = pd.DataFrame(masked_records)
print("\nstill analysable — open cases by topic:")
print(mdf[mdf["status"] == "open"]["topic"].value_counts().to_string())

# %% [markdown]
# ## Step 6 — Residual risk (worked)
#
# "After masking, the file still contains constituent names (regex cannot
# detect them reliably) and topic-plus-area combinations that could
# re-identify a household in a small community; C-1005's embedded instruction
# also survives masking untouched, because redaction removes data, not
# intent. I would release this file for aggregate analysis only, under a
# data-sharing agreement, with names stripped by an NER pass and any
# free-text field treated as untrusted input by downstream systems."
#
# ## Reflection (expected answers)
# 1. Names and intent — names require knowing what *kind* of thing a string
#    is (NER, context), and intent is not a string property at all. Regex
#    sees shapes, not semantics.
# 2. You lose the ability to contact the constituent, deduplicate by person,
#    or geocode precisely — masking trades operational utility for safety;
#    the right grain (ZIP3? county?) is a policy choice.
# 3. Not on regex alone: certify only after an NER pass, a documented
#    re-identification analysis, and a decision on free text. "The regex
#    found nothing" is evidence about three patterns, not about the file.
