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
# # Lab 3.2 — Prompt the Ladder: Bloom's Taxonomy  *(SOLUTION / instructor copy)*
#
# **Chapter 3 — Desktop GenAI at Work** · 45 minutes
#
# **Objectives**
# 1. Classify a government GenAI task by Bloom level before prompting.
# 2. Write and run three prompts at each of the six levels.
# 3. Match temperature and verification strategy to the level.
# 4. Explain each level's characteristic risk and its control.
#
# Framework: revised Bloom's taxonomy (Anderson & Krathwohl, 2001) mapped to
# generative AI, adapted from neurals.ca/agents/concepts/bloom-taxonomy.

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
# ## Setup — the substrate

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

print("substrate ready:",
      f"{len(sr_counts)} 311 types, {len(uc_slice)} use cases, "
      f"{len(aqi_hot)} AQI counties")

# %% [markdown]
# ## Level 1 — Remember
#
# **Instructor note.** Every worked prompt at this level fences the model
# into the source ("use only", "exact quote", "not stated"). Expected
# student stumble: prompts that forget the escape hatch, inviting
# fabrication. Temperature 0.0 throughout — point out that L1 wants zero
# creativity.

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
# ### 1C — worked: quote the bright line
#
# **Worked prompt + what to look for:** the answer must be verbatim — the
# mechanical check below must print `True`. If a student's prompt elicits a
# paraphrase, tighten "verbatim quote, no commentary".

# %%
CANNED_L1C = ("Pasting a constituent's record into a public chatbot is a "
              "reportable data spill.")

l1c = chat(
    [{"role": "user", "content":
      "Task level: Remember / Quote.\n"
      "From the policy below, return the exact sentence that states the "
      "consequence of pasting a constituent's record into a public "
      "chatbot. One verbatim quote, no commentary, no paraphrase. If no "
      "such sentence exists, write \"not stated\".\n\n"
      f"{policy}"}],
    offline=CANNED_L1C, temperature=0.0)
print(l1c)
print("\nquote verified in policy:", l1c.strip().strip('"') in policy)

# %% [markdown]
# ## Level 2 — Understand
#
# **Instructor note.** The control is "preserve every exception/prohibition"
# — it converts the smoothing risk into a checklist. Have students count
# "must not"s in source vs output. Temperature still low (0.1–0.2).

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
# ### 2C — worked: the public-dashboard explainer
#
# **Worked prompt + what to look for:** numbers must survive exactly. Have
# students check 1,547 / 760 / 2,942 against `sr_counts` — smoothing shows
# up here as rounded or dropped figures.

# %%
CANNED_L2C = (
    "Aircraft noise complaints dominate this 311 extract with 1,547 "
    "requests, far ahead of general information calls at 760. Street "
    "flooding (\"Water On Street\") follows at 257, with tree emergencies "
    "(159), graffiti removal (136), and tree debris clean-up (83) rounding "
    "out the top six. Together these six categories account for 2,942 of "
    "the 4,000 requests in the file."
)

l2c = chat(
    [{"role": "user", "content":
      "Task level: Understand / Explain.\n"
      "Write three plain-language sentences for a public dashboard "
      "explaining the 311 request counts below. Preserve every number "
      "exactly — no rounding, no dropped categories. Describe the pattern "
      "only; do not speculate about causes.\n\n"
      f"{sr_counts.to_string()}"}],
    offline=CANNED_L2C, temperature=0.2)
print(l2c)

# %% [markdown]
# ## Level 3 — Apply
#
# **Instructor note.** The prompt carries the whole procedure: ordered
# rules, "first match wins", an escalation bucket, cited rules per decision.
# The verification is a known-answer test — students should already know
# where each input lands. Temperature 0.3–0.4.

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
# ### 3C — worked: run the masking procedure
#
# **Worked prompt + what to look for:** the executional check below must
# print "none". If a student's output keeps any raw field, the procedure
# failed — that is an Apply-level (executional) error, caught by testing.

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

l3c = chat_json(
    [{"role": "user", "content":
      "Task level: Apply / Execute a procedure.\n"
      "Procedure: mask the fields name, ssn, email, phone, and address by "
      "replacing their values with \"[REDACTED]\". Keep case_id, topic, "
      "summary, and status unchanged. Do not add or remove fields.\n"
      "Return a JSON object with exactly these keys: case_id, name, ssn, "
      "email, phone, address, topic, summary, status.\n\n"
      f"Record:\n{json.dumps(citizen, indent=2)}"}],
    offline=CANNED_L3C, temperature=0.3)
print(json.dumps(l3c, indent=2))

leaked = [f for f in ("name", "ssn", "email", "phone", "address")
          if l3c.get(f) == citizen[f]]
print("\nfields left unmasked:", leaked or "none — procedure executed cleanly")

