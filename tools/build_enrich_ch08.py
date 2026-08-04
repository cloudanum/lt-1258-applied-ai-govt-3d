"""Enrich Ch08 (AI Operations and Reporting) for the 1258 a3 revision.

Steps (per authoring-agent workflow):
  (a) in-place TEXT EDITS to stale/incorrect slides (run-level, format-preserving)
  (b) append 9 new slides (MLOps depth, federal oversight, Copilot/ChatGPT GenAI
      analysis, reporting best practice)
  (c) ONE final arrange() placing every slide in its final position (moves the
      appended-at-end GenAI slide into the reporting section)
  (d) save + verify (count, zip integrity)

All factual claims trace to 1258/research/refs-ch06-ch08-data-ops.md
(URLs verified live 2026-08-01).
"""
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pptx_tools as P

DECK = Path("/Users/iahmad/Creator/Courses_and_conferences/LT/1258/"
            "1258a4-author-input/decks/1258-Ch08-Operations-Reporting.pptx")

V = "(verified 2026-08-01)"


# --------------------------------------------------------------------------- #
# (a) In-place text edits
# --------------------------------------------------------------------------- #
def _run(slide, shape_name, para_idx, run_idx=0):
    for sh in slide.shapes:
        if sh.name == shape_name and sh.has_text_frame:
            return sh.text_frame.paragraphs[para_idx].runs[run_idx]
    raise KeyError(f"{shape_name} p{para_idx}")


def _shape(slide, shape_name):
    for sh in slide.shapes:
        if sh.name == shape_name:
            return sh
    raise KeyError(shape_name)


