"""a4 pass 2b — tighten three merged bullets that restated their neighbours.

The merge pass folded absorbed slides in as extra bullets. Three of them
overlapped content already on the surviving slide, which is exactly the
redundancy this revision is removing. Rewrite them to carry only the part the
host slide did not already say.

Run:  python tools/build_a4_tighten.py
"""
import a4_common as A
import pptx_tools as P


def run():
    path = A.deck("Ch00-Course-Launch")
    prs = P.open_deck(path)
    s = list(prs.slides)

    # s22 Bloom's — bullet 1 already names the full ladder
    A.must_edit(s[21],
        "The ladder: Remember - Understand - Apply - Analyze - Evaluate - Create",
        "Sequence is the Anderson & Krathwohl (2001) revision of Bloom's original",
        "Ch00 s22")

    # s16 Getting In — step 4 already says Firefox opens automatically; keep only the fallback
    A.must_edit(s[15],
        "Firefox opens JupyterLab automatically; if not, double-click 'Start Labs' on the desktop "
        "(if prompted for a password it is: pw)",
        "If Firefox does not open JupyterLab, double-click 'Start Labs' on the desktop "
        "(password, if asked: pw)",
        "Ch00 s16")

    # s25 Checkpoint — bullets 1-2 already state VM + green healthcheck
    A.must_edit(s[24],
        "You are done when: notebook list visible, healthcheck open and run, checks 1-3 green",
        "If any of these is missing, fix it now — Chapter 1 does not start until the room is green",
        "Ch00 s25")

    P.save(prs, path)
    n = A.verify(path, 25)
    print(f"  Ch00: 3 merged bullets tightened, {n} slides")


if __name__ == "__main__":
    print("a4 pass 2b — tighten merged bullets")
    run()
