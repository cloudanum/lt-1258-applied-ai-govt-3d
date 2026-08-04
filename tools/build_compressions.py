"""Build the remaining reworked decks by applying the plan's §2.1 dispositions.

Compression method: for each topic range the plan says 'compress N->k', we KEEP the
first k slides of the range (the lead/overview slides) and DROP the tail (the
deep-dive detail the plan demotes to appendices). Specific dated slides named in
the plan are dropped explicitly; specific new slides are appended. This is a
faithful mechanical execution of the plan; final slide-level polish is an author
review pass (noted in MOVES.md).
"""
from pathlib import Path
import pptx_tools as P

BASE = Path("/Users/iahmad/Creator/Courses_and_conferences/LT/1258")
CH = BASE / "1258-Chap"
AP = BASE / "1258-App"
OUT = BASE / "1258a4-author-input/decks"


def keeprange(a, b, k):
    """First k indices of the inclusive 1-based range [a,b]."""
    return list(range(a, min(b, a + k - 1) + 1))


def build(src, keep, out, title=None, appends=None, insert_at=None):
    """append-before-delete: open full deck, append new slides (unique partnames
    guaranteed while all originals present), then ARRANGE to the final order.
    keep = 1-based original indices to keep, in order. appends = list of new
    slides appended at the END unless insert_at gives a keep-list position."""
    prs = P.open_deck(src)
    n_orig = len(list(prs.slides._sldIdLst))
    appends = appends or []
    for t, b, nt in appends:                  # append first -> partnames safe
        P.append_content(prs, t, b, nt)
    # final order as current 0-based indices
    keep0 = [i - 1 for i in keep]             # kept originals keep their positions
    new0 = [n_orig + j for j in range(len(appends))]
    if insert_at is None:
        order = keep0 + new0                  # new slides at the end
    else:
        order = list(keep0)
        for pos, np in sorted(zip(insert_at, new0)):
            order.insert(pos, np)
    P.arrange(prs, order)
    if title:
        P.retitle(prs, 0, title)
    P.save(prs, out)
    import zipfile
    names = zipfile.ZipFile(out).namelist()
    assert not {x for x in names if names.count(x) > 1}, f"dupes in {out}"
    return len(list(prs.slides._sldIdLst))


# ---------- New Ch01: AI & ML Foundations (94 -> ~50) ----------
CRISP = [
 ("How an AI Project Runs: CRISP-DM",
  ["A repeatable lifecycle for data/AI projects, used throughout this course",
   "Business understanding -> Data understanding -> Data preparation",
   "Modeling -> Evaluation -> Deployment, then iterate",
   "Gives every instructor and student a shared map of the work"],
  "Formalizes CRISP-DM, which Greg Adams noted Imran teaches from his book. Now in the deck."),
 ("CRISP-DM in Government Practice",
  ["Business understanding = the mission need and the policy constraints",
   "Data preparation is usually the largest phase (Chapter 6 goes deep)",
   "Evaluation must include fairness, security, and explainability, not just accuracy",
   "Deployment includes monitoring for drift (Chapter 8)"],
  ""),
]
ch01_keep = (keeprange(1,14,10) +          # taxonomy/history -> 10
             keeprange(16,24,5) +          # why AI matters -> 5 (s15 CAGR dropped)
             keeprange(25,30,5) +          # gov tech stack/FedRAMP -> 5
             keeprange(31,36,5) +          # labs 1.1/1.2 + K-means
             keeprange(37,48,7) +          # supervised ML -> 7
             keeprange(49,51,3) +          # NLP bridge -> 3 (rest -> AppD)
             keeprange(58,63,6) +          # NLP-for-gov -> 6
             [75] +                         # Do Now: Google NL API
             keeprange(88,89,2) +          # computer vision -> 2
             [93,94])                       # summary
# (s52-57 embeddings detail, s76-81 ANN internals, s82-87, s90-92 -> AppD/drop)

