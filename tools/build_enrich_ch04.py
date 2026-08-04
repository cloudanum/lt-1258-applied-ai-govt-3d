"""Enrich Ch04 'Modern GenAI and Prompt Engineering' (51 -> 55 slides).

(a) In-place text edits (stale 2026 naming, mislabeled citations, old-chapter
    agenda/summary, notes artifacts) preserving run formatting where possible.
(b) Append 4 new slides (2026 cheat sheet, government AI access, reasoning
    effort knob [flex], structured outputs as a platform feature).
(c) One final arrange() permutation placing all 55 slides.
Every factual claim traces to 1258/research/refs-ch04-prompt-eng.md
(URLs verified live 2026-08-01).
"""
from pathlib import Path
import pptx_tools as P

BASE = Path("/Users/iahmad/Creator/Courses_and_conferences/LT")
DECK = BASE / "1258/1258a4-author-input/decks/1258-Ch04-ModernGenAI-PromptEng.pptx"

SRC_OPENAI_MODELS = "Source: OpenAI — Models, https://platform.openai.com/docs/models (verified 2026-08-01)"
SRC_ANTH_MODELS = "Source: Anthropic — Claude Models Overview, https://docs.anthropic.com/en/docs/about-claude/models/overview (verified 2026-08-01)"
SRC_VERTEX_MODELS = "Source: Google Cloud — Vertex AI Google Models, https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models (verified 2026-08-01)"
SRC_LLAMA = "Source: Meta — Llama Models, https://www.llama.com/ (verified 2026-08-01)"
SRC_OPENAI_REASONING = "Source: OpenAI — Reasoning Models Guide, https://platform.openai.com/docs/guides/reasoning (verified 2026-08-01)"
SRC_ANTH_THINKING = "Source: Anthropic — Extended Thinking / Adaptive Thinking, https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking (verified 2026-08-01)"
SRC_GEMINI_THINKING = "Source: Google — Gemini Thinking, https://ai.google.dev/gemini-api/docs/thinking (verified 2026-08-01)"
SRC_AZURE_REASONING = "Source: Microsoft Learn — Azure OpenAI Reasoning Models, https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/reasoning (verified 2026-08-01)"
SRC_VERTEX_PROMPTING = "Source: Google Cloud — Introduction to Prompting, https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/introduction-prompt-design (verified 2026-08-01)"
SRC_OPENAI_SO = "Source: OpenAI — Structured Outputs, https://platform.openai.com/docs/guides/structured-outputs (verified 2026-08-01)"
SRC_ANTH_SO = "Source: Anthropic — Structured Outputs, https://docs.anthropic.com/en/docs/build-with-claude/structured-outputs (verified 2026-08-01)"
SRC_GEMINI_SO = "Source: Google — Gemini Structured Output, https://ai.google.dev/gemini-api/docs/structured-output (verified 2026-08-01)"
SRC_NIST = "Source: NIST — AI RMF Generative AI Profile (NIST AI 600-1), https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf (verified 2026-08-01)"
SRC_GSA_OES = "Source: GSA Office of Evaluation Sciences — Evaluating GenAI Chat Tools, https://oes.gsa.gov/projects/2533-evaluating-gen-ai-chat-tools/ (verified 2026-08-01)"
SRC_PROMPT_REPORT = "Source: The Prompt Report (Schulhoff et al., TMLR 2025), https://arxiv.org/abs/2406.06608 (verified 2026-08-01)"
SRC_COT = "Source: Wei et al. — Chain-of-Thought Prompting Elicits Reasoning in Large Language Models (NeurIPS 2022), https://arxiv.org/abs/2201.11903 (verified 2026-08-01)"

# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _tf_with(slide, anchor):
    for sh in slide.shapes:
        if sh.has_text_frame and anchor in sh.text_frame.text:
            return sh.text_frame
    raise AssertionError(f"anchor not found: {anchor!r}")


