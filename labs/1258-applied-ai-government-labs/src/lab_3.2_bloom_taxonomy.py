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
# # Lab 3.2 — Prompt the Ladder: Bloom's Taxonomy for Government GenAI Tasks
#
# *Chapter 3 — Desktop GenAI at Work · 45 minutes · JupyterLab with the
# OpenAI API via `lab_common` (canned offline fallback)*
#
# AI is not **smart-or-dumb**. It works across six levels of cognitive
# sophistication, from pure recall to maximum creativity — and the level of
# the *task* you hand it sets the prompt architecture you need, the
# creativity you can expect, and the kind of risk you take on. In this lab
# you climb that ladder one rung at a time: at each of the six Bloom levels
# you study what the level demands, run **two worked government examples**,
# and write **one prompt of your own** — 18 prompts in all.
#
# Framework: the revised Bloom's taxonomy (Anderson & Krathwohl, 2001) mapped
# onto generative AI, adapted from the neurals.ca agent-concepts page on
# Bloom's Taxonomy (neurals.ca/agents/concepts/bloom-taxonomy).
#
# Cells marked `# YOUR CODE` are for you. Offline, every call returns a
# realistic canned answer so you can keep working.

# %% [markdown]
# ## Objectives
#
# By the end of this lab, you will:
#
# - Classify a government GenAI task by Bloom level **before** writing the
#   prompt.
# - Write and run three prompts at each of the six levels against real
#   government material.
# - Match temperature and verification strategy to the level.
# - Explain each level's characteristic risk and how the prompt controls it.

# %% [markdown]
# ## Setup
#
# **Datasets and files** (all under `labs/data/`):
#
# - `gov_memo.txt` — GAO-style CDO memorandum: interim guidance on generative
#   AI for constituent services (Remember/Understand/Evaluate examples)
# - `corpus/ai_acceptable_use_policy.md` — agency AI acceptable-use policy
#   (Remember/Understand/Apply examples)
# - `federal_ai_use_cases.csv` — federal AI use-case inventory extract
#   (Remember/Analyze/Evaluate examples)
# - `chicago_311.csv` — 4,000 real Chicago 311 service requests
#   (Understand/Apply/Analyze/Create examples)
# - `epa_aqi_by_county.csv` — EPA county air-quality summary, 2024
#   (Analyze example)
# - `citizen_records.json` — five synthetic constituent records (Apply
#   example; synthetic PII for training)
#
# **Tools:** pandas, plus the OpenAI chat API through `lab_common.chat()` /
# `lab_common.chat_json()` — offline these return canned stand-ins, so the
# notebook never hard-fails on a keyless machine.
#
# **Data rule:** every file above is either genuinely public US government
# data (documented in `data/MANIFEST.json`) or synthetic material written for
# this course. Never paste real agency data containing PII into these
# notebooks — or into any AI tool.

# %%
# API key status — lab_common loads OPENAI_API_KEY from the environment
# (classroom VM) or the course .env file at import. The key is never printed.
# With no key, every AI call below falls back to a realistic canned output.
import lab_common as lc

if lc.online():
    print(f"OpenAI API key found — live mode (model: {lc.CHAT_MODEL}).")
else:
    print("No API key found — offline mode: AI calls return realistic canned "
          "outputs, so every step still runs.\nAsk your instructor if you "
          "expected a key on this machine.")

# %% [markdown]
# ### The substrate (provided)
#
# Slices of the six course datasets, prepared once and reused across the
# levels. Note that the *prompts* change per level — the material stays the
# same. That is the point of the lab: same data, six different kinds of ask.

# %%
import json
import pandas as pd
from lab_common import chat, chat_json

memo = open("data/gov_memo.txt").read()
policy = open("data/corpus/ai_acceptable_use_policy.md").read()

c311 = pd.read_csv("data/chicago_311.csv", low_memory=False)
sr_counts = c311["sr_type"].value_counts().head(6)
top3 = sr_counts.index.tolist()[:3]
ward_slice = (c311[c311["sr_type"].isin(top3)]
              .groupby(["ward", "sr_type"]).size().unstack(fill_value=0))
ward_slice = ward_slice.loc[
    ward_slice.sum(axis=1).sort_values(ascending=False).index].head(5)

uc = pd.read_csv("data/federal_ai_use_cases.csv", low_memory=False)
uc_slice = (uc[["agency_name", "use_case_name", "development_stage",
                "problem_solved"]]
            .dropna(subset=["use_case_name"]).head(4))

aqi = pd.read_csv("data/epa_aqi_by_county.csv")
aqi_hot = (aqi[aqi["Unhealthy Days"] > 0]
           .sort_values("Unhealthy Days", ascending=False).head(3))

citizen = json.load(open("data/citizen_records.json"))["records"][0]

print("Top 311 request types:"); print(sr_counts.to_string(), "\n")
print("Use-case inventory slice:")
print(uc_slice[["agency_name", "use_case_name", "development_stage"]]
      .to_string(index=False), "\n")
print("Highest-unhealthy-day AQI counties:")
print(aqi_hot[["State", "County", "Unhealthy Days", "Max AQI"]]
      .to_string(index=False))

