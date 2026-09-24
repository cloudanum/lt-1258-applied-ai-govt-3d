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
# # Lab 4.3 — The PTCF Upgrade  *(SOLUTION / instructor copy)*
#
# **Chapter 4 — Modern GenAI and Prompt Engineering** · 45 minutes
#
# **Objectives**
# 1. Decompose any prompt into the four PTCF pillars.
# 2. Rebuild all six Bloom levels as PTCF prompts; score base vs PTCF.
# 3. Name which PTCF component does the most work at each level.
# 4. Diagnose and repair a misaligned PTCF contract.
#
# Frameworks: PTCF from *The Art of Agent Prompting* (30 Agents, Ch. 3);
# Bloom levels from neurals.ca/agents/concepts/bloom-taxonomy.

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
# ## Setup — the substrate (identical to Lab 3.2)

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

print("substrate ready")

# %%
BASE = {
    "L1A": "List the dates and deadlines in this memo.",
    "L1B": "Which of these use cases are pre-deployment?",
    "L1C": "What does the policy say about pasting constituent records "
           "into a public chatbot?",
    "L2A": "Summarize this memo for a new employee.",
    "L2B": "Explain the data categories in this policy to a contractor.",
    "L2C": "Write a few sentences about these 311 counts for the public.",
    "L3A": "Classify these 311 request types.",
    "L3B": "For each scenario, say if it's allowed under the policy.",
    "L3C": "Mask the PII in this record and return JSON.",
    "L4A": "What's driving the top 311 request types by ward?",
    "L4B": "Compare these two AI use cases.",
    "L4C": "What's causing the unhealthy air days in this county?",
    "L5A": "Which of these three GenAI candidates should we pilot next?",
    "L5B": "Rank these three options for improving the memo.",
    "L5C": "Is this vendor claim believable?",
    "L6A": "Give me GenAI pilot ideas for a permitting office.",
    "L6B": "Draft a public notice about our AI use.",
    "L6C": "Write a concept note for automating 311 triage.",
}
print(f"{len(BASE)} base prompts loaded")

# %%
scorecard = {}

# %% [markdown]
# ## Level 1 — Remember
#
# **Instructor note.** The base output drops the 3(a) row and paraphrases
# the 3(b) quote ("Suspected" vanished) — Accuracy 3, Completeness 2.
# Point out that every fence in the PTCF version lives in a different
# pillar: boundary in Task, sourcing in Context, verbatim in Format.

# %%
CANNED_BASE_L1A = (
    "Key dates: the memo is from March 14, 2026 and takes effect "
    "immediately. Exposure must be reported within one business day. The "
    "guidance stays in effect until replaced."
)

CANNED_PTCF_L1A = (
    "section | requirement | timeframe | supporting quote\n"
    "3(a) | human review before release | not stated | not stated\n"
    "3(b) | report suspected exposure | within one business day | "
    "\"Suspected exposure must be reported within one business day.\"\n"
    "4 | effective date | immediately (memo date: March 14, 2026) | "
    "\"This guidance is effective immediately\"\n"
    "4 | expiry | until superseded | "
    "\"remains in effect until superseded by final Department policy.\""
)

base_l1a = chat(
    [{"role": "user", "content": f"{BASE['L1A']}\n\n{memo}"}],
    offline=CANNED_BASE_L1A, temperature=0.0)
print("BASE:\n", base_l1a, "\n" + "=" * 60 + "\n")

PTCF_L1A = (
    "[PERSONA] You are a meticulous records-management analyst with ten "
    "years of experience auditing federal memoranda. Your communication is "
    "precise and literal.\n"
    "[TASK] Extract every date, deadline, and reporting timeframe from the "
    "memorandum provided. You must not infer, complete, or estimate any "
    "date. Where no timeframe is stated, record \"not stated\".\n"
    "[CONTEXT] Your table feeds a compliance audit workbook; the memorandum "
    "between <memo> tags is the only authoritative source. When the text "
    "is ambiguous, prefer \"not stated\" over guessing.\n"
    "[FORMAT] A pipe-delimited table: section | requirement | timeframe | "
    "exact supporting quote. No commentary before or after."
)

ptcf_l1a = chat(
    [{"role": "system", "content": PTCF_L1A},
     {"role": "user", "content": f"<memo>\n{memo}\n</memo>"}],
    offline=CANNED_PTCF_L1A, temperature=0.0)
print("PTCF:\n", ptcf_l1a)

scorecard["L1A_base"] = {"accuracy": 3, "completeness": 2, "format": 2, "tone": 3}
scorecard["L1A_ptcf"] = {"accuracy": 5, "completeness": 5, "format": 5, "tone": 5}

# %%
CANNED_PTCF_L1B = (
    "agency_name | use_case_name | stage_verbatim\n"
    "Commodity Futures Trading Commission | Stress Testing Scenarios with "
    "Deep Learning | Pre-deployment\n"
    "Department of Homeland Security | Smartphone Information Forensics "
    "Triage | Pre-deployment\n"
    "(2 rows matched the exact stage value; no stages were interpreted or "
    "grouped.)"
)