def replace_in_runs(slide, old, new, count=1):
    n = 0
    for sh in slide.shapes:
        if not sh.has_text_frame:
            continue
        for p in sh.text_frame.paragraphs:
            for r in p.runs:
                if old in r.text:
                    r.text = r.text.replace(old, new)
                    n += 1
                    if n >= count:
                        return n
    raise AssertionError(f"text not found in runs: {old!r}")


def set_para_text(p, text):
    if p.runs:
        p.runs[0].text = text
        for r in p.runs[1:]:
            r._r.getparent().remove(r._r)
    else:
        p.text = text


def rewrite_bullets(slide, anchor, bullets):
    tf = _tf_with(slide, anchor)
    paras = list(tf.paragraphs)
    for i, b in enumerate(bullets):
        if i < len(paras):
            set_para_text(paras[i], b)
        else:
            np = tf.add_paragraph()
            np.text = b
    for p in paras[len(bullets):]:
        p._p.getparent().remove(p._p)


def drop_paragraph(slide, anchor):
    tf = _tf_with(slide, anchor)
    for p in tf.paragraphs:
        if anchor in p.text:
            p._p.getparent().remove(p._p)
            return
    raise AssertionError(f"paragraph not found: {anchor!r}")


def get_notes(slide):
    return slide.notes_slide.notes_text_frame.text if slide.has_notes_slide else ""


def set_notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def edit_notes(slide, old, new):
    t = get_notes(slide)
    assert old in t, f"notes text not found: {old!r}"
    set_notes(slide, t.replace(old, new))


def edit_notes_tail(slide, marker, new_tail):
    t = get_notes(slide)
    i = t.find(marker)
    assert i >= 0, f"notes marker not found: {marker!r}"
    set_notes(slide, t[:i] + new_tail)


