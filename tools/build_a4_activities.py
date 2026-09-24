"""Generate the activity registry and the LT-format lab manual from one source.

`content_activities.py` holds every demo, Do Now and lab exactly once. This
script emits:

  registry/activities.yaml          machine-readable registry (supersedes labs.yaml)
  legacy/labs/workbook/1258-WBa4-Lab-Manual.md  the participant lab manual, LT house format

Because both come from the same dictionaries, the registry contract
(`id == workbook heading == slide callout`) holds by construction.

The LT manual format is taken from the a1 workbook (1258-WBa1.docx):

    Lab X.Y <Title>
      Objectives            "By the end of this lab, you will:"
      Introduction          scenario paragraph
      Where This Fits       <- a4 addition: chapter, slides, timing
      Resources             data files, corpus, tools
      Steps                 numbered
      Reflection questions
      Key takeaway

Run:  python tools/build_a4_activities.py
"""
import re
from pathlib import Path

import yaml

import content_activities as C

ROOT = Path(__file__).resolve().parent.parent
REG = ROOT / "registry" / "activities.yaml"
MANUAL = ROOT / "legacy" / "labs" / "workbook" / "1258-WBa4-Lab-Manual.md"

KIND_WORD = {"demo": "Demo", "donow": "Activity", "lab": "Lab"}
ENV_WORD = {"vm": "CloudShare VM (JupyterLab)", "browser": "Browser + AI assistant",
            "paper": "Paper — no computer needed", "none": "None"}


def notebook_for(a):
    """The notebook an activity opens.

    Taken from the activity's own Steps wherever they name one, so the manual,
    the registry and the step text can never disagree. Falls back to a name
    derived from the id.
    """
    for s in a["steps"]:
        m = re.search(r"`(lab_[\w.]+\.ipynb)`", s)
        if m:
            return m.group(1)
    if a["kind"] == "lab" and a["env"] == "vm":
        slug = re.sub(r"[^a-z0-9]+", "_",
                      a["title"].lower().split("(")[0].strip())[:24].strip("_")
        return f"lab_{a['id'].split()[-1]}_{slug}.ipynb"
    return {"browser": "browser", "paper": "paper", "vm": "notebook", "none": "none"}[a["env"]]


# --------------------------------------------------------------------------- registry
LABS_YAML = ROOT / "registry" / "labs.yaml"

# `Do Now 1.A` / `DONOW 0.1` / `DO NOW 0.1` are the same activity written three
# ways. The workbook prints "DO NOW", so that is the form the registry carries.
def canon_id(lab_id):
    out = re.sub(r"^DONOW\b", "DO NOW", lab_id.strip())
    return re.sub(r"^Do Now\b", "DO NOW", out)


def kind_of(lab_id):
    if lab_id.startswith(("Lab ", "Optional Lab ", "Ex ")):
        return "lab"
    return "demo" if lab_id.startswith("Demo ") else "donow"


def labs_overlay():
    """registry/labs.yaml is canonical for the scheduling facts.

    a4 shipped two registries that disagreed: labs.yaml matched the workbook's
    durations on all seven new lab pages, while activities.yaml carried flat
    30-minute placeholders, a different Lab 7.3 title, and no Ex 6.1 at all.
    labs.yaml now wins for id, title, chapter, artifact, environment, duration
    and flex; content_activities.py keeps ownership of the prose.
    """
    doc = yaml.safe_load(LABS_YAML.read_text())
    out = {}
    for lab in doc["labs"]:
        out[canon_id(lab["id"])] = {
            "title": lab["title"],
            "chapter": lab["chapter"],
            "artifact": lab["artifact"],
            "environment": str(lab["environment"]).lower(),
            "duration_min": lab["duration_min"],
            "flex": bool(lab.get("flex", False)),
            "slide_ref": lab.get("slide_ref") or [],
        }
    return out


