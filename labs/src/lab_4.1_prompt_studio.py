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
# # Lab 4.1 — Prompt Engineering Studio
#
# *Chapter 4 — Modern GenAI and Prompt Engineering · 45 minutes · JupyterLab
# with pandas and the OpenAI API via `lab_common` (canned offline fallback)*
#
# This is the consolidation lab, and it is a ladder: four rungs, each one
# change to the prompt — **zero-shot → few-shot → role + format contract →
# reasoning-model comparison** — every output scored against the same rubric.
# The finding is not the four outputs; it is which single rung bought the most
# quality. Prompting spine: rung **P4**.
#
# Cells marked `# YOUR CODE` are for you. Offline, every call returns a
# realistic canned answer so you can keep working.

# %% [markdown]
# ## Objectives
#
# By the end of this lab, you will:
#
# - Measurably improve an output by iterating your prompt.
# - Apply zero-shot, few-shot, role + format, and reasoning-model techniques.
# - Score outputs against a rubric.

# %% [markdown]
# ## Setup
#
# **Datasets and files** (all under `labs/data/`):
#
# - `gov_memo.txt` — the **policy memo**: a synthetic CDO memorandum giving
#   interim guidance on generative AI for constituent services. Five lettered
#   rules in section 3. Substrate for rungs 1–3.
# - `constituent_feedback.csv` — the **constituent-feedback set**: fifteen
#   synthetic messages of mixed urgency. Substrate for rung 4.
# - `MANIFEST.json` — the **dataset description**: provenance for every file
#   in `data/`, public and synthetic.
# - `chicago_311.csv`, `corpus/ai_acceptable_use_policy.md` — used by the
#   stretch section.
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
# The workbook source pack: the policy memo, the constituent-feedback set, and
# the dataset description in `MANIFEST.json` — plus the two files the stretch
# section uses.

# %%
from lab_common import chat, chat_json

memo = open("data/gov_memo.txt").read()
policy = open("data/corpus/ai_acceptable_use_policy.md").read()

import pandas as pd
c311 = pd.read_csv("data/chicago_311.csv", low_memory=False)
sr_types = c311["sr_type"].dropna().unique().tolist()

# The constituent-feedback set: fifteen messages of deliberately mixed urgency,
# from routine records requests to two live safety emergencies. Rung 4's hard
# task.
feedback = pd.read_csv("data/constituent_feedback.csv")
complaints = feedback["text"].tolist()

print(f"memo: {len(memo)} chars | policy: {len(policy)} chars | "
      f"{len(sr_types)} distinct 311 request types | "
      f"{len(complaints)} constituent messages")

# %% [markdown]
# ## Steps
#
# The prompt ladder — four rungs, each one change to the prompt, each scored
# against the same rubric. The point is not the four outputs; it is seeing which
# single change bought the most quality.
#
# 1. **Zero-shot.** Ask the assistant to "summarize the policy memo." Score it.
#    ✓ You have a baseline output and a rubric score.
# 2. **Few-shot.** Give two examples of the summary style you want, then ask
#    again. ✓ You can see how examples changed the output.
# 3. **Role + format contract.** *"You are a policy analyst. Summarize the memo
#    as a 5-row table: rule | who it affects | effective date | source line."*
#    Score it. ✓ You have a structured, role-shaped output.
# 4. **Reasoning-model comparison.** Run the hardest task — classify each
#    constituent complaint by theme and urgency — on a standard model and on a
#    reasoning model. Compare. ✓ You can describe when the reasoning model
#    helped.
#
# Score every output 1–5 per rubric dimension and record it in the `scorecard`
# dict.

# %% [markdown]
# ### The course rubric — score every output 1–5 per dimension
#
# | Dimension | 1 | 3 | 5 |
# |---|---|---|---|
# | **Accuracy** | invented or wrong claims | minor overstatement | every claim supported |
# | **Completeness** | misses the point | covers it thinly | covers it, no padding |
# | **Format** | ignores instructions | mostly follows them | exactly what was asked |
# | **Tone** | wrong register | uneven | right for the audience |

