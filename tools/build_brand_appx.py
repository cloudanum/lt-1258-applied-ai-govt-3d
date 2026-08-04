"""
build_brand_appx.py — apply LT standard branding/structure to the four 1258
appendix decks (rev a4):

  1258-AppA-ML-LifeCycle.pptx              (24 -> 25 slides)
  1258-AppB-Security-DeepDive.pptx         (22 -> 23 slides)
  1258-AppC-Transformer-LLM-Internals.pptx (29 -> 30 slides)
  1258-AppD-Classic-ML-DeepDive.pptx       (20 -> 21 slides)

Idempotent: always rebuilds from decks/_bak6/<deck>.

Per deck:
  1. New opener slide on layout 'Chapter Title Government':
     CENTER_TITLE (idx 0) = appendix name, SUBTITLE (idx 1) = 'Appendix X'.
     The old slide 1 (a title-acting slide on '2_Chapter Title AI1') duplicates
     this opener, so it is dropped; its speaker notes (AppB jogger text) are
     folded into the new opener's notes.
  2. New 'Chapter Objectives' slide, 4-6 bullets in body placeholder idx 15.
     (No Contents slide for appendices.)
  3. Activity slides rebuilt on dedicated layouts at the same position;
     title + speaker notes carried over:
       AppA s23 'Optional Lab A.1'  -> Exercise Reference Slide with Typing Hands
       AppB s8  'Lab B.1'           -> Exercise Reference Slide with Typing Hands
       AppB s11 'DO NOW: Score Toxicity Like a Moderator'
                                    -> Do Now with Typing Hands (bullets verbatim)
       AppD s4  'Lab 1.2'           -> Exercise Reference Slide with Typing Hands
       AppD s8  'Lab 1.1'           -> Exercise Reference Slide with Typing Hands
     Lab bodies use the canonical 'In your Lab Manual, refer to Lab X.Y: <title>'
     plus the lab's time. Lab titles/times come from registry/activities.yaml
     (Lab 1.1/1.2, both 30 min) and registry/labs.yaml (Optional Lab A.1/B.1,
     both 30 min) — the AppD deck bodies still named the retired pre-a4 labs,
     and their notes (carried over) document the a4 repointing.

Run:  ../../.venv-courseware/bin/python tools/build_brand_appx.py
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pptx_tools import open_deck, arrange, save  # noqa: E402

DECKS = Path(__file__).resolve().parent.parent / "decks"
BAK = DECKS / "_bak6"


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


def _fill_lines(ph, lines):
    tf = ph.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line


def _notes(slide):
    return slide.notes_slide.notes_text_frame.text if slide.has_notes_slide else ""


def _body_lines(slide):
    """Paragraph texts of the largest non-title placeholder."""
    body = None
    for ph in slide.placeholders:
        if ph.placeholder_format.idx != 0 and ph.has_text_frame:
            if body is None or (ph.width or 0) * (ph.height or 0) > (body.width or 0) * (body.height or 0):
                body = ph
    if body is None:
        return []
    return [p.text for p in body.text_frame.paragraphs if p.text.strip()]


def build(deck, orig_count, name, subtitle, objectives, activities, order0):
    """activities: list of (orig_index0, new_layout, title, body_lines_or_None).
    body_lines=None means copy the old slide's body verbatim."""
    src = BAK / deck
    out = DECKS / deck
    shutil.copy(src, out)
    prs = open_deck(out)
    slides = list(prs.slides)
    n0 = len(slides)
    assert n0 == orig_count, f"{deck}: expected {orig_count} slides, got {n0}"

    # 1. Chapter Title (folds old slide 1 notes)
    old1_notes = _notes(slides[0])
    t = prs.slides.add_slide(_layout(prs, "Chapter Title Government"))
    _ph(t, 0).text_frame.text = name
    _ph(t, 1).text_frame.text = subtitle
    if old1_notes.strip():
        t.notes_slide.notes_text_frame.text = old1_notes

    # 2. Chapter Objectives (idx 15 is the displayed body on this layout)
    o = prs.slides.add_slide(_layout(prs, "Chapter Objectives"))
    _fill_lines(_ph(o, 15), objectives)

    # 3. Activity rebuilds (appended after the two openers, in given order)
    for orig0, layout_name, title, body in activities:
        old = slides[orig0]
        old_notes = _notes(old)
        if body is None:
            body = _body_lines(old)
        s = prs.slides.add_slide(_layout(prs, layout_name))
        _ph(s, 0).text_frame.text = title
        _fill_lines(_ph(s, 1), body)
        if old_notes.strip():
            s.notes_slide.notes_text_frame.text = old_notes

    arrange(prs, order0)
    save(prs, out)

    prs2 = open_deck(out)
    print(f"saved {out.name} ({len(list(prs2.slides))} slides)")


