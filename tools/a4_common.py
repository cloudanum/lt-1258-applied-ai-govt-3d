"""Shared helpers for the a3 -> a4 optimization pass.

a4 does three things to the a3 decks, in place:
  (1) fix broken hyperlink targets and the stale examples the Aug-2026 audit found;
  (2) reduce five over-long chapters by MERGE and DEMOTE (never silent deletion);
  (3) keep every edit at run level so Publications' styling survives.

Everything here is deliberately small and side-effect free so the per-chapter
scripts read as a list of intentions, not as XML plumbing.
"""
from pathlib import Path
import zipfile
from pptx.oxml.ns import qn

BASE = Path(__file__).resolve().parents[1]
DECKS = BASE / "decks"


def deck(name):
    """decks/1258-<name>.pptx"""
    return DECKS / f"1258-{name}.pptx"


# ---------------------------------------------------------------- text edits

def _norm(s):
    """Deck text is peppered with non-breaking spaces from years of PowerPoint
    editing; match on normalised text so anchors don't depend on invisible bytes."""
    return s.replace("\xa0", " ").replace("‑", "-")


def edit_bullet(slide, old_sub, new_sub, all_matches=False):
    """Replace text inside a bullet, preserving the first run's formatting.

    Same contract as the a3 enrich scripts: collapse the paragraph into run 0 so
    the theme font/size/colour of the leading run wins. Returns True if replaced.
    """
    hit = False
    target = _norm(old_sub)
    for sh in slide.shapes:
        if not sh.has_text_frame:
            continue
        for p in sh.text_frame.paragraphs:
            if not p.runs:
                continue
            full = _norm("".join(r.text for r in p.runs))
            if target in full:
                p.runs[0].text = full.replace(target, new_sub)
                for r in p.runs[1:]:
                    r.text = ""
                if not all_matches:
                    return True
                hit = True
    return hit


def must_edit(slide, old_sub, new_sub, where=""):
    """edit_bullet, but loud when the anchor has moved — and idempotent, so the
    pass can be re-run after a partial failure without tripping."""
    if edit_bullet(slide, old_sub, new_sub):
        return True
    body = _norm(" ".join(sh.text_frame.text for sh in slide.shapes if sh.has_text_frame))
    if _norm(new_sub) in body:
        return True                      # already applied on an earlier run
    raise AssertionError(f"anchor not found {where}: {old_sub!r}")


def _body_shape(slide):
    """The bullet area: largest-area placeholder with a text frame.

    Same heuristic pptx_tools uses — in this LT template the main bullet area is
    the OBJECT placeholder, while the BODY placeholder is a tiny footer caption.
    """
    best, best_area = None, -1
    for sh in slide.shapes:
        if not sh.has_text_frame:
            continue
        try:
            area = (sh.width or 0) * (sh.height or 0)
        except (TypeError, ValueError):
            area = 0
        if area > best_area:
            best, best_area = sh, area
    return best


def add_bullet(slide, text, copy_format_from=-2):
    """Append a bullet to the slide's main text frame, cloning run formatting
    from an existing paragraph so the merged line matches its neighbours."""
    sh = _body_shape(slide)
    if sh is None:
        return False
    tf = sh.text_frame
    donors = [p for p in tf.paragraphs if p.runs]
    p = tf.add_paragraph()
    r = p.add_run()
    r.text = text
    if donors:
        d = donors[copy_format_from] if abs(copy_format_from) <= len(donors) else donors[-1]
        p.level = d.level
        src, dst = d.runs[0].font, r.font
        try:
            dst.size, dst.bold, dst.italic = src.size, src.bold, src.italic
            if src.name:
                dst.name = src.name
        except (AttributeError, ValueError):
            pass
    return True


def get_notes(slide):
    return slide.notes_slide.notes_text_frame.text if slide.has_notes_slide else ""


def set_notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def append_notes(slide, text):
    tf = slide.notes_slide.notes_text_frame
    tf.text = tf.text.rstrip() + "\n" + text


def edit_notes(slide, old_sub, new_sub):
    """Substring replace inside speaker notes. Returns True if it changed."""
    cur = get_notes(slide)
    if old_sub not in cur:
        return False
    set_notes(slide, cur.replace(old_sub, new_sub))
    return True


# ---------------------------------------------------------------- hyperlinks

def _iter_parts(prs):
    yield prs.part
    for p in prs.part.package.iter_parts():
        yield p


def retarget_url(prs, old_url, new_url):
    """Repoint every external relationship whose target contains old_url.

    Dead links in these decks live in slideN.xml.rels, behind visible text that
    a previous pass already corrected — so retargeting (not deleting) restores
    the click without touching the wording.
    """
    n = 0
    for part in _iter_parts(prs):
        for rel in list(part.rels.values()):
            if rel.is_external and old_url in str(rel.target_ref):
                # `target_ref` is a lazyproperty: reading it above cached the old
                # value in the instance __dict__, and serialization reads the cache.
                # Set the backing field *and* evict the cache, or the edit is a no-op.
                rel._target = new_url
                rel.__dict__["target_ref"] = new_url
                n += 1
    return n


def find_urls(prs, needle=""):
    """[(partname, url)] for every external rel, optionally filtered."""
    out = []
    for part in _iter_parts(prs):
        for rel in part.rels.values():
            if rel.is_external:
                u = str(rel.target_ref)
                if needle in u:
                    out.append((str(part.partname), u))
    return out


# ---------------------------------------------------------------- deck hygiene

def clean_orphan_slides(prs):
    """Drop rels to slide parts that are not in sldIdLst.

    Orphans are leftovers from earlier edit history; appended slides take
    partname len(sldIdLst)+1 and would collide with them on save, producing
    duplicate zip entries. (Lifted verbatim from the a3 enrich scripts.)
    """
    real = {prs.part.rels[e.get(qn("r:id"))].target_part for e in prs.slides._sldIdLst}
    drops = []
    for pt in prs.part.package.iter_parts():
        for rId, rel in pt.rels.items():
            if rel.is_external:
                continue
            tp = rel.target_part
            if str(tp.partname).startswith("/ppt/slides/") and tp not in real:
                drops.append((pt, rId))
    for pt, rId in drops:
        if hasattr(pt, "drop_rel"):
            pt.drop_rel(rId)
        else:
            pt.rels.pop(rId)
    return len(drops)


def verify(path, expected=None):
    """zip integrity + no duplicate partnames + optional slide count."""
    z = zipfile.ZipFile(path)
    assert z.testzip() is None, f"zip integrity failed: {path}"
    names = z.namelist()
    dupes = {x for x in names if names.count(x) > 1}
    assert not dupes, f"duplicate partnames in {path}: {dupes}"
    import re
    with z.open("ppt/presentation.xml") as fh:
        n = len(re.findall(b"<p:sldId ", fh.read()))
    if expected is not None:
        assert n == expected, f"{Path(path).name}: expected {expected} slides, got {n}"
    return n


def titles(prs):
    """[(1-based index, title)] using the deck's own last-line-is-title convention."""
    out = []
    for i, s in enumerate(prs.slides, 1):
        txt = [sh.text_frame.text for sh in s.shapes if sh.has_text_frame]
        lines = [l for l in "\n".join(txt).split("\n") if l.strip()]
        out.append((i, lines[-1].strip() if lines else "(blank)"))
    return out
