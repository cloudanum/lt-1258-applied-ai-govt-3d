"""Restore the 50-60 slide band for Ch09 (Summary & Roadmap), rev a4.

The a4 reduction cut Ch09 from 50 to 30/32 — chiefly by moving the 8-slide
glossary to the workbook, plus trends/roles/recap depth. This script ports back
eighteen content slides from the enriched a3 deck
(`1258a3-author-input/decks/_bak2/`):
  - Recap of Key AI Concepts and Skills
  - Trends depth: Multimodal AI, Open-Weight/On-Prem, 2026 by the Numbers,
    What Gartner Tells CIOs for 2026, Interactive Q&A
  - Next Steps by role (Manager / Analyst / IT Operations) + Final Recap
  - The full 8-slide Course Glossary
NOT ported: the P10 walkthrough pair (src 24-25, "Score Both Against the
Rubric" / "Debrief: What the Delta Teaches") and the old lab launcher (src 34)
— a4 has its own Lab 9.1 launcher and DO NOW 9.x activity slides.

Idempotent: reads the pristine a4 deck from `decks/_bak2/`, writes
`decks/1258-Ch09-Summary-Roadmap.pptx`.

Run:  .venv-courseware/bin/python tools/build_restore_band_ch09.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import pptx_tools as T

DEST_BAK = ROOT / "decks" / "_bak2" / "1258-Ch09-Summary-Roadmap.pptx"
SRC = (ROOT.parent / "1258a3-author-input" / "decks" / "_bak2"
       / "1258-Ch09-Summary-Roadmap.pptx")
OUT = ROOT / "decks" / "1258-Ch09-Summary-Roadmap.pptx"

PLAN = (
    [("a4", i) for i in range(1, 5)]       # through "Three Days, One Arc"
    + [("src", 4)]                         # Recap of Key AI Concepts and Skills
    + [("a4", i) for i in range(5, 16)]    # Day recaps .. Reasoning Models
    + [("src", 16), ("src", 17), ("src", 18), ("src", 19), ("src", 20)]
                                           # Multimodal, Open-Weight, 2026 Numbers, Gartner, Q&A
    + [("a4", i) for i in range(16, 28)]   # Prompting Spine .. Next Steps by Role
    + [("src", 35), ("src", 36), ("src", 37), ("src", 38)]
                                           # Manager / Analyst / IT Ops + Final Recap
    + [("a4", i) for i in range(28, 31)]   # Recommended Resources .. Policy and Guidance
    + [("src", i) for i in range(42, 50)]  # Course Glossary (1..8 of 8)
    + [("a4", 31), ("a4", 32)]             # Lab 9.1 launcher, Thank You
)

EXPECT_A4 = {
    3: "Activities in This Chapter", 4: "Three Days, One Arc",
    5: "What You Can Now Do — Day 1", 15: "Reasoning Models",
    16: "The Prompting Spine", 27: "Next Steps by Role",
    28: "Recommended Resources", 30: "Policy and Guidance to Bookmark",
    31: "Lab 9.1", 32: "Thank You",
}
EXPECT_SRC = {
    4: "Recap of Key AI Concepts",
    16: "Multimodal AI", 17: "Open-Weight and On-Prem AI",
    18: "2026 by the Numbers", 19: "What Gartner Tells CIOs",
    20: "Interactive Q&A Session",
    35: "Next Steps if You Are a Manager", 36: "Next Steps if You Are an Analyst",
    37: "Next Steps if You Are in IT Operations",
    38: "Final Recap of Lessons Learned",
    42: "Course Glossary (1 of 8)", 43: "Course Glossary (2 of 8)",
    44: "Course Glossary (3 of 8)", 45: "Course Glossary (4 of 8)",
    46: "Course Glossary (5 of 8)", 47: "Course Glossary (6 of 8)",
    48: "Course Glossary (7 of 8)", 49: "Course Glossary (8 of 8)",
}


def titles(path):
    return [t for _, t, _ in T.inventory(str(path))]


def main():
    a4_t = titles(DEST_BAK)
    src_t = titles(SRC)
    for idx, frag in EXPECT_A4.items():
        assert frag in a4_t[idx - 1], f"a4 slide {idx}: expected {frag!r}, got {a4_t[idx-1]!r}"
    for idx, frag in EXPECT_SRC.items():
        assert frag in src_t[idx - 1], f"src slide {idx}: expected {frag!r}, got {src_t[idx-1]!r}"

    dst = T.open_deck(str(DEST_BAK))
    src = T.open_deck(str(SRC))
    src_slides = list(src.slides)
    order, clone_pos = [], {}
    for kind, idx in PLAN:
        if kind == "a4":
            order.append(idx - 1)
        else:
            if idx not in clone_pos:
                T.clone_slide(dst, src_slides[idx - 1])
                clone_pos[idx] = len(dst.slides._sldIdLst) - 1
            order.append(clone_pos[idx])
    T.arrange(dst, order)
    T.save(dst, str(OUT))
    print(f"Ch09 restored: {len(PLAN)} slides "
          f"({sum(1 for k, _ in PLAN if k == 'a4')} kept + "
          f"{sum(1 for k, _ in PLAN if k == 'src')} ported) -> {OUT}")


if __name__ == "__main__":
    main()
