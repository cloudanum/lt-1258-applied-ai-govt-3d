#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="/home/student/1258-new"
LABS_DIR="$PROJECT_DIR/labs"
LOG_FILE="${JUPYTER_1258_LOG:-/tmp/1258-jupyter-lab.log}"
PORT="${JUPYTER_1258_PORT:-8888}"
OPEN_BROWSER="${JUPYTER_1258_OPEN_BROWSER:-True}"

if [[ -x "$PROJECT_DIR/.venv/bin/jupyter-lab" ]]; then
  JUPYTER_BIN="$PROJECT_DIR/.venv/bin/jupyter-lab"
  JUPYTER_ARGS=()
elif command -v jupyter-lab >/dev/null 2>&1; then
  JUPYTER_BIN="$(command -v jupyter-lab)"
  JUPYTER_ARGS=()
elif command -v jupyter >/dev/null 2>&1; then
  JUPYTER_BIN="$(command -v jupyter)"
  JUPYTER_ARGS=(lab)
else
  echo "Could not find jupyter-lab. Install it in $PROJECT_DIR/.venv or on PATH." >&2
  exit 1
fi

cd "$LABS_DIR"
{
  echo "[$(date -Is)] Starting Course 1258 JupyterLab"
  echo "Jupyter binary: $JUPYTER_BIN"
  echo "Lab root: $LABS_DIR"
  echo "Port: $PORT"
} >> "$LOG_FILE"

exec "$JUPYTER_BIN" "${JUPYTER_ARGS[@]}" \
  --ServerApp.root_dir="$LABS_DIR" \
  --ServerApp.port="$PORT" \
  --ServerApp.open_browser="$OPEN_BROWSER" \
  --ServerApp.default_url="/lab" \
  >> "$LOG_FILE" 2>&1