# %% [markdown]
# ## The ladder at a glance
#
# | Level | What you're asking | Signature verbs | Output space | Characteristic risk | Temp | Verify by |
# |---|---|---|---|---|---|---|
# | 1 · Remember | Retrieve, extract, quote a stored fact | list, define, extract, quote | Narrow — one right answer | Confident fabrication | 0.0–0.2 | Quote spot-check; a non-expert can do it |
# | 2 · Understand | Explain, summarize, paraphrase | summarize, explain, paraphrase | Slightly wider | Smoothing — a dropped caveat | 0.0–0.2 | Source-consistency check |
# | 3 · Apply | Run a fixed procedure on new input | classify, calculate, execute | Fenced by the rules | Executional error | 0.3–0.6 | Test against known examples |
# | 4 · Analyze | Decompose, compare, find patterns | compare, diagnose, trace, infer | Wide | Spurious connection | 0.3–0.6 | Force the reasoning into the open |
# | 5 · Evaluate | Judge, score, rank against criteria | judge, score, recommend, critique | Wide + normative | Hidden assumptions; unauditable verdict | 0.7–1.0 | Rubric + accountable human approver |
# | 6 · Create | Design, synthesize something new | design, generate, synthesize, invent | Maximal — no answer key | Unverifiable plausibility | 0.7–1.0 | Domain judgment + structured audit |
#
# **Classify before you prompt.** Run the task down this list; the first
# "yes" sets the level:
#
# 1. Is the answer a fact to recall or pull from a source? → *Remember*
# 2. Restate or compress material without adding judgment? → *Understand*
# 3. Run a fixed procedure on new input? → *Apply*
# 4. Decompose something or find relationships? → *Analyze*
# 5. Judge what is better or what should be done? → *Evaluate*
# 6. Produce something new with no single correct answer? → *Create*
#
# Two rules run the whole ladder: **constrain low** (Levels 1–2: close the
# output space so fabrication has nowhere to hide) and **scaffold high**
# (Levels 5–6: give structured room to roam — criteria, constraints,
# alternatives, explicit reasoning). Creative tasks need *more* structure,
# not less.

# %% [markdown]
# ## Steps
#
# 1. Run the Setup cells and read the ladder table. (3 min)
# 2. **L1 Remember:** run the two extraction examples; write the policy-quote
#    prompt. (6 min)
# 3. **L2 Understand:** two summaries; write the dashboard explainer. (6 min)
# 4. **L3 Apply:** two procedure runs; write the masking prompt. (6 min)
# 5. **L4 Analyze:** two diagnoses; write the AQI trace. (7 min)
# 6. **L5 Evaluate:** two rubric judgments; write the vendor critique. (7 min)
# 7. **L6 Create:** two designs; write the triage concept note. (6 min)
# 8. Pull one Create task down the ladder into a six-stage pipeline. (4 min)
#
# At every level: read the worked prompt, note the temperature, and answer
# the **Before you trust it** question — that question *is* the lesson.

# %% [markdown]
# ## Level 1 — Remember: retrieve and extract
#
# **What you're asking:** find a fact, field, quote, or label that already
# exists in the source. There is one right answer, and you want **zero**
# creativity.
#
# - **Risk:** *confident fabrication* — an invented fact stated as fluently
#   as a real one.
# - **Prompt move:** constrain and ground. Fence the model into the source:
#   "use only the text below; if it is not stated, write 'not stated'; do
#   not infer."
# - **Temperature 0.0–0.2:** near-deterministic token choice.
# - **Verify by:** checking the quote against the source — a competent
#   non-expert can do it.

# %% [markdown]
# ### Example 1A (worked) — Extract every timeframe from the CDO memo
#
# A compliance officer needs every date, deadline, and reporting timeframe
# in the memo, each with its exact supporting quote.

# %%
CANNED_L1A = (
    "section | requirement | timeframe | supporting quote\n"
    "3(a) | human review before release | no timeframe stated | not stated\n"
    "3(b) | report suspected exposure | within one business day | "
    "\"Suspected exposure must be reported within one business day.\"\n"
    "4 | effective date | immediately | "
    "\"This guidance is effective immediately\"\n"
    "4 | expiry | until superseded | "
    "\"remains in effect until superseded by final Department policy.\""
)

l1a = chat(
    [{"role": "user", "content":
      "Task level: Remember / Extract.\n"
      "Use only the memorandum between <memo> tags. Extract every date, "
      "deadline, or reporting timeframe.\n"
      "Return a table: section | requirement | timeframe | exact supporting "
      "quote.\n"
      "If a timeframe is not explicitly stated, write \"not stated\". "
      "Do not infer.\n\n"
      f"<memo>\n{memo}\n</memo>"}],
    offline=CANNED_L1A, temperature=0.0)
print(l1a)

# %% [markdown]
# **Why this works:** the fences do the work — "use only the memo", "exact
# supporting quote", "not stated" as an allowed answer. The model cannot
# pad or guess without visibly breaking the format.
#
# **Before you trust it:** paste each quote back into a search of the memo.
# At Level 1 that mechanical check is the *whole* verification strategy.

# %% [markdown]
# ### Example 1B (worked) — List the pre-deployment use cases
#
# An oversight analyst wants the use cases in the inventory slice that are
# exactly at the `Pre-deployment` stage — copied verbatim, nothing added.

# %%
CANNED_L1B = (
    "agency_name | use_case_name\n"
    "Commodity Futures Trading Commission | Stress Testing Scenarios with "
    "Deep Learning\n"
    "Department of Homeland Security | Smartphone Information Forensics Triage"
)

uc_text = uc_slice[["agency_name", "use_case_name", "development_stage"]] \
    .to_string(index=False)

l1b = chat(
    [{"role": "user", "content":
      "Task level: Remember / Extract.\n"
      "From the inventory rows below, list every use case whose "
      "development_stage is exactly \"Pre-deployment\".\n"
      "Return: agency_name | use_case_name — copied exactly as written. "
      "Do not paraphrase, complete, or infer. If none, write \"none\".\n\n"
      f"{uc_text}"}],
    offline=CANNED_L1B, temperature=0.0)
print(l1b)

# %% [markdown]
# **Why this works:** "copied exactly as written" plus "do not paraphrase"
# turns the task into pure retrieval. **Before you trust it:** count the
# `Pre-deployment` rows in the slice yourself and compare — two lines of
# pandas settles it.

# %% [markdown]
# ### Example 1C (your turn) — Quote the bright line
#
# Your training deck needs the *exact* sentence from the acceptable-use
# policy that states what happens when an employee pastes a constituent's
# record into a public chatbot. Write the prompt: demand a verbatim quote
# and nothing else.

# %%
CANNED_L1C = ("Pasting a constituent's record into a public chatbot is a "
              "reportable data spill.")

