"""
lab_common.py — shared helpers for the Course 1258 (rev a4) lab notebooks.

Design goals (per LT-Lab-Environment-Plan.md):
  * The OpenAI key is read from the class **key file** IT fills in
    (`/home/student/Keys/keys.txt` on the VM) or from a **.env file** at the
    course root — or from real environment variables, which win over both.
    Students never paste a key into a notebook, and no key is ever committed:
    the key file sits outside the course tree, `.env` is git-ignored, and only
    `.env.example` ships.
  * Every helper has an OFFLINE fallback so the labs (and the release-gate
    `nbconvert --execute` smoke run) work with the network disabled and no key:
      - embeddings  -> deterministic local hashing embedding
      - data.gov    -> cached_datagov.json
      - chat / JSON -> caller-supplied canned response
      - PII masking -> regex (the VM image also has Presidio for a richer version)
  * Nothing here contains a hard-coded key or model snapshot.
"""

from __future__ import annotations
import os
import re
import json
import math
import hashlib
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"


# --------------------------------------------------------------------------- #
# Key file + .env loading — no dependency required
# --------------------------------------------------------------------------- #
# On the classroom VM the class key is dropped into a file of its own, outside
# the course tree, and `start_jupyter_labs.sh` copies it into `.env` before
# JupyterLab starts. Reading it here as well costs nothing and covers what the
# launcher cannot: a notebook opened without the Desktop icon, or a VM where
# `.env` could not be rewritten. IT still only ever edits the one file.
KEYS_FILE = Path(os.getenv("COURSE_KEYS_FILE") or "/home/student/Keys/keys.txt")

# What the shipped templates carry in place of a key. Read as "no key", so an
# unfilled key file never shadows a real key sitting in `.env`.
_PLACEHOLDER_MARKS = ("REPLACE", "PASTE", "YOUR-KEY", "YOUR_KEY")


def _is_placeholder(val) -> bool:
    v = (val or "").strip().upper()
    return (not v or v == "SK-..." or v.startswith("SK-XXX")
            or any(m in v for m in _PLACEHOLDER_MARKS))


def _set_if_unset(name, val) -> None:
    """Assign only what the process does not already carry, so a real
    environment variable always wins. Note that the release smoke test exports
    OPENAI_API_KEY="" to force the offline path: empty still counts as set."""
    if name and name not in os.environ:
        os.environ[name] = val


def _env_pairs(text, bare_key_name=None):
    """(name, value) pairs from KEY=VALUE text, tolerating blank lines, `#`
    comments, an `export ` prefix, quotes and CRLF endings. With
    `bare_key_name`, a line holding nothing but the key (`sk-...`, no `NAME=`)
    is returned under that name — a pasted key often arrives that way.
    """
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].strip()
        if "=" in line:
            name, _, val = line.partition("=")
            yield name.strip(), val.strip().strip('"').strip("'")
        elif bare_key_name and line.startswith("sk-"):
            yield bare_key_name, line


def _read_text(path):
    """The file's text, or None when it is missing or unreadable. A key file
    copied in as root is readable only by root, and that has to degrade to
    canned answers rather than break the import of every notebook."""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def load_keys_file(path=None):
    """Read the class key file into os.environ. Returns the file when it was
    readable and had a key filled in, else None (no file, unreadable, or still
    holding the template placeholder).

    Runs *before* `load_dotenv()` and, like it, never overwrites what is
    already set — so precedence is: real environment variable > key file >
    `.env`, and the key IT copied in today beats a stale one left in `.env`.
    """
    key_path = Path(path) if path else KEYS_FILE
    text = _read_text(key_path)
    if text is None:
        return None
    used = None
    for name, val in _env_pairs(text, bare_key_name="OPENAI_API_KEY"):
        if _is_placeholder(val):
            continue
        _set_if_unset(name, val)
        used = key_path
    return used