PTCF_L1B = (
    "[PERSONA] You are an oversight analyst preparing a briefing table for "
    "Congress; you copy values verbatim and never editorialize.\n"
    "[TASK] From the inventory rows provided, select every use case whose "
    "development_stage is exactly \"Pre-deployment\". You must not treat "
    "\"Pilot\" or any other stage as equivalent.\n"
    "[CONTEXT] The rows below are an official extract; matching is on the "
    "exact stage string, not its spirit. If no row matches, report "
    "\"none\".\n"
    "[FORMAT] Pipe-delimited table: agency_name | use_case_name | "
    "stage_verbatim, followed by one line stating how many rows matched. "
    "No other text."
)

ptcf_l1b = chat(
    [{"role": "system", "content": PTCF_L1B},
     {"role": "user", "content":
      uc_slice[["agency_name", "use_case_name", "development_stage"]]
      .to_string(index=False)}],
    offline=CANNED_PTCF_L1B, temperature=0.0)
print(ptcf_l1b)

# %% [markdown]
# ### 1C — worked: PTCF for the bright-line quote

# %%
CANNED_PTCF_L1C = ("Pasting a constituent's record into a public chatbot "
                   "is a reportable data spill.")

PTCF_L1C = (
    "[PERSONA] You are a compliance trainer who quotes policy verbatim and "
    "never paraphrases.\n"
    "[TASK] Return the exact sentence from the policy provided that states "
    "the consequence of pasting a constituent's record into a public "
    "chatbot. You must not paraphrase, summarize, or comment. If no such "
    "sentence exists, write \"not stated\".\n"
    "[CONTEXT] The quote goes into a training deck and will be attributed "
    "to the policy; a paraphrase would put words in the policy's mouth. "
    "The provided text is the only source.\n"
    "[FORMAT] One quoted sentence, or \"not stated\". No other text."
)

ptcf_l1c = chat(
    [{"role": "system", "content": PTCF_L1C},
     {"role": "user", "content": policy}],
    offline=CANNED_PTCF_L1C, temperature=0.0)
print(ptcf_l1c)
print("\nquote verified in policy:", ptcf_l1c.strip().strip('"') in policy)

# %% [markdown]
# ## Level 2 — Understand
#
# **Instructor note.** The base summary keeps three of four guidance
# clauses and drops both the one-business-day deadline and the
# federal-record clause — the smoothing lesson in one paragraph. Typical
# scores: base 3/2/3/4, PTCF 5/5/5/5.

# %%
CANNED_BASE_L2A = (
    "The memo gives divisions interim rules for using generative AI in "
    "constituent services. Staff should use approved tools, review AI "
    "output before release, and avoid putting private data into public "
    "tools. It is effective immediately."
)

CANNED_PTCF_L2A = (
    "The memo sets interim rules for using generative AI in constituent "
    "services until the final policy arrives. A responsible employee must "
    "review and approve every AI-assisted product before it reaches a "
    "constituent or the public record — the employee, not the tool, is "
    "accountable. Only public information may go into public AI tools; "
    "constituent records, Social Security numbers, and other PII must "
    "never enter an unapproved tool, and suspected exposure must be "
    "reported within one business day. Internal information may only be "
    "handled by the enterprise assistant under the Department's "
    "data-protection agreement. AI-assisted correspondence about agency "
    "business is a federal record and must be retained. The guidance is "
    "effective immediately. Caveat newcomers miss: even a rough AI-"
    "drafted letter about agency business is already a federal record."
)

base_l2a = chat(
    [{"role": "user", "content": f"{BASE['L2A']}\n\n{memo}"}],
    offline=CANNED_BASE_L2A, temperature=0.1)
print("BASE:\n", base_l2a, "\n" + "=" * 60 + "\n")

PTCF_L2A = (
    "[PERSONA] You are an onboarding writer for a federal department who "
    "turns policy into faithful plain language for new employees.\n"
    "[TASK] Summarize the provided memorandum for a new employee. Preserve "
    "every exception, deadline, and accountability rule. You must not add "
    "rules that are not present, and you must not drop any of the four "
    "guidance clauses.\n"
    "[CONTEXT] The summary is the employee's only briefing before their "
    "first week; a dropped caveat is a compliance incident. End with one "
    "sentence labelled \"Caveat newcomers miss:\".\n"
    "[FORMAT] One paragraph, 120 words or fewer, then the labelled caveat "
    "sentence. No headings, no bullets."
)

ptcf_l2a = chat(
    [{"role": "system", "content": PTCF_L2A},
     {"role": "user", "content": memo}],
    offline=CANNED_PTCF_L2A, temperature=0.1)
print("PTCF:\n", ptcf_l2a)

scorecard["L2A_base"] = {"accuracy": 3, "completeness": 2, "format": 3, "tone": 4}
scorecard["L2A_ptcf"] = {"accuracy": 5, "completeness": 5, "format": 5, "tone": 5}

# %%
CANNED_PTCF_L2B = (
    "1. Public data — published reports, open data from data.gov — may be "
    "used with any approved tool.\n"
    "2. Internal data — everyday work material — may be used only with the "
    "agency-provisioned enterprise assistant under the agency's "
    "data-protection agreement. Never a public chatbot.\n"
    "3. Sensitive or regulated data — PII, health, financial, law "
    "enforcement — may be used only with tools specifically authorized for "
    "that category.\n"
    "The bright line: you must not enter nonpublic information into any AI "
    "tool not approved for that data category; pasting a constituent's "
    "record into a public chatbot is a reportable data spill.\n"
    "When in doubt, treat the data as the more restricted category and ask "
    "the information security office."
)

