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
# # Lab 6.2 — GenAI-Assisted Cleaning with Structured Outputs
#
# *Chapter 6 — Data for AI: Collection, Quality, and Governance · 35 minutes
# · JupyterLab with pandas and the OpenAI API via `lab_common` (canned
# offline fallback)*
#
# Lab 6.1 found the defects. Now fix a class of them with GenAI — and then
# check the fixer, because schema-correct is not the same as correct.
#
# Cells marked `# YOUR CODE` are for you. Offline, `chat_json` returns a
# realistic canned mapping so every step still runs.

# %% [markdown]
# ## Objectives
#
# By the end of this lab, you will:
#
# - Use a model to normalise messy categorical data at volume.
# - Enforce a schema so the output is machine-usable.
# - Audit the model's work and measure what it got wrong.

# %% [markdown]
# ## Setup
#
# **Datasets and files** (all under `labs/data/`):
#
# - `chicago_311.csv` — the same 4,000-request extract you assessed in
#   Lab 6.1 (real, public; see `data/MANIFEST.json`). Target column:
#   `sr_type`, 68 free-typed request labels.
#
# **Tools:** pandas, plus the OpenAI chat API through
# `lab_common.chat_json()` (JSON mode). Offline, a keyword-rule canned
# mapping stands in for the model so every step still runs.
#
# **Data rule:** the extract is genuinely public data. The values sent to
#   the model are service-request labels only — never send resident-level
#   fields (addresses, names) to an external API.

# %%
# API key status — lab_common loads OPENAI_API_KEY from the environment
# (classroom VM) or the course .env file at import. The key is never printed.
# With no key, every AI call below falls back to a realistic canned mapping.
import lab_common as lc

if lc.online():
    print(f"OpenAI API key found — live mode (model: {lc.CHAT_MODEL}).")
else:
    print("No API key found — offline mode: AI calls return realistic canned "
          "mappings, so every step still runs.\nAsk your instructor if you "
          "expected a key on this machine.")

# %% [markdown]
# ## Steps
#
# 1. Open `lab_6.2_genai_cleaning.ipynb` and run the Setup cells.
# 2. Extract 60 raw values from a messy categorical column. (4 min)
# 3. Call the model with a **strict JSON schema**:
#    `{raw, canonical, confidence}`. (6 min)
# 4. Parse the response; fail loudly if it does not validate. (5 min)
# 5. Sample 20 mappings and check them by hand. Record the error rate.
#    (7 min)
# 6. Find one high-confidence wrong mapping and explain what misled it.
#    (5 min)
# 7. Re-run the failures with a tightened prompt and compare. (5 min)
# 8. State the human-review rate you would require in production. (3 min)

# %% [markdown]
# ### Step 2 — Extract 60 raw values (4 min)
#
# The target: `sr_type` in the 311 extract — 68 free-typed request labels.
# The goal: map each to a **controlled vocabulary** of service categories a
# dashboard can group by.

# %%
import pandas as pd
from lab_common import chat_json

df = pd.read_csv("data/chicago_311.csv", low_memory=False)

raw_values = None
# YOUR CODE: the 60 most frequent distinct sr_type values, as a list.

if raw_values is None:
    raw_values = df["sr_type"].value_counts().head(60).index.tolist()
    print("(reference extraction applied)\n")
print(f"{len(raw_values)} raw values, e.g.: {raw_values[:6]}")

CANONICAL = [
    "Noise", "Information & 311 Services", "Water & Drainage",
    "Urban Forestry", "Graffiti & Property Damage",
    "Streets & Transportation", "Sanitation & Waste",
    "Pest & Animal Control", "Buildings & Housing",
    "Code Enforcement & Violations", "Other",
]

# %% [markdown]
# ### Step 3 — Call the model with a strict JSON schema (6 min)
#
# Ask for one object per raw value: `{raw, canonical, confidence}` —
# `canonical` restricted to the controlled vocabulary, `confidence` 0–1.
# JSON mode makes the answer machine-usable; the schema makes it *checkable*.

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

MAPPING_PROMPT = None
# YOUR CODE: the prompt. It must (a) give the controlled vocabulary, (b)
# demand JSON {"mappings": [{raw, canonical, confidence}, ...]} with one
# object per input value, (c) tell the model to use "Other" with low
# confidence rather than force a fit.

mappings = None
if MAPPING_PROMPT:
    mappings = chat_json(
        [{"role": "user", "content":
          MAPPING_PROMPT + "\n\nVALUES:\n" + "\n".join(raw_values)}],
        offline=canned_mapping(raw_values))
if mappings is None:
    mappings = canned_mapping(raw_values)
    print("(canned mapping applied — write MAPPING_PROMPT above to run your own)\n")

mapped = pd.DataFrame(mappings["mappings"])
print(mapped.head(10).to_string(index=False))

# %% [markdown]
# ### Step 4 — Fail loudly if it does not validate (5 min)
#
# A schema you never check is a hope, not a contract. Validate every item;
# raise on the first violation. The demo at the bottom proves the check bites.