l1c = None
# YOUR CODE: chat() with a user message asking for the exact sentence from
# `policy` (include the policy text). Require one verbatim quote, no
# commentary. Pass offline=CANNED_L1C and temperature=0.0.

if l1c is None:
    l1c = CANNED_L1C
    print("(canned quote — write your extraction prompt above to run your own)\n")
print(l1c)

# the Remember-level check: does the quote actually exist in the source?
print("\nquote verified in policy:", l1c.strip().strip('"') in policy)

# %% [markdown]
# ## Level 2 — Understand: explain and summarize
#
# **What you're asking:** restate or compress existing material faithfully.
# Many valid restatements exist — the goal is fidelity, not novelty.
#
# - **Risk:** *smoothing* — a material caveat or exception quietly dropped
#   from an otherwise clean summary.
# - **Prompt move:** ground in the source and *name what must survive*:
#   "preserve every exception and deadline; add no terms that are not
#   present."
# - **Temperature 0.0–0.2:** still near-deterministic.
# - **Verify by:** source-consistency check — does every claim in the
#   summary trace to the source, and did any caveat go missing?

# %% [markdown]
# ### Example 2A (worked) — The memo for a new employee
#
# Onboarding needs a 120-word summary of the CDO memo. The deadlines and
# exceptions are exactly what a newcomer cannot afford to lose.

# %%
CANNED_L2A = (
    "The memo sets interim rules for using generative AI in constituent "
    "services until the final policy arrives. A responsible employee must "
    "review and approve every AI-assisted product before it reaches a "
    "constituent or the public record — the employee, not the tool, is "
    "accountable. Only public information may go into public AI tools; "
    "constituent records, Social Security numbers, and other PII must never "
    "enter an unapproved tool, and suspected exposure must be reported "
    "within one business day. Internal information may only be handled by "
    "the enterprise assistant under the Department's data-protection "
    "agreement. AI-assisted correspondence about agency business is a "
    "federal record and must be retained. The guidance is effective "
    "immediately. Caveat newcomers miss: even a rough AI-drafted letter "
    "about agency business is already a federal record."
)

l2a = chat(
    [{"role": "user", "content":
      "Task level: Understand / Summarize.\n"
      "Summarize the memorandum below for a new employee in 120 words or "
      "fewer. Preserve every exception, deadline, and accountability rule. "
      "Add no rules that are not present. End with one sentence labelled "
      "\"Caveat newcomers miss:\".\n\n"
      f"{memo}"}],
    offline=CANNED_L2A, temperature=0.1)
print(l2a)

# %% [markdown]
# **Why this works:** "preserve every exception and deadline" converts the
# smoothing risk into an explicit checklist. **Before you trust it:** re-read
# §3 of the memo side by side with the summary and tick off a–d. If one
# clause is missing, the summary failed — fluent is not faithful.

# %% [markdown]
# ### Example 2B (worked) — The data categories, for a contractor
#
# A contractor starting Monday needs the policy's three data categories in
# plain language — with every "must not" intact.

# %%
CANNED_L2B = (
    "Think of agency data in three buckets.\n"
    "1. Public data — published reports, open data from data.gov — may be "
    "used with any approved tool.\n"
    "2. Internal data — everyday work material — may be used only with the "
    "agency-provisioned enterprise assistant operating under the agency's "
    "data-protection agreement. Never a public chatbot.\n"
    "3. Sensitive or regulated data — PII, health, financial, law "
    "enforcement — may be used only with tools specifically authorized for "
    "that category.\n"
    "And the bright line: you must not enter nonpublic information into any "
    "AI tool not approved for that data category. Pasting a constituent's "
    "record into a public chatbot is a reportable data spill."
)

l2b = chat(
    [{"role": "user", "content":
      "Task level: Understand / Explain.\n"
      "Explain the three data categories in the policy below to a first-week "
      "contractor, in plain language. Keep every prohibition (\"must not\") "
      "intact and explicit. Use a numbered list. Do not add permissions or "
      "exceptions that are not stated.\n\n"
      f"{policy}"}],
    offline=CANNED_L2B, temperature=0.1)
print(l2b)

# %% [markdown]
# **Why this works:** "keep every prohibition intact" tells the model the
# prohibitions are load-bearing. **Before you trust it:** count the "must
# not"s in the source and in the output — the numbers must match.

# %% [markdown]
# ### Example 2C (your turn) — The public-dashboard explainer
#
# The open-data portal needs three plain-language sentences explaining the
# top-six 311 request types for a public dashboard — with every number
# preserved exactly. Write the prompt (give the model the `sr_counts` text).

# %%
CANNED_L2C = (
    "Aircraft noise complaints dominate this 311 extract with 1,547 "
    "requests, far ahead of general information calls at 760. Street "
    "flooding (\"Water On Street\") follows at 257, with tree emergencies "
    "(159), graffiti removal (136), and tree debris clean-up (83) rounding "
    "out the top six. Together these six categories account for 2,942 of "
    "the 4,000 requests in the file."
)

l2c = None
# YOUR CODE: chat() asking for a three-sentence plain-language explainer of
# sr_counts.to_string() for a public dashboard. Require every number to be
# preserved exactly and no causes to be speculated about.
# Pass offline=CANNED_L2C and temperature=0.2.

if l2c is None:
    l2c = CANNED_L2C
    print("(canned explainer — write your summary prompt above to run your own)\n")
print(l2c)

# %% [markdown]
# ## Level 3 — Apply: run a known procedure
#
# **What you're asking:** use a fixed rule, formula, or procedure on new
# input. The method is given; only the input varies. The output space is
# fenced by the rules.
#
# - **Risk:** *executional error* — an off-by-one, a missed edge case.
#   Procedural, not factual, and therefore catchable by testing.
# - **Prompt move:** specify the procedure, the rule order, the edge cases,
#   and the escalation path for missing information.
# - **Temperature 0.3–0.6:** flexible enough to map inputs to rules without
#   abandoning logic.
# - **Verify by:** testing against examples with known answers.

