#!/usr/bin/env python3
"""build_notes_ch00.py — delivery-notes rewrite for 1258-Ch00-Course-Launch.pptx (53 slides).

Idempotent: restores the deck from decks/_bak7/, rebuilds every note as
SAY/ASK hook + KEY POINT + time cue + TRANSITION, and re-appends preserved
markers ([flex], Source lines, spine rungs, author/IG flags) extracted
verbatim from the backup notes. Slide text/layouts/counts are untouched.

Run: ../../.venv-courseware/bin/python tools/build_notes_ch00.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from notes_common import apply_notes, verify

TAG = "Ch00-Course-Launch"
COUNT = 53

FLEX_CORE = {
    9: "how to engage all week — ask questions, do every lab, tie each activity to your job, collect keeper prompts",
    14: "OMB M-25-21 is the governing memo — CAIO, public inventories, high-impact safeguards, required GenAI acceptable-use policy",
    15: "four bookmarks to take home — GSA AI Guide, GSA training tracks, Community of Practice, NIST AI RMF",
    41: "the six Bloom's levels in plain words, mapped to course activities",
    43: "hands-on-first is deliberate — adults learn by solving immediate, real problems using their own experience",
}

NOTES = {
1: """SAY: "Three days from now you'll re-score the prompt you write this morning — and watch the course show up in the difference."
KEY POINT: Welcome. This launch hour: who's in the room, the lab environment, the accounts and the data rule, and the three-day map.
FLEX VALVE: this chapter runs a full morning — if we fall behind, the [flex] slides are the valve; I skip them first.
(~2 min)
TRANSITION: What this launch hour will accomplish — the objectives.""",
2: """ASK: "What would you need to see by Thursday to call these three days a good use of your time?"
KEY POINT: Five outcomes for this hour: a verified running lab, what the course will and won't make of you, the data rule, the course map and prompting spine, and how activities work.
(~2 min)
TRANSITION: The road we take to get there — the chapter contents.""",
3: """SAY: "This hour has one hard deadline: everyone at a green healthcheck before Chapter 1."
KEY POINT: The flow — welcome and expectations, the federal AI snapshot, the lab environment, accounts and the data rule, how we learn, then the activities that pace the morning.
(~2 min)
TRANSITION: First, the activities themselves, with their times.""",
4: """ASK: "What's the one thing that can derail this whole week? A broken lab setup — this lineup is how we prevent it."
KEY POINT: One demo, four DO NOWs, one lab — 65 minutes of the morning is hands-on; full instructions for everything are in the Lab Manual.
(~2 min — walk the list; these times are the morning's budget)
TRANSITION: Before any of that — who this course is actually for.""",
5: """SAY: "Say it plainly: this course is for users of AI, not builders of models — that is what changed in this revision."
KEY POINT: You work in government IT and use — or will use — AI tools; no programming background assumed; every activity uses real government tasks and public or synthetic data.
(~2 min)
TRANSITION: Let's meet the users — introductions.""",
6: """ASK: "Name, agency, role — and one task you wish AI could help with. Who wants to go first?"
KEY POINT: Two minutes per row; capture every wish-list task on the whiteboard — it becomes raw material for the Day-3 90-day-roadmap discussion.
(~10 min for the room — keep it moving; instructor scribes the wish list)
TRANSITION: With the room mapped, the expectations contract.""",
7: """SAY: "Here is the promise half of the contract — read it as four commitments."
KEY POINT: What the course will do: build practical skill with the assistants agencies actually use, teach prompting and output-checking, show real agency deployments, and put you through hands-on labs to a capstone build.
(~2 min)
TRANSITION: The other half — what it won't do.""",
8: """ASK: "Who's quietly worried this will be too technical — or not technical enough? This slide answers both."
KEY POINT: It won't make you a data scientist or ML engineer, won't train models from scratch, isn't legal/procurement/policy certification, and doesn't replace your agency's own acceptable-use training — deep-dive appetites get the appendices and next-step courses.
(~2 min)
TRANSITION: Given that contract, how to get the most out of the three days.""",
9: """SAY: "Three days fly — these four habits are how the value survives the flight home."
KEY POINT: Ask questions as they come, try every lab (fallback paths mean no one stays stuck), connect each activity to a real task from your job, and collect keeper prompts — your take-home toolkit.
(~1 min if taught)
TRANSITION: Now the context for all of it: federal AI today, in numbers.""",
10: """SAY: "571 to 1,110 — reported federal AI use cases nearly doubled in one year, and these are audited GAO numbers, not vendor hype."
KEY POINT: Growth spans mission work and internal operations, and generative-AI cases rose about ninefold in the same period; your agency publishes its own use-case inventory every year — look it up this week.
(~2 min)
TRANSITION: The generative slice of that growth is the steeper story.""",
11: """ASK: "Ninefold growth in a single year — where do you think agencies are actually using generative AI?"
KEY POINT: 32 to 282 GenAI use cases; the gains are communications, information access, and program tracking — and 10 of 12 selected agencies told GAO existing policy can present obstacles, which sets up the data-rule slides later this hour.
(~2 min)
TRANSITION: National numbers — now wins you could recognize in your own agency.""",
12: """SAY: "Critical-minerals analysis cut from years to weeks — that's USGS, running in production, documented in a public strategy."
KEY POINT: Interior's public AI strategy shows running systems: USGS minerals work in weeks, wildfire-intelligence automation saving 200+ expert-hours a year, on FedRAMP-authorized cloud paired with on-prem/HPC for sensitive workloads.
(~2 min)
TRANSITION: The operations side of the same strategy is where the hours add up.""",
13: """ASK: "What would your office do with 7,000 labor-days back?"
KEY POINT: Grants review in 4 hours instead of 500+; a Park Service tool estimated to save 7,000 labor-days a year — draw the lesson explicitly: frontline staff with approved tools, not moonshots, drove the ROI. That pattern is what this course trains you to repeat.
(~2 min)
TRANSITION: What is the policy machinery behind 'approved tools'? One slide.""",
14: """SAY: "When someone asks 'what actually requires us to do this?' — the answer is OMB M-25-21, April 2025."
KEY POINT: M-25-21 replaced M-24-10 (M-25-22 covers acquisition): every agency has a Chief AI Officer and governance structure, publishes strategies and annual inventories, safeguards high-impact AI — decisions affecting rights or safety — and must have a generative-AI acceptable-use policy.
(~2 min if taught)
TRANSITION: And nobody has to figure this out alone — the support ecosystem.""",
15: """ASK: "Where would you look on Monday for the federal government's own AI playbook?"
KEY POINT: Four bookmarks to take home: the GSA AI Guide for Government, GSA's government-wide training tracks, the cross-agency Community of Practice, and the NIST AI Risk Management Framework.
(~1 min if taught)
TRANSITION: Now the course itself — the objectives we'll hold ourselves to.""",
16: """SAY: "Read these as commitments: by Thursday, each one is something you'll have done, not just heard about."
KEY POINT: Five course-level objectives — AI foundations, risk management, operational excellence, data and reporting mastery, hands-on proficiency — and each maps to a Bloom's level.
(~2 min)
TRANSITION: That mapping, made explicit.""",
17: """ASK: "Which matters more to your agency — that you understand AI, or that you can use it? This course refuses to choose."
KEY POINT: Foundations and applications target Understand; labs move you to Apply and Analyze; risk and operations work builds Analyze and Evaluate; the capstone agent build reaches Create.
(~2 min)
TRANSITION: Where those objectives live — the full course contents.""",
18: """SAY: "Skim this map now; by Wednesday evening you'll have a working opinion about every row on it."
KEY POINT: Chapters 0-9 across three days — foundations, applications, desktop GenAI, prompting, security, data, building, operations, roadmap — plus four appendices for depth.
(~2 min)
TRANSITION: The appendices deserve ten seconds of their own.""",
19: """ASK: "Who here wants the deeper technical dive? The appendices are yours."
KEY POINT: Appendices A-D: the ML life cycle, challenges and ethics, the building blocks of generative AI, and classic ML with data engineering — depth material beyond the core three days.
(~1 min)
TRANSITION: Before the map, the conventions that make the week readable.""",
20: """SAY: "One numbering system runs the whole week: DO NOWs warm up, labs go deep, [flex] means your instructor decides."
KEY POINT: Labs are numbered by chapter — Lab 4.1 is Chapter 4's first lab, and notebook filenames match (lab_4.1); exercises are shorter; items marked [flex] are taught when time allows.
(~2 min)
TRANSITION: Now the whole three days on one slide.""",
21: """ASK: "Looking at this map — which day holds the most for your job?"
KEY POINT: Day 1: foundations, applications, desktop GenAI. Day 2: prompt engineering, security, data. Day 3: building with LLMs, operations, your roadmap — hands-on labs every day, capstone closes Day 3.
(~2 min)
TRANSITION: One thread runs through all of it — the prompting spine.""",
22: """SAY: "You'll write a prompt before lunch today that we score again on Thursday — the difference is the course, made visible."
KEY POINT: P0 to P10: named rungs inside activities you already do, one rubric all week — accuracy, completeness, format, tone — and by Day 3 PM you re-score your own Day-1 prompt.
(~2 min)
TRANSITION: Where those keeper prompts live — your Prompt Card.""",
23: """ASK: "What's the one thing you'll actually take back to your desk on Monday? In this course, it's a card."
KEY POINT: Each spine rung contributes one keeper prompt; by Day 3 you hold roughly ten field-tested prompts; the card lives in your workbook — same rubric, same card, all week.
(~2 min)
TRANSITION: Time to make it real — your lab environment.""",
24: """SAY: "No installs, no admin rights, no tickets to your IT shop — your lab runs in a browser tab."
KEY POINT: Labs run on a CloudShare VM reached through the browser; use the in-browser Viewer only — do NOT click the RDP button; the next slides get everyone in and running.
(~2 min — circulate and confirm everyone is in before proceeding)
TRANSITION: Your first DO NOW starts now.""",
25: """ASK: "Ready to see your lab? Fifteen minutes from now, everyone in this room is at a green healthcheck."
KEY POINT: Three steps: launch the VM and open the in-browser Viewer; reach JupyterLab and open lab_0.1_healthcheck.ipynb; Run All Cells and confirm the green PASS checks. While VMs boot, you write your first prompt (P0).
(15 min activity — instructor circulates constantly; do not start Chapter 1 until the room is green)
TRANSITION: The exact path in, step by step.""",
26: """SAY: "Four steps between you and a running lab: Learning Tree account, Launch Lab, in-browser Viewer — and Firefox opens the lab for you."
KEY POINT: Sign in to My Learning Tree, open the course page, click Launch Lab, use the in-browser Viewer; if Firefox doesn't open JupyterLab, double-click 'Start Labs' on the desktop (password, if asked: pw).
(~1 min — show it, then let them do it)
TRANSITION: While machines boot, we don't wait — we write.""",
27: """SAY: "This card is the course's own experiment: written before any prompting instruction, reopened on Day 3."
KEY POINT: Think of one real task from your job, write the prompt exactly as you'd type it, post it to the whiteboard — no scoring, no coaching yet; we unseal these at P10 and measure how far your prompting has come.
(5 min activity — keep them writing, not optimizing)
TRANSITION: One trap to sidestep on the way back to the VM.""",
28: """ASK: "Who's already spotted the RDP button? Hands up — now promise me you won't click it."
KEY POINT: The RDP button errors and is not needed — it is the single most common launch failure; always use the in-browser Viewer, and if you clicked RDP by mistake, just return to the Viewer.
(~1 min)
TRANSITION: Assuming we're all in the Viewer — starting the labs.""",
29: """SAY: "Firefox should open straight into JupyterLab; if it doesn't, one desktop icon fixes it."
KEY POINT: Autostart is the front door (bookmark: 'Course Labs'); the fallback is the 'Start Labs' desktop icon; the one-time password is 'pw'; you should see a file list of lab notebooks.
(~1 min)
TRANSITION: Thirty seconds of orientation so that file list makes sense.""",
30: """SAY: "Everything on this screen gets reused in every lab this week — thirty seconds now saves hours later."
KEY POINT: Left panel is the file browser; a notebook is a list of cells — run them in order; Run All Cells executes top to bottom; if a run hangs, Restart Kernel and re-run; notebook names match lab numbers, all data is public or synthetic, solutions ship on the VM.
(~2 min)
TRANSITION: Two more things about what's in that file list.""",
31: """ASK: "Stuck on a lab late on Day 2 — what's your move? Try first, then peek: solution notebooks are on the VM."
KEY POINT: Names match lab numbers (lab_1.2 = Lab 1.2); datasets are public or synthetic; solution notebooks exist if you get stuck; some labs use an AI assistant in your browser instead of a notebook.
(~1 min)
TRANSITION: So how do we prove the environment is healthy? Four checks.""",
32: """SAY: "Four green checks are the difference between a smooth week and a broken one: packages, data files, the API key, and data.gov."
KEY POINT: Checks 1-3 must be green — required packages installed, lab data files readable, the class API key works on a one-token call; check 4 (data.gov reachable) is informational — cached fallbacks exist.
(~1 min)
TRANSITION: Run it now.""",
33: """SAY: "Open lab_0.1_healthcheck.ipynb, Run All Cells — green means go."
KEY POINT: Confirm the first checks say PASS; raise your hand on any red FAIL — every red gets a fix before anyone moves on.
(Within the 15-min DO NOW 0.1 — instructor pairs reds with fixes; this notebook is the tech check)
TRANSITION: Here is exactly what 'done' looks like.""",
34: """ASK: "How do you know you're done? Don't guess — compare your screen to this checklist."
KEY POINT: Done = file list of notebooks in the left panel, healthcheck open with all cells executed, checks 1-3 green PASS; a hand up on anything red gets an instructor.
(~1 min — visually confirm every screen; this is the gate for Chapter 1)
TRANSITION: If you're not seeing this, it's almost always one of five things.""",
35: """SAY: "If your screen disagrees, it's almost always one of these five."
KEY POINT: The five common failures: RDP button errors (use the Viewer); a cosmetic .bashrc error (proceed if labs run); Firefox didn't open Jupyter ('Start Labs' icon); password prompt ('pw', one time); empty notebook list (re-run 'Start Labs', then re-launch the VM). If a class hits a sixth, report it so the table grows.
(~2 min — work the list top to bottom for anyone red)
TRANSITION: Environment green. Now the accounts you'll use — and the rule that governs them.""",
36: """ASK: "Which ChatGPT account should you use this week? The answer is a rule, not a preference."
KEY POINT: Use only the assistant account your instructor designates; public or synthetic data only — never paste real agency or personal data; the rule holds for every lab and mirrors your agency's acceptable-use policy.
(~2 min)
TRANSITION: The same rule, stated as a decision you can reuse at work.""",
37: """SAY: "In class: the designated account. At work: your agency's approved licensed tool. On your own: free tools, public data only."
KEY POINT: The decision rule — nothing but the designated account in class; the approved licensed tool at work, never a personal account; free public tools are fine for learning and public data; unsure? Ask your IT or AI governance office first.
(~2 min)
TRANSITION: The rule itself, up front, before any lab touches an assistant.""",
38: """ASK: "What happens to text you paste into a public chatbot? Assume the worst — you're right."
KEY POINT: Public or synthetic data only, every lab, every prompt, all three days; no PII, procurement-sensitive, or law-enforcement data in any unapproved tool; bullet 4 is literal policy — M-25-21 requires every agency to have a generative-AI acceptable-use policy; a pasted constituent record is a reportable spill.
(~2 min)
TRANSITION: This rule isn't anti-AI — it's what keeps AI usable. Why, next.""",
39: """SAY: "The rule exists so agencies can keep using AI — every avoided spill is one more year the tools stay approved."
KEY POINT: Public chatbots may store what you paste, outside your agency's control; pasting a constituent record is a reportable data spill; frame constructively — the rule makes approved AI use sustainable; Chapter 5 goes deep on the risks.
(~2 min)
TRANSITION: Now, how we'll learn all this — a quick look under the hood of the course design.""",
40: """SAY: "Remember, understand, apply, analyze, evaluate, create — this course is engineered to move you up that ladder."
KEY POINT: Lectures build understanding; labs move you to Apply and Analyze; the capstone reaches Create. Instructor note: cite the Anderson & Krathwohl (2001) revision — verb forms, Create at the top — not the 1956 original.
(~2 min)
TRANSITION: The six levels in plain words.""",
41: """ASK: "What's the difference between evaluating and creating? By Thursday, you'll have done both."
KEY POINT: Plain words: recall a fact, explain it, use it on a new task, compare and troubleshoot, judge quality against criteria — our rubric does this — and build something new: the capstone agent.
(~2 min if taught — teach when the room wants the theory)
TRANSITION: Here's how each day climbs.""",
42: """SAY: "Day 1 you understand and apply; Day 2 you analyze; Day 3 you evaluate and create — the week is the ladder."
KEY POINT: Day 1: Understand/Apply. Day 2: Apply/Analyze. Day 3: Evaluate/Create with the capstone. Objectives, activities, and assessments are all aligned to these levels.
(~1 min)
TRANSITION: Why so little lecture? Because that's how adults learn.""",
43: """SAY: "Notice we put a working lab before any theory this morning — that was a design decision, not an accident."
KEY POINT: Adults learn best when new skills solve immediate, real problems, with their own experience as a resource — which is why every activity uses government scenarios, not toy examples, and why debriefs harvest the room's experience.
(~2 min if taught — the answer to 'why so little lecture?')
TRANSITION: One shared tool makes the doing social — the class whiteboard.""",
44: """ASK: "Who's used Mural? Either way, by the first debrief you'll be posting like a pro."
KEY POINT: We use a shared Mural board for discussions and lab debriefs: your instructor shares the link, ideas go on sticky notes, we review as a group — and the wish list from introductions already lives there.
(~1 min)
TRANSITION: The rhythm those debriefs belong to.""",
45: """SAY: "Learn a little, do it, talk about what happened — repeat for three days."
KEY POINT: Every concept follows the same rhythm: short lecture, an immediate lab or exercise, then a debrief — what worked, what surprised you, what you'd do differently; many debriefs land on the whiteboard.
(~1 min)
TRANSITION: Two norms make the whiteboard worth reading.""",
46: """ASK: "What makes a sticky note worth reading? Short, specific, one idea — and everyone posts."
KEY POINT: One idea per sticky; everyone posts — the quietest observation is often the useful one; we review the board after each activity and return to it on Day 3. Instructor: the board was cloned before class (Day-0 tech check).
(~1 min)
TRANSITION: Zooming back out — the roadmap as themes.""",
47: """SAY: "Same map, wider lens: foundations first, then craft, then building."
KEY POINT: Day 1: foundations, applications, desktop GenAI. Day 2: prompt engineering, security, data for AI. Day 3: building with LLMs — APIs, RAG, agents — plus operations; hands-on labs throughout, capstone on Day 3.
(~1 min)
TRANSITION: The practicalities for the week.""",
48: """ASK: "The logistics question I always get: 'Can I reach my VM after hours?' Yes — from your My Learning Tree account, anytime."
KEY POINT: Three days, lecture plus labs daily; the CloudShare VM is reachable anytime; workbook pages accompany every lab including DO NOW 0.1; the whiteboard link and class AI accounts come from your instructor.
(~2 min — add room-specific details: breaks, building rules)
TRANSITION: Ten terms that carry the week — part one.""",
49: """SAY: "Six terms, zero jargon allowed past this slide — every one recurs from Chapter 1 onward."
KEY POINT: AI/ML learns patterns from data; generative AI/LLMs produce content; a prompt is your instruction; hallucination is confident, plausible, wrong output; RAG grounds answers in your documents; an agent acts, not just chats.
(~2 min — orientation, not instruction; formal definitions come in Ch01/Ch04/Ch07)
TRANSITION: Part two — the institutional terms.""",
50: """ASK: "Who is your agency's Chief AI Officer? If you don't know, that's homework — M-25-21 says you have one."
KEY POINT: API (Day 3 makes it hands-on), FedRAMP, acceptable-use policy, Chief AI Officer, the annual public use-case inventory, synthetic data — the CAIO and the inventory are M-25-21 requirements; FedRAMP and the AUP recur in Ch03/Ch05.
(~2 min)
TRANSITION: Let's close the launch with the one-slide summary.""",
51: """SAY: "Federal AI use nearly doubled in a year — you are not studying a trend, you are joining one."
KEY POINT: This course turns government IT staff into effective, safe AI users; you now know the environment, the accounts, the data rule, and the map.
(~1 min)
TRANSITION: One last hands-on before Chapter 1: the environment and data tour.""",
52: """SAY: "Your VM works — now take twenty minutes to learn the room before the course leans on it."
KEY POINT: Lab 0.1: open lab_0.1_environment_tour.ipynb, run the environment cell, then the data inventory cell — where the notebooks are, where the data is (MANIFEST.json, federal_ai_use_cases.csv, chicago_311.csv), and how a notebook reaches the model via the OpenAI key in .env.
(20 min lab — circulate; full instructions in the Lab Manual)
TRANSITION: Final gate before Chapter 1 — the checkpoint.""",
53: """ASK: "Hands up if you can state the data rule from memory. Keep them up only if you mean it."
KEY POINT: Before Chapter 1: a running VM with JupyterLab open, green PASS on checks 1-3, your P0 prompt on the whiteboard, and the data rule — public or synthetic only — memorized; if any hand is up, fix it now.
(~3 min — check each item; the IG forbids starting Chapter 1 before the room is green)
TRANSITION: Room is green — on to Chapter 1, AI and ML Foundations.""",
}

if __name__ == "__main__":
    apply_notes(TAG, COUNT, NOTES, FLEX_CORE)
    verify(TAG, COUNT)
