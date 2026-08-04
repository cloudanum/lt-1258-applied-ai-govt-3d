"""Ch00 Course Launch enrichment content (rev a3): 12 existing slides + 38 new = 50.

Factual claims trace to 1258/research/refs-ch00-ch09-launch-trends.md (URLs verified
2026-08-01) and to GAO-25-107653 (verified live at gao.gov on 2026-08-01). Lab/DONOW
specifics trace to the IG (1258-IGa3-Instructor-Guide.md), the Revision Plan (§2, §3.1)
and the workbook lab pages. Content is author input; Pubs styles it.
"""

GAO_SRC = ("Source: U.S. GAO — Artificial Intelligence: Generative AI Use and Management "
           "at Federal Agencies (GAO-25-107653), https://www.gao.gov/products/gao-25-107653 "
           "(verified 2026-08-01)")
DOI_SRC = ("Source: U.S. Department of the Interior — Department of the Interior Artificial "
           "Intelligence Strategy (2025), https://www.doi.gov/sites/default/files/documents/2025-09/"
           "doi-ai-strategy.pdf (verified 2026-08-01)")
M25_SRC = ("Source: OMB — M-25-21: Accelerating Federal Use of AI through Innovation, Governance, "
           "and Public Trust, https://www.whitehouse.gov/wp-content/uploads/2025/02/"
           "M-25-21-Accelerating-Federal-Use-of-AI-through-Innovation-Governance-and-Public-Trust.pdf "
           "(verified 2026-08-01)")
CELT_SRC = ("Source: Iowa State University CELT — Bloom's Taxonomy, "
            "https://celt.iastate.edu/prepare-and-teach/design-your-course/blooms-taxonomy/ "
            "(verified 2026-08-01)")
KENT_SRC = ("Source: Anderson & Krathwohl via University of Kent — A Taxonomy for Learning, "
            "Teaching, and Assessing, https://www.kent.ac.uk/brussels/handbook/taxonomy.pdf "
            "(verified 2026-08-01)")

# Corrected TOC lines (slide 3) — titles match the shipped a3 chapter decks.
TOC_CHAPTERS = [
    "\t\tIntroduction and Overview",
    "Chapter 1\tAI and ML Foundations for Government",
    "Chapter 2\tAI Applications Across Government and Public Data",
    "Chapter 3\tDesktop GenAI: Everyday AI for Government Staff",
    "Chapter 4\tModern GenAI and Prompt Engineering",
    "Chapter 5\tAI Security, Risks, and Responsible AI",
    "Chapter 6\tData for AI: Collection, Quality, and Governance",
    "Chapter 7\tBuilding with LLMs: APIs, RAG, and Agents",
    "Chapter 8\tAI Operations and Reporting in Government",
    "Chapter 9\tCourse Summary and Your Agency AI Roadmap",
    "\t\tNext Steps",
]

# Corrected appendix TOC (slide 4) — four appendices in rev a3.
TOC_APPENDICES = [
    "Appendix A\tMachine Learning Life Cycle Core Principles",
    "Appendix B\tChallenges and Ethical Considerations",
    "Appendix C\tBuilding Block of Generative AI",
    "Appendix D\tClassic ML and Data Engineering Deep Dive",
]

NOTES_OBJECTIVES = (
    "Course-level objectives (unchanged from a2). Each one maps to a Bloom's level — see "
    "'Course Objectives and Bloom's Levels' later in this unit and the Bloom's slides near "
    "the end of the launch block. Alignment of objectives, instruction, and assessment per "
    "Iowa State CELT guidance. " + CELT_SRC)

NOTES_TOC = ("Corrected for rev a3: the TOC now reflects the Ch00-Ch09 structure (the old TOC "
             "listed eight chapters and ended at 'Chapter 8 Course Summary'). Titles match the "
             "shipped chapter decks.")

NOTES_TOC_APPENDIX = ("Corrected for rev a3: the course now ships four appendices (A-D); the "
                      "old slide listed only A-C.")

NOTES_BLOOMS = (
    "Formalizes Bloom's, which Greg noted Imran teaches from memory. Now it's in the deck for "
    "any instructor. Note for instructors: the sequence shown is the Anderson & Krathwohl (2001) "
    "revision of Bloom's 1956 taxonomy — verb forms, Create at the top — so cite the 2001 "
    "revision, not the 1956 original. " + KENT_SRC)

