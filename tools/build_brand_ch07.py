"""
build_brand_ch07.py — apply LT standard branding/structure to
1258-Ch07-Building-with-LLMs.pptx (Chapter 7 'Building with LLMs: APIs, RAG, and Agents').

Idempotent: always rebuilds from decks/_bak6/1258-Ch07-Building-with-LLMs.pptx.

Changes (vs. 58-slide original):
  1. Chapter Title rebuilt on layout 'Chapter Title Government'
     (old slide 1 was a title slide on '2_Chapter Title AI1' — python-pptx
     cannot change a slide's layout, so it is rebuilt; title/subtitle/notes
     carried over verbatim).
  2. New Chapter Objectives slide (layout 'Chapter Objectives'), body idx 15.
  3. New Contents slide (layout 'Content with Header. Full Page').
  4. Duplicate 'Activities in This Chapter' overview dropped (old slides 3+4
     were identical-titled duplicates with contradictory lab times; old slide 3
     matches registry/activities.yaml durations and is kept on its content
     layout, per the standard).
  5. Lab slides rebuilt on 'Exercise Reference Slide with Typing Hands' at the
     same positions; title + speaker notes verbatim, body replaced with the
     Lab Manual reference line + key lines incl. time from the registry:
       old 15 'Lab 7.1: First Calls with the OpenAI API'    (30 min)
       old 34 'Lab 7.2: RAG over Government Documents'      (30 min)
       old 51 'Lab 7.3: Build an AI Agent (Capstone)'       (45 min)

Final slide count: 58 + 3 openers - 1 old title - 1 duplicate overview = 59.

Run:  ../../../.venv-courseware/bin/python tools/build_brand_ch07.py
   (from 1258/1258a4-author-input/)
"""
from __future__ import annotations
import shutil
from pathlib import Path

from pptx_tools import open_deck, arrange, save

HERE = Path(__file__).resolve().parent
DECKS = HERE.parent / "decks"
SRC = DECKS / "_bak6" / "1258-Ch07-Building-with-LLMs.pptx"
OUT = DECKS / "1258-Ch07-Building-with-LLMs.pptx"

CHAPTER_NAME = "Building with LLMs: APIs, RAG, and Agents"
SUBTITLE = "Chapter 7"

OBJECTIVES = [
    "Make your first LLM API calls — current SDK, key in an environment variable",
    "Build a RAG pipeline over government documents, with citations",
    "Explain agent loops and the guardrails that keep agents in bounds",
    "Choose prompting vs. RAG vs. fine-tuning with the decision matrix",
]

CONTENTS = [
    "From 2018 to Now: A Short Timeline",
    "LLM APIs and Structured Outputs",
    "LLM Application Architecture: Frameworks and MCP",
    "RAG: Retrieval-Augmented Generation",
    "Agentic AI: Loops, Tools, and Guardrails",
    "Fine-Tuning and the Decision Matrix",
    "Hugging Face and the Open Ecosystem",
    "Demo 7.1: One API Call, Dissected — 10 min",
    "DO NOW 7.A–7.D: Hugging Face tour; cost at agency scale; prompt as code; where RAG fails",
    "Lab 7.1: First Calls with the OpenAI API — 30 min",
    "Lab 7.2: RAG over Government Documents — 30 min",
    "Lab 7.3: Citizen Services Triage Agent (Capstone) — 45 min",
]

