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
import textwrap
from lab_common import load_corpus, embed_texts, cosine_topk, get_client, CHAT_MODEL

# %% [markdown]
# ## Step 1 — Load and chunk the corpus
#
# Long documents are split into overlapping chunks so retrieval can return just
# the relevant passage. Here each paragraph is a chunk (our docs are short).

# %%
docs = load_corpus()
chunks = []
for d in docs:
    for para in [p.strip() for p in d["text"].split("\n\n") if len(p.strip()) > 60]:
        chunks.append({"source": d["source"], "text": para})
print(f"{len(docs)} documents -> {len(chunks)} chunks")

# %% [markdown]
# ## Step 2 — Embed the chunks
#
# Each chunk becomes a vector. In production you would store these in a vector
# database (Chroma, FAISS, pgvector, Azure AI Search). Here we keep the vectors in
# memory and rank with cosine similarity — the same idea, no extra service.

# %%
chunk_vecs = embed_texts([c["text"] for c in chunks])
print(f"embedded {len(chunk_vecs)} chunks, dim={len(chunk_vecs[0])}")

# %% [markdown]
# ## Step 3 — Retrieve

# %%
def retrieve(question, k=3):
    qv = embed_texts([question])[0]
    hits = cosine_topk(qv, chunk_vecs, k=k)
    return [(chunks[i], score) for i, score in hits]

QUESTION = "How long are program case files kept before they are destroyed?"
retrieved = retrieve(QUESTION, k=3)
for c, score in retrieved:
    print(f"[{score:.3f}] {c['source']}: {textwrap.shorten(c['text'], 90)}")

# %% [markdown]
# ## Step 4 — Grounded answer (with citations)

# %%
def grounded_answer(question, retrieved):
    client = get_client()
    context = "\n\n".join(f"[{c['source']}] {c['text']}" for c, _ in retrieved)
    if client is None:
        return "(offline) Retrieved context that would be sent to the model:\n" + context
    resp = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system",
             "content": "Answer ONLY from the provided context. Cite the source file in "
                        "brackets after each fact. If the answer is not in the context, say so."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
    )
    return resp.choices[0].message.content

print(grounded_answer(QUESTION, retrieved))

# %% [markdown]
# ## Step 5 — Ungrounded answer (no retrieval) — compare
#
# Ask the same question with no context. Without grounding, the model may give a
# plausible but unsourced number — which for policy work is a liability.

# %%
def ungrounded_answer(question):
    client = get_client()
    if client is None:
        return "(offline) With no retrieval, the model would answer from memory, unsourced."
    resp = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": question}],
    )
    return resp.choices[0].message.content

print("GROUNDED:\n", grounded_answer(QUESTION, retrieved))
print("\nUNGROUNDED:\n", ungrounded_answer(QUESTION))

# %% [markdown]
# ## Debrief
# 1. Which answer would you put in front of a constituent, and why?
# 2. Our chunks were whole paragraphs. What breaks if chunks are too big? Too small?
# 3. When does RAG *fail* — what kinds of questions can retrieval not help with?
# 4. What does a FedRAMP-authorized production version of this look like (where do
#    the documents, the vector store, and the model live)?
