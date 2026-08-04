"""
build_brand_ch02.py — apply the LT standard branding/structure to
1258-Ch02-Applications-Public-Data.pptx (Chapter 2 'AI Applications Across
Government and Public Data'), rev a4. Same standard as 4703
(tools/build_brand_m1.py); exemplar 2016/PRE--Author Proof/Ch01-Pass5.pptx.

Idempotent: always rebuilds from decks/_bak6/1258-Ch02-Applications-Public-Data.pptx.

Changes (vs. 53-slide original):
  1. Slide 1 (chapter title) rebuilt on layout 'Chapter Title Government'
     (was '2_Chapter Title AI1'): CENTER_TITLE idx 0 = chapter name,
     SUBTITLE idx 1 = 'Chapter 2'; speaker notes carried over verbatim.
  2. Slide 2 (already on 'Chapter Objectives') kept in place; the four
     stale objectives in body idx 15 are replaced with the a4 objectives
     (verified federal applications, gov AI platforms, data.gov, use-case
     inventories).
  3. New Contents slide on 'Content with Header. Full Page' (sections +
     the chapter's activities), inserted at position 3.
  4. Activities overview: slide 3 'Activities in This Chapter' (70-min
     budget, matches registry/activities.yaml) KEPT on its content layout;
     slide 4 (stale duplicate: Lab 2.1 '40 min', 80-min budget) dropped.
  5. Lab slides rebuilt on 'Exercise Reference Slide with Typing Hands'
     (both old slides titled 'Lab 2.1...'):
       - old slide 48 (was 'Workbook Reference Slide with Writing'): body
         becomes 'In your Lab Manual, refer to Lab 2.1: Public Data
         Expedition — Profile an Agency Dataset' + the Lab 7.3 forward
         pointer + 'Time: 30 minutes' (registry duration_min).
       - old slide 52 (end-of-chapter launcher): same standard body with
         the notebook task line; old slide 51 (verbatim duplicate with a
         stale '40 minutes') dropped. Notes copied verbatim in both.
  6. Slide 53 (closing 'Chapter Objectives' duplicate of slide 2, carrying
     the stale objectives) dropped.

No Demo/DO NOW slides exist in this deck (they live in the Activities
overview + Lab Manual), so no Do Now/Demo layout rebuilds are needed.

Final slide count: 53 + 1 contents - 3 stale duplicates = 51 (in the
50-60 band; no [flex] trims needed).

Run:  ../../.venv-courseware/bin/python tools/build_brand_ch02.py
"""
from __future__ import annotations
import shutil
from pathlib import Path

from pptx_tools import open_deck, arrange, save

HERE = Path(__file__).resolve().parent
DECKS = HERE.parent / "decks"
SRC = DECKS / "_bak6" / "1258-Ch02-Applications-Public-Data.pptx"
OUT = DECKS / "1258-Ch02-Applications-Public-Data.pptx"

CHAPTER_NAME = "AI Applications Across Government and Public Data"
SUBTITLE = "Chapter 2"

OBJECTIVES = [
    "Survey verified AI applications across federal agencies and their operational impacts",
    "Use the government's own AI platforms: GenAI.mil, Maven Smart System, and GSA OneGov",
    "Find and assess datasets on data.gov and other public data portals",
    "Read agency AI use-case inventories to see what your agency is doing",
]

CONTENTS = [
    "Why Governments Need AI",
    "AI Application Domains: Health, Cyber Defense, Infrastructure, Public Safety, Automation",
    "Cautionary Cases: When Government AI Goes Wrong",
    "Government AI Platforms in 2026: GenAI.mil, Maven, USAi.gov, OneGov",
    "AI Use-Case Inventories",
    "Public Data: data.gov and Key Portals",
    "Activities: Demo 2.1, DO NOW 2.A–2.D, Lab 2.1",
]

LAB_REF_LINE = ("In your Lab Manual, refer to Lab 2.1: "
                "Public Data Expedition — Profile an Agency Dataset")