# %%
scorecard = {}  # {pattern_name: {"accuracy": n, "completeness": n, "format": n, "tone": n}}
# You will fill this in as you go — it drives Stretch B (improve the weakest).

# %% [markdown]
# ### Rung 1 — Zero-shot (8 min)
#
# Ask the assistant to "summarize the policy memo" with no examples, no role, no
# scaffolding — the baseline everything else is measured against. Score it.

# %%
CANNED_ZEROSHOT = (
    "The memo gives divisions interim rules for using generative AI in "
    "constituent services: a human must review every AI-assisted product "
    "before release, only public information may go into public AI tools, "
    "internal work must use the approved enterprise assistant, and AI-drafted "
    "correspondence is a federal record that must be retained. It is "
    "effective immediately until a final policy is issued."
)

zero_shot = None
# YOUR CODE: chat() with a one-line user message asking for a summary of
# `memo`. Pass offline=CANNED_ZEROSHOT.

if zero_shot is None:
    zero_shot = CANNED_ZEROSHOT
    print("(canned zero-shot summary — write your prompt above to run your own)\n")
print(zero_shot)

# %% [markdown]
# ### Rung 2 — Few-shot (10 min)
#
# Same memo, same request — but first show the model **two examples of the
# summary style you want**. Nothing else changes. Write the two exemplars in the
# house style you would actually send: one line per rule, the affected group
# named, no throat-clearing.

# %%
CANNED_FEWSHOT = (
    "Human review — every division: no AI-assisted product reaches a "
    "constituent or the public record until a named employee has approved it. "
    "The employee carries the accountability, not the tool.\n"
    "Data handling — every employee: public information only in public tools. "
    "Constituent records and SSNs never go into an unapproved tool; suspected "
    "exposure is reported within one business day.\n"
    "Approved tools — division IT leads: internal work uses the enterprise "
    "assistant covered by the data-protection agreement. The CIO owns the list.\n"
    "Recordkeeping — records officers: AI-assisted correspondence documenting "
    "agency business is a federal record and follows the retention schedule.\n"
    "Disclosure — constituent-facing staff: say in the closing line when a "
    "reply was drafted with AI help, and log the tool and the reviewer."
)

few_shot = None
# YOUR CODE: write two exemplars showing the summary STYLE you want (take two
# rules from the memo and write them the way you would send them), then ask for
# the rest of the memo in that same style. chat() with offline=CANNED_FEWSHOT.

if few_shot is None:
    few_shot = CANNED_FEWSHOT
    print("(canned few-shot output — write your exemplars above to run your own)\n")
print(few_shot)
print("\n✓ Compare against rung 1. What did the two examples actually change —")
print("  the content, or the shape?")

# %% [markdown]
# ### Rung 3 — Role + format contract (12 min)
#
# Two changes at once, because they work as a pair: give the model a **role**
# and a **format contract**. The role sets what it optimises for; the contract
# says exactly what shape to return.
#
# > *"You are a policy analyst. Summarize the memo as a 5-row table:
# > rule | who it affects | effective date | source line."*
#
# The memo has five lettered rules in section 3 — one row each. The `source
# line` column is the one that keeps it honest: it forces the model to point at
# the clause it used, so you can check it.

# %%
ROLE_FORMAT_SYSTEM = "You are a policy analyst."
ROLE_FORMAT_ASK = (
    "Summarize the memo as a 5-row markdown table with exactly these columns: "
    "rule | who it affects | effective date | source line. One row per lettered "
    "rule in section 3. The source line column must quote the clause you used.")

CANNED_ROLE_FORMAT = """\
| rule | who it affects | effective date | source line |
|---|---|---|---|
| Human review before release | Every division releasing AI-assisted work | 2026-03-14 | "must be reviewed and approved by a responsible employee before release" |
| Public information only in public tools | All employees using AI tools | 2026-03-14 | "Only public information may be entered into public AI tools." |
| Use the approved enterprise assistant | Divisions handling internal information | 2026-03-14 | "Divisions must use the enterprise assistant provisioned under the Department's data-protection agreement" |
| Retain AI-assisted correspondence as a record | Records officers, correspondence staff | 2026-03-14 | "is a federal record and must be retained according to the applicable records schedule" |
| Disclose AI assistance and log the reviewer | Constituent-facing staff | 2026-03-14 | "must say so in a brief closing line" |"""

