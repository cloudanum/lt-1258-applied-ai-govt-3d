"""
build_brand_ch08.py — apply LT standard branding/structure to
1258-Ch08-Operations-Reporting.pptx (Chapter 8 'AI Operations & Reporting
in Government').

Idempotent: always rebuilds from decks/_bak6/1258-Ch08-Operations-Reporting.pptx.

Changes (vs. 53-slide original):
  1. Old slide 1 (chapter title on layout '2_Chapter Title AI1') rebuilt on
     layout 'Chapter Title Government' at position 1; title, subtitle, and
     speaker notes copied verbatim.
  2. Old slide 2 (Chapter Objectives, 4 bullets) is already on the correct
     'Chapter Objectives' layout — kept untouched.
  3. New Contents slide (layout 'Content with Header. Full Page') inserted at
     position 3: section lines + the chapter's activities.
  4. Old slide 4 ('Activities in This Chapter' duplicate with stale times —
     Lab 8.1 40 min / Lab 8.2 35 min vs. registry 30/30, budget 117 vs. 102)
     dropped; old slide 3 (registry-consistent) kept on its content layout.
  5. Old slide 40 'Lab 8.1: Visualization and Reporting from EPA Data'
     (Full Page Blank) rebuilt on 'Exercise Reference Slide with Typing
     Hands' at the same position; body = Lab Manual reference line + the 3
     step lines + registry time (30 minutes); notes copied verbatim.
  6. Old slide 46 ('In your Workbook, please refer to Lab 8.1: Visualization
     Using Python', Full Page Blank) dropped: stale duplicate of the Lab 8.1
     reference (pre-a4 title, contradicts registry on flex).
  7. Old slides 51 and 52 (duplicate 'Lab 8.2: GenAI-Assisted Analysis and
     Briefing' launchers, 35 vs. 30 min) consolidated: one Lab 8.2 slide
     rebuilt on 'Exercise Reference Slide with Typing Hands' at position 51
     with registry time (30 minutes); the duplicate dropped.
  Demo 8.1 and DO NOW 8.A-8.D exist only as lines on the 'Activities in This
  Chapter' overview (registry slide_refs confirm) — left as-is.

Final slide count: 53 - 6 dropped + 4 added = 51 (in the 50-60 band).

Run:  ../../.venv-courseware/bin/python tools/build_brand_ch08.py
"""
from __future__ import annotations
import shutil
from pathlib import Path

from pptx_tools import open_deck, arrange, save

HERE = Path(__file__).resolve().parent
DECKS = HERE.parent / "decks"
SRC = DECKS / "_bak6" / "1258-Ch08-Operations-Reporting.pptx"
OUT = DECKS / "1258-Ch08-Operations-Reporting.pptx"

CHAPTER_NAME = "AI Operations and Reporting in Government"
SUBTITLE = "Chapter 8"

CONTENTS = [
    "AI and Cloud Computing for Government",
    "MLOps: Pipelines, Monitoring, and Drift",
    "Federal AI Oversight: GAO Principles and OMB M-25-21",
    "Dashboards and Honest Reporting",
    "GenAI-Assisted Analysis",
    "Demo 8.1: Watching a Model Drift",
    "DO NOW 8.A: Which Metric Catches This?",
    "DO NOW 8.B: Pilot to Production Readiness",
    "DO NOW 8.C: Critique This Dashboard",
    "DO NOW 8.D: Ask, Then Verify",
    "Lab 8.1: Visualization and Reporting from EPA Data",
    "Lab 8.2: GenAI-Assisted Analysis and Briefing",
]

LAB81_TITLE = "Lab 8.1: Visualization and Reporting from EPA Data"
LAB81_BODY = [
    "In your Lab Manual, refer to Lab 8.1: Visualization and Reporting from EPA Data",
    "Rank counties by unhealthy days; chart the top 15",
    "Apply the guidelines: sorted, labelled, honest scale",
    "Assemble a one-page briefing with a recommendation",
    "30 minutes",
]

LAB82_TITLE = "Lab 8.2: GenAI-Assisted Analysis and Briefing"
LAB82_BODY = [
    "In your Lab Manual, refer to Lab 8.2: GenAI-Assisted Analysis and Briefing",
    "Open `lab_8.2_genai_reporting.ipynb`",
    "Send a profile of the EPA data and ask for five candidate findings",
    "Pick the three most decision-relevant",
    "30 minutes",
]


def _layout(prs, name):
    for lay in prs.slide_masters[0].slide_layouts:
        if lay.name == name:
            return lay
    raise KeyError(f"layout not found: {name}")


