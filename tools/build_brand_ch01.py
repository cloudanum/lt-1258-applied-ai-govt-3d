"""
build_brand_ch01.py — apply LT standard branding/structure to
1258-Ch01-AI-ML-Foundations.pptx (Chapter 1 'AI & ML Foundations for Government').

Idempotent: always rebuilds from decks/_bak6/1258-Ch01-AI-ML-Foundations.pptx.

Changes (vs. 57-slide original):
  1. New Chapter Title slide (layout 'Chapter Title Government'):
     CENTER_TITLE (idx 0) = chapter name, SUBTITLE (idx 1) = 'Chapter 1'.
     Replaces old slide 1, which sat on the wrong title layout
     ('2_Chapter Title AI1'); it had no notes/bullets to fold.
  2. New Chapter Objectives slide (layout 'Chapter Objectives'), body idx 15,
     4 standard bullets. Old slide 2 (legacy 8-line objectives on the same
     layout) duplicates the opener: its lines + speaker notes are folded into
     the new slide's notes and the old slide is dropped.
  3. New Contents slide (layout 'Content with Header. Full Page'): section
     lines + the chapter's activities (Demo 1.1, DO NOW 1.A-1.D, Labs 1.1-1.2,
     times from registry/activities.yaml).
  4. 'Activities in This Chapter' overview KEPT on its content layout — but the
     deck held TWO adjacent copies (old slides 3 and 4). Old slide 4 is stale
     (40-min labs / 125-min budget contradict the registry's 30 min / 105 min),
     so it is dropped; the registry-accurate copy (old slide 3) stays.
  5. Lab 1.1 rebuilt on 'Exercise Reference Slide with Typing Hands' at old
     slide 24's position. Old slide 24 (content layout) dropped; old slide 25
     (a botched 'Workbook Reference Slide with Writing' with title/body swapped)
     dropped, its disclaimer caption folded into the new slide's notes.
  6. Lab 1.2 rebuilt on 'Exercise Reference Slide with Typing Hands' at old
     slide 55's position. Old slides 55 and 56 were near-identical launchers
     (40 min vs. registry-correct 30 min); both dropped, one new slide added.

Final slide count: 57 - 7 dropped + 5 added = 55 (in the 50-60 band; no
[flex] trims needed).

Run:  ../../.venv-courseware/bin/python tools/build_brand_ch01.py
"""
from __future__ import annotations
import shutil
from pathlib import Path

from pptx_tools import open_deck, arrange, save

HERE = Path(__file__).resolve().parent
DECKS = HERE.parent / "decks"
SRC = DECKS / "_bak6" / "1258-Ch01-AI-ML-Foundations.pptx"
OUT = DECKS / "1258-Ch01-AI-ML-Foundations.pptx"

CHAPTER_NAME = "AI and ML Foundations for Government"
SUBTITLE = "Chapter 1"

OBJECTIVES = [
    "Distinguish AI, machine learning, deep learning, and generative AI",
    "Explain classic ML at the concept level: clustering, decision trees, and random forests",
    "Run an AI project using CRISP-DM",
    "Read federal AI adoption numbers and what they mean for your agency",
]

CONTENTS = [
    "Taxonomy & History: AI, ML, Deep Learning, Generative AI",
    "Why AI Matters in Government",
    "Classic ML: Clustering, Decision Trees, Random Forests",
    "NLP Bridge: Text, Vision, and Unstructured Data",
    "How an AI Project Runs: CRISP-DM",
    "Demo 1.1: Supervised, Unsupervised, Generative — One Dataset (10 min)",
    "DO NOW 1.A: Explain It to a CIO, Then to a Citizen (10 min)",
    "DO NOW 1.B: Classic ML or GenAI? (7 min)",
    "DO NOW 1.C: Prompt It or Train It? (10 min)",
    "DO NOW 1.D: Find Your Agency in the Inventory (8 min)",
    "Lab 1.1: Exploring the Federal AI Use Case Inventory (30 min)",
    "Lab 1.2: Clustering Counties by Air Quality (K-Means) (30 min)",
]

LAB11_TITLE = "Lab 1.1: Exploring the Federal AI Use Case Inventory"
LAB11_BODY = [
    "In your Lab Manual, refer to Lab 1.1: Exploring the Federal AI Use Case Inventory",
    "Load the real OMB inventory — 1,500+ federal AI use cases; group by agency, development stage, and high-impact flag",
    "Write three findings, each with the code that produced it",
    "30 minutes",
]