role_format = None
# YOUR CODE: chat() with ROLE_FORMAT_SYSTEM as the system message and
# ROLE_FORMAT_ASK + the memo as the user message. Pass
# offline=CANNED_ROLE_FORMAT.

if role_format is None:
    role_format = CANNED_ROLE_FORMAT
    print("(canned role+format output — write your call above to run your own)\n")
print(role_format)
print("\n✓ Five rows, four columns, every source line traceable to section 3?")
print("  Score format adherence honestly — a 4-row table is not a 5-row table.")

# %% [markdown]
# ### Rung 4 — Reasoning-model comparison (15 min)
#
# The hardest task in the lab: classify **every** constituent message by
# **theme** and **urgency**. Fifteen messages, mixed — two are live safety
# emergencies, one is a compliment, several are routine records requests. Run it
# on the standard model and on a reasoning model, then compare.
#
# Urgency is where they diverge. Getting theme right is pattern-matching;
# getting urgency right needs the model to notice that "flood water is coming up
# through the drain" outranks "I would like copies of the grant awards" even
# though both are politely worded.

# %%
from lab_common import CHAT_MODEL, REASONING_MODEL

TRIAGE_ASK = (
    "Classify each numbered constituent message by theme (a short noun phrase) "
    "and urgency (high / medium / low). Return one line per message as: "
    "N | theme | urgency. Judge urgency by consequence of delay, not by tone.")

numbered = "\n".join(f"{i}. {t}" for i, t in enumerate(complaints, 1))

CANNED_TRIAGE_STANDARD = """\
1 | air quality | medium
2 | disaster assistance | medium
3 | website accessibility | medium
4 | records request | low
5 | building safety | medium
6 | public health data | medium
7 | billing dispute | medium
8 | accessible parking | low
9 | positive feedback | low
10 | privacy complaint | medium
11 | flooding | high
12 | service navigation | low
13 | address correction | low
14 | records request | low
15 | benefits stopped | medium"""

CANNED_TRIAGE_REASONING = """\
1 | air quality / health impact | medium
2 | disaster assistance backlog | medium
3 | website accessibility (civil rights) | high
4 | records request | low
5 | gas odour — building safety | high
6 | public health data currency | high
7 | billing dispute | medium
8 | accessible parking (ADA) | medium
9 | positive feedback | low
10 | privacy breach — PII disclosed aloud | high
11 | active flooding — life safety | high
12 | service navigation | low
13 | address correction | medium
14 | records request | low
15 | benefits terminated without notice | high"""

def triage_with(model, canned):
    """One classification pass on the given model, with a canned fallback."""
    return chat([{"role": "user", "content": f"{TRIAGE_ASK}\n\n{numbered}"}],
                model=model, offline=canned)

if REASONING_MODEL == CHAT_MODEL:
    print(f"NOTE: OPENAI_REASONING_MODEL is unset, so both columns would be "
          f"{CHAT_MODEL}.\n      Set it in .env to run a real comparison; the "
          f"canned outputs below show\n      what the difference looks like.\n")

standard_out = triage_with(CHAT_MODEL, CANNED_TRIAGE_STANDARD)
reasoning_out = triage_with(REASONING_MODEL, CANNED_TRIAGE_REASONING)

print(f"--- standard model ({CHAT_MODEL}) ---")
print(standard_out)
print(f"\n--- reasoning model ({REASONING_MODEL}) ---")
print(reasoning_out)

# %%
# Where did they disagree on urgency? That is the whole finding.
def urgency_map(text):
    out = {}
    for line in text.strip().splitlines():
        parts = [p.strip() for p in line.split("|")]
        if len(parts) == 3 and parts[0].isdigit():
            out[int(parts[0])] = parts[2].lower()
    return out

a, b = urgency_map(standard_out), urgency_map(reasoning_out)
diffs = [(n, a[n], b[n]) for n in sorted(set(a) & set(b)) if a[n] != b[n]]
print(f"urgency disagreements: {len(diffs)} of {len(set(a) & set(b))}\n")
for n, x, y in diffs:
    print(f"  msg {n:>2}: standard={x:<7} reasoning={y:<7}  {complaints[n - 1][:60]}...")
