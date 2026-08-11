# For Python Programmers — the original code-forward labs

This folder preserves the **original, code-forward versions** of the Course 1258
(rev a4) lab notebooks, exactly as they were before the labs were rewritten for a
non-programmer audience.

## Which version should I use?

| Audience | Use |
|---|---|
| Most participants (non-programmers) | The notebooks at the **`labs/` root** (one level up) — the guided, low-code versions |
| Participants comfortable with Python | The notebooks **in this folder** — same labs, same data, same outputs, with the full pandas / scikit-learn / OpenAI SDK code visible and written by hand |

Both versions are functionally the same lab: same datasets, same steps, same
learning objectives, same offline/canned fallbacks. In the root versions the
machinery lives in `../lab_helpers.py`; here it is written out in the notebook
cells for you to read, run, and modify.

## Contents

- `lab_*.ipynb` — the 16 original student notebooks (`# YOUR CODE` cells)
- `solutions/` — the 15 instructor `*_solutions.ipynb` + `transcripts/`
- `src/` — the jupytext `.py` sources these notebooks were built from
- `lab_common.py` — the shared helper module these notebooks import
- `data` → symlink to `../data` (the shared lab datasets; run notebooks from
  this folder so relative paths resolve)

## Notes

- Run the notebooks **from this folder** (JupyterLab: open them in place) —
  they reference `data/...` and `lab_common` relatively.
- This folder is a **frozen snapshot**: `../build_notebooks.sh` rebuilds only the
  root labs from `../src/` and never touches anything here.
- Everything runs offline with no API key (canned fallbacks), exactly like the
  root versions.
