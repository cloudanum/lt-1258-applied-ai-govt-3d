#!/usr/bin/env python3
"""build_notes_ch02.py — delivery-notes rewrite for 1258-Ch02-Applications-Public-Data.pptx (51 slides).

Idempotent: restores the deck from decks/_bak7/, rebuilds every note as
SAY/ASK hook + KEY POINT + time cue + TRANSITION, and re-appends preserved
markers ([flex], Source lines, spine rungs, author/IG flags) extracted
verbatim from the backup notes. Slide text/layouts/counts are untouched.

Run: ../../.venv-courseware/bin/python tools/build_notes_ch02.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from notes_common import apply_notes, verify

TAG = "Ch02-Applications-Public-Data"
COUNT = 51

FLEX_CORE = {
    17: "CISA Malware Next-Gen is a real federal AI service anyone can use via login.gov — static/dynamic analysis, PDF + STIX 2.1 results",
    28: "~1.7M users and 100,000+ user-built agents — the agent-builder pattern on GenAI.mil is real and verifiable",
    30: "the fielded agent programs are Agent Network, Enterprise Agents, and GenAI.mil's builder — not rumored platform names",
    40: "data.gov's catalog was rebuilt in 2025 — use the DCAT/data.json feeds, not the retired CKAN API",
}

NOTES = {
1: """SAY: "This afternoon: what the government is actually doing with AI — the running systems, the cautionary tales, and the platforms you can use yourself."
KEY POINT: Chapter 2 surveys verified federal AI applications and their impacts, teaches you to find and assess public datasets, and shows you how to read agency use-case inventories.
FLEX VALVE: this chapter runs to the end of Day 1 — if we fall behind, the [flex] slides are the valve; I skip them first.
(~2 min)
TRANSITION: The four objectives.""",
2: """ASK: "By the end of today, would you rather know what AI your agency runs — or where to find the data to build with? You'll have both."
KEY POINT: Objectives: survey verified applications and operational impacts; use the government's own platforms — GenAI.mil, Maven Smart System, GSA OneGov; find and assess datasets on data.gov and other portals; read agency use-case inventories.
(~2 min)
TRANSITION: The chapter's route.""",
3: """SAY: "Health, cyber defense, infrastructure, public safety, automation — five domains, then the cases where it went wrong, then the platforms."
KEY POINT: The arc: why governments need AI, five application domains, cautionary cases, 2026 government platforms, use-case inventories, and public data — with Demo 2.1, DO NOWs 2.A-2.D, and Lab 2.1.
(~2 min)
TRANSITION: The activity budget.""",
4: """ASK: "How much of this afternoon is hands-on? Seventy minutes — including a dataset you'll still be using on Day 3."
KEY POINT: One demo, four DO NOWs, and the 30-minute Public Data Expedition; full instructions in the Lab Manual; DO NOW 2.B is the [flex] item.
(~2 min — walk the list; these times are the chapter's budget)
TRANSITION: Start with the why.""",
5: """SAY: "Citizens get 24/7 service from their bank's app — they now expect the same from their government."
KEY POINT: Citizen demands evolve fast; AI enables predictive capabilities, real-time decision-making, and optimized resource allocation — the outcome is bureaucracy transformed into streamlined, citizen-focused administration.
(~2 min)
TRANSITION: What those expectations look like up close.""",
6: """SAY: "24/7 answers, streamlined processes, tailored services — the private sector set the bar, and citizens now expect it everywhere."
KEY POINT: AI meets rising expectations three ways: chatbots and virtual assistants around the clock, automation of routine tasks so staff focus on complex work, and personalized, proactive support.
(~1 min)
TRANSITION: The harder problems AI tackles.""",
7: """SAY: "Climate, pandemics, economic instability, cyber threats — the hard problems are all data problems at scale."
KEY POINT: AI analyzes vast data to find patterns, builds predictive models so agencies act proactively rather than reactively, and optimizes where resources and services go.
(~2 min)
TRANSITION: And the payoff when agencies adopt.""",
8: """ASK: "What does AI adoption actually buy a federal agency? GAO counted about 1,200 use cases across 20 agencies — back in FY2022."
KEY POINT: Adoption fosters innovation: automating routine work, enabling new service-delivery approaches, and promoting experimentation and learning — GAO's baseline review cataloged ~1,200 use cases across 20 of 23 CFO Act agencies even in FY2022.
(~2 min)
TRANSITION: Domain one: health.""",
9: """SAY: "An algorithm reads a retinal scan and catches diabetic eye disease at ~90% sensitivity and ~98% specificity — validated and published in JAMA."
KEY POINT: Health AI that holds up: validated diagnostics (Gulshan et al., JAMA 2016), faster medical-imaging reads, outbreak monitoring that integrates EHR, climate, and social data, and predictive resource allocation during crises.
(~2 min)
TRANSITION: How public-health agencies put that to work.""",
10: """ASK: "Where would you spot the next outbreak first — in a headline, or in millions of clinical notes?"
KEY POINT: CDC applies AI and NLP across surveillance, diagnostics, forecasting, and outbreak management — with NCEZID, CSELS, and the Center for Forecasting and Outbreak Analytics among the divisions exploring uses.
(~2 min)
TRANSITION: Clustering does similar duty in healthcare.""",
11: """SAY: "Same K-Means you ran this morning, aimed at outbreaks, opioid clusters, and underserved populations."
KEY POINT: Clustering in healthcare: mapping pandemic hotspots for quarantine planning, pinpointing opioid-misuse clusters for focused intervention, and segmenting populations for equitable, targeted care.
(~1 min)
TRANSITION: NLP at national scale.""",
12: """ASK: "How do you find every cancer case in a mountain of pathology reports? The CDC's answer is NLP."
KEY POINT: CDC uses NLP to process clinical notes and unstructured medical data — earlier outbreak detection, faster containment, better public-health monitoring; the slide's references cover the cancer-surveillance program and the CDC/FDA NLP web service.
(~2 min)
TRANSITION: Diagnostics, where regulation does the scaling.""",
13: """SAY: "Want to know where medical AI actually works? Don't trust vendor stats — read the FDA's authorization list."
KEY POINT: Hundreds of AI-enabled medical devices are FDA-authorized for US marketing — radiology leads, cardiology and neurology next, each entry dated with submission number and manufacturer; regulation is the scaling mechanism, so cite the list rather than accuracy claims.
(~2 min)
TRANSITION: Domain two: cyber defense.""",
14: """ASK: "Ransomware moves in minutes — who on your team is awake and watching at machine speed?"
KEY POINT: AI shifts cybersecurity from reactive to proactive: continuous monitoring of network traffic for anomalies, zero-day pattern recognition across systems, and automated incident response via SOAR platforms.
(~2 min)
TRANSITION: Protection before, and recovery after.""",
15: """SAY: "The same behavioral analytics that recommend your next purchase can flag the insider downloading files they shouldn't."
KEY POINT: AI secures sensitive data with encryption and behavioral analytics — UEBA tools flag anomalous access patterns — and accelerates post-attack recovery by identifying vulnerabilities and restoring from secured backups.
(~1 min)
TRANSITION: A federal example you can point to.""",
16: """SAY: "Of the first 1,600 files submitted to CISA's automated malware service, about 200 came back malicious — that's the detection ratio in production."
KEY POINT: Continuous monitoring spots phishing, malware, and ransomware and acts instantly — blocking suspicious email, isolating infected machines; the federal proof: CISA's Malware Next-Gen triaged 1,600 pilot submissions, about 200 confirmed suspicious or malicious.
(~2 min)
TRANSITION: The full CISA story — a service you can use.""",
17: """ASK: "Who in this room has ever submitted a suspicious file for analysis? After this slide, you know where."
KEY POINT: CISA's automated malware analysis: in government use since November 2023, open to any organization or individual via login.gov since April 2024, static and dynamic analysis with results as PDF and STIX 2.1 — a complement to commercial tools, not a replacement.
(~2 min if taught — a real federal AI service the audience can actually use)
TRANSITION: Domain three: the infrastructure under everything.""",
18: """SAY: "Pittsburgh gave traffic signals a brain and cut wait times ~40% — peer-reviewed, not a vendor brochure."
KEY POINT: Predictive maintenance anticipates failures in bridges, railways, and pipelines; Pittsburgh's SURTRAC adaptive signals cut waits ~40% and travel times ~25% in field tests (CMU, ICAPS 2013); the rail-maintenance figure is vendor-reported — label it that way if you cite it.
(~2 min)
TRANSITION: Disasters, where prediction buys time.""",
19: """ASK: "What would your agency do with twelve more hours of wildfire warning?"
KEY POINT: AI fuses weather patterns, infrastructure data, and population density to forecast disaster severity — enabling proactive planning and resource allocation, like predicting wildfire spread for timely evacuations.
(~1 min)
TRANSITION: Who's doing this in the federal family?""",
20: """SAY: "Don't take my word for what DHS runs in disaster response — the use-case inventory lists it, by name, in public."
KEY POINT: DHS components field AI for disaster response — FEMA, TSA, USCIS, CISA use cases are listed in the public DHS AI Use Case Inventory; the impact is faster aid deployment and better coordination.
(~2 min)
TRANSITION: Crisis management, minute by minute.""",
21: """ASK: "911 calls, social media, traffic sensors, hospital beds — in a crisis, who reads all four at once?"
KEY POINT: Emergency coordination fuses real-time sources: call content for type and severity, social posts for ground truth, traffic data for routing, hospital capacity for care — and AI triages incoming reports to route the right resource first; real federal cases live in the DHS inventory.
(~2 min)
TRANSITION: Now the cautionary case — when prediction went wrong.""",
22: """SAY: "23,631 crime predictions. Fewer than 100 matched a reported crime. This is what AI failure with a badge looks like."
KEY POINT: PredPol/Geolitica: Lum & Isaac's audit found ~2x targeting disparity plus a patrol feedback loop — predicting policing, not crime; LAPD's inspector general could not confirm crime reduction and LAPD dropped it in 2020; Geolitica shut down in 2023. The pipeline: prediction on people demands fairness review, independent audit, and willingness to kill the program.
(~3 min — this is the chapter's conscience; let it breathe)
TRANSITION: From a hard lesson to a useful tool: clustering for the environment.""",
23: """ASK: "Which neighborhoods share a disaster-risk profile? Cluster them, and FEMA knows where to pre-position."
KEY POINT: K-Means on historical disaster data, geographical features, and real-time sensor feeds identifies high-risk areas with similar profiles — proactive resource allocation that saves lives and minimizes damage.
(~1 min)
TRANSITION: Domain five: the back office.""",
24: """SAY: "The UK Home Office let an algorithm stream visa applications by nationality — a legal challenge shut it down in 2020."
KEY POINT: Document automation and RPA extract, summarize, and route at scale — but the UK visa-streaming case is the governance warning: automated triage of people needs bias review; it pairs with the PredPol lesson.
(~2 min)
TRANSITION: Now the model version of doing it right — USCIS.""",
25: """SAY: "USCIS built its GenAI assistant the way you'd want your agency to: private cloud, PII controls, and a human who must approve every output."
KEY POINT: PAiTH (Private AI Tech Hub) is USCIS's internal persona-based assistant — legal research, contracts, translation, developer, and security-compliance personas — deployed in a private cloud with data-sovereignty controls and mandatory human review before any official use. Teach it as a model deployment.
(~2 min)
TRANSITION: PAiTH is one platform — here is the 2026 platform landscape.""",
26: """ASK: "GenAI.mil, USAi.gov, OneGov — who has heard of at least one of these?"
KEY POINT: Agencies now run shared, sanctioned platforms staff can actually use: DoD's GenAI.mil (launched December 2025), GSA's USAi.gov for civilians, OneGov agreements for buying, and public inventories for accountability. Naming note: current official releases say 'Department of War' — the deck keeps DoD wording for familiarity; preserve source wording in direct quotes.
(~2 min)
TRANSITION: The biggest of them: GenAI.mil.""",
27: """SAY: "December 9, 2025: an entire department gets its own frontier-AI platform — certified for CUI at Impact Level 5."
KEY POINT: GenAI.mil is real, live, and DoD-wide: first hosted model is Google Cloud's Gemini for Government with more following, retrieval (RAG) and web-grounding built in, free training offered to all department personnel.
(~2 min)
TRANSITION: What scale looks like eight months in.""",
28: """ASK: "How many people use GenAI.mil? About 1.7 million — and they've built over 100,000 custom agents."
KEY POINT: Adoption at scale (figures per DoD CDAO Cameron Stanley at the AWS Summit, June 2026): models from OpenAI, Google, xAI, NVIDIA, Microsoft, Oracle, and AWS; ChatGPT became CUI-eligible in July 2026; IL6/IL7 expansion planned. The takeaway: a sanctioned platform with a user agent-builder is a real pattern — do not use rumored platform names.
(~2 min if taught — skip first if the room is civilian-heavy and short on time)
TRANSITION: From chat to operations: Maven.""",
29: """SAY: "From a 2017 imagery project to a formal program of record — Maven is what AI at operational scale looks like."
KEY POINT: Maven Smart System (the correct current name): grown into a fused command-and-control platform used by combatant commands in live operations; a $795M license modification runs through May 2029; the March 2026 memo transitions it to a program of record by September 30, 2026 — bringing standard acquisition oversight.
(~2 min)
TRANSITION: And the agent programs behind the headlines.""",
30: """SAY: "When you hear 'the Pentagon is building agents,' ask which program — there are real names, and this slide has them."
KEY POINT: The January 2026 AI Acceleration Strategy names seven Pace-Setting Projects: Agent Network (agents for battle management and decision support), Enterprise Agents (a playbook for secure enterprise workflows), and GenAI.mil's custom-agent builder — where most staff will meet agents. Teach these authoritative names.
(~2 min if taught)
TRANSITION: The civilian counterpart.""",
31: """ASK: "What's the civilian counterpart to GenAI.mil? GSA's answer is USAi.gov — free to federal agencies."
KEY POINT: USAi.gov: a multi-model Chat assistant for everyday work, one unified API across OpenAI, Google, and Anthropic models, and a console with agency usage metrics and model evaluations — check your agency's access. Instructors can demo Chat live if the room has access.
(~2 min)
TRANSITION: How agencies buy all this.""",
32: """SAY: "One dollar per agency — that's a real, published OneGov price, through August 2026."
KEY POINT: OneGov agreements set government-wide terms: Claude Enterprise and ChatGPT Enterprise at $1 per agency (through Aug 2026), Gemini for Government $0.47, Perplexity $0.25, Grok $0.42; FedRAMP authorization required, reuse existing ATOs, involve your CIO, CAIO, CDO, CISO, and privacy officer early. Check GSA's Buy AI page for the current table before quoting prices in class.
(~2 min)
TRANSITION: Buying is half the story — accountability is the other.""",
33: """ASK: "What's the authoritative answer to 'what is agency X doing with AI'? It's published. Every year. By law."
KEY POINT: OMB M-25-21 requires annual public use-case inventories; high-impact AI (rights, safety, critical infrastructure) needs risk practices first; the DHS inventory covers FEMA, TSA, USCIS, CISA; GAO tracks compliance — ~1,200 use cases across 20 agencies back in FY2022. Exercise: have students look up their own agency's inventory.
(~2 min)
TRANSITION: Now the raw material for everything you've seen: public data.""",
34: """SAY: "Every lab you'll run in this course starts here: a public dataset."
KEY POINT: Section shift — public datasets are the raw material for every lab in this course.
(~1 min)
TRANSITION: What counts as a public dataset.""",
35: """ASK: "Census records, weather observations, health trends — who paid for all that data? You did. That's why it's public."
KEY POINT: Public datasets are collections made freely available by governments, organizations, and institutions — numerical, textual, geospatial, categorical — delivered as CSV, API, or JSON for seamless integration.
(~2 min)
TRANSITION: Why they matter beyond convenience.""",
36: """SAY: "Open data is how a citizen checks the government's homework — and how a small team builds on a billion-dollar data collection."
KEY POINT: Three reasons public datasets matter: transparency and accountability, enabling innovation (AI models trained on climate data), and collaboration across borders on shared challenges.
(~1 min)
TRANSITION: The benefits, sector by sector.""",
37: """SAY: "Think of public data as infrastructure — like roads, everybody's work runs better on it."
KEY POINT: Benefits: citizens analyze spending, crime, and welfare statistics; researchers fuel AI, robotics, and medical advances; small and medium businesses gain market analysis they could never afford to collect.
(~1 min)
TRANSITION: The policy and collaboration layer.""",
38: """ASK: "How would you design an equitable program without demographic data? Guesswork is not a policy method."
KEY POINT: Public data supports policy and education — equitable social programs built on demographic data — and cross-national collaboration, with shared datasets fueling global climate and health initiatives.
(~1 min)
TRANSITION: The U.S. anchor: data.gov — starting with its scale.""",
39: """SAY: "548,327 datasets from more than 120 publishing organizations — and the catalog underneath was rebuilt in 2025."
KEY POINT: Data.gov hosts 548,327 datasets (as of August 2026) from 120+ federal, state, local, tribal, and university publishers across health, transportation, energy, and climate; programmatic access is via DCAT/data.json feeds.
(~2 min)
TRANSITION: What the rebuild changed.""",
40: """ASK: "What happened to the old data.gov API? It's gone — the catalog was rebuilt in 2025, and the feeds changed with it."
KEY POINT: Up from ~300,000 datasets in older course material to 548,327; the new custom catalog replaced the legacy CKAN system in 2025; the legacy catalog runs at catalog-old.data.gov only through fall 2026; programmatic access is the DCAT/data.json harvest feeds, not the old CKAN API.
(~2 min if taught)
TRANSITION: What data.gov stands for beyond the numbers.""",
41: """SAY: "Data.gov is not just a download site — its four objectives read like a governance statement."
KEY POINT: It represents the U.S. commitment to open data and transparency: accessibility, innovation, civic engagement, and efficiency.
(~1 min)
TRANSITION: The principles underneath.""",
42: """SAY: "Available, machine-readable, non-discriminatory, license-free — four tests any dataset should pass."
KEY POINT: Open data principles: freely available in accessible formats, machine-readable, accessible to everyone, free of reuse restrictions — aligned with the Open Government Directive and the Data Act.
(~1 min)
TRANSITION: What's actually in the catalog.""",
43: """SAY: "Every agency on this slide publishes data your labs could use tomorrow."
KEY POINT: Data.gov spans public health, environment, economy, safety, and education: NOAA weather and climate (hurricane paths, forecasts), HHS vaccination and outbreak data, Education graduation and funding trends — with global research impact.
(~2 min)
TRANSITION: Finding one dataset in hundreds of thousands.""",
44: """ASK: "548,327 datasets — how do you find the one you need?"
KEY POINT: Search and filter by geography, timeframe, agency, or dataset type; topic categories like Energy, Transportation, Agriculture, and Health group the catalog; datasets come as CSV, JSON, XML, and APIs.
(~1 min)
TRANSITION: How you know what you're looking at: metadata.""",
45: """SAY: "A dataset without metadata is a box without a label — source, date, and variable definitions are what make it usable."
KEY POINT: Metadata provides source, creation date, and variable definitions so data is properly understood; standardization across agencies delivers consistency and interoperability.
(~1 min)
TRANSITION: Where data.gov is heading.""",
46: """SAY: "Dashboards, AI-powered analysis, mobile access — the catalog is becoming a workbench."
KEY POINT: The direction: visualization tools that simplify complex datasets, ML that identifies trends and forecasts needs, enhanced search and mobile optimization — all promoting data-driven decisions and transparency.
(~1 min)
TRANSITION: A quick look across the border.""",
47: """ASK: "Whose climate data would you use to study the Arctic? Canada's open portal is one answer — open data doesn't stop at borders."
KEY POINT: Canada's Open Government Portal offers demographics, economy, public safety, and environment datasets under an open license — free for businesses, researchers, and citizens.
(~1 min)
TRANSITION: Enough portals — time to profile real data yourselves.""",
48: """SAY: "Thirty minutes, three real datasets, one skill: profiling — answering 'can we use this?' with evidence, not opinion."
KEY POINT: Lab 2.1 Public Data Expedition: profile agency datasets — shape, columns, dtypes, nulls, distinct counts, example values — and bookmark one dataset; you'll query it with your agent in Lab 7.3, the capstone.
(30 min lab — circulate; keep them profiling, not browsing; the bookmark feeds the Day-3 capstone)
TRANSITION: Before the lab, one strategy slide.""",
49: """SAY: "Nobody builds government AI alone — the winning pattern is partnerships and shared knowledge."
KEY POINT: Best practices: public-private partnerships for access to cutting-edge tools (DARPA's university research partnerships), and knowledge sharing through joint innovation hubs and open-source development.
(~2 min)
TRANSITION: Chapter wrap.""",
50: """ASK: "Which AI application or strategy do you think could transform your agency's workflows?"
KEY POINT: The chapter in one view: applications across health, cybersecurity, disaster response, and administration; case studies with real impact; cautionary cases demanding transparency and fairness; and collaborative strategies. Next step: identify a priority workflow in your department for a pilot.
(~2 min — take two or three answers to the whiteboard)
TRANSITION: Now the expedition itself — Lab 2.1.""",
51: """SAY: "A programme office hands you a dataset and asks 'can we use this?' — profiling is how you answer."
KEY POINT: Open lab_2.1_data_expedition.ipynb and profile three real datasets — cdc_flu_wastewater.csv, nyc_air_quality.csv, chicago_311.csv: shape, columns, dtypes, null count, distinct count, and an example value per column. Three fast profiles beat one slow one.
(30 min lab — circulate; full instructions in the Lab Manual)
TRANSITION: Debrief the profiles — then Chapter 3, the assistants on your desktop.""",
}

if __name__ == "__main__":
    apply_notes(TAG, COUNT, NOTES, FLEX_CORE)
    verify(TAG, COUNT)