print("\n✓ Read the disagreements. Which model would you trust to route a queue,")
print("  and what would it cost you to be wrong in each direction?")

# %% [markdown]
# ## Stretch (not timed)
#
# The workbook page ends at rung 4. Everything below is optional — the other
# three patterns from the a2 lab, kept because they are useful, and the Prompt
# Card that Lab 4.2 builds on.

# %% [markdown]
# ### Stretch A — A harder single-model question
#
# Give the model the hardest item you have — a multi-constraint question on the
# memo — with **no** chain-of-thought instruction. Modern reasoning models do the
# work internally; your job is to ask the hard thing clearly.

# %%
HARD_ITEM = (
    "A division wants to use a free public chatbot to draft reply letters that "
    "quote from constituent case files, and to skip review for 'routine' "
    "replies. Under the memo, which specific clauses does this violate, and "
    "what is the smallest change that would make the plan compliant?"
)
CANNED_REASONING = (
    "The plan violates three clauses. Clause 3(b): case-file contents are "
    "nonpublic constituent information and may never enter an unapproved "
    "public tool. Clause 3(a): 'routine' is not an exception — every "
    "AI-assisted product bound for a constituent must be reviewed and "
    "approved by a responsible employee. Clause 3(c): internal information "
    "may only be handled by the enterprise assistant under the Department's "
    "data-protection agreement. The smallest compliant change: keep the "
    "drafting workflow but run it on the approved enterprise assistant and "
    "keep human review for every letter."
)

reasoning = None
# YOUR CODE: chat() with HARD_ITEM + the memo text. Pass offline=CANNED_REASONING.

if reasoning is None:
    reasoning = CANNED_REASONING
    print("(canned reasoning output — write your call above to run your own)\n")
print(reasoning)

# %% [markdown]
# ### Stretch B — Iterate on your weakest output
#
# Look at your scorecard. Take the **worst-scoring** output so
# far and improve it in three rounds, keeping each version. Write what you
# changed each round.

# %%
iterations = []
# YOUR CODE: three rounds. Append (prompt, output) tuples to `iterations`.
# Change ONE thing per round (specificity? format constraint? audience?) so
# you can see what actually moved the score.

if not iterations:
    print("(no iterations yet — this step is yours; see the solution copy "
          "for a worked example)")

# %% [markdown]
# #### Iteration log (write here)
#
# - Round 1 — changed: / score before → after:
# - Round 2 — changed: / score before → after:
# - Round 3 — changed: / score before → after:

# %% [markdown]
# ### Stretch C — Role: a FOIA officer on the acceptable-use policy
#
# "You are a FOIA officer..." — set a role, then apply it to the
# acceptable-use policy.

# %%
CANNED_ROLE = (
    "From a FOIA officer's desk, three points in this policy matter most. "
    "First, AI-drafted correspondence about agency business is a federal "
    "record, so it enters the retention system and is potentially FOIA-"
    "releasable — drafts are not invisible. Second, the PII prohibition "
    "aligns with Exemption 6 practice: what we would redact before release "
    "must never leave the boundary in the first place. Third, the "
    "human-review clause assigns accountability the way FOIA assigns it — "
    "to a named official, not a tool."
)

role_out = None
# YOUR CODE: system message "You are a FOIA officer reviewing a draft
# acceptable-use policy..." + the policy text. Pass offline=CANNED_ROLE.

if role_out is None:
    role_out = CANNED_ROLE
    print("(canned role output — write your role prompt above to run your own)\n")
print(role_out)

# %% [markdown]
# ### Stretch D — Structured output: entities as JSON
#
# Extract the memo's key entities into a table a program can
# use. Force JSON and parse it — this is the pattern that feeds downstream
# systems.

