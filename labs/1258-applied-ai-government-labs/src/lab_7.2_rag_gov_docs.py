# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Lab 7.2 — RAG over Government Documents
#
# *Chapter 7 — Building with LLMs: APIs, RAG, and Agents · 30 minutes · JupyterLab + OpenAI API (local embedding fallback offline)*
#
# Four agency policy documents and a question whose answer is buried in one of
# them. This is the pattern behind every "chat with our documents" pilot:
# retrieve the right chunks, ground the answer in them, force citations — and
# verify those citations instead of trusting them.
#
# Cells marked `# YOUR CODE` are yours to write. Every cell runs as shipped: a
# reference implementation and labelled canned answers keep the lab moving, and
# embeddings fall back to a deterministic local hasher when there is no key.

# %% [markdown]
# ## Objectives
#
# By the end of this lab, you will:
#
# - Build a working retrieval pipeline over real policy documents.
# - Force citations and verify them.
# - Diagnose retrieval failure rather than blaming the model.

# %% [markdown]
# ## Setup
#
# - **Corpus (synthetic training documents, modelled on public federal practice):**
#   - `data/corpus/ai_acceptable_use_policy.md`
#   - `data/corpus/data_governance_standard.md`
#   - `data/corpus/foia_processing_guidance.md`
#   - `data/corpus/records_retention_policy.md`
# - **Key:** `OPENAI_API_KEY` from the environment / course `.env` (never printed).
#   Without it, chunk embeddings use the deterministic local fallback in
#   `lab_common` and generation returns labelled canned answers — retrieval still
#   works end to end.
# - **Helpers:** `lab_common` provides `load_corpus`, `embed_texts`,
#   `cosine_topk`, `get_client`, `online`, `CHAT_MODEL`, `EMBED_MODEL`.

# %%
# API key: uses OPENAI_API_KEY from the environment (classroom VM); when run on
# the author's machine it falls back to the course .env file found by walking up
# from the notebook directory. The key is never printed.
import os, pathlib
def _load_api_key():
    if os.getenv("OPENAI_API_KEY") is not None:
        return  # environment wins — an explicitly empty value forces offline mode
    for p in [pathlib.Path.cwd(), *pathlib.Path.cwd().parents]:
        env = p / ".env"
        if env.is_file():
            for line in env.read_text().splitlines():
                k, _, v = line.partition("=")
                if k.strip() == "OPENAI_API_KEY" and v.strip():
                    os.environ["OPENAI_API_KEY"] = v.strip()
                    return
_load_api_key()
if not os.getenv("OPENAI_API_KEY"):
    print("OPENAI_API_KEY not set - ask your instructor, or the AI steps will be skipped/mocked.")

# %%
import re
import textwrap
import matplotlib.pyplot as plt
from lab_common import (load_corpus, embed_texts, cosine_topk,
                        get_client, online, CHAT_MODEL, EMBED_MODEL)

EMBEDDER_USED = {"name": "not yet run"}

def embed(texts):
    """Embed via lab_common; if the API call itself fails (quota, network),
    say so and use the deterministic local fallback instead of crashing."""
    try:
        vecs = embed_texts(texts)
        EMBEDDER_USED["name"] = (f"OpenAI {EMBED_MODEL}" if online()
                                 else "local hashing fallback (offline)")
        return vecs
    except Exception as e:
        print(f"({type(e).__name__} — embedding API failed; using the local fallback)")
        EMBEDDER_USED["name"] = "local hashing fallback (API call failed)"
        from lab_common import _local_embed
        return [_local_embed(t) for t in texts]

# %% [markdown]
# The pipeline you are about to build — keep this picture in mind; every step
# below is one box of it:

# %%
fig, ax = plt.subplots(figsize=(10, 2.4))
boxes = ["QUESTION", "embed", "retrieve\ntop-k chunks", "context +\nquestion", "LLM\ngrounded answer", "verify\ncitations"]
for i, label in enumerate(boxes):
    ax.add_patch(plt.Rectangle((i * 1.75, 0.3), 1.35, 0.55, fill=False))
    ax.text(i * 1.75 + 0.675, 0.575, label, ha="center", va="center", fontsize=9)
    if i < len(boxes) - 1:
        ax.annotate("", xy=(i * 1.75 + 1.72, 0.575), xytext=(i * 1.75 + 1.38, 0.575),
                    arrowprops=dict(arrowstyle="->"))
ax.text(2.6, 0.05, "same embedder for chunks and question", fontsize=8, style="italic")
ax.text(7.9, 0.05, "answer ONLY from the chunks", fontsize=8, style="italic")
ax.set_xlim(-0.1, 10.4); ax.set_ylim(-0.15, 1.1); ax.axis("off")
plt.tight_layout(); plt.show()

# %% [markdown]
# ## Steps
#
# ### Step 1 — Open the notebook
#
# You are here. Run the Setup cells above first (loader, imports, diagram).

# %% [markdown]
# ### Step 2 — Load the four documents and chunk them (4 min)
#
# Chunk = one paragraph (blank-line separated), dropping tiny fragments. Print
# the chunk count **and** the sizes — chunk size is the knob you will turn in
# Step 9.

