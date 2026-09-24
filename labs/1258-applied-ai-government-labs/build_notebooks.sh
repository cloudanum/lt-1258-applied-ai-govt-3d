#!/usr/bin/env bash
# Convert jupytext .py sources -> .ipynb, then run the offline smoke test:
# every newly-authored a4 notebook (student + solution) must execute with
# OPENAI_API_KEY="" and no network. Solutions run from solutions/ (their
# first cell shims cwd/sys.path back to labs/). Expected-output transcripts
# are extracted from the executed solution notebooks.
# Usage: bash build_notebooks.sh
set -euo pipefail
# Locate .venv-courseware by walking up from this script (the course tree
# moves between checkouts, so a fixed depth breaks).
VENV=""
_d="$(cd "$(dirname "$0")" && pwd)"
while [ "$_d" != "/" ]; do
  if [ -x "$_d/.venv-courseware/bin/python" ]; then
    VENV="$_d/.venv-courseware/bin"
    break
  fi
  _d="$(dirname "$_d")"
done
if [ -z "$VENV" ]; then
  echo "ERROR: .venv-courseware not found in any parent of $(dirname "$0")" >&2
  exit 1
fi
PY="$VENV/python"
cd "$(dirname "$0")"

# Pin the notebooks to the course kernel when it is registered, so students
# don't land on a bare "python3" kernel that lacks the openai package.
KERNEL="${KERNEL:-1258-a4}"
JUPYTEXT_KERNEL_ARG=()
if "$PY" -m jupyter kernelspec list 2>/dev/null | grep -qw "$KERNEL"; then
  JUPYTEXT_KERNEL_ARG=(--set-kernel "$KERNEL")
else
  echo "note: kernel '$KERNEL' not registered; keeping notebooks' own kernelspec." >&2
fi

echo "== Converting jupytext sources to .ipynb =="
for src in src/*.py; do
  base=$(basename "$src" .py)
  # student notebooks keep their name at labs/ root; SOLUTION -> solutions/
  if [[ "$base" == *_SOLUTION ]]; then
    out="solutions/${base%_SOLUTION}_solutions.ipynb"
  else
    out="${base}.ipynb"
  fi
  "$PY" -m jupytext --to notebook --output "$out" "$src" \
    "${JUPYTEXT_KERNEL_ARG[@]}" >/dev/null
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
  lab_1.3_decisiontree
  lab_1.4_nlp_ner
  lab_2.1_data_expedition
  lab_3.2_bloom_taxonomy
  lab_4.1_prompt_studio
  lab_4.2_prompt_templates
  lab_4.3_ptcf_bloom
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
  lab_1.3_decisiontree
  lab_1.4_nlp_ner
  lab_2.1_data_expedition
  lab_3.2_bloom_taxonomy
  lab_4.1_prompt_studio
  lab_4.2_prompt_templates
  lab_4.3_ptcf_bloom
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
