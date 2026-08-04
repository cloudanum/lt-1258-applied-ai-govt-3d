"""Enrich Ch05 'AI Security, Risks, and Responsible AI' (1258 rev a3).

Corrections (trace to 1258/research/refs-ch05-security-governance.md):
  - Slides 10/12/13: NIST AI 100-2e2023 citation -> AI 100-2e2025 (March 2025)
  - Slide 13: wrong figure caption (Predictive caption on a Generative slide)
  - Slide 27: unsourced 'federal health tracking' case study -> labeled hypothetical
  - Slide 42: spaCy has no EMAIL entity label; DLP detector count stale
  - Slide 46: IBM watsonx.ai -> watsonx.governance (product name)
  - Slide 61: FISMA = 2014 Modernization Act (not 2002 Management Act)
  - Slides 64-65: EU AI Act = in-force Regulation (EU) 2024/1689 + post-Omnibus
    timeline; slide 64's 'US has no plans to regulate' note deleted (false);
    slide 65's 'too big to fail' systemic-risk note corrected (10^25 FLOPs GPAI)
  - Slide 66: 'UN Ethics of AI' -> UNESCO Recommendation on the Ethics of AI
  - Slide 69: federal-policy moving-target slide updated to mid-2026 state and
    MOVED into the policy block (after the OMB M-25-21 slide)
  - SAIF 'six elements' garbling: belongs to AppB (refs Correction 6) — no SAIF
    slide exists in Ch05; flagged in the report, not edited here.

New slides (5, from refs Enrichment Candidates):
  N1 Securing AI Agents: Five Eyes Guidance (May 2026)   [after GenAI-attacks block]
  N2 Why Prompt Injection Can't Be Patched (NCSC)        [after slide 14]
  N3 OMB M-25-21: The Rules That Bind Your Agency        [policy block, after 61]
  N4 De-identification, Done Federally: NIST SP 800-188  [after data-minimization 31]  [flex]
  N5 AI Data Security: The Real Cost of Poisoning        [after poisoning slide 11]   [flex]

Trims (dedupe-only, 16 slides): 9, 18, 22, 23, 30, 33, 35, 37, 40, 44, 48, 49,
51, 59, 62, 68 (1-based, original deck) — exact/near-duplicates concentrated in
the attack-taxonomy / security-concepts sprawl; 68 is a verbatim repeat of
slide 2's objectives.
Lab slides (Lab 3.1/3.2/3.4 pointers) and the Do Now slide are untouched.
"""
from pathlib import Path
import pptx_tools as P

DECK = Path("/Users/iahmad/Creator/Courses_and_conferences/LT/1258/"
            "1258a4-author-input/decks/1258-Ch05-Security-Risks-Responsible-AI.pptx")

NIST_AML = ("Source: NIST — Adversarial Machine Learning: A Taxonomy and Terminology "
            "of Attacks and Mitigations (AI 100-2e2025), "
            "https://csrc.nist.gov/pubs/ai/100/2/e2025/final (verified 2026-08-01)")
EC_AIACT = ("Source: European Commission — AI Act regulatory framework, "
            "https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai "
            "(verified 2026-08-01)")


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def all_paras(slide):
    """Every text paragraph on the slide, across all shapes."""
    out = []
    for sh in slide.shapes:
        if sh.has_text_frame:
            out.extend(sh.text_frame.paragraphs)
    return out


def set_para_text(p, text):
    """Rewrite a paragraph's text, preserving the first run's formatting."""
    if p.runs:
        p.runs[0].text = text
        for r in p.runs[1:]:
            r.text = ""
    else:
        p.text = text


def replace_text(slide, old_sub, new_text):
    """Find the paragraph containing old_sub and replace its whole text."""
    for p in all_paras(slide):
        if old_sub in p.text:
            set_para_text(p, new_text)
            return True
    raise AssertionError(f"not found: {old_sub!r}")


def drop_para(slide, old_sub):
    for p in all_paras(slide):
        if old_sub in p.text:
            p._element.getparent().remove(p._element)
            return True
    raise AssertionError(f"not found: {old_sub!r}")


def add_bullet(slide, text):
    ph = P._body_placeholder(slide)
    assert ph is not None
    ph.text_frame.add_paragraph().text = text