# New slides, in final pedagogical order of appearance (interleaved with existing
# slides by build_enrich_ch00.py's arrange() permutation).
CH00_NEW = [
 # --- opening / re-frame ---
 ("Course Launch: Objectives",
  ["Get your CloudShare lab environment running and verified (DO NOW 0.1)",
   "Know which AI account to use this week — and the data rule that governs it",
   "See the three-day course map and the prompting spine (P0 to P10)",
   "Understand how labs, debriefs, and the class whiteboard work"],
  "Chapter opener, house style (matches the Ch03-Ch09 'Chapter objectives:' pattern). These are "
  "the launch unit's own objectives; the course-level objectives come a few slides later."),
 ("Welcome: Who This Course Is For",
  ["You work in government IT and use — or will use — AI tools in your job",
   "No programming or data-science background is assumed",
   "You will leave able to use AI assistants effectively, safely, and within policy",
   "Every activity uses real government tasks and public or synthetic data"],
  "Re-frame for the AI-user audience. Say it plainly: this course is for users of AI, not "
  "builders of models — that is what changed in this revision."),
 ("Introductions: Who's in the Room",
  ["Your name, agency, and role",
   "One AI tool you have used — or one task you wish AI could help with",
   "Instructor: capture the tasks on the whiteboard",
   "We revisit that wish list on Day 3 when you build your roadmap"],
  "Two minutes per row of the room. The wish-list stickies become raw material for the Day-3 "
  "90-day-roadmap discussion and let attendees watch the course arc land on their own needs."),
 ("What This Course Will Do",
  ["Build practical skill with the AI assistants government staff actually use",
   "Teach you to prompt well, check output, and know AI's limits",
   "Show how agencies deploy AI today — applications, risks, and operations",
   "Give you hands-on labs on public and synthetic data, plus a capstone agent build"],
  "The positive half of the expectations contract."),
 ("What This Course Won't Do",
  ["It will not make you a data scientist or machine-learning engineer",
   "It will not teach you to train large models from scratch",
   "It is not legal, procurement, or policy certification for your agency",
   "It does not replace your agency's own AI acceptable-use training"],
  "Set expectations early — prevents the two classic Day-1 complaints: 'too technical' and "
  "'not technical enough.' Point deep-dive appetites to the appendices and next-step courses."),
 ("How to Get the Most Out of These Three Days",
  ["Ask questions as they come — the room's experience is course material",
   "Try every lab; fallback paths mean no one stays stuck for long",
   "Connect each activity to a real task from your own job",
   "Collect your keeper prompts — they are your take-home toolkit"],
  "[flex] Skip when the room is senior or time is tight; the advice repeats implicitly all week."),
 # --- AI in government today ---
 ("AI in Government Today: The Numbers (as of mid-2026)",
  ["GAO reviewed 11 agencies' AI inventories: use cases nearly doubled in one year",
   "Reported AI use cases grew from 571 in 2023 to 1,110 in 2024",
   "Growth spans mission work and internal operations — not just pilots",
   "Your agency publishes its own AI use-case inventory every year"],
  "Measured, audited growth — not hype. Have attendees look up their own agency's public "
  "inventory this week (M-25-21 requires it). " + GAO_SRC),
 ("Generative AI in Government: Ninefold Growth (as of mid-2026)",
  ["Generative-AI use cases rose about ninefold: 32 in 2023 to 282 in 2024",
   "Agencies cite gains in communications, information access, and program tracking",
   "Top challenges: complying with federal policy, budget, and technical resources",
   "Agencies struggle to keep acceptable-use policies current — this course helps"],
  "Same GAO review: officials at 10 of 12 selected agencies said existing federal policy could "
  "present obstacles, and rapid change complicates keeping GenAI policies current — sets up the "
  "data-rule slides later this hour. " + GAO_SRC),
 ("Federal AI Wins with Numbers: Mission",
  ["USGS: critical-minerals analysis cut from years to weeks",
   "NICC: wildfire-intelligence automation saves 200+ expert-hours per year",
   "Interior pairs FedRAMP-authorized cloud with on-prem/HPC for sensitive workloads",
   "These are running systems, documented in a public agency AI strategy"],
  "Quantified frontline use cases from Interior's public, M-25-21-aligned AI strategy "
  "(September 2025). " + DOI_SRC),
 ("Federal AI Wins with Numbers: Operations",
  ["Grants review: 8,000 awards reviewed in 4 hours — previously 500+ hours",
   "National Park Service: funding-request tool estimated to save 7,000 labor-days/year",
   "The pattern: frontline staff with approved tools, not moonshots, drove the ROI",
   "That pattern is exactly what this course trains you to repeat"],
  "Draw the lesson explicitly: the biggest returns came from frontline staff using approved "
  "tools on ordinary work. " + DOI_SRC),
 ("Your Policy Landscape: OMB M-25-21 in One Slide",
  ["OMB M-25-21 (April 2025) governs federal AI use; it replaced M-24-10",
   "Your agency has a Chief AI Officer and an AI governance structure",
   "Agencies publish AI strategies and annual public use-case inventories",
   "'High-impact AI' — decisions affecting rights or safety — has mandatory safeguards",
   "Every agency must have a generative-AI acceptable-use policy"],
  "[flex] Depth slide for rooms that ask 'what actually requires us to do this?' M-25-21 "
  "(Apr 3, 2025) rescinded and replaced M-24-10; companion memo M-25-22 covers AI acquisition. "
  "'High-impact AI' = output is a principal basis for decisions with legal, material, binding, "
  "or significant effect on rights or safety. " + M25_SRC),
 ("You Are Not Alone: The Federal AI Support Ecosystem",
  ["GSA AI Guide for Government — plain-language chapters for decision-makers",
   "GSA government-wide AI Training Series: technical, acquisition, and leadership tracks",
   "GSA AI Community of Practice — peer agencies sharing what works",
   "NIST AI Risk Management Framework — the federal trustworthiness reference"],
  "[flex] Bookmark slide — attendees take these links home. Sources: GSA CoE — AI Guide for "
  "Government, https://coe.gsa.gov/coe/ai-guide-for-government/ ; GSA — AI Strategies and "
  "Compliance Plan, https://www.gsa.gov/artificial-intelligence/resources/ai-strategies-and-compliance-plan "
  "; NIST — AI Risk Management Framework, https://www.nist.gov/itl/ai-risk-management-framework "
  "(all verified 2026-08-01)"),
 # --- objectives mapping (existing slide 2 sits just before this) ---
 ("Course Objectives and Bloom's Levels",
  ["Foundations and applications objectives target Understand",
   "Labs and exercises move you to Apply and Analyze",
   "Risk and operations work builds Analyze and Evaluate",
   "The capstone agent build reaches Create"],
  "Makes the objectives-to-Bloom's link explicit, per Iowa State CELT guidance on aligning "
  "objectives, instruction, and assessment. " + CELT_SRC),
 # --- conventions and course map ---
 ("Course Conventions: DO NOWs, Exercises, Labs, and Flex",
  ["DO NOWs are short startup activities — DO NOW 0.1 is coming up in minutes",
   "Labs are numbered by chapter: Lab 4.1 is Chapter 4's first lab",
   "Exercises (Ex) are shorter in-class activities; optional labs go deeper",
   "Items marked [flex] are taught when time allows — your instructor decides"],
  "Explains the numbering conventions so registry IDs make sense all week. Notebook filenames "
  "match lab numbers (lab_4.1 belongs to Lab 4.1)."),
 ("Course Map: Three Days at a Glance",
  ["Day 1: Foundations (Ch01), Applications & Public Data (Ch02), Desktop GenAI (Ch03)",
   "Day 2: Prompt Engineering (Ch04), Security & Responsible AI (Ch05), Data for AI (Ch06)",
   "Day 3: APIs, RAG & Agents (Ch07), Operations & Reporting (Ch08), Roadmap (Ch09)",
   "Hands-on labs every day; the capstone agent build closes Day 3"],
  "Chapter-level map; the 'Course Roadmap' slide near the end of this unit restates the same "
  "arc as themes. Timing per the IG Day 1-3 tables."),
 ("The Prompting Spine: P0 to P10",
  ["Prompting is a through-line: a named rung (P0-P10) inside activities you already do",
   "One scoring rubric — accuracy, completeness, format, tone — used all week",
   "You write your first prompt (P0) today, before any instruction",
   "On Day 3 (P10) you rewrite it with everything you learned — and see the difference"],
  "The visible promise. Rungs live inside existing activities and get no new activity IDs "
  "(Revision Plan §3.1). By Day 3 PM each attendee re-scores their own Day-1 prompt against "
  "the rubric and watches three days add up."),
 ("Your Prompt Card: The Take-Home Artifact",
  ["Each spine rung contributes one keeper prompt to your Prompt Card",
   "By Day 3 you hold roughly ten field-tested prompts for real work",
   "The card lives in your workbook — keep it at your desk on Monday",
   "Same rubric, same card, all week — no new tools to learn"],
  "Revision Plan §3.1 and Lab Planner R5: the Prompt Card is the course take-home artifact."),
 # --- DO NOW 0.1 full walkthrough (existing CloudShare slide sits just before) ---
 ("DO NOW 0.1: The Next 15 Minutes",
  ["Goal: everyone at a running JupyterLab with a green healthcheck — before Chapter 1",
   "Step 1: launch your VM and open the in-browser Viewer",
   "Step 2: reach JupyterLab and open lab_0.1_healthcheck.ipynb",
   "Step 3: Run All Cells and confirm the green PASS checks",
   "While your VM boots, you will also write your first prompt (P0)"],
  "15 minutes total, per the IG timing table. Instructor circulates; do not start Chapter 1 "
  "until the room is green."),
 ("While Your VM Boots: Your First Prompt (P0)",
  ["Think of one real task from your job you would ask an AI assistant to do",
   "Write the prompt — exactly as you would type it — on your card",
   "No scoring, no explanation yet; post it to the class whiteboard",
   "We unseal these on Day 3 and measure how far your prompting has come"],
  "Spine rung P0 (Revision Plan §3.1): the cards are written before any prompting instruction, "
  "posted unscored, and reopened at P10 on Day 3 — the course's own pre/post evidence."),
 ("The RDP Button — Do Not Use",
  ["CloudShare shows an RDP button — it errors and is not needed",
   "Always use the in-browser Viewer to reach your VM desktop",
   "If you clicked RDP by mistake, just return to the Viewer",
   "Instructors: this is the single most common launch failure"],
  "Known CloudShare issue (Greg Adams' report; row 1 of the IG's failure table). Worth its own "
  "slide — it costs whole classes ten minutes when it is only a bullet."),
 ("Lab Environment Tour: JupyterLab",
  ["Left panel: file browser with all lab notebooks and data files",
   "A notebook is a list of cells — code or text; run them in order",
   "Run menu -> Run All Cells executes the whole notebook top to bottom",
   "If a run hangs: Kernel menu -> Restart Kernel, then re-run"],
  "Thirty-second orientation for attendees who have never seen Jupyter. Everything here is "
  "used again in every notebook lab this week."),
 ("Lab Environment Tour: Notebooks and Data Files",
  ["Notebook names match lab numbers: lab_1.2 belongs to Lab 1.2",
   "All datasets are public (for example, data.gov) or synthetic",
   "Solution notebooks are available if you get stuck — try first, then peek",
   "Some labs use an AI assistant in your browser instead of a notebook"],
  "Names-match-lab-numbers is the a3 rename fix (see MOVES.md). Solutions and expected-output "
  "transcripts ship on the VM per the lab plan."),
 ("Healthcheck: What the Four Checks Prove",
  ["Check 1: the required Python packages are installed",
   "Check 2: the lab data files are present and readable",
   "Check 3: the class API key works with a one-token test call",
   "Check 4: data.gov is reachable — informational; a fallback exists"],
  "The four checks per the Revision Plan. Checks 1-3 must be green; check 4 is informational "
  "per the workbook, and cached fallbacks exist for offline classrooms."),
 ("You're Done When You See This",
  ["A file list of lab notebooks in JupyterLab's left panel",
   "lab_0.1_healthcheck.ipynb open, all cells executed",
   "Checks 1-3 showing green PASS",
   "Raise your hand for anything red — your instructor has a fix"],
  "The 'you're done when you see this' checkpoint from the Revision Plan. Instructor: visually "
  "confirm every screen before moving on — this is the gate for Chapter 1."),
 ("If Something Goes Wrong: The Five Common Failures",
  ["RDP button errors -> use the in-browser Viewer (known issue)",
   "A .bashrc error in the terminal -> cosmetic; if labs run, proceed",
   "Firefox doesn't open Jupyter -> double-click 'Start Labs' on the desktop",
   "Password prompt -> it is: pw (one time)",
   "Empty notebook list -> re-run 'Start Labs'; if still empty, re-launch the VM"],
  "The IG's five most common startup failures, verbatim. If a class hits a sixth, report it to "
  "PD Lab so the table grows."),
 # --- accounts and the data rule (existing slide 9 sits just before) ---
 ("Which AI Account Should You Use?",
  ["In class: the assistant account your instructor designates — nothing else",
   "At work: your agency's approved, licensed tool — not a personal account",
   "Free public tools: fine for learning and public data only",
   "Unsure whether a tool is approved? Ask your IT or AI governance office first"],
  "Answers Greg Adams' 'which ChatGPT account?' question as a decision rule. Editions, tiers, "
  "and FedRAMP detail come in Chapter 3; this slide is only the rule."),
 ("The Data Rule, Up Front",
  ["Public or synthetic data only in class labs — never real agency or personal data",
   "No PII, procurement-sensitive, or law-enforcement data in any unapproved tool",
   "This rule holds for every lab, every prompt, all three days",
   "It mirrors the acceptable-use policy your agency is required to have"],
  "Stated before any lab touches an assistant (Andrew Tait's guardrail). Bullet 4 is literal "
  "policy: M-25-21 §3(b)(iv) requires every agency to establish a generative-AI acceptable-use "
  "policy within 270 days of April 2025. " + M25_SRC),
 ("Why the Data Rule Exists",
  ["Public chatbots may store what you paste — outside your agency's control",
   "Pasting a constituent record into a public tool is a reportable data spill",
   "The rule is not anti-AI — it is how agencies keep using AI",
   "Chapter 5 goes deep on risks; for now, the rule keeps everyone safe"],
  "Course doctrine (Ch03 data rule). Frame constructively: the rule is what makes approved AI "
  "use sustainable, not a reason to avoid the tools."),
 # --- how we learn (existing Bloom's slide sits just before) ---
 ("The Six Levels in Plain Words",
  ["Remember: recall a fact; Understand: explain it in your own words",
   "Apply: use it on a new task; Analyze: compare and troubleshoot",
   "Evaluate: judge quality against criteria — our rubric does this",
   "Create: build something new — the capstone agent"],
  "[flex] Depth slide — teach when the room wants the theory. The sequence is the Anderson & "
  "Krathwohl (2001) revision of Bloom's taxonomy. " + KENT_SRC),
 ("How Each Day Moves You Up the Ladder",
  ["Day 1: Understand and Apply — what AI is, using assistants on real tasks",
   "Day 2: Apply and Analyze — prompting, security scenarios, data quality",
   "Day 3: Evaluate and Create — score outputs, then build an agent",
   "Objectives, activities, and assessments are aligned to these levels"],
  "The day-level Bloom's map. Alignment of objectives, instruction, and assessment per Iowa "
  "State CELT guidance. " + CELT_SRC),
 ("Why This Course Is Hands-On: How Adults Learn",
  ["Adults learn best when new skills solve immediate, real problems",
   "Your experience is a resource — debriefs harvest it for the room",
   "That is why a working lab comes before any theory this morning",
   "And why every activity uses government scenarios, not toy examples"],
  "[flex] Rationale slide for instructors asked 'why so little lecture?' — Knowles' andragogy "
  "assumptions (problem-centered immediacy, experience as resource, self-direction). "
  "Source: infed.org — Malcolm Knowles, informal adult education, self-direction and andragogy, "
  "https://infed.org/dir/malcolm-knowles-informal-adult-education-self-direction-and-andragogy/ "
  "(verified 2026-08-01)"),
 # --- how labs, debriefs, and Mural work (existing whiteboard slide sits before) ---
 ("The Activity Rhythm: Learn, Do, Debrief",
  ["Short lecture segments introduce each concept",
   "A lab or exercise immediately puts it to work",
   "A debrief follows: what worked, what surprised you, what you'd do differently",
   "Many debriefs land on the class whiteboard — bring your observations"],
  "The repeating pattern all week. Debrief questions with model answers live in the IG for "
  "every activity."),
 ("Whiteboard Norms: Getting Value from Mural",
  ["One idea per sticky note; short and specific beats long and general",
   "Everyone posts — the quietest observation is often the useful one",
   "We review the board together after each activity",
   "The board stays up all week; we return to it on Day 3"],
  "Bill Appelbe's whiteboard pattern, operationalized. Instructor: clone the board before "
  "class (Day-0 tech check, IG §2)."),
 # --- close of launch unit (existing roadmap slide sits just before) ---
 ("Logistics for the Week",
  ["The course runs three days; every day mixes lecture and hands-on labs",
   "Your CloudShare VM is reachable anytime from your My Learning Tree account",
   "Workbook pages accompany every lab — including DO NOW 0.1",
   "The whiteboard link and class AI accounts come from your instructor"],
  "Generic logistics only — room-specific details (breaks, building rules) are the instructor's "
  "to add verbally."),
 ("Key Terms for the Week (1 of 2)",
  ["AI / machine learning: systems that learn patterns from data to make predictions",
   "Generative AI / LLM: models that produce text, images, or other content",
   "Prompt: the instruction you give an AI assistant",
   "Hallucination: confident, plausible — and wrong — AI output",
   "RAG: retrieval-augmented generation — grounding answers in your documents",
   "Agent: an AI that uses tools and acts, not just chats"],
  "Mini-glossary, part 1. Every term recurs from Chapter 1 onward; attendees can add their own "
  "terms to the workbook. Formal definitions are taught in Ch01/Ch04/Ch07 — this is orientation, "
  "not instruction."),
 ("Key Terms for the Week (2 of 2)",
  ["API: how programs call an AI model — Day 3 makes this hands-on",
   "FedRAMP: the federal security authorization for cloud services",
   "Acceptable-use policy (AUP): your agency's rules for AI tools",
   "Chief AI Officer (CAIO): the official accountable for your agency's AI",
   "Use-case inventory: your agency's annual public list of AI systems",
   "Synthetic data: made-up data shaped like real data — safe for labs"],
  "Mini-glossary, part 2. The CAIO and the annual public use-case inventory are M-25-21 "
  "requirements; FedRAMP and the AUP recur in Ch03/Ch05. " + M25_SRC),
 ("Chapter Summary: Course Launch",
  ["This course turns government IT staff into effective, safe AI users",
   "Federal AI use nearly doubled in one year — you are joining a live shift",
   "You now know the environment, the accounts, the data rule, and the map",
   "Next: Chapter 1 — AI and ML Foundations for Government"],
  "Chapter summary, house style. The GAO figure is the one-slide version of the snapshot "
  "block from earlier this hour."),
 ("Checkpoint: What You Should Have Right Now",
  ["A running VM with JupyterLab open in your browser",
   "A healthcheck showing green PASS on checks 1-3",
   "Your first prompt (P0) posted to the class whiteboard",
   "The data rule: public or synthetic only — you can state it from memory"],
  "Final gate before Chapter 1. If any hand is up, fix it now — the IG forbids starting "
  "Chapter 1 before the room is green."),
]

