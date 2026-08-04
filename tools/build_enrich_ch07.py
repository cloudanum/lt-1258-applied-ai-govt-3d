"""Enrich Ch07 'Building with LLMs: APIs, RAG, and Agents' (1258 rev a3).

Corrections (trace to 1258/research/refs-ch07-llm-apis-rag-agents.md):
  - Slide 9:  strict JSON-Schema Structured Outputs now guarantee adherence
  - Slide 10: Responses API is now primary; Assistants API dies Aug 26, 2026
  - Slide 6:  'stateless' nuance (Responses can store state server-side)
  - Slide 12: verified FedRAMP/IL ladder with dates (Azure OpenAI, Bedrock/Claude)
  - Slide 18: drop 'still early' MCP framing (spec 2025-11-25, broad adoption)
  - Slide 25: note Google's Gemini Enterprise rebranding of Vertex Vector Search
  - Slides 45-47: OpenAI self-serve fine-tuning wind-down -> re-scope the 'how'
                  to Azure OpenAI in-boundary / open-weight + HF PEFT
  - Slide 50: PEFT is the open-weight fine-tuning path

New slides (5): hybrid search, Ragas evaluation, MCP 2026 status/adoption,
tool allow-lists as an API feature, CISA/NSA + NIST CAISI agent guidance.
Labs 7.1/7.2/7.3 and Do Now 7.A untouched.
"""
from pathlib import Path
import pptx_tools as P

DECK = Path("/Users/iahmad/Creator/Courses_and_conferences/LT/1258/"
            "1258a4-author-input/decks/1258-Ch07-Building-with-LLMs.pptx")

SO = ("Source: OpenAI — Structured Outputs guide, "
      "https://platform.openai.com/docs/guides/structured-outputs (verified 2026-08-01)")
SDK = ("Source: OpenAI — openai-python README, https://github.com/openai/openai-python ; "
       "API Deprecations, https://platform.openai.com/docs/deprecations (verified 2026-08-01)")
DEPREC = ("Source: OpenAI — API Deprecations, "
          "https://platform.openai.com/docs/deprecations (verified 2026-08-01)")
FEDRAMP = ("Sources: Microsoft — Azure OpenAI authorization, "
           "https://devblogs.microsoft.com/azuregov/azure-openai-authorization/ ; "
           "Anthropic — Claude in Amazon Bedrock, "
           "https://www.anthropic.com/news/claude-in-amazon-bedrock-fedramp-high "
           "(verified 2026-08-01)")
MCP = ("Source: MCP — Specification (rev 2025-11-25), "
       "https://modelcontextprotocol.io/specification/latest (verified 2026-08-01)")


def body_tf(slide):
    ph = P._body_placeholder(slide)
    return ph.text_frame if ph is not None else None


def set_bullet(slide, para_idx, text):
    """Replace a bullet's text, preserving the first run's formatting."""
    p = body_tf(slide).paragraphs[para_idx]
    if p.runs:
        p.runs[0].text = text
        for r in p.runs[1:]:
            r.text = ""
    else:
        p.text = text


def add_bullet(slide, text):
    body_tf(slide).add_paragraph().text = text


def append_note(slide, text):
    tf = slide.notes_slide.notes_text_frame
    if tf.text.strip():
        tf.add_paragraph().text = text
    else:
        tf.text = text


