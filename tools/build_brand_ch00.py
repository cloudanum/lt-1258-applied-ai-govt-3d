"""
build_brand_ch00.py — apply LT standard branding/structure to
1258-Ch00-Course-Launch.pptx (Chapter 0 'Course Launch & Lab Environment').

Idempotent: always rebuilds from decks/_bak6/1258-Ch00-Course-Launch.pptx.

Changes (vs. 54-slide original):
  1. New Chapter Title slide (layout 'Chapter Title Government'):
     CENTER_TITLE = chapter name, SUBTITLE = 'Chapter 0'. The old slide 1
     ('Introduction and Overview', a title-acting slide on layout
     '2_Chapter Title AI1') is folded into the opener notes and dropped.
  2. New Course Objectives slide (layout 'Course Objectives', body idx 15).
     Replaces old slide 2 'Course Launch: Objectives' (wrong layout); its
     bullets are reworked to the four stated launch objectives and its
     speaker notes are carried over.
  3. New Contents slide (layout 'Content with Header. Full Page'):
     section lines + the chapter's activities with times from
     registry/activities.yaml.
  4. Old slide 4 'Activities in This Chapter' dropped: stale duplicate of
     slide 3 (Lab 0.1 listed as 25 min; registry and slide 3 say 20 min).
     Slide 3 (registry-matching) is KEPT on its content layout.
  5. Activity rebuilds (title + bullets + notes copied verbatim, same
     sequence position, old slide dropped):
       - 'DO NOW 0.1: The Next 15 Minutes'  Content w/ Header -> Do Now with Typing Hands
       - 'DO NOW: Run the Healthcheck'      Content w/ Header -> Do Now with Typing Hands
       - 'Lab 0.1: Course Environment and Data Tour' (two duplicate slides,
         25- and 20-minute variants) -> ONE 'Exercise Reference Slide with
         Typing Hands': 'In your Lab Manual, refer to Lab 0.1: ...' + key
         lines incl. the registry time (20 min). Both old slides dropped.
     Note: slides 'Lab Environment Tour: JupyterLab' / '...Notebooks and
     Data Files' start with 'Lab' but are environment-tour CONTENT (part of
     the DO NOW 0.1 walkthrough, no lab to reference) — left untouched.

Final slide count: 54 - 4 drops + 3 openers = 53 (in the 50-60 band; no
flex trims needed).

Run:  ../../.venv-courseware/bin/python tools/build_brand_ch00.py
"""
from __future__ import annotations
import shutil
from pathlib import Path

from pptx_tools import open_deck, arrange, save

HERE = Path(__file__).resolve().parent
DECKS = HERE.parent / "decks"
SRC = DECKS / "_bak6" / "1258-Ch00-Course-Launch.pptx"
OUT = DECKS / "1258-Ch00-Course-Launch.pptx"

CHAPTER_NAME = "Course Launch & Lab Environment"
SUBTITLE = "Chapter 0"

OBJECTIVES = [
    "Get your CloudShare lab environment running and verified — every attendee at a running Jupyter (DO NOW 0.1)",
    "Know what this course will make of you as an AI user — and what it won't",
    "Name the data rule that governs which AI account you use this week",
    "See the three-day course map and the prompting spine (P0 to P10)",
    "Understand the activity rhythm: demos, DO NOWs, labs, and debriefs",
]

CONTENTS = [
    "Welcome: Who This Course Is For",
    "Your Lab Environment: CloudShare and JupyterLab",
    "AI Accounts and Data Rules",
    "How We Learn: Bloom's Taxonomy",
    "Course Map: Three Days at a Glance",
    "The Activity Rhythm: Learn, Do, Debrief",
    "Demo 0.1: Your Lab Environment, End to End — 10 min",
    "DO NOW 0.1: Environment Healthcheck — 15 min",
    "DO NOW 0.2: Your First Prompt (Baseline Card) — 5 min",
    "DO NOW 0.3: Which Account, Which Data? — 8 min",
    "DO NOW 0.4: AI Already in Your Day — 7 min [flex]",
    "Lab 0.1: Course Environment and Data Tour — 20 min",
]

# 1-based positions in the ORIGINAL deck
IDX_OLD_TITLE = 1        # 'Introduction and Overview' (title-acting) -> fold + drop
IDX_OLD_OBJECTIVES = 2   # 'Course Launch: Objectives' -> rebuilt as Course Objectives opener
IDX_ACTIVITIES_KEEP = 3  # 'Activities in This Chapter' (registry-matching) -> KEEP
IDX_ACTIVITIES_DUP = 4   # stale duplicate -> drop
IDX_DONOW_A = 25         # 'DO NOW 0.1: The Next 15 Minutes'
IDX_DONOW_B = 33         # 'DO NOW: Run the Healthcheck'
IDX_LAB_A = 52           # 'Lab 0.1 ...' (25-min stale variant)
IDX_LAB_B = 53           # 'Lab 0.1 ...' (20-min registry variant)


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


def _slide_lines(slide):
    """Title text, body (text, level) paragraphs from the main non-title
    placeholder, notes."""
    title = slide.shapes.title.text_frame.text if slide.shapes.title else ""
    body = None
    for ph in slide.placeholders:
        if ph.placeholder_format.idx != 0 and ph.has_text_frame:
            if body is None or (ph.width or 0) * (ph.height or 0) > (body.width or 0) * (body.height or 0):
                body = ph
    bullets = [(p.text, p.level) for p in body.text_frame.paragraphs if p.text.strip()] if body is not None else []
    notes = slide.notes_slide.notes_text_frame.text if slide.has_notes_slide else ""
    return title, bullets, notes


