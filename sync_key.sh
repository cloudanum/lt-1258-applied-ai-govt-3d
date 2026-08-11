#!/usr/bin/env bash
# sync_key.sh — copy the class OpenAI key from the file IT drops it in to the
# course .env that the lab notebooks read:
#
#     /home/student/Keys/keys.txt   ->   /home/student/1258-new/.env
#
# The Desktop launcher runs this before starting JupyterLab, so a key copied
# in before class needs no further step; IT can also run it by hand after
# swapping the key. Only the OPENAI_API_KEY line of .env is rewritten — the
# model aliases and the comments around it are left exactly as they are.
#
# The key is never printed, only its last four characters.
#
# "No key yet" is not an error. The labs are built to run on labelled canned
# answers when there is no key, so an unfilled keys.txt must never keep the
# class out of JupyterLab. Exit 1 is kept for a sync that was asked for and
# could not be done (an unwritable .env).
#
# Overridable for testing: KEYS_FILE, PROJECT_DIR.
set -uo pipefail

KEYS_FILE="${KEYS_FILE:-/home/student/Keys/keys.txt}"
PROJECT_DIR="${PROJECT_DIR:-/home/student/1258-new}"
ENV_FILE="$PROJECT_DIR/.env"
ENV_EXAMPLE="$PROJECT_DIR/.env.example"
VAR="OPENAI_API_KEY"

say() { printf '[1258] %s\n' "$*"; }

# Trim surrounding whitespace and a trailing CR (keys pasted from Windows or
# from a mail client arrive with CRLF endings, and a stray \r on the end of a
# key is invisible in an editor but produces a puzzling 401).
trim() {
  local s="${1%$'\r'}"
  s="${s#"${s%%[![:space:]]*}"}"
  s="${s%"${s##*[![:space:]]}"}"
  printf '%s' "$s"
}

# The values the templates ship with, so an unfilled file never overwrites a
# real key that is already in place.
is_placeholder() {
  local v="${1^^}"
  [[ -z "$v" ]] && return 0
  case "$v" in
    *REPLACE*|*PASTE*|*YOUR-KEY*|*YOUR_KEY*|SK-...|SK-XXX*) return 0 ;;
  esac
  return 1
}

# First usable OPENAI_API_KEY in $1. Accepts `OPENAI_API_KEY=sk-...`, the same
# with an `export ` in front or quotes around the value, and a bare `sk-...`
# on a line of its own — whichever way the key was pasted in.
extract_key() {
  local line name val
  while IFS= read -r line || [[ -n "$line" ]]; do
    line="$(trim "$line")"
    [[ -z "$line" || "${line:0:1}" == "#" ]] && continue
    [[ "$line" == export\ * ]] && line="$(trim "${line#export }")"
    if [[ "$line" == *=* ]]; then
      name="$(trim "${line%%=*}")"
      [[ "$name" == "$VAR" ]] || continue
      val="$(trim "${line#*=}")"
    elif [[ "$line" == sk-* ]]; then
      val="$line"
    else
      continue
    fi
    val="${val%\"}"; val="${val#\"}"; val="${val%\'}"; val="${val#\'}"
    val="$(trim "$val")"
    is_placeholder "$val" && continue
    printf '%s' "$val"
    return 0
  done < "$1"
  return 1
}

if [[ ! -f "$KEYS_FILE" ]]; then
  say "no key file at $KEYS_FILE"
  say "leaving $ENV_FILE alone — the labs use the key it already holds, or"
  say "canned answers if it holds none"
  exit 0
fi

# The key file is the one place the secret lives; keep it to its owner. A
# failure here (for example a file copied in as root) is only a warning — the
# key is still readable and the class still runs.
if [[ -O "$KEYS_FILE" && "$(stat -c '%a' "$KEYS_FILE" 2>/dev/null)" != "600" ]]; then
  chmod 600 "$KEYS_FILE" 2>/dev/null && say "tightened permissions on $KEYS_FILE to 600"
fi

if ! key="$(extract_key "$KEYS_FILE")" || [[ -z "$key" ]]; then
  say "no key filled in yet at $KEYS_FILE"
  say "leaving $ENV_FILE alone — the labs use the key it already holds, or"
  say "canned answers if it holds none"
  exit 0
fi

if [[ ! -f "$ENV_FILE" ]]; then
  if [[ -f "$ENV_EXAMPLE" ]]; then
    cp "$ENV_EXAMPLE" "$ENV_FILE" || { say "ERROR: cannot create $ENV_FILE"; exit 1; }
    say "created $ENV_FILE from .env.example"
  else
    printf '# Course 1258 — lab environment configuration\n' > "$ENV_FILE" \
      || { say "ERROR: cannot create $ENV_FILE"; exit 1; }
    say "created $ENV_FILE"
  fi
  chmod 600 "$ENV_FILE" 2>/dev/null
fi

if current="$(extract_key "$ENV_FILE")" && [[ "$current" == "$key" ]]; then
  say "$ENV_FILE already has this key (ends ...${key: -4}) — nothing to do"
  chmod 600 "$ENV_FILE" 2>/dev/null
  exit 0
fi

# Rewrite through a temporary file so an interrupted run cannot leave .env
# half-written, and so the key never sits in a world-readable file.
tmp="$(mktemp "${ENV_FILE}.sync.XXXXXX")" || { say "ERROR: cannot write in $PROJECT_DIR"; exit 1; }
trap 'rm -f "$tmp"' EXIT
chmod 600 "$tmp" 2>/dev/null

found=0
while IFS= read -r line || [[ -n "$line" ]]; do
  stripped="$(trim "$line")"
  if [[ "${stripped:0:1}" != "#" && "$stripped" == *=* \
        && "$(trim "${stripped%%=*}")" == "$VAR" ]]; then
    printf '%s=%s\n' "$VAR" "$key" >> "$tmp"
    found=1
  else
    printf '%s\n' "${line%$'\r'}" >> "$tmp"
  fi
done < "$ENV_FILE"
if [[ "$found" -eq 0 ]]; then
  printf '%s=%s\n' "$VAR" "$key" >> "$tmp"
fi

if ! mv "$tmp" "$ENV_FILE"; then
  say "ERROR: could not update $ENV_FILE (check permissions)"
  exit 1
fi
trap - EXIT
chmod 600 "$ENV_FILE" 2>/dev/null

say "key from $KEYS_FILE (ends ...${key: -4}) written to $ENV_FILE"
if [[ -n "${OPENAI_API_KEY:-}" ]]; then
  say "note: OPENAI_API_KEY is also set in the environment — a real environment"
  say "      variable wins over both files, so check it is the class key"
fi
exit 0