def build_registry():
    rows = []
    for ch, items in C.CHAPTERS:
        for a in items:
            rows.append({
                "id": canon_id(a["id"]),
                "title": a["title"],
                "kind": a["kind"],
                "chapter": ch,
                "deck": C.DECK_OF[ch],
                "artifact": notebook_for(a),
                "environment": a["env"],
                "duration_min": a["minutes"],
                "needs_openai_key": bool(a["needs_key"]),
                "data": a["data"],
                "spine_rung": a["spine"],
                "flex": bool(a["flex"]),
            })

    # --- apply the canonical overlay -------------------------------------- #
    overlay = labs_overlay()
    prior = {}
    if REG.exists():                      # keep slide_ref that validate_registry
        old = yaml.safe_load(REG.read_text()) or {}   # --fix-slide-refs populated
        prior = {canon_id(a["id"]): a for a in old.get("activities", [])}

    for row in rows:
        row["slide_ref"] = prior.get(row["id"], {}).get("slide_ref", [])
        if row["id"] in overlay:
            row.update({k: v for k, v in overlay[row["id"]].items() if v != []})
            if overlay[row["id"]]["slide_ref"]:
                row["slide_ref"] = overlay[row["id"]]["slide_ref"]

    # activities that exist only in labs.yaml (carried-forward and paper labs)
    have = {r["id"] for r in rows}
    for lab_id, facts in overlay.items():
        if lab_id in have:
            continue
        old = prior.get(lab_id, {})
        rows.append({
            "id": lab_id,
            "title": facts["title"],
            "kind": old.get("kind", kind_of(lab_id)),
            "chapter": facts["chapter"],
            "deck": C.DECK_OF.get(facts["chapter"], ""),
            "artifact": facts["artifact"],
            "environment": facts["environment"],
            "duration_min": facts["duration_min"],
            "needs_openai_key": bool(old.get("needs_openai_key", False)),
            "data": old.get("data", []),
            "spine_rung": old.get("spine_rung"),
            "flex": facts["flex"],
            "slide_ref": facts["slide_ref"] or old.get("slide_ref", []),
        })

    order = {ch: i for i, (ch, _) in enumerate(C.CHAPTERS)}
    rows.sort(key=lambda r: (order.get(r["chapter"], 99), r["id"]))

    doc = {
        "course": "1258",
        "revision": "a4",
        "contract": ("id == workbook heading == slide callout == handout section. "
                     "GENERATED: prose from tools/content_activities.py, scheduling facts "
                     "(title/chapter/artifact/environment/duration/flex) from "
                     "registry/labs.yaml, which is canonical. Edit those, then re-run "
                     "tools/build_a4_activities.py."),
        "shape": "each chapter: 1 demo + 4 activities/Do Nows + 1-2 labs (Ch07 has 3: the "
                 "agent capstone is the course deliverable)",
        "openai_key": "read from .env at the package root; see .env.example",
        "activities": rows,
    }
    REG.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100))
    return rows


# --------------------------------------------------------------------------- manual
def render_asset(a, slide_hint):
    w = KIND_WORD[a["kind"]]
    out = [f"### {a['id']} {a['title']}", ""]

    out += ["**Objectives**", "", f"By the end of this {w.lower()}, you will:", ""]
    out += [f"- {o}" for o in a["objectives"]] + [""]

    out += ["**Introduction**", "", a["scenario"], ""]

    out += ["**Where this fits**", "",
            f"- Chapter: **{a['chapter']} {C.CHAPTER_TITLES[a['chapter']]}**",
            f"- Slides: {slide_hint}",
            f"- Time: **{a['minutes']} minutes**"
            + ("  *(flex — your instructor may skip this)*" if a["flex"] else ""),
            f"- Environment: {ENV_WORD[a['env']]}"]
    if a["spine"]:
        out += [f"- Prompting spine: rung **{a['spine']}**"]
    out += [""]

    res = []
    if a["data"]:
        res += [f"- `labs/data/{d}`" for d in a["data"]]
    if a["needs_key"]:
        res += ["- OpenAI API key — loaded automatically from `.env`; never paste a key "
                "into a notebook"]
    if a["kind"] == "lab" and a["env"] == "vm":
        res += [f"- Notebook: `labs/{notebook_for(a)}`"]
    if res:
        out += ["**Resources**", ""] + res + [""]

    out += ["**Steps**", ""]
    out += [f"{i}. {s}" for i, s in enumerate(a["steps"], 1)] + [""]

    out += ["**Reflection questions**", ""]
    out += [f"- {q}" for q in a["reflection"]] + [""]
    out += ["---", ""]
    return out