EX = "Exercise Reference Slide with Typing Hands"
DN = "Do Now with Typing Hands"

# ----------------------------------------------------------------- AppA ---- #
def appa():
    activities = [(
        22, EX, "Optional Lab A.1",
        ["In your Lab Manual, refer to Lab A.1: Ideating AI Use Cases",
         "Optional self-study · 30 minutes"],
    )]
    # title, objectives, orig 2..22, new lab, orig 24
    order0 = [24, 25] + list(range(1, 22)) + [26] + [23]
    build(
        "1258-AppA-ML-LifeCycle.pptx", 24,
        "Machine Learning Life Cycle Core Principles", "Appendix A",
        [
            "Describe the phases of a machine learning project life cycle",
            "Apply data-driven decision making and iterative improvement principles",
            "Identify AI opportunities in your department with structured ideation",
            "Evaluate and prioritize AI use cases with a feasibility matrix",
            "Map workflows and define actionable next steps for AI adoption",
        ],
        activities, order0,
    )


# ----------------------------------------------------------------- AppB ---- #
def appb():
    activities = [
        (7, EX, "Lab B.1",
         ["In your Lab Manual, refer to Lab B.1: Chronicle SIEM: Real-Time Cyber Threat Analysis",
          "30 minutes"]),
        (10, DN, "DO NOW: Score Toxicity Like a Moderator", None),  # body verbatim
    ]
    # title, objectives, orig 2..7, lab, orig 9..10, do-now, orig 12..22
    order0 = [22, 23] + list(range(1, 7)) + [24] + list(range(8, 10)) + [25] + list(range(11, 22))
    build(
        "1258-AppB-Security-DeepDive.pptx", 22,
        "Challenges and Ethical Considerations", "Appendix B",
        [
            "Describe the Google Secure AI Framework (SAIF)",
            "Explain how Chronicle SIEM detects and contextualizes threats in real time",
            "Apply Zero Trust principles to generative AI systems and content",
            "Assess Google Workspace AI data protection and digital sovereignty controls",
            "Weigh the costs of moderation false positives and false negatives",
            "Outline AI governance and ethical guidelines for public sector use",
        ],
        activities, order0,
    )


# ----------------------------------------------------------------- AppC ---- #
def appc():
    order0 = [29, 30] + list(range(1, 29))
    build(
        "1258-AppC-Transformer-LLM-Internals.pptx", 29,
        "Building Block of Generative AI", "Appendix C",
        [
            "Explain how sequential data shaped RNN and Seq2Seq architectures",
            "Describe the information bottleneck and how attention resolves it",
            "Distinguish encoder, decoder, and encoder-decoder transformer variants",
            "Explain BERT's masked language modeling and embeddings",
            "Contrast GPT and BERT architectures, training, and use cases",
            "Recognize how LangChain prompt templates enhance NLP workflows",
        ],
        [], order0,
    )


# ----------------------------------------------------------------- AppD ---- #
def appd():
    activities = [
        (3, EX, "Lab 1.2",
         ["In your Lab Manual, refer to Lab 1.2: Clustering Counties by Air Quality (K-Means)",
          "30 minutes"]),
        (7, EX, "Lab 1.1",
         ["In your Lab Manual, refer to Lab 1.1: Exploring the Federal AI Use Case Inventory",
          "30 minutes"]),
    ]
    # title, objectives, orig 2..3, lab1.2, orig 5..7, lab1.1, orig 9..20
    order0 = [20, 21] + list(range(1, 3)) + [22] + list(range(4, 7)) + [23] + list(range(8, 20))
    build(
        "1258-AppD-Classic-ML-DeepDive.pptx", 20,
        "Classic ML and Data Engineering Deep Dive", "Appendix D",
        [
            "Apply decision trees and random forests to classification problems",
            "Distinguish supervised and unsupervised machine learning",
            "Represent text numerically with Word2Vec and GloVe embeddings",
            "Explain why deep learning suits high-dimensional, non-linear data",
            "Describe how artificial neural networks learn",
            "Identify Vision AI use cases across public sectors",
        ],
        activities, order0,
    )


if __name__ == "__main__":
    appa()
    appb()
    appc()
    appd()
