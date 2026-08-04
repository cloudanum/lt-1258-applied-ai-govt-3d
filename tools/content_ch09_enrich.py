"""New slides for Ch09 'Course Summary and Your Agency AI Roadmap' enrichment
(rev a3). 39 new slides appended to the 11 existing ones -> 50 total.
Content is author input; every research-grounded note cites a source verified
live 2026-08-01 (see 1258/research/refs-ch00-ch09-launch-trends.md).

Append order N1..N39; final positions are set by build_enrich_ch09.py."""

SRC_ANTHROPIC = ("Source: Anthropic — Building Effective Agents, "
                 "https://www.anthropic.com/engineering/building-effective-agents (verified 2026-08-01)")
SRC_O3 = ("Source: OpenAI — Introducing OpenAI o3 and o4-mini, "
          "https://openai.com/index/introducing-o3-and-o4-mini/ (verified 2026-08-01)")
SRC_GEMINI = ("Source: Google DeepMind — Introducing Gemini 2.0: our new AI model for the agentic era, "
              "https://blog.google/technology/google-deepmind/google-gemini-ai-update-december-2024/ (verified 2026-08-01)")
SRC_GPTOSS = ("Source: OpenAI — Introducing gpt-oss, "
              "https://openai.com/index/introducing-gpt-oss/ (verified 2026-08-01)")
SRC_DOI = ("Source: DOI OCIO — Department of the Interior Artificial Intelligence Strategy (2025), "
           "https://www.doi.gov/sites/default/files/documents/2025-09/doi-ai-strategy.pdf (verified 2026-08-01)")
SRC_AIINDEX = ("Source: Stanford HAI — The 2026 AI Index Report, "
               "https://hai.stanford.edu/ai-index/2026-ai-index-report (verified 2026-08-01)")
SRC_AIINDEX12 = ("Source: Stanford HAI — Inside the AI Index: 12 Takeaways from the 2026 Report, "
                 "https://hai.stanford.edu/news/inside-the-ai-index-12-takeaways-from-the-2026-report (verified 2026-08-01)")
SRC_GARTNER = ("Source: Gartner — Top Strategic Technology Trends for 2026, "
               "https://www.gartner.com/en/articles/top-technology-trends-2026 (verified 2026-08-01)")
SRC_M2521 = ("Source: OMB — M-25-21: Accelerating Federal Use of AI through Innovation, Governance, "
             "and Public Trust, "
             "https://www.whitehouse.gov/wp-content/uploads/2025/02/M-25-21-Accelerating-Federal-Use-of-AI-"
             "through-Innovation-Governance-and-Public-Trust.pdf (verified 2026-08-01)")
SRC_GSA = ("Source: GSA — AI Strategies and Compliance Plan, "
           "https://www.gsa.gov/artificial-intelligence/resources/ai-strategies-and-compliance-plan (verified 2026-08-01)")
SRC_GSA_GUIDE = ("Source: GSA Centers of Excellence — AI Guide for Government, "
                 "https://coe.gsa.gov/coe/ai-guide-for-government/ (verified 2026-08-01)")
SRC_NIST = ("Source: NIST — AI Risk Management Framework, "
            "https://www.nist.gov/itl/ai-risk-management-framework (verified 2026-08-01)")

