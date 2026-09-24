#!/usr/bin/env bash
# Convert jupytext .py sources -> .ipynb, then run the offline smoke test:
# every newly-authored a4 notebook (student + solution) must execute with
# OPENAI_API_KEY="" and no network. Solutions run from solutions/ (their
# first cell shims cwd/sys.path back to labs/). Expected-output transcripts
# are extracted from the executed solution notebooks.
# Usage: bash build_notebooks.sh
set -euo pipefail
cd "$(dirname "$0")"

# Interpreter: an active venv wins, then the repo's own .venv, then whatever
# python3 is on PATH. The old hard-coded ../../../.venv-courseware path assumed
# the repo sat three levels below the venv's parent and resolved to /home in a
# plain clone, so the very first jupytext call aborted the whole run.
if [[ -n "${VIRTUAL_ENV:-}" && -x "$VIRTUAL_ENV/bin/python" ]]; then
  PY="$VIRTUAL_ENV/bin/python"
elif [[ -x "../.venv/bin/python" ]]; then
  PY="$(cd .. && pwd)/.venv/bin/python"
else
  PY="$(command -v python3 || true)"
fi
if [[ -z "$PY" ]] || ! "$PY" -c "import jupytext, nbconvert" 2>/dev/null; then
  echo "ERROR: no interpreter with jupytext + nbconvert." >&2
  echo "  tried: \$VIRTUAL_ENV, ../.venv/bin/python, python3" >&2
  echo "  fix:   uv venv --python 3.12 ../.venv && \\" >&2
  echo "         uv pip install --python ../.venv/bin/python jupyterlab jupytext openai \\" >&2
  echo "             pandas scikit-learn matplotlib pyyaml nbformat nbconvert ipykernel" >&2
  exit 2
fi
KERNEL="${KERNEL:-1258-a4}"
if ! "$PY" -m jupyter kernelspec list 2>/dev/null | grep -qw "$KERNEL"; then
  echo "note: kernel '$KERNEL' not registered; using the notebooks' own kernelspec." >&2
  KERNEL=""
fi
KERNEL_ARG=()
[[ -n "$KERNEL" ]] && KERNEL_ARG=(--ExecutePreprocessor.kernel_name="$KERNEL")
# Same choice for the notebooks' own kernelspec: pin them to the course kernel
# when it is registered, so students don't land on a bare "python3" kernel.
JUPYTEXT_KERNEL_ARG=()
[[ -n "$KERNEL" ]] && JUPYTEXT_KERNEL_ARG=(--set-kernel "$KERNEL")
echo "interpreter: $PY"

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

# Every notebook must execute fully offline. The 7.x labs used to be excluded
# as "needs a live key", but each of their call sites has a labelled canned
# fallback, so keeping them out only hid regressions in exactly the notebooks
# whose documented contingency is the transcript.
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
  lab_7.1_openai_api
  lab_7.2_rag_gov_docs
  lab_7.3_agent
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
  lab_7.1_openai_api
  lab_7.2_rag_gov_docs
  lab_7.3_agent
  lab_8.1_visualization
  lab_8.2_genai_reporting
)

fail=0
for nb in "${STUDENT[@]}"; do
  if "$PY" -m nbconvert --to notebook --execute --inplace \
       --ExecutePreprocessor.timeout=180 "${KERNEL_ARG[@]}" \
       "${nb}.ipynb" >"/tmp/1258-smoke-${nb}.log" 2>&1; then
    echo "  PASS  ${nb}.ipynb"
  else
    echo "  FAIL  ${nb}.ipynb   (log: /tmp/1258-smoke-${nb}.log)"
    tail -n 12 "/tmp/1258-smoke-${nb}.log" | sed "s/^/        /"
    fail=1
  fi
done
for nb in "${SOLUTION[@]}"; do
  if ( cd solutions && "$PY" -m nbconvert --to notebook --execute --inplace \
       --ExecutePreprocessor.timeout=180 "${KERNEL_ARG[@]}" \
       "${nb}_solutions.ipynb" >"/tmp/1258-smoke-${nb}-sol.log" 2>&1 ); then
    echo "  PASS  solutions/${nb}_solutions.ipynb"
  else
    echo "  FAIL  solutions/${nb}_solutions.ipynb   (log: /tmp/1258-smoke-${nb}-sol.log)"
    tail -n 12 "/tmp/1258-smoke-${nb}-sol.log" | sed "s/^/        /"
    fail=1
  fi
done

echo
if [[ "$fail" -ne 0 ]]; then
  echo "== SMOKE FAILURES — see above =="
  echo "   transcripts NOT regenerated (a partial run would overwrite good ones)"
  exit 1
fi

echo "== Transcripts from executed solution notebooks =="
"$PY" make_transcripts.py "${SOLUTION[@]}"

echo "== Done. Notebooks in $(pwd) and $(pwd)/solutions =="
ls -1 *.ipynb