def append_note(slide, text):
    tf = slide.notes_slide.notes_text_frame
    if tf.text.strip():
        tf.add_paragraph().text = text
    else:
        tf.text = text


def set_notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


# --------------------------------------------------------------------------- #
# (a) TEXT EDITS to existing slides (indices are 0-based, pre-append)
# --------------------------------------------------------------------------- #
def apply_edits(prs):
    s = list(prs.slides)
    assert len(s) == 69, f"expected 69 slides, found {len(s)}"

    # --- Slide 10 (idx 9): NIST AI 100-2e2023 -> e2025 citation
    replace_text(s[9], "AI.100-2e2023",
        "National Institute of Standards and Technology (2025) NIST Trustworthy and "
        "Responsible AI. NIST AI 100-2e2025. Adversarial Machine Learning: A Taxonomy "
        "and Terminology of Attacks and Mitigations. Fig. 1: Taxonomy of attacks on "
        "Predictive AI systems. Available at https://csrc.nist.gov/pubs/ai/100/2/e2025/final")
    append_note(s[9],
        "Citation updated to NIST AI 100-2e2025 (March 2025), which supersedes e2023; "
        "the updated edition expands the GenAI taxonomy (LLM, RAG, and agent-specific "
        "attacks) and adds a glossary. " + NIST_AML)

    # --- Slide 12 (idx 11): same citation update (Fig. 2, predictive)
    replace_text(s[11], "AI.100-2e2023",
        "National Institute of Standards and Technology (2025) NIST Trustworthy and "
        "Responsible AI. NIST AI 100-2e2025. Adversarial Machine Learning: A Taxonomy "
        "and Terminology of Attacks and Mitigations. Fig. 2: Taxonomy of attacks on "
        "Predictive AI systems. Available at https://csrc.nist.gov/pubs/ai/100/2/e2025/final")
    append_note(s[11],
        "Citation updated to NIST AI 100-2e2025 (March 2025), which supersedes e2023. "
        + NIST_AML)

    # --- Slide 13 (idx 12): e2025 citation + fix wrong figure caption
    replace_text(s[12], "AI.100-2e2023",
        "National Institute of Standards and Technology (2025) NIST Trustworthy and "
        "Responsible AI. NIST AI 100-2e2025. Adversarial Machine Learning: A Taxonomy "
        "and Terminology of Attacks and Mitigations. Taxonomy of attacks on Generative "
        "AI systems. Available at https://csrc.nist.gov/pubs/ai/100/2/e2025/final")
    append_note(s[12],
        "Two fixes: (1) the citation moved from the superseded e2023 to AI 100-2e2025 "
        "(March 2025); (2) the old caption mislabeled this Generative-AI slide with the "
        "Predictive-AI figure ('Fig. 2: Taxonomy of attacks on Predictive AI systems'). "
        "The e2025 GenAI taxonomy adds LLM-, RAG-, and agent-specific attacks. " + NIST_AML)

    # --- Slide 27 (idx 26): unsourced case study -> labeled hypothetical
    replace_text(s[26], "Federal health tracking system exposed",
        "Hypothetical case study: a federal health-tracking system exposes millions of "
        "patient records via misconfigured storage")
    append_note(s[26],
        "AUTHOR FLAG: this case study is illustrative, not a documented incident — no "
        "matching public breach could be verified. Substitute a named incident (e.g., a "
        "specific HHS or VA breach) at the next revision, or keep the hypothetical label.")

    # --- Slide 42 (idx 41): spaCy EMAIL fix + DLP detector count
    replace_text(s[41], "Identifies common entities such as",
        "Identifies common entities: PERSON, ORG, GPE, LOC, DATE — no built-in EMAIL label")
    replace_text(s[41], "over 100 types of PII",
        "Pre-trained with hundreds of infoType detectors: SSNs, government IDs, credentials, API keys")
    replace_text(s[41], "EMAIL\xa0=",
        "spaCy: PERSON = John Doe, LOC = 123 Elm Street (email needs regex or a custom component)")
    replace_text(s[41], "Includes confidence levels for each entity",
        "Google Cloud DLP: EMAIL_ADDRESS = john.doe@example.com, with likelihood scores per entity")
    append_note(s[41],
        "Corrected: stock spaCy English pipelines use the OntoNotes label scheme "
        "(PERSON, ORG, GPE, LOC, DATE, ...) with NO EMAIL entity — the previous example "
        "output was wrong for stock models; email detection needs a regex/custom "
        "component, or Google Cloud DLP's EMAIL_ADDRESS infoType. DLP now ships hundreds "
        "of built-in detectors (including credential/secret types), not 'over 100.' "
        "Sources: Explosion AI — spaCy trained pipelines (English), https://spacy.io/models/en ; "
        "Google Cloud — Sensitive Data Protection infoType reference, "
        "https://cloud.google.com/sensitive-data-protection/docs/infotypes-reference "
        "(verified 2026-08-01)")

    # --- Slide 46 (idx 45): IBM product name
    replace_text(s[45], "IBM watsonx.ai: governance",
        "IBM watsonx.governance: responsible-AI governance tool on cloud or on-premises")
    append_note(s[45],
        "Corrected product name: the governance product is watsonx.governance "
        "(watsonx.ai is the AI/model studio). Source: IBM — watsonx.governance, "
        "https://www.ibm.com/products/watsonx-governance (verified 2026-08-01)")

    # --- Slide 61 (idx 60): FISMA 2014 Modernization Act
    replace_text(s[60], "Federal Information Security Management Act",
        "FISMA (Federal Information Security Modernization Act of 2014): sets standards "
        "for securing federal information systems, including PII")
    append_note(s[60],
        "Corrected statute name: the operative law is the Federal Information Security "
        "MODERNIZATION Act of 2014 (P.L. 113-283), which amended the 2002 Management "
        "Act; it codifies DHS/CISA's role, Binding Operational Directives, and "
        "major-incident reporting. Source: CISA — Federal Information Security "
        "Modernization Act, "
        "https://www.cisa.gov/topics/cyber-threats-and-advisories/federal-information-security-modernization-act "
        "(verified 2026-08-01)")

    # --- Slide 64 (idx 63): EU AI Act in force + delete false US note
    P.retitle(prs, 63, "EU AI Act: Regulation (EU) 2024/1689")
    replace_text(s[63], "Comprehensive AI law",
        "Comprehensive AI law — in force since August 1, 2024, obligations phasing in through 2028")
    replace_text(s[63], "europarl.europa.eu",
        "https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai")
    set_notes(s[63],
        "Speaker Notes: The EU AI Act is IN FORCE (August 1, 2024) and phasing in — see "
        "the next slide for the post-Omnibus dates. The four-risk-tier content here "
        "remains accurate. The old note claiming the US 'has no plans to regulate AI' "
        "was deleted — false as of mid-2026: EO 14179 (Jan 2025) governs federal AI, "
        "binding OMB memos M-25-21/M-25-22 set agency rules, M-26-04 adds unbiased-AI "
        "procurement principles, and EO 14365 (Dec 2025) moves to preempt state AI "
        "laws. The US regulates by executive action rather than one comprehensive "
        "statute. " + EC_AIACT)

    # --- Slide 65 (idx 64): GenAI rules + post-Omnibus timeline; fix note
    P.retitle(prs, 64, "EU AI Act: GenAI Rules and Phase-In Timeline")
    # merge the three labeling lines into one dated bullet
    replace_text(s[64], "Content generated or modified",
        "AI-generated or modified content (images, audio, video, deepfakes) must be "
        "clearly labeled — applies from Aug 2, 2026")
    drop_para(s[64], "Must be clearly labeled as AI-generated")
    drop_para(s[64], "Images, audio or video, deepfakes")
    add_bullet(s[64], "AI Omnibus (in force July 27, 2026): 9th prohibition — AI "
        "nudification/CSAM tools — applies Dec 2026")
    add_bullet(s[64], "Annex III high-risk obligations apply Dec 2, 2027; Annex I "
        "product-embedded rules Aug 2, 2028")
    set_notes(s[64],
        "Speaker Notes: Under the AI Act, 'systemic risk' attaches to high-impact "
        "general-purpose AI models (cumulative training compute >= 10^25 FLOPs), "
        "triggering thorough evaluation and serious-incident reporting to the "
        "Commission — NOT the 2008 financial-crisis 'too big to fail' sense the old "
        "note described. Timeline shown is the post-Omnibus state (AI Omnibus "
        "Regulation in force July 27, 2026): prohibitions since Feb 2025, GPAI rules "
        "since Aug 2025, transparency/labeling from Aug 2, 2026, Annex III high-risk "
        "Dec 2, 2027, Annex I Aug 2, 2028. " + EC_AIACT)

    # --- Slide 66 (idx 65): UNESCO, not 'UN'
    P.retitle(prs, 65, "UNESCO Recommendation on the Ethics of AI")
    append_note(s[65],
        "Corrected label: this is the UNESCO Recommendation on the Ethics of AI "
        "(adopted November 2021 by 193 Member States — the first global standard on AI "
        "ethics; voluntary), a UNESCO instrument, not a UN General Assembly one. The "
        "four values on the slide match the source. Source: UNESCO — Recommendation on "
        "the Ethics of Artificial Intelligence, "
        "https://www.unesco.org/en/artificial-intelligence/recommendation-ethics "
        "(verified 2026-08-01)")

    # --- Slide 69 (idx 68): update the moving-target slide to mid-2026 state
    replace_text(s[68], "Executive orders and OMB memos on AI change",
        "Executive orders and OMB memos on AI change with administrations — verify at teaching time")
    replace_text(s[68], "Verify the current federal AI policy",
        "As of mid-2026: EO 14179 governs; EO 14110 revoked; AI Action Plan at ai.gov")
    replace_text(s[68], "Core obligations (privacy, security",
        "OMB M-25-21/M-25-22 set binding agency rules; M-26-04 adds unbiased-AI procurement")
    replace_text(s[68], "own AI policy is the operative rule",
        "EO 14365 (Dec 2025) moves to preempt state AI laws — state government use carved out")
    add_bullet(s[68], "NIST AI RMF under revision; privacy, security, testing, transparency persist")
    add_bullet(s[68], "Your agency's own AI policy remains the operative rule for daily work")
    set_notes(s[68],
        "Speaker Notes: The framing is unchanged — verify at teaching time — but the "
        "anchors are now concrete (as of mid-2026): EO 14179 (Jan 23, 2025) is the "
        "governing AI executive order (EO 14110 revoked); OMB M-25-21/M-25-22 (Apr "
        "2025) are the operative binding memos; M-26-04 (Dec 2025) implements "
        "unbiased-AI procurement principles; EO 14365 (Dec 2025) seeks to preempt "
        "state AI laws but expressly does not preempt state-government procurement/"
        "use rules; America's AI Action Plan lives at ai.gov; NIST AI RMF 1.0 is "
        "under revision with a critical-infrastructure profile concept note (Apr "
        "2026). Sources: White House — EO 14179, "
        "https://www.federalregister.gov/documents/2025/01/31/2025-02172/removing-barriers-to-american-leadership-in-artificial-intelligence ; "
        "OMB — memoranda index, https://www.whitehouse.gov/omb/information-resources/guidance/memoranda/ ; "
        "White House — EO 14365, "
        "https://www.federalregister.gov/documents/2025/12/16/2025-23092/ensuring-a-national-policy-framework-for-artificial-intelligence ; "
        "ai.gov (verified 2026-08-01)")


