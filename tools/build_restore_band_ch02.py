"""Restore the 50-60 slide band for Ch02 (Applications + Public Data), rev a4.

The a4 reduction merged duplicate section slides, removed a bare-URL slide and
repointed links (52 -> 46/48). This script ports back three content slides from
the enriched a3 deck (`1258a3-author-input/decks/_bak2/`) that carry real
teaching value: the public-datasets intro, the Data.gov cornerstone slide and
the integration best-practices slide. The old "Lab 2.1" launcher (src 49) is
NOT ported — a4 has its own Lab 2.1 launcher.

Idempotent: reads the pristine a4 deck from `decks/_bak2/`, writes
`decks/1258-Ch02-Applications-Public-Data.pptx`.

Run:  .venv-courseware/bin/python tools/build_restore_band_ch02.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import pptx_tools as T

DEST_BAK = ROOT / "decks" / "_bak2" / "1258-Ch02-Applications-Public-Data.pptx"
SRC = (ROOT.parent / "1258a3-author-input" / "decks" / "_bak2"
       / "1258-Ch02-Applications-Public-Data.pptx")
OUT = ROOT / "decks" / "1258-Ch02-Applications-Public-Data.pptx"

PLAN = (
    [("a4", i) for i in range(1, 34)]      # through "The Use of AI in Government—Five Key Areas"
    + [("src", 36)]                        # Introduction to Public Datasets—Unlocking the Power...
    + [("a4", i) for i in range(34, 39)]   # Why Public Datasets .. Data.gov in 2026
    + [("src", 42)]                        # Data.gov: A Cornerstone of Open Government
    + [("a4", i) for i in range(39, 46)]   # Open Data Principles .. old Lab 2.1 launcher
    + [("src", 50)]                        # Best Practices and Strategies for Successful AI Integration
    + [("a4", i) for i in range(46, 49)]   # Summary, a4 Lab 2.1 launcher, closing objectives
)

EXPECT_A4 = {
    3: "Activities in This Chapter", 33: "The Use of AI in Government",
    34: "Why Are Public Datasets Important", 38: "Data.gov in 2026",
    39: "Open Data Principles", 45: "Lab 2.1", 46: "Summary",
    47: "Lab 2.1: Public Data Expedition",
}
EXPECT_SRC = {
    36: "Introduction to Public Datasets",
    42: "Data.gov: A Cornerstone of Open Government",
    50: "Best Practices and Strategies for Successful AI Integration",
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
    print(f"Ch02 restored: {len(PLAN)} slides "
          f"({sum(1 for k, _ in PLAN if k == 'a4')} kept + "
          f"{sum(1 for k, _ in PLAN if k == 'src')} ported) -> {OUT}")


if __name__ == "__main__":
    main()