LAB12_TITLE = "Lab 1.2: Clustering Counties by Air Quality (K-Means)"
LAB12_BODY = [
    "In your Lab Manual, refer to Lab 1.2: Clustering Counties by Air Quality (K-Means)",
    "Open lab_1.2_clustering.ipynb and load epa_aqi_by_county.csv; scale the numeric day-count columns",
    "Fit K-Means with k=3; print each cluster's size and column means",
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


def _notes(slide):
    return slide.notes_slide.notes_text_frame.text if slide.has_notes_slide else ""


def main():
    shutil.copy(SRC, OUT)
    prs = open_deck(OUT)
    slides = list(prs.slides)
    assert len(slides) == 57, f"expected 57 slides, got {len(slides)}"

    # Capture content to carry over before any rebuild.
    assert slides[0].placeholders[0].text_frame.text.strip() == CHAPTER_NAME
    old2_lines = [p.text for p in slides[1].placeholders[15].text_frame.paragraphs if p.text.strip()]
    old2_notes = _notes(slides[1])
    assert slides[3].placeholders[0].text_frame.text.strip() == "Activities in This Chapter"
    assert slides[23].placeholders[0].text_frame.text.strip() == LAB11_TITLE
    lab11_notes = _notes(slides[23])
    lab11_caption = slides[24].placeholders[12].text_frame.text.strip()  # old slide 25 disclaimer
    assert slides[54].placeholders[0].text_frame.text.strip() == LAB12_TITLE
    lab12_notes = _notes(slides[54])

    # 1. Chapter Title (replaces old slide 1 on the correct Government layout)
    t = prs.slides.add_slide(_layout(prs, "Chapter Title Government"))
    _ph(t, 0).text_frame.text = CHAPTER_NAME
    _ph(t, 1).text_frame.text = SUBTITLE

    # 2. Chapter Objectives (folds old slide 2: legacy lines + notes -> notes)
    o = prs.slides.add_slide(_layout(prs, "Chapter Objectives"))
    _fill_body(_ph(o, 15), OBJECTIVES)
    o.notes_slide.notes_text_frame.text = "\n".join(
        [old2_notes.rstrip(), "", "Framing (from the original objectives slide):"] + old2_lines
    ).strip()

    # 3. Contents
    c = prs.slides.add_slide(_layout(prs, "Content with Header. Full Page"))
    _ph(c, 0).text_frame.text = "Contents"
    _fill_body(_ph(c, 1), CONTENTS)

    # 4. Lab 1.1 -> Exercise Reference Slide with Typing Hands
    l1 = prs.slides.add_slide(_layout(prs, "Exercise Reference Slide with Typing Hands"))
    _ph(l1, 0).text_frame.text = LAB11_TITLE
    _fill_body(_ph(l1, 1), LAB11_BODY)
    l1.notes_slide.notes_text_frame.text = "\n".join(
        x for x in [lab11_notes.rstrip(), lab11_caption] if x
    )

    # 5. Lab 1.2 -> Exercise Reference Slide with Typing Hands
    l2 = prs.slides.add_slide(_layout(prs, "Exercise Reference Slide with Typing Hands"))
    _ph(l2, 0).text_frame.text = LAB12_TITLE
    _fill_body(_ph(l2, 1), LAB12_BODY)
    l2.notes_slide.notes_text_frame.text = lab12_notes

    # Order (0-based originals 0..56; new slides appended at 57..61):
    #   openers 57,58,59; overview orig 2; orig 4..22; lab1.1 (60) at old pos 24;
    #   orig 25..53; lab1.2 (61) at old pos 55; recap orig 56.
    # Dropped: 0 (old title), 1 (old objectives, folded), 3 (stale overview dup),
    #          23+24 (old Lab 1.1 pair), 54+55 (old Lab 1.2 dup pair).
    order0 = (
        [57, 58, 59]
        + [2]
        + list(range(4, 23))
        + [60]
        + list(range(25, 54))
        + [61]
        + [56]
    )
    arrange(prs, order0)
    save(prs, OUT)

    # quick echo
    prs2 = open_deck(OUT)
    print(f"saved {OUT} ({len(list(prs2.slides))} slides)")
    for i, s in enumerate(prs2.slides):
        title = s.shapes.title.text_frame.text.replace("\n", " ")[:60] if s.shapes.title else "(no title)"
        print(f"{i+1:>2} [{s.slide_layout.name}] {title}")


if __name__ == "__main__":
    main()
