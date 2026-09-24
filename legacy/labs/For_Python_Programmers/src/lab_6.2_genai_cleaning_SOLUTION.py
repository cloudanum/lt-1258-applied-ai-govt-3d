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
# # Lab 6.2 — GenAI-Assisted Cleaning with Structured Outputs  *(SOLUTION / instructor copy)*
#
# **Chapter 6 — Data for AI: Collection, Quality, and Governance** · 35 minutes
#
# **Objectives**
# 1. Use a model to normalise messy categorical data at volume.
# 2. Enforce a schema so the output is machine-usable.
# 3. Audit the model's work and measure what it got wrong.

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
# ## Step 1 — Extract 60 raw values

# %%
import pandas as pd
from lab_common import chat_json

df = pd.read_csv("data/chicago_311.csv", low_memory=False)

raw_values = df["sr_type"].value_counts().head(60).index.tolist()
print(f"{len(raw_values)} raw values, e.g.: {raw_values[:6]}")

CANONICAL = [
    "Noise", "Information & 311 Services", "Water & Drainage",
    "Urban Forestry", "Graffiti & Property Damage",
    "Streets & Transportation", "Sanitation & Waste",
    "Pest & Animal Control", "Buildings & Housing",
    "Code Enforcement & Violations", "Other",
]

# %% [markdown]
# ## Step 2 — Call the model with a strict JSON schema
#
# **Worked prompt** below. Offline, the canned mapping plays the model's
# part — including its characteristic mistake (next steps).

# %%
def canned_mapping(values):
    """Offline stand-in for the model's mapping (keyword rules, as a real
    model would infer from the label text)."""
    RULES = [
        (("aircraft noise",), ("Noise", 0.98)),
        (("information only",), ("Information & 311 Services", 0.97)),
        (("graffiti",), ("Graffiti & Property Damage", 0.95)),
        (("tree", "weed"), ("Urban Forestry", 0.92)),
        (("water", "sewer", "leak"), ("Water & Drainage", 0.9)),
        (("rodent", "rat", "animal", "pet "), ("Pest & Animal Control", 0.9)),
        (("sanitation", "garbage", "recycling", "yard waste", "dumping",
          "vacant lot", "dead animal"), ("Sanitation & Waste", 0.9)),
        (("building", "plumbing", "porch", "restaurant", "business",
          "housing", "café", "wage", "cab "), ("Buildings & Housing", 0.85)),
        (("vehicle", "parking", "sticker"), ("Streets & Transportation", 0.85)),
        (("street", "traffic", "pothole", "sidewalk", "sign", "alley",
          "scooter", "divvy"), ("Streets & Transportation", 0.88)),
    ]
    out = []
    for v in values:
        low = v.lower()
        canonical, conf = next((c for keys, c in RULES
                                if any(k in low for k in keys)), ("Other", 0.5))
        out.append({"raw": v, "canonical": canonical, "confidence": conf})
    return {"mappings": out}

MAPPING_PROMPT = (
    "You are normalizing Chicago 311 request-type labels into a controlled "
    "vocabulary for a city dashboard.\n"
    "VOCABULARY: " + ", ".join(CANONICAL) + ".\n"
    "Return JSON only: {\"mappings\": [{\"raw\": ..., \"canonical\": ..., "
    "\"confidence\": 0-1}, ...]} with exactly one object per input value. "
    "If no category fits well, use \"Other\" with confidence <= 0.5 rather "
    "than forcing a fit."
)

mappings = chat_json(
    [{"role": "user", "content":
      MAPPING_PROMPT + "\n\nVALUES:\n" + "\n".join(raw_values)}],
    offline=canned_mapping(raw_values))

mapped = pd.DataFrame(mappings["mappings"])
print(mapped.head(10).to_string(index=False))

# %% [markdown]
# ## Step 3 — Fail loudly if it does not validate

# %%
def validate(items, vocab):
    for i, m in enumerate(items):
        assert set(m) >= {"raw", "canonical", "confidence"}, f"item {i}: missing keys"
        assert m["canonical"] in vocab, f"item {i}: '{m['canonical']}' not in vocabulary"
        assert 0.0 <= m["confidence"] <= 1.0, f"item {i}: confidence out of range"
    return True

print("valid:", validate(mappings["mappings"], CANONICAL))