def load_dotenv(path=None):
    """Read KEY=VALUE lines from .env into os.environ without overwriting
    anything already set. Searches this file's directory and its parents so it
    works whether the notebook runs from labs/ or from the course root.

    Deliberately dependency-free: python-dotenv is not guaranteed on the VM
    image, and one 15-line reader is cheaper than another provisioning request.
    """
    here = Path(__file__).resolve()
    # list(...) before slicing: Path.parents is only sliceable on 3.10+, and the
    # classroom VM image is not guaranteed to be newer than 3.9.
    candidates = [Path(path)] if path else [
        p / ".env" for p in [here.parent, *list(here.parents)[:3]]
    ]
    for env_path in candidates:
        text = _read_text(env_path)
        if text is None:
            continue
        for name, val in _env_pairs(text):
            _set_if_unset(name, val)
        return env_path
    return None


# Order matters — see load_keys_file().
KEYS_PATH = load_keys_file()
DOTENV_PATH = load_dotenv()

# Model + embedding names come from the environment / .env, with current
# low-cost aliases as defaults. One line to bump when a model retires.
# `or` rather than a getenv default: .env ships these keys present-but-empty
# (OPENAI_REASONING_MODEL=), and getenv's default only applies when the name is
# *absent*, so an empty value would sail through as "" and be sent as the model.
CHAT_MODEL = os.getenv("OPENAI_MODEL") or "gpt-5-mini"
EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL") or "text-embedding-3-small"

# Lab 4.1 rung 4 compares a standard model against a reasoning model on the same
# hard task. Env-driven so the classroom account decides which reasoning model is
# actually available — confirm the value before teaching, and leave it equal to
# CHAT_MODEL if the account has no reasoning model provisioned (the lab then
# reports that the comparison is unavailable rather than silently comparing a
# model with itself).
REASONING_MODEL = os.getenv("OPENAI_REASONING_MODEL") or CHAT_MODEL

# Lab 7.1 Exercise 3 varies `temperature`, which the gpt-5 family rejects
# outright ("Unsupported value: 'temperature' does not support 0.0 with this
# model. Only the default (1) is supported"). That exercise therefore pins its
# own temperature-capable model; everything else stays on CHAT_MODEL. Override
# in .env if your account carries a different one.
TEMPERATURE_MODEL = os.getenv("OPENAI_TEMPERATURE_MODEL") or "gpt-4.1-mini"


# --------------------------------------------------------------------------- #
# OpenAI client (returns None cleanly when no key is present *or works*)
# --------------------------------------------------------------------------- #
# A key that is configured is not the same as a key that can spend. An expired
# card, an exhausted classroom account or a revoked key all authenticate fine
# and then fail at call time with 429/401 — and the old code only checked that
# the variable was non-empty, so every helper raised straight out of the cell
# and stopped the notebook. Every call site here already carries a canned
# answer for the no-key case; this makes a *failing* key take that same path.
_API_FAILED = False


def note_api_failure(exc) -> None:
    """Record a failed live call and say so. Never silent: a student must not
    read a canned reply as live model output."""
    global _API_FAILED
    first, _API_FAILED = not _API_FAILED, True
    if first:
        print(f"[canned fallback] The OpenAI call failed — "
              f"{type(exc).__name__}: {str(exc)[:160]}\n"
              f"[canned fallback] The rest of this notebook uses its built-in "
              f"canned responses. The lab still works; the wording is fixed "
              f"rather than generated.")
    else:
        print(f"(canned fallback — {type(exc).__name__})")


def api_failed() -> bool:
    """True once a live call has failed in this session."""
    return _API_FAILED


def confirm(prompt: str, default: bool = False) -> bool:
    """Ask a yes/no question, or fall back to `default` where there is no stdin.

    Lab 7.3's approval gate is interactive by design — a student types y/n in
    JupyterLab. Under `nbconvert --execute` there is no stdin, so a bare
    input() raises StdinNotImplementedError and takes the whole notebook down.
    That only bites with a working key (offline, the agent returns its canned
    trace before ever reaching the gate), which is precisely when the release
    smoke test most needs to get through. Denying by default keeps the
    guardrail's meaning intact: no reviewer present, no consequential action.
    """
    try:
        return input(prompt).strip().lower() == "y"
    except Exception:
        # input() has already echoed `prompt`; only add the outcome.
        print(f"[no reviewer available — defaulting to "
              f"{'APPROVE' if default else 'DENY'}]")
        return default