# %% [markdown]
# ### Example 3A (worked) — Classify 311 types under a fixed rule list
#
# Streets & Sanitation wants incoming request types bucketed by a published
# rule list — no improvisation, and anything unmatched goes to a human.

# %%
RULES_311 = (
    "Routing rules (apply in order, first match wins):\n"
    "1. Any type containing 'Aircraft Noise' -> Noise & Nuisance\n"
    "2. Any type starting with 'Tree' -> Urban Forestry\n"
    "3. Any type containing 'Graffiti' -> Property & Streets\n"
    "4. Any type containing 'Water' -> Water & Drainage\n"
    "5. Any type containing 'INFORMATION ONLY' -> Information\n"
    "6. No rule matches -> Needs Human Review"
)

CANNED_L3A = (
    "Tree Debris Clean-Up Request -> Urban Forestry (rule 2)\n"
    "Water On Street Complaint -> Water & Drainage (rule 4)\n"
    "Broken Street Light Complaint -> Needs Human Review (rule 6 — no "
    "rule matches; escalate, do not guess)"
)

l3a = chat(
    [{"role": "user", "content":
      "Task level: Apply / Classify.\n"
      f"{RULES_311}\n\n"
      "Classify each request type below using the rules above, in order. "
      "Use no rule that is not listed. Return one line per input: "
      "type -> category (rule number). If no rule matches, route to Needs "
      "Human Review — do not invent a category.\n\n"
      "Tree Debris Clean-Up Request\n"
      "Water On Street Complaint\n"
      "Broken Street Light Complaint"}],
    offline=CANNED_L3A, temperature=0.4)
print(l3a)

# %% [markdown]
# **Why this works:** ordered rules, "first match wins", "use no rule that
# is not listed", and an explicit escalation bucket. The model's job is
# execution, not judgment. **Before you trust it:** run the known-answer
# test — you already know where each of the three inputs should land.

# %% [markdown]
# ### Example 3B (worked) — Apply the data-category rules to three scenarios
#
# Security awareness training needs the policy's data-category rules applied
# to three everyday scenarios, each with the rule it rests on.

# %%
SCENARIOS = (
    "Scenario 1: An employee pastes a published GAO report into a public "
    "chatbot and asks for a summary.\n"
    "Scenario 2: An employee pastes a constituent's home address into a "
    "public chatbot to draft a reply letter.\n"
    "Scenario 3: An employee drafts an internal memo using the "
    "agency-provisioned enterprise assistant."
)

CANNED_L3B = (
    "Scenario 1 -> Public data; permitted in any approved tool. Rule: Data "
    "Categories, 'Public data ... may be used with any approved tool.'\n"
    "Scenario 2 -> Sensitive/regulated data (PII) in an unapproved tool; "
    "prohibited — a reportable data spill. Rule: Prohibited Uses, 'must not "
    "enter nonpublic information into any AI tool that has not been "
    "approved for that data category.'\n"
    "Scenario 3 -> Internal data; permitted — enterprise assistant only. "
    "Rule: Data Categories, 'Internal data may be used only with the "
    "agency-provisioned enterprise assistant.'"
)

l3b = chat(
    [{"role": "user", "content":
      "Task level: Apply / Determine.\n"
      "Use only the data-category rules in the policy below. For each "
      "scenario, decide: permitted or prohibited, which data category "
      "applies, and the exact rule you relied on. If a scenario depends on "
      "a fact the policy does not give, say \"cannot determine from "
      "policy\".\n\n"
      f"Policy:\n{policy}\n\n{SCENARIOS}"}],
    offline=CANNED_L3B, temperature=0.3)
print(l3b)

# %% [markdown]
# **Why this works:** decision + category + cited rule makes every judgment
# auditable, and "cannot determine from policy" is an allowed answer.
# **Before you trust it:** check that each cited rule actually exists in the
# policy — same mechanical habit as Level 1.

# %% [markdown]
# ### Example 3C (your turn) — Run the masking procedure
#
# Before a synthetic constituent record can leave the boundary for
# analytics, this procedure must run: mask `name`, `ssn`, `email`, `phone`,
# and `address`; keep `case_id`, `topic`, `summary`, and `status` unchanged;
# return JSON only. Write the `chat_json()` call for the `citizen` record.

# %%
CANNED_L3C = {
    "case_id": citizen["case_id"],
    "name": "[REDACTED]",
    "ssn": "[REDACTED]",
    "email": "[REDACTED]",
    "phone": "[REDACTED]",
    "address": "[REDACTED]",
    "topic": citizen["topic"],
    "summary": citizen["summary"],
    "status": citizen["status"],
}

l3c = None
# YOUR CODE: chat_json() with the masking procedure above and the citizen
# record (json.dumps(citizen, indent=2)) in the user message. Require the
# exact field list. Pass offline=CANNED_L3C and temperature=0.3.

if l3c is None:
    l3c = CANNED_L3C
    print("(canned masked record — write your chat_json call above to run "
          "your own)\n")
print(json.dumps(l3c, indent=2))

# executional check: no raw PII value may survive in the output
leaked = [f for f in ("name", "ssn", "email", "phone", "address")
          if l3c.get(f) == citizen[f]]
print("\nfields left unmasked:", leaked or "none — procedure executed cleanly")

# %% [markdown]
# ## Level 4 — Analyze: decompose and compare
#
# **What you're asking:** break a thing into parts and surface relationships,
# causes, and patterns. Choosing *which* connections matter is itself partly
# subjective — the output space widens.
#
# - **Risk:** *spurious connection* — a plausible relationship that is not
#   real; correlation read as cause. Risk starts rising sharply here.
# - **Prompt move:** make the reasoning explicit and separable. Require
#   every claim to be labelled **(given / inferred / assumption)**, demand
#   competing hypotheses, and forbid correlation-as-causation.
# - **Temperature 0.3–0.6:** anchored but flexible.
# - **Verify by:** a domain expert reading the reasoning — this is where
#   non-expert verification stops being enough.

# %% [markdown]
# ### Example 4A (worked) — Diagnose the 311 pattern by ward
#
# The city manager asks: what is driving the top three request types, and
# why are they concentrated in these wards?