CH09_NEW_SLIDES = [
 # --- Arc + per-day synthesis (N1-N4) ---
 ("Three Days, One Arc: From AI User to AI Builder",
  ["Day 1: foundations, government applications, desktop assistants",
   "Day 2: prompting technique, security and risk, data for AI",
   "Day 3: APIs, RAG, agents, operations — and this roadmap",
   "You arrived as an AI user; you leave able to build and govern"],
  "Framing slide for the recap. One sentence per day, then: 'today we turn that into a plan "
  "you can execute back at your agency.'"),
 ("What You Can Now Do — Day 1: Use AI Safely, Find the Data",
  ["Use desktop AI assistants under your agency's acceptable-use policy",
   "Apply the data rule: public or synthetic data in approved tools only",
   "Spot where AI fits government work — and where it does not",
   "Find and assess public datasets, such as data.gov, for AI use"],
  "Recap Day 1 (Ch01-Ch03, Labs 1.x, 2.1, 3.1). Ask for a show of hands: who used an approved "
  "assistant for real work before this course? Who feels safer doing it now?"),
 ("What You Can Now Do — Day 2: Prompt, Judge, Secure",
  ["Climb the prompt ladder: zero-shot, few-shot, role + format contract",
   "Score any output against a rubric — accuracy, completeness, format, tone",
   "Recognize prompt injection, data leakage, and shadow AI risks",
   "Minimize and mask PII before it touches a model"],
  "Recap Day 2 (Ch04-Ch06, Labs 4.1, 5.x). The ladder and the rubric return in the P10 "
  "re-score later in this chapter — flag that now."),
 ("What You Can Now Do — Day 3: Call APIs, Build RAG, Govern an Agent",
  ["Call an LLM API from Python and control cost and behavior",
   "Ground answers in your own documents with retrieval-augmented generation",
   "Build a tool-using agent — and keep a human in the loop",
   "Monitor, visualize, and explain model behavior in operations"],
  "Recap Day 3 (Ch07-Ch08, Labs 7.1-7.3, 8.x). The capstone agent (Lab 7.3) is the proof "
  "point: attendees have already built the thing the trends slides describe."),

 # --- Use-case enrichment (N5) ---
 ("Federal AI Wins, With Numbers (2025)",
  ["USGS critical-minerals analysis cut from years to weeks",
   "Wildfire-intelligence automation saves 200+ expert-hours per year (NICC)",
   "8,000 grant awards reviewed in 4 hours — previously 500+ staff-hours",
   "An NPS funding-request tool estimated to save 7,000 labor-days per year",
   "Pattern: frontline staff with approved tools, not moonshots"],
  "All four cases are from DOI's public AI strategy (September 2025). The lesson for attendees: "
  "the biggest returns came from giving frontline staff approved tools for real work, which is "
  "exactly what the 90-day roadmap is built to replicate.\n" + SRC_DOI),

 # --- Governance bridge (N6) ---
 ("Human-in-the-Loop Is Policy, Not Preference",
  ["OMB M-25-21 requires human oversight for high-impact AI",
   "Agencies must be able to intervene — and discontinue underperforming systems",
   "Commercial agent designs echo this: confirmation before sensitive actions",
   "'AI enhances, not replaces' is a compliance position, not a slogan"],
  "Reframe the course's recurring slogan as policy. M-25-21's minimum practices for high-impact "
  "AI include human oversight and intervention capability; Google's agent designs (e.g., Project "
  "Mariner) likewise ask before sensitive actions.\n" + SRC_M2521 + "\n" + SRC_GEMINI),

 # --- Trends depth (N7-N12, all [flex]) ---
 ("What 'Agentic AI' Actually Means",
  ["Workflows: models orchestrated along predefined code paths",
   "Agents: models that dynamically direct their own process and tool use",
   "Start with the simplest pattern that works — often one good prompt plus retrieval",
   "Composable patterns: chaining, routing, parallelization, orchestrator-workers",
   "Full agents pay off only when flexibility is needed at scale"],
  "[flex] Anthropic's taxonomy is the reference definition as of mid-2026. Connect back to Lab "
  "7.3: the capstone agent sits at the far end of this ladder, and most real needs are met "
  "earlier — the same 'start simple' message as the 90-day roadmap.\n" + SRC_ANTHROPIC),
 ("Reasoning Models: AI That Thinks Before It Answers",
  ["Trained to think longer before responding — more thinking, better answers",
   "Test-time compute: inference effort scales quality on hard problems",
   "Reasoning models can use tools agentically: web, Python, image analysis",
   "'Thinking with images': visual input inside the chain of thought",
   "The reasoning-effort dial trades cost against quality — budget accordingly"],
  "[flex] For a non-specialist audience: these models spend more compute at answer time instead "
  "of only at training time. OpenAI reported o3 made 20% fewer major errors than o1 on hard "
  "real-world tasks per external experts. Lab tie: the reasoning-model rung of the Lab 4.1 "
  "prompt ladder.\n" + SRC_O3),
 ("Multimodal AI: One Model for Text, Image, Audio, Video",
  ["Natively multimodal input and output are now standard at the frontier",
   "Gemini 2.0: text, image, video, audio in; image and speech out",
   "Agent prototypes act in the world — a browser agent scored 83.5% on WebVoyager",
   "Government uses: form processing, map and diagram reading, accessibility"],
  "[flex] Named, dated exemplar: Google's Gemini 2.0 launch (December 2024) framed the 'agentic "
  "era.' Government relevance is practical: digitized forms, geospatial imagery, and Section 508 "
  "accessibility work are all multimodal problems.\n" + SRC_GEMINI),
 ("Open-Weight and On-Prem AI for Sensitive Environments",
  ["Open-weight models you can download and run inside your own boundary",
   "gpt-oss-120b: near-parity reasoning on a single 80 GB GPU (Apache 2.0)",
   "gpt-oss-20b: runs on edge devices with 16 GB of memory",
   "Full chain-of-thought access and adjustable reasoning effort",
   "Federal exemplar: DOI pairs FedRAMP cloud with on-prem HPC for sensitive work"],
  "[flex] The data-sovereignty trend that matters most to agencies: capable open-weight models "
  "(OpenAI's gpt-oss, August 2025) make on-prem deployment realistic. DOI's strategy is the "
  "public federal pattern — FedRAMP-authorized commercial cloud plus on-prem/HPC for sensitive "
  "workloads.\n" + SRC_GPTOSS + "\n" + SRC_DOI),
 ("2026 by the Numbers: Adoption, Capability, Cost, Energy",
  ["88% of organizations report using AI (AI Index, April 2026)",
   "SWE-bench Verified coding scores rose from 60% to near 100% in one year",
   "US–China top-model gap effectively closed — 2.7% as of March 2026",
   "AI data-center power capacity reached 29.6 GW — New York State peak scale",
   "Capability is accelerating; so are resource and governance demands"],
  "[flex] Balances the hype: capability is still compounding AND the resource/governance bill is "
  "arriving (energy, workforce disruption). Useful when leadership asks 'are we behind?'\n"
  + SRC_AIINDEX + "\n" + SRC_AIINDEX12),
 ("What Gartner Tells CIOs for 2026",
  ["Ten strategic trends in three buckets: platforms, orchestration, trust",
   "Multiagent systems: cooperating agents, not one monolith",
   "Domain-specific language models: accuracy on agency-specific tasks",
   "AI security platforms: defenses for prompt injection and data leakage",
   "Digital provenance: knowing whether content is AI-generated"],
  "[flex] This is the vocabulary attendees' CIOs will bring back from conferences (presented at "
  "Gartner IT Symposium/Xpo, October 2025). Spotlight the four most government-relevant trends "
  "and map each to a course chapter.\n" + SRC_GARTNER),

 # --- P10 re-score walkthrough (N13-N17) ---
 ("The Prompting Spine: P0 to P10",
  ["On Day 1 you wrote P0 — a first attempt at a real work prompt, sealed",
   "Since then: the prompt ladder, the rubric, RAG, and agents",
   "P10 is that same task, rewritten with everything you now know",
   "Next: unseal P0 and measure how far you have come"],
  "Interactive segment. Instructor: have the sealed P0 cards ready before this chapter. The "
  "ritual only works if P0 is genuinely untouched — no peeking since Day 1."),
 ("Unseal Your P0: The Before Picture",
  ["Open your sealed P0 card from Day 1 — do not edit it yet",
   "Re-read the task and your original prompt exactly as written",
   "Run it once more, as-is, in your approved assistant",
   "Score that output against the rubric; write the score on the card"],
  "Give 5 quiet minutes. Remind: public or synthetic inputs only — the P0 task was written to be "
  "safe for the class assistant. The baseline score goes on the card in ink."),
 ("Rewrite P0 with the Prompt Ladder",
  ["Zero-shot: restate the task, the audience, and the constraints plainly",
   "Few-shot: add two examples of the output style you want",
   "Role + format contract: 'You are a policy analyst; answer as a 5-row table'",
   "Hard subtask? Compare a reasoning model against the standard model",
   "The rewritten prompt is your P10"],
  "Same ladder as Lab 4.1 (Workbook). Circulate and coach: most quality comes from the role + "
  "format contract rung for government writing tasks."),
 ("Score Both Against the Rubric",
  ["Rubric, 1-5 each: accuracy, completeness, format adherence, tone",
   "Score the P0 output and the P10 output side by side",
   "Compute the delta — that number is your course ROI in miniature",
   "Post your before/after scores on the class whiteboard"],
  "Same rubric as Labs 3.1/4.1, now 1-5. The whiteboard histogram of deltas is the emotional "
  "peak of Day 3 — leave time for it."),
 ("Debrief: What the Delta Teaches",
  ["Which rung of the ladder bought the most quality for your task?",
   "Where did the model stay confidently wrong despite better prompts?",
   "When would you stop iterating and switch to RAG or a deterministic tool?",
   "Take P10 home: repeat the ritual on one real task within 30 days"],
  "Debrief prompts. Land the last bullet hard — the 30-day repetition is the bridge to the "
  "90-day roadmap that follows."),

 # --- 90-day roadmap worked template (N18-N25) ---
 ("Your Policy Landscape: OMB M-25-21 in One Slide",
  ["Your agency has a Chief AI Officer; a governance board oversees AI use",
   "High-impact AI carries mandatory minimum risk-management practices",
   "Agencies publish a public AI use-case inventory every year",
   "A generative-AI acceptable-use policy is required — the class rule mirrors it",
   "Compliance plans refresh every two years through 2036"],
  "M-25-21 (April 3, 2025) rescinded and replaced M-24-10; it is the operative instrument as of "
  "mid-2026. 'High-impact' = AI whose output is a principal basis for decisions with legal, "
  "material, binding, or significant effect on rights or safety.\n" + SRC_M2521),
 ("Who Does What: Your Agency's AI Governance Cast",
  ["Chief AI Officer (CAIO): accountable for the agency's AI program",
   "AI Governance Board: the senior body that approves and oversees AI use",
   "Chief Data Officer: data quality, access, and stewardship",
   "You: the informed user who spots use cases and flags risks"],
  "Names matter when attendees go home: the first roadmap step for many is simply finding out "
  "who their CAIO is. M-25-21 required CAIO designation and governance boards (CFO Act "
  "agencies); GSA's public plan shows the pattern in practice.\n" + SRC_M2521 + "\n" + SRC_GSA),
 ("Steal This Strategy: GSA's Three-Tier AI Adoption Model",
  ["Tier 1: an enterprise chatbot for all staff — culture and productivity first",
   "Tier 2: API integrations and agentic 'co-pilots' inside workflows",
   "Tier 3: embedded, high-impact uses with heightened oversight",
   "A shared platform (USAi) and fast FedRAMP '20x' authorization lower the barrier",
   "Governance scales with risk: a board plus an AI oversight committee"],
  "GSA's public M-25-21 strategy (September 2025) is the worked exemplar: Tier 1 chatbot via "
  "USAi, Tier 2 API/agentic integrations, Tier 3 embedded high-impact such as Login.gov face "
  "matching. Attendees can copy the tier skeleton directly into their 90-day plan.\n" + SRC_GSA),
 ("Evaluate Against a Rubric: NIST AI RMF + GenAI Profile",
  ["The AI Risk Management Framework is the federal reference for trustworthy AI",
   "Four functions: Govern, Map, Measure, Manage",
   "The GenAI Profile enumerates generative risks: confabulation, privacy, integrity",
   "Free companions: AI RMF Playbook, Crosswalk, and Resource Center",
   "The AI RMF is under revision — check for updates (as of August 2026)"],
  "This is the 'evaluate against a rubric; document risks and guardrails' instrument for weeks "
  "9-12 of the roadmap. AI RMF 1.0 (January 2023) plus the GenAI Profile NIST-AI-600-1 (July "
  "2024); revision status date-stamped.\n" + SRC_NIST),
 ("The 90-Day Roadmap as a 30/60/90 Template",
  ["Days 1-30: pick one low-risk use case; confirm data, rules, and sponsor",
   "Days 31-60: prototype with prompting or RAG; human in the loop throughout",
   "Days 61-90: evaluate, document risks and guardrails, brief leadership",
   "Skeleton: GSA's tiers — start at Tier 1, earn your way toward Tier 3",
   "Anchors: your AUP, the use-case inventory, high-impact practices (M-25-21)"],
  "The template slide: the next three slides walk each 30-day block, and the classic action "
  "slide after them is the one to photograph. Everything traces to two public anchors: GSA's "
  "tiered model and M-25-21's duties.\n" + SRC_GSA + "\n" + SRC_M2521),
 ("Days 1-30: Pick the Right First Use Case",
  ["High value, low risk: internal productivity before public-facing decisions",
   "Confirm the data exists, is usable, and is approved for AI use",
   "Read your agency's AI acceptable-use policy before touching a tool",
   "Line up a sponsor and one measurable definition of success",
   "Check whether your idea already sits in the agency use-case inventory"],
  "Coaching points: the best first pilots are boring — summarization, drafting, search over "
  "public documents. The use-case inventory check avoids duplicating a sibling office's work.\n"
  + SRC_M2521 + "\n" + SRC_GSA),
 ("Days 31-60: Prototype with Guardrails",
  ["Prototype with prompting first; add RAG when answers need your documents",
   "Keep a human reviewing every output that leaves your desk",
   "Log what you tried: prompts, models, and failure modes",
   "Watch for the high-impact trigger: legal or material effects on the public",
   "If it triggers, pause and engage your CAIO and governance board"],
  "The 'start with the simplest pattern' advice from Anthropic's agent guidance, applied to a "
  "federal pilot. The high-impact determination is an M-25-21 duty, not a judgment call to "
  "defer.\n" + SRC_ANTHROPIC + "\n" + SRC_M2521),
 ("Days 61-90: Evaluate, Document, Brief",
  ["Evaluate outputs against your rubric — accuracy, completeness, format, tone",
   "Document risks and guardrails using the NIST AI RMF as your checklist",
   "Write the one-page brief: value, cost, risks, and the next decision",
   "Deliver it to your manager; ask what would justify scaling",
   "Success is a trusted, documented pilot — not a production launch"],
  "Same rubric the class used all week — evaluation is a habit, not a phase. The brief format "
  "mirrors what governance boards ask for.\n" + SRC_NIST + "\n" + SRC_GSA),

 # --- Role-based next steps (N26-N28) ---
 ("Next Steps if You Are a Manager",
  ["Read your agency's AI strategy and acceptable-use policy this month",
   "Approve one Tier 1-style pilot from the 30/60/90 template",
   "Ask every AI proposal three questions: data? oversight? measure of success?",
   "Protect training time — AI skills are a workforce investment"],
  "Managers set the demand signal. The AI Training Act (Pub. L. 117-207) is the statutory hook "
  "for the last bullet; GSA runs its government-wide AI Training Series under it.\n" + SRC_GSA
  + "\n" + SRC_M2521),
 ("Next Steps if You Are an Analyst",
  ["Repeat the P0-to-P10 ritual on one real recurring task within 30 days",
   "Build a personal prompt library with rubric scores attached",
   "Ground every ask in your source documents, RAG-style",
   "Volunteer your best before/after as a demo for your team"],
  "Analysts convert the course into habit. The demo suggestion copies GSA's 'Friday Demo Days' "
  "pattern — show, don't tell.\n" + SRC_GSA),
 ("Next Steps if You Are in IT Operations",
  ["Inventory shadow AI: find what staff use, then offer approved alternatives",
   "Know your boundary options: FedRAMP-authorized cloud vs. open-weight on-prem",
   "Plan for AI security: prompt injection, data leakage, provenance checks",
   "Watch capacity and cost: reasoning and agentic workloads add usage fast"],
  "IT ops owns the supply side: approved tools, boundaries, and monitoring. Boundary options per "
  "gpt-oss/DOI; the AI-security and provenance agenda per Gartner's 2026 trends.\n" + SRC_GPTOSS
  + "\n" + SRC_DOI + "\n" + SRC_GARTNER),

 # --- Resources (N29-N30) ---
 ("Keep Learning: The Federal AI Training Ecosystem",
  ["GSA's government-wide AI Training Series: technical, acquisition, leadership tracks",
   "Established under the AI Training Act (Pub. L. 117-207)",
   "GSA's AI Community of Practice offers peer support across agencies",
   "Start locally: a 'Friday Demo Days' pattern costs nothing to copy"],
  "Replaces the unverifiable 'AI for Governance Summit' with communities that exist and are "
  "official. All are free and government-wide.\n" + SRC_GSA),
 ("Policy and Guidance to Bookmark",
  ["OMB M-25-21: the operative federal AI policy — replaced M-24-10 (April 2025)",
   "NIST AI RMF and GenAI Profile: the risk vocabulary your leadership uses",
   "GSA's AI Guide for Government: a chaptered 'where to start' reference",
   "Your agency's own AI strategy and use-case inventory — required and public"],
  "The take-home bookmark list. Every item is public; the last one is the most useful and the "
  "least read.\n" + SRC_M2521 + "\n" + SRC_NIST + "\n" + SRC_GSA_GUIDE),

 # --- Course glossary (N31-N38, reference slides) ---
 ("Course Glossary (1 of 8): A",
  ["Acceptable-use policy (AUP): your agency's rules for what AI tools and data are allowed",
   "Agent: a model that dynamically directs its own process and tool use",
   "Agentic workflow: a model orchestrated along a predefined code path",
   "AI use-case inventory: your agency's annual public list of AI systems in use"],
  "Reference slide — for look-up after class, not presented linearly."),
 ("Course Glossary (2 of 8): C-F",
  ["Chain-of-thought: the model's step-by-step working before its answer",
   "Chief AI Officer (CAIO): the official accountable for your agency's AI program",
   "Embeddings: numeric vectors that let machines compare text by meaning",
   "FedRAMP: the federal authorization program for cloud service security"],
  "Reference slide — for look-up after class, not presented linearly."),
 ("Course Glossary (3 of 8): F-H",
  ["Few-shot prompting: giving the model examples of the output you want",
   "Fine-tuning: further training a model on your own data",
   "Generative AI: models that create text, images, audio, or video",
   "Hallucination (confabulation): fluent output that is factually wrong"],
  "Reference slide — for look-up after class, not presented linearly."),
 ("Course Glossary (4 of 8): H-M",
  ["High-impact AI (M-25-21): AI whose output principally drives consequential decisions",
   "Human-in-the-loop: a person reviews or approves before the output is used",
   "Large language model (LLM): a model trained to predict and generate text",
   "Multimodal model: one model handling text, image, audio, and video"],
  "Reference slide — for look-up after class, not presented linearly."),
 ("Course Glossary (5 of 8): M-P",
  ["OMB M-25-21: the operative federal policy on agency AI use (April 2025)",
   "Open-weight model: a downloadable model you can run on your own infrastructure",
   "Prompt: the instruction and context you give a model",
   "Prompt injection: hostile text that tries to hijack a model's instructions"],
  "Reference slide — for look-up after class, not presented linearly."),
 ("Course Glossary (6 of 8): R-S",
  ["RAG (retrieval-augmented generation): answers grounded in your documents",
   "Reasoning model: a model trained to think longer before answering",
   "Rubric: scored criteria — accuracy, completeness, format, tone",
   "Shadow AI: staff using unapproved AI tools outside IT's visibility"],
  "Reference slide — for look-up after class, not presented linearly."),
 ("Course Glossary (7 of 8): T-Z",
  ["Temperature: a dial controlling how predictable or varied output is",
   "Token: the chunk of text a model reads or writes at a time",
   "Workflow vs. agent: predefined path vs. model-directed process",
   "Zero-shot prompting: asking with no examples — the ladder's first rung"],
  "Reference slide — for look-up after class, not presented linearly."),
 ("Course Glossary (8 of 8): Frameworks",
  ["NIST AI RMF: the federal voluntary framework for trustworthy AI",
   "Explainable AI (XAI): techniques that make model decisions interpretable",
   "Data minimization: give the model only the data the task requires",
   "Digital provenance: evidence of whether content is AI-generated"],
  "Reference slide — for look-up after class, not presented linearly."),

 # --- Closing (N39) ---
 ("Thank You — and Your Course Evaluation",
  ["Thank you for three days of hard, hands-on work",
   "Your evaluation shapes the next revision — please complete it today",
   "Take with you: your P10, the 30/60/90 template, and the bookmark list",
   "Stay connected through your agency's AI community and the federal training series"],
  "Instructor: point to the evaluation form/link before anyone packs up. If the class whiteboard "
  "will be exported, say how attendees will receive it."),
]