def _call_with_retry(fn, attempts: int = 4, base: float = 1.5):
    """Run `fn()`, waiting out transient failures with exponential backoff.

    A classroom is a thundering herd: twenty students hitting one org key in
    the same minute trip org-level rate limits even on a perfectly healthy
    account, and a lab that gives up on the first 429 teaches the wrong lesson
    about reliability. Those are worth retrying.

    An exhausted balance, a bad key or an unsupported parameter are not — no
    amount of backoff fixes them — so they re-raise immediately and the caller
    falls back to its canned answer.
    """
    import time
    import random
    for i in range(attempts):
        try:
            return fn()
        except Exception as e:
            s = str(e).lower()
            # Match both the machine `code` and the human message text: the
            # SDK stringifies the whole error body, so e.g. an unsupported
            # parameter shows up as code `unsupported_value` *and* as the
            # prose "Unsupported value: 'temperature' does not support 0.0".
            permanent = any(k in s for k in (
                "insufficient_quota", "credit_balance", "invalid_api_key",
                "unsupported_value", "unsupported value",
                "unsupported_parameter", "unsupported parameter",
                "does not support", "does not exist", "model_not_found",
                "invalid_request_error"))
            if permanent or i == attempts - 1:
                raise
            time.sleep(base * (2 ** i) + random.random())


def get_client():
    """Return an OpenAI client if a key is configured and has not already
    failed, else None (offline). Returning None after the first failure is what
    lets the notebooks' existing `if client is not None:` branches fall back on
    their own, instead of every later cell re-raising the same error."""
    if not os.getenv("OPENAI_API_KEY") or _API_FAILED:
        return None
    try:
        from openai import OpenAI
        return OpenAI()  # reads OPENAI_API_KEY from the environment
    except Exception:
        return None


def online() -> bool:
    return get_client() is not None


# --------------------------------------------------------------------------- #
# Chat helpers: one-call text and JSON completions with canned offline fallback
# --------------------------------------------------------------------------- #
def chat(messages, offline=None, model=None, **kwargs):
    """
    One chat completion; returns the assistant's message text.

    When no key is configured, returns `offline` (a canned string supplied by
    the caller) instead, so the lab keeps working with a realistic-looking
    response. Extra kwargs (e.g. temperature=...) are passed through to the API.

    `model` defaults to CHAT_MODEL. Lab 4.1 rung 4 overrides it to run the same
    prompt on REASONING_MODEL and compare.
    """
    client = get_client()
    if client is None:
        return offline
    try:
        resp = _call_with_retry(lambda: client.chat.completions.create(
            model=model or CHAT_MODEL, messages=messages, **kwargs))
        return resp.choices[0].message.content
    except Exception as e:
        note_api_failure(e)
        return offline


def chat_json(messages, offline=None, **kwargs):
    """
    Chat completion forced to JSON output; returns the parsed object.

    When no key is configured, returns `offline` (an already-parsed canned
    object supplied by the caller).
    """
    client = get_client()
    if client is None:
        return offline
    try:
        resp = _call_with_retry(lambda: client.chat.completions.create(
            model=CHAT_MODEL, messages=messages,
            response_format={"type": "json_object"}, **kwargs))
        return json.loads(resp.choices[0].message.content)
    except Exception as e:
        # Also catches a model that returns unparseable JSON: the caller wants
        # a usable object either way, and the canned one is schema-correct.
        note_api_failure(e)
        return offline