# ---------- New Ch02: Applications + Public Data (82 -> ~44) ----------
PREDPOL_REFRAME = [
 ("Predictive Policing: A Cautionary Case Study",
  ["Early systems (e.g., PredPol, later renamed) promised to forecast crime hotspots",
   "In practice they raised serious bias, transparency, and civil-liberties concerns",
   "Many jurisdictions discontinued them; treat as a lesson, not a model to copy",
   "The takeaway: high-stakes prediction on people demands fairness review and oversight"],
  "Replaces the 3 uncritical PredPol slides (old s37-39) with one cautionary slide. "
  "PredPol rebranded to Geolitica in 2021 and predictive policing has been widely discontinued."),
]
ch02_keep = (keeprange(1,7,6) +            # why gov needs AI
             keeprange(11,21,5) +          # health/CDC
             keeprange(23,27,3) +          # cyber
             keeprange(29,35,4) +          # infrastructure
             keeprange(41,44,3) +          # public safety (non-PredPol) + environment
             keeprange(46,51,3) +          # process automation
             keeprange(62,73,12) +         # DATA.GOV block (protected)
             [74] +                         # international portals (1)
             keeprange(79,82,4))            # Lab 2.1 + best practices + summary
# PredPol reframe slide appended (old s37-40 dropped)

# ---------- New Ch05: Security (old Ch03, 95 -> ~62) dedupe-only ----------
ch05_keep = (keeprange(1,25,22) +          # four dims, ATLAS, Lab 3.1 (dedupe 3)
             keeprange(26,46,16) +         # risk, CIA, PII, prompt injection, Lab 3.2
             keeprange(47,52,5) +          # PII + Lab 3.3
             keeprange(53,63,6) +          # responsible AI, de-id (advanced -> AppB)
             keeprange(64,77,8) +          # bias, threat modeling, Lab 3.4
             keeprange(78,93,9) +          # regulations (EU AI Act, NIST, OWASP)
             [94,95])                       # summary
EO_NOTE = [
 ("Federal AI Policy: A Moving Target",
  ["Executive orders and OMB memos on AI change with administrations",
   "Verify the current federal AI policy at teaching time — this area updates often",
   "Core obligations (privacy, security, testing, transparency) persist across changes",
   "Your agency's own AI policy is the operative rule for daily work"],
  "Replaces the specific rescinded-EO framing. IG notes this slide has a ~6-month shelf life."),
]

# ---------- New Ch06: Data for AI (old Ch05, 54 -> ~26) ----------
EX61 = [
 ("Exercise 6.1: Shared-Spreadsheet Data Collection",
  ["Everyone adds a few rows to a shared sheet against a loose schema",
   "We then audit the sheet together against the data-quality attributes",
   "You feel the quality problems by creating them — then fix the schema",
   "See Workbook Exercise 6.1"],
  "Greg Adams called this exercise 'brilliant.' Now formalized. A prepared messy sheet ships as an offline fallback. "
  "Debrief: schema vs free-text; who owns quality; the cleaned sheet can feed Labs 7.2/7.3."),
]
ch06_keep = (keeprange(1,6,3) +            # intro
             [8,9,10,11] +                  # tool survey (skip Dataprep s14,15; keep Glue/Wrangler/Dataflow)
             keeprange(17,24,4) +          # pipelines/quality
             keeprange(25,35,6) +          # GenAI for data prep
             keeprange(36,44,4) +          # data quality attributes
             keeprange(45,52,5) +          # governance framework
             [53,54])                       # summary

# ---------- New Ch08: Operations & Reporting (old Ch04 51 + old Ch07 33 -> ~40) ----------
# Built by merging: keep the core of old Ch04, then clone the kept slides of old Ch07.
ch08_ch04_keep = (keeprange(1,2,2) +       # title/objectives
                  keeprange(3,22,8) +      # cloud/data lake/warehouse (dedup)
                  keeprange(24,38,8) +     # MLOps
                  keeprange(39,50,8) +     # drift/oversight/LIME (payload)
                  [51])                     # objectives