def _fill_body_leveled(ph, bullets):
    tf = ph.text_frame
    tf.word_wrap = True
    for i, (text, level) in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = text
        p.level = level


def main():
    shutil.copy(SRC, OUT)
    prs = open_deck(OUT)
    slides = list(prs.slides)
    assert len(slides) == 54, f"expected 54 slides, got {len(slides)}"

    # Capture content to carry over before any rebuild.
    s1_title, _, s1_notes = _slide_lines(slides[IDX_OLD_TITLE - 1])
    assert s1_title == "Introduction and Overview", s1_title
    s2_title, _, s2_notes = _slide_lines(slides[IDX_OLD_OBJECTIVES - 1])
    assert s2_title == "Course Launch: Objectives", s2_title
    s25_title, s25_bullets, s25_notes = _slide_lines(slides[IDX_DONOW_A - 1])
    assert s25_title.startswith("DO NOW"), s25_title
    s33_title, s33_bullets, s33_notes = _slide_lines(slides[IDX_DONOW_B - 1])
    assert s33_title.startswith("DO NOW"), s33_title
    lab_title, _, lab_notes = _slide_lines(slides[IDX_LAB_B - 1])  # 20-min registry variant
    assert lab_title.startswith("Lab 0.1"), lab_title

    # 1. Chapter Title (folds old slide 1 into notes)
    t = prs.slides.add_slide(_layout(prs, "Chapter Title Government"))
    _ph(t, 0).text_frame.text = CHAPTER_NAME
    _ph(t, 1).text_frame.text = SUBTITLE
    t.notes_slide.notes_text_frame.text = "\n".join(
        [
            "Standard chapter opener (Chapter Title Government).",
            f"Folded and dropped the original title-acting slide 1, '{s1_title}' "
            "(was on layout '2_Chapter Title AI1'; no bullets or notes of its own).",
            s1_notes,
            "Chapter 0, Day 1 AM: course launch — welcome and introductions, the lab "
            "environment (CloudShare + JupyterLab), AI accounts and the data rule, how "
            "we learn (Bloom's), the three-day course map, and the chapter's activities.",
        ]
    ).strip()

    # 2. Course Objectives (idx 15 is the displayed body on this layout);
    #    carries old slide 2's speaker notes.
    o = prs.slides.add_slide(_layout(prs, "Course Objectives"))
    _fill_body(_ph(o, 15), OBJECTIVES)
    o.notes_slide.notes_text_frame.text = s2_notes

    # 3. Contents
    c = prs.slides.add_slide(_layout(prs, "Content with Header. Full Page"))
    _ph(c, 0).text_frame.text = "Contents"
    _fill_body(_ph(c, 1), CONTENTS)
    c.notes_slide.notes_text_frame.text = (
        "Chapter contents (standard opener). Sections follow the deck flow; "
        "activity times from registry/activities.yaml."
    )

    # 4. Activity rebuilds on dedicated layouts (same sequence position).
    d1 = prs.slides.add_slide(_layout(prs, "Do Now with Typing Hands"))
    _ph(d1, 0).text_frame.text = s25_title
    _fill_body_leveled(_ph(d1, 1), s25_bullets)
    d1.notes_slide.notes_text_frame.text = s25_notes

    d2 = prs.slides.add_slide(_layout(prs, "Do Now with Typing Hands"))
    _ph(d2, 0).text_frame.text = s33_title
    _fill_body_leveled(_ph(d2, 1), s33_bullets)
    d2.notes_slide.notes_text_frame.text = s33_notes

    lab = prs.slides.add_slide(_layout(prs, "Exercise Reference Slide with Typing Hands"))
    _ph(lab, 0).text_frame.text = lab_title
    _fill_body(_ph(lab, 1), [
        "In your Lab Manual, refer to Lab 0.1: Course Environment and Data Tour",
        "Open lab_0.1_environment_tour.ipynb — run the environment cell, then the data inventory cell",
        "20 minutes",
    ])
    lab.notes_slide.notes_text_frame.text = lab_notes

    # Order (0-based indices into the deck AFTER appending; appended are
    # 54=title, 55=objectives, 56=contents, 57=donowA, 58=donowB, 59=lab).
    # Kept originals: drop idx 0 (old title), 1 (old objectives),
    # 3 (stale activities dup), 24/32 (old DO NOWs), 51/52 (old lab pair).
    order0 = (
        [54, 55, 56]                 # openers
        + [2]                        # Activities in This Chapter (kept)
        + list(range(4, 24))         # slides 5..24
        + [57]                       # DO NOW 0.1 rebuilt (was slide 25)
        + list(range(25, 32))        # slides 26..32
        + [58]                       # DO NOW healthcheck rebuilt (was slide 33)
        + list(range(33, 51))        # slides 34..51
        + [59]                       # Lab 0.1 exercise reference (was slides 52-53)
        + [53]                       # slide 54 checkpoint
    )
    arrange(prs, order0)
    save(prs, OUT)

    # quick echo
    prs2 = open_deck(OUT)
    n = len(list(prs2.slides))
    print(f"saved {OUT} ({n} slides)")
    assert n == 53, n
    for i, s in enumerate(prs2.slides):
        title = s.shapes.title.text_frame.text.replace("\n", " ")[:58] if s.shapes.title else "(no title)"
        print(f"{i+1:>2} [{s.slide_layout.name}] {title}")


if __name__ == "__main__":
    main()
