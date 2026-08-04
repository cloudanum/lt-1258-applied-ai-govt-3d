"""Build new Ch03 (Desktop GenAI, all-new content on the course template) and the
Ch00 additions (existing 4 intro slides + 8 launch/DONOW slides)."""
from pathlib import Path
import pptx_tools as P
import content_ch03 as C

BASE = Path("/Users/iahmad/Creator/Courses_and_conferences/LT/1258")
OUT = BASE / "1258a4-author-input/decks"

# Ch03: start from a COPY of old Ch05 (same template/master), strip to just the
# title slide, retitle, and append the all-new Desktop GenAI slides. Using an
# existing deck as the base guarantees identical masters/theme.
def build_ch03():
    src = BASE / "1258-Chap/1258-Ch05.pptx"
    prs = P.open_deck(src)
    P.keep_only(prs, [1])                      # keep only slide 1 as a template carrier
    out = OUT / "1258-Ch03-Desktop-GenAI.pptx"
    P.save(prs, out); prs = P.open_deck(out)   # save+reopen (partname hygiene)
    # replace the single carried slide's content by appending new slides then
    # dropping the carrier.
    for i, (t, b, n) in enumerate(C.CH03_SLIDES):
        P.append_content(prs, t, b, n)
    # drop the original carrier slide (now at index 0); keep the appended ones
    P._drop_slide(prs, 0)
    P.retitle(prs, 0, C.CH03_TITLE)
    P.save(prs, out)
    return len(list(prs.slides._sldIdLst)), out


def build_ch00():
    src = BASE / "1258-Chap/1258-Ch00.pptx"
    out = OUT / "1258-Ch00-Course-Launch.pptx"
    prs = P.open_deck(src)                      # keep all 4 existing intro slides
    for t, b, n in C.CH00_ADDITIONS:
        P.append_content(prs, t, b, n)
    P.save(prs, out)
    return len(list(prs.slides._sldIdLst)), out


if __name__ == "__main__":
    import zipfile
    OUT.mkdir(parents=True, exist_ok=True)
    for fn in (build_ch03, build_ch00):
        n, out = fn()
        names = zipfile.ZipFile(out).namelist()
        dupes = {x for x in names if names.count(x) > 1}
        assert not dupes, f"dupes in {out}: {dupes}"
        print(f"{out.name}: {n} slides, no dup partnames")