# %%
CANNED_L4A = (
    "1. Observable facts (given): Ward 41 holds nearly all aircraft-noise "
    "complaints (1,447); Ward 28 holds most information-only calls (698); "
    "water-on-street is spread thin across wards 35, 37, and 29.\n"
    "2. Symptom clusters: a single-ward noise concentration; a single-ward "
    "information-call concentration; a diffuse flooding pattern.\n"
    "3. Competing hypotheses:\n"
    "   H1 (inferred): Ward 41 contains or borders the airport — noise "
    "tracks flight paths, not population. For: extreme single-ward "
    "concentration. Against: nothing in the data. Needed: a ward map.\n"
    "   H2 (inferred): Ward 28's information-call volume signals a service "
    "gap — residents call because answers are hard to find online. For: "
    "volume is an order of magnitude above other wards. Against: call "
    "content is not in the slice. Needed: call notes or transcripts.\n"
    "   H3 (assumption): water complaints follow rainfall events. Not "
    "testable from this slice — need request dates and weather data.\n"
    "4. Most likely: H1 — but it remains a correlation until the geography "
    "is confirmed. Do not act on H2 or H3 without the missing data."
)

l4a = chat(
    [{"role": "user", "content":
      "Task level: Analyze / Diagnose.\n"
      "Analyze the 311 counts by ward below. Produce: (1) observable facts, "
      "(2) symptom clusters, (3) three competing root-cause hypotheses with "
      "evidence for and against each, (4) the missing data that would "
      "confirm or kill each, (5) the most likely cause with a confidence "
      "level.\n"
      "Label every claim as (given), (inferred), or (assumption). Do not "
      "present correlation as causation unless the evidence supports "
      "it.\n\n"
      f"{ward_slice.to_string()}"}],
    offline=CANNED_L4A, temperature=0.5)
print(l4a)

# %% [markdown]
# **Why this works:** the claim labels turn fluent prose into an auditable
# structure — you can disagree with H2 without throwing out the facts.
# **Before you trust it:** could you defend every "(given)" from the table
# itself? If a "given" is not in the data, the whole diagnosis is suspect.

# %% [markdown]
# ### Example 4B (worked) — Compare two inventory entries
#
# An oversight reviewer wants the first two use cases in the inventory slice
# compared — same and different, with nothing invented.

# %%
uc_two = uc_slice.head(2).to_string(index=False, max_colwidth=80)

CANNED_L4B = (
    "Shared (given): both are Commodity Futures Trading Commission systems "
    "applied to the agency's own market data; neither is described as "
    "public-facing.\n"
    "Different (given): the first is Pre-deployment and exploratory — "
    "deep-learning stress-test scenarios for futures and options "
    "portfolios; the second is Deployed and operational — anomaly "
    "detection flagging potentially erroneous data loads.\n"
    "Different (inferred): the verification burden differs. A deployed "
    "data-quality gate needs measurable precision and recall; a "
    "pre-deployment scenario generator is judged by expert review of "
    "plausibility.\n"
    "Missing (given): the slice carries no performance metrics for either "
    "system, so any comparison of accuracy would be an assumption, not a "
    "finding."
)

l4b = chat(
    [{"role": "user", "content":
      "Task level: Analyze / Compare.\n"
      "Compare the two inventory rows below. Produce: what is shared, what "
      "is different, what is missing, and one inference you are confident "
      "in. Label every claim (given), (inferred), or (assumption). Do not "
      "praise or rank — that would be Evaluate.\n\n"
      f"{uc_two}"}],
    offline=CANNED_L4B, temperature=0.4)
print(l4b)

# %% [markdown]
# **Why this works:** "do not praise or rank" holds the line at Analyze —
# the moment you ask "which is better" you have climbed to Evaluate and owe
# a rubric. **Before you trust it:** the "(inferred)" claims are where an
# expert earns their pay; the "(given)"s anyone can check.

# %% [markdown]
# ### Example 4C (your turn) — Trace the AQI anomaly
#
# An environmental program office asks: what is driving the unhealthy days
# in the top county of `aqi_hot` (San Bernardino, CA)? Write the prompt:
# ask which pollutant dominates, demand labelled hypotheses, and ask what
# daily data would confirm them.

# %%
aqi_row = aqi_hot.head(1).to_string(index=False)

CANNED_L4C = (
    "Dominant driver (given): ozone accounts for 218 of 366 measured days "
    "and PM2.5 for 123 in San Bernardino County; the 61 unhealthy days sit "
    "inside an ozone-dominated profile.\n"
    "H1 (inferred): a summer photochemical-smog regime — heat and sunlight "
    "convert vehicle and industrial emissions into ozone downwind of the "
    "Los Angeles basin. For: ozone dominance. Against: nothing in the "
    "slice. Needed: daily AQI series and meteorology.\n"
    "H2 (inferred): episodic wildfire smoke pushed PM2.5 and the Max AQI "
    "of 593 to hazardous levels on a few days. For: extreme peak vs a "
    "median far lower. Against: smoke days are not flagged in the slice. "
    "Needed: fire-perimeter records and daily PM2.5.\n"
    "Do not attribute the hazardous peak to either cause without the daily "
    "data — annual counts cannot separate a season from an episode."
)

l4c = None
# YOUR CODE: chat() with the aqi_row text; ask which pollutant dominates the
# county's unhealthy days, for labelled competing hypotheses, and for the
# daily data that would confirm them. Pass offline=CANNED_L4C, temperature=0.5.

if l4c is None:
    l4c = CANNED_L4C
    print("(canned trace — write your analysis prompt above to run your own)\n")
print(l4c)

