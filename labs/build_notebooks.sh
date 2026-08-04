#!/usr/bin/env bash
# Convert jupytext .py sources -> .ipynb, then run the offline smoke test:
# every newly-authored a4 notebook (student + solution) must execute with
# OPENAI_API_KEY="" and no network. Solutions run from solutions/ (their
# first cell shims cwd/sys.path back to labs/). Expected-output transcripts
# are extracted from the executed solution notebooks.
# Usage: bash build_notebooks.sh
set -euo pipefail
VENV="$(cd "$(dirname "$0")/../../.." && pwd)/.venv-courseware/bin"
PY="$VENV/python"
cd "$(dirname "$0")"

echo "== Converting jupytext sources to .ipynb =="
for src in src/*.py; do
  base=$(basename "$src" .py)
  # student notebooks keep their name at labs/ root; SOLUTION -> solutions/
  if [[ "$base" == *_SOLUTION ]]; then
    out="solutions/${base%_SOLUTION}_solutions.ipynb"
  else
    out="${base}.ipynb"
  fi
  "$PY" -m jupytext --to notebook --output "$out" "$src" >/dev/null
  echo "  $src -> $out"
done

echo
echo "== Offline smoke test (OPENAI_API_KEY=\"\", no network) =="
export OPENAI_API_KEY=""   # force the offline/canned paths

# Notebooks that must execute fully offline. The pre-existing 7.x notebooks
# need a live key by design (their fallback is the transcript), so the smoke
# covers the healthcheck and the a4 roster only.
STUDENT=(
  lab_0.1_healthcheck
  lab_0.1_environment_tour
  lab_1.1_ai_inventory
  lab_1.2_clustering
  lab_2.1_data_expedition
  lab_4.1_prompt_studio
  lab_4.2_prompt_templates
  lab_5.1_adversarial
  lab_5.2_pii
  lab_6.1_data_quality
  lab_6.2_genai_cleaning
  lab_8.1_visualization
  lab_8.2_genai_reporting
)
SOLUTION=(
  lab_0.1_environment_tour
  lab_1.1_ai_inventory
  lab_1.2_clustering
  lab_2.1_data_expedition
  lab_4.1_prompt_studio
  lab_4.2_prompt_templates
  lab_5.1_adversarial
  lab_5.2_pii
  lab_6.1_data_quality
  lab_6.2_genai_cleaning
  lab_8.1_visualization
  lab_8.2_genai_reporting
)

fail=0
for nb in "${STUDENT[@]}"; do
  if "$PY" -m nbconvert --to notebook --execute --inplace \
       --ExecutePreprocessor.timeout=180 "${nb}.ipynb" >/dev/null 2>&1; then
    echo "  PASS  ${nb}.ipynb"
  else
    echo "  FAIL  ${nb}.ipynb"
    fail=1
  fi
done
for nb in "${SOLUTION[@]}"; do
  if ( cd solutions && "$PY" -m nbconvert --to notebook --execute --inplace \
       --ExecutePreprocessor.timeout=180 "${nb}_solutions.ipynb" >/dev/null 2>&1 ); then
    echo "  PASS  solutions/${nb}_solutions.ipynb"
  else
    echo "  FAIL  solutions/${nb}_solutions.ipynb"
    fail=1
  fi
done

echo
echo "== Transcripts from executed solution notebooks =="
"$PY" make_transcripts.py "${SOLUTION[@]}"

echo
if [[ "$fail" -ne 0 ]]; then
  echo "== SMOKE FAILURES — see above =="
  exit 1
fi
echo "== Done. Notebooks in $(pwd) and $(pwd)/solutions =="
ls -1 *.ipynb