def build_manual(slide_refs):
    L = [
        "---",
        'title: "Course 1258 — Lab Manual"',
        'subtitle: "Applied AI for Government IT Professionals · Revision a4"',
        "---",
        "",
        "# Lab Manual",
        "",
        "Every activity in this course appears here, in the order you meet it. Each chapter "
        "has **one demo** your instructor runs, **four short activities or Do Nows** you run "
        "yourself, and **one or two labs** that go deep.",
        "",
        "## Before you start",
        "",
        "**Your environment.** Labs marked *CloudShare VM* run in JupyterLab in your browser. "
        "There is nothing to install.",
        "",
        "**The API key.** Labs that call a model read the key from a `.env` file that already "
        "sits beside the `labs/` folder. You will never be asked to paste a key into a "
        "notebook, and you should never do so. If a notebook reports no key, tell your "
        "instructor.",
        "",
        "**The data.** Six public datasets ship with the course under `labs/data/`, with "
        "sources recorded in `MANIFEST.json`. They are downloaded ahead of class because "
        "data.gov retired its API in 2026 and classroom networks are unreliable.",
        "",
        "**The one rule that never changes: public or synthetic data only.** Every dataset "
        "and document in this manual is public US government data or synthetic material "
        "written for the course. Never paste real agency, personal or sensitive data into "
        "any assistant during this class.",
        "",
        "## The datasets",
        "",
        "| File | What it is |",
        "|---|---|",
        "| `federal_ai_use_cases.csv` | OMB 2025 Federal AI Use Case Inventory — real agency AI, as data |",
        "| `federal_ai_cots.csv` | The same inventory's commercial off-the-shelf entries |",
        "| `chicago_311.csv` | City of Chicago 311 requests — genuinely messy operational data |",
        "| `cdc_flu_wastewater.csv` | CDC influenza wastewater surveillance — a real time series |",
        "| `epa_aqi_by_county.csv` | EPA annual Air Quality Index by county, 2024 |",
        "| `nyc_air_quality.csv` | NYC air-quality indicators by neighbourhood and period |",
        "",
        "---",
        "",
    ]
    for ch, items in C.CHAPTERS:
        L += [f"# {ch} — {C.CHAPTER_TITLES[ch]}", ""]
        for kind in ("demo", "donow", "lab"):
            for a in [x for x in items if x["kind"] == kind]:
                L += render_asset(a, slide_refs.get(a["id"], "see chapter deck"))
    MANUAL.write_text("\n".join(L))
    return MANUAL


if __name__ == "__main__":
    rows = build_registry()
    print(f"  registry: {REG.relative_to(ROOT)} — {len(rows)} activities")

    # slide refs get filled in by build_a4_slides.py; use a placeholder until then
    refs = {}
    p = build_manual(refs)
    print(f"  manual:   {p.relative_to(ROOT)} — {p.stat().st_size:,} bytes")

    core = sum(r["duration_min"] for r in rows if not r["flex"])
    flex = sum(r["duration_min"] for r in rows if r["flex"])
    print(f"\n  activity time: {core} min core + {flex} min flex = {core+flex} min")
    print(f"  3-day contact is ~1440 min; core leaves ~{1440-core} min for lecture "
          f"across 460 slides")
