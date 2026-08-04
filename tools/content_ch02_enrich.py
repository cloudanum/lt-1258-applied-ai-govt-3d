"""New slides for the Ch02 enrichment pass (gov-platforms block + deepened
PredPol cautionary slide + Data.gov-2026 slide). Every factual claim traces to
1258/research/refs-ch02-gov-apps-platforms.md (URLs verified live 2026-08-01).
"""

VER = "(verified 2026-08-01)"

# Rebuilt PredPol cautionary slide (replaces the appended end-of-deck one and
# moves into the public-safety block). Deepened per refs: Lum & Isaac audit,
# LAPD OIG 2019, The Markup, Geolitica shutdown.
PREDPOL = (
 "Predictive Policing: A Cautionary Case Study",
 ["PredPol (renamed Geolitica in 2021) promised to forecast crime hotspots",
  "Academic audit (Lum & Isaac, 2016): predictions targeted Black residents ~2x more",
  "Feedback loop: predictions sent patrols back — predicting policing, not crime",
  "LAPD's inspector general (2019) could not confirm crime reduction; LAPD dropped it in 2020",
  "The Markup: under 0.5% of 23,631 Plainfield, NJ predictions matched reported crimes",
  "Geolitica shut down in 2023 — prediction on people demands fairness review and audit"],
 "Replaces the 3 uncritical PredPol slides (old s37-39) with one cautionary slide; moved here into the "
 "public-safety block where it belongs pedagogically.\n"
 "Four evidence legs to teach: (1) Lum & Isaac's Oakland audit found ~2x targeting disparity plus a "
 "self-reinforcing patrol feedback loop; (2) LAPD OIG's March 2019 review of data-driven policing found "
 "effectiveness unclear, and LAPD — the earliest adopter — dropped PredPol in 2020; (3) The Markup's "
 "analysis of 23,631 Geolitica predictions for Plainfield, NJ found fewer than 100 (<0.5%) matched "
 "later-reported crimes; (4) Geolitica ceased operations at the end of 2023, with its technology absorbed "
 "into SoundThinking's ResourceRouter — 'renamed, not gone.'\n"
 "Lesson pipeline: prediction on people -> fairness review -> independent audit -> willingness to kill "
 "the program.\n"
 "Source: The Markup — Predictive Policing Software Terrible at Predicting Crimes, "
 "https://themarkup.org/prediction-bias/2023/10/02/predictive-policing-software-terrible-at-predicting-crimes "
 f"{VER}\n"
 "Source: AMS Feature Column — Quantifying Injustice (on Lum & Isaac, Significance 2016), "
 f"https://mathvoices.ams.org/featurecolumn/2020/07/01/fc-2020-07/ {VER}\n"
 "Source: LAPD Office of the Inspector General — Significant Reports (March 12, 2019 review), "
 f"https://www.oig.lacity.org/significant-reports {VER}\n"
 "Source: WIRED — SoundThinking buys parts of PredPol creator Geolitica, "
 f"https://www.wired.com/story/soundthinking-geolitica-acquisition-predictive-policing/ {VER}"
)

