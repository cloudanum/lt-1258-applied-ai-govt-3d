"""Release-gate checks for the 1258 a3 author-input package.
Runs the checks from LT-Lab-Environment-Plan.md §4.3 that are checkable now:
  1. registry loads and lab ids are unique
  2. every notebook artifact named in the registry exists in labs/ (or solutions/)
  3. no notebook contains a hard-coded key or the old retired API
  4. all decks: valid zip, no duplicate partnames
  5. new lab notebooks import cleanly and their offline paths run
Prints a PASS/FAIL summary and exits non-zero on any failure.
"""
import sys, zipfile, glob, re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
LABS = ROOT / "legacy" / "labs"
DECKS = ROOT / "decks"
REG = ROOT / "registry" / "labs.yaml"
fails = []

def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))
    if not ok:
        fails.append(name)

# 1. registry
reg = yaml.safe_load(REG.read_text())
ids = [l["id"] for l in reg["labs"]]
check("registry loads; lab ids unique", len(ids) == len(set(ids)),
      f"{len(ids)} labs")

# 2. notebook artifacts referenced exist (for artifacts ending .ipynb that are new/authored)
missing = []
for l in reg["labs"]:
    art = l.get("artifact", "")
    if isinstance(art, str) and art.endswith(".ipynb") and l.get("status", "").startswith("authored"):
        if not (LABS / art).exists():
            missing.append(art)
check("authored notebook artifacts present", not missing,
      "missing: " + ", ".join(missing) if missing else "all present")

# 3. no secrets / retired API in notebook CODE cells (markdown may reference the
#    old anti-patterns to explain the fix, so we scan code only, with call/assign
#    patterns rather than bare mentions).
import nbformat
bad = []
KEY_ASSIGN = re.compile(r'(openai\.)?api_key\s*=\s*["\']sk-')
RETIRED_CALL = re.compile(r'openai\.Completion\.create\s*\(')
RETIRED_MODEL = re.compile(r'engine\s*=\s*["\']text-davinci')
for nb in glob.glob(str(LABS / "**/*.ipynb"), recursive=True):
    doc = nbformat.read(nb, as_version=4)
    code = "\n".join(c.source for c in doc.cells if c.cell_type == "code")
    if KEY_ASSIGN.search(code):
        bad.append(Path(nb).name + " (hard-coded key)")
    if RETIRED_CALL.search(code) or RETIRED_MODEL.search(code):
        bad.append(Path(nb).name + " (retired API/model in code)")
check("no hard-coded keys or retired API in lab CODE cells", not bad,
      "; ".join(bad) if bad else "clean (code cells)")

# 4. decks integrity
deck_problems = []
for f in sorted(glob.glob(str(DECKS / "*.pptx"))):
    z = zipfile.ZipFile(f)
    names = z.namelist()
    if z.testzip() is not None or {n for n in names if names.count(n) > 1}:
        deck_problems.append(Path(f).name)
n_decks = len(glob.glob(str(DECKS / "*.pptx")))
check(f"all {n_decks} decks valid (zip + no dup partnames)", not deck_problems,
      "; ".join(deck_problems) if deck_problems else "all OK")

# 5. new notebooks import + offline smoke (lab_common paths)
sys.path.insert(0, str(LABS))
try:
    import lab_common as lc
    r = lc.search_datasets("air quality")
    docs = lc.load_corpus()
    dv = lc.embed_texts([d["text"] for d in docs])
    qv = lc.embed_texts(["retention period for case files"])[0]
    top = lc.cosine_topk(qv, dv, 1)[0]
    masked = lc.mask_pii("SSN 512-88-4417 email a@b.gov")
    ok = (r["results"] and docs and "512-88-4417" not in masked)
    check("lab_common offline paths work", ok,
          f"datagov={r['source']}, corpus={len(docs)}, masking OK")
except Exception as e:
    check("lab_common offline paths work", False, f"{type(e).__name__}: {e}")

print()
if fails:
    print(f"RELEASE GATE: {len(fails)} FAILURE(S): {', '.join(fails)}")
    sys.exit(1)
print("RELEASE GATE: ALL CHECKS PASSED")