# --------------------------------------------------------------------------- #
# (a) in-place text edits — indices are 0-based against the ORIGINAL 51 slides
# --------------------------------------------------------------------------- #
def text_edits(prs):
    s = list(prs.slides)

    # Slide 1 (idx 0): banner 'Chapter 6' -> 'Chapter 4' (only jogger in deck)
    replace_in_runs(s[0], "Chapter 6", "Chapter 4")

    # Slide 2 (idx 1): agenda described the old chapter — match current flow
    rewrite_bullets(s[1], "GenAI Ecosystems", [
        "The 2026 model landscape: families, tiers, and context windows",
        "Prompting fundamentals: elements, examples, and chain-of-thought",
        "Reasoning models and the effort control",
        "Output control: roles, formats, structured outputs, and grounding",
        "Evaluation and verification: rubrics, LLM-as-judge, government habits",
    ])
    set_notes(s[1],
        "Agenda rewritten to match the current slide flow — the old agenda described the "
        "pre-a3 chapter (GenAI capabilities, ecosystems, use cases, ethics).")

    # Slide 5 (idx 4): stale model names -> verified 2026 set, date-stamped
    rewrite_bullets(s[4], "GPT-5 / GPT-4o", [
        "OpenAI GPT-5.6 family (Sol / Terra / Luna) — 1.05M-token context",
        "Anthropic Claude Opus 5, Sonnet 5, Haiku 4.5",
        "Google Gemini 3.x Flash and Gemini 2.5 Pro",
        "Open-weight: Meta Llama 4 Scout / Maverick — self-host inside your boundary",
        "Multimodal is standard; names pinned as of Aug 2026 — they will change",
    ])
    set_notes(s[4],
        "Corrects stale 'GPT-5 / GPT-4o family' naming (GPT-4o is legacy; o-series is legacy). "
        "Categories still matter more than versions; the cheat-sheet slide that follows pins the "
        "current names in one place so labs stay current.\n"
        + SRC_OPENAI_MODELS + "\n" + SRC_ANTH_MODELS + "\n" + SRC_VERTEX_MODELS + "\n" + SRC_LLAMA)

    # Slide 7 (idx 6): unverifiable 'ChatGPT Gov' SKU; tier also gates context size
    replace_in_runs(s[6], "ChatGPT Gov", "ChatGPT Enterprise (FedRAMP)")
    replace_in_runs(s[6],
        "Rule of thumb: the tier determines what data you may put in — not the model",
        "Rule of thumb: the tier determines what data you may enter — and your context size")
    set_notes(s[6],
        "This is the 'free vs paid tiers' item Bill Appelbe asked for. Connect to the Chapter 3 "
        "data rule. As of Aug 2026 the ChatGPT context window itself is tier-gated (~27K free to "
        "400K reasoning on Pro), so tier choice is about more than data terms. 'ChatGPT Gov' could "
        "not be re-verified as a distinct SKU; OpenAI's government posture is now ChatGPT Enterprise "
        "and API Platform for FedRAMP.\n"
        "Source: OpenAI — ChatGPT Pricing, https://openai.com/chatgpt/pricing/ (verified 2026-08-01)\n"
        "Source: OpenAI — ChatGPT Enterprise and API Platform for FedRAMP, "
        "https://help.openai.com/en/articles/20001070-chatgpt-enterprise-and-api-platform-for-fedramp (verified 2026-08-01)")

    # Slide 8 (idx 7): context-window understatement -> 1M-token norm
    replace_in_runs(s[7],
        "Modern windows are large (hundreds of thousands of tokens) but not infinite",
        "1M-token windows are the 2026 frontier norm (GPT-5.6: 1.05M; Claude Opus 5: 1M)")
    set_notes(s[7],
        "Sets up RAG as the answer to 'my corpus is bigger than the window'. As of Aug 2026, "
        "1M-token windows are the frontier norm: GPT-5.6 family 1.05M; Claude Opus/Sonnet 5 1M; "
        "Gemini 2.5 Pro 1M; Meta claims 10M for Llama 4 (vendor claim — attribute it). The trade-off "
        "shifts from 'will it fit' to cost, latency, and attention quality over long inputs.\n"
        + SRC_OPENAI_MODELS + "\n" + SRC_ANTH_MODELS + "\n" + SRC_VERTEX_MODELS)

    # Slide 12 (idx 11): stray editing artifact in notes
    edit_notes(s[11], "helpful examples to start with!pen_spark",
               "helpful examples to start with!")

    # Slide 14 (idx 13): vague journal gesture -> The Prompt Report
    edit_notes(s[13],
        'Technical Insight: Reference "Journal of Artificial Intelligence Research" for studies on '
        "context's influence on AI comprehension.",
        "Technical Source: The Prompt Report — a systematic survey of 58 prompting techniques "
        "(Schulhoff et al., TMLR 2025).\n" + SRC_PROMPT_REPORT)

    # Slide 15 (idx 14): off-topic RLHF citation -> OpenAI prompt-engineering guide;
    # plus GSA OES federal evidence (refs: slide-15 enrichment)
    edit_notes_tail(s[14], "Reference\nOpenAI Blog",
        "Federal evidence (GSA OES evaluation of GSA's internal GenAI chat, 2025): 35% adoption in "
        "five weeks; a median of only 6 prompts per user; 82% never changed the default model; only "
        "16% gave feedback; top barriers were inaccurate content and poor output quality. This "
        "chapter teaches the habits the 82% never practice.\n"
        "Reference\n"
        "OpenAI Prompt Engineering Guide — the on-topic citation (the old RLHF blog post was about "
        "model training, not prompting): https://platform.openai.com/docs/guides/prompt-engineering\n"
        "Source: OpenAI — Prompt Engineering Guide, https://platform.openai.com/docs/guides/prompt-engineering (verified 2026-08-01)\n"
        + SRC_GSA_OES)

    # Slide 16 (idx 15): mislabeled 'Google AI Blog' citation -> Vertex prompting intro
    edit_notes_tail(s[15], "Reference\nGoogle AI Blog",
        "Reference\n"
        "Google Cloud Vertex AI — Introduction to Prompting (replaces the old 'Google AI Blog' link, "
        "which actually pointed at a post about emergent phenomena, not a prompting guide): "
        "https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/introduction-prompt-design\n"
        + SRC_VERTEX_PROMPTING)

    # Slide 17 (idx 16): 'multi-shot' is non-standard — drop the bullet
    drop_paragraph(s[16], "Multi-shot:")
    set_notes(s[16], get_notes(s[16]) +
        "\nTerminology note: 'multi-shot' is not a standard category — The Prompt Report's "
        "58-technique taxonomy has no such entry; larger example sets are simply few-shot. The "
        "bullet was removed from the slide.\n" + SRC_PROMPT_REPORT)

    # Slides 23 & 24 (idx 22, 23): vague 'AI Magazine' gesture -> CoT primary paper
    for i in (22, 23):
        edit_notes(s[i],
            'Technical Source: Reference studies from journals like "AI Magazine" that highlight '
            "the importance of interpretability in AI systems.",
            "Technical Source: Wei et al., 'Chain-of-Thought Prompting Elicits Reasoning in Large "
            "Language Models' (NeurIPS 2022) — the primary paper for this technique.\n"
            "Caveat for the transparency claim: NIST AI 600-1 documents confabulated logic and "
            "citations — a visible reasoning chain is not proof of correctness.\n"
            + SRC_COT + "\n" + SRC_NIST)

    # Slide 26 (idx 25): 'o-series' naming superseded — reasoning is a mode
    rewrite_bullets(s[25], "OpenAI o-series", [
        "Chain-of-thought (previous slides) is a manual trick: you ask the model to 'think step by step'",
        "Reasoning is now a built-in mode of the main model families, not a separate product",
        "OpenAI reasoning.effort (none → max); Claude adaptive thinking; Gemini thinking_level",
        "You ask the question and the model reasons — a huge shift since this course began",
    ])
    set_notes(s[25],
        "REFRAME the old CoT slides (kept just before this) as historical technique. Corrects "
        "superseded 'OpenAI o-series' naming: o-series is legacy — reasoning is a mode of the GPT-5.x "
        "family via reasoning.effort (none to max). Claude's manual 'extended thinking' is deprecated "
        "on Claude 4.6+ in favor of adaptive thinking steered by an effort parameter.\n"
        + SRC_OPENAI_REASONING + "\n" + SRC_ANTH_THINKING + "\n" + SRC_AZURE_REASONING)

    # Slide 32 (idx 31): same mislabeled Google citation -> Vertex prompting intro
    edit_notes_tail(s[31], "References\nGoogle AI Blog",
        "References\n"
        "Google Cloud Vertex AI — Introduction to Prompting (replaces the old 'Google AI Blog' link, "
        "which actually pointed at a post about emergent phenomena, not a prompting guide): "
        "https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/introduction-prompt-design\n"
        + SRC_VERTEX_PROMPTING)

    # Slide 46 (idx 45): federal-standard vocabulary — NIST 'confabulation'
    replace_in_runs(s[45],
        "AI creating plausible but inaccurate information",
        "Plausible but inaccurate content — NIST AI 600-1 calls this 'confabulation'")
    replace_in_runs(s[45],
        "Fabricating non-existent data or references",
        "Confabulated logic and citations that make wrong answers look justified")
    set_notes(s[45], get_notes(s[45]) +
        "\nNIST AI 600-1 (Generative AI Profile) risk #2 is Confabulation: confidently stated but "
        "erroneous or false content, explicitly including confabulated logic or citations. Risk #7 "
        "(Human-AI Configuration) covers automation bias and over-reliance — the reason the "
        "mitigation bullets matter.\n" + SRC_NIST)

    # Slide 51 (idx 50): summary recapped the old chapter (stale DALL-E) — rewrite
    rewrite_bullets(s[50], "DALL-E", [
        "Key takeaways",
        "The 2026 landscape: capable models, 1M-token context, government-ready tiers",
        "Prompting is a specification skill: role, task, context, format, constraints",
        "Reasoning is a mode you dial: match effort to task stakes and budget the cost",
        "Evaluation closes the loop: rubrics, verification habits, human accountability",
        "Closing thought",
        '"Generative AI is a transformative tool that enhances efficiency and creativity in '
        'governance, but its responsible use is essential to maintaining trust and fairness."',
        "Next steps",
        "Complete Lab 4.1 and save your best prompts as reusable templates",
        "Identify one content-heavy workflow where grounded, verified prompting could help",
    ])
    set_notes(s[50],
        "Recap rewritten to match the current chapter — the old summary recapped the pre-a3 chapter "
        "and named DALL-E (stale). Recap the highlights: the 2026 model landscape, the prompting "
        "spine, reasoning effort, and evaluation. Encourage participants to reflect on pilot "
        "workflows. Question: 'Which rung of the Lab 4.1 ladder bought you the most quality?'")


