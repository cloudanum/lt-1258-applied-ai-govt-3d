"""
build_brand_ch05.py — apply LT standard branding/structure to
1258-Ch05-Security-Risks-Responsible-AI.pptx
(Chapter 5 'AI Security, Risks, and Responsible AI').

Idempotent: always rebuilds from decks/_bak6/1258-Ch05-Security-Risks-Responsible-AI.pptx.

Changes (vs. 60-slide original):
  1. Slide 1 rebuilt on layout 'Chapter Title Government' (was
     '2_Chapter Title AI1'): CENTER_TITLE = chapter name, SUBTITLE =
     'Chapter 5'; speaker notes carried over verbatim.
  2. Slide 2 ('Chapter Objectives', already the right layout): body
     placeholder idx 15 rewritten with the four a4 chapter objectives;
     notes kept.
  3. New Contents slide on 'Content with Header. Full Page', inserted at
     position 3.
  4. Activity slides rebuilt on dedicated layouts, same position, title +
     speaker notes carried over:
       - slide 22 'Lab 5.1: Adversarial Examples and Model Robustness'
         (Content with Header. Full Page) -> 'Exercise Reference Slide
         with Typing Hands'; body = 'In your Lab Manual, refer to
         Lab 5.1: ...' + key lines + 30 min (registry/activities.yaml).
       - slide 33 'Lab 5.2: Detect and Mask PII in Citizen Records'
         -> same treatment.
       - slide 49 'DO NOW 5.C' (Workbook Reference Slide with Writing)
         -> 'Do Now with Typing Hands' (registry environment: vm);
         workbook pointer corrected to the a4 Lab Manual heading
         'DO NOW 5.C: Injection Red Team' (was the stale
         'Insider Threat Scenarios').
  5. Flex trim to stay in the 50-60 band after +1 net slide: old slide 13
     'AI Data Security: The Real Cost of Poisoning' (notes start with
     '[flex] ') dropped; poisoning depth remains covered by the
     surrounding 'Attacks on Predictive AI Systems' slides.

Final slide count: 60 (60 + 1 Contents - 1 flex trim; openers/activities
are 1:1 replacements).

Run:  ../../.venv-courseware/bin/python tools/build_brand_ch05.py
"""
from __future__ import annotations
import shutil
from pathlib import Path

from pptx_tools import open_deck, arrange, save

HERE = Path(__file__).resolve().parent
DECKS = HERE.parent / "decks"
SRC = DECKS / "_bak6" / "1258-Ch05-Security-Risks-Responsible-AI.pptx"
OUT = DECKS / "1258-Ch05-Security-Risks-Responsible-AI.pptx"

CHAPTER_NAME = "AI Security, Risks, and Responsible AI"
SUBTITLE = "Chapter 5"

OBJECTIVES = [
    "Map the AI attack surface using NIST AI 100-2e2025",
    "Explain prompt injection and why it can't be patched",
    "Protect PII — masking vs. de-identification",
    "Navigate the 2026 federal policy spine and the EU AI Act",
]

CONTENTS = [
    "5.1 The AI Attack Surface — Four Dimensions of Vulnerability",
    "5.2 Attacks on Predictive AI and Adversarial ML",
    "5.3 Attacks on Generative AI and Prompt Injection",
    "5.4 Data Privacy, PII, and De-identification",
    "5.5 Responsible AI and Insider Threats",
    "5.6 Policy and Regulation: The Federal Spine and the EU AI Act",
    "Activities: Demo 5.1, DO NOW 5.A–5.D, Labs 5.1–5.2",
]

LAB51_BODY = [
    "In your Lab Manual, refer to Lab 5.1: Adversarial Examples and Model Robustness",
    "Train a small classifier, then break it on purpose",
    "Find the smallest perturbation that flips a prediction, then apply one defence and re-measure",
    "Time: 30 minutes",
]

LAB52_BODY = [
    "In your Lab Manual, refer to Lab 5.2: Detect and Mask PII in Citizen Records",
    "Run a detector over synthetic records and real 311 free text; find three items it misses",
    "Mask without destroying analytic value; report residual risk",
    "Time: 30 minutes",
]

