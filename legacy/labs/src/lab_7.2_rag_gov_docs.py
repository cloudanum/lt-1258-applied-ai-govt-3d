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
# *Chapter 7 — Building with LLMs: APIs, RAG, and Agents · 40 minutes · JupyterLab + OpenAI API (local embedding fallback offline)*
#
# Four agency policy documents and a question whose answer is buried in one of
# them. This is the pattern behind every "chat with our documents" pilot:
# retrieve the right chunks, ground the answer in them, force citations — and
# verify those citations instead of trusting them.
#
# Cells marked `# YOUR TURN` ask you to edit ordinary text (a question, an
# instruction) or a number, and re-run the cell. Every cell runs as shipped:
# labelled canned answers keep the lab moving, and embeddings fall back to a
# deterministic local hasher when there is no key — so retrieval still works
# end to end, with no network.

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
#   Without it, chunk embeddings use a deterministic local fallback and
#   generation returns labelled canned answers — retrieval still works end to
#   end.
# - **How this notebook works:** every step is one provided cell — run it with
#   Shift+Enter and read what it prints. Cells marked `# YOUR TURN` ask you to
#   edit the text (ordinary quoted text — no code) or a number, and re-run the
#   cell. Everything runs as shipped, so you can never get stuck.

# %%
# ▶ Setup — run this cell first (click it, then Shift+Enter).
# It loads the course helper functions used by every step below.
from lab_helpers import *
lab_status()

# %% [markdown]
# The pipeline you are about to build — keep this picture in mind; every step
# below is one box of it. Run the cell to draw it.

# %%
show_rag_pipeline_diagram()

# %% [markdown]
# ## Steps
#
# 1. Run the load + chunk cell. ✓ You see *"N documents → M chunks."*
# 2. Run the embed cell. ✓ *"embedded M chunks."*
# 3. Retrieve the top 3 chunks for your question and inspect them.
#    ✓ The retrieved chunks are about the question.
# 4. Edit the grounding instruction so the model answers only from the
#    context and cites the source file. ✓ The grounded answer carries
#    `[filename]` citations.
# 5. Run the ungrounded comparison. ✓ You can see the difference.
#
# Run the Setup cell above first.

# %% [markdown]
# ### Step 1 — Load the four documents and chunk them (5 min)
#
# Chunk = one paragraph (blank-line separated), dropping tiny fragments. The
# cell prints the chunk count **and** the sizes — chunk size is the knob you
# turn in the stretch section.

# %%
chunks = load_policy_chunks()

# %% [markdown]
# ### Step 2 — Embed the chunks (4 min)
#
# One vector per chunk. With a key this uses OpenAI embeddings; offline it falls
# back to a deterministic local hasher (dim 256) — good enough to rank four
# small documents, which is why the lab works with no network.

# %%
vecs = embed_policy_chunks(chunks)

# %% [markdown]
# ### Step 3 — Retrieve the top 3 chunks and inspect them (8 min)
#
# The cell embeds your question with the **same** embedder, ranks the chunks by
# similarity, and prints the top 3. Read the chunks *before* generating — is
# the answer actually in them? Edit the question and re-run.

# %%
QUESTION = "How long are program case files kept before they are destroyed?"   # ← YOUR TURN: ask a different question, then re-run this cell

retrieved = show_retrieved_passages(chunks, vecs, QUESTION)

# %% [markdown]
# ### Step 4 — Generate grounded, with citations and quotes (10 min)
#
# The grounding instruction does the work. Yours must make the model:
#
# - answer **only** from the provided context,
# - cite the source file in `[brackets]` after every fact,
# - quote the exact sentence it relied on,
# - and say so plainly when the context does not contain the answer.
#
# That last clause is the one people leave out, and it is the one that stops the
# pipeline inventing an answer. A working instruction is provided — edit it and
# re-run.

# %%
GROUNDING_SYSTEM = """Answer ONLY from the provided context. After every fact, cite the source file in [brackets] and quote the exact sentence you relied on. If the context does not contain the answer, say so — do not use outside knowledge."""   # ← YOUR TURN: edit the grounding instruction, then re-run this cell

answer = ask_gov_docs(QUESTION, retrieved, GROUNDING_SYSTEM)

# %% [markdown]
# ### Step 5 — Run the ungrounded comparison (8 min)
#
# Same question, no context, no retrieval. The cell puts the two answers side
# by side — read them as a constituent would: one cites a file you can open,
# the other sounds equally confident and is wrong about the period.

# %%
compare_with_ungrounded(QUESTION, answer)

# %% [markdown]
# ## Stretch (not timed)
#
# The workbook page ends at Step 5. Everything below is optional.

# %% [markdown]
# ### Stretch A — Check every citation against the source file
#
# A citation is a claim, not a fact. The checker below verifies (a) every
# `[file.md]` tag names a real corpus file and (b) every quoted sentence
# actually appears in the corpus. Run it on your grounded answer.

# %%
check_answer_citations(answer)

# %% [markdown]
# ### Stretch B — Confirm or refute one DO NOW 7.D prediction
#
# Take one failure you predicted in DO NOW 7.D and test it. The question below
# is designed to fail cleanly: the answer is **absent from all four documents**.
# A well-grounded pipeline should say so instead of improvising.

# %%
HARD_QUESTION = "What is the agency's AI training budget for fiscal year 2027?"   # ← YOUR TURN: try your own unanswerable question, then re-run this cell

try_unanswerable_question(chunks, vecs, GROUNDING_SYSTEM, HARD_QUESTION)

# %% [markdown]
# ### Stretch C — Change the chunk size and re-run the failing question
#
# Paragraph chunks are one choice. Fixed-width windows are another. The cell
# re-chunks at ~450 characters, re-embeds, and re-runs your Step 3 question —
# did retrieval change? When would fixed windows beat paragraphs?

# %%
CHUNK_WIDTH = 450   # ← YOUR TURN: try a different window width (e.g. 200 or 800), then re-run this cell

try_fixed_width_chunks(QUESTION, width=CHUNK_WIDTH)

# %% [markdown]
# ## Deliverable
#
# 1. The top-3 retrieved chunks for the retention question, with scores.
# 2. The grounded answer whose citations **passed** the Stretch A checker.
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
# - **A red error naming `chunks` or `vecs`** — you ran a later cell before
#   Step 1 or 2. Run the notebook in order (Kernel → Restart & Run All).
# - **The answer cites the right file but a wrong quote** — that is exactly what
#   Stretch A catches. Require an exact quote per claim in `GROUNDING_SYSTEM`.
# - **Quote check says NOT FOUND for a real quote** — markdown emphasis (`**`)
#   breaks exact matching; the checker's normalizer handles it — make sure you
#   re-ran Stretch A after editing the answer.
# - **Grounded answer uses outside knowledge anyway** — strengthen the
#   instruction ("if the context does not contain the answer, say so") and show
#   the model what abstaining looks like (Stretch B).
# - **`dim=256` printed in Step 2** — you are on the local fallback (no key);
#   retrieval still works, scores just look different.

# %% [markdown]
# ---
# *Curious about the Python behind these steps? The full code-forward version
# of this lab lives in the `For_Python_Programmers/` folder.*