# %% [markdown]
# ## Level 5 — Evaluate: judge against criteria
#
# **What you're asking:** rank, score, recommend, or approve. The output now
# asserts what *should* be — it carries normative weight.
#
# - **Risk:** *hidden assumptions* — a confident verdict you cannot audit
#   because the model silently supplied both the criteria and the answer.
# - **Prompt move:** externalize the criteria. Make the model restate the
#   rubric first, score each criterion separately with evidence, flag
#   unsupported scores, and end with questions for the human decision maker.
#   Never let it supply criteria and verdict invisibly.
# - **Temperature 0.7–1.0:** room to weigh trade-offs.
# - **Verify by:** rubric + an accountable human approver. This is decision
#   support, not the decision.

# %% [markdown]
# ### Example 5A (worked) — Score three candidate GenAI uses
#
# The CDO's office must pick the next GenAI pilot for constituent services.
# Three candidates, one rubric — and every score needs evidence.

# %%
RUBRIC = ("Rubric: constituent impact 35%, risk of harm 30%, operating "
          "cost 20%, speed to pilot 15%. Score each 1–5 (higher = better "
          "on that criterion).")

CANDIDATES = (
    "Candidate 1 — Draft routine correspondence replies (pilots in the "
    "memo showed time savings; enterprise assistant already provisioned).\n"
    "Candidate 2 — Auto-triage 311 requests to departments (2,942 requests "
    "in the top six categories; no accuracy evidence available).\n"
    "Candidate 3 — Summarize public-meeting transcripts (public input "
    "only; smaller audience)."
)

CANNED_L5A = (
    "Rubric restated: constituent impact 35%, risk of harm 30%, operating "
    "cost 20%, speed to pilot 15% — higher is better on every criterion.\n"
    "Scores (1-5, evidence in brackets):\n"
    "- Correspondence drafting: impact 4 [memo section 2: measured time "
    "savings], risk 4 [human review per section 3(a) catches errors], "
    "cost 4 [existing enterprise assistant], speed 5 [pilots already "
    "ran]. Weighted: 4.2.\n"
    "- 311 auto-triage: impact 4 [2,942 requests in top categories], risk "
    "2 [misrouted requests delay service; no accuracy data — partially "
    "unsupported], cost 3, speed 3. Weighted: 3.1.\n"
    "- Transcript summaries: impact 2 [small audience], risk 5 [public "
    "input only], cost 4, speed 4. Weighted: 3.6.\n"
    "Ranked shortlist: 1) correspondence drafting 4.2, 2) transcript "
    "summaries 3.6, 3) 311 auto-triage 3.1.\n"
    "Top risks: triage misclassification; review becoming a rubber stamp.\n"
    "Questions for the decision maker: what triage accuracy is acceptable? "
    "Who audits the reviewers?\n"
    "This is decision support — the decision belongs to the named official."
)

l5a = chat(
    [{"role": "user", "content":
      "Task level: Evaluate / Recommend.\n"
      "First restate the criteria and weights you will use, then judge "
      "against them — and against nothing else.\n"
      f"{RUBRIC}\n"
      "Score each candidate 1-5 per criterion, apply the weights exactly, "
      "and cite evidence for every score. If evidence is missing, mark the "
      "score \"unsupported\".\n"
      "Return: score table | ranked shortlist | top risks | questions for "
      "the decision maker. Close with: this is decision support, not the "
      "decision.\n\n"
      f"{CANDIDATES}"}],
    offline=CANNED_L5A, temperature=0.7)
print(l5a)

# %% [markdown]
# **Why this works:** rubric first, verdict second — the criteria are yours,
# the arithmetic is visible, and "unsupported" is an allowed score.
# **Before you trust it:** recompute one weighted score by hand. If the
# model's arithmetic disagrees with yours, its ranking is advisory at best.

# %% [markdown]
# ### Example 5B (worked) — Rank three options for strengthening the memo
#
# The interim memo works but audits are hard. Three policy options are on
# the table; the CDO wants a defensible ranking.

# %%
OPTIONS = (
    "Option A — Require each division to keep an AI-use log (tool, "
    "purpose, reviewer) for every AI-assisted product.\n"
    "Option B — Extend the human-review rule to internal-only products, "
    "not just constituent-facing ones.\n"
    "Option C — Prohibit public AI tools entirely, including for public "
    "information."
)

CANNED_L5B = (
    "Criteria restated: risk reduction 40%, operational burden 25% (higher "
    "score = lower burden), auditability 20%, staff acceptance 15%.\n"
    "1. Option A (AI-use log) — ranked first. Directly attacks the "
    "unreviewed-release risk in the memo's background; cheap to run; makes "
    "every other control auditable. Scores: risk 5, burden 4, audit 5, "
    "acceptance 4. Weighted: 4.6.\n"
    "2. Option B (review internal products too) — second. More assurance, "
    "but roughly doubles review load for material that never leaves the "
    "building. Scores: risk 4, burden 2, audit 3, acceptance 3. Weighted: "
    "3.2.\n"
    "3. Option C (ban public tools) — last. Removes one exposure path but "
    "pushes staff to unmanaged personal accounts — shadow use the log "
    "would have caught. Scores: risk 3, burden 2, audit 1, acceptance 1. "
    "Weighted: 2.2.\n"
    "Flagged as unsupported: all acceptance scores rest on no survey "
    "evidence — collect staff feedback before finalizing.\n"
    "Recommendation: adopt A now, pilot B in one division, reject C as "
    "counterproductive. Decision support, not the decision."
)

l5b = chat(
    [{"role": "user", "content":
      "Task level: Evaluate / Rank.\n"
      "Criteria: risk reduction 40%, operational burden 25% (higher score "
      "= lower burden), auditability 20%, staff acceptance 15%.\n"
      "Restate the criteria, score each option 1-5 per criterion with the "
      "weights applied exactly, rank the options, and flag any score that "
      "lacks evidence as \"unsupported\". Ground every risk claim in the "
      "memo below.\n\n"
      f"Memo:\n{memo}\n\n{OPTIONS}"}],
    offline=CANNED_L5B, temperature=0.8)
print(l5b)

# %% [markdown]
# **Why this works:** the criteria and weights are fixed before the verdict,
# risk claims must trace to the memo, and the Option C reasoning shows why
# evaluation needs domain judgment, not just arithmetic. **Before you trust
# it:** ask who is accountable if the ranking is wrong — at Level 5 there
# must be a named human, and it is not the model.