PTCF_L2B = (
    "[PERSONA] You are a security-awareness trainer briefing first-week "
    "contractors; plain language, zero jargon, no softened prohibitions.\n"
    "[TASK] Explain the policy's three data categories and what the "
    "contractor may and must not do with each. Keep every \"must not\" "
    "explicit. You must not add permissions or exceptions that are not "
    "stated.\n"
    "[CONTEXT] The contractor starts Monday and has seen no other "
    "material; this briefing is their only guardrail. Add the standing "
    "rule for doubt: treat data as the more restricted category and ask "
    "the information security office.\n"
    "[FORMAT] Numbered list, one item per category, then a two-sentence "
    "\"bright line\" paragraph. 130 words or fewer."
)

ptcf_l2b = chat(
    [{"role": "system", "content": PTCF_L2B},
     {"role": "user", "content": policy}],
    offline=CANNED_PTCF_L2B, temperature=0.1)
print(ptcf_l2b)

# %% [markdown]
# ### 2C — worked: PTCF for the dashboard explainer

# %%
CANNED_PTCF_L2C = (
    "Aircraft noise complaints dominate this 311 extract with 1,547 "
    "requests, far ahead of general information calls at 760. Street "
    "flooding (\"Water On Street\") follows at 257, with tree emergencies "
    "(159), graffiti removal (136), and tree debris clean-up (83) "
    "rounding out the top six. Together these six categories account for "
    "2,942 of the 4,000 requests in the file."
)

PTCF_L2C = (
    "[PERSONA] You are an open-data portal editor who writes for the "
    "general public and treats every published number as auditable.\n"
    "[TASK] Write three plain-language sentences explaining the 311 "
    "request counts provided. Preserve every number exactly — no "
    "rounding, no dropped categories. Describe the pattern only; you "
    "must not speculate about causes.\n"
    "[CONTEXT] The text appears on a public dashboard where numbers are "
    "checked against the underlying file; an invented figure is a "
    "correction notice.\n"
    "[FORMAT] Three sentences, no list, no headline."
)

ptcf_l2c = chat(
    [{"role": "system", "content": PTCF_L2C},
     {"role": "user", "content": sr_counts.to_string()}],
    offline=CANNED_PTCF_L2C, temperature=0.2)
print(ptcf_l2c)

# %% [markdown]
# ## Level 3 — Apply
#
# **Instructor note.** The base categories ("Parks & Trees", "Electrical")
# are invented — plausible and wrong. Accuracy 1. The PTCF version's Task
# pillar carries the whole procedure; Format forces the rule citation that
# makes errors findable. Typical: base 1/3/3/3, PTCF 5/5/5/4.

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

INPUTS_311 = ("Tree Debris Clean-Up Request\nWater On Street Complaint\n"
              "Broken Street Light Complaint")

CANNED_BASE_L3A = (
    "Tree Debris Clean-Up Request -> Parks & Trees\n"
    "Water On Street Complaint -> Streets & Sanitation\n"
    "Broken Street Light Complaint -> Electrical"
)

CANNED_PTCF_L3A = (
    "Tree Debris Clean-Up Request -> Urban Forestry (rule 2)\n"
    "Water On Street Complaint -> Water & Drainage (rule 4)\n"
    "Broken Street Light Complaint -> Needs Human Review (rule 6 — no "
    "rule matches; escalated, not guessed)"
)

base_l3a = chat(
    [{"role": "user", "content":
      f"{BASE['L3A']}\n\n{INPUTS_311}"}],
    offline=CANNED_BASE_L3A, temperature=0.4)
print("BASE:\n", base_l3a, "\n" + "=" * 60 + "\n")

PTCF_L3A = (
    "[PERSONA] You are a 311 intake clerk with five years on the desk; you "
    "route by the book and take pride in never freelancing a category.\n"
    "[TASK] Classify each request type using only the routing rules below, "
    "applied in order — first match wins. You must not invent categories "
    "or use outside knowledge. If no rule matches, route to Needs Human "
    "Review.\n"
    f"[CONTEXT] Routing rules:\n{RULES_311}\n"
    "Misrouted requests delay service to residents, so an honest "
    "escalation always beats a confident guess.\n"
    "[FORMAT] One line per input: type -> category (rule number). No "
    "commentary."
)

ptcf_l3a = chat(
    [{"role": "system", "content": PTCF_L3A},
     {"role": "user", "content": INPUTS_311}],
    offline=CANNED_PTCF_L3A, temperature=0.4)
print("PTCF:\n", ptcf_l3a)

scorecard["L3A_base"] = {"accuracy": 1, "completeness": 3, "format": 3, "tone": 3}
scorecard["L3A_ptcf"] = {"accuracy": 5, "completeness": 5, "format": 5, "tone": 4}

# %%
SCENARIOS = (
    "Scenario 1: An employee pastes a published GAO report into a public "
    "chatbot and asks for a summary.\n"
    "Scenario 2: An employee pastes a constituent's home address into a "
    "public chatbot to draft a reply letter.\n"
    "Scenario 3: An employee drafts an internal memo using the "
    "agency-provisioned enterprise assistant."
)