# Gov-platforms block, inserted after the process-automation block (old s24)
# and before the public-datasets section divider (old s25).
PLATFORM_SLIDES = [
 ("Government AI Platforms in 2026",
  ["Federal agencies now run shared, sanctioned AI platforms staff can actually use",
   "DoD: GenAI.mil — a department-wide generative-AI platform launched December 2025",
   "Civilian: USAi.gov — GSA's shared AI suite, free to federal agencies",
   "Buying: GSA OneGov agreements set government-wide terms, some at $1 per agency",
   "Accountability: public AI use-case inventories show what each agency actually runs"],
  "Block opener. The chapter taught application areas; this block names the platforms government staff "
  "will actually touch in 2026. All entries verified against primary sources on 2026-08-01. Naming note: "
  "current official DoD releases use 'Department of War' (war.gov); the deck keeps DoD/Pentagon wording "
  "for familiarity — direct quotes must preserve the source's wording."),
 ("GenAI.mil: DoD's Enterprise GenAI Platform",
  ["Launched December 9, 2025 as the Department's bespoke AI platform",
   "First hosted frontier model: Google Cloud's Gemini for Government, more followed",
   "Certified for Controlled Unclassified Information (CUI) at Impact Level 5 (IL5)",
   "Includes retrieval (RAG) and web-grounding against Google Search",
   "Free training offered to all department personnel"],
  "This is the correct, current name and status: GenAI.mil is real, live, and DoD-wide as of August 2026.\n"
  "Source: U.S. Department of War — The War Department Unleashes AI on New GenAI.mil Platform, "
  "https://www.war.gov/News/Releases/Release/Article/4354916/the-war-department-unleashes-ai-on-new-genaimil-platform/ "
  f"{VER}"),
 ("GenAI.mil at Scale (as of mid-2026)",
  ["~1.7 million users and 100,000+ custom agents built by users (July 2026)",
   "Hosts models from OpenAI, Google, xAI, NVIDIA, Microsoft, Oracle, and AWS",
   "ChatGPT became CUI-eligible on the platform in July 2026",
   "Expansion to higher classification levels (IL6/IL7) is planned",
   "Takeaway: a sanctioned platform with a user agent-builder is now a real pattern"],
  "[flex] Depth slide — skip if the room is civilian-heavy and short on time. Figures are per DoD CDAO "
  "Cameron Stanley at the AWS Summit, June 2026. The 100,000+ user-built agents figure is the verifiable "
  "reality behind second-hand rumors of an 'agent designer' platform — do not use that name.\n"
  "Source: Nextgov/FCW — GenAI.mil records almost 1.7M users, plans new model additions, "
  f"https://www.nextgov.com/artificial-intelligence/2026/07/genaimil-records-almost-17m-users-plans-new-model-additions/414568/ {VER}"),
 ("Maven Smart System: AI at Operational Scale",
  ["Grew from 2017 Project Maven imagery AI into a fused command-and-control platform",
   "Used by combatant commands in live operations",
   "$795M software-license modification announced May 2025, running through May 2029",
   "March 2026 memo: transition to a formal program of record by September 30, 2026",
   "Oversight moves from NGA to a CDAO Maven Smart System Program Office"],
  "For balance, note the public transparency/oversight debate that accompanied Maven's expansion; a "
  "program-of-record transition brings standard acquisition oversight. Correct current name: Maven Smart "
  "System (not 'Palantir Maven').\n"
  "Source: DefenseScoop — Palantir's Maven Smart System to become Pentagon program of record, "
  f"https://defensescoop.com/2026/04/15/palantir-maven-smart-system-pentagon-program-transition-feinberg/ {VER}\n"
  "Source: U.S. Department of War — DoD Contracts for May 21, 2025 ($795M Maven Smart System modification), "
  f"https://www.war.gov/News/Contracts/Contract/Article/4194643/ {VER}"),
 ("Agents in Government: The Real Programs",
  ["January 2026 AI Acceleration Strategy names seven 'Pace-Setting Projects'",
   "Agent Network: AI agents for battle management and decision support",
   "Enterprise Agents: a playbook for secure agents in enterprise workflows",
   "GenAI.mil's custom-agent builder is where most staff will meet agents",
   "Hype check: these are the fielded program names — not rumored platforms"],
  "[flex] Depth slide. Frames agent hype against what is actually fielded. Teach these authoritative "
  "names; nothing real matches second-hand names like 'agent designer'.\n"
  "Source: U.S. Department of War — War Department Launches AI Acceleration Strategy, "
  "https://www.war.gov/News/Releases/Release/Article/4376420/war-department-launches-ai-acceleration-strategy-to-secure-american-military-ai/ "
  f"{VER}"),
 ("USAi.gov: The Civilian Government AI Suite",
  ["GSA's shared AI platform, free to federal agencies",
   "Chat: a multi-model assistant for everyday work",
   "Unified API to OpenAI, Google, and Anthropic models",
   "Console: agency usage metrics and model evaluations",
   "Civilian counterpart to DoD's GenAI.mil — check your agency's access"],
  "FedRAMP-oriented security posture. A hands-on candidate for the course toolkit; instructors can demo "
  "Chat live if the room has access.\n"
  "Source: U.S. General Services Administration — USAi.gov, https://www.usai.gov/ " f"{VER}"),
 ("How Agencies Buy AI in 2026: GSA OneGov",
  ["OneGov: government-wide AI agreements negotiated by GSA (as of mid-2026)",
   "Claude Enterprise $1 and ChatGPT Enterprise $1 per agency (through Aug 2026)",
   "Gemini for Government $0.47; Perplexity $0.25; Grok $0.42 per agency",
   "FedRAMP authorization required; reuse existing ATOs where possible",
   "Involve your CIO, CAIO, CDO, CISO, and privacy officer early"],
  "Practical procurement literacy: the '$1 deals' are real OneGov agreements with published end dates — "
  "check the GSA Buy AI page for the current table before quoting prices in class.\n"
  "Source: U.S. General Services Administration — Buy AI (OneGov agreements and AI procurement guidance), "
  f"https://www.gsa.gov/artificial-intelligence/buy-ai {VER}"),
 ("What Is Your Agency Doing? AI Use-Case Inventories",
  ["OMB M-25-21 requires agencies to publish annual AI use-case inventories",
   "The authoritative answer to 'what is agency X actually doing with AI'",
   "'High-impact AI' (rights, safety, critical infrastructure) needs risk practices first",
   "Example: the DHS inventory covers FEMA, TSA, USCIS, and CISA use cases",
   "GAO tracks compliance; ~1,200 use cases were cataloged across 20 agencies in FY2022"],
  "Exercise: have students look up their own agency's inventory. GAO's baseline review covered 20 of 23 "
  "CFO Act agencies and issued 35 recommendations; its live page now tracks agency M-25-21 compliance "
  "into 2026.\n"
  "Source: U.S. Department of Homeland Security — AI Use Case Inventory, "
  f"https://www.dhs.gov/ai/use-case-inventory {VER}\n"
  "Source: U.S. GAO — Artificial Intelligence: Agencies Have Begun Implementation but Need to Complete "
  f"Key Requirements (GAO-24-105980), https://www.gao.gov/products/gao-24-105980 {VER}"),
]

