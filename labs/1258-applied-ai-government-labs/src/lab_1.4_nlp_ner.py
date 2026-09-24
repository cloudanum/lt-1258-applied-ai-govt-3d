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
# # Lab 1.4 — Named Entity Recognition: Press Releases
#
# *Course 1258 — Applied AI for Government IT Professionals · Ch01 AI and ML
# Foundations for Government · 30 minutes (flex — your instructor may skip
# this) · CloudShare VM (JupyterLab) · pandas + matplotlib + optional spaCy
# — no API key needed*
#
# Most government text is **unstructured**: press releases, memos, FOIA
# dumps, inspection notes. Before you can search it, redact it, link it, or
# feed it to any downstream system, you have to find the *who, what, where,
# when, and how much* hiding in the prose. That job is **Named Entity
# Recognition (NER)**. In this lab you run two NER extractors over five
# synthetic agency press releases — a statistical model (spaCy, if
# installed) and a transparent rule+gazetteer extractor that always works —
# then visualize the entities inline and as charts.

# %% [markdown]
# ## Objectives
#
# By the end of this lab, you will:
#
# - Explain what NER extracts and why it matters for search, redaction,
#   and records work.
# - Run two different extractors over the same text and compare them.
# - Render highlighted entities inline (the graphic a reviewer wants).
# - Summarize entities by type and by document in charts.
# - Extend the extractor with a rule of your own — and see it fire.

# %% [markdown]
# ## Setup
#
# - **Dataset:** `data/press_releases.json` — five **synthetic** agency
#   press releases written for this course. All people, programs, dollar
#   amounts, and contact details are fictitious; the agencies and laws are
#   real.
# - **Tools:** pandas, matplotlib, and the extractor below. If spaCy and
#   its `en_core_web_sm` model are installed, the lab uses them
#   automatically; otherwise a rule+gazetteer extractor does the job. Both
#   paths feed the same visualizations.
# - **No API key is needed** — this lab never calls a model.
# - **The one rule that never changes:** public or synthetic data only.
# - Cells marked `# YOUR CODE` are for you to complete. Each has a reference
#   fallback that runs if you leave it blank.

# %% [markdown]
# ## Steps
#
# 1. **(3 min)** Load the press releases and read one.
# 2. **(6 min)** Read through the two-path extractor: spaCy when present,
#    rules+gazetteers always.
# 3. **(5 min)** Render the highlighted text — the centerpiece graphic.
# 4. **(4 min)** Chart entity counts by type.
# 5. **(4 min)** Chart entities per document.
# 6. **(5 min)** Add a rule of your own and watch it fire.
# 7. **(3 min)** Stretch: point the extractor at the CDO memo.

# %% [markdown]
# ### Step 1 — Load the releases (provided)

# %%
import json
import pandas as pd
import matplotlib.pyplot as plt

releases = json.load(open("data/press_releases.json"))["releases"]
pr = releases[0]
print(f"{len(releases)} releases loaded\n")
print(f"{pr['id']} — {pr['title']}\n({pr['agency']}, {pr['date']})\n")
print(pr["body"])

# %% [markdown]
# ### Step 2 — The two-path extractor (provided)
#
# **Path A — spaCy (statistical).** A pretrained model tags ORG, PERSON,
# GPE (places), DATE, MONEY, and LAW spans by learned pattern — it
# generalizes to texts it has never seen, but you cannot read its rules.
#
# **Path B — rules + gazetteers (always available).** Regular expressions
# catch rigid formats (dates, dollar amounts, emails, phone numbers);
# **gazetteers** — plain lists of known names — catch agencies, officials,
# places, and laws. Fully transparent: every match traces to a line of
# code you can show a reviewer. This is the same pattern `lab_common` uses
# for PII masking in Lab 5.2.
#
# Read the code — you will extend it in Step 6.

# %%
import re

# --- Path A: spaCy, if it is installed with a language model ------------
try:
    import spacy
    _nlp = spacy.load("en_core_web_sm")
    HAVE_SPACY = True
except Exception:
    _nlp = None
    HAVE_SPACY = False

_SPACY_LABELS = {"ORG", "PERSON", "GPE", "DATE", "MONEY", "LAW"}

# --- Path B: regexes + gazetteers ----------------------------------------
MONTHS = ("January|February|March|April|May|June|July|August|September|"
          "October|November|December")
REGEXES = [
    ("DATE",  rf"\b(?:{MONTHS}) \d{{1,2}}, \d{{4}}\b"),
    ("MONEY", r"\$\d+(?:\.\d+)? (?:million|billion)"),
    ("EMAIL", r"[\w.+-]+@[\w-]+\.[\w.-]+"),
    ("PHONE", r"\b\d{3}-\d{3}-\d{4}\b"),
]