# %%
CANNED_ENTITIES = {"entities": [
    {"type": "organization", "name": "Office of the Chief Data Officer", "detail": "issuing office and point of contact"},
    {"type": "date", "name": "March 14, 2026", "detail": "memo date; effective immediately"},
    {"type": "rule", "name": "Human review", "detail": "responsible employee must approve AI-assisted products before release"},
    {"type": "rule", "name": "Data handling", "detail": "only public information in public tools; report exposure within one business day"},
    {"type": "rule", "name": "Approved tools", "detail": "enterprise assistant required for internal information"},
    {"type": "rule", "name": "Recordkeeping", "detail": "AI-assisted correspondence is a federal record"},
]}

entities = None
# YOUR CODE: chat_json() asking for the memo's entities under key "entities",
# each with {type, name, detail}. Pass offline=CANNED_ENTITIES.

if entities is None:
    entities = CANNED_ENTITIES
    print("(canned entities — write your chat_json call above to run your own)\n")
print(pd.DataFrame(entities["entities"]).to_string(index=False))

# %% [markdown]
# ### Stretch E — Grounding: answer only from the policy
#
# Answer **only** from the acceptable-use policy, and require the
# model to quote the sentence it relied on. Grounding is the difference
# between "plausible" and "defensible".

# %%
QUESTION = ("What happens if an employee pastes a constituent's record into "
            "a public chatbot?")
CANNED_GROUNDED = (
    "It is a reportable data spill. The policy states: \"Pasting a "
    "constituent's record into a public chatbot is a reportable data spill.\" "
    "Constituent records are PII — a sensitive/regulated data category — and "
    "may only be used with tools specifically authorized for that category, "
    "which a public chatbot is not."
)

grounded = None
# YOUR CODE: chat() with QUESTION + the policy text; instruct the model to
# answer only from the policy and to quote the supporting sentence.
# Pass offline=CANNED_GROUNDED.

if grounded is None:
    grounded = CANNED_GROUNDED
    print("(canned grounded answer — write your call above to run your own)\n")
print(grounded)

# check the quote really is in the policy (grounding, verified mechanically):
quote = "Pasting a constituent's record into a public chatbot is a reportable data spill."
print("\nquote verified in policy:", quote in policy)

# %% [markdown]
# ### Stretch F — Your Prompt Card (Lab 4.2 builds on this)
#
# Copy your best prompt from each pattern into the markdown cell below. This
# is the seed of the template library you build in Lab 4.2.
#
# #### My Prompt Card (write here)
#
# - Zero-shot:
# - Few-shot:
# - Reasoning:
# - Iteration (final version):
# - Role:
# - Structured output:
# - Grounding:

# %% [markdown]
# ## Deliverable
#
# One **before/after prompt pair** with its two rubric scores, and a one-line
# note on **which rung of the ladder bought the most quality**.
#
# (Keep the full `scorecard` too — it is the evidence behind that one line.)

# %% [markdown]
# ## Reflection
# 1. Where did the model sound confident but get a fact wrong? How did you catch
#    it?
# 2. When would you stop iterating and switch approach (RAG? a different tool)?

# %% [markdown]
# ## Debrief (instructor-led)
#
# - **Compare Prompt Cards.** Which pattern showed the most divergence
#   between students' prompts — and what does that tell you about the
#   pattern?
# - **Live vs canned.** If anyone ran offline, re-run one cell with the key
#   present and compare: did the rubric score change?
# - **Bridge to Lab 4.2.** Which of your seven prompts is the best candidate
#   to templatize, and which slots would it need?

# %% [markdown]
# ## Troubleshooting
#
# - **`FileNotFoundError: data/gov_memo.txt`** — the kernel's working
#   directory is not `labs/`. Restart the kernel from the `labs/` folder and
#   Run All.
# - **`ModuleNotFoundError: lab_common`** — same cause: the notebook must run
#   with `labs/` as its working directory.
# - **Every AI cell prints "(canned ...)"** — no API key is visible. On the
#   classroom VM the key is injected; on your own machine it comes from the
#   course `.env`. The lab is fully usable either way.
# - **API errors (rate limit, authentication)** — re-run the cell once; if it
#   persists, the canned path keeps you moving. Tell your instructor.
# - **`quote verified in policy: False`** — the quoted sentence is not in the
#   policy. That is the grounding lesson: require the quote, then check it
#   mechanically before you trust the answer.