# Cyber-block enrichment: the real federal AI service, placed after the
# real-time threat detection slide (old s14).
CISA_SLIDE = (
 "CISA Malware Next-Gen: Federal AI You Can Use",
 ["CISA's automated malware-analysis service — in government use since November 2023",
  "Opened to any organization or individual in April 2024 via login.gov",
  "Static and dynamic analysis; results delivered as PDF and STIX 2.1",
  "Pilot: about 200 of 1,600 submissions confirmed suspicious or malicious",
  "A complement to commercial tools, not a replacement"],
 "[flex] Depth slide. A real, current federal AI-in-cyber-defense service the audience can actually use — "
 "stronger than vendor case studies. CISA's own announcement page has moved; the trade press quotes it "
 "in full.\n"
 "Source: BleepingComputer — CISA makes its Malware Next-Gen analysis system publicly available, "
 "https://www.bleepingcomputer.com/news/security/cisa-makes-its-malware-next-gen-analysis-system-publicly-available/ "
 f"{VER}"
)

# Data.gov enrichment, placed after the corrected Data.gov portal slide (old s30).
DATAGOV_SLIDE = (
 "Data.gov in 2026: Rebuilt and Bigger",
 ["548,327 datasets as of August 2026 — up from ~300,000 in older course material",
  "120+ publishers: federal, state, local, tribal, and university organizations",
  "New custom catalog replaced the legacy CKAN system in 2025",
  "Legacy CKAN catalog runs at catalog-old.data.gov only through fall 2026",
  "Programmatic access: DCAT/data.json harvest feeds, not the old CKAN API"],
 "[flex] Depth slide. The production catalog is now a custom Python/Flask + OpenSearch application; the "
 "CKAN Action API no longer exists at catalog.data.gov. AUTHOR FLAG: Lab 2.1's verification steps must be "
 "re-checked against the new catalog UI and feeds before the next delivery.\n"
 "Source: GSA / Data.gov — catalog.data.gov homepage (548,327 datasets), https://catalog.data.gov/ " f"{VER}\n"
 "Source: GSA data.gov team — catalog.data.gov architecture wiki, "
 f"https://github.com/GSA/data.gov/wiki/catalog.data.gov {VER}"
)