GAZETTEERS = {
    "ORG": ["City of Chicago Department of Transportation",
            "Office of the Chief Data Officer",
            "U.S. Environmental Protection Agency", "EPA Region 9", "EPA",
            "U.S. General Services Administration",
            "Technology Transformation Service",
            "Centers for Disease Control and Prevention", "CDC",
            "National Wastewater Surveillance System",
            "U.S. Department of Veterans Affairs",
            "Office of Information and Technology",
            "Records Management Center"],
    "PERSON": ["Maria Delgado", "David Chen", "Robin Patel",
               "Dr. Elena Brooks", "Elena Brooks", "Thomas Reyes"],
    "GPE": ["San Bernardino County", "California", "San Francisco",
            "Chicago", "Washington", "Atlanta", "St. Louis", "Missouri"],
    "LAW": ["Clean Air Act", "Federal Acquisition Regulation",
            "Section 508", "Federal Records Act"],
}


def _rule_entities(text):
    """Yield {start, end, label, text} spans from regexes + gazetteers."""
    spans = []
    for label, pattern in REGEXES:
        for m in re.finditer(pattern, text):
            spans.append({"start": m.start(), "end": m.end(),
                          "label": label, "text": m.group()})
    for label, names in GAZETTEERS.items():
        for name in names:  # longest names first prevents double-hits
            for m in re.finditer(re.escape(name), text):
                spans.append({"start": m.start(), "end": m.end(),
                              "label": label, "text": m.group()})
    # resolve overlaps: earliest start wins; ties go to the longer span
    spans.sort(key=lambda e: (e["start"], -(e["end"] - e["start"])))
    kept, last_end = [], -1
    for e in spans:
        if e["start"] >= last_end:
            kept.append(e)
            last_end = e["end"]
    return kept


def extract_entities(text):
    """One interface for both paths: list of {start, end, label, text}."""
    if HAVE_SPACY:
        return [{"start": e.start_char, "end": e.end_char,
                 "label": e.label_, "text": e.text}
                for e in _nlp(text).ents if e.label_ in _SPACY_LABELS]
    return _rule_entities(text)


print(f"extractor ready — path: "
      f"{'spaCy (en_core_web_sm)' if HAVE_SPACY else 'rules + gazetteers (spaCy not installed)'}")

# %% [markdown]
# ### Step 3 — Highlight the entities (the centerpiece)
#
# A displaCy-style renderer that works from **either** extractor: each
# entity is marked in its label's color, with the label in small caps.
# This is the view a records officer actually works in.

# %%
from html import escape
from IPython.display import HTML, display

LABEL_COLORS = {
    "ORG": "#aee1f9", "PERSON": "#f9c6d0", "GPE": "#c9f0c2",
    "DATE": "#f9e3a8", "MONEY": "#d9ccf9", "LAW": "#f5cda8",
    "EMAIL": "#e2e2e2", "PHONE": "#e2e2e2", "WARD": "#b8e6d4",
}


def render_entities(text, ents, title=None):
    ents = sorted(ents, key=lambda e: e["start"])
    parts, pos = [], 0
    for e in ents:
        parts.append(escape(text[pos:e["start"]]))
        color = LABEL_COLORS.get(e["label"], "#dddddd")
        parts.append(
            f'<mark style="background:{color};padding:2px 5px;'
            f'border-radius:4px">{escape(e["text"])}'
            f'<small style="font-weight:bold;color:#555">'
            f' {e["label"]}</small></mark>')
        pos = e["end"]
    parts.append(escape(text[pos:]))
    head = (f"<div style='font-weight:bold;margin-top:12px'>{escape(title)}"
            f"</div>") if title else ""
    return HTML(head + "<p style='font-family:Georgia,serif;"
                "line-height:2.0'>" + "".join(parts) + "</p>")


for r in releases[:3]:
    ents = extract_entities(r["body"])
    display(render_entities(r["body"], ents, title=f"{r['id']} — {r['title']}"))

# %% [markdown]
# **What to notice:** gazetteers only find what they know — the rule path
# catches every *format* (dates, money, emails) but only the *names* in
# its lists. If spaCy is installed, compare: the model finds names it was
# never told about, but may miss an email or mistag an agency. Every
# extractor has a blind spot; the question is whether yours matters for
# the job.

# %% [markdown]
# ### Step 4 — Count by type (provided)
#
# The summary chart for a briefing: what kinds of things did the corpus
# mention?

# %%
all_ents = []
for r in releases:
    for e in extract_entities(r["body"]):
        all_ents.append({"doc": r["id"], **e})
ent_df = pd.DataFrame(all_ents)

by_label = ent_df["label"].value_counts()
by_label.plot.barh(
    color=[LABEL_COLORS.get(l, "#bbb") for l in by_label.index],
    title=f"Entities by type across {len(releases)} press releases",
    xlabel="mentions")
plt.gca().invert_yaxis()
plt.tight_layout(); plt.show()

