#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="/home/student/1258-new"
LABS_DIR="$PROJECT_DIR/labs/1258-applied-ai-government-labs"
LOG_FILE="${JUPYTER_1258_LOG:-/tmp/1258-jupyter-lab.log}"
PORT="${JUPYTER_1258_PORT:-8888}"
OPEN_BROWSER="${JUPYTER_1258_OPEN_BROWSER:-True}"

# IT drops the class key in /home/student/Keys/keys.txt; copy it into .env
# (what the notebooks read) before the server starts, so a key swapped in
# before class needs no other step. Never fatal: with no key the labs run on
# canned answers, and a failed sync must not keep the class out of JupyterLab.
# Its output — masked to the key's last four characters — goes to $LOG_FILE.
if [[ -x "$PROJECT_DIR/sync_key.sh" ]]; then
  "$PROJECT_DIR/sync_key.sh" >> "$LOG_FILE" 2>&1 || true
fi

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