# --------------------------------------------------------------------------- #
# (b) NEW slides (appended; placed by the final arrange)
# --------------------------------------------------------------------------- #
NEW_SLIDES = [
    # N1 — after the GenAI-attacks / prompt-injection pair
    ("Securing AI Agents: Five Eyes Guidance (May 2026)", [
        "First joint CISA/NSA/Five Eyes guidance focused on agentic AI (May 1, 2026)",
        "Agents act on your behalf: compromise means actions taken, not just text",
        "Align agent risk management with your existing cybersecurity frameworks",
        "Least privilege on tools and data; human approval for high-impact actions",
        "Log inputs, outputs, and tool calls; start agents on low-risk tasks only",
        "Agent-specific defenses: see Chapter 7",
    ],
     "Speaker Notes: This is the reference government audiences will expect named in "
     "2026 — the first joint Five Eyes guidance (CISA, NSA, ASD's ACSC, CCCS, NCSC-NZ, "
     "NCSC-UK) on agentic AI services. Core message: agents take actions, so a "
     "compromised agent is a compromised operator, not just a wrong answer. Map agent "
     "risk onto frameworks the agency already runs, constrain tool/data access, gate "
     "consequential actions on humans, and log everything. Cross-reference Chapter 7 "
     "for agent architecture and defenses. Source: CISA — Careful Adoption of Agentic "
     "AI Services, https://www.cisa.gov/resources-tools/resources/careful-adoption-agentic-ai-services "
     "(verified 2026-08-01)"),

    # N2 — directly after slide 14 (GenAI attacks incl. prompt injection)
    ("Why Prompt Injection Can't Be Patched", [
        "SQL injection was fixed by separating data from instructions (parameterized queries)",
        "LLMs make no such distinction — to the model there is only the next token",
        "Treat the model as an inherently confusable deputy, not a fixable component (NCSC)",
        "Reduce impact: deterministic non-LLM safeguards, least-privilege tools, approval gates",
        "Log all inputs, outputs, tool calls; reject uses that can't tolerate residual risk",
        "Attack mechanics: Chapter 4; agent-specific defenses: Chapter 7",
    ],
     "Speaker Notes: The NCSC (Dec 2025) argues the SQL-injection analogy is dangerous: "
     "SQL injection was solvable because databases can enforce a data/instruction "
     "boundary; LLMs cannot — every token is just the next token — so prompt injection "
     "may never be fully mitigated. Design rules: deterministic (non-LLM) safeguards "
     "around the model, least-privilege tool access, human approval for high-impact "
     "actions, full logging, and walking away from use cases whose security can't "
     "tolerate the residual risk. Greshake et al. (2023) defined the indirect-injection "
     "attack class covered in Chapter 4. Sources: UK NCSC — Prompt injection is not SQL "
     "injection, https://www.ncsc.gov.uk/blog-post/prompt-injection-is-not-sql-injection ; "
     "Greshake et al. — Not what you've signed up for, https://arxiv.org/abs/2302.12173 "
     "(verified 2026-08-01)"),

    # N3 — policy block, after slide 61 (federal statutes)
    ("OMB M-25-21: The Rules That Bind Your Agency", [
        "Binding government-wide memo (April 2025); rescinded and replaced M-24-10",
        "Requires Chief AI Officers, governance boards, annual public AI use-case inventories",
        "High-impact AI — output driving decisions with legal or significant effect — needs risk practices",
        "Mandates a generative-AI acceptable-use policy — why your agency has one",
        "M-25-22: vendors may not train on non-public agency data without consent",
        "M-26-04 (Dec 2025): unbiased-AI principles for federal LLM procurement",
    ],
     "Speaker Notes: For federal AI *users* this is the operative rulebook, not the "
     "headline laws. M-25-21 created CAIOs and agency AI governance boards, requires "
     "the annual public AI use-case inventory (the federal version of the asset "
     "inventory slide), defines 'high-impact AI' (output serving as the principal "
     "basis for decisions with legal, material, binding, or significant effect on "
     "rights or safety) with mandatory minimum risk practices, and required every "
     "agency to publish a generative-AI acceptable-use policy. M-25-22 governs "
     "acquisition (competition, data rights, no vendor training on your non-public "
     "data); M-26-04 adds EO 14319's unbiased-AI principles for procured LLMs. "
     "National-security systems are excluded. Sources: OMB — M-25-21, "
     "https://www.whitehouse.gov/wp-content/uploads/2025/02/M-25-21-Accelerating-Federal-Use-of-AI-through-Innovation-Governance-and-Public-Trust.pdf ; "
     "OMB — memoranda index, https://www.whitehouse.gov/omb/information-resources/guidance/memoranda/ "
     "(verified 2026-08-01)"),

    # N4 — after slide 31 (data-minimization strategies: remove/mask/aggregate)
    ("De-identification, Done Federally: NIST SP 800-188", [
        "Masking is not de-identification — masked data can often be re-identified",
        "Pick a sharing model: publish, synthetic data, query interface, protected enclave",
        "Stand up a Disclosure Review Board before releasing any dataset",
        "Adopt a measurable de-identification standard; run re-identification studies",
        "Formal methods such as differential privacy give provable protection",
    ],
     "[flex] Depth slide — skip if short on time; the one line to land is 'masking is "
     "not de-identification.' SP 800-188 (NIST + US Census Bureau, 2023) is the federal "
     "how-to: choose a data-sharing model, govern releases through a Disclosure Review "
     "Board, and prove protection with re-identification studies or formal methods "
     "(differential privacy). Direct quote for emphasis: 'not all tools that merely "
     "mask personal information provide sufficient functionality for performing "
     "de-identification.' Source: NIST — SP 800-188, De-Identifying Government "
     "Datasets, https://csrc.nist.gov/pubs/sp/800/188/final (verified 2026-08-01)"),

    # N5 — after slide 11 (poisoning/evasion attacks)
    ("AI Data Security: The Real Cost of Poisoning", [
        "NSA/CISA/FBI joint guidance (May 2025): secure data across the AI lifecycle",
        "Split-view poisoning: corrupt curated web datasets for roughly $60–$1,000",
        "Frontrunning: up to 6.5% of Wikipedia snapshots demonstrably poisonable",
        "Defenses: provenance tracking, checksums, digital signatures, trusted infrastructure",
        "Encrypt training data (FIPS 140-3 storage); watch for drift versus poisoning",
    ],
     "[flex] Depth slide — the $60 figure is the memorable takeaway. The joint CSI "
     "deep-dives three data risks: supply chain, maliciously modified (poisoned) data, "
     "and drift. Split-view poisoning buys expired domains to serve poisoned content to "
     "dataset crawlers for ~$60–$1,000; frontrunning times malicious Wikipedia edits "
     "so snapshots capture them (up to 6.5% demonstrably poisonable). Ten best "
     "practices include provenance tracking, hashes/checksums, digital signatures, "
     "FIPS 140-3 validated storage, privacy-preserving techniques (differential "
     "privacy, federated learning), secure deletion, and ongoing risk assessment. "
     "Source: NSA/CISA/FBI — AI Data Security: Best Practices for Securing Data Used "
     "to Train & Operate AI Systems, "
     "https://media.defense.gov/2025/May/22/2003720601/-1/-1/0/CSI_AI_DATA_SECURITY.PDF "
     "(verified 2026-08-01)"),
]