def text_edits(prs):
    s = list(prs.slides)

    # --- Slide 9 (idx 8): notes — dated EC2 P3 hardware ref -> generic modern
    s[8].notes_slide.notes_text_frame.text = (
        "Speaker Notes:\n"
        "Provide a demonstration of TensorFlow running on an NVIDIA GPU.\n"
        "Discuss current cloud accelerated-computing options — GPU instance families "
        "such as AWS EC2's P-series and Google Cloud TPUs — as alternatives to "
        "on-premises hardware.\n"
        "Highlight the growing adoption of GPUs in AI, including their use in "
        "gaming, which parallels deep learning."
    )

    # --- Slide 11 (idx 10): drop unverified FEMA NLP claim; fix CDC claim
    body = "Content Placeholder 1"
    _run(s[10], body, 0).text = "Applied AI in Government"
    _run(s[10], body, 1).text = "Department of Homeland Security (DHS)"
    _run(s[10], body, 2).text = ("Publishes a public inventory of agency AI use cases, "
                                 "framed by OMB M-25-21 high-impact AI rules*")
    _run(s[10], body, 4).text = ("Uses NLP (eMaRC Plus) to identify reportable cancer "
                                 "cases from pathology reports**")
    s[10].notes_slide.notes_text_frame.text = (
        "Speaker Notes:\n"
        "Discuss how agencies apply AI to unstructured and operational data.\n"
        "The CDC's National Program of Cancer Registries uses dictionary-based "
        "(eMaRC Plus) and statistical NLP to automate identification of reportable "
        "cancer cases from unstructured pathology and lab reports — cancer-registry "
        "surveillance, not outbreak tracking.\n"
        "DHS publishes its AI use cases in a public inventory framed by OMB M-25-21's "
        "'high-impact AI' definition. An earlier version of this slide cited a FEMA "
        "social-media NLP use case that could not be verified against the current "
        "inventory; it was removed.\n"
        "Source: CDC — Natural Language Processing for Cancer Surveillance, "
        "https://www.cdc.gov/national-program-cancer-registries/data-modernization/"
        f"natural-language-processing.html {V}\n"
        "Source: DHS — AI Use Case Inventory, "
        f"https://www.dhs.gov/ai/use-case-inventory {V}"
    )

    # --- Slide 12 (idx 11): drop unverifiable IRS "over 20 source systems" figure
    _run(s[11], body, 2).text = ("Operates the Compliance Data Warehouse (CDW), "
                                 "integrating data across source systems to support "
                                 "tax administration")
    _run(s[11], body, 4).text = ("Employs the Planning Database (PDB) containing "
                                 "housing, demographic, and socio-economic data to "
                                 "aid in survey and census planning*")
    foot = _shape(s[11], "Text Placeholder 7")
    p0 = foot.text_frame.paragraphs[0]          # the brillient vendor footnote
    p0._p.getparent().remove(p0._p)
    foot.text_frame.paragraphs[0].runs[0].text = "*"   # '**' -> '*'
    s[11].notes_slide.notes_text_frame.text = (
        "Speaker Notes:\n"
        "Discuss the scalability and integration of hybrid solutions, merging data "
        "lakes and warehouses for government workflows.\n"
        "The earlier 'over 20 source systems' figure for the IRS CDW rested on a "
        "vendor case study that could not be verified; the slide now states the "
        "CDW's role generically.\n"
        "The Census Planning Database is verified: ACS housing/demographic/"
        "socio-economic estimates at tract and block-group levels, Disclosure "
        "Review Board-cleared.\n"
        "Source: US Census Bureau — Planning Database, "
        "https://www.census.gov/topics/research/guidance/planning-databases.html "
        f"{V}"
    )

    # --- Slide 25 (idx 24): notes — update stale EU AI Act audit claim
    s[24].notes_slide.notes_text_frame.text = (
        "Speaker Notes:\n"
        "Lead with US federal monitoring expectations: GAO-21-519SP names monitoring "
        "one of four AI accountability principles.\n"
        "For international context, the updated EU AI Act timeline (as of mid-2026): "
        "transparency rules apply from August 2026; high-risk obligations — "
        "including logging, human oversight, and post-market monitoring — phase in "
        "from December 2027.\n"
        "Discuss the importance of proactive oversight to avoid crises stemming "
        "from unregulated AI use.\n"
        "Explain why tracking performance metrics is critical to maintaining public "
        "trust in AI applications.\n"
        "Source: European Commission — EU AI Act Regulatory Framework, "
        "https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai "
        f"{V}"
    )

    # --- Slide 26 (idx 25): oversight framing -> federal instruments
    _run(s[25], body, 1).text = ("Regular risk audits guided by GAO's AI "
                                 "accountability framework")
    _run(s[25], body, 2).text = ("NIST AI RMF plus OMB M-25-21 rules for "
                                 "high-impact AI")
    s[25].notes_slide.notes_text_frame.text = (
        "Speaker Notes:\n"
        "The primary federal frames: NIST AI RMF (Govern/Map/Measure/Manage; RMF 1.0 "
        "is under revision as of mid-2026), OMB M-25-21 minimum risk-management "
        "practices for high-impact AI, and GAO-21-519SP's four accountability "
        "principles (governance, data, performance, monitoring — next slide).\n"
        "The UK's former Office for AI no longer exists as such; its functions were "
        "merged into the new Government Digital Service announced January 27, 2025.\n"
        "Source: NIST — AI Risk Management Framework, "
        f"https://www.nist.gov/itl/ai-risk-management-framework {V}\n"
        "Source: GAO — Artificial Intelligence: An Accountability Framework for "
        f"Federal Agencies (GAO-21-519SP), https://www.gao.gov/products/gao-21-519sp {V}\n"
        "Source: UK GDS — 'Same name, new ambitions', "
        f"https://gds.blog.gov.uk/2025/01/27/same-name-new-ambitions/ {V}"
    )

    # --- Slide 34 (idx 33): GDPR lead -> Privacy Act / FISMA for US federal staff
    _run(s[33], body, 7).text = ("Follow Privacy Act and FISMA requirements; HIPAA "
                                 "where health data is involved")
    s[33].notes_slide.notes_text_frame.text = (
        "Speaker Notes:\n"
        "The data landscape is like the infrastructure of a city — each source and "
        "process must work seamlessly together.\n"
        "For US federal staff, lead compliance discussions with the Privacy Act of "
        "1974, FISMA, and CIPSEA (enumerated in OMB M-25-05's applicability list); "
        "retain HIPAA for health data and mention GDPR only as international context.\n"
        "Source: OMB M-25-05 — Phase 2 Implementation of the Evidence Act, "
        "https://bidenwhitehouse.archives.gov/wp-content/uploads/2025/01/"
        "M-25-05-Phase-2-Implementation-of-the-Foundations-for-Evidence-Based-"
        f"Policymaking-Act-of-2018-Open-Government-Data-Access-and-Management-Guidance.pdf {V}"
    )

    # --- Slide 37 (idx 36): Looker Studio renamed BACK to Data Studio (Apr 2026)
    _run(s[36], body, 3).text = ("Google Data Studio: free tier, with Pro at "
                                 "$9/user/project/month (renamed back April 2026)")
    s[36].notes_slide.notes_text_frame.text = (
        "Speaker Notes:\n"
        "Google renamed Looker Studio back to Data Studio on April 11, 2026 — the "
        "product's third name (Google Data Studio 2016, Looker Studio 2022, Data "
        "Studio 2026). The slide title is correct again; no user migration action "
        "was required. Free self-service tier remains; Data Studio Pro adds CMEK "
        "and admin controls.\n"
        "Compare scenarios: Tableau for highly interactive dashboards; Data Studio "
        "for quick, cost-effective reporting; Power BI where Microsoft 365 is "
        "standard.\n"
        "Source: Google Cloud — Data Studio product page, "
        f"https://cloud.google.com/looker-studio {V}\n"
        "Source: PPC Land — 'Data Studio is back: Google kills Looker Studio name "
        "for good' (Apr 17, 2026), "
        f"https://ppc.land/data-studio-is-back-google-kills-looker-studio-name-for-good/ {V}"
    )

    # --- Slide 41 (idx 40): delete unsourced case-study numbers
    _run(s[40], body, 6).text = ("Faster response through unified, real-time "
                                 "situational awareness")
    _run(s[40], body, 7).text = ("Better resource prioritization from automated, "
                                 "live data feeds")
    s[40].notes_slide.notes_text_frame.text = (
        "Speaker Notes:\n"
        "This is an illustrative scenario, not a measured case study — earlier "
        "versions showed unsourced percentage outcomes ('25% faster response', "
        "'30% optimization'), which were removed.\n"
        "Walk participants through the scenario: from fragmented data to seamless "
        "AI-enabled integration.\n"
        "Question: 'Which departments in your agency could benefit from similar "
        "AI-driven dashboards?'"
    )


