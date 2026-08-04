"""
lab_common.py — shared helpers for the Course 1258 (rev a4) lab notebooks.

Design goals (per LT-Lab-Environment-Plan.md):
  * The OpenAI key is read from a **.env file** at the course root (or from real
    environment variables, which win if both are set). Students never paste a key
    into a notebook, and no key is ever committed: `.env` is git-ignored and only
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
# .env loading — no dependency required
# --------------------------------------------------------------------------- #
def load_dotenv(path=None):
    """Read KEY=VALUE lines from .env into os.environ without overwriting
    anything already set. Searches this file's directory and its parents so it
    works whether the notebook runs from labs/ or from the course root.

    Deliberately dependency-free: python-dotenv is not guaranteed on the VM
    image, and one 15-line reader is cheaper than another provisioning request.
    """
    candidates = [Path(path)] if path else [
        p / ".env" for p in [Path(__file__).resolve().parent, *Path(__file__).resolve().parents[:3]]
    ]
    for env_path in candidates:
        if not env_path.is_file():
            continue
        for raw in env_path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key, val = key.strip(), val.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = val
        return env_path
    return None


DOTENV_PATH = load_dotenv()

# Model + embedding names come from the environment / .env, with current
# low-cost aliases as defaults. One line to bump when a model retires.
CHAT_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")
EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")


# --------------------------------------------------------------------------- #
# OpenAI client (returns None cleanly when no key is present)
# --------------------------------------------------------------------------- #
def get_client():
    """Return an OpenAI client if a key is configured, else None (offline)."""
    if not os.getenv("OPENAI_API_KEY"):
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
def chat(messages, offline=None, **kwargs):
    """
    One chat completion; returns the assistant's message text.

    When no key is configured, returns `offline` (a canned string supplied by
    the caller) instead, so the lab keeps working with a realistic-looking
    response. Extra kwargs (e.g. temperature=...) are passed through to the API.
    """
    client = get_client()
    if client is None:
        return offline
    resp = client.chat.completions.create(model=CHAT_MODEL, messages=messages, **kwargs)
    return resp.choices[0].message.content


def chat_json(messages, offline=None, **kwargs):
    """
    Chat completion forced to JSON output; returns the parsed object.

    When no key is configured, returns `offline` (an already-parsed canned
    object supplied by the caller).
    """
    client = get_client()
    if client is None:
        return offline
    resp = client.chat.completions.create(
        model=CHAT_MODEL, messages=messages,
        response_format={"type": "json_object"}, **kwargs)
    return json.loads(resp.choices[0].message.content)


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
        resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
        return [d.embedding for d in resp.data]
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
