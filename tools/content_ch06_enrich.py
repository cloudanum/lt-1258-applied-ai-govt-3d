"""New slides for the Ch06 'Data for AI' a3 enrichment (24 slides).

Every factual claim traces to 1258/research/refs-ch06-ch08-data-ops.md
(URLs verified live 2026-08-01). Slides marked [flex] are skippable depth;
their notes start with '[flex] '."""

FCSM = ("Source: Federal Committee on Statistical Methodology — A Framework for Data Quality (FCSM-20-04), "
        "https://nces.ed.gov/FCSM/pdf/FCSM.20.04_A_Framework_for_Data_Quality.pdf (verified 2026-08-01)")
DAMA = ("Source: DAMA UK Working Group — The Six Primary Dimensions for Data Quality Assessment, "
        "https://www.dama-uk.org/resources/the-six-primary-dimensions-for-data-quality-assessment (verified 2026-08-01)")
ISO8000 = ("Source: ISO — ISO 8000-1:2022 Data quality, Part 1: Overview, "
           "https://www.iso.org/standard/81745.html (verified 2026-08-01)")
M2505 = ("Source: OMB — M-25-05, Phase 2 Implementation of the Evidence Act, "
         "https://bidenwhitehouse.archives.gov/wp-content/uploads/2025/01/M-25-05-Phase-2-Implementation-of-the-Foundations-for-Evidence-Based-Policymaking-Act-of-2018-Open-Government-Data-Access-and-Management-Guidance.pdf (verified 2026-08-01)")
DATAGOV = ("Source: GSA TTS with OMB and the CDO Council — Federal Open Data Policy and Standards hub, "
           "https://strategy.data.gov/ (verified 2026-08-01)")
NIST800188 = ("Source: NIST — SP 800-188, De-Identifying Government Datasets: Techniques and Governance, "
              "https://www.nist.gov/publications/de-identifying-government-datasets-techniques-and-governance (verified 2026-08-01)")
ONS = ("Source: UK Office for National Statistics — Methodology Working Paper 16: Synthetic Data Pilot, "
       "https://www.ons.gov.uk/methodology/methodologicalpublications/generalmethodology/onsworkingpaperseries/onsmethodologyworkingpaperseriesnumber16syntheticdatapilot (verified 2026-08-01)")
JORDON = ("Source: Jordon, Yoon & van der Schaar — Synthetic Data: what, why and how?, "
          "https://arxiv.org/abs/2205.03257 (verified 2026-08-01)")
OPENAI_SO = ("Source: OpenAI — Structured Outputs (API docs), "
             "https://platform.openai.com/docs/guides/structured-outputs (verified 2026-08-01)")
GEMINI_SO = ("Source: Google — Gemini API Structured Output, "
             "https://ai.google.dev/gemini-api/docs/structured-output (verified 2026-08-01)")
OPENAI_DA = ("Source: OpenAI Help Center — Data analysis with ChatGPT, "
             "https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt (verified 2026-08-01)")
ROH = ("Source: Roh, Heo & Whang — A Survey on Data Collection for Machine Learning, "
       "https://arxiv.org/abs/1811.03402 (verified 2026-08-01)")
GEBRU = ("Source: Gebru et al. — Datasheets for Datasets, "
         "https://arxiv.org/abs/1803.09010 (verified 2026-08-01)")
DATAPREP = ("Source: Google Cloud — Dataprep by Trifacta documentation, "
            "https://cloud.google.com/dataprep/docs (verified 2026-08-01)")
DATABREW = ("Source: AWS — AWS Glue DataBrew, "
            "https://aws.amazon.com/glue/features/databrew/ (verified 2026-08-01)")
NISTRMF = ("Source: NIST — AI Risk Management Framework (AI RMF 1.0), "
           "https://www.nist.gov/itl/ai-risk-management-framework (verified 2026-08-01)")
DHS = ("Source: U.S. Department of Homeland Security — AI Use Case Inventory, "
       "https://www.dhs.gov/ai/use-case-inventory (verified 2026-08-01)")
GAO = ("Source: U.S. GAO — GAO-21-519SP, Artificial Intelligence: An Accountability Framework for Federal Agencies, "
       "https://www.gao.gov/products/gao-21-519SP (verified 2026-08-01)")