# --------------------------------------------------------------------------- #
# (b) New slides: (title, bullets, notes) — appended in this order -> idx 43..51
# --------------------------------------------------------------------------- #
NEW_SLIDES = [
    # A (43) — after slide 18 (pipeline tools)
    ("MLOps Pipelines: CI/CD and Continuous Training",
     ["CI/CD for ML automates testing and deployment of data, code, and models",
      "Continuous training (CT) re-runs the pipeline automatically on new data",
      "Version data, code, and models together for reproducibility and audit",
      "Automated gates catch bad data or weak models before deployment",
      "Many ML projects never reach production; disciplined pipelines close the gap"],
     "Speaker Notes:\n"
     "Extend the pipeline discussion into operations: MLOps unites data science, IT "
     "operations, and business stakeholders around automated, versioned, monitored "
     "delivery — the Kreuzberger et al. definition the chapter already cites. The "
     "arXiv preprint is free-access for students.\n"
     "Source: Kreuzberger, Kühl, Hirschl — Machine Learning Operations (MLOps): "
     f"Overview, Definition, and Architecture (IEEE Access 2023), https://arxiv.org/abs/2205.02302 {V}"),
    # B (44) — after slide 25 (metrics & monitoring)
    ("MLOps in Production: What to Monitor",
     ["Model performance: accuracy and error rates against a known baseline",
      "Input data: schema changes, missing values, shifting distributions",
      "Pipeline health: latency, failures, and resource consumption",
      "Mission outcomes: is the model still improving the metric that matters?",
      "GAO's accountability framework names monitoring a core principle"],
     "Speaker Notes:\n"
     "GAO-21-519SP organizes federal AI accountability around four principles — "
     "governance, data, performance, and monitoring — each with key practices and "
     "audit questions. Monitoring means continuous performance tracking with "
     "documented thresholds, not a one-time pre-launch check.\n"
     "Source: GAO — Artificial Intelligence: An Accountability Framework for Federal "
     f"Agencies (GAO-21-519SP), https://www.gao.gov/products/gao-21-519sp {V}"),
    # C (45) — [flex] depth
    ("Drift Deep Dive: Detection and Hidden Technical Debt",
     ["Data drift: input distributions shift away from the training data",
      "Concept drift: the relationship between inputs and outcomes changes",
      "Detectors: statistical tests like KS, MMD, and chi-squared (e.g., Alibi Detect)",
      "Hidden feedback loops: a model's own outputs become future training data",
      "Undeclared consumers: downstream systems quietly depend on your model"],
     "[flex] Depth slide — skip if time is short.\n"
     "Sculley et al. (Google, NeurIPS 2015) argue ML systems accrue hidden "
     "maintenance debt: boundary erosion, entanglement, hidden feedback loops, and "
     "undeclared consumers. Alibi Detect is a maintained open-source library "
     "(v0.13.0, Dec 2025) implementing KS, MMD, Cramér–von Mises, chi-squared, and "
     "classifier-based drift detectors.\n"
     "Source: Sculley et al. — Hidden Technical Debt in Machine Learning Systems "
     "(NeurIPS 2015), https://papers.nips.cc/paper/5656-hidden-technical-debt-in-"
     f"machine-learning-systems {V}\n"
     f"Source: Seldon — Alibi Detect, https://github.com/SeldonIO/alibi-detect {V}"),
    # D (46) — [flex] depth
    ("Retraining Triggers and Model Retirement",
     ["Scheduled retraining: fixed cadence (e.g., quarterly) with refreshed data",
      "Triggered retraining: performance or drift metrics cross a set threshold",
      "Validate the retrained model before it replaces the production version",
      "Retire models whose mission need or data supply has ended",
      "NIST AI RMF's Manage function covers ongoing risk response and change"],
     "[flex] Depth slide — skip if time is short.\n"
     "Trade-off: scheduled retraining is predictable but may retrain needlessly; "
     "triggered retraining responds to real drift but needs reliable monitoring. "
     "The NIST AI RMF's Manage function covers risk response and change management "
     "across the AI lifecycle; note that AI RMF 1.0 is under revision as of mid-2026.\n"
     "Source: NIST — AI Risk Management Framework, "
     f"https://www.nist.gov/itl/ai-risk-management-framework {V}"),
    # E (47) — after slide 26 (oversight)
    ("Federal AI Oversight: GAO Principles and OMB M-25-21",
     ["GAO-21-519SP: four accountability principles — governance, data, performance, monitoring",
      "Each principle carries key practices and audit questions for agencies",
      "OMB M-25-21 defines high-impact AI: output drives decisions affecting rights or safety",
      "High-impact AI requires minimum risk-management practices before deployment",
      "NIST AI RMF provides the voluntary risk framework underneath both"],
     "Speaker Notes:\n"
     "This is the audit-ready checklist. M-25-21's high-impact definition covers AI "
     "whose output is a principal basis for decisions with legal, material, binding, "
     "or significant effect on rights, safety, access to services, or critical "
     "infrastructure (as framed on the DHS use-case inventory page).\n"
     "Source: GAO — Artificial Intelligence: An Accountability Framework for Federal "
     f"Agencies (GAO-21-519SP), https://www.gao.gov/products/gao-21-519sp {V}\n"
     "Source: DHS — AI Use Case Inventory, https://www.dhs.gov/ai/use-case-inventory "
     f"{V}"),
    # F (48) — reporting best practice, after slide 38 (dashboard components)
    ("Reporting Best Practice: From Data to Decision",
     ["Start with the decision the report must support, not the data you have",
      "One message per view: headline metric first, detail on drilldown",
      "Use consistent definitions and time grains across all reports",
      "Annotate anomalies and known data gaps directly on the dashboard",
      "Test every dashboard with real users before rolling it out"],
     "Speaker Notes:\n"
     "Practical best practice, no single external source. Tie back to the data-"
     "integrity slides: a beautiful dashboard over inconsistent definitions erodes "
     "trust faster than no dashboard at all. Ask participants which recurring "
     "report in their office fails the 'one message per view' test."),
    # G (49) — after slide 37 (dashboard tools)
    ("Copilot in Power BI for Government",
     ["Ask questions in natural language; get summaries, visuals, and DAX",
      "Requires paid Fabric capacity (F2+) or Power BI Premium (P1+)",
      "Pro or Premium Per User licenses alone are not sufficient",
      "Not supported in sovereign clouds — a direct Azure Government caveat (as of mid-2026)",
      "Prep semantic models for AI and verify answers before relying on them"],
     "Speaker Notes:\n"
     "Key licensing facts as of mid-2026: Copilot in Power BI requires a paid Fabric "
     "capacity (F2 or higher) or Power BI Premium (P1+); Pro/PPU licenses alone are "
     "insufficient. It is enabled by default but admin-controlled, and — critical "
     "for this audience — NOT supported in sovereign clouds, so Azure Government "
     "tenants cannot use it today. Semantic models should be 'prepped for AI' for "
     "reliable answers; prompts are limited to 10,000 characters.\n"
     "Source: Microsoft Learn — Copilot in Power BI, "
     "https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-introduction "
     f"{V}"),
    # H (50) — GenAI block, after the moved GenAI slide
    ("ChatGPT for Data Analysis",
     ["Upload a CSV or spreadsheet; ask questions in plain language",
      "Runs Python in a stateful notebook behind the scenes",
      "Produces tables, statistics, and interactive charts",
      "Prep helps: descriptive headers, one record per row, no split tables",
      "Review the generated code, outputs, and assumptions before relying on results"],
     "Speaker Notes:\n"
     "Per OpenAI's documentation: supported spreadsheet/CSV/PDF uploads, Python-"
     "backed analysis in a stateful notebook, interactive charts — and an explicit "
     "instruction to review generated code, outputs, and assumptions. The Python "
     "environment cannot make external web requests. Remind participants: the data "
     "rule applies — public or approved data only unless in an authorized "
     "enterprise tool.\n"
     "Source: OpenAI Help Center — Data analysis with ChatGPT, "
     f"https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt {V}"),
    # I (51) — GenAI block, verification habit
    ("GenAI-Assisted Analysis: Ask, Then Verify",
     ["Ask the tool to show the query or code it actually ran",
      "Schema-correct output is not necessarily semantically correct",
      "Spot-check results against a known subset of your data",
      "Treat AI-generated insight as a draft until a human validates it",
      "Public or approved data only — the data rule still applies"],
     "Speaker Notes:\n"
     "The verification habit applies across ChatGPT data analysis, Copilot in Power "
     "BI, and Data Studio conversational analytics. Google's Gemini structured-"
     "output guidance makes the key distinction: syntactic correctness is not "
     "semantic correctness — validate values, not just formats.\n"
     "Source: OpenAI Help Center — Data analysis with ChatGPT, "
     f"https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt {V}\n"
     "Source: Google — Gemini API Structured Output, "
     f"https://ai.google.dev/gemini-api/docs/structured-output {V}"),
]


