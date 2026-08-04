"""
build_brand_ch06.py — apply LT standard branding/structure to
1258-Ch06-Data-for-AI.pptx (Chapter 6 'Data for AI: Collection, Quality, and
Governance'). Same standard as 4703 (see 4703a2-author-input/tools/build_brand_m1.py).

Idempotent: always rebuilds from decks/_bak6/1258-Ch06-Data-for-AI.pptx.

Changes (vs. 54-slide original):
  1. Old slide 1 (title slide on layout '2_Chapter Title AI1') rebuilt on
     'Chapter Title Government': CENTER_TITLE = chapter name, SUBTITLE =
     'Chapter 6'; speaker notes carried over verbatim.
  2. Old slide 2 already sits on 'Chapter Objectives' — kept in place; its
     body (idx 15) is updated to the chapter's four stated objectives.
  3. New Contents slide on 'Content with Header. Full Page' (section lines +
     the chapter's activities), inserted as slide 3.
  4. Activity slides rebuilt on dedicated layouts, same positions:
       s20 'DO NOW 6.B: Propose the Schema'  -> 'Do Now with Typing Hands'
         (registry: kind=donow, environment=vm; title/bullets/notes verbatim)
       s21 'Lab 6.1: Data Quality Assessment of Chicago 311'
         -> 'Exercise Reference Slide with Typing Hands'
         (standard lab-reference body; 30 min per registry/activities.yaml)
       s52/53 'Lab 6.2: GenAI-Assisted Cleaning with Structured Outputs'
         -> one 'Exercise Reference Slide with Typing Hands' (30 min per
         registry); s53 was a duplicate launcher of s52.
  5. Duplicates dropped:
       s4  — second 'Activities in This Chapter' overview, stale (lab times
             45/35 min and 125-min budget contradict the registry's 30/30 and
             105 min); s3, which matches the registry, is kept.
       s51 — exact duplicate of the objectives slide (no notes).

Final slide count: 54 - 6 dropped + 1 contents + 1 title rebuild net 0 = 52
(within the 50-60 band; no [flex] trims needed).

Run:  ../../.venv-courseware/bin/python tools/build_brand_ch06.py
"""
from __future__ import annotations
import shutil
from pathlib import Path

from pptx_tools import open_deck, arrange, save

HERE = Path(__file__).resolve().parent
DECKS = HERE.parent / "decks"
SRC = DECKS / "_bak6" / "1258-Ch06-Data-for-AI.pptx"
OUT = DECKS / "1258-Ch06-Data-for-AI.pptx"

CHAPTER_NAME = "Data for AI: Collection, Quality, and Governance"
SUBTITLE = "Chapter 6"

OBJECTIVES = [
    "Design data collection schemas — fields, types, allowed values, and validation rules",
    "Assess data against the six dimensions of data quality",
    "Use GenAI for data preparation with structured outputs",
    "Explain synthetic data and the governance frameworks that oversee it",
]

CONTENTS = [
    "6.1 Data Collection: Schema First",
    "6.2 The Six Dimensions of Data Quality",
    "6.3 GenAI for Data Preparation",
    "6.4 Pipelines and Storage",
    "6.5 Synthetic Data and De-identification",
    "6.6 Governance and Oversight",
    "Demo 6.1: Profiling Real Data, Warts and All",
    "DO NOW 6.A: Six Dimensions on Ten Rows",
    "DO NOW 6.B: Propose the Schema",
    "DO NOW 6.C: Real, Synthetic, or Neither?",
    "DO NOW 6.D: Write the Cleaning Prompt",
    "Lab 6.1: Data Quality Assessment of Chicago 311",
    "Lab 6.2: GenAI-Assisted Cleaning with Structured Outputs",
]

LAB61_BODY = [
    "In your Lab Manual, refer to Lab 6.1: Data Quality Assessment of Chicago 311",
    "Assess real operational data against all six dimensions",
    "Quantify each defect — null rates, duplicates, invalid dates",
    "Build a scorecard and a go / no-go recommendation — 30 minutes",
]

