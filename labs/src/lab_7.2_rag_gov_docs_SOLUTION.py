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
# # Lab 7.2 — RAG over Government Documents  *(SOLUTION / instructor copy)*
#
# **Chapter 7 — Building with LLMs: APIs, RAG & Agents**
#
# Retrieval-Augmented Generation (RAG) grounds an LLM's answer in *your* documents
# so it cites real sources instead of guessing. You will build a small RAG
# pipeline over a set of public agency documents, then compare a **grounded**
# answer (with retrieval) against an **ungrounded** one (without) and see the
# difference.
#
# **Objectives**
# 1. Chunk and embed a document corpus.
# 2. Retrieve the most relevant chunks for a question.
# 3. Generate an answer grounded in the retrieved text, with citations.
# 4. Observe how ungrounded answers drift or hallucinate.
#
# The retrieval steps run with **no API key** (a local embedding fallback lets the
# pipeline work offline); the final answer generation uses the model when a key is
# available.

# %%
# Instructor copies live in solutions/, one level below labs/ — find labs/
# (where lab_common.py, lab_helpers.py and data/ are) and run from there.
import os, sys
from pathlib import Path

for _cand in (Path.cwd(), *Path.cwd().parents):
    if (_cand / "lab_common.py").is_file():
        os.chdir(_cand)
        if str(_cand) not in sys.path:
            sys.path.insert(0, str(_cand))
        break

from lab_helpers import *

# %% [markdown]
# ## Step 1 — Load and chunk the corpus
#
# Long documents are split into chunks so retrieval can return just the
# relevant passage. Here each paragraph is a chunk (our docs are short).
#
# **Expected:** 4 documents → 26 chunks (6 / 7 / 7 / 6 per file).

# %%
chunks = load_policy_chunks()

# %% [markdown]
# ## Step 2 — Embed the chunks
#
# Each chunk becomes a vector. In production you would store these in a vector
# database (Chroma, FAISS, pgvector, Azure AI Search). Here we keep the vectors
# in memory and rank with cosine similarity — the same idea, no extra service.
#
# **Expected offline:** `embedded 26 chunks, dim=256` and the local hashing
# fallback named as the embedder.

# %%
vecs = embed_policy_chunks(chunks)

# %% [markdown]
# ## Step 3 — Retrieve
#
# **Expected:** all three top chunks come from `records_retention_policy.md`
# (scores ≈ 0.50 / 0.47 / 0.43 offline) — the retention answer is genuinely in
# the corpus. If a student's top chunks are from the wrong file, the question
# was edited into something the corpus does not cover — that is Stretch B's
# lesson, not a bug.

# %%
QUESTION = "How long are program case files kept before they are destroyed?"

retrieved = show_retrieved_passages(chunks, vecs, QUESTION)

# %% [markdown]
# ## Step 4 — Grounded answer (with citations)
#
# **Worked grounding instruction** below — the four load-bearing clauses:
# context-only, `[filename]` after every fact, an exact quote per fact, and an
# explicit "not in the context" escape hatch. The last is the one students
# leave out.

# %%
GROUNDING_SYSTEM = (
    "Answer ONLY from the provided context. After every fact, cite the source "
    "file in [brackets] and quote the exact sentence you relied on. If the "
    "context does not contain the answer, say so — do not use outside knowledge."
)

answer = ask_gov_docs(QUESTION, retrieved, GROUNDING_SYSTEM)

# %% [markdown]
# ## Step 5 — Ungrounded answer (no retrieval) — compare
#
# Ask the same question with no context. Without grounding, the model may give a
# plausible but unsourced number — which for policy work is a liability.
#
# **Expected contrast:** grounded says **7 years** with a citation; ungrounded
# says **3 years** with equal confidence. (The canned ungrounded answer is
# deliberately wrong about the period — that is the teaching point.)

# %%
compare_with_ungrounded(QUESTION, answer)

# %% [markdown]
# ## Stretch A — Check every citation against the source file
#
# **Expected:** the `[records_retention_policy.md]` tag exists, and the quoted
# sentence verifies against the corpus.

# %%
check_answer_citations(answer)

# %% [markdown]
# ## Stretch B — The unanswerable question
#
# **Expected:** low retrieval scores, and the grounded answer abstains instead
# of improvising. A pipeline that answers the budget question from this corpus
# is hallucinating — tighten the grounding instruction.

# %%
HARD_QUESTION = "What is the agency's AI training budget for fiscal year 2027?"

try_unanswerable_question(chunks, vecs, GROUNDING_SYSTEM, HARD_QUESTION)

# %% [markdown]
# ## Stretch C — Fixed-width chunks
#
# **Expected:** 17 fixed-width chunks instead of 26 paragraphs; the retention
# passage still ranks first, but chunks now cut across paragraph boundaries —
# the trade-off to narrate (no orphan sentences vs. split context).

# %%
CHUNK_WIDTH = 450

try_fixed_width_chunks(QUESTION, width=CHUNK_WIDTH)

# %% [markdown]
# ## Debrief
# 1. Which answer would you put in front of a constituent, and why?
# 2. Our chunks were whole paragraphs. What breaks if chunks are too big? Too small?
# 3. When does RAG *fail* — what kinds of questions can retrieval not help with?
# 4. What does a FedRAMP-authorized production version of this look like (where do
#    the documents, the vector store, and the model live)?