# --------------------------------------------------------------------------- #
# Embeddings: OpenAI when available, deterministic local fallback otherwise
# --------------------------------------------------------------------------- #
def _local_embed(text: str, dim: int = 256) -> list[float]:
    """
    Deterministic offline embedding: hashed character 3-grams into `dim` buckets,
    L2-normalized. Not production-grade, but stable and good enough to rank a
    small document corpus so the RAG pipeline demonstrably works with no network.
    """
    vec = [0.0] * dim
    t = re.sub(r"\s+", " ", text.lower())
    for i in range(len(t) - 2):
        gram = t[i:i + 3]
        h = int(hashlib.md5(gram.encode()).hexdigest(), 16)
        vec[h % dim] += 1.0
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a list of texts. Uses OpenAI embeddings if a key is set, else local."""
    client = get_client()
    if client is not None:
        try:
            resp = _call_with_retry(
                lambda: client.embeddings.create(model=EMBED_MODEL, input=texts))
            return [d.embedding for d in resp.data]
        except Exception as e:
            note_api_failure(e)
    return [_local_embed(t) for t in texts]


def cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)) or 1.0
    nb = math.sqrt(sum(y * y for y in b)) or 1.0
    return dot / (na * nb)


def cosine_topk(query_vec, doc_vecs, k=3):
    """Return [(index, score), ...] for the top-k most similar doc vectors."""
    scored = [(i, cosine(query_vec, dv)) for i, dv in enumerate(doc_vecs)]
    scored.sort(key=lambda t: t[1], reverse=True)
    return scored[:k]


# --------------------------------------------------------------------------- #
# data.gov dataset search: live CKAN first, cached snapshot fallback
# --------------------------------------------------------------------------- #
def search_datasets(query: str, rows: int = 5) -> dict:
    """
    Search data.gov for public datasets. Tries the live CKAN API, then falls back
    to the bundled cached snapshot so the lab works behind government proxies.
    Returns {"source": "live"|"cached", "results": [{title, org, notes, tags}]}.
    """
    try:
        import requests
        r = requests.get(
            "https://catalog.data.gov/api/3/action/package_search",
            params={"q": query, "rows": rows},
            timeout=8,
            headers={"User-Agent": "lt-1258-lab"},
        )
        r.raise_for_status()
        payload = r.json()
        if payload.get("success"):
            return {"source": "live", "results": _shape(payload["result"]["results"])}
    except Exception:
        pass  # fall through to cache

    cached = json.loads((DATA_DIR / "cached_datagov.json").read_text())
    results = cached["result"]["results"]
    q = query.lower()
    filtered = [
        d for d in results
        if q in d["title"].lower()
        or q in d["notes"].lower()
        or any(q in tag.lower() for tag in d.get("tags", []))
    ] or results  # if nothing matches, return the full small catalog
    return {"source": "cached", "results": _shape(filtered[:rows])}


def _shape(raw_results: list[dict]) -> list[dict]:
    out = []
    for d in raw_results:
        out.append({
            "title": d.get("title", ""),
            "organization": (d.get("organization") or {}).get("title", ""),
            "notes": (d.get("notes", "") or "")[:300],
            "tags": [t if isinstance(t, str) else t.get("name", "")
                     for t in d.get("tags", [])][:6],
        })
    return out


# --------------------------------------------------------------------------- #
# PII masking guardrail: Presidio on the VM, regex fallback everywhere
# --------------------------------------------------------------------------- #
_SSN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
_EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
_PHONE = re.compile(r"\b\d{3}[.\-]\d{3}[.\-]\d{4}\b")


def mask_pii(text: str) -> str:
    """
    Redact SSNs, emails, and phone numbers. Tries Presidio (available on the VM
    image from the Lab 5.3 environment) for entity-aware masking, then falls back
    to regex so the guardrail always runs.
    """
    try:
        from presidio_analyzer import AnalyzerEngine
        from presidio_anonymizer import AnonymizerEngine
        analyzer = AnalyzerEngine()
        anonymizer = AnonymizerEngine()
        results = analyzer.analyze(text=text, language="en")
        return anonymizer.anonymize(text=text, analyzer_results=results).text
    except Exception:
        pass
    text = _SSN.sub("[REDACTED-SSN]", text)
    text = _EMAIL.sub("[REDACTED-EMAIL]", text)
    text = _PHONE.sub("[REDACTED-PHONE]", text)
    return text


def load_citizen_records() -> list[dict]:
    return json.loads((DATA_DIR / "citizen_records.json").read_text())["records"]


def load_corpus() -> list[dict]:
    """Load the RAG corpus as [{'source': filename, 'text': ...}, ...]."""
    docs = []
    for p in sorted((DATA_DIR / "corpus").glob("*.md")):
        docs.append({"source": p.name, "text": p.read_text()})
    return docs