CANNED_PTCF_L3B = (
    "Scenario 1 -> permitted | Public data | rule: 'Public data ... may be "
    "used with any approved tool.'\n"
    "Scenario 2 -> prohibited | Sensitive/regulated (PII) in an unapproved "
    "tool — reportable data spill | rule: 'must not enter nonpublic "
    "information into any AI tool that has not been approved for that "
    "data category.'\n"
    "Scenario 3 -> permitted | Internal data via the enterprise assistant "
    "| rule: 'Internal data may be used only with the agency-provisioned "
    "enterprise assistant.'\n"
    "Undetermined scenarios: none — all three resolve on stated facts."
)

PTCF_L3B = (
    "[PERSONA] You are an agency compliance officer who decides "
    "scenario-by-scenario and always shows the rule behind the decision.\n"
    "[TASK] For each scenario provided, decide permitted or prohibited, "
    "name the data category, and cite the exact policy rule relied on. If "
    "a scenario turns on a fact the policy does not give, answer \"cannot "
    "determine from policy\" — you must not fill gaps with assumptions.\n"
    "[CONTEXT] Your decisions go into security-awareness training "
    "material, so every one must be traceable to the policy text "
    "provided. Use no rule that is not in the text.\n"
    "[FORMAT] One line per scenario: scenario -> decision | category | "
    "rule: '<quoted rule>'. End with a line listing any undetermined "
    "scenarios, or 'none'."
)

ptcf_l3b = chat(
    [{"role": "system", "content": PTCF_L3B},
     {"role": "user", "content": f"Policy:\n{policy}\n\n{SCENARIOS}"}],
    offline=CANNED_PTCF_L3B, temperature=0.3)
print(ptcf_l3b)

# %% [markdown]
# ### 3C — worked: PTCF for the masking procedure

