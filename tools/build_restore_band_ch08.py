"""Restore the 50-60 slide band for Ch08 (Operations & Reporting), rev a4.

The a4 reduction merged duplicate MLOps/implementation slides and folded in the
two [flex] drift slides (52 -> 44/46). This script ports back five content
slides from the enriched a3 deck (`1258a3-author-input/decks/_bak2/`):
  - ML-Pipeline diagram slide
  - Contextual Bandits use-case example
  - Drift Deep Dive: Detection and Hidden Technical Debt  [flex drift depth]
  - Retraining Triggers and Model Retirement              [flex drift depth]
  - Understanding the Data Landscape
The old "Lab 8.1" launcher (src 46) is NOT ported — a4 has its own lab slides.
The merged duplicates (src 12, 15) stay merged.

Idempotent: reads the pristine a4 deck from `decks/_bak2/`, writes
`decks/1258-Ch08-Operations-Reporting.pptx`.

Run:  .venv-courseware/bin/python tools/build_restore_band_ch08.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import pptx_tools as T

DEST_BAK = ROOT / "decks" / "_bak2" / "1258-Ch08-Operations-Reporting.pptx"
SRC = (ROOT.parent / "1258a3-author-input" / "decks" / "_bak2"
       / "1258-Ch08-Operations-Reporting.pptx")
OUT = ROOT / "decks" / "1258-Ch08-Operations-Reporting.pptx"

PLAN = (
    [("a4", i) for i in range(1, 7)]       # through "Machine Learning Phases"
    + [("src", 6)]                         # ML-Pipeline (diagram)
    + [("a4", i) for i in range(7, 19)]    # Step One .. Intro to Operationalizing AI
    + [("src", 21)]                        # Example Use-Case: Contextual Bandits
    + [("a4", i) for i in range(19, 25)]   # Challenges .. MLOps in Production: What to Monitor
    + [("src", 28), ("src", 29)]           # Drift Deep Dive + Retraining Triggers
    + [("a4", i) for i in range(25, 34)]   # Oversight .. Data Visualization Guidelines
    + [("src", 39)]                        # Understanding the Data Landscape
    + [("a4", i) for i in range(34, 47)]   # Reporting Requirements .. Summary
)

EXPECT_A4 = {
    3: "Activities in This Chapter", 6: "Machine Learning Phases",
    7: "Step One—Data Extraction", 18: "Introduction to Operationalizing AI",
    19: "Challenges in Transitioning AI", 24: "MLOps in Production: What to Monitor",
    25: "Establishing Oversight", 33: "Data Visualization Guidelines",
    34: "Reporting and Dashboard Requirements", 45: "Lab 8.2", 46: "Summary",
}
EXPECT_SRC = {
    6: "ML-Pipeline",
    21: "Example Use-Case: Contextual Bandits",
    28: "Drift Deep Dive: Detection and Hidden Technical Debt",
    29: "Retraining Triggers and Model Retirement",
    39: "Understanding the Data Landscape",
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
    print(f"Ch08 restored: {len(PLAN)} slides "
          f"({sum(1 for k, _ in PLAN if k == 'a4')} kept + "
          f"{sum(1 for k, _ in PLAN if k == 'src')} ported) -> {OUT}")


if __name__ == "__main__":
    main()