# %% [markdown]
# ### Example 5C (your turn) — Critique the vendor claim
#
# A vendor pitches: *"Our chatbot deflects 60% of constituent calls at 99%
# accuracy."* All you have is the federal use-case inventory slice. Write
# the prompt: what does the evidence support, what is unsupported, and what
# three questions would you put to the vendor?

# %%
CANNED_L5C = (
    "Claim under review: \"deflects 60% of calls at 99% accuracy.\"\n"
    "Supported by the inventory slice: nothing. The inventory records "
    "purpose, development stage, and data descriptions — it carries no "
    "deflection or accuracy metrics for any listed system. (given)\n"
    "Undefined terms (given): \"deflected\" — to where, and measured how? "
    "\"accuracy\" — judged by whom, on what labelled sample?\n"
    "Plausible but unverified (inferred): triage and summarization pilots "
    "do exist in government — the DHS and CFTC entries show the genre — so "
    "the claim is not impossible. It is unaudited.\n"
    "Questions for the vendor: (1) How large was the evaluation dataset "
    "and who labelled it? (2) What exactly counts as \"deflected\", and "
    "what is the downstream escalation rate? (3) Which comparable "
    "government deployment can we call?\n"
    "Until those arrive, treat the claim as marketing, not evidence."
)

l5c = None
# YOUR CODE: chat() with the vendor claim and the uc_slice text
# (uc_slice.to_string(index=False, max_colwidth=60)); ask what the evidence
# supports, what is unsupported, and three questions for the vendor.
# Require claim labels. Pass offline=CANNED_L5C, temperature=0.8.

if l5c is None:
    l5c = CANNED_L5C
    print("(canned critique — write your evaluation prompt above to run "
          "your own)\n")
print(l5c)

# %% [markdown]
# ## Level 6 — Create: synthesize the novel
#
# **What you're asking:** design, invent, or draft something genuinely new —
# a concept, a plan, an artifact. Maximal output space, peak creativity, no
# answer key.
#
# - **Risk:** *unverifiable plausibility* — coherent, confident, and
#   possibly unworkable, with nothing to check against.
# - **Prompt move:** scaffold. Hard constraints, several divergent options
#   *before* any refinement, an explicit risk statement per option, and
#   ideation separated from evaluation.
# - **Temperature 0.7–1.0:** the associative divergence this level needs.
# - **Verify by:** domain judgment + structured audit. Only expertise can
#   tell good output from confident nonsense here.

# %% [markdown]
# ### Example 6A (worked) — Three pilot concepts for a permitting office
#
# A city permitting office wants GenAI pilot ideas. The instinct is to ask
# for "the best idea" — the discipline is to demand three *distinct*
# concepts under hard constraints, then evaluate separately.

# %%
CANNED_L6A = (
    "Concept 1 — Completeness pre-check. User: permit applicant. Problem: "
    "a large share of applications bounce for missing documents. Flow: "
    "applicant uploads a draft package; the assistant lists missing items "
    "against the published checklist; a human clerk makes the final call. "
    "Assumptions: the checklist is current. Risks: an outdated checklist "
    "gives false confidence. MVP experiment: shadow-run on 50 historical "
    "rejected applications and measure the catch rate. Why distinct: helps "
    "*before* submission.\n"
    "Concept 2 — Plain-language status explainer. User: resident checking "
    "a permit. Problem: cryptic status codes generate phone calls. Flow: "
    "the status page renders the code in plain language with the next "
    "step; the assistant never advises beyond the code. Assumptions: code "
    "definitions are documented. Risks: over-explaining a legal hold. MVP: "
    "the 20 most common codes, readability-tested with 10 residents. "
    "Distinct: explains *after* submission; generates no decisions.\n"
    "Concept 3 — Inspector report first-drafter. User: field inspector. "
    "Problem: an hour a day lost to typing notes. Flow: voice notes become "
    "a structured draft in the report template; the inspector edits and "
    "signs. Assumptions: template fields are stable. Risks: invented "
    "observations — every sentence must trace to the audio. MVP: 5 "
    "inspectors, 2 weeks, measure edit distance between draft and final. "
    "Distinct: internal productivity with human authorship preserved.\n"
    "All three keep a human as the decision-maker, per the memo's review "
    "clause."
)

l6a = chat(
    [{"role": "user", "content":
      "Task level: Create / Design.\n"
      "Generate three DISTINCT generative-AI pilot concepts for a city "
      "permitting office.\n"
      "Hard constraints: existing staff only; no auto-approval of any "
      "permit decision; WCAG-AA accessible; shippable as a 90-day pilot.\n"
      "For each concept give: target user | problem | flow | assumptions | "
      "risks | MVP experiment | why it is meaningfully different from the "
      "other two.\n"
      "Produce all three before refining any one. Do not evaluate them — "
      "evaluation is a separate step with its own rubric."}],
    offline=CANNED_L6A, temperature=0.9)
print(l6a)

# %% [markdown]
# **Why this works:** the constraints fence the design space, "three
# distinct before refining" forces divergence, and deferring evaluation
# keeps Create and Evaluate from contaminating each other. **Before you
# trust it:** only someone who knows permitting can judge these — that is
# the definition of Level 6 risk. Circulate to a domain expert, with the
# assumptions list on top.

# %% [markdown]
# ### Example 6B (worked) — The public AI-use notice
#
# The division must post a public notice about how it uses AI in
# constituent services. Two audiences, two registers, same memo rules.

# %%
CANNED_L6B = (
    "Formal (website): \"This division uses approved artificial-"
    "intelligence tools to help draft routine correspondence and summarize "
    "public documents. Every AI-assisted product is reviewed and approved "
    "by a responsible employee before release. AI tools receive public "
    "information only. AI-assisted correspondence that documents agency "
    "business is retained as a federal record. Questions: Office of the "
    "Chief Data Officer.\"\n"
    "Plain-language (service counter): \"We sometimes use AI to help write "
    "letters and summarize public records. A person always checks the work "
    "before anything goes out. We never put your personal information into "
    "public AI tools. Ask us if you want to know more.\""
)