CENSUS_PDB = ("Source: U.S. Census Bureau — Planning Database, "
              "https://www.census.gov/topics/research/guidance/planning-databases.html (verified 2026-08-01)")

# (title, bullets, notes) — appended in this order; final position set by arrange()
NEW_SLIDES = [
 # N1 — data collection methods
 ("How Government Data Gets Collected",
  ["Administrative records: tax filings, benefits claims, permits, case-management systems",
   "Surveys and censuses: designed instruments with controlled questions (Census, BLS)",
   "Sensors and telemetry: traffic counters, weather stations, infrastructure feeds",
   "Documents and web: forms, PDFs, emails, public web content",
   "Third-party and shared data: commercial vendors, state/local partners, other agencies"],
  "Ground the chapter in reality: most government AI projects start from administrative "
  "data collected for another purpose, not from data designed for AI. Ask the room which "
  "of these sources their agency already holds.\n" + ROH),
 # N2 — schema-first collection design (sets up Ex 6.1)
 ("Collection Design: Schema First",
  ["A schema defines fields, types, allowed values, and required entries before collection",
   "Loose schemas invite free-text drift: 'N/A', 'unknown', five different date formats",
   "Validation rules at entry time cost far less than cleaning later",
   "Decide ownership: who may add columns, who resolves conflicts",
   "Exercise 6.1 lets you feel this by breaking a loose schema yourselves"],
  "Bridge slide into Exercise 6.1: the exercise deliberately uses a loose schema so "
  "participants generate the defects themselves, then discover why schema-first design "
  "matters. Do not reveal the punchline before the exercise."),
 # N3 — the three quality frames
 ("Three Frames for Data Quality",
  ["DAMA UK: the classic six — completeness, uniqueness, timeliness, validity, accuracy, consistency",
   "FCSM-20-04: the federal statistical frame — utility, objectivity, integrity, 11 dimensions",
   "ISO 8000: the international standard series for data-quality measurement and management",
   "All three agree: quality is fitness for purpose, measured dimension by dimension",
   "This course uses the DAMA six; know the federal frame for official statistics"],
  "The deck's attribute list is a simplification of the DAMA canonical six. FCSM-20-04 is "
  "the U.S. federal statistical system's official framework; ISO 8000-1:2022 is the "
  "international standards citation when neither is enough.\n"
  + DAMA + "\n" + FCSM + "\n" + ISO8000),
 # N4-N9 — the six dimensions
 ("Dimension 1: Accuracy",
  ["Data correctly represent the real-world fact they describe",
   "Test: compare records against an authoritative source or ground truth",
   "Government example: an outdated address in a benefits record misdirects official mail",
   "Typical fixes: validation against reference data, verification workflows"],
  "Accuracy is the dimension everyone assumes and few measure. FCSM-20-04 treats it as "
  "'accuracy and reliability' under the objectivity domain. Ask: what is your ground truth, "
  "and how would you know if the data drifted from it?\n" + DAMA + "\n" + FCSM),
 ("Dimension 2: Completeness",
  ["All required records and fields are present — nothing silently missing",
   "Test: count nulls; reconcile record counts against source systems",
   "Government example: missing incident reports make a district look safer than it is",
   "Typical fixes: required-field rules, reconciliation totals, gap reports"],
  "Missingness is usually not random: the records most likely to be missing often differ "
  "from the rest — a bias problem as well as a quality problem.\n" + DAMA),
 ("Dimension 3: Consistency",
  ["The same fact is recorded the same way across systems and over time",
   "Test: cross-check the same entity's records in different systems",
   "Government example: 'DC', 'D.C.', and 'District of Columbia' fragment a statewide count",
   "Typical fixes: shared reference data and standard code lists (state, county codes)"],
  "Consistency failures multiply when agencies share data: each system's local conventions "
  "collide at integration time. FCSM-20-04 calls a close cousin 'coherence'.\n"
  + DAMA + "\n" + FCSM),
 ("Dimension 4: Timeliness",
  ["Data are current enough for the decision they support",
   "Test: measure the lag between the real-world event and data availability",
   "Government example: decade-old census tract data misdirects today's grant allocations",
   "Typical fixes: refresh schedules, staleness flags, documented as-of dates"],
  "Timeliness is relative to the decision: annual data is fine for capital planning and "
  "useless for emergency response. FCSM-20-04 splits timeliness from punctuality.\n"
  + DAMA + "\n" + FCSM),
 ("Dimension 5: Validity",
  ["Values conform to defined formats, types, and ranges",
   "Test: check every field against its schema rules",
   "Government example: a birthdate of February 30, or a four-digit ZIP code",
   "Typical fixes: entry-time validation, constrained picklists, schema enforcement"],
  "Validity is the cheapest dimension to enforce — rules are mechanical — and the one a "
  "loose shared spreadsheet violates first. Watch it happen live in Exercise 6.1.\n" + DAMA),
 ("Dimension 6: Uniqueness",
  ["Each real-world entity appears exactly once — no duplicates",
   "Test: deduplicate on keys; fuzzy-match names and addresses",
   "Government example: a constituent registered twice could receive duplicate payments",
   "Typical fixes: master-data management, unique identifiers, merge procedures"],
  "Duplicates inflate counts and distort every downstream model. Fuzzy matching trades "
  "false merges against missed duplicates — a policy choice, not just a technical one.\n" + DAMA),
 # N10-N12 — Ex 6.1 walkthrough
 ("Exercise 6.1 Walkthrough: Propose the Schema",
  ["Before touching the shared sheet, draft a schema: fields, types, required values",
   "Example: date_collected (YYYY-MM-DD), agency (picklist), record_count (integer)",
   "Decide what is optional versus required — and who adjudicates disputes",
   "Post the schema where everyone can see it before data entry starts"],
  "Walkthrough part 1. Have two or three participants propose the schema aloud and let the "
  "class critique it. The gap between the proposed schema and what people actually type is "
  "the lesson. See Workbook Exercise 6.1."),
 ("Exercise 6.1 Walkthrough: Audit the Sheet",
  ["After everyone adds rows, audit the sheet against all six dimensions",
   "Accuracy: any impossible or implausible values?",
   "Completeness: which required cells are blank?",
   "Consistency: how many spellings of the same agency?",
   "Validity and uniqueness: format violations and duplicate rows"],
  "Walkthrough part 2. Tally defects per dimension on the class whiteboard — the DAMA six "
  "become the audit checklist, so the framework is used, not just defined. A prepared messy "
  "sheet ships as the offline fallback."),
 ("Exercise 6.1 Debrief: Which Defects Did the Model Miss?",
  ["Now ask a GenAI assistant to find the data-quality problems in the sheet",
   "Compare its list against the class audit: what did it catch, what did it miss?",
   "Models are strong on format issues, weaker on wrong-but-plausible values",
   "The lesson: AI assists the audit; it does not replace domain judgment"],
  "Walkthrough part 3. Typical outcome: the assistant flags date formats and duplicates "
  "reliably but misses semantically wrong entries (a real-looking agency in the wrong "
  "state) because that takes domain knowledge. Reinforces the validation habit from the "
  "structured-outputs slides.\n" + OPENAI_DA),
 # N13 — structured outputs
 ("Making GenAI Extraction Reliable: Structured Outputs",
  ["Free-text LLM answers break pipelines: prose where you needed a number",
   "Structured outputs constrain the model to a JSON Schema you supply",
   "OpenAI 'strict' mode and Gemini both support schema-constrained JSON",
   "Every field required, no extra properties: the response parses every time",
   "This turns 'LLM fills in fields' into dependable, schema-valid extraction"],
  "The engineering reality behind the 'semantic imputation' and 'contextual enrichment' "
  "claims on the earlier slides: production teams do not parse prose — they constrain the "
  "model to a schema. Both major vendors document the same pattern.\n"
  + OPENAI_SO + "\n" + GEMINI_SO),
 # N14 — validation habit
 ("The Validation Habit: Schema-Correct Is Not Correct",
  ["Structured output guarantees valid JSON — not true values",
   "Always validate semantics: ranges, cross-field logic, spot-checks against the source",
   "Chat-with-your-data tools run generated code you can inspect",
   "Ask the tool to show its method; review code and assumptions before trusting results",
   "In government work, you remain accountable for the number you report"],
  "Syntactic correctness is not semantic correctness — Gemini's own docs say to validate "
  "values, and OpenAI's data-analysis doc says to review generated code, outputs, and "
  "assumptions. Make 'show your work' a standard prompt.\n" + GEMINI_SO + "\n" + OPENAI_DA),
 # N15 [flex] — tool landscape incl. Dataprep status
 ("The Data-Prep Tool Landscape (as of mid-2026)",
  ["Cloud-native: AWS Glue DataBrew and SageMaker Data Wrangler (this chapter)",
   "Desktop and enterprise: Power BI dataflows, Alteryx Designer Cloud",
   "In flux: Google Cloud Dataprep — docs live, marketing redirects to BigQuery",
   "Trifacta is now part of Alteryx; no formal Dataprep sunset has been announced",
   "Choose by fit: data location, team skills, and security authorization"],
  "[flex] Depth slide — skip if running behind. Dataprep status as of 2026-08-01: "
  "documentation still live, the marketing URL redirects to BigQuery, and Trifacta now "
  "redirects to Alteryx Designer Cloud — treat as 'in flux,' not officially sunset, and "
  "re-verify before each course run. DataBrew remains an offered AWS service.\n"
  + DATAPREP + "\n" + DATABREW),
 # N16 [flex] — pipeline anatomy
 ("Pipeline Anatomy: Ingest, Store, Prepare, Serve",
  ["Ingest: batch loads and streaming feeds from source systems",
   "Store: a raw landing zone plus curated, cleaned layers",
   "Prepare: cleaning, joining, validating — where this chapter's tools live",
   "Serve: warehouse tables, APIs, dashboards, model features",
   "Automate each handoff; manual steps are where errors and delays breed"],
  "[flex] Depth slide connecting the chapter's tools to the pipeline architecture Chapter 8 "
  "develops in MLOps terms. Key point for AI users: 'prepare' is not one step — it recurs "
  "at every handoff."),
 # N17 [flex] — storage choices
 ("Storage Choices: Warehouse, Lake, Lakehouse",
  ["Data warehouse: structured, curated, fast for reporting (e.g., Census planning databases)",
   "Data lake: low-cost raw storage for anything, schema applied on read",
   "Lakehouse: lake storage with warehouse-style management layered on top",
   "Government reality: all three coexist; know where your data actually lives",
   "The storage decision shapes cost, governance, and who can use the data"],
  "[flex] Depth slide. The Census Planning Database is a real federal warehouse example: "
  "ACS estimates plus operational variables at tract and block-group level, cleared by the "
  "Census Disclosure Review Board.\n" + CENSUS_PDB),
 # N18 — labeling
 ("Labeling and Annotation Best Practices",
  ["Supervised AI needs labeled examples: someone must decide the right answers",
   "Write annotation guidelines with worked examples before labeling starts",
   "Measure labeler agreement; adjudicate disagreements, don't average them away",
   "Match the labeler to the task: crowdworkers, domain experts, or weak supervision",
   "Document who labeled, how, and when — label choices embed judgment and bias"],
  "Labels are human judgments frozen into data. The Roh et al. survey maps when to use "
  "crowdsourcing versus expert labeling versus weak supervision; Datasheets for Datasets "
  "is the documentation habit that makes label provenance visible.\n" + ROH + "\n" + GEBRU),
 # N19 — synthetic data intro
 ("Synthetic Data: When Fake Data Is the Safe Data",
  ["Synthetic data are artificially generated to mimic real data's structure and statistics",
   "Use it to develop and test without touching personal records",
   "No one-to-one link to real people — the Census Bureau framing",
   "Good for: code testing, training environments, sharing across security boundaries",
   "Caution: models trained on synthetic quirks inherit them — evaluate fidelity"],
  "This course's own lab data follows this pattern. The ONS paper quotes the US Census "
  "Bureau definition; Jordon et al. is a plain-language explainer on the failure modes "
  "(privacy leakage, fidelity loss) that are easy to overlook.\n" + ONS + "\n" + JORDON),
 # N20 [flex] — ONS spectrum
 ("The ONS Synthetic Data Spectrum",
  ["The UK statistics office defines six levels, from no risk to extreme risk",
   "Level 1: synthetic structural — schema only, no values; for code testing",
   "Middle levels: more analytical value, progressively more disclosure risk",
   "Level 6: synthetically-augmented replica — high utility, extreme disclosure risk",
   "The trade-off is fundamental: utility and privacy pull in opposite directions"],
  "[flex] Depth slide. ONS Methodology Working Paper 16 lays out the six-level spectrum and "
  "reviews tools (synthpop, simPop, Faker, Mockaroo). The spectrum gives agencies a shared "
  "vocabulary for how 'synthetic' a dataset really is.\n" + ONS),
 # N21 [flex] — de-identification
 ("De-identification and NIST SP 800-188",
  ["Masking names is not de-identification: quasi-identifiers re-identify people",
   "NIST SP 800-188: pick a sharing model — de-identified release, synthetic, query, enclave",
   "Stand up a Disclosure Review Board; adopt measurable de-identification standards",
   "Run re-identification studies to test whether your protection actually works",
   "Real example: Census Bureau public products are Disclosure Review Board-cleared"],
  "[flex] Depth slide pairing with the public-records use case. ZIP + birthdate + sex is "
  "the classic quasi-identifier combination. NIST SP 800-188 is the federal how-to; the "
  "Census Planning Database page is a working DRB example.\n" + NIST800188 + "\n" + CENSUS_PDB),
 # N22 — federal data governance
 ("Federal Data Governance: Evidence Act, CDOs, M-25-05",
  ["The Evidence Act's OPEN Government Data Act made federal data open by default",
   "Every agency has a Chief Data Officer and a Data Governance Body",
   "OMB M-25-05 (January 2025): comprehensive data inventories in JSON (DCAT-US 3.0)",
   "'Machine-readable' has a statutory definition: computer-processable, no meaning lost",
   "strategy.data.gov is the live hub for federal data policy and CDO guidance"],
  "The DAMA-style framework on the next slides is generic; this is its US federal "
  "instantiation. M-25-05 (which rescinds M-13-13) assigns implementation to agency CDOs "
  "and Data Governance Bodies and requires data.gov/data.json hosting. Note: the CDO "
  "Council's old standalone site no longer resolves — use the strategy.data.gov hub.\n"
  + M2505 + "\n" + DATAGOV),
 # N23 — federal AI oversight anchors
 ("Federal AI Oversight: NIST AI RMF, OMB M-25-21, GAO",
  ["NIST AI RMF: voluntary risk framework — Govern, Map, Measure, Manage",
   "As of mid-2026 the AI RMF 1.0 is being revised — check for updates",
   "OMB M-25-21: minimum risk-management practices for 'high-impact' AI before deployment",
   "High-impact: output principally drives decisions affecting rights, safety, or services",
   "GAO-21-519SP: the auditor's lens — governance, data, performance, monitoring"],
  "These three instruments are where this chapter's data-quality work meets federal AI "
  "policy: GAO's data principle and M-25-21's data-quality practices both assume the "
  "dimensions and governance covered here. The high-impact definition is from OMB M-25-21 "
  "as applied on the DHS AI use-case inventory page.\n" + NISTRMF + "\n" + DHS + "\n" + GAO),
 # N24 [flex] — dataset documentation
 ("Documenting Datasets: Datasheets and DCAT-US",
  ["Every dataset should ship with documentation: motivation, composition, collection, uses",
   "'Datasheets for Datasets' is the standard academic template",
   "Federal angle: M-25-05 requires inventory metadata in DCAT-US 3.0 JSON",
   "Good documentation is both a usability tool and a fairness tool",
   "If a dataset has no documentation, treat its quality as unknown"],
  "[flex] Depth slide. The datasheet questions (Why was it collected? Who is in it? How was "
  "it labeled?) are exactly the questions an AI user should ask before trusting a dataset. "
  "DCAT-US 3.0 is the machine-readable federal version of the same habit.\n"
  + GEBRU + "\n" + M2505),
]