# --------------------------------------------------------------------------- #
# (a) TEXT EDITS to existing slides (indices are 0-based, pre-append)
# --------------------------------------------------------------------------- #
def apply_edits(prs):
    s = list(prs.slides)

    # Slide 6 (idx 5): stateless nuance for the Responses era
    set_bullet(s[5], 2, "You send the whole conversation each time — stateless by default")
    add_bullet(s[5], "The Responses API can optionally store state server-side — an audit consideration")
    append_note(s[5],
        "2026 nuance: Chat Completions is stateless (you resend the conversation each call); the "
        "Responses API adds optional server-side state (stored responses / Conversations). Know where "
        "the transcript lives — that is an audit and records question. " + SDK)

    # Slide 9 (idx 8): strict Structured Outputs
    set_bullet(s[8], 0, "Structured Outputs (strict mode): the API guarantees JSON matches your schema")
    set_bullet(s[8], 1, "Supply a JSON Schema — all fields required, no extra properties; refusals flagged")
    set_bullet(s[8], 2, "Function calling: the model returns structured arguments to call your code")
    set_bullet(s[8], 3, "The mechanism the agent lab (7.3) is built on — still validate as defense-in-depth")
    append_note(s[8],
        "Updated 2026: strict JSON-Schema mode guarantees schema adherence — no parse-and-retry loop. "
        "Requires additionalProperties:false and all fields required; Pydantic supported via "
        "responses.parse; refusals are programmatically detectable. Keep validation as defense-in-depth. " + SO)

    # Slide 10 (idx 9): Responses API is primary now
    set_bullet(s[9], 0, "Use the openai>=1.x SDK; the Responses API is now the primary API")
    add_bullet(s[9], "Chat Completions is supported indefinitely; the Assistants API retires Aug 2026")
    append_note(s[9],
        "As of Aug 2026, OpenAI calls the Responses API 'the primary API for interacting with OpenAI "
        "models'; Chat Completions is 'supported indefinitely', so labs won't break either way. The "
        "Assistants API shuts down Aug 26, 2026 — do not teach it. Pin a current model (gpt-5.5 family "
        "as of Aug 2026). " + SDK)

    # Slide 12 (idx 11): verified FedRAMP / IL ladder
    set_bullet(s[11], 1, "Azure OpenAI: FedRAMP High (2024) up through IL6 to Top Secret (Apr 2025)")
    set_bullet(s[11], 2, "Claude via Amazon Bedrock: FedRAMP High + DoD IL4/5 in GovCloud (Jun 2025)")
    append_note(s[11],
        "Verified ladder: Azure OpenAI approved within FedRAMP High for Azure Government (Sept 2024), "
        "DoD IL4/IL5, IL6 in Azure Government Secret (Feb 2025), and Government Top Secret per ICD 503 — "
        "authorized at all classification levels as of Apr 16, 2025. Claude via Amazon Bedrock approved "
        "for FedRAMP High and DoD IL4/5 in AWS GovCloud (US) on Jun 11, 2025. " + FEDRAMP)

    # Slide 18 (idx 17): MCP is no longer 'early'
    set_bullet(s[17], 3, "Young but adopted by all major vendors — pilot non-sensitive tools first")
    append_note(s[17],
        "Tone update (2026): MCP is no longer 'emerging' — latest spec revision 2025-11-25; Claude, "
        "ChatGPT, VS Code, and Cursor all support it; OpenAI's own SDKs speak it; NIST CAISI (Feb 2026) "
        "is investing in agent protocol ecosystems. Keep the pilot-first caution. The spec's own security "
        "section: user consent before invoking any tool; tool descriptions are untrusted unless from a "
        "trusted server. " + MCP)

    # Slide 25 (idx 24): Google rebranding note (bullets unchanged)
    append_note(s[24],
        "Naming note (mid-2026): Google is folding Vertex AI Vector Search into its 'Gemini Enterprise "
        "Agent Platform' branding — the service and concepts are unchanged. All four options verified: "
        "FAISS (Meta), Chroma, pgvector (vectors inside PostgreSQL), Azure AI Search (managed, hybrid, "
        "in-boundary RAG grounding). Source: Google Cloud — Vector Search overview, "
        "https://cloud.google.com/vertex-ai/docs/vector-search/overview (verified 2026-08-01)")

    # Slides 45-47 (idx 44-46): fine-tuning re-scope
    append_note(s[44],
        "Teach the concept as evergreen, but date-stamp the platform story: OpenAI is winding down "
        "self-serve fine-tuning (orgs that never fine-tuned blocked since May 7, 2026; new-job creation "
        "for existing customers ends Jan 6, 2027). The durable government path is Azure OpenAI inside a "
        "boundary or open-weight models + Hugging Face PEFT. " + DEPREC)

    add_bullet(s[45], "Platform check (mid-2026): OpenAI is winding down self-serve fine-tuning")
    append_note(s[45],
        "Costs are unchanged, but the platform moved: as of mid-2026 OpenAI self-serve fine-tuning is "
        "being wound down — new-job creation for existing customers ends Jan 6, 2027; fine-tuned-model "
        "inference continues until base-model deprecation. Plan fine-tuning inside a boundary (Azure "
        "OpenAI) or on open-weight models. " + DEPREC)

    set_bullet(s[46], 3, "For agencies: Azure OpenAI in-boundary, or open-weight models + HF PEFT")
    add_bullet(s[46], "Often you combine: a fine-tuned model inside a RAG pipeline")
    append_note(s[46],
        "The escalation order (prompt -> RAG -> fine-tune) follows OpenAI's own optimization guidance: "
        "evals first, then prompting, then fine-tune. For the 'how' in government: Azure OpenAI "
        "fine-tuning inside a FedRAMP boundary, or open-weight models + PEFT from Hugging Face on your "
        "own hardware. Source: OpenAI — Model optimization guide, "
        "https://platform.openai.com/docs/guides/fine-tuning ; Hugging Face, https://huggingface.co/ "
        "(verified 2026-08-01)")

    # Slide 50 (idx 49): PEFT is the open fine-tuning path
    add_bullet(s[49], "PEFT: parameter-efficient fine-tuning of open-weight models in your boundary")
    append_note(s[49],
        "PEFT (parameter-efficient fine-tuning) is the open-weight fine-tuning path now that OpenAI "
        "self-serve fine-tuning is winding down — pairs with the fine-tuning slides. Source: Hugging "
        "Face, https://huggingface.co/ (verified 2026-08-01)")