# %%
def validate(items, vocab):
    for i, m in enumerate(items):
        assert set(m) >= {"raw", "canonical", "confidence"}, f"item {i}: missing keys"
        assert m["canonical"] in vocab, f"item {i}: '{m['canonical']}' not in vocabulary"
        assert 0.0 <= m["confidence"] <= 1.0, f"item {i}: confidence out of range"
    return True

print("valid:", validate(mappings["mappings"], CANONICAL))

# prove it fails loudly: corrupt one entry on purpose
bad = [dict(m) for m in mappings["mappings"]]
bad[3]["canonical"] = "Stuff"
try:
    validate(bad, CANONICAL)
    print("PROBLEM: validator accepted a bad value")
except AssertionError as e:
    print(f"validator correctly rejected the corrupt item ({e})")

# %% [markdown]
# ### Step 5 — Audit: sample 20 and check by hand (7 min)
#
# The model's schema passed; now grade its *judgement*. Read the 20 sampled
# mappings below, mark the wrong ones in the markdown cell, and compute the
# error rate.

# %%
audit_sample = mapped.sample(20, random_state=7).sort_index()
print(audit_sample.to_string())

errors_found = None
# YOUR CODE: how many of the 20 are wrong? (Read each one. Set errors_found
# to your count so the error rate prints.)

if errors_found is None:
    errors_found = 1  # placeholder — replace with YOUR count from reading
    print("(placeholder count of 1 applied — set your own)\n")
print(f"error rate: {errors_found / 20:.0%} of the audited sample")

# %% [markdown]
# #### Which were wrong, and why (write here)
#
# -
# -

# %% [markdown]
# ### Step 6 — The high-confidence wrong mapping (5 min)
#
# Filter to confidence ≥ 0.85 and find one mapping that is *confidently*
# wrong. What in the label text misled the model?

# %%
confident = mapped[mapped["confidence"] >= 0.85]
print(confident.to_string(index=False))

# %% [markdown]
# #### Your pick and explanation (write here)
#
# *Mapping, what it should be, and what in the text misled the model:*
#
# -

# %% [markdown]
# ### Step 7 — Tighten the prompt, re-run the failures (5 min)
#
# One sentence of domain knowledge in the prompt fixes a whole error class.
# Tighten, re-run only the failures, and compare.

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

remapped = None
if MAPPING_PROMPT:
    remapped = chat_json(
        [{"role": "user", "content": MAPPING_PROMPT + TIGHTENER
          + "\n\nVALUES:\n" + "\n".join(failures)}],
        offline=canned_mapping_v2(failures))
if remapped is None:
    remapped = canned_mapping_v2(failures)
    print("(canned re-mapping applied)\n")
print(pd.DataFrame(remapped["mappings"]).to_string(index=False))

# %% [markdown]
# ### Step 8 — State the human-review rate (3 min)
#
# Given your measured error rate, what share of mappings would you route to a
# human in production — all, a sample, or only low-confidence ones? Write it
# as an operational rule with a number.
#
# #### Your rule (write here)
#
# -

# %% [markdown]
# ## Deliverable
# 1. The mapping table with validation passing (and the deliberate failure).
# 2. Your audited error rate and the high-confidence wrong mapping explained.
# 3. The tightened-prompt re-run.
# 4. Your human-review rule.

# %% [markdown]
# ## Reflection
# 1. What error rate would you accept, and who decides?
# 2. Did confidence correlate with correctness?
# 3. Which defects from Lab 6.1 can GenAI *not* fix?

# %% [markdown]
# ## Debrief (instructor-led)
#
# - **Compare error rates.** What did different auditors count as "wrong"?
#   Did the disagreement itself reveal an ambiguity in the controlled
#   vocabulary?
# - **Confidence as a routing signal.** Would routing only low-confidence
#   mappings to humans have caught your high-confidence wrong one?
# - **Cost of the loop.** Each tightened prompt is a re-run and a re-audit.
#   At what fleet size does that stop being worth it versus a lookup table
#   curated by hand?

# %% [markdown]
# ## Troubleshooting
#
# - **`FileNotFoundError: data/chicago_311.csv`** — the kernel's working
#   directory is not `labs/`. Restart the kernel from the `labs/` folder and
#   Run All.
# - **The canned mapping prints even with a key set** — `MAPPING_PROMPT` is
#   still `None`. Write the prompt string (the YOUR CODE comment lists its
#   three requirements) and re-run from that cell down.
# - **`json.JSONDecodeError` on a live call** — `chat_json` already forces
#   JSON mode; a parse failure usually means the prompt asked for prose
#   around the JSON. Demand "JSON only" and re-run.
# - **`AssertionError` from `validate`** — if it comes from the corruption
#   demo, the validator is working (read the printed message). If it comes
#   from your own mapping, the model broke the schema contract: fail loudly
#   is the correct behavior, not a bug.
# - **`errors_found` prints as a placeholder** — that is deliberate: the
#   audit only counts if *you* read the 20 rows and set the number.