# Final arrangement as 0-based indices into (12 existing slides at 0-11) + (38 new
# appended at 12-49). Existing: 0 title, 1 objectives, 2 TOC, 3 appendix TOC,
# 4 CloudShare, 5 Getting In, 6 Starting Labs, 7 DO NOW healthcheck, 8 accounts/data,
# 9 Bloom's, 10 whiteboard, 11 roadmap.
ORDER0 = [
    0,                       #  1 title
    12, 13, 14, 15, 16, 17,  #  2-7  launch objectives, welcome, intros, will/won't, get-most[flex]
    18, 19, 20, 21,          #  8-11 AI-in-gov snapshot (GAO x2, DOI x2)
    22, 23,                  # 12-13 M-25-21 [flex], support ecosystem [flex]
    1,                       # 14 course objectives (existing)
    24,                      # 15 objectives & Bloom's
    2, 3,                    # 16-17 TOC + appendices (corrected)
    25,                      # 18 conventions
    26, 27, 28,              # 19-21 course map, spine P0-P10, prompt card
    4,                       # 22 CloudShare (existing)
    29,                      # 23 DO NOW 0.1 overview
    5,                       # 24 Getting In (existing)
    30,                      # 25 P0 while VM boots
    31,                      # 26 RDP button
    6,                       # 27 Starting the Labs (existing)
    32, 33,                  # 28-29 tour JupyterLab, tour notebooks/data
    34,                      # 30 four checks
    7,                       # 31 DO NOW healthcheck (existing)
    35, 36,                  # 32-33 done-when, five failures
    8,                       # 34 accounts & data rules (existing)
    37, 38, 39,              # 35-37 which account, data rule, why the rule
    9,                       # 38 Bloom's (existing, notes corrected)
    40, 41, 42,              # 39-41 six levels [flex], days up ladder, adults learn [flex]
    10,                      # 42 whiteboard (existing)
    43, 44,                  # 43-44 rhythm, Mural norms
    11,                      # 45 course roadmap (existing)
    45,                      # 46 logistics
    46, 47,                  # 47-48 key terms 1-2
    48, 49,                  # 49-50 chapter summary, checkpoint
]