# --------------------------------------------------------------------------- #
# (c) final arrangement (0-based indices into the post-append deck)
# --------------------------------------------------------------------------- #
# pre-append: old slides 1-69 -> idx 0-68; appended N1..N5 -> idx 69,70,71,72,73
N1, N2, N3, N4, N5 = 69, 70, 71, 72, 73
ORDER0 = [
    0, 1, 2, 3,                      # title, objectives, need for AI security, agenda
    4, 5, 6, 7,                      # four dimensions (dropped 8 = old 9 CTA recap)
    9, 10, N5, 11, 12, 13, N2, N1,   # NIST taxonomy block + poisoning economics + NCSC + agents
    14, 15, 16, 18, 19, 20,          # ATLAS, adversarial examples, FGSM, robustness, Lab 3.1, federal ATLAS
    23, 24, 25,                      # CIA triad
    26, 27, 28, 30, N4, 31, 33,      # privacy, securing AI, minimization, SP 800-188, practice, Lab 3.2
    35, 37, 38, 40, 41, 42,          # controls, operations, PII, gov PII, detection, masking
    44, 45, 46, 49,                  # Responsible AI, implementing, Do Now, bias & policy
    51, 52, 53, 54, 55, 56,          # threat modeling, insider threats x3, Lab 3.4, asset inventory
    57, 59, 60, N3, 68,              # GDPR/OECD, US laws, federal statutes, OMB M-25-21, moving-target
    62, 63, 64, 65, 66,              # legal implications, EU AI Act x2, UNESCO, summary
]

DROPPED_1BASED = [9, 18, 22, 23, 30, 33, 35, 37, 40, 44, 48, 49, 51, 59, 62, 68]


def main():
    prs = P.open_deck(DECK)
    apply_edits(prs)
    for title, bullets, notes in NEW_SLIDES:
        P.append_content(prs, title, bullets, notes)
    n = len(list(prs.slides._sldIdLst))
    assert n == 74, f"expected 74 slides after appends, found {n}"
    assert len(ORDER0) == 58
    assert len(set(ORDER0)) == 58
    assert sorted(set(range(74)) - set(ORDER0)) == [i - 1 for i in DROPPED_1BASED]
    P.arrange(prs, ORDER0)
    P.save(prs, DECK)
    print(f"saved {DECK.name}: {len(ORDER0)} slides")


if __name__ == "__main__":
    main()