bad = [dict(m) for m in mappings["mappings"]]
bad[3]["canonical"] = "Stuff"
try:
    validate(bad, CANONICAL)
    print("PROBLEM: validator accepted a bad value")
except AssertionError as e:
    print(f"validator correctly rejected the corrupt item ({e})")

# %% [markdown]
# ## Step 4 — Audit: sample 20 and check by hand
#
# **Expected errors in this sample (seed 7):** `Sanitation Code Violation`
# is the systematic one — mapped to *Sanitation & Waste* at 0.9 confidence
# when it is a code-enforcement action. Depending on the draw, students may
# also flag `Water Lead Test Kit Request` (a health-testing programme, not
# drainage) and `Finance Parking Code Enforcement Review` (revenue
# enforcement, not transportation). Expected error rate: **1–3 of 20
# (5–15%)**.

# %%
audit_sample = mapped.sample(20, random_state=7).sort_index()
print(audit_sample.to_string())

errors_found = int(audit_sample["raw"].str.contains(
    "Sanitation Code Violation|Water Lead Test Kit|Finance Parking").sum())
print(f"error rate: {errors_found / 20:.0%} of the audited sample "
      f"({errors_found} wrong of 20)")

# %% [markdown]
# ## Step 5 — The high-confidence wrong mapping
#
# **Expected pick:** `Sanitation Code Violation -> Sanitation & Waste`,
# confidence 0.9. The word "Sanitation" is a *department name*, not a service
# description — the model matched the surface token and never saw the
# enforcement semantics. This is the canonical GenAI-cleaning failure mode:
# the label is lexically close to the wrong category and the model's
# confidence reflects lexical match strength, not judgement.

# %%
confident = mapped[mapped["confidence"] >= 0.85]
print(confident.to_string(index=False))
print("\nthe confidently wrong one:")
print(confident[confident["raw"] == "Sanitation Code Violation"].to_string(index=False))

# %% [markdown]
# ## Step 6 — Tighten the prompt, re-run the failures
#
# **Expected:** all five 'Violation' labels move to
# `Code Enforcement & Violations`. One sentence of domain knowledge fixed a
# whole error class — cheaper than more data, faster than a bigger model.
# And the audit question repeats: did the fix break anything that was right?
# (Re-run the validator and eyeball the full table again — it did not.)

# %%
TIGHTENER = ("\nIMPORTANT: distinguish service delivery from enforcement — "
             "labels containing 'Violation' are code-enforcement actions "
             "(Code Enforcement & Violations), not service requests, even "
             "when the enforcing department sounds like a service (e.g. "
             "Sanitation).")

def canned_mapping_v2(values):
    base = canned_mapping(values)["mappings"]
    for m in base:
        if "violation" in m["raw"].lower():
            m.update(canonical="Code Enforcement & Violations", confidence=0.9)
    return {"mappings": base}

failures = mapped[mapped["raw"].str.contains("Violation", case=False)]["raw"].tolist()
print("re-running failures:", failures)

remapped = chat_json(
    [{"role": "user", "content": MAPPING_PROMPT + TIGHTENER
      + "\n\nVALUES:\n" + "\n".join(failures)}],
    offline=canned_mapping_v2(failures))
remap_df = pd.DataFrame(remapped["mappings"])
print(remap_df.to_string(index=False))
print("re-mapped valid:", validate(remapped["mappings"], CANONICAL))

# %% [markdown]
# ## Step 7 — Human-review rule (worked)
#
# "Route to human review: (a) every mapping with confidence < 0.8, (b) 100%
# of mappings for any *new* vocabulary category in its first month, and (c)
# a 5% random audit of the remainder — with the measured 5–15% base error
# rate, unaudited automation is not defensible for anything feeding a public
# dashboard."
#
# ## Reflection (expected answers)
# 1. For a public dashboard: near zero on high-volume categories — and the
#    decision belongs to the data owner and the accountability chain (the
#    official who signs the dashboard), not the person who wrote the prompt.
# 2. Weakly — confidence tracks lexical match strength, so the most
#    dangerous errors are the *confident* ones (Sanitation Code Violation at
#    0.9). Confidence is useful for triage order, not for trust.
# 3. GenAI cannot fix missing values (the 100%-null columns), cannot detect
#    duplicates, and cannot judge accuracy against the real world — those
#    need collection changes, keys, and audits respectively.
