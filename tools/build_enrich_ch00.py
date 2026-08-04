"""Enrich 1258-Ch00-Course-Launch.pptx: 12 existing slides -> 50.

Order of operations (per workflow):
  (a) in-place text edits to existing slides (TOC correction, speaker notes),
  (b) append 38 new slides,
  (c) one final arrange() with the full permutation,
  (d) save + verify (count, testzip, dup partnames, inventory).

Backup taken to decks/_bak/ before first run. Re-running rebuilds from the backup
so the script is idempotent.
"""
from pathlib import Path
import copy
import shutil
import zipfile

import pptx_tools as P
import content_ch00_enrich as C

BASE = Path("/Users/iahmad/Creator/Courses_and_conferences/LT/1258")
DECK = BASE / "1258a4-author-input/decks/1258-Ch00-Course-Launch.pptx"
BAK = BASE / "1258a4-author-input/decks/_bak/1258-Ch00-Course-Launch.pptx"


def _set_para_text(p, text):
    """Replace a paragraph's text, keeping the first run's formatting."""
    runs = p.runs
    if runs:
        runs[0].text = text
        for r in runs[1:]:
            r._r.getparent().remove(r._r)
    else:
        p.add_run().text = text


def _rewrite_body(slide, new_lines):
    """Rewrite the main body placeholder's lines in place, preserving formatting;
    adds paragraphs (cloned from the last one) if more lines are needed."""
    body = P._body_placeholder(slide)
    tf = body.text_frame
    paras = list(tf.paragraphs)
    template = copy.deepcopy(paras[-1]._p)          # clone BEFORE editing
    while len(paras) < len(new_lines):
        tf._txBody.append(copy.deepcopy(template))
        paras = list(tf.paragraphs)
    for p, line in zip(paras, new_lines):
        _set_para_text(p, line)


def main():
    # idempotent: always start from the pristine backup
    shutil.copy(BAK, DECK)
    prs = P.open_deck(DECK)
    slides = list(prs.slides)
    assert len(slides) == 12, f"expected 12 slides in backup, got {len(slides)}"

    # (a) TEXT EDITS to existing slides -------------------------------------
    # slide 2 (idx 1): objectives — add Bloom's-mapping speaker note (refs: optional enrich)
    slides[1].notes_slide.notes_text_frame.text = C.NOTES_OBJECTIVES
    # slide 3 (idx 2): TOC — old 8-chapter list -> a3 Ch00-Ch09 structure (refs Correction #3)
    _rewrite_body(slides[2], C.TOC_CHAPTERS)
    slides[2].notes_slide.notes_text_frame.text = C.NOTES_TOC
    # slide 4 (idx 3): appendix TOC — A-C -> A-D
    _rewrite_body(slides[3], C.TOC_APPENDICES)
    slides[3].notes_slide.notes_text_frame.text = C.NOTES_TOC_APPENDIX
    # slide 10 (idx 9): Bloom's — correct the lineage in the notes (refs Correction #4)
    slides[9].notes_slide.notes_text_frame.text = C.NOTES_BLOOMS

    # (b) APPEND new slides --------------------------------------------------
    for t, b, n in C.CH00_NEW:
        P.append_content(prs, t, b, n)

    # (c) ONE final arrange --------------------------------------------------
    n_total = len(list(prs.slides._sldIdLst))
    assert n_total == 50, f"expected 50 before arrange, got {n_total}"
    assert sorted(C.ORDER0) == list(range(50)), "ORDER0 is not a permutation of 0..49"
    P.arrange(prs, C.ORDER0)

    # (d) save + verify ------------------------------------------------------
    P.save(prs, DECK)
    names = zipfile.ZipFile(DECK).namelist()
    dupes = {x for x in names if names.count(x) > 1}
    assert not dupes, f"dup partnames: {dupes}"
    bad = zipfile.ZipFile(DECK).testzip()
    assert bad is None, f"corrupt member: {bad}"
    for idx, title, w in P.inventory(DECK):
        print(f"{idx:>3}  {w:>4}w  {title}")
    print(f"\n{DECK.name}: {len(P.inventory(DECK))} slides, testzip OK, no dup partnames")


if __name__ == "__main__":
    main()
