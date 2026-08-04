#!/usr/bin/env python3
"""build_notes_ch03.py — delivery-notes rewrite for 1258-Ch03-Desktop-GenAI.pptx (58 slides).

Idempotent: restores the deck from decks/_bak7/, rebuilds every note as
SAY/ASK hook + KEY POINT + time cue + TRANSITION, and re-appends preserved
markers ([flex], Source lines, spine rungs, author/IG flags) extracted
verbatim from the backup notes. Slide text/layouts/counts are untouched.

Run: ../../.venv-courseware/bin/python tools/build_notes_ch03.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from notes_common import apply_notes, verify

TAG = "Ch03-Desktop-GenAI"
COUNT = 58

FLEX_CORE = {
    16: "the 2025-26 AI Prioritization Initiative fast-tracked assistants — months, not years (closed to new entrants)",
    17: "GSA's $1 OneGov deals centralize acquisition — watch GSA announcements; your agency decides what you get",
    19: "M365 Copilot stays inside your government tenant — same product name, different feature set and posture per cloud",
    22: "models are fluent and confident even when wrong — verify names, dates, numbers, and citations",
    26: "summaries drop caveats and dissent — quote source lines; read the original for decision-relevant work",
    40: "opt-outs and retention settings mitigate — they never authorize nonpublic data in a consumer tool",
    46: "everyday productivity use is lightly governed; decision-shaping use is heavily governed — know the line",
    49: "the spill pathway is routine content — emails, meeting notes, constituent data — not malice",
    52: "the four assistants are a snapshot — the FedRAMP lookup plus your AUP are the durable evaluation tools",
}

NOTES = {
1: """SAY: "This is the chapter about the tools already on your desktop — the four assistants your coworkers opened this morning."
KEY POINT: Chapter 3 covers the four desktop assistants and their government editions, five everyday work patterns, tiers and who trains on your prompts, and the data rule with shadow-AI awareness — closing with the Lab 3.1 task relay.
FLEX VALVE: this chapter closes Day 1 — if we fall behind, the [flex] slides are the valve; I skip them first.
(~2 min)
TRANSITION: The objectives.""",
2: """ASK: "Be honest — who used a chat assistant this week? This chapter makes that habit effective and safe."
KEY POINT: You will recognize the four assistants and their government editions, choose by FedRAMP authorization status, apply GenAI to five work patterns, apply the data rule and your AUP to every prompt, and spot shadow-AI risk.
(~2 min)
TRANSITION: The route.""",
3: """SAY: "Four assistants, five patterns, one data rule — that's the whole chapter."
KEY POINT: Contents: the four assistants staff use daily; editions and the FedRAMP scoreboard; five everyday patterns with worked examples; free, paid, and enterprise tiers; the data rule, your AUP, and shadow AI — plus Demo 3.1, DO NOWs 3.A-3.D, and Lab 3.1.
(~2 min)
TRANSITION: Why this chapter exists at all.""",
4: """SAY: "Most of your coworkers will never open a Jupyter notebook — but they opened a chat assistant today. That's what gov staff use daily."
KEY POINT: Staff meet AI through chat assistants, not code; they use them daily for research, writing, and summarizing — the productivity and the risk both live here, and teaching the tool they actually use is what makes this course stick.
(~2 min)
TRANSITION: The activity lineup.""",
5: """SAY: "A demo, four short DO NOWs, and a 30-minute task relay — 73 minutes of practice on the tools you actually have."
KEY POINT: Demo 3.1 runs four assistants on one task; DO NOWs cover summarizing for a named reader, text-to-diagram, paste-decisions, and a shadow-AI inventory ([flex]); Lab 3.1 is the relay — full instructions in the Lab Manual.
(~2 min — walk the list; these times are the chapter's budget)
TRANSITION: First, the numbers that prove this is where staff meet AI.""",
6: """ASK: "What share of federal GenAI use is everyday mission-enabling work — writing, search, summarization? Sixty-one percent."
KEY POINT: GAO toplines: use cases nearly doubled (571 to 1,110), GenAI up about 9x (32 to 282), and 61% of 2024 GenAI use cases are mission-enabling — exactly this chapter's five patterns. Your coworkers are already using these tools.
(~2 min)
TRANSITION: Meet the four.""",
7: """SAY: "ChatGPT, Copilot, Gemini, Claude — the right one is usually the one your agency licensed."
KEY POINT: Four capable assistants: ChatGPT the most widely known, Copilot embedded in Word/Excel/Outlook/Teams, Gemini in Workspace and the browser, Claude strong at writing and analysis; as of mid-2026 all four have U.S. government offerings.
(~2 min)
TRANSITION: One at a time — ChatGPT first.""",
8: """ASK: "Who here has used ChatGPT? Keep your hand up if you know which tier is FedRAMP certified."
KEY POINT: ChatGPT: strong at drafting, brainstorming, summarizing, and conversational research; frontier models with context windows that grow by tier; the Enterprise/API service is FedRAMP 20x Moderate certified, and ChatGPT Gov lets agencies self-host inside their own Azure Government tenant — certification covers the enterprise service, not the consumer app.
(~2 min)
TRANSITION: The one that lives inside Word and Outlook.""",
9: """SAY: "Copilot's pitch: never leave Word, Excel, Outlook, or Teams — the assistant comes to your documents instead of your documents going to a chatbot."
KEY POINT: M365 Copilot grounds answers in your work content — documents, email, meetings — and runs inside your government tenant (GCC, GCC High, DoD clouds); new features arrive later in government clouds than in commercial.
(~2 min)
TRANSITION: Google's entry.""",
10: """SAY: "If your agency runs on Google Workspace, Gemini is the natural front door — and its government edition carries FedRAMP High."
KEY POINT: Gemini handles text, images, and files in one conversation inside Docs, Sheets, and Gmail; the product name to remember is 'Gemini for Government' — FedRAMP High-authorized — and the front door to Google's accredited public-sector cloud.
(~2 min)
TRANSITION: The fourth: Claude.""",
11: """ASK: "What would you do with an assistant that reads a million tokens — a whole IG report in one prompt?"
KEY POINT: Claude: strong writing, analysis, and careful long-document work with up to 1M-token context; Claude for Government is FedRAMP High — offered to all three branches for $1 for one year — and approved for DoD IL4/IL5 via Amazon Bedrock in AWS GovCloud. The $1 was a 2025 GSA OneGov agreement — how government buys AI, not a standing price.
(~2 min)
TRANSITION: So which one do you reach for?""",
12: """SAY: "Authorization first, task fit second, brand preference last — that's the whole decision."
KEY POINT: Start with what your agency is licensed and authorized for; match the tool to the task — M365 documents point to Copilot, Workspace to Gemini, long documents to a large-context assistant; drafting and general Q&A: any approved one; free personal accounts are for learning and public data only.
(~2 min)
TRANSITION: The editions behind those authorizations.""",
13: """SAY: "Read this slide as a shopping list your security office already approved — every row is a government edition."
KEY POINT: The government editions: ChatGPT Enterprise/Gov (FedRAMP 20x Moderate), M365 Copilot (GCC/GCC High/DoD), Gemini for Government (FedRAMP High), Claude for Government (FedRAMP High; $1 for a year via GSA OneGov). The edition, not the brand, determines what data you may use.
(~2 min)
TRANSITION: The scoreboard, date-stamped.""",
14: """ASK: "Which of these five services could your agency use tomorrow? The answer has a date stamp — this table will drift."
KEY POINT: The mid-2026 scoreboard: ChatGPT Enterprise + API (FedRAMP 20x Moderate), M365 Copilot (GCC/GCC High/DoD, IL5 in DoD), Gemini for Government (FedRAMP High), Claude for Government (FedRAMP High; IL4/IL5 via Bedrock GovCloud), Perplexity Enterprise Pro for Government (certified early 2026) — verify on the FedRAMP Marketplace before relying on it.
(~2 min)
TRANSITION: So let's learn the lookup — the durable skill.""",
15: """SAY: "Memorize the lookup, not the table: fedramp.gov, Marketplace, exact service name."
KEY POINT: Search the exact service name; editions differ — one tier's authorization may not cover another; confirm the impact level (Moderate vs. High matters for your data); match against your agency's approved-tools list; when in doubt, ask your security office. Instructor: demo the live Marketplace — listings are JS-rendered and change often.
(~2 min)
TRANSITION: Why did this suddenly move so fast? FedRAMP 20x.""",
16: """SAY: "After years of slow authorizations, three assistants got certified in months — here's the mechanism."
KEY POINT: The AI Prioritization Initiative (Aug 2025-Apr 2026, closed to new entrants) fast-tracked conversational AI; FedRAMP 20x uses Key Security Indicators and automated continuous validation; criteria included enterprise controls (SSO, SCIM, RBAC), GSA MAS availability, agency demand — and customer data must not train models outside the customer environment.
(~2 min if taught — skip if the class is non-technical or time is short)
TRANSITION: The buying side of speed: OneGov.""",
17: """ASK: "What does an enterprise AI license cost an agency? In August 2025, GSA got the price down to a dollar."
KEY POINT: The OneGov Anthropic deal: Claude for Enterprise + Government at $1 per agency for a year, covering all three branches via GSA MAS, explicitly supporting OMB M-25-21/M-25-22 adoption — for users, the point is to watch GSA announcements; when your agency signs on, an enterprise edition with real data protections may appear at no cost to your office.
(~2 min if taught)
TRANSITION: What authorization means for where your data goes.""",
18: """SAY: "FedRAMP authorization is not paperwork — it's the boundary that decides whether your data may go in."
KEY POINT: Public/free assistants are generally NOT authorized for nonpublic data; enterprise government editions run inside authorized boundaries (Azure Gov, AWS GovCloud, GCP); know your agency's authorized tool list before pasting anything sensitive — and verify on the Marketplace, because the list keeps moving (GSA, NASA, and VA told GAO that FedRAMP timelines delay acquisition).
(~2 min)
TRANSITION: For M365 shops: what 'inside the boundary' means.""",
19: """SAY: "Same product name, three different clouds — GCC, GCC High, DoD — and the online demo you saw may not match your tenant yet."
KEY POINT: M365 Copilot runs entirely inside your agency's government cloud tenant: prompts, responses, and generated content stay in the government cloud; GCC aligns to FedRAMP Moderate, GCC High targets CUI/ITAR/FedRAMP High, DoD meets IL5; expect feature lag versus commercial.
(~2 min if taught — depth for M365 shops)
TRANSITION: Enough procurement — let's use the tools. Pattern one.""",
20: """ASK: "New acronym in a meeting this morning — how fast could an assistant get you oriented? And when should you not believe it?"
KEY POINT: Research pattern: ask for plain-language explanations of unfamiliar topics, policies, or acronyms; ask follow-ups to go deeper; always verify facts against an authoritative source — the model can be confidently wrong; great for getting oriented fast, not a citation of record.
(~2 min)
TRANSITION: Watch it on a real task.""",
21: """SAY: "You just inherited a public grants program you know nothing about — fifteen minutes from now, you're oriented."
KEY POINT: Demo flow on a public program: 'Explain this program — purpose, who it serves, key offices — in plain language'; follow up with 'What acronyms will I see in its documents?'; then verify every fact against the agency's official .gov pages — public program information only, never internal case data.
(~3 min — run it live; show one follow-up going deeper and one confident answer that needs verification)
TRANSITION: That last habit deserves its own slide.""",
22: """SAY: "The most dangerous sentence an assistant writes is the confident, plausible, wrong one."
KEY POINT: Hallucination is an institutional concern — five agencies told GAO that bias and hallucination are a top GenAI challenge; treat output as a smart colleague's first answer, not a citation of record; check names, dates, numbers, and citations against authoritative sources.
(~1 min if taught — fold into Pattern 1 if time is tight)
TRANSITION: Pattern two: the one everyone tries first — summarization.""",
23: """ASK: "Who has pasted a long document into a chatbot and asked for bullets? What did you check before forwarding them?"
KEY POINT: Summarization pattern: long public reports, meeting notes, email threads — ask for the summary in a specific form (5 bullets, an executive paragraph, action items); public documents only unless you're in an approved enterprise tool; review that nothing important was dropped or distorted.
(~2 min)
TRANSITION: Why whole reports now fit in one prompt.""",
24: """SAY: "~12 pages free, ~250 pages pro, a whole IG report in Claude — the context window is the quiet spec that changed summarization."
KEY POINT: Context window = how much the model can consider at once: ChatGPT about 27K tokens (Free) up to 400K (Pro reasoning models); Claude's current models up to 1M tokens; figures change often — check the vendor's current tier table. Verbal caveat: system instructions and memory consume part of the window.
(~2 min)
TRANSITION: Put it to work on a public report.""",
25: """SAY: "Take a published inspector-general audit — public by design — and compress it twice: five bullets, then three sentences for the branch chief."
KEY POINT: Demo flow with a large-context assistant: 'Summarize in 5 bullets: findings, recommendations, affected programs'; then 'Draft a 3-sentence executive paragraph for my branch chief'; spot-check the bullets against the report's actual findings — watch for dropped caveats.
(~3 min — run live; demonstrates requested-format prompting plus the verification habit)
TRANSITION: The failure mode to watch for.""",
26: """ASK: "What vanishes first when a 40-page report becomes five bullets? The caveats."
KEY POINT: Summaries compress — caveats, dissent, and uncertainty drop out; NCDIT warns that relying on summaries may mischaracterize the original; ask the model to quote the source lines behind each claim — a self-check technique to take home — and read the original sections for anything decision-relevant.
(~2 min if taught — fold into the summarization pattern if time is tight)
TRANSITION: Pattern three: drafting.""",
27: """SAY: "The model writes the first draft; you own the final word — that division of labor is the whole pattern."
KEY POINT: Draft routine correspondence, then edit; rewrite for tone, reading level, or length ('rewrite for a 6th-grade reading level'); you remain accountable for accuracy and appropriateness — and AI-assisted correspondence that documents agency business is a federal record.
(~2 min)
TRANSITION: Watch the two-step on a routine email.""",
28: """SAY: "A routine status email about a public deadline: role, audience, purpose, tone, length — plus your bullet outline."
KEY POINT: Demo the two-step: draft with role/audience/purpose/tone/length and a bullet outline, then 'rewrite for a general audience; keep it under 150 words'; edit names, dates, and commitments before sending; if it documents agency business, it is a federal record — retain it properly.
(~3 min — run live; emphasize the human edit pass: first draft, never the final word)
TRANSITION: Records and disclosure — the rules behind that last bullet.""",
29: """ASK: "When does a chatbot draft become a federal record? The moment it documents agency business."
KEY POINT: NCDIT's rule lands hard: treat anything entered into a public GenAI tool as released to the public; disclose AI-drafted content where your AUP requires it — name the system, model, and version; use official accounts so records are retained, not personal logins.
(~2 min)
TRANSITION: Pattern four: pictures from words.""",
30: """SAY: "Describe a process in a paragraph, get a flowchart back — text-to-diagram is the fastest pattern nobody expects."
KEY POINT: Generate process flows and org charts by describing them in words; ask for Mermaid or a described diagram you can paste into your tools — the fast way to turn a paragraph of process into a picture; covered hands-on in Lab 3.1.
(~2 min)
TRANSITION: Watch one render.""",
31: """SAY: "Take a public application process, ask for a Mermaid flowchart, paste, render — then interrogate the logic."
KEY POINT: Demo: 'Turn this paragraph into a Mermaid flowchart'; render it in your diagram tool; review the logic — models add plausible-sounding steps that don't exist; ask for a layout change to show iteration. Mermaid goes deeper in Chapter 4.
(~3 min — show one render, then one deliberate iteration)
TRANSITION: Beyond text: files and images.""",
32: """ASK: "Is uploading a PDF safer than pasting its text? A spill is a spill either way."
KEY POINT: Assistants now read attached PDFs, slides, spreadsheets, and images — ask questions about a public PDF or the story behind a chart; the same data rule applies to attachments, and enterprise tiers handle files under the same no-training terms.
(~2 min — demo with a public PDF, e.g., a published report)
TRANSITION: Pattern five: code and troubleshooting.""",
33: """SAY: "You don't need to be a developer for this one — an Excel formula that won't parse is reason enough."
KEY POINT: Code help: explain an error message and suggest a fix; explain what code or a formula does; write a small script; verify and test anything before running it on real systems — useful even for non-developers doing light automation.
(~2 min)
TRANSITION: The worked example — then the rule that governs it.""",
34: """SAY: "Paste the exact error text, ask for the two most likely causes, get the fix step by step — and test on a copy, never production."
KEY POINT: Demo on a real error message (works for Excel formulas and desktop tools, not just Python): have the assistant explain any code it gives you; test on a copy or sample data first; strip hostnames, usernames, and paths — error text leaks infrastructure details. The sanitizing habit is the part to drill.
(~2 min)
TRANSITION: What real AUPs say about code.""",
35: """ASK: "Which needs security-office approval first: pasting citizen data, or pasting code? In North Carolina, both."
KEY POINT: NCDIT requires written security-office approval before entering code into public GenAI — code reveals internal systems, logic, and vulnerabilities, and AI-generated code can introduce new ones; check your agency's rule before pasting any code, even snippets.
(~2 min)
TRANSITION: Now the tier system behind all these rules.""",
36: """SAY: "Free, paid, enterprise — the tier controls what data you may enter, not how smart the model is."
KEY POINT: Free: fine for learning and public data — consumer terms, no data agreement. Paid individual: higher limits, still consumer terms — may train unless you opt out. Enterprise/Government: admin control, no training by default, FedRAMP posture.
(~2 min)
TRANSITION: What paying actually buys.""",
37: """SAY: "A paid seat buys you limits and speed — it does not buy you a data agreement."
KEY POINT: Individual plans keep consumer terms (ChatGPT Free ~27K tokens vs. Pro up to 400K); Business/Enterprise adds SSO, SCIM, RBAC, SOC 2, audit logs, and data residency — and your data is not used for training by default; demo the live pricing page rather than quoting figures.
(~2 min)
TRANSITION: The matrix that surprises everyone.""",
38: """ASK: "True or false: 'Claude never trains on your data.' It was true once — it isn't for consumer tiers anymore."
KEY POINT: ChatGPT Free/Go/Plus/Pro may train unless you opt out; Claude Free/Pro/Max may train if you allow it — policy changed Sept-Oct 2025; paid individual does not mean private — consumer terms still apply; enterprise and government tiers: no training by default.
(~2 min)
TRANSITION: All four vendors, one matrix.""",
39: """SAY: "Walk this matrix row by row — then forget the rows and keep the skill: find each vendor's current data-use policy page."
KEY POINT: Mid-2026 matrix: ChatGPT consumer trains unless you opt out, Business/Enterprise never by default; M365 Copilot content stays inside your government tenant; Gemini Government edition carries FedRAMP High protections — consumer terms differ, check them; Claude consumer trains if allowed (5-year retention), Work/Government tiers exempt.
(~2 min)
TRANSITION: The settings that mitigate — and their limit.""",
40: """ASK: "What does opting out actually buy you? Thirty days of retention instead of five years — and still not permission."
KEY POINT: Opted-in Claude consumer chats: retained up to 5 years; opted out: 30 days; NCDIT advises opting out and disabling chat history for higher-risk uses; enterprise tiers let administrators control retention centrally — settings are not authorization: an opt-out is a mitigation, never permission to paste nonpublic data.
(~2 min if taught)
TRANSITION: Which brings us to the rule itself.""",
41: """SAY: "The one rule this course repeats at every lab — say it with me before the slide finishes."
KEY POINT: Never paste nonpublic information into a tool not approved for it: no PII, procurement-sensitive, law-enforcement, or classified data in public assistants; public data is fine in any approved tool; a constituent record in a public chatbot is a reportable data spill. Anchors: GSA and DHS limit commercial GenAI to publicly available information; VA prohibits web-based public GenAI with sensitive data.
(~2 min)
TRANSITION: This isn't course caution — it's documented agency practice.""",
42: """SAY: "All twelve agencies GAO reviewed restrict GenAI use in some capacity — and all twelve train staff on protecting information."
KEY POINT: GSA and DHS limit commercial GenAI use to publicly available information only; VA prohibits web-based public GenAI with sensitive VA data — the data rule is documented agency practice, not this course being cautious. If a student says 'my agency has no rule,' the M-25-21 mandate two slides on answers it.
(~2 min)
TRANSITION: The class version of the same rule.""",
43: """SAY: "Every lab this week runs on public or synthetic data — no exceptions — and here's the heuristic that makes it easy."
KEY POINT: Good public sources: data.gov, published reports, Federal Register notices; synthetic means invented data that looks real but describes no real person or case; the test: if you'd hesitate to post it on your agency's public website, don't paste it. State it once, repeat it at every lab.
(~2 min)
TRANSITION: The policy engine behind all agency AUPs.""",
44: """ASK: "Does your agency have a GenAI acceptable-use policy? OMB says it must — the deadline was about December 2025."
KEY POINT: OMB M-25-21 (Apr 2025) replaced M-24-10: each agency maintains a generative-AI AUP (within 270 days), designates a Chief AI Officer, and inventories use cases annually; companion M-25-22 governs acquisition — including no vendor training on federal data. Takeaway: your agency has a GenAI policy — find it and read it.
(~2 min)
TRANSITION: What a real AUP looks like, clause by clause.""",
45: """SAY: "North Carolina published theirs — concrete, public, and it maps one-to-one onto this chapter's rules."
KEY POINT: The model clauses: never enter PII or confidential data into public GenAI tools; written security-office approval before entering code; independently fact-check all output; disclose and cite AI-drafted content (system, model, version); use official accounts and re-assess approved tools at least annually. Students can compare it against their own agency's AUP in the micro-exercise.
(~2 min)
TRANSITION: Where the governance line sits.""",
46: """SAY: "Drafting an email and deciding a benefit are both 'using AI' — the law treats them very differently."
KEY POINT: M-25-21's high-impact AI — output driving decisions with legal or material effects on rights or safety — triggers mandatory risk-management practices; desktop drafting and summarizing usually aren't high-impact, but when your use case moves toward decisions about people, escalate to your CAIO.
(~2 min if taught — one message, then bridge to Chapter 5)
TRANSITION: The risk that walks in on personal phones: shadow AI.""",
47: """ASK: "Quick show of hands — who knows someone using an AI tool IT hasn't approved? That's shadow AI, and it's usually well-intentioned."
KEY POINT: Shadow AI moves agency data into unmanaged services; the fix is not banning AI — it is providing approved tools and clear rules; report tools you wish you had; don't route around the policy. Frame constructively.
(~2 min)
TRANSITION: The survey numbers behind the concern.""",
48: """SAY: "81% use unapproved tools; 45% work around the blocks — which is why 'just ban it' fails."
KEY POINT: Present explicitly as vendor-commissioned surveys, not government statistics: UpGuard 2026 — 81% of employees use unapproved AI tools, 45% find workarounds; PagerDuty 2026 — 88% have shared work information with public AI tools, 66% have used unauthorized tools. No equivalent .gov dataset exists, but the pattern is consistent.
(~2 min)
TRANSITION: What people actually paste — the spill pathway.""",
49: """ASK: "What do people actually paste into public AI tools? Emails, meeting notes — and a third admit to customer data."
KEY POINT: The spill pathway is routine content: 43% shared emails, 40% meeting notes, 34% customer data — in a government room, map 'customer data' to constituent data, because that is the reportable spill; 89% used AI personally before work; 81% believe leadership plays by different rules — a trust gap to close. (PagerDuty survey of 1,250 office professionals, Jun 2026 — present as a survey.)
(~2 min if taught)
TRANSITION: Your turn: find your own agency's policy.""",
50: """SAY: "Three minutes, right now: search for your agency's generative-AI acceptable-use policy."
KEY POINT: M-25-21 required every agency to have one by ~December 2025; GAO found 11 of 12 major agencies already had GenAI use guidelines; look for approved tools, allowed data classes, and disclosure rules — bring what you find to the Lab 3.1 debrief.
(3-5 min exercise — policies are public, personal devices fine; debrief who found one, who couldn't, and what the approved-tools list says)
TRANSITION: One more judgment skill before the lab.""",
51: """ASK: "When is the right answer NOT to use an assistant at all?"
KEY POINT: Don't use a desktop assistant when the data is sensitive and the tool isn't approved for it, when you can't verify the output and the stakes are high, or when a deterministic tool — a form, a calculator, a database query — is the right answer. Good judgment about when to reach for AI is a professional skill.
(~2 min)
TRANSITION: The landscape won't sit still — one horizon slide.""",
52: """SAY: "The four assistants are a snapshot — the landscape won't sit still, and your evaluation tools shouldn't either."
KEY POINT: Perplexity Enterprise Pro for Government also earned FedRAMP certification (early 2026); GenAI.mil is training department personnel; new services will keep arriving — judge each by the same tests: authorization, data terms, your AUP. The lookup skill outlasts any brand list.
(~2 min if taught)
TRANSITION: Time for the relay.""",
53: """ASK: "Four timed tasks — summarize, diagram, troubleshoot, draft — which one will your assistant ace?"
KEY POINT: Lab 3.1 Desktop GenAI Task Relay: work in your agency-approved or class-designated assistant; public/synthetic inputs only; score each output with the 3-point rubric.
(30 min lab including debrief — keep tasks timeboxed; debrief where tools differed, what your AUP allows, and free-vs-paid friction observed)
TRANSITION: Tasks one and two.""",
54: """SAY: "Task one compresses a public document into five bullets; task two turns a public process into a Mermaid diagram."
KEY POINT: Work in your agency-approved assistant (or the class-designated one); public/synthetic inputs only — the class rule applies to every task; timeboxed: move on when time is called — partial output is fine.
(~2 min to brief — tasks run inside the 30-min lab)
TRANSITION: Tasks three and four.""",
55: """ASK: "Troubleshoot, then draft — which of the four tasks will your assistant handle worst? Note it; that's debrief material."
KEY POINT: Task 3: explain the provided error message and propose a fix. Task 4: write a short routine email, then rewrite it for tone and length. Score each output with the 3-point rubric on the next slide.
(~2 min to brief)
TRANSITION: The rubric you'll score with.""",
56: """SAY: "Accurate, fit, safe — three dimensions, thirty seconds per task, and suddenly 'the AI did well' means something."
KEY POINT: Score each task 0-2 per dimension: accurate (facts check out against the source, nothing invented), fit (matches the requested format, length, audience), safe (no nonpublic data in, no overclaiming out); compare totals across tools on the board.
(~1 min — keep scoring fast; the whiteboard comparison across assistants is the payoff)
TRANSITION: Debrief.""",
57: """SAY: "Same prompt, four assistants, different scores — now we find out why."
KEY POINT: Debrief questions: where did tools differ on the same task; what did your agency's AUP allow that the class rule didn't — or vice versa; what friction did free vs. paid tiers create; which pattern will you use first back at your desk?
(~5 min debrief — whiteboard; the AUP question lands best if the micro-exercise ran earlier)
TRANSITION: The chapter in five lines.""",
58: """ASK: "A week from now, which of these five keeps you out of trouble? Say it with me: never paste nonpublic data into an unapproved tool."
KEY POINT: Four capable assistants — the right one is the authorized one; the edition and tier, not the brand, set your data permissions; consumer tiers may train on your chats, enterprise and gov tiers don't by default; and your agency has a GenAI AUP (OMB M-25-21) — read it and follow it.
(~2 min)
TRANSITION: Day 2 opens with Chapter 4 — prompt engineering, where the P0-P10 spine goes deep. The data rule from this chapter applies everywhere.""",
}

if __name__ == "__main__":
    apply_notes(TAG, COUNT, NOTES, FLEX_CORE)
    verify(TAG, COUNT)