# --------------------------------------------------------------------------- #
# Build
# --------------------------------------------------------------------------- #
def main():
    prs = P.open_deck(DECK)
    assert len(list(prs.slides)) == 43, "expected 43 slides in source deck"

    text_edits(prs)

    for title, bullets, notes in NEW_SLIDES:
        P.append_content(prs, title, bullets, notes)

    # (c) final arrangement (0-based indices into the CURRENT order):
    #   0..17   slides 1-18 (intro, cloud, EDA, pipelines, MLOps, pipeline tools)
    #   43      new A: CI/CD + continuous training
    #   18..24  slides 19-25 (operationalizing .. metrics & monitoring)
    #   44,45,46 new B, C, D (monitor, drift deep dive, retraining)
    #   25      slide 26 (oversight)
    #   47      new E: federal oversight (GAO + M-25-21)
    #   26..36  slides 27-37 (reporting section .. dashboard tools)
    #   49      new G: Copilot in Power BI for government
    #   37      slide 38 (dashboard components)
    #   48      new F: reporting best practice
    #   38..40  slides 39-41 (Lab 7.1 launcher, real-time AI, case study)
    #   42      slide 43 (GenAI-assisted analysis — MOVED into reporting section)
    #   50,51   new H, I (ChatGPT data analysis, verify habit)
    #   41      slide 42 (Summary)
    order0 = (list(range(0, 18)) + [43]
              + list(range(18, 25)) + [44, 45, 46]
              + [25] + [47]
              + list(range(26, 37)) + [49] + [37] + [48]
              + [38, 39, 40] + [42] + [50, 51] + [41])
    assert sorted(order0) == list(range(52))
    P.arrange(prs, order0)
    P.save(prs, DECK)

    # (d) verify
    n = len(list(P.open_deck(DECK).slides))
    assert n == 52, f"expected 52 slides, got {n}"
    assert zipfile.ZipFile(DECK).testzip() is None, "zip integrity failed"
    names = zipfile.ZipFile(DECK).namelist()
    dupes = {x for x in names if names.count(x) > 1}
    assert not dupes, f"dup partnames: {dupes}"
    print(f"OK: {DECK.name} — {n} slides, zip clean, no dup partnames")


if __name__ == "__main__":
    main()