# --------------------------------------------------------------------------- #
# (b) NEW SLIDES (appended, then arranged into position)
# --------------------------------------------------------------------------- #
NEW = [
    # N1 — after slide 23 (Embeddings)
    ("Hybrid Search: Vectors and Keywords Together",
     ["Vector search finds meaning; keyword search finds exact strings",
      "Government documents run on acronyms, form numbers, and exact citations",
      "Hybrid search runs both in one query and merges the ranked results",
      "Azure AI Search and Google vector search offer hybrid as a first-class mode",
      "pgvector pairs with PostgreSQL full-text search for the same effect"],
     "Tempers the 'vectors beat keyword' implication of the embeddings slide: for exact identifiers "
     "(a form number, 'Section 508') keyword wins; for paraphrase, vectors win; hybrid usually beats "
     "either alone. Source: Microsoft — Azure AI Search vector search overview, "
     "https://learn.microsoft.com/en-us/azure/search/vector-search-overview (verified 2026-08-01)"),

    # N2 — after slide 27 (When RAG Fails)
    ("Evaluating RAG with Ragas: From Vibes to Metrics",
     ["Ragas scores a RAG pipeline on separate, measurable dimensions",
      "Retrieval: did we fetch the right chunks for the question?",
      "Faithfulness: is every claim in the answer supported by the context?",
      "Generation: is the final answer relevant and well formed?",
      "Reference-free metrics — no human-labeled answer key required"],
     "[flex] Skippable if time is tight; this operationalizes the previous slide's 'evaluate retrieval "
     "and generation separately.' Natural extension: score Lab 7.2's grounded vs. ungrounded answers. "
     "Source: Es et al. — RAGAS (EACL 2024), https://arxiv.org/abs/2309.15217 ; Ragas docs, "
     "https://docs.ragas.io/ (verified 2026-08-01)"),

    # N3 — after slide 18 (MCP in Government)
    ("MCP in 2026: Spec Status and Adoption",
     ["Open standard; latest specification revision dated 2025-11-25",
      "Adopted across vendors: Claude, ChatGPT, VS Code, Cursor, and more",
      "OpenAI's Responses API and Agents SDK both speak MCP natively",
      "NIST CAISI (Feb 2026) is investing in open agent protocol ecosystems",
      "Young but real — pilot with non-sensitive tools first"],
     "Replaces the deck's original 'emerging fast' framing with dated facts. The spec is JSON-RPC 2.0 "
     "between hosts, clients, and servers, with a built-in Security & Trust section (consent before "
     "tool invocation; tool descriptions untrusted unless from a trusted server). Source: MCP — "
     "Specification, https://modelcontextprotocol.io/specification/latest ; NIST — CAISI AI Agent "
     "Standards Initiative, https://www.nist.gov/caisi/ai-agent-standards-initiative (verified 2026-08-01)"),

    # N4 — after slide 39 (Guardrails II)
    ("Tool Allow-Lists Are Now an API Feature",
     ["tool_choice.allowed_tools: the API itself restricts which tools the model may call",
      "MCP clients add static or dynamic tool filters — allow-lists at the protocol layer",
      "require_approval per tool: read = never, delete = always",
      "Keep the offered tool set small — every tool definition costs input tokens",
      "Lab 7.3 Stage C turns these controls from policy into running code"],
     "This is the previous slide's least-privilege principle expressed as parameters students can "
     "actually set. Approval maps are per-tool, e.g. {\"delete_file\": \"always\"}. OpenAI's guidance: "
     "aim for fewer than 20 initially available tools; tool schemas are billed as input tokens. "
     "Source: OpenAI — Function Calling guide, "
     "https://platform.openai.com/docs/guides/function-calling ; OpenAI Agents SDK MCP docs, "
     "https://openai.github.io/openai-agents-python/mcp/ (verified 2026-08-01)"),

    # N5 — after slide 40 (Guardrails III)
    ("What the Government Says About Agents (2026)",
     ["CISA, NSA, and Five Eyes partners: Careful Adoption of Agentic AI Services (May 2026)",
      "Least privilege; start agents on low-risk, non-sensitive tasks",
      "Human approval before high-impact actions — exactly your Lab 7.3 guardrails",
      "NIST CAISI (Feb 2026): agent standards, open protocols, agent identity research",
      "Your lab guardrails are not opinion — they are official guidance"],
     "First joint Five Eyes government security guidance on agentic AI; maps one-to-one onto "
     "Guardrails I-III. CAISI's three pillars: industry-led agent standards, community/open agent "
     "protocols, and agent authentication/identity research. Sources: CISA — Careful Adoption of "
     "Agentic AI Services, https://www.cisa.gov/resources-tools/resources/careful-adoption-agentic-ai-services "
     "; NIST — CAISI AI Agent Standards Initiative, "
     "https://www.nist.gov/caisi/ai-agent-standards-initiative (verified 2026-08-01)"),
]