# %%
docs = load_corpus()

def chunk_docs(docs, min_len=60):
    """One chunk per paragraph (blank-line separated), dropping tiny fragments."""
    out = []
    for d in docs:
        for para in [p.strip() for p in d["text"].split("\n\n") if len(p.strip()) > min_len]:
            out.append({"source": d["source"], "text": para})
    return out

chunks = chunk_docs(docs)
sizes = sorted(len(c["text"]) for c in chunks)
print(f"{len(docs)} documents -> {len(chunks)} chunks")
print(f"chunk sizes (chars): min {sizes[0]}, median {sizes[len(sizes) // 2]}, max {sizes[-1]}")
for d in docs:
    print(f"  {d['source']}: {sum(1 for c in chunks if c['source'] == d['source'])} chunks")

# %% [markdown]
# ### Step 3 — Embed the chunks (3 min)
#
# One vector per chunk. With a key this uses OpenAI embeddings; offline it falls
# back to a deterministic local hasher (dim 256) — good enough to rank four
# small documents, which is why the lab works with no network.

# %%
chunk_vecs = embed([c["text"] for c in chunks])
print(f"embedded {len(chunk_vecs)} chunks, dim={len(chunk_vecs[0])}")
print("embedder:", EMBEDDER_USED["name"])

# %% [markdown]
# ### Step 4 — Ask WITHOUT retrieval, and note what it invents (4 min)
#
# Same question, no context. Write down anything it states that you cannot
# confirm from the corpus — you will check it in Step 6.

# %%
QUESTION = "How long are program case files kept before they are destroyed?"

CANNED_UNGROUNDED = (
    "Program case files are generally kept for 3 years after the case is closed, "
    "after which they are destroyed. Some agencies keep them longer if litigation "
    "is expected. (Typical ungrounded answer: confident, plausible — and, for this "
    "corpus, wrong about the period.)")

def ask_plain(question):
    client = get_client()
    if client is None:
        print("(offline) canned ungrounded reply — answered from memory, unsourced:\n")
        return CANNED_UNGROUNDED
    try:
        resp = client.chat.completions.create(
            model=CHAT_MODEL, messages=[{"role": "user", "content": question}])
        return resp.choices[0].message.content
    except Exception as e:
        print(f"({type(e).__name__} — call failed; canned ungrounded reply:)\n")
        return CANNED_UNGROUNDED

print(ask_plain(QUESTION))

# %% [markdown]
# ### Step 5 — Retrieve the top 3 chunks and inspect them (5 min)
#
# Complete `retrieve`: embed the question with the **same** embedder, rank chunks
# by cosine similarity, return the top-k `(chunk, score)` pairs. Read the chunks
# *before* generating — is the answer actually in them?

# %%
def retrieve(question, k=3):
    # YOUR CODE: embed the question, rank chunks, return [(chunks[i], score), ...].
    # Reference implementation below — replace it with your own.
    qv = embed([question])[0]
    return [(chunks[i], score) for i, score in cosine_topk(qv, chunk_vecs, k)]

retrieved = retrieve(QUESTION, k=3)
for c, score in retrieved:
    print(f"[{score:.3f}] {c['source']}")
    print(textwrap.fill(textwrap.shorten(c["text"], 220), 100), "\n")

# %% [markdown]
# ### Step 6 — Generate grounded, with citations and quotes (5 min)
#
# The system prompt does the work: answer **only** from the chunks, cite the
# source file after each fact, and quote the exact sentence relied on. If the
# context does not contain the answer, the model must say so.

# %%
CANNED_GROUNDED = (
    "Program case files are kept for 7 years after the case is closed, then "
    "destroyed [records_retention_policy.md]. The policy states: \"Program case "
    "files are retained for 7 years after the case is closed.\" Note the contrast "
    "with routine administrative correspondence (3 years) in the same file.")
CANNED_ABSENT = ("The provided documents do not say anything about an AI training "
                 "budget for fiscal year 2027. No citation is possible.")

def _canned_grounded(question):
    # the canned stand-in knows two questions: the retention one and the absent one
    return CANNED_ABSENT if "budget" in question.lower() else CANNED_GROUNDED

GROUNDING_SYSTEM = (
    "Answer ONLY from the provided context. After every fact, cite the source "
    "file in [brackets] and quote the exact sentence you relied on. If the "
    "context does not contain the answer, say so — do not use outside knowledge.")
# YOUR CODE: tighten GROUNDING_SYSTEM — e.g. require one quote per claim, or a
# "confidence" line. Re-run and see what changes.

def grounded_answer(question, retrieved):
    client = get_client()
    context = "\n\n".join(f"[{c['source']}] {c['text']}" for c, _ in retrieved)
    if client is None:
        print("(offline) canned grounded reply:\n")
        return _canned_grounded(question)
    try:
        resp = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[
                {"role": "system", "content": GROUNDING_SYSTEM},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
            ])
        return resp.choices[0].message.content
    except Exception as e:
        print(f"({type(e).__name__} — call failed; canned grounded reply:)\n")
        return _canned_grounded(question)