print(by_label.to_string())

# %% [markdown]
# ### Step 5 — Entities per document (provided)
#
# Which releases are dense with which kinds of entities? A stacked view
# shows each document's profile at a glance — handy for triage ("which of
# these 500 documents even mentions money?").

# %%
per_doc = (ent_df.groupby(["doc", "label"]).size()
           .unstack(fill_value=0)
           .reindex(sorted(ent_df["doc"].unique())))
per_doc.plot.bar(stacked=True, figsize=(9, 4.5),
                 color=[LABEL_COLORS.get(c, "#bbb") for c in per_doc.columns],
                 ylabel="entities", title="Entity profile per press release")
plt.legend(title="label", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout(); plt.show()

# %% [markdown]
# ### Step 6 — Your turn: add a rule
#
# The rule path is only as good as its lists — and improving it is a
# *coding* task, not a retraining task. That is its superpower. Add one:
#
# - a **WARD** gazetteer/regex that catches `Ward 28`, `Ward 41` (PR-001), or
# - a new **ORG** or **PERSON** you spot in a release, or
# - a **DATE** variant like `the 2026-27 flu season` (harder — optional).
#
# Then re-run the extraction on PR-001 and count what changed.

# %%
before = len(extract_entities(releases[0]["body"]))

# YOUR CODE: append a ("WARD", r"\bWard \d+\b") tuple to REGEXES (or a
# name to a GAZETTEERS list), then re-run extraction on releases[0].

after = len(extract_entities(releases[0]["body"]))
if after == before:
    # reference answer — replace with your own rule above
    REGEXES.append(("WARD", r"\bWard \d+\b"))
    after = len(extract_entities(releases[0]["body"]))
    print("(reference rule added — replace with your own above)")

print(f"entities in PR-001: before={before}, after={after}")
display(render_entities(releases[0]["body"],
                        extract_entities(releases[0]["body"]),
                        title="PR-001 — after your rule"))

# %% [markdown]
# ### Step 7 — Stretch: point it at the CDO memo (optional)
#
# Real course text, no gazetteer tuned for it. What does the extractor
# still catch (dates, the Office of the Chief Data Officer), and what does
# it miss? That gap *is* the lesson: an extractor is a product decision,
# not a fact of nature.

# %%
memo = open("data/gov_memo.txt").read()
memo_ents = extract_entities(memo)
print(f"{len(memo_ents)} entities found in gov_memo.txt")
display(render_entities(memo, memo_ents, title="gov_memo.txt"))

# %% [markdown]
# ## Deliverable
# 1. The highlighted rendering of one press release, with a one-line note
#    on anything the extractor mistagged or missed.
# 2. The by-type and per-document charts.
# 3. Your added rule: what it catches now that it missed before.
# 4. Two sentences: when would you deploy the gazetteer, and when the
#    statistical model?

# %% [markdown]
# ## Reflection
# 1. Which extractor would you trust for **redaction** (PII must be
#    caught, over-redaction is tolerable)? Which for **search indexing**?
# 2. A gazetteer of agency names is transparent but always out of date.
#    Who owns updating it in a real agency — and what breaks when nobody
#    does?
# 3. NER is often the *first* stage of a pipeline (find → classify →
#    link). What would the next stage be for these press releases?

# %% [markdown]
# ## Debrief (instructor-led)
#
# - **Compare paths.** If some students have spaCy and some do not, put
#   the two PR-001 renderings side by side: model recall vs rule
#   transparency.
# - **The blind-spot inventory.** Collect one missed entity per student
#   on the board. Regex, gazetteer, or model — which fix is cheapest for
#   each?
# - **Bridge to Lab 5.2.** PII detection is NER with legal consequences:
#   same spans, but a miss is a reportable spill.

# %% [markdown]
# ## Troubleshooting
#
# - **`FileNotFoundError: data/press_releases.json`** — the kernel's
#   working directory is not `labs/`. Restart the kernel from the `labs/`
#   folder and Run All.
# - **`extractor ready — path: rules + gazetteers`** — spaCy is not
#   installed here. That is fine: every step works. To try the statistical
#   path elsewhere: `pip install spacy && python -m spacy download
#   en_core_web_sm`, then restart the kernel.
# - **Your new rule did not fire** — regexes are case-sensitive and the
#   gazetteer match is exact-substring. Print the target sentence and
#   test your pattern with `re.findall(pattern, sentence)` first.
# - **A name is highlighted twice / overlapping** — the overlap resolver
#   keeps the earliest-starting, longest span. Put longer names in the
#   gazetteer (e.g. the full agency name, not just its abbreviation) to
#   win the tie.
# - **spaCy tags something oddly** — expected: it is a statistical model
#   with its own label scheme (FAC, NORP, CARDINAL are filtered out
#   here). That behavior *is* the compare-and-contrast material.