# %% [markdown]
# ## Level 4 — Analyze
#
# **Instructor note.** Claim labels (given / inferred / assumption) are the
# control. Push students on any "(given)" that is not literally in the
# table — that is where spurious connections hide. Temperature 0.4–0.5.

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
# ### 4C — worked: trace the AQI anomaly
#
# **Worked prompt + what to look for:** the key teaching beat is the last
# line — annual counts cannot separate a season from an episode. Students
# who accept "ozone causes the hazardous peak" have read correlation as
# cause.

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

l4c = chat(
    [{"role": "user", "content":
      "Task level: Analyze / Trace.\n"
      "The row below is the US county with the most unhealthy air-quality "
      "days in 2024. Which pollutant dominates its measurement days? Offer "
      "two competing hypotheses for the unhealthy-day pattern, label every "
      "claim (given), (inferred), or (assumption), and name the daily data "
      "that would confirm or kill each hypothesis. Do not present "
      "correlation as causation.\n\n"
      f"{aqi_row}"}],
    offline=CANNED_L4C, temperature=0.5)
print(l4c)

# %% [markdown]
# ## Level 5 — Evaluate
#
# **Instructor note.** Rubric first, verdict second — criteria are fixed by
# the human, scores carry evidence, "unsupported" is allowed, and the close
# is always "decision support, not the decision." Have students recompute
# one weighted score by hand. Temperature 0.7–0.8.

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
# ### 5C — worked: critique the vendor claim
#
# **Worked prompt + what to look for:** the finding is "supported: nothing"
# — students often expect the model to split the difference. The discipline
# is that absence of evidence is itself the finding, plus three sharp
# questions.

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

l5c = chat(
    [{"role": "user", "content":
      "Task level: Evaluate / Critique.\n"
      "A vendor claims their chatbot \"deflects 60% of constituent calls "
      "at 99% accuracy.\" Using only the inventory rows below as evidence: "
      "state what the evidence supports, what is unsupported, which terms "
      "are undefined, and three questions to put to the vendor. Label "
      "every claim (given), (inferred), or (assumption). Do not accept or "
      "reject the claim — audit it.\n\n"
      f"{uc_slice.to_string(index=False, max_colwidth=60)}"}],
    offline=CANNED_L5C, temperature=0.8)
print(l5c)

# %% [markdown]
# ## Level 6 — Create
#
# **Instructor note.** Scaffold, don't loosen: hard constraints, three
# divergent concepts before any refinement, risks per concept, evaluation
# explicitly deferred. Temperature 0.8–0.9. Only domain judgment verifies
# this level — circulate outputs with the assumptions list on top.

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
# ### 6C — worked: the 311 triage concept note
#
# **Worked prompt + what to look for:** the closing "level check" is the
# teachable moment — real workflows mix levels, and you govern at the
# highest. Students who skip the failure mode have not finished the
# exercise.

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

l6c = chat(
    [{"role": "user", "content":
      "Task level: Create / Design.\n"
      "Write a one-paragraph concept note for automating triage of "
      "incoming 311 requests for Streets & Sanitation. Include: the "
      "concept | the data it may use (no requester PII) | where the human "
      "stays in the loop | the biggest failure mode and its mitigation | "
      "the metric that proves it works. End with a \"level check\": which "
      "Bloom levels does the concept mix, and which level should govern "
      "it? Ground the volume argument in the counts below.\n\n"
      f"{sr_counts.to_string()}"}],
    offline=CANNED_L6C, temperature=0.9)
print(l6c)

# %% [markdown]
# ## Step 8 — Pull it down the ladder (worked)
#
# **Model answer** for the 311-triage decomposition:
#
# - **Retrieve:** pull the request type, description, and ward for each new
#   311 request — fields only, no requester PII. (Remember)
# - **Summarize:** one neutral sentence per request, preserving every
#   stated fact. (Understand)
# - **Apply:** run the published routing rule list; unmatched types go to
#   Needs Human Review. (Apply)
# - **Analyze:** weekly, cluster the misroutes and overrides to find where
#   the rules fail. (Analyze)
# - **Evaluate:** monthly, score the pilot against minutes-to-correct-
#   department and escalation accuracy; a named supervisor signs off.
#   (Evaluate)
# - **Create:** only now draft rule-list changes or new categories, each
#   with a risk note. (Create)
#
# Verification matches the level at every stage — mechanical at 1–3, expert
# at 4, accountable human at 5–6.

# %% [markdown]
# ## Grading notes
#
# - **Six student prompts (1C–6C):** full marks when the prompt names the
#   task level, carries the level's control (fences at 1–2, procedure at 3,
#   claim labels at 4, rubric-first at 5, constraints + divergence at 6),
#   and uses the level's temperature band.
# - **"What I would check" sentences:** must match the level's verification
#   column — mechanical at the bottom, expert judgment at the top.
# - **Pipeline decomposition:** one line per stage, governed at the highest
#   level present.