ch07_old_keep = (keeprange(3,7,3) +        # reporting strategy
                 keeprange(8,16,4) +       # viz theory/pandas
                 keeprange(17,25,4) +      # dashboards (fix naming in review)
                 [26] +                     # Lab 7.1 (viz) -> renumbered 8.1
                 keeprange(27,31,2) +      # case studies
                 [32])                      # summary
GENAI_REPORTING = [
 ("GenAI-Assisted Analysis and Reporting",
  ["Modern BI tools embed AI: Copilot in Power BI, natural-language queries",
   "Ask questions of your data in plain language; get charts and summaries",
   "Still verify: check the query the tool actually ran",
   "The modern complement to the Python visualization skills in this chapter"],
  "New slide bridging the old reporting chapter to 2026 tools."),
]

# ---------- New Ch09: Summary & Roadmap (old Ch08, 12 -> 10) ----------
ch09_keep = [1,2,3,4,5,6,7,9,10,11]        # drop s8 (quantum), s12 (dup summary)
ROADMAP = [
 ("Your 90-Day Agency AI Roadmap",
  ["Weeks 1-4: pick one high-value, low-risk use case; confirm the data and the rules",
   "Weeks 5-8: prototype with prompting or RAG; keep a human in the loop",
   "Weeks 9-12: evaluate against a rubric; document risks and guardrails; brief your manager",
   "Start small, show value, build trust — then scale"],
  "Actionable closing slide replacing the quantum filler. Gives students a concrete next step."),
]


def build_merge_ch08(out):
    # append-before-delete: keep ALL of old Ch04 present while cloning Ch07 slides
    # and appending new ones, then ARRANGE to the final order.
    prs = P.open_deck(CH / "1258-Ch04.pptx")
    n4 = len(list(prs.slides._sldIdLst))
    src7 = P.open_deck(CH / "1258-Ch07.pptx")
    kept7 = [s for i, s in enumerate(src7.slides, 1) if i in set(ch07_old_keep)]
    for s in kept7:                            # cloned slides land at positions n4..n4+k-1
        P.clone_slide(prs, s)
    n_after_clone = n4 + len(kept7)
    for t, b, nt in GENAI_REPORTING:           # new slides after the clones
        P.append_content(prs, t, b, nt)
    ch04_pos = [i - 1 for i in ch08_ch04_keep]
    clone_pos = list(range(n4, n_after_clone))
    new_pos = list(range(n_after_clone, n_after_clone + len(GENAI_REPORTING)))
    P.arrange(prs, ch04_pos + clone_pos + new_pos)
    P.retitle(prs, 0, "AI Operations and Reporting in Government")
    P.save(prs, out)
    import zipfile
    names = zipfile.ZipFile(out).namelist()
    assert not {x for x in names if names.count(x) > 1}, "dupes in ch08"
    return len(list(prs.slides._sldIdLst))


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    r = {}
    r["Ch01"] = build(CH/"1258-Ch01.pptx", ch01_keep, OUT/"1258-Ch01-AI-ML-Foundations.pptx",
                      "AI and ML Foundations for Government", CRISP)
    r["Ch02"] = build(CH/"1258-Ch02.pptx", ch02_keep, OUT/"1258-Ch02-Applications-Public-Data.pptx",
                      "AI Applications Across Government and Public Data", PREDPOL_REFRAME)
    r["Ch05"] = build(CH/"1258-Ch03.pptx", ch05_keep, OUT/"1258-Ch05-Security-Risks-Responsible-AI.pptx",
                      "AI Security, Risks, and Responsible AI", EO_NOTE)
    r["Ch06"] = build(CH/"1258-Ch05.pptx", ch06_keep, OUT/"1258-Ch06-Data-for-AI.pptx",
                      "Data for AI: Collection, Quality, and Governance", EX61)
    r["Ch08"] = build_merge_ch08(OUT/"1258-Ch08-Operations-Reporting.pptx")
    r["Ch09"] = build(CH/"1258-Ch08.pptx", ch09_keep, OUT/"1258-Ch09-Summary-Roadmap.pptx",
                      "Course Summary and Your Agency AI Roadmap", ROADMAP)
    for k, v in r.items():
        print(f"{k}: {v} slides")