# %%
CANNED_PTCF_L3C = {
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

PTCF_L3C = (
    "[PERSONA] You are a data-privacy technician executing a standard "
    "de-identification procedure before records leave the boundary.\n"
    "[TASK] Execute this procedure exactly: replace the values of name, "
    "ssn, email, phone, and address with \"[REDACTED]\"; keep case_id, "
    "topic, summary, and status unchanged. Add no fields, remove no "
    "fields.\n"
    "[CONTEXT] The output feeds an analytics environment outside the "
    "privacy boundary; a single missed field is a reportable spill.\n"
    "[FORMAT] A JSON object with exactly these keys: case_id, name, ssn, "
    "email, phone, address, topic, summary, status. No commentary."
)

ptcf_l3c = chat_json(
    [{"role": "system", "content": PTCF_L3C},
     {"role": "user", "content": json.dumps(citizen, indent=2)}],
    offline=CANNED_PTCF_L3C, temperature=0.3)
print(json.dumps(ptcf_l3c, indent=2))

leaked = [f for f in ("name", "ssn", "email", "phone", "address")
          if ptcf_l3c.get(f) == citizen[f]]
print("\nfields left unmasked:", leaked or "none — procedure executed cleanly")

# %% [markdown]
# ## Level 4 — Analyze
#
# **Instructor note.** The base output states three causes as fact; none of
# them is in the table. That is the spurious-connection risk in one
# paragraph. The PTCF Format pillar (claim labels) is what makes the
# reasoning auditable. Typical: base 2/3/2/3, PTCF 5/5/5/4.

# %%
CANNED_BASE_L4A = (
    "Ward 41's aircraft noise complaints are caused by the airport nearby. "
    "Ward 28 residents clearly need better online services, which is why "
    "they call for information so often. Water complaints cluster in "
    "wards 35, 37 and 29 because of aging drainage infrastructure there."
)

CANNED_PTCF_L4A = (
    "1. Observable facts (given): Ward 41 holds nearly all aircraft-noise "
    "complaints (1,447); Ward 28 holds most information-only calls (698); "
    "water-on-street is spread thin across wards 35, 37, and 29.\n"
    "2. Symptom clusters: single-ward noise concentration; single-ward "
    "information-call concentration; diffuse flooding.\n"
    "3. Competing hypotheses:\n"
    "   H1 (inferred): Ward 41 contains or borders the airport. For: "
    "extreme single-ward concentration. Against: nothing in the data. "
    "Needed: a ward map.\n"
    "   H2 (inferred): Ward 28's call volume signals an online service "
    "gap. For: volume an order of magnitude above other wards. Against: "
    "call content not in the slice. Needed: call notes.\n"
    "   H3 (assumption): water complaints follow rainfall. Not testable "
    "here — need dates and weather data.\n"
    "4. Most likely: H1 — still a correlation until geography confirms "
    "it. Do not act on H2 or H3 without the missing data."
)

base_l4a = chat(
    [{"role": "user", "content":
      f"{BASE['L4A']}\n\n{ward_slice.to_string()}"}],
    offline=CANNED_BASE_L4A, temperature=0.5)
print("BASE:\n", base_l4a, "\n" + "=" * 60 + "\n")

PTCF_L4A = (
    "[PERSONA] You are a city performance analyst who has been burned by "
    "premature root-cause stories; you separate what the data says from "
    "what you suspect.\n"
    "[TASK] Analyze the 311 counts by ward provided. Surface symptom "
    "clusters, then offer three competing root-cause hypotheses with "
    "evidence for and against each, the missing data that would confirm "
    "or kill each, and the most likely cause with a confidence level. You "
    "must not present correlation as causation.\n"
    "[CONTEXT] Your readout goes to the city manager, who may act on it; "
    "a spurious connection here misdirects crews and budget. Every claim "
    "must be labelled (given), (inferred), or (assumption).\n"
    "[FORMAT] Four numbered sections: facts, clusters, hypotheses, most "
    "likely cause. Claim labels inline. Under 250 words."
)

ptcf_l4a = chat(
    [{"role": "system", "content": PTCF_L4A},
     {"role": "user", "content": ward_slice.to_string()}],
    offline=CANNED_PTCF_L4A, temperature=0.5)
print("PTCF:\n", ptcf_l4a)

scorecard["L4A_base"] = {"accuracy": 2, "completeness": 3, "format": 2, "tone": 3}
scorecard["L4A_ptcf"] = {"accuracy": 5, "completeness": 5, "format": 5, "tone": 4}

# %%
CANNED_PTCF_L4B = (
    "Shared (given): both are CFTC systems applied to the agency's own "
    "market data; neither is described as public-facing.\n"
    "Different (given): the first is Pre-deployment and exploratory — "
    "deep-learning stress-test scenarios; the second is Deployed and "
    "operational — anomaly detection for data loads.\n"
    "Different (inferred): the verification burden differs — measurable "
    "precision/recall for the deployed gate vs expert plausibility review "
    "for the scenario generator.\n"
    "Missing (given): no performance metrics for either system, so any "
    "accuracy comparison would be an assumption.\n"
    "Not addressed (by design): which is better — that is an Evaluate "
    "question and needs a rubric."
)

PTCF_L4B = (
    "[PERSONA] You are an oversight reviewer for an interagency AI working "
    "group; you compare systems soberly and say what the record cannot "
    "tell you.\n"
    "[TASK] Compare the two inventory rows provided: what is shared, what "
    "is different, what is missing, and one inference you are confident "
    "in. You must not praise, rank, or recommend — judgment is a separate "
    "task with its own rubric.\n"
    "[CONTEXT] Your note feeds a congressional briefing; claims must be "
    "checkable against the rows. Label every claim (given), (inferred), "
    "or (assumption).\n"
    "[FORMAT] Four labelled bullets — Shared / Different / Missing / Not "
    "addressed — then the one confident inference."
)

ptcf_l4b = chat(
    [{"role": "system", "content": PTCF_L4B},
     {"role": "user", "content":
      uc_slice.head(2).to_string(index=False, max_colwidth=80)}],
    offline=CANNED_PTCF_L4B, temperature=0.4)
print(ptcf_l4b)

# %% [markdown]
# ### 4C — worked: PTCF for the AQI trace

# %%
aqi_row = aqi_hot.head(1).to_string(index=False)

CANNED_PTCF_L4C = (
    "Dominant driver (given): ozone accounts for 218 of 366 measured days "
    "and PM2.5 for 123 in San Bernardino County; the 61 unhealthy days "
    "sit inside an ozone-dominated profile.\n"
    "H1 (inferred): a summer photochemical-smog regime downwind of the "
    "Los Angeles basin. For: ozone dominance. Against: nothing in the "
    "slice. Needed: daily AQI series and meteorology.\n"
    "H2 (inferred): episodic wildfire smoke drove the Max AQI of 593. "
    "For: extreme peak against a far lower median. Against: smoke days "
    "not flagged in the slice. Needed: fire-perimeter records and daily "
    "PM2.5.\n"
    "Bottom line: annual counts cannot separate a season from an episode "
    "— do not attribute the hazardous peak without the daily data."
)

PTCF_L4C = (
    "[PERSONA] You are an environmental program analyst who separates "
    "observation from hypothesis as a matter of habit.\n"
    "[TASK] Identify which pollutant dominates the county's measurement "
    "days, offer two competing hypotheses for the unhealthy-day pattern, "
    "and name the daily data that would confirm or kill each. Label every "
    "claim (given), (inferred), or (assumption). You must not attribute "
    "the hazardous peak to a cause on annual counts alone.\n"
    "[CONTEXT] Your note informs a regional air-quality program review; "
    "correlation-as-causation here misdirects mitigation funding.\n"
    "[FORMAT] Labelled claims, two hypotheses, bottom line — under 200 "
    "words."
)

ptcf_l4c = chat(
    [{"role": "system", "content": PTCF_L4C},
     {"role": "user", "content": aqi_row}],
    offline=CANNED_PTCF_L4C, temperature=0.5)
print(ptcf_l4c)

# %% [markdown]
# ## Level 5 — Evaluate
#
# **Instructor note.** The pivotal comparison of the lab: the base answer
# picks Candidate 2 using invisible criteria — and the stated rubric makes
# it the *loser*. Externalized criteria changed the answer, not just its
# presentation. Typical: base 2/2/2/4, PTCF 5/5/5/5.

# %%
CANDIDATES = (
    "Candidate 1 — Draft routine correspondence replies (pilots in the "
    "memo showed time savings; enterprise assistant already provisioned).\n"
    "Candidate 2 — Auto-triage 311 requests to departments (2,942 requests "
    "in the top six categories; no accuracy evidence available).\n"
    "Candidate 3 — Summarize public-meeting transcripts (public input "
    "only; smaller audience)."
)

RUBRIC = ("constituent impact 35%, risk of harm 30%, operating cost 20%, "
          "speed to pilot 15% — score 1–5, higher is better")

CANNED_BASE_L5A = (
    "I recommend Candidate 2, the 311 auto-triage. It has the largest "
    "volume and the biggest potential time savings, and routing is a "
    "well-understood problem. Candidates 1 and 3 are worthwhile but lower "
    "impact."
)

CANNED_PTCF_L5A = (
    "Rubric restated: constituent impact 35%, risk of harm 30%, operating "
    "cost 20%, speed to pilot 15% — higher is better on every criterion.\n"
    "Scores (1-5, evidence in brackets):\n"
    "- Correspondence drafting: impact 4 [memo section 2: time savings], "
    "risk 4 [human review per section 3(a)], cost 4 [existing assistant], "
    "speed 5 [pilots ran]. Weighted: 4.2.\n"
    "- 311 auto-triage: impact 4 [2,942 requests], risk 2 [misroutes delay "
    "service; no accuracy data — partially unsupported], cost 3, speed 3. "
    "Weighted: 3.1.\n"
    "- Transcript summaries: impact 2 [small audience], risk 5 [public "
    "input only], cost 4, speed 4. Weighted: 3.6.\n"
    "Ranked shortlist: 1) correspondence 4.2, 2) transcripts 3.6, 3) "
    "auto-triage 3.1.\n"
    "Top risks: triage misclassification; review as rubber stamp.\n"
    "Questions for the decision maker: acceptable triage accuracy? who "
    "audits reviewers?\n"
    "This is decision support — the decision belongs to the named "
    "official."
)

base_l5a = chat(
    [{"role": "user", "content": f"{BASE['L5A']}\n\n{CANDIDATES}"}],
    offline=CANNED_BASE_L5A, temperature=0.7)
print("BASE:\n", base_l5a, "\n" + "=" * 60 + "\n")

PTCF_L5A = (
    "[PERSONA] You are a senior policy advisor who prepares decision memos "
    "for a Chief Data Officer; your rankings are always auditable.\n"
    "[TASK] Score the three candidates against this rubric and nothing "
    f"else: {RUBRIC}. Restate the rubric first, score each criterion "
    "separately with evidence in brackets, apply the weights exactly, and "
    "mark any score that lacks evidence \"unsupported\".\n"
    "[CONTEXT] This memo informs but does not make the decision; a named "
    "official decides. Your audience will challenge every score, so "
    "unsupported assertions are worse than admitted gaps.\n"
    "[FORMAT] Rubric restatement | score table | ranked shortlist | top "
    "risks | questions for the decision maker | the closing line: this is "
    "decision support, not the decision."
)

ptcf_l5a = chat(
    [{"role": "system", "content": PTCF_L5A},
     {"role": "user", "content": CANDIDATES}],
    offline=CANNED_PTCF_L5A, temperature=0.7)
print("PTCF:\n", ptcf_l5a)

scorecard["L5A_base"] = {"accuracy": 2, "completeness": 2, "format": 2, "tone": 4}
scorecard["L5A_ptcf"] = {"accuracy": 5, "completeness": 5, "format": 5, "tone": 5}

# %%
OPTIONS = (
    "Option A — Require each division to keep an AI-use log (tool, "
    "purpose, reviewer) for every AI-assisted product.\n"
    "Option B — Extend the human-review rule to internal-only products, "
    "not just constituent-facing ones.\n"
    "Option C — Prohibit public AI tools entirely, including for public "
    "information."
)

CANNED_PTCF_L5B = (
    "Criteria restated: risk reduction 40%, operational burden 25% (higher "
    "= lower burden), auditability 20%, staff acceptance 15%.\n"
    "1. Option A — first: attacks the unreviewed-release risk directly; "
    "cheap; makes every other control auditable. Weighted: 4.6.\n"
    "2. Option B — second: more assurance, roughly double the review "
    "load. Weighted: 3.2.\n"
    "3. Option C — last: pushes staff to unmanaged personal accounts — "
    "shadow use the log would have caught. Weighted: 2.2.\n"
    "Unsupported: all acceptance scores — no survey evidence yet.\n"
    "Recommendation: adopt A, pilot B in one division, reject C. Decision "
    "support, not the decision."
)

PTCF_L5B = (
    "[PERSONA] You are a management analyst who has watched blanket bans "
    "fail; you rank options against stated criteria and say when evidence "
    "is thin.\n"
    "[TASK] Rank the three options using these criteria and weights: risk "
    "reduction 40%, operational burden 25% (higher score = lower burden), "
    "auditability 20%, staff acceptance 15%. Restate the criteria, score "
    "1-5 per criterion, apply weights exactly, flag unsupported scores. "
    "Ground every risk claim in the memo provided.\n"
    "[CONTEXT] The CDO acts on your ranking; a criterion you invent "
    "quietly becomes policy. Use the given criteria and no others.\n"
    "[FORMAT] Criteria restatement | ranked options with weighted scores | "
    "unsupported flags | one-paragraph recommendation ending: decision "
    "support, not the decision."
)

ptcf_l5b = chat(
    [{"role": "system", "content": PTCF_L5B},
     {"role": "user", "content": f"Memo:\n{memo}\n\n{OPTIONS}"}],
    offline=CANNED_PTCF_L5B, temperature=0.8)
print(ptcf_l5b)

# %% [markdown]
# ### 5C — worked: PTCF for the vendor critique

# %%
CANNED_PTCF_L5C = (
    "Claim under review: \"deflects 60% of calls at 99% accuracy.\"\n"
    "Supported by the inventory slice: nothing — the inventory records "
    "purpose, stage, and data descriptions; no performance metrics. "
    "(given)\n"
    "Undefined terms (given): \"deflected\" — to where, measured how? "
    "\"accuracy\" — judged by whom, on what sample?\n"
    "Plausible but unverified (inferred): government triage pilots exist "
    "— the genre is real; the numbers are unaudited.\n"
    "Questions for the vendor: (1) evaluation dataset size and labeller; "
    "(2) definition of \"deflected\" and the downstream escalation rate; "
    "(3) a comparable government deployment we can call.\n"
    "Disposition: treat as marketing until the answers arrive."
)

PTCF_L5C = (
    "[PERSONA] You are a procurement-science advisor who audits vendor "
    "performance claims for a living; unaudited numbers are marketing "
    "until proven otherwise.\n"
    "[TASK] Audit the vendor claim \"deflects 60% of constituent calls at "
    "99% accuracy\" using only the inventory rows provided as evidence: "
    "what the evidence supports, what is unsupported, which terms are "
    "undefined, and three questions for the vendor. You must not accept "
    "or reject the claim — audit it.\n"
    "[CONTEXT] The inventory records purpose, stage, and data descriptions "
    "only; if a metric is not there, it is not evidence. Label every "
    "claim (given), (inferred), or (assumption).\n"
    "[FORMAT] Labelled findings | three numbered questions | one-line "
    "disposition."
)

ptcf_l5c = chat(
    [{"role": "system", "content": PTCF_L5C},
     {"role": "user", "content":
      "Vendor claim: \"Our chatbot deflects 60% of constituent calls at "
      "99% accuracy.\"\n\nInventory evidence:\n"
      + uc_slice.to_string(index=False, max_colwidth=60)}],
    offline=CANNED_PTCF_L5C, temperature=0.8)
print(ptcf_l5c)

# %% [markdown]
# ## Level 6 — Create
#
# **Instructor note.** Base idea 2 ("approves simple permits instantly")
# violates the office's core constraint — the naive prompt never stated it.
# The Persona + Context pillars are the tether. Typical: base 2/2/2/3,
# PTCF 5/5/5/4.

# %%
CANNED_BASE_L6A = (
    "1. A chatbot that answers permit questions automatically.\n"
    "2. An AI that approves simple permits instantly to cut the backlog.\n"
    "3. An AI that inspects applications and decides which need review."
)

CANNED_PTCF_L6A = (
    "Concept 1 — Completeness pre-check. User: permit applicant. Problem: "
    "applications bounce for missing documents. Flow: assistant lists "
    "missing items against the published checklist; a human clerk "
    "decides. Assumptions: checklist is current. Risks: false confidence "
    "from an outdated checklist. MVP: shadow-run on 50 historical "
    "rejections, measure catch rate. Distinct: helps before submission.\n"
    "Concept 2 — Plain-language status explainer. User: resident. "
    "Problem: cryptic status codes generate calls. Flow: status page "
    "rendered in plain language; never advises beyond the code. Risks: "
    "over-explaining a legal hold. MVP: 20 common codes, readability test "
    "with 10 residents. Distinct: explains after submission, decides "
    "nothing.\n"
    "Concept 3 — Inspector report first-drafter. User: field inspector. "
    "Problem: an hour a day typing notes. Flow: voice notes to a "
    "structured draft; inspector edits and signs. Risks: invented "
    "observations — every sentence must trace to the audio. MVP: 5 "
    "inspectors, 2 weeks, edit-distance metric. Distinct: internal "
    "productivity, human authorship preserved.\n"
    "All three keep a human as the decision-maker, per the memo's review "
    "clause."
)

base_l6a = chat(
    [{"role": "user", "content": BASE["L6A"]}],
    offline=CANNED_BASE_L6A, temperature=0.9)
print("BASE:\n", base_l6a, "\n" + "=" * 60 + "\n")

PTCF_L6A = (
    "[PERSONA] You are a service designer who has shipped government "
    "pilots that survived audit; you are creative inside constraints and "
    "plain about risks.\n"
    "[TASK] Generate three DISTINCT generative-AI pilot concepts for a "
    "city permitting office. Produce all three before refining any one. "
    "You must not evaluate or rank them — evaluation is a separate step "
    "with its own rubric.\n"
    "[CONTEXT] Hard constraints: existing staff only; no auto-approval of "
    "any permit decision (a human decides, per the department's AI memo); "
    "WCAG-AA accessible; shippable as a 90-day pilot. Ideas that violate "
    "a constraint are failures, not stretch goals.\n"
    "[FORMAT] Per concept: target user | problem | flow | assumptions | "
    "risks | MVP experiment | why it is meaningfully different. End with "
    "one line naming the review clause all three concepts satisfy."
)

ptcf_l6a = chat(
    [{"role": "system", "content": PTCF_L6A},
     {"role": "user", "content":
      "Generate the three concepts now."}],
    offline=CANNED_PTCF_L6A, temperature=0.9)
print("PTCF:\n", ptcf_l6a)

scorecard["L6A_base"] = {"accuracy": 2, "completeness": 2, "format": 2, "tone": 3}
scorecard["L6A_ptcf"] = {"accuracy": 5, "completeness": 5, "format": 5, "tone": 4}

# %%
CANNED_PTCF_L6B = (
    "Formal (website): \"This division uses approved artificial-"
    "intelligence tools to help draft routine correspondence and "
    "summarize public documents. Every AI-assisted product is reviewed "
    "and approved by a responsible employee before release. AI tools "
    "receive public information only. AI-assisted correspondence that "
    "documents agency business is retained as a federal record. "
    "Questions: Office of the Chief Data Officer.\"\n"
    "Plain-language (service counter): \"We sometimes use AI to help "
    "write letters and summarize public records. A person always checks "
    "the work before anything goes out. We never put your personal "
    "information into public AI tools. Ask us if you want to know more.\""
)

PTCF_L6B = (
    "[PERSONA] You are a public-affairs writer who drafts plain-language "
    "government notices that survive legal review.\n"
    "[TASK] Draft the division's public AI-use notice in two variants. "
    "Stay consistent with the memo provided — human review, public "
    "information only, federal-record retention, point of contact. You "
    "must not invent capabilities, guarantees, or commitments the memo "
    "does not state.\n"
    "[CONTEXT] The notice is a public commitment; every sentence will be "
    "read as policy. Two audiences: website readers and service-counter "
    "visitors.\n"
    "[FORMAT] Variant 1 formal, 80 words or fewer; variant 2 plain-"
    "language, 60 words or fewer. Label each."
)

ptcf_l6b = chat(
    [{"role": "system", "content": PTCF_L6B},
     {"role": "user", "content": memo}],
    offline=CANNED_PTCF_L6B, temperature=0.8)
print(ptcf_l6b)

# %% [markdown]
# ### 6C — worked: PTCF for the triage concept note

# %%
CANNED_PTCF_L6C = (
    "Concept: a triage assistant for Streets & Sanitation 311 intake that "
    "suggests a routing category and draft priority for each new request. "
    "Data used: request type, description text, and ward — never "
    "requester name, address, or contact details. Human-in-the-loop: "
    "every low-confidence classification and any request open longer than "
    "48 hours routes to a human dispatcher with one-click override. "
    "Biggest failure mode: a water-main break misclassified as routine "
    "flooding — mitigated by a keyword escalation list that bypasses the "
    "model. Metric: median minutes-to-correct-department vs baseline, "
    "reviewed weekly with dispatch leads. Level check: mixes Apply "
    "(classification) and Evaluate (priority scoring) — govern at "
    "Evaluate."
)

PTCF_L6C = (
    "[PERSONA] You are a municipal service designer who writes concept "
    "notes that dispatch leads can critique in one read.\n"
    "[TASK] Write a one-paragraph concept note for automating triage of "
    "incoming 311 requests for Streets & Sanitation. Cover: the concept, "
    "the data it may use, where the human stays in the loop, the biggest "
    "failure mode and its mitigation, and the metric that proves it "
    "works. End with a \"level check\": which Bloom levels the concept "
    "mixes and which should govern it.\n"
    "[CONTEXT] Hard constraints: no requester PII (request type, "
    "description text, and ward only); a human dispatcher can override "
    "with one click; the volume argument must use the request counts "
    "provided.\n"
    "[FORMAT] One paragraph, then the labelled level-check line."
)

ptcf_l6c = chat(
    [{"role": "system", "content": PTCF_L6C},
     {"role": "user", "content": sr_counts.to_string()}],
    offline=CANNED_PTCF_L6C, temperature=0.9)
print(ptcf_l6c)

# %% [markdown]
# ## Step 3 — Anti-pattern diagnosis (worked)

# %%
CANNED_DIAG = (
    "The conflict: the Persona (\"creative, experimental, unconventional "
    "interpretations, clever workarounds\") pulls against the Task "
    "(\"apply exemptions correctly\") and the Context (\"legal "
    "liability\"). Exemption decisions are conservative, statute-bound "
    "judgments; a persona rewarded for novelty will stretch exemptions on "
    "the hard cases — exactly where liability lives. The Format pillar is "
    "the only one that fits.\n"
    "Repaired Persona: \"You are a careful FOIA officer with deep "
    "knowledge of the nine exemptions. You apply them conservatively, "
    "cite the exemption for every redaction, and refer genuinely novel "
    "questions of interpretation to the chief FOIA officer rather than "
    "resolving them creatively.\""
)
print(CANNED_DIAG)

# %% [markdown]
# ## Step 4 — Tally the scorecard

# %%
rows = []
for key, scores in scorecard.items():
    rows.append({"example": key, **scores, "total": sum(scores.values())})

tally = pd.DataFrame(rows)
print(tally.to_string(index=False))
base_mean = tally[tally["example"].str.endswith("base")]["total"].mean()
ptcf_mean = tally[tally["example"].str.endswith("ptcf")]["total"].mean()
print(f"\nmean total — base: {base_mean:.1f} vs PTCF: {ptcf_mean:.1f}")

# %% [markdown]
# ## Grading notes
#
# - **Six student PTCF contracts (1C–6C):** full marks when all four
#   pillars are present, the level's lead component carries the level's
#   control (fences at 1–2, procedure at 3, claim labels at 4, rubric +
#   boundary at 5, constraints at 6), and the call uses the level's
#   temperature band.
# - **Anti-pattern:** full marks for naming *which* pillars conflict and
#   *why it bites on ambiguous requests*; the repaired Persona must be
#   conservative, cite-driven, and include an escalation path for novel
#   interpretations.
# - **Scorecard:** expect the largest deltas at L3 (invented categories)
#   and L5 (winner flips). If a student's delta is zero at L5, they scored
#   the base output on presentation instead of auditability.
