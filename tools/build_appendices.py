"""Build appendices:
  AppA  = old AppA, unchanged (ML Life Cycle & Ideation, incl. Lab A.1)
  AppB  = old AppB, unchanged (Security deep dive: SAIF/Chronicle/Zero-Trust, Lab B.1)
  AppC  = old AppC (transformer/LLM internals) + BERT overflow cloned from old Ch06
  AppD  = NEW: assembled entirely from demoted Ch01 detail slides (zero new authoring)
"""
import shutil
from pathlib import Path
import pptx_tools as P

BASE = Path("/Users/iahmad/Creator/Courses_and_conferences/LT/1258")
CH = BASE / "1258-Chap"
AP = BASE / "1258-App"
OUT = BASE / "1258a4-author-input/decks"


def _check(out):
    import zipfile
    names = zipfile.ZipFile(out).namelist()
    assert not {x for x in names if names.count(x) > 1}, f"dupes in {out}"
    return len(list(P.open_deck(out).slides._sldIdLst))


def passthrough(src, out):
    shutil.copy(src, out)
    return _check(out)


def build_appC(out):
    # old AppC + BERT-internals overflow (old Ch06 s38-46) cloned in.
    prs = P.open_deck(AP / "1258-AppC.pptx")
    src6 = P.open_deck(CH / "1258-Ch06.pptx")
    bert = [s for i, s in enumerate(src6.slides, 1) if i in range(38, 47)]
    for s in bert:
        P.clone_slide(prs, s)
    P.save(prs, out)
    return _check(out)


def build_appD(out):
    # NEW: title carrier from old AppC template + demoted Ch01 detail slides.
    prs = P.open_deck(AP / "1258-AppC.pptx")
    n0 = len(list(prs.slides._sldIdLst))
    src1 = P.open_deck(CH / "1258-Ch01.pptx")
    demoted = [45, 46, 47, 48,          # decision-tree extensions
               52, 53, 54, 55, 56, 57,  # NLP embeddings: Word2Vec/GloVe/TF-IDF
               76, 77, 78, 79, 80, 81,  # deep learning internals: perceptron/backprop
               90, 91, 92]              # computer vision detail
    kept = [s for i, s in enumerate(src1.slides, 1) if i in set(demoted)]
    for s in kept:
        P.clone_slide(prs, s)
    # keep only slide 1 (title carrier) + the cloned demoted slides
    order = [0] + list(range(n0, n0 + len(kept)))
    P.arrange(prs, order)
    P.retitle(prs, 0, "Appendix D: Classic ML and Data Engineering Deep Dive")
    P.save(prs, out)
    return _check(out)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    print("AppA:", passthrough(AP/"1258-AppA.pptx", OUT/"1258-AppA-ML-LifeCycle.pptx"), "slides")
    print("AppB:", passthrough(AP/"1258-AppB.pptx", OUT/"1258-AppB-Security-DeepDive.pptx"), "slides")
    print("AppC:", build_appC(OUT/"1258-AppC-Transformer-LLM-Internals.pptx"), "slides")
    print("AppD:", build_appD(OUT/"1258-AppD-Classic-ML-DeepDive.pptx"), "slides")