def _ph(slide, idx):
    for ph in slide.placeholders:
        if ph.placeholder_format.idx == idx:
            return ph
    raise KeyError(f"placeholder idx {idx} not on slide")


def _fill_body(ph, lines):
    tf = ph.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line


def _title_of(slide):
    if slide.shapes.title is not None and slide.shapes.title.has_text_frame:
        return slide.shapes.title.text_frame.text.strip().replace("\n", " ")
    for ph in slide.placeholders:
        if ph.placeholder_format.idx == 0 and ph.has_text_frame:
            return ph.text_frame.text.strip().replace("\n", " ")
    return ""


def _notes_of(slide):
    return slide.notes_slide.notes_text_frame.text if slide.has_notes_slide else ""


def main():
    shutil.copy(SRC, OUT)
    prs = open_deck(OUT)
    slides = list(prs.slides)
    assert len(slides) == 53, f"expected 53 slides, got {len(slides)}"

    # Sanity-check the slides this script rebuilds or drops.
    assert _title_of(slides[0]) == CHAPTER_NAME, _title_of(slides[0])
    assert _title_of(slides[2]) == "Activities in This Chapter"
    assert _title_of(slides[3]) == "Activities in This Chapter"
    assert _title_of(slides[39]).startswith("Lab 8.1"), _title_of(slides[39])
    # slide 46 is the stale Lab 8.1 workbook reference: steps sit in the TITLE
    # placeholder and 'In your Workbook...' in the OBJECT placeholder (idx 1).
    assert _ph(slides[45], 1).text_frame.text.startswith("In your Workbook")
    assert _title_of(slides[50]).startswith("Lab 8.2"), _title_of(slides[50])
    assert _title_of(slides[51]).startswith("Lab 8.2"), _title_of(slides[51])

    # Capture text to carry over before any rebuild.
    old1_sub = _ph(slides[0], 1).text_frame.text
    old1_notes = _notes_of(slides[0])
    lab81_notes = _notes_of(slides[39])
    lab82_notes = _notes_of(slides[50])

    # 1. Chapter Title on 'Chapter Title Government' (replaces old slide 1)
    t = prs.slides.add_slide(_layout(prs, "Chapter Title Government"))
    _ph(t, 0).text_frame.text = CHAPTER_NAME
    _ph(t, 1).text_frame.text = old1_sub if old1_sub.strip() else SUBTITLE
    t.notes_slide.notes_text_frame.text = old1_notes

    # 2. Contents (old slide 2 objectives already on the right layout — kept)
    c = prs.slides.add_slide(_layout(prs, "Content with Header. Full Page"))
    _ph(c, 0).text_frame.text = "Contents"
    _fill_body(_ph(c, 1), CONTENTS)

    # 3. Lab 8.1 on 'Exercise Reference Slide with Typing Hands'
    l1 = prs.slides.add_slide(_layout(prs, "Exercise Reference Slide with Typing Hands"))
    _ph(l1, 0).text_frame.text = LAB81_TITLE
    _fill_body(_ph(l1, 1), LAB81_BODY)
    l1.notes_slide.notes_text_frame.text = lab81_notes

    # 4. Lab 8.2 on 'Exercise Reference Slide with Typing Hands'
    l2 = prs.slides.add_slide(_layout(prs, "Exercise Reference Slide with Typing Hands"))
    _ph(l2, 0).text_frame.text = LAB82_TITLE
    _fill_body(_ph(l2, 1), LAB82_BODY)
    l2.notes_slide.notes_text_frame.text = lab82_notes

    # Order (0-based; originals 0..52, new slides appended at 53..56).
    # Drops: 0 (old title), 3 (stale overview dup), 39 (old Lab 8.1),
    #        45 (stale workbook ref), 50 (old Lab 8.2), 51 (dup Lab 8.2).
    order0 = (
        [53, 1, 54, 2]          # title, objectives, contents, activities overview
        + list(range(4, 39))    # orig slides 5..39
        + [55]                  # Lab 8.1 reference (at old position 40)
        + list(range(40, 45))   # orig slides 41..45
        + list(range(46, 50))   # orig slides 47..50
        + [56]                  # Lab 8.2 reference (at old position 51)
        + [52]                  # summary
    )
    arrange(prs, order0)
    save(prs, OUT)

    # quick echo
    prs2 = open_deck(OUT)
    print(f"saved {OUT} ({len(list(prs2.slides))} slides)")
    for i, s in enumerate(prs2.slides):
        title = _title_of(s)[:60] or "(no title)"
        print(f"{i+1:>2} [{s.slide_layout.name}] {title}")


if __name__ == "__main__":
    main()