# old 1-based positions of the lab slides
LABS = {
    15: {
        "title": "Lab 7.1: First Calls with the OpenAI API",
        "body": [
            "In your Lab Manual, refer to Lab 7.1: First Calls with the OpenAI API",
            "30 minutes — VM notebook (lab_7.1_openai_api.ipynb); needs your OpenAI key",
            "Make working chat calls; vary the system prompt and temperature; get structured JSON out of a real government memo",
            "Read token usage and estimate cost at agency scale",
        ],
    },
    34: {
        "title": "Lab 7.2: RAG over Government Documents",
        "body": [
            "In your Lab Manual, refer to Lab 7.2: RAG over Government Documents",
            "30 minutes — VM notebook (lab_7.2_rag_gov_docs.ipynb) over four public agency policy documents",
            "Build the chunk -> embed -> retrieve -> answer pipeline; compare a grounded, cited answer against an ungrounded one",
            "See how chunking and retrieval quality change the result",
        ],
    },
    51: {
        "title": "Lab 7.3: Build an AI Agent (Capstone)",
        "body": [
            "In your Lab Manual, refer to Lab 7.3: Citizen Services Triage Agent (Capstone)",
            "45 minutes — VM notebook (lab_7.3_agent.ipynb); this is the course capstone",
            "Tools, an agent loop, and guardrails: single tool call -> agent loop -> guardrails + injection defense -> orchestration",
            "Ties together the API (Lab 7.1), retrieval (Lab 7.2), and PII security (Chapter 5)",
        ],
    },
}


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
    assert len(slides) == 58, f"expected 58 slides, got {len(slides)}"

    # sanity-check the slides we touch
    assert slides[0].shapes.title.text_frame.text.strip() == CHAPTER_NAME
    assert slides[3].shapes.title.text_frame.text.strip() == "Activities in This Chapter"
    lab_notes = {}
    for pos, spec in LABS.items():
        t = slides[pos - 1].shapes.title.text_frame.text.strip()
        assert t == spec["title"], f"slide {pos}: {t!r}"
        lab_notes[pos] = _notes(slides[pos - 1])
    old1_notes = _notes(slides[0])

    # 1. Chapter Title (rebuild of old slide 1 on the Government layout)
    t = prs.slides.add_slide(_layout(prs, "Chapter Title Government"))
    _ph(t, 0).text_frame.text = CHAPTER_NAME
    _ph(t, 1).text_frame.text = SUBTITLE
    if old1_notes:
        t.notes_slide.notes_text_frame.text = old1_notes

    # 2. Chapter Objectives (idx 15 is the displayed body on this layout)
    o = prs.slides.add_slide(_layout(prs, "Chapter Objectives"))
    _fill_body(_ph(o, 15), OBJECTIVES)

    # 3. Contents
    c = prs.slides.add_slide(_layout(prs, "Content with Header. Full Page"))
    _ph(c, 0).text_frame.text = "Contents"
    _fill_body(_ph(c, 1), CONTENTS)

    # 4. Lab rebuilds on 'Exercise Reference Slide with Typing Hands'
    lab_new = {}
    for pos, spec in LABS.items():
        s = prs.slides.add_slide(_layout(prs, "Exercise Reference Slide with Typing Hands"))
        _ph(s, 0).text_frame.text = spec["title"]
        _fill_body(_ph(s, 1), spec["body"])
        if lab_notes[pos]:
            s.notes_slide.notes_text_frame.text = lab_notes[pos]
        lab_new[pos] = s

    # Order (0-based over 58 originals + 6 appended at 58..63):
    #   new title, objectives, contents,
    #   orig 2 (timeline), orig 3 (activities overview)   [orig 1 old title and
    #   orig 4 duplicate overview dropped], orig 5..14, new Lab 7.1,
    #   orig 16..33, new Lab 7.2, orig 35..50, new Lab 7.3, orig 52..58
    order0 = (
        [58, 59, 60]
        + [1, 2]
        + list(range(4, 14))
        + [61]
        + list(range(15, 33))
        + [62]
        + list(range(34, 50))
        + [63]
        + list(range(51, 58))
    )
    arrange(prs, order0)
    save(prs, OUT)

    # quick echo
    prs2 = open_deck(OUT)
    n = len(list(prs2.slides))
    print(f"saved {OUT} ({n} slides)")
    for i, s in enumerate(prs2.slides):
        title = s.shapes.title.text_frame.text.replace("\n", " ")[:58] if s.shapes.title else "(no title)"
        print(f"{i+1:>2} [{s.slide_layout.name}] {title}")


if __name__ == "__main__":
    main()
