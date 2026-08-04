"""Restore the 50-60 slide band for Ch06 (Data for AI), rev a4.

The a4 reduction collapsed the six one-per-dimension data-quality slides to 2,
the tool catalogue to 2 and governance to 2 (52 -> 38/40). This script ports
back twelve content slides from the enriched a3 deck
(`1258a3-author-input/decks/_bak2/`):
  - Dimensions 3-6 (Consistency, Timeliness, Validity, Uniqueness)
  - DataBrew / Data Wrangler government-use-case slides
  - Storage Choices (warehouse/lake/lakehouse)
  - ONS Synthetic Data Spectrum
  - Government Use Cases 2 and 3
  - Data Governance Framework: Strategy + Organization and People
The old Exercise 6.1 walkthrough/debrief slides (src 18-21) are NOT ported —
a4 has its own DO NOW 6.B / Lab 6.1 activity slides.

Idempotent: reads the pristine a4 deck from `decks/_bak2/`, writes
`decks/1258-Ch06-Data-for-AI.pptx`.

Run:  .venv-courseware/bin/python tools/build_restore_band_ch06.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import pptx_tools as T

DEST_BAK = ROOT / "decks" / "_bak2" / "1258-Ch06-Data-for-AI.pptx"
SRC = (ROOT.parent / "1258a3-author-input" / "decks" / "_bak2"
       / "1258-Ch06-Data-for-AI.pptx")
OUT = ROOT / "decks" / "1258-Ch06-Data-for-AI.pptx"

PLAN = (
    [("a4", i) for i in range(1, 14)]      # through "Dimension 2: Completeness"
    + [("src", 13), ("src", 14), ("src", 15), ("src", 16)]   # Dimensions 3-6
    + [("a4", i) for i in range(14, 23)]   # Relevance .. AWS Glue DataBrew—Overview
    + [("src", 28)]                        # AWS Glue DataBrew—Government Use Cases
    + [("a4", 23)]                         # Amazon SageMaker Data Wrangler—Overview
    + [("src", 30)]                        # Data Wrangler—Government Use Cases
    + [("a4", i) for i in range(24, 27)]   # Tool Landscape .. Pipeline Anatomy
    + [("src", 34)]                        # Storage Choices: Warehouse, Lake, Lakehouse
    + [("a4", 27), ("a4", 28)]             # Labeling .. Synthetic Data
    + [("src", 37)]                        # The ONS Synthetic Data Spectrum
    + [("a4", 29), ("a4", 30)]             # De-identification .. Government Use Case 1
    + [("src", 40), ("src", 41)]           # Government Use Cases 2 and 3
    + [("a4", i) for i in range(31, 37)]   # Role of AI .. Governance Framework: Vision
    + [("src", 48), ("src", 49)]           # Governance Framework: Strategy + Organization
    + [("a4", i) for i in range(37, 41)]   # Datasheets/DCAT-US .. Summary
)

EXPECT_A4 = {
    3: "Activities in This Chapter", 13: "Dimension 2: Completeness",
    14: "Relevance and Accuracy", 15: "DO NOW 6.B", 16: "Lab 6.1",
    22: "AWS Glue DataBrew", 23: "Amazon SageMaker Data Wrangler",
    26: "Pipeline Anatomy", 28: "Synthetic Data",
    30: "Government Use Case 1", 36: "The Data Governance Framework: Vision",
    37: "Documenting Datasets", 39: "Lab 6.2", 40: "Summary",
}
EXPECT_SRC = {
    13: "Dimension 3: Consistency", 14: "Dimension 4: Timeliness",
    15: "Dimension 5: Validity", 16: "Dimension 6: Uniqueness",
    28: "AWS Glue DataBrew—Government Use Cases",
    30: "Amazon SageMaker Data Wrangler—Government Use Cases",
    34: "Storage Choices: Warehouse, Lake, Lakehouse",
    37: "The ONS Synthetic Data Spectrum",
    40: "Government Use Case 2", 41: "Government Use Case 3",
    48: "The Data Governance Framework: Strategy",
    49: "The Data Governance Framework: Organization and People",
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
    print(f"Ch06 restored: {len(PLAN)} slides "
          f"({sum(1 for k, _ in PLAN if k == 'a4')} kept + "
          f"{sum(1 for k, _ in PLAN if k == 'src')} ported) -> {OUT}")


if __name__ == "__main__":
    main()
