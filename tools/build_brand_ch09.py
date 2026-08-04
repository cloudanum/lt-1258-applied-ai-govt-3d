"""
build_brand_ch09.py — apply LT standard branding/structure to
1258-Ch09-Summary-Roadmap.pptx (Chapter 9 'Course Summary and Your Agency
AI Roadmap').

Idempotent: always rebuilds from decks/_bak6/1258-Ch09-Summary-Roadmap.pptx.

Changes (vs. 52-slide original):
  1. New Chapter Title slide (layout 'Chapter Title Government'):
     CENTER_TITLE (idx 0) = chapter name, SUBTITLE (idx 1) = 'Chapter 9'.
     Folds the old slide 1 (a title-acting slide on '2_Chapter Title AI1'):
     its notes (jogger text, session placement, instructor notes) carry over
     verbatim; old slide dropped.
  2. New Chapter Objectives slide (layout 'Chapter Objectives'), body idx 15,
     4 bullets: synthesize the three days; read the 2026 trends honestly;
     build a 30/60/90 agency AI roadmap; measure before/after (P0->P10).
     The old slide 2 ('Course Objectives') is NOT folded — it is recap
     content for this summary chapter and stays as a content slide.
  3. New Contents slide (layout 'Content with Header. Full Page'):
     section lines + the chapter's activities.
  4. Activities overview: slides 3 and 4 were duplicates of
     'Activities in This Chapter'. Keep slide 3 (its times match
     registry/activities.yaml — Lab 9.1 = 30 min; slide 4 is stale, 40 min),
     drop slide 4. Overview stays on its content layout.
  5. Lab 9.1 launcher: slides 50 and 51 were duplicates. Rebuilt once on
     layout 'Exercise Reference Slide with Typing Hands' at the same
     position; title + notes copied verbatim; body becomes the Lab Manual
     reference line + key lines incl. the registry time (30 min).
     Both old slides dropped.

Final slide count: 52 - 4 dropped + 4 added = 52 (in the 50-60 band;
no [flex] trims needed).

Run:  ../../../.venv-courseware/bin/python tools/build_brand_ch09.py
       (from 1258/1258a4-author-input/, or an absolute interpreter path)
"""
from __future__ import annotations
import shutil
from pathlib import Path

from pptx_tools import open_deck, arrange, save

HERE = Path(__file__).resolve().parent
DECKS = HERE.parent / "decks"
SRC = DECKS / "_bak6" / "1258-Ch09-Summary-Roadmap.pptx"
OUT = DECKS / "1258-Ch09-Summary-Roadmap.pptx"

CHAPTER_NAME = "Course Summary and Your Agency AI Roadmap"
SUBTITLE = "Chapter 9"

OBJECTIVES = [
    "Synthesize the three days — from AI user to AI builder",
    "Read the 2026 trends honestly — adoption, capability, cost, energy",
    "Build a 30/60/90 AI roadmap for your agency",
    "Measure your own before/after — unseal P0, rewrite at P10",
]

CONTENTS = [
    "9.1 Three Days, One Arc: Course Synthesis",
    "9.2 The 2026 AI Landscape: Trends, Honestly",
    "9.3 Capstone Debrief: Unseal P0, Rewrite at P10",
    "9.4 Your 90-Day Agency AI Roadmap",
    "9.5 Next Steps by Role",
    "9.6 Resources and Course Glossary",
    "Activities: Demo 9.1, DO NOW 9.A–9.D, Lab 9.1",
]

LAB_TITLE = "Lab 9.1: Your 90-Day Agency AI Roadmap"
LAB_BODY = [
    "In your Lab Manual, refer to Lab 9.1: Your 90-Day Agency AI Roadmap",
    "Start from the use case you circled in DO NOW 9.B; find one precedent in federal_ai_use_cases.csv",
    "Days 1-30: define the problem, confirm the data exists, name the owner",
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
    return slide.shapes.title.text_frame.text.strip() if slide.shapes.title else ""


def main():
    shutil.copy(SRC, OUT)
    prs = open_deck(OUT)
    slides = list(prs.slides)
    assert len(slides) == 52, f"expected 52 slides, got {len(slides)}"

    # Capture content to carry over before any rebuild.
    assert _title_of(slides[0]) == CHAPTER_NAME, _title_of(slides[0])
    old1_notes = slides[0].notes_slide.notes_text_frame.text if slides[0].has_notes_slide else ""
    assert _title_of(slides[2]) == "Activities in This Chapter"
    assert _title_of(slides[3]) == "Activities in This Chapter"
    assert _title_of(slides[50]) == LAB_TITLE, _title_of(slides[50])
    old_lab_notes = (
        slides[50].notes_slide.notes_text_frame.text if slides[50].has_notes_slide else ""
    )

    # 1. Chapter Title (folds old slide 1: notes carry over verbatim)
    t = prs.slides.add_slide(_layout(prs, "Chapter Title Government"))
    _ph(t, 0).text_frame.text = CHAPTER_NAME
    _ph(t, 1).text_frame.text = SUBTITLE
    t.notes_slide.notes_text_frame.text = old1_notes

    # 2. Chapter Objectives (idx 15 is the displayed body on this layout)
    o = prs.slides.add_slide(_layout(prs, "Chapter Objectives"))
    _fill_body(_ph(o, 15), OBJECTIVES)

    # 3. Contents
    c = prs.slides.add_slide(_layout(prs, "Content with Header. Full Page"))
    _ph(c, 0).text_frame.text = "Contents"
    _fill_body(_ph(c, 1), CONTENTS)

    # 4. Lab 9.1 rebuild -> Exercise Reference Slide with Typing Hands
    lab = prs.slides.add_slide(_layout(prs, "Exercise Reference Slide with Typing Hands"))
    _ph(lab, 0).text_frame.text = LAB_TITLE
    _fill_body(_ph(lab, 1), LAB_BODY)
    lab.notes_slide.notes_text_frame.text = old_lab_notes

    # Order (0-based orig indices; new slides appended at 52,53,54,55):
    #   title, objectives, contents,
    #   orig 3 (Activities overview, keep — registry-correct times),
    #   orig 2 (Course Objectives recap — content of this summary chapter),
    #   orig 5..49 (all content),
    #   new lab slide,
    #   orig 52 (Thank You).
    # Dropped: orig 1 (old title), orig 4 (stale activities dup),
    #          orig 50, orig 51 (old lab launcher dups).
    order0 = [52, 53, 54, 2, 1] + list(range(4, 49)) + [55, 51]
    arrange(prs, order0)
    save(prs, OUT)

    # quick echo
    prs2 = open_deck(OUT)
    print(f"saved {OUT} ({len(list(prs2.slides))} slides)")
    for i, s in enumerate(prs2.slides):
        title = s.shapes.title.text_frame.text.replace("\n", " ")[:55] if s.shapes.title else "(no title)"
        print(f"{i+1:>2} [{s.slide_layout.name}] {title}")


if __name__ == "__main__":
    main()