answer = grounded_answer(QUESTION, retrieved)
print(answer)

# %% [markdown]
# ### Step 7 — Check every citation against the source file (3 min)
#
# A citation is a claim, not a fact. The checker below verifies (a) every
# `[file.md]` tag names a real corpus file and (b) every quoted sentence
# actually appears in the corpus. Run it on your grounded answer.

# %%
def _plain(s):
    """Strip markdown emphasis so quotes match the raw files."""
    return re.sub(r"[*_#`]", "", s)

def check_citations(answer, docs):
    files = {d["source"]: d["text"] for d in docs}
    for tag in sorted(set(re.findall(r"\[([\w.\-]+\.md)\]", answer))):
        print(f"source [{tag}]: {'exists' if tag in files else 'MISSING — fabricated citation'}")
    quotes = re.findall(r'"([^"]{20,})"', answer)
    if not quotes:
        print("no quoted sentences found — demand quotes in the system prompt")
    for q in quotes:
        hits = [name for name, text in files.items() if _plain(q).strip() in _plain(text)]
        print(f"quote \"{q[:60]}...\":",
              "verified in " + ", ".join(hits) if hits else "NOT FOUND — possible fabrication")

check_citations(answer, docs)

# %% [markdown]
# ### Step 8 — Confirm or refute one DO NOW 7.D prediction (3 min)
#
# Take one failure you predicted in DO NOW 7.D and test it. The question below
# is designed to fail cleanly: the answer is **absent from all four documents**.
# A well-grounded pipeline should say so instead of improvising.

# %%
HARD_QUESTION = "What is the agency's AI training budget for fiscal year 2027?"

retrieved_hard = retrieve(HARD_QUESTION, k=3)
print("top chunks for an unanswerable question (note the low scores):")
for c, score in retrieved_hard:
    print(f"  [{score:.3f}] {c['source']}: {textwrap.shorten(c['text'], 80)}")

print()
print(grounded_answer(HARD_QUESTION, retrieved_hard))
print("\nMy 7.D prediction confirmed/refuted (write here): ...")

# %% [markdown]
# ### Step 9 — Change the chunk size and re-run the failing question (3 min)
#
# Paragraph chunks are one choice. Fixed-width windows are another. Re-chunk at
# ~450 characters, re-embed, and re-run your failing question — did retrieval
# change? When would fixed windows beat paragraphs?

# %%
def chunk_by_size(docs, width=450):
    """Fixed-width character windows instead of whole paragraphs."""
    out = []
    for d in docs:
        flat = " ".join(d["text"].split())
        for i in range(0, len(flat), width):
            piece = flat[i:i + width]
            if len(piece) > 60:
                out.append({"source": d["source"], "text": piece})
    return out

chunks2 = chunk_by_size(docs)
vecs2 = embed([c["text"] for c in chunks2])
print(f"fixed-width: {len(chunks2)} chunks (was {len(chunks)} paragraphs)")
qv = embed([QUESTION])[0]
for i, score in cosine_topk(qv, vecs2, 3):
    print(f"[{score:.3f}] {chunks2[i]['source']}: {textwrap.shorten(chunks2[i]['text'], 90)}")

# %% [markdown]
# ## Deliverable
#
# 1. The top-3 retrieved chunks for the retention question, with scores.
# 2. The grounded answer whose citations **passed** the Step 7 checker.
# 3. One line: your DO NOW 7.D prediction, confirmed or refuted, and what fixed
#    (or would fix) the failure — chunking or prompting.

# %% [markdown]
# ## Reflection
#
# 1. Did chunking or prompting fix your failing question?
# 2. How would you detect a wrong citation at scale?
# 3. What would you tell a programme office promised "95% accuracy"?

# %% [markdown]
# ## Debrief (instructor-led)
#
# 1. Which answer would you put in front of a constituent, and why?
# 2. What breaks if chunks are too big? Too small?
# 3. When does RAG *fail* — and which failure is invisible to the user?
# 4. What does a FedRAMP production version of this pipeline look like?

# %% [markdown]
# ## Troubleshooting
#
# - **Every question retrieves the same chunks** — offline, the local hashing
#   embeddings are character-based and scores cluster; that is expected. With a
#   key, real embeddings sharpen the ranking.
# - **`IndexError` or `NameError` on `chunk_vecs`** — you ran a later cell before
#   Step 3. Run the notebook in order (Kernel → Restart & Run All).
# - **The answer cites the right file but a wrong quote** — that is exactly what
#   Step 7 catches. Require an exact quote per claim in `GROUNDING_SYSTEM`.
# - **Quote check says NOT FOUND for a real quote** — markdown emphasis (`**`)
#   breaks exact matching; the checker's `_plain` normalizer handles it — make
#   sure you re-ran Step 7 after editing the answer.
# - **Grounded answer uses outside knowledge anyway** — strengthen the system
#   prompt ("if the context does not contain the answer, say so") and show the
#   model what abstaining looks like (Step 8).
# - **`dim=256` printed in Step 3** — you are on the local fallback (no key);
#   retrieval still works, scores just look different.