l6b = chat(
    [{"role": "user", "content":
      "Task level: Create / Draft.\n"
      "Draft a public notice about how the division uses AI in constituent "
      "services, in two variants: (1) formal, for the website, 80 words or "
      "fewer; (2) plain-language, for a service-counter poster, 60 words "
      "or fewer.\n"
      "Both must stay consistent with the memo below — human review, "
      "public information only, federal-record retention, point of "
      "contact. Invent no capabilities or guarantees the memo does not "
      "state.\n\n"
      f"{memo}"}],
    offline=CANNED_L6B, temperature=0.8)
print(l6b)

# %% [markdown]
# **Why this works:** even at Create, the memo is the tether — "invent no
# guarantees the memo does not state" keeps creativity from becoming a
# compliance incident. **Before you trust it:** legal and communications
# review. "A person always checks the work" is a public commitment; someone
# accountable must own it.

# %% [markdown]
# ### Example 6C (your turn) — The 311 triage concept note
#
# Streets & Sanitation asks for a one-paragraph concept note: automate
# triage of incoming 311 requests. Write the prompt requiring: concept |
# data used (no requester PII) | where the human stays in the loop |
# biggest failure mode and its mitigation | the metric that proves it
# works.

# %%
CANNED_L6C = (
    "Concept: a triage assistant for Streets & Sanitation 311 intake that "
    "suggests the routing category and a draft priority for each new "
    "request. Data used: request type, description text, and ward — never "
    "requester name, address, or contact details. Human-in-the-loop: every "
    "low-confidence classification and any request open longer than 48 "
    "hours routes to a human dispatcher, who can override with one click. "
    "Biggest failure mode: a water-main break misclassified as routine "
    "flooding — mitigated by a keyword escalation list that bypasses the "
    "model entirely. Metric: median minutes-to-correct-department against "
    "the current baseline, reviewed weekly with the dispatch leads. Level "
    "check: the concept mixes Apply (classification) and Evaluate "
    "(priority scoring), so it is governed at the higher level — Evaluate."
)

l6c = None
# YOUR CODE: chat() asking for the concept note described above. You may
# ground it in sr_counts.to_string(). Pass offline=CANNED_L6C,
# temperature=0.9.

if l6c is None:
    l6c = CANNED_L6C
    print("(canned concept note — write your design prompt above to run "
          "your own)\n")
print(l6c)

# %% [markdown]
# ## Step 8 — Pull it down the ladder (4 min)
#
# The single most powerful risk technique: **decompose high-level work into
# lower-level substeps.** A Create task usually breaks into Analyze +
# Evaluate + a much smaller Create — each stage prompted and validated at
# its own level, shrinking the unfalsifiable core you must take on faith.
#
# | Stage | Level | Purpose | Output |
# |---|---|---|---|
# | 1 · Retrieve | Remember | Find the relevant source passages | Quotes, IDs, metadata |
# | 2 · Summarize | Understand | Convert evidence into usable notes | Neutral summary with caveats |
# | 3 · Apply | Apply | Run the rules or standards | Preliminary classification |
# | 4 · Analyze | Analyze | Identify patterns and causes | Hypotheses + evidence |
# | 5 · Evaluate | Evaluate | Score the alternatives | Rubric table + recommendation |
# | 6 · Create | Create | Draft the solution or artifact | Plan, design, or message |
#
# Govern the whole pipeline at its **highest** consequential level — but
# verify each stage at its own.
#
# #### Your decomposition (write here)
#
# Take Example 6C's 311-triage concept and fill in one line per stage:
#
# - Retrieve:
# - Summarize:
# - Apply:
# - Analyze:
# - Evaluate:
# - Create:

# %% [markdown]
# ## Deliverable
# 1. All six `# YOUR CODE` prompts (1C–6C) with their outputs.
# 2. For one output per level, one sentence: what you would check before
#    trusting it.
# 3. The six-stage pipeline decomposition of the 311-triage concept.

# %% [markdown]
# ## Reflection
# 1. At which level did the canned/worked output *look* most trustworthy
#    relative to how much verification it actually deserves?
# 2. Which level's prompt had to carry the most structure? Why does that
#    surprise people?
# 3. Name one task from your own work and classify it. What level did you
#    *used* to prompt it at?

# %% [markdown]
# ## Debrief (instructor-led)
#
# - **Same data, six asks.** Compare one student's L1 output with another's
#   L6 output on the same file. What changed — the model, or the task?
# - **The human reviewer's address.** At which level does a non-expert
#   reviewer stop being enough? (The Analyze/Evaluate boundary — where the
#   *kind* of risk changes, not just its size.)
# - **Live vs canned.** Re-run one cell per level with the key present. Did
#   the level's characteristic risk show up in the live output?
# - **Bridge to Lab 4.3.** Which of your six prompts would most improve if
#   it were rebuilt as a full Persona–Task–Context–Format contract? That is
#   the next lab.

# %% [markdown]
# ## Troubleshooting
#
# - **`FileNotFoundError: data/gov_memo.txt`** — the kernel's working
#   directory is not `labs/`. Restart the kernel from the `labs/` folder
#   and Run All.
# - **`ModuleNotFoundError: lab_common`** — same cause: the notebook must
#   run with `labs/` as its working directory.
# - **Every AI cell prints "(canned ...)"** — no API key is visible. On the
#   classroom VM the key is injected; on your own machine it comes from the
#   course `.env`. The lab is fully usable either way.
# - **Live output ignores the temperature or format** — re-run the cell;
#   if a high-level (5–6) prompt returns a flat summary, the model drifted
#   down the ladder. Add "task level:" back to the first line and demand
#   the structure explicitly. Models default to the lowest level available.
# - **`quote verified in policy: False`** — the model (or you) produced a
#   quote that is not in the source. That is the Level 1 lesson: require
#   the quote, then check it mechanically before you trust the answer.