LAB62_BODY = [
    "In your Lab Manual, refer to Lab 6.2: GenAI-Assisted Cleaning with Structured Outputs",
    "Open lab_6.2_genai_cleaning.ipynb and extract 60 raw values from a messy categorical column",
    "Call the model with a strict JSON schema: {raw, canonical, confidence} — 30 minutes",
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


def _replace_body(ph, lines):
    tf = ph.text_frame
    tf.clear()
    _fill_body(ph, lines)


def _slide_lines(slide):
    """Title text, body paragraphs (main non-title placeholder), notes."""
    title = slide.shapes.title.text_frame.text if slide.shapes.title else ""
    body = None
    for ph in slide.placeholders:
        if ph.placeholder_format.idx != 0 and ph.has_text_frame:
            if body is None or (ph.width or 0) * (ph.height or 0) > (body.width or 0) * (body.height or 0):
                body = ph
    bullets = [p.text for p in body.text_frame.paragraphs if p.text.strip()] if body is not None else []
    notes = slide.notes_slide.notes_text_frame.text if slide.has_notes_slide else ""
    return title, bullets, notes


def main():
    shutil.copy(SRC, OUT)
    prs = open_deck(OUT)
    slides = list(prs.slides)
    assert len(slides) == 54, f"expected 54 slides, got {len(slides)}"

    # Capture content to carry over before any rebuild.
    t1 = _ph(slides[0], 0).text_frame.text
    st1 = _ph(slides[0], 1).text_frame.text
    n1 = slides[0].notes_slide.notes_text_frame.text if slides[0].has_notes_slide else ""
    assert t1 == CHAPTER_NAME and st1 == SUBTITLE, (t1, st1)

    dn_title, dn_bullets, dn_notes = _slide_lines(slides[19])   # s20 DO NOW 6.B
    assert dn_title == "DO NOW 6.B: Propose the Schema", dn_title
    l61_title, _l61_bullets, l61_notes = _slide_lines(slides[20])  # s21 Lab 6.1
    assert l61_title == "Lab 6.1: Data Quality Assessment of Chicago 311", l61_title
    l62_title, _l62_bullets, l62_notes = _slide_lines(slides[52])  # s53 Lab 6.2 (30 min)
    assert l62_title == "Lab 6.2: GenAI-Assisted Cleaning with Structured Outputs", l62_title

    # 1. Chapter Title on the standard layout (notes carried verbatim).
    t = prs.slides.add_slide(_layout(prs, "Chapter Title Government"))
    _ph(t, 0).text_frame.text = CHAPTER_NAME
    _ph(t, 1).text_frame.text = SUBTITLE
    t.notes_slide.notes_text_frame.text = n1

    # 2. Objectives: old slide 2 already on 'Chapter Objectives' — update body.
    _replace_body(_ph(slides[1], 15), OBJECTIVES)

    # 3. Contents.
    c = prs.slides.add_slide(_layout(prs, "Content with Header. Full Page"))
    _ph(c, 0).text_frame.text = "Contents"
    _fill_body(_ph(c, 1), CONTENTS)

    # 4. Activity rebuilds (title + bullets + notes verbatim; lab bodies standardized).
    d = prs.slides.add_slide(_layout(prs, "Do Now with Typing Hands"))
    _ph(d, 0).text_frame.text = dn_title
    _fill_body(_ph(d, 1), dn_bullets)
    d.notes_slide.notes_text_frame.text = dn_notes

    l1 = prs.slides.add_slide(_layout(prs, "Exercise Reference Slide with Typing Hands"))
    _ph(l1, 0).text_frame.text = l61_title
    _fill_body(_ph(l1, 1), LAB61_BODY)
    l1.notes_slide.notes_text_frame.text = l61_notes

    l2 = prs.slides.add_slide(_layout(prs, "Exercise Reference Slide with Typing Hands"))
    _ph(l2, 0).text_frame.text = l62_title
    _fill_body(_ph(l2, 1), LAB62_BODY)
    l2.notes_slide.notes_text_frame.text = l62_notes

    # New slides are 0-based 54..58 in append order: T=54, C=55, D=56, L1=57, L2=58.
    # Final order: title, objectives(s2), contents, activities-overview(s3),
    # s5..s19, DO NOW 6.B, Lab 6.1, s22..s50, Lab 6.2, summary(s54).
    order0 = [54, 1, 55, 2] + list(range(4, 19)) + [56, 57] + list(range(21, 50)) + [58, 53]
    arrange(prs, order0)
    save(prs, OUT)

    # quick echo
    prs2 = open_deck(OUT)
    n = len(list(prs2.slides))
    print(f"saved {OUT} ({n} slides)")
    assert 50 <= n <= 60, f"out of band: {n}"
    for i, s in enumerate(prs2.slides):
        title = s.shapes.title.text_frame.text.replace("\n", " ")[:55] if s.shapes.title else "(no title)"
        print(f"{i+1:>2} [{s.slide_layout.name}] {title}")


if __name__ == "__main__":
    main()