# --------------------------------------------------------------------------- #
# (b) new slides
# --------------------------------------------------------------------------- #
NEW_SLIDES = [
    # N1 — after old slide 5 (model landscape)
    ("The 2026 Model Cheat Sheet (as of Aug 2026)",
     ["OpenAI GPT-5.6: Sol (flagship), Terra (balanced), Luna (cost-sensitive) — 1.05M context",
      "Anthropic Claude: Opus 5, Sonnet 5, Haiku 4.5 — 1M context",
      "Google Gemini: 3.x Flash (newest GA), 2.5 Pro — 1M context",
      "Meta Llama 4 Scout / Maverick — open-weight; run inside your own boundary",
      "Every family now exposes a reasoning-effort control (next section)",
      "Names churn every few months — learn the pattern; this slide pins Aug 2026"],
     "Pinned, dated reference so the rest of the course can stay version-agnostic; re-check the "
     "vendor model pages at each revision. Llama 4's 10M-token context is Meta's own claim — "
     "attribute it if you mention it. Google's flagship naming is mid-transition (3.x Flash GA, "
     "newer Pro in preview), so the slide stays at family level.\n"
     + SRC_OPENAI_MODELS + "\n" + SRC_ANTH_MODELS + "\n" + SRC_VERTEX_MODELS + "\n" + SRC_LLAMA),

    # N2 — after old slide 7 (tiers)
    ("Government AI Access in 2026",
     ["FedRAMP-certified early 2026: ChatGPT Enterprise, Gemini for Government, Perplexity for Government",
      "OpenAI FedRAMP API traffic uses a dedicated endpoint: gov.api.openai.com",
      "Microsoft 365 Copilot runs in GCC, GCC High, and DoD — prompts stay in-tenant",
      "GSA OneGov offered ChatGPT Enterprise government-wide: $1 per agency for one year",
      "Decision rule stands: the approved tier determines what data you may enter"],
     "As of Aug 2026. FedRAMP's AI prioritization fast-track (conversational AI) completed in "
     "April 2026; certification criteria included SSO/SCIM/RBAC, no training on customer data, and "
     "GSA MAS availability. The OneGov deal (Aug 2025) supported OMB M-25-21/M-25-22 and included "
     "federal-employee training resources. Check the FedRAMP Marketplace for current status before "
     "procuring.\n"
     "Source: FedRAMP — AI Prioritization, https://www.fedramp.gov/ai/ (verified 2026-08-01)\n"
     "Source: OpenAI — ChatGPT Enterprise and API Platform for FedRAMP, "
     "https://help.openai.com/en/articles/20001070-chatgpt-enterprise-and-api-platform-for-fedramp (verified 2026-08-01)\n"
     "Source: Microsoft Learn — Microsoft 365 Copilot in U.S. Government Clouds, "
     "https://learn.microsoft.com/en-us/copilot/microsoft-365/gov-overview (verified 2026-08-01)\n"
     "Source: GSA — GSA Announces New Partnership with OpenAI (OneGov), "
     "https://www.gsa.gov/about-gsa/newsroom/news-releases/gsa-announces-new-partnership-with-openai-delivering-deep-discount-to-chatgpt-08062025 (verified 2026-08-01)"),

    # N3 — after old slide 29 (cost/latency/effort) [flex]
    ("Reasoning Effort: One Knob, Three Vendor Names",
     ["OpenAI reasoning.effort: none, low, medium, high, xhigh, max",
      "Anthropic: adaptive thinking, steered by an effort parameter",
      "Google Gemini: thinking_level low / medium / high",
      "Reasoning tokens are billed as output tokens on all three platforms",
      "Price spread (OpenAI, per million tokens): Sol $5/$30 vs. Luna $1/$6",
      "Match effort to stakes: eligibility analysis = high; form letter = low or none"],
     "[flex] Depth slide — skip if time is short; the previous slide carries the core message. "
     "Task mapping follows Google's guidance: low for lookups/classification, default for "
     "comparisons and drafting, high for multi-step analysis, math, and code. OpenAI recommends "
     "reserving at least 25K tokens of headroom for reasoning + output when experimenting, and "
     "capping spend with max_output_tokens. Azure gotcha: reasoning models reject temperature, "
     "top_p, penalties, and logprobs.\n"
     + SRC_OPENAI_REASONING + "\n" + SRC_ANTH_THINKING + "\n" + SRC_GEMINI_THINKING + "\n" + SRC_AZURE_REASONING),

    # N4 — after old slide 38 (structured outputs)
    ("Structured Outputs: Now a Platform Feature",
     ["All three major platforms guarantee schema-valid JSON — not just 'please output JSON'",
      "OpenAI Structured Outputs (strict JSON Schema); Claude and Gemini equivalents",
      "The guarantee is structural: schema-valid ≠ factually correct — validate values",
      "Handle refusals and token-limit cutoffs as normal failure modes",
      "This turns a chat model into a dependable workflow component (Lab 7.1)"],
     "Grounds the previous slide's JSON claim. OpenAI Structured Outputs uses strict JSON Schema "
     "(all fields required, additionalProperties false); Claude structured outputs is in public "
     "beta; Gemini uses response_format with a schema. All three vendors warn that schema "
     "adherence does not make the values true — always validate before the output feeds another "
     "system.\n"
     + SRC_OPENAI_SO + "\n" + SRC_ANTH_SO + "\n" + SRC_GEMINI_SO),
]


def build():
    prs = P.open_deck(DECK)
    assert len(list(prs.slides)) == 51, "expected the 51-slide baseline"
    text_edits(prs)
    for t, b, n in NEW_SLIDES:
        P.append_content(prs, t, b, n)
    # (c) one final permutation: old 0-50, appended N1..N4 at indices 51..54
    order = (
        list(range(0, 5)) + [51] +          # old 1-5, cheat sheet
        list(range(5, 7)) + [52] +          # old 6-7, gov access
        list(range(7, 29)) + [53] +         # old 8-29, reasoning-effort knob
        list(range(29, 38)) + [54] +        # old 30-38, structured outputs platform
        list(range(38, 51))                 # old 39-51
    )
    assert len(order) == 55 and sorted(order) == list(range(55))
    P.arrange(prs, order)
    P.save(prs, DECK)
    return len(list(prs.slides._sldIdLst))


if __name__ == "__main__":
    import zipfile
    n = build()
    print(f"saved {DECK.name}: {n} slides")
    assert zipfile.ZipFile(DECK).testzip() is None, "zip corruption"
    print("zipfile.testzip(): OK")
    for idx, title, w in P.inventory(DECK):
        print(f"{idx:>3}  {w:>4}w  {title}")
