"""Enrich Ch09 'Course Summary and Your Agency AI Roadmap' (rev a3):
correct stale/incorrect text on existing slides in place, append 39 new slides
(content_ch09_enrich.CH09_NEW_SLIDES), then arrange all 50 into final order.

Run:  cd 1258/1258a4-author-input/tools && ../../../.venv-courseware/bin/python build_enrich_ch09.py
A pre-change backup lives in decks/_bak/."""
from pathlib import Path
import sys
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pptx_tools as P
import content_ch09_enrich as C

DECK = Path(__file__).resolve().parent.parent / "decks" / "1258-Ch09-Summary-Roadmap.pptx"


def _para_text(p):
    return "".join(r.text for r in p.runs)


def _replace_para(slide, old, new):
    """Replace the full text of the paragraph whose text == old, preserving the
    first run's formatting. Raises if not found."""
    for sh in slide.shapes:
        if not sh.has_text_frame:
            continue
        for p in sh.text_frame.paragraphs:
            if p.runs and _para_text(p) == old:
                p.runs[0].text = new
                for r in p.runs[1:]:
                    r.text = ""
                return
    raise ValueError(f"paragraph not found: {old!r}")


def _append_notes(slide, extra):
    tf = slide.notes_slide.notes_text_frame
    tf.text = (tf.text.rstrip() + "\n\n" + extra) if tf.text.strip() else extra


def _set_notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def fix_existing(prs):
    slides = list(prs.slides)

    # --- Slide 1: stale metadata (Chapter 8 / EDA jogger / Day 1 2:15pm) ---
    s = slides[0]
    _replace_para(s, "Chapter 8", "Chapter 9")
    _set_notes(s, "Jogger text: Course Summary\n"
                  "Direction: Left then right\n"
                  "Chapter starts: Day 3 (PM session)\n"
                  "Instructor notes: Closing unit — recap, verified 2026 trends, the P10 "
                  "re-score, and the 90-day agency AI roadmap. Rev a3: fixed stale metadata "
                  "(was 'Chapter 8', jogger 'Exploratory Data Analysis', 'Day 1 at 2:15pm').")

    # --- Slide 3: tool list did not match the a3 lab stack ---
    s = slides[2]
    _replace_para(s, "Designing interactive dashboards with real-time data",
                  "Building data visualizations and AI-assisted reports in Python")
    _replace_para(s, "Hands-on experience with AI tools like Tableau, Power BI, and Generative AI APIs",
                  "Hands-on labs: JupyterLab notebooks, desktop AI assistants, and the OpenAI API")
    _append_notes(s, "Rev a3: corrected the lab tool list — Tableau/Power BI are not in the a3 "
                     "lab registry; labs run in JupyterLab notebooks, browser-based desktop "
                     "assistants, and the OpenAI API (Labs 1.x-8.x per registry/labs.yaml).")

    # --- Slide 4: enrich notes with verified DOI numbers ---
    _append_notes(slides[3],
                  "Rev a3: verified quantified federal cases now have their own slide "
                  "('Federal AI Wins, With Numbers') — USGS minerals years-to-weeks, NICC 200+ "
                  "expert-hours/yr, 8,000 grants in 4 hours, NPS ~7,000 labor-days/yr.\n"
                  + C.SRC_DOI)

    # --- Slide 5: tie audits/validations to named instruments ---
    _append_notes(slides[4],
                  "Rev a3: name the instruments behind 'regular audits and validations' — the "
                  "NIST AI RMF 1.0 plus GenAI Profile (NIST-AI-600-1) and OMB M-25-21's minimum "
                  "risk-management practices for high-impact AI.\n" + C.SRC_NIST + "\n" + C.SRC_M2521)

    # --- Slide 6: replace generic/unsourced trends with verified 2026 trends ---
    s = slides[5]
    P.retitle(prs, 5, "The 2026 AI Landscape: Emerging Trends")
    _replace_para(s, "Machine learning trends", "Agentic AI")
    _replace_para(s, "Specialized models for governance tasks like fraud detection and resource planning",
                  "Models that plan, use tools, and act — beyond chat (as of mid-2026)")
    _replace_para(s, "Generative AI innovations", "Reasoning and multimodal models")
    _replace_para(s, "Expanding applications in content creation, summarization, and citizen communication",
                  "Think longer before answering; text, image, audio, and video in one model")
    _replace_para(s, "Automation tools", "Open-weight and on-prem AI")
    _replace_para(s, "Streamlining workflows for data preparation, analysis, and report generation",
                  "Capable models inside your own boundary for sensitive data (as of mid-2026)")
    _set_notes(s, "Rev a3: replaced generic, unsourced trend bullets with the verified 2026 "
                  "picture — agentic systems (Anthropic's workflow/agent taxonomy), reasoning "
                  "models (OpenAI o3/o4-mini), native multimodality (Gemini 2.0), and "
                  "open-weight/on-prem viability (gpt-oss; DOI's hybrid pattern). The six "
                  "[flex] slides that follow give each trend a full treatment with dated "
                  "numbers.\n" + C.SRC_ANTHROPIC + "\n" + C.SRC_O3 + "\n" + C.SRC_GEMINI
               + "\n" + C.SRC_GPTOSS)

    # --- Slide 9: Negnevitsk -> Negnevitsky + label 2011; replace unverifiable summit ---
    s = slides[8]
    # run-level fix to preserve the italic title / plain author formatting
    fixed = False
    for sh in s.shapes:
        if not sh.has_text_frame:
            continue
        for p in sh.text_frame.paragraphs:
            for r in p.runs:
                if r.text == "Negnevitsk":
                    r.text = "Negnevitsky (2011)"
                    fixed = True
    assert fixed, "Negnevitsk run not found"
    _replace_para(s, "For foundational knowledge",
                  "Classical AI foundations (expert systems, fuzzy logic); predates deep learning")
    _replace_para(s, "AI for Governance Summit",
                  "GSA AI Community of Practice and government-wide AI Training Series")
    _replace_para(s, "Online forums and meetups for networking and collaboration",
                  "NIST AI Resource Center and GSA AI Guide for Government")
    _set_notes(s, "Speaker Notes:\nShare how participants can continue their learning journey "
                  "through recommended resources.\nEncourage joining AI communities for peer "
                  "support and expert advice.\nVisualization:\nResource Grid: categorized into "
                  "books, courses, and forums.\n\nRev a3: corrected the author name (Negnevitsky) "
                  "and labeled the 2011 edition as classical-AI foundations — it predates deep "
                  "learning. Replaced the unverifiable 'AI for Governance Summit' with verified "
                  "federal communities: GSA's AI Community of Practice and AI Training Series, "
                  "NIST's Trustworthy & Responsible AI Resource Center, and GSA's AI Guide for "
                  "Government.\n" + C.SRC_GSA + "\n" + C.SRC_NIST + "\n" + C.SRC_GSA_GUIDE)

    # --- Slide 10: 'enhance, not replace' is policy ---
    _append_notes(slides[9],
                  "Rev a3: M-25-21 itself requires human oversight for high-impact AI — "
                  "'enhance, not replace' is policy, not just good advice.\n" + C.SRC_M2521)

    # --- Slide 11: map the weeks onto M-25-21 artifacts and GSA's tiers ---
    _append_notes(slides[10],
                  "Rev a3: this action slide is now the cap of a worked 30/60/90 template "
                  "(preceding slides). Weeks 1-4 = Tier 1-style selection + AUP check; weeks "
                  "5-8 = prototype with human oversight; weeks 9-12 = NIST AI RMF evaluation, "
                  "high-impact determination, use-case-inventory awareness, and the leadership "
                  "brief. Keep this slide prominent — it is the one attendees photograph.\n"
                  + C.SRC_GSA + "\n" + C.SRC_M2521 + "\n" + C.SRC_NIST)