DONOW5C_BODY = [
    "In your Lab Manual, refer to DO NOW 5.C: Injection Red Team",
]

# 0-based indices in the ORIGINAL 60-slide deck
IDX_TITLE, IDX_OBJECTIVES = 0, 1
IDX_FLEX_TRIM = 12          # 'AI Data Security: The Real Cost of Poisoning'
IDX_LAB51, IDX_LAB52, IDX_DONOW = 21, 32, 48


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
    tf.clear()
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line


def _notes(slide):
    return slide.notes_slide.notes_text_frame.text if slide.has_notes_slide else ""


def main():
    shutil.copy(SRC, OUT)
    prs = open_deck(OUT)
    slides = list(prs.slides)
    assert len(slides) == 60, f"expected 60 slides, got {len(slides)}"

    # Capture content to carry over before any rebuild.
    old1 = slides[IDX_TITLE]
    old1_title = old1.shapes.title.text_frame.text
    old1_sub = _ph(old1, 1).text_frame.text
    old1_notes = _notes(old1)
    assert old1_title == CHAPTER_NAME, old1_title
    lab51_title = slides[IDX_LAB51].shapes.title.text_frame.text
    lab51_notes = _notes(slides[IDX_LAB51])
    assert lab51_title.startswith("Lab 5.1:"), lab51_title
    lab52_title = slides[IDX_LAB52].shapes.title.text_frame.text
    lab52_notes = _notes(slides[IDX_LAB52])
    assert lab52_title.startswith("Lab 5.2:"), lab52_title
    donow_title = slides[IDX_DONOW].shapes.title.text_frame.text
    donow_notes = _notes(slides[IDX_DONOW])
    assert donow_title.startswith("DO NOW"), donow_title
    assert _notes(slides[IDX_FLEX_TRIM]).startswith("[flex]")

    # 1. Chapter Title on 'Chapter Title Government'
    t = prs.slides.add_slide(_layout(prs, "Chapter Title Government"))
    _ph(t, 0).text_frame.text = old1_title
    _ph(t, 1).text_frame.text = old1_sub
    t.notes_slide.notes_text_frame.text = old1_notes

    # 2. Chapter Objectives: rewrite body idx 15 in place (right layout already)
    _fill_body(_ph(slides[IDX_OBJECTIVES], 15), OBJECTIVES)

    # 3. Contents
    c = prs.slides.add_slide(_layout(prs, "Content with Header. Full Page"))
    _ph(c, 0).text_frame.text = "Contents"
    _fill_body(_ph(c, 1), CONTENTS)

    # 4. Activity rebuilds on dedicated layouts
    e1 = prs.slides.add_slide(_layout(prs, "Exercise Reference Slide with Typing Hands"))
    _ph(e1, 0).text_frame.text = lab51_title
    _fill_body(_ph(e1, 1), LAB51_BODY)
    e1.notes_slide.notes_text_frame.text = lab51_notes

    e2 = prs.slides.add_slide(_layout(prs, "Exercise Reference Slide with Typing Hands"))
    _ph(e2, 0).text_frame.text = lab52_title
    _fill_body(_ph(e2, 1), LAB52_BODY)
    e2.notes_slide.notes_text_frame.text = lab52_notes

    d = prs.slides.add_slide(_layout(prs, "Do Now with Typing Hands"))
    _ph(d, 0).text_frame.text = donow_title
    _fill_body(_ph(d, 1), DONOW5C_BODY)
    d.notes_slide.notes_text_frame.text = donow_notes

    # New slides appended at 0-based 60..64: title, contents, lab51, lab52, donow
    NEW_TITLE, NEW_CONTENTS, NEW_LAB51, NEW_LAB52, NEW_DONOW = 60, 61, 62, 63, 64
    order0 = [NEW_TITLE, IDX_OBJECTIVES, NEW_CONTENTS]
    for i in range(2, 60):
        if i == IDX_FLEX_TRIM:
            continue                                # flex trim
        if i == IDX_LAB51:
            order0.append(NEW_LAB51)
        elif i == IDX_LAB52:
            order0.append(NEW_LAB52)
        elif i == IDX_DONOW:
            order0.append(NEW_DONOW)
        else:
            order0.append(i)
    assert len(order0) == 60, len(order0)
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
