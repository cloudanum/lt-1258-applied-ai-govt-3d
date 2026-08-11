"""Friendly-lab guardrail for the Course 1258 (rev a4) non-programmer rewrite.

The student notebooks at labs/ root are the guided, low-code versions of the
labs: every step is one plain-English helper call, and students only edit
simple values in `# YOUR TURN` cells. This script enforces that contract:

  1. No "scary" constructs in student code cells — no imports other than the
     `from lab_helpers import *` setup line, no def/try/except, no loops or
     comprehensions, no lambda, no json/re/os/sys, no pandas/sklearn/
     matplotlib/openai calls, no asserts, no f-string prints.
  2. Every `# YOUR TURN` cell ships pre-filled with a working reference value
     (so the offline smoke gate always executes end-to-end).
  3. Prints a per-lab "visible lines of code" table, before (archived
     code-forward originals in For_Python_Programmers/) vs after — the
     evidence that the rewrite actually reduced the Python students see.

Usage:  .venv/bin/python tools/check_friendly.py
Exits non-zero on any failure.
"""
import re
import sys
from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parent.parent
LABS = ROOT / "labs"
ARCHIVE = LABS / "For_Python_Programmers"

STUDENT_LABS = [
    "lab_0.1_healthcheck",
    "lab_0.1_environment_tour",
    "lab_1.1_ai_inventory",
    "lab_1.2_clustering",
    "lab_2.1_data_expedition",
    "lab_4.1_prompt_studio",
    "lab_4.2_prompt_templates",
    "lab_5.1_adversarial",
    "lab_5.2_pii",
    "lab_6.1_data_quality",
    "lab_6.2_genai_cleaning",
    "lab_7.1_openai_api",
    "lab_7.2_rag_gov_docs",
    "lab_7.3_agent",
    "lab_8.1_visualization",
    "lab_8.2_genai_reporting",
]

ALLOWED_IMPORT = "from lab_helpers import *"

# Constructs a non-programmer should never see in a student cell. Each entry is
# (label, compiled regex). Matched against every line of every code cell.
SCARY = [
    ("import other than lab_helpers",
     re.compile(r"^\s*(import|from)\s+(?!lab_helpers\s+import\s+\*)\S+")),
    ("function definition", re.compile(r"^\s*def\s")),
    ("try/except", re.compile(r"^\s*(try|except|finally)\b")),
    ("loop", re.compile(r"^\s*(for|while)\s")),
    ("comprehension", re.compile(r"[=\(\[]\s*.*\bfor\s+\w+\s+in\b.*[\)\]]")),
    ("lambda", re.compile(r"\blambda\b")),
    ("json module", re.compile(r"\bjson\.")),
    ("re module", re.compile(r"\bre\.(compile|match|search|sub|findall)")),
    ("os/sys", re.compile(r"\b(os|sys)\.")),
    ("pathlib", re.compile(r"\bPath\b")),
    ("pandas", re.compile(r"\bpd\.")),
    ("sklearn", re.compile(r"\bsklearn\b|\.fit\(|\.fit_transform\(")),
    ("matplotlib", re.compile(r"\bplt\.")),
    ("openai sdk", re.compile(r"\bopenai\b|\.chat\.completions")),
    ("assert", re.compile(r"^\s*assert\b")),
    ("f-string print", re.compile(r"\bprint\s*\(\s*f[\"']")),
]

fails = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))
    if not ok:
        fails.append(name)


def code_cells(path):
    doc = nbformat.read(path, as_version=4)
    return [c for c in doc.cells if c.cell_type == "code"]


def visible_loc(path):
    """Non-blank, non-comment lines across all code cells."""
    n = 0
    for c in code_cells(path):
        for line in c.source.splitlines():
            s = line.strip()
            if s and not s.startswith("#"):
                n += 1
    return n


print("== Scary-construct scan (student notebooks) ==")
for lab in STUDENT_LABS:
    problems = []
    for i, cell in enumerate(code_cells(LABS / f"{lab}.ipynb"), 1):
        for label, pat in SCARY:
            for line in cell.source.splitlines():
                if pat.search(line):
                    problems.append(f"cell {i}: {label}: {line.strip()[:60]}")
    check(f"{lab}: no scary constructs", not problems,
          "; ".join(problems[:3]) if problems else "clean")

print()
print("== YOUR TURN cells are pre-filled ==")
for lab in STUDENT_LABS:
    problems = []
    for i, cell in enumerate(code_cells(LABS / f"{lab}.ipynb"), 1):
        if "YOUR TURN" not in cell.source:
            continue
        # A pre-filled value: an assignment whose right-hand side is not None.
        ok = any(re.search(r"^\s*\w+\s*=\s*(?!None\b)\S", ln)
                 for ln in cell.source.splitlines())
        if not ok:
            problems.append(f"cell {i} has no pre-filled value")
    check(f"{lab}: YOUR TURN cells pre-filled", not problems,
          "; ".join(problems) if problems else "all pre-filled (or none present)")

print()
print("== Visible lines of code: before (archive) vs after (friendly) ==")
print(f"{'lab':34s} {'before':>7s} {'after':>7s} {'change':>8s}")
total_before = total_after = 0
for lab in STUDENT_LABS:
    before = visible_loc(ARCHIVE / f"{lab}.ipynb")
    after = visible_loc(LABS / f"{lab}.ipynb")
    total_before += before
    total_after += after
    pct = (after - before) / before * 100 if before else 0
    print(f"{lab:34s} {before:7d} {after:7d} {pct:7.0f}%")
print(f"{'TOTAL':34s} {total_before:7d} {total_after:7d} "
      f"{(total_after - total_before) / total_before * 100:7.0f}%")

print()
if fails:
    print(f"FRIENDLY CHECK: {len(fails)} FAILURE(S)")
    sys.exit(1)
print("FRIENDLY CHECK: ALL CHECKS PASSED")