def main():
    prs = P.open_deck(DECK)
    n0 = len(list(prs.slides))
    assert n0 == 51, f"expected 51 slides, found {n0}"

    apply_edits(prs)                                   # (a) text edits first

    for t, b, n in NEW:                                # (b) append new slides
        P.append_content(prs, t, b, n)
    # current indices: 0-50 original, 51=N1 hybrid, 52=N2 ragas, 53=N3 mcp,
    #                  54=N4 allow-lists, 55=N5 gov guidance

    # (c) one final arrange: full permutation, final pedagogical order
    order0 = (
        list(range(0, 18)) +        # slides 1-18 (through MCP in Government)
        [53] +                      # N3 MCP 2026 status/adoption
        list(range(18, 23)) +       # slides 19-23 (RAG concept -> embeddings)
        [51] +                      # N1 hybrid search
        list(range(23, 27)) +       # slides 24-27 (chunking -> RAG failures)
        [52] +                      # N2 Ragas evaluation
        list(range(27, 39)) +       # slides 28-39 (gov RAG -> Guardrails II)
        [54] +                      # N4 allow-lists as API feature
        [39] +                      # slide 40 (Guardrails III)
        [55] +                      # N5 government agentic guidance
        list(range(40, 51))         # slides 41-51 (failure modes -> summary)
    )
    assert sorted(order0) == list(range(56)), "order0 must be a permutation of 0..55"
    P.arrange(prs, order0)
    P.save(prs, DECK)
    print(f"saved {DECK.name}: {len(list(prs.slides))} slides")


if __name__ == "__main__":
    main()
