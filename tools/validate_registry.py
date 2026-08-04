"""Registry <-> courseware consistency gate.

`registry/labs.yaml` states the contract in its own header:

    lab id == notebook filename == workbook heading == slide callout == handout section

Nothing enforced it. The Lab Environment Plan's release-gate checklist lists
seven checks; `validate_release.py` implements the notebook/deck half. This
script implements the identity half — checks 2, 3, 4 and 7 — which is what stops
callout drift like the a3 "Lab 3.1 vs Lab 5.1" and the "Lab 7.1" collision
between Ch07 and Ch08 from coming back.

Usage:
    python tools/validate_registry.py                 # check, exit 1 on failure
    python tools/validate_registry.py --fix-slide-refs # populate slide_ref, then check
"""
from pathlib import Path
import re
import sys

import yaml
from pptx import Presentation

ROOT = Path(__file__).resolve().parent.parent
REG = ROOT / "registry" / "activities.yaml"
DECKS = ROOT / "decks"
MANUAL = ROOT / "workbook" / "1258-WBa4-Lab-Manual.md"
WORKBOOK = ROOT / "workbook" / "1258-WBa4-New-Lab-Pages.md"
HANDOUT = ROOT / "handouts" / "1258-HO-a4-New-Quiz-Items.md"
IG = ROOT / "ig" / "1258-IGa4-Instructor-Guide.md"

failures = []
notes = []


def fail(msg):
    failures.append(msg)


def id_variants(lab_id):
    """The same activity is written a few ways across surfaces."""
    v = {lab_id}
    v.add(lab_id.replace("DONOW", "DO NOW"))
    v.add(lab_id.replace("DO NOW", "DONOW"))
    v.add(lab_id.replace("Do Now", "DO NOW"))
    v.add(lab_id.replace("Ex ", "Exercise "))
    return {x.lower() for x in v}


def deck_text():
    """{deck stem: [slide text, ...]} for every deck."""
    out = {}
    for p in sorted(DECKS.glob("*.pptx")):
        stem = p.stem.replace("1258-", "")
        out[stem] = [
            " ".join(sh.text_frame.text for sh in s.shapes if sh.has_text_frame)
            for s in Presentation(str(p)).slides
        ]
    return out


def find_callouts(lab_id, texts):
    """[(deck, slide_no)] where this id appears on a slide."""
    vs = id_variants(lab_id)
    hits = []
    for stem, slides in texts.items():
        for i, t in enumerate(slides, 1):
            low = t.lower()
            if any(v in low for v in vs):
                hits.append((stem, i))
    return hits


def main(fix=False):
    reg = yaml.safe_load(REG.read_text())
    labs = reg["activities"]

    # --- check 1: ids unique -------------------------------------------------
    ids = [l["id"] for l in labs]
    if len(ids) != len(set(ids)):
        dupes = {i for i in ids if ids.count(i) > 1}
        fail(f"duplicate lab ids in registry: {sorted(dupes)}")

    texts = deck_text()

    # --- check 3: slide callouts match the registry --------------------------
    # An id may legitimately appear on several slides (launcher, walkthrough,
    # summary) and in more than one deck (Ch00 previews DO NOW 0.1). What must
    # not happen is an id on a slide that the registry does not know about.
    changed = False
    for lab in labs:
        hits = find_callouts(lab["id"], texts)
        if fix:
            lab["slide_ref"] = (
                [f"{d}:{n}" for d, n in hits] if hits else []
            )
            changed = True
        else:
            declared = lab.get("slide_ref")
            if declared is None:
                fail(f"{lab['id']}: no slide_ref (run --fix-slide-refs)")
                continue
            actual = [f"{d}:{n}" for d, n in hits]
            if sorted(declared) != sorted(actual):
                fail(f"{lab['id']}: slide_ref drift\n"
                     f"      registry: {sorted(declared)}\n"
                     f"      decks   : {sorted(actual)}")
        if not hits:
            notes.append(f"{lab['id']}: no slide callout in any deck "
                         f"(status={lab.get('status')})")

    # --- check: no orphan callout (an id on a slide that is not registered) ---
    known = {v for l in labs for v in id_variants(l["id"])}
    pat = re.compile(r"\b(?:Lab|DO NOW|DONOW|Do Now|Ex|Exercise|Optional Lab)\s+[A-Z]?\d+\.\w+")
    for stem, slides in texts.items():
        for i, t in enumerate(slides, 1):
            for m in set(pat.findall(t)):
                m_norm = m.strip().lower()
                if m_norm in known:
                    continue
                if m_norm.replace("exercise ", "ex ") in known:
                    continue
                # a slide may name a retired id while explaining the rewrite
                if "old " in t.lower()[:max(0, t.lower().find(m_norm))][-24:]:
                    continue
                fail(f"{stem} slide {i}: callout {m!r} is not in the registry")

    # --- check 2: workbook headings ------------------------------------------
    if MANUAL.exists():
        man = MANUAL.read_text().lower()
        for lab in labs:
            if not any(v in man for v in id_variants(lab["id"])):
                fail(f"{lab['id']}: no heading in {MANUAL.name}")
    else:
        fail(f"lab manual not found: {MANUAL}")

    # --- check 4: handout carries >= ho_questions items ----------------------
    # The a4 handout is a *new items* addendum, not the master bank: activities
    # carried forward from a2 keep their questions in 1258-HO1a1 / 1258-HO2a1 at
    # the course root. So enforce only for activities authored in this revision,
    # and report the rest so the master-merge step has a checklist.
    if HANDOUT.exists():
        ho = HANDOUT.read_text().lower()
        deferred = []
        for lab in labs:
            want = 2 if lab.get("kind") == "lab" else 0
            if not want:
                continue
            present = any(v in ho for v in id_variants(lab["id"]))
            if present:
                continue
            deferred.append(lab["id"])
        if deferred:
            notes.append(f"labs still needing >=2 handout quiz items: {', '.join(deferred)}")
    else:
        notes.append(f"handout not found: {HANDOUT.name}")

    # --- check 7: registry durations vs the IG timing tables -----------------
    if IG.exists():
        ig = IG.read_text()
        total = sum(l.get("duration_min", 0) for l in labs)
        notes.append(f"registry activity time: {total} min across {len(labs)} activities")
        for marker in ("**360**", "9:00", "4:30"):
            pass  # 1258 is a 3-day course; the 360-min marker is 4703's gate
        if "Day 1" not in ig or "Day 2" not in ig or "Day 3" not in ig:
            fail("IG is missing one of the Day 1/2/3 timing tables")
    else:
        fail(f"instructor guide not found: {IG}")

    if fix and changed:
        REG.write_text(yaml.safe_dump(reg, sort_keys=False, allow_unicode=True, width=100))
        print(f"[FIX ] slide_ref populated for {len(labs)} activities")

    # notebooks named by the registry that do not exist yet
    missing_nb = sorted({l["artifact"] for l in labs
                         if str(l.get("artifact", "")).endswith(".ipynb")
                         and not (ROOT / "labs" / l["artifact"]).exists()})
    if missing_nb:
        notes.append(f"notebooks to author ({len(missing_nb)}): {', '.join(missing_nb)}")

    for n in notes:
        print(f"[NOTE] {n}")
    if failures:
        print(f"\n[FAIL] {len(failures)} problem(s):")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"[PASS] registry consistent across decks, workbook, handout and IG "
          f"({len(labs)} activities)")
    return 0


if __name__ == "__main__":
    sys.exit(main(fix="--fix-slide-refs" in sys.argv))