# Final order as 0-based indices into the deck AFTER appending:
# 0-10 = original slides, 11-49 = N1..N39 in append order.
ORDER0 = [
    0,          # 1  Title (Ch09, corrected)
    1,          # 2  Course Objectives
    11,         # 3  Three Days, One Arc
    2,          # 4  Recap of Key Concepts (corrected)
    12,         # 5  Day 1 synthesis
    13,         # 6  Day 2 synthesis
    14,         # 7  Day 3 synthesis
    3,          # 8  Use Cases in Government
    15,         # 9  Federal AI Wins, With Numbers
    4,          # 10 Challenges, Risks, Best Practices
    6,          # 11 XAI and Ethical Frameworks
    16,         # 12 Human-in-the-Loop Is Policy
    5,          # 13 The 2026 AI Landscape: Emerging Trends (corrected)
    17,         # 14 Agentic AI [flex]
    18,         # 15 Reasoning Models [flex]
    19,         # 16 Multimodal AI [flex]
    20,         # 17 Open-Weight / On-Prem [flex]
    21,         # 18 2026 by the Numbers [flex]
    22,         # 19 Gartner 2026 [flex]
    7,          # 20 Interactive Q&A
    23,         # 21 The Prompting Spine: P0 to P10
    24,         # 22 Unseal Your P0
    25,         # 23 Rewrite P0 with the Ladder
    26,         # 24 Score Both Against the Rubric
    27,         # 25 Debrief: What the Delta Teaches
    28,         # 26 M-25-21 in One Slide
    29,         # 27 AI Governance Cast
    30,         # 28 GSA Three-Tier Model
    31,         # 29 NIST AI RMF + GenAI Profile
    32,         # 30 30/60/90 Template
    33,         # 31 Days 1-30
    34,         # 32 Days 31-60
    35,         # 33 Days 61-90
    10,         # 34 Your 90-Day Agency AI Roadmap (action slide, prominent)
    36,         # 35 Next Steps: Manager
    37,         # 36 Next Steps: Analyst
    38,         # 37 Next Steps: IT Ops
    9,          # 38 Final Recap
    8,          # 39 Recommended Resources (corrected)
    39,         # 40 Federal AI Training Ecosystem
    40,         # 41 Policy and Guidance to Bookmark
    41, 42, 43, 44, 45, 46, 47, 48,  # 42-49 Glossary 1-8
    49,         # 50 Thank You / Evaluation
]


def main():
    prs = P.open_deck(DECK)
    assert len(list(prs.slides)) == 11, "expected the 11-slide a2 deck; backup is in decks/_bak"
    fix_existing(prs)
    for t, b, n in C.CH09_NEW_SLIDES:
        P.append_content(prs, t, b, n)
    assert len(list(prs.slides)) == 50
    P.arrange(prs, ORDER0)
    P.save(prs, DECK)

    # verification: reopen, count, zip integrity, no dup partnames
    prs2 = P.open_deck(DECK)
    n = len(list(prs2.slides))
    zf = zipfile.ZipFile(DECK)
    assert zf.testzip() is None, "zip corruption"
    names = zf.namelist()
    dupes = {x for x in names if names.count(x) > 1}
    assert not dupes, f"dupes: {dupes}"
    print(f"saved {DECK.name}: {n} slides, zip OK, no dup partnames")
    for idx, title, w in P.inventory(DECK):
        print(f"{idx:>3}  {w:>4}w  {title}")


if __name__ == "__main__":
    main()
