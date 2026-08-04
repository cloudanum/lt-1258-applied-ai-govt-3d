"""
build_brand_ch04.py — apply LT standard branding/structure to
1258-Ch04-ModernGenAI-PromptEng.pptx (Chapter 4 'Modern GenAI & Prompt Engineering').

Idempotent: always rebuilds from decks/_bak6/1258-Ch04-ModernGenAI-PromptEng.pptx.

Changes (vs. 59-slide original):
  1. Chapter Title rebuilt on layout 'Chapter Title Government' (old slide 1 was
     on '2_Chapter Title AI1'; python-pptx cannot re-layout, so rebuild+drop).
     CENTER_TITLE = chapter name, SUBTITLE = 'Chapter 4'. Old notes were empty.
  2. New Chapter Objectives slide (layout 'Chapter Objectives'), body idx 15.
  3. New Contents slide (layout 'Content with Header. Full Page'): folds the old
     slide-2 agenda ('1_Section Title AI1') section lines + the chapter's
     activities; the old agenda slide's note is carried into the Contents notes.
  4. Duplicate 'Activities in This Chapter' overview (old slide 4, stale 45-min
     Lab 4.1) dropped; old slide 3 kept — it matches registry/activities.yaml.
  5. Lab 4.1 (old slide 56) and Lab 4.2 (old slides 57 + exact-dup 58) rebuilt on
     layout 'Exercise Reference Slide with Typing Hands' at the same positions:
     body = 'In your Lab Manual, refer to Lab X.Y: <title>' + key lines incl.
     the registry time (30 min each); notes copied verbatim.

Final slide count: 59 + 5 new - 6 dropped = 58 (in the 50-60 band; no flex trims).

Run:  ../../.venv-courseware/bin/python tools/build_brand_ch04.py
"""
from __future__ import annotations
import shutil
from pathlib import Path

from pptx_tools import open_deck, arrange, save

HERE = Path(__file__).resolve().parent
DECKS = HERE.parent / "decks"
SRC = DECKS / "_bak6" / "1258-Ch04-ModernGenAI-PromptEng.pptx"
OUT = DECKS / "1258-Ch04-ModernGenAI-PromptEng.pptx"

CHAPTER_NAME = "Modern GenAI and Prompt Engineering"
SUBTITLE = "Chapter 4"

OBJECTIVES = [
    "Navigate the 2026 model landscape: families, tiers, and context windows",
    "Apply core and advanced prompt techniques, from zero-shot to few-shot and chain-of-thought",
    "Use reasoning models deliberately, matching effort to task stakes and budget",
    "Produce structured outputs with roles, formats, and grounding",
    "Evaluate outputs with the rubric and government verification habits",
]

CONTENTS = [
    "The 2026 model landscape: families, tiers, and context windows",
    "Prompting fundamentals: elements, examples, and chain-of-thought",
    "Reasoning models and the effort control",
    "Output control: roles, formats, structured outputs, and grounding",
    "Evaluation and verification: rubrics, LLM-as-judge, government habits",
    "Demo 4.1: Zero-Shot, Few-Shot, Reasoning — Same Task — 10 min",
    "DO NOW 4.A: Add Two Examples — 10 min",
    "DO NOW 4.B: Give the Model a Job — 8 min",
    "DO NOW 4.C: Ask for the Shape You Need — 10 min",
    "DO NOW 4.D: Answer Only From This Document — 8 min",
    "Lab 4.1: Prompt Engineering Studio — 30 min",
    "Lab 4.2: Build a Reusable Prompt Template Library — 30 min",
]

LAB41_TITLE = "Lab 4.1: Prompt Engineering Studio"
LAB41_BODY = [
    "In your Lab Manual, refer to Lab 4.1: Prompt Engineering Studio",
    "Improve real outputs through iteration against a scoring rubric",
    "Ladder: zero-shot -> few-shot -> role + format contract -> reasoning-model comparison",
    "30 minutes",
]

LAB42_TITLE = "Lab 4.2: Build a Reusable Prompt Template Library"
LAB42_BODY = [
    "In your Lab Manual, refer to Lab 4.2: Build a Reusable Prompt Template Library",
    "Take your best prompt from Lab 4.1 and replace the specifics with [BRACKETED] slots",
    "Write it as a Python function taking those slots as arguments",
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


def _title(slide):
    return slide.shapes.title.text_frame.text.strip() if slide.shapes.title else ""


def _notes(slide):
    return slide.notes_slide.notes_text_frame.text if slide.has_notes_slide else ""


def main():
    shutil.copy(SRC, OUT)
    prs = open_deck(OUT)
    slides = list(prs.slides)
    assert len(slides) == 59, f"expected 59 slides, got {len(slides)}"

    # Sanity-check the slides being folded / rebuilt / dropped.
    assert _title(slides[0]) == CHAPTER_NAME, _title(slides[0])
    assert slides[0].slide_layout.name == "2_Chapter Title AI1"
    assert slides[1].slide_layout.name == "1_Section Title AI1"
    agenda_notes = _notes(slides[1])
    assert _title(slides[2]) == "Activities in This Chapter"
    assert _title(slides[3]) == "Activities in This Chapter"  # stale duplicate
    assert _title(slides[55]) == LAB41_TITLE
    assert _title(slides[56]) == LAB42_TITLE
    assert _title(slides[57]) == LAB42_TITLE  # exact duplicate
    lab41_notes = _notes(slides[55])
    lab42_notes = _notes(slides[56])

    # 1. Chapter Title on the standard Government layout
    t = prs.slides.add_slide(_layout(prs, "Chapter Title Government"))
    _ph(t, 0).text_frame.text = CHAPTER_NAME
    _ph(t, 1).text_frame.text = SUBTITLE

    # 2. Chapter Objectives (idx 15 is the displayed body on this layout)
    o = prs.slides.add_slide(_layout(prs, "Chapter Objectives"))
    _fill_body(_ph(o, 15), OBJECTIVES)

    # 3. Contents (folds the old slide-2 agenda; carries its note)
    c = prs.slides.add_slide(_layout(prs, "Content with Header. Full Page"))
    _ph(c, 0).text_frame.text = "Contents"
    _fill_body(_ph(c, 1), CONTENTS)
    if agenda_notes.strip():
        c.notes_slide.notes_text_frame.text = agenda_notes

    # 4. Lab rebuilds on 'Exercise Reference Slide with Typing Hands'
    l1 = prs.slides.add_slide(_layout(prs, "Exercise Reference Slide with Typing Hands"))
    _ph(l1, 0).text_frame.text = LAB41_TITLE
    _fill_body(_ph(l1, 1), LAB41_BODY)
    l1.notes_slide.notes_text_frame.text = lab41_notes

    l2 = prs.slides.add_slide(_layout(prs, "Exercise Reference Slide with Typing Hands"))
    _ph(l2, 0).text_frame.text = LAB42_TITLE
    _fill_body(_ph(l2, 1), LAB42_BODY)
    l2.notes_slide.notes_text_frame.text = lab42_notes

    # New slides are appended at 0-based 59..63. Keep/order:
    #   openers (59,60,61), activities overview (2), content (4..54),
    #   lab rebuilds (62,63), summary (58).
    # Dropped: 0 (old title), 1 (agenda), 3 (dup overview), 55 (old Lab 4.1),
    #          56, 57 (old Lab 4.2 x2).
    order0 = [59, 60, 61, 2] + list(range(4, 55)) + [62, 63, 58]
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
