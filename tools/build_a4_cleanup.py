"""a4 pass 3 — housekeeping.

Two defects, both mine or inherited, neither visible on a slide:

  1. Duplicated speaker-note blocks. `append_notes` is not idempotent, and
     build_a4_fixes.py was re-run while the URL retargeting was being debugged,
     so some correction notes were appended several times.
  2. Orphan slide parts — slide XML present in the package but referenced by
     neither presentation.xml.rels nor sldIdLst. Ch01 carried one from a3; the
     reduce pass left one in Ch06. They do not render, but Publications sees them.

Run:  python tools/build_a4_cleanup.py
"""
import re
import zipfile

import a4_common as A
import pptx_tools as P

DECKS = ["Ch00-Course-Launch", "Ch01-AI-ML-Foundations", "Ch02-Applications-Public-Data",
         "Ch03-Desktop-GenAI", "Ch04-ModernGenAI-PromptEng", "Ch05-Security-Risks-Responsible-AI",
         "Ch06-Data-for-AI", "Ch07-Building-with-LLMs", "Ch08-Operations-Reporting",
         "Ch09-Summary-Roadmap", "AppA-ML-LifeCycle", "AppB-Security-DeepDive",
         "AppC-Transformer-LLM-Internals", "AppD-Classic-ML-DeepDive"]


def dedupe_notes(prs):
    """Drop repeated paragraphs within a slide's notes, keeping first occurrence.

    Only exact, non-trivial repeats are removed — short lines like 'Speaker Notes:'
    are left alone because they legitimately recur as section headers.
    """
    fixed = 0
    for slide in prs.slides:
        if not slide.has_notes_slide:
            continue
        tf = slide.notes_slide.notes_text_frame
        paras = tf.text.split("\n")
        seen, out = set(), []
        for p in paras:
            key = p.strip()
            if len(key) > 40 and key in seen:
                continue
            if len(key) > 40:
                seen.add(key)
            out.append(p)
        if len(out) != len(paras):
            tf.text = "\n".join(out)
            fixed += 1
    return fixed


def main():
    total_notes = total_orphans = 0
    for name in DECKS:
        path = A.deck(name)
        prs = P.open_deck(path)
        orph = A.clean_orphan_slides(prs)
        notes = dedupe_notes(prs)
        if orph or notes:
            P.save(prs, path)
            bits = []
            if notes:
                bits.append(f"{notes} slide(s) with duplicated notes")
            if orph:
                bits.append(f"{orph} orphan rel(s)")
            print(f"  {name}: " + ", ".join(bits))
        total_notes += notes
        total_orphans += orph

    print(f"\n  {total_notes} slides de-duplicated, {total_orphans} orphan rels dropped")

    print("\n  verifying no orphan slide parts remain:")
    bad = 0
    for name in DECKS:
        path = A.deck(name)
        z = zipfile.ZipFile(path)
        parts = len([n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)])
        real = len(re.findall(b"<p:sldId ", z.read("ppt/presentation.xml")))
        if parts != real:
            print(f"    {name}: {real} real vs {parts} parts")
            bad += 1
    print("    none" if not bad else f"    {bad} deck(s) still carry orphans")


if __name__ == "__main__":
    print("a4 pass 3 — housekeeping")
    main()