LAB_TIME_LINE = "Time: 30 minutes"  # registry/activities.yaml Lab 2.1 duration_min

LAB48_BODY = [
    LAB_REF_LINE,
    "Bookmark a dataset you find — you will query it with an agent in Lab 7.3",
    LAB_TIME_LINE,
]

LAB52_BODY = [
    LAB_REF_LINE,
    "Open lab_2.1_data_expedition.ipynb — profile three real datasets "
    "(shape, columns, dtypes; null count, distinct count, example value per column)",
    LAB_TIME_LINE,
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
    tf.clear()
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
    assert len(slides) == 53, f"expected 53 slides, got {len(slides)}"

    def title(i1):
        s = slides[i1 - 1]
        return s.shapes.title.text_frame.text.strip() if s.shapes.title else ""

    assert title(1) == CHAPTER_NAME, title(1)
    assert title(3) == "Activities in This Chapter", title(3)
    assert title(4) == "Activities in This Chapter", title(4)
    assert title(48) == "Lab 2.1", title(48)
    assert title(51).startswith("Lab 2.1: Public Data Expedition"), title(51)
    assert title(52).startswith("Lab 2.1: Public Data Expedition"), title(52)
    assert "40 minutes" in _ph(slides[50], 1).text_frame.text      # stale dup
    assert "30 minutes" in _ph(slides[51], 1).text_frame.text      # current
    lab48_notes = _notes(slides[47])
    lab52_notes = _notes(slides[51])
    title_notes = _notes(slides[0])

    # 1. Chapter Title on the correct Government layout (folds old slide 1)
    t = prs.slides.add_slide(_layout(prs, "Chapter Title Government"))
    _ph(t, 0).text_frame.text = CHAPTER_NAME
    _ph(t, 1).text_frame.text = SUBTITLE
    t.notes_slide.notes_text_frame.text = title_notes

    # 2. Objectives: slide 2 stays on 'Chapter Objectives'; refresh body idx 15
    _fill_body(_ph(slides[1], 15), OBJECTIVES)

    # 3. Contents
    c = prs.slides.add_slide(_layout(prs, "Content with Header. Full Page"))
    _ph(c, 0).text_frame.text = "Contents"
    _fill_body(_ph(c, 1), CONTENTS)

    # 5. Lab rebuilds on 'Exercise Reference Slide with Typing Hands'
    lab48 = prs.slides.add_slide(_layout(prs, "Exercise Reference Slide with Typing Hands"))
    _ph(lab48, 0).text_frame.text = "Lab 2.1"
    _fill_body(_ph(lab48, 1), LAB48_BODY)
    lab48.notes_slide.notes_text_frame.text = lab48_notes

    lab52 = prs.slides.add_slide(_layout(prs, "Exercise Reference Slide with Typing Hands"))
    _ph(lab52, 0).text_frame.text = title(52)
    _fill_body(_ph(lab52, 1), LAB52_BODY)
    lab52.notes_slide.notes_text_frame.text = lab52_notes

    # Order (0-based into the working deck: orig 0..52, appended 53..56):
    #   new title, orig objectives(1), new contents, orig activities(2),
    #   orig 5..47 (idx 4..46), new lab48, orig 49..50 (idx 48..49), new lab52
    # Dropped: orig 1 (0), orig 4 (3), orig 48 (47), orig 51 (50), orig 52 (51), orig 53 (52)
    order0 = [53, 1, 54, 2] + list(range(4, 47)) + [55, 48, 49, 56]
    arrange(prs, order0)
    save(prs, OUT)

    prs2 = open_deck(OUT)
    n = len(list(prs2.slides))
    print(f"saved {OUT} ({n} slides)")
    assert 50 <= n <= 60, f"out of band: {n}"
    for i, s in enumerate(prs2.slides):
        tt = s.shapes.title.text_frame.text.replace("\n", " ")[:55] if s.shapes.title else "(no title)"
        print(f"{i+1:>2} [{s.slide_layout.name}] {tt}")


if __name__ == "__main__":
    main()
