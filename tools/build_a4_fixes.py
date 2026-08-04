"""a4 pass 1 — correctness fixes. No slide counts change here.

Three groups, all sourced from the Aug-2026 multi-model audit and a full
link-validation sweep of every URL in every deck:

  A. Dead hyperlink targets. Nine of the twelve broken links sat in
     slideN.xml.rels *behind visible text a previous pass had already
     corrected* — the words were fixed, the links never were. Retargeting
     restores the click without touching wording.
  B. Stale examples that survived the a3 sweep in summaries and speaker notes.
  C. EO 14409 (Jun 2026), the one federal policy instrument the decks miss.

Run:  python tools/build_a4_fixes.py
"""
import a4_common as A
import pptx_tools as P

# --------------------------------------------------------------- A. dead URLs
# old -> new. Every replacement was validated live on 2026-08-01.
URL_FIXES = {
    # Ch02 — the corrected citation is already ON the slide; point the link at it
    "http://health.google/ai-retinopathy":
        "https://jamanetwork.com/journals/jama/fullarticle/2588763",
    "http://deepmind.com/energy-efficiency":
        "https://deepmind.google/discover/blog/deepmind-ai-reduces-google-data-centre-cooling-bill-by-40/",
    "http://surtrac.net/":
        "https://aaai.org/papers/00434-13594-smart-urban-signal-networks-initial-application-of-the-surtrac-adaptive-traffic-signal-control-system/",
    "http://sanfranciscoems.com/":
        "https://www.dhs.gov/ai/use-case-inventory",
    # Ch02 — vendor pages that moved
    "http://paloaltonetworks.com/soar":
        "https://www.paloaltonetworks.com/cortex/cortex-xsoar",
    "http://darktrace.com":
        "https://www.darktrace.com/",
    "http://siemens.com/smart-maintenance":
        "https://www.siemens.com/global/en/products/services.html",
    "http://ibm.com/security/ai":
        "https://www.ibm.com/think/topics/ueba",
    "http://barcelona.cat/smartcity":
        "https://www.barcelona.cat/en/",
    "http://govtech.gov.sg/askjamie":
        "https://www.tech.gov.sg/products-and-services/",
    "https://www.tech.gov.sg/products-and-services/vica/":
        "https://www.tech.gov.sg/products-and-services/",
    # AppA — IRS reorganised these
    "https://www.irs.gov/statistics/soi-tax-stats":
        "https://www.irs.gov/statistics",
    "https://www.irs.gov/newsroom/irs-combats-covid-related-tax-fraud":
        "https://www.irs.gov/compliance/criminal-investigation",
    # bare-domain placeholders -> the real portals
    "http://www.data.gov": "https://www.data.gov/",
    "http://open.canada.ca": "https://open.canada.ca/en",
    "http://bluedot.global": "https://www.bluedot.global/",
    # www.canada.ca refuses automated requests outright; tbs-sct.canada.ca serves
    # the actual instrument — the Directive on Automated Decision-Making.
    "http://canada.ca/ai-policy":
        "https://www.tbs-sct.canada.ca/pol/doc-eng.aspx?id=32592",
    "https://www.canada.ca/en/government/system/digital-government/digital-government-innovations/responsible-use-ai.html":
        "https://www.tbs-sct.canada.ca/pol/doc-eng.aspx?id=32592",
    # dama-uk.org went offline entirely (even the apex 404s as of 2026-08-01).
    # The UK Government Data Quality Framework carries the same six dimensions
    # and is a live government source.
    "https://www.dama-uk.org/resources/the-six-primary-dimensions-for-data-quality-assessment":
        "https://www.gov.uk/government/publications/the-government-data-quality-framework",
}

# Source lines quoted inside speaker notes. These are prose, not rels, so they
# need a separate substring pass. NB: notes that *name* a dead URL in order to
# explain a correction ("siemens.com/... is not a real citation URL") are left
# alone on purpose — they document the fix.
NOTE_SOURCE_FIXES = [
    ("Ch02-Applications-Public-Data",
     "https://www.tech.gov.sg/products-and-services/vica/ (verified 2026-08-01)",
     "https://www.tech.gov.sg/products-and-services/ (VICA product page returned 404 on "
     "2026-08-01; cite the GovTech products index and confirm the live VICA URL at teaching time)"),
    ("Ch06-Data-for-AI",
     "https://www.dama-uk.org/resources/the-six-primary-dimensions-for-data-quality-assessment",
     "https://www.gov.uk/government/publications/the-government-data-quality-framework "
     "(DAMA-UK's site went offline in 2026; the UK Government Data Quality Framework carries "
     "the same six dimensions)"),
]


def fix_note_sources():
    n = 0
    for name, old, new in NOTE_SOURCE_FIXES:
        path = A.deck(name)
        prs = P.open_deck(path)
        hit = False
        for slide in prs.slides:
            if A.edit_notes(slide, old, new):
                hit = True
                n += 1
        if hit:
            P.save(prs, path)
            print(f"  {name}: source citation repointed in notes")
    return n

DECK_NAMES = [
    "Ch00-Course-Launch", "Ch01-AI-ML-Foundations", "Ch02-Applications-Public-Data",
    "Ch03-Desktop-GenAI", "Ch04-ModernGenAI-PromptEng", "Ch05-Security-Risks-Responsible-AI",
    "Ch06-Data-for-AI", "Ch07-Building-with-LLMs", "Ch08-Operations-Reporting",
    "Ch09-Summary-Roadmap", "AppA-ML-LifeCycle", "AppB-Security-DeepDive",
    "AppC-Transformer-LLM-Internals", "AppD-Classic-ML-DeepDive",
]

AUDIT = ("Link audit (a4, 2026-08-01): every URL in this deck was fetched and validated. "
         "Dead targets were repointed to the source already cited on the slide.")


def fix_urls():
    """Repoint the rel targets AND rewrite the URL where it is printed as visible
    footnote text, so the slide and the click agree."""
    total = 0
    for name in DECK_NAMES:
        path = A.deck(name)
        prs = P.open_deck(path)
        n = sum(A.retarget_url(prs, old, new) for old, new in URL_FIXES.items())
        shown = 0
        for slide in prs.slides:
            for old, new in URL_FIXES.items():
                if A.edit_bullet(slide, old, new, all_matches=True):
                    shown += 1
        if n or shown:
            P.save(prs, path)
            print(f"  {name}: {n} hyperlink(s) repointed, {shown} visible URL(s) rewritten")
            total += n
    return total


# ------------------------------------------------- B. stale examples in text
def fix_ch01():
    path = A.deck("Ch01-AI-ML-Foundations")
    prs = P.open_deck(path)
    s = list(prs.slides)

    # s7 notes — DALL-E/ChatGPT as *the* GenAI examples is three years stale
    A.edit_notes(s[6],
        "Share impactful examples like OpenAI’s DALL-E for image generation or ChatGPT for text generation.",
        "Share current examples: GPT-5 and Claude for text and code, Gemini for multimodal, "
        "and image models such as DALL-E 3 / Imagen. Name the capability, not one product — "
        "the leaders change between deliveries.")

    # s8 timeline — 'e.g., GPT-4' froze the 2020s row at 2023
    A.must_edit(s[7],
        "2020s Generative AI (e.g., GPT-4) transforms content creation, natural language processing, and diverse industry applications",
        "2022–2026 Generative AI goes mainstream — ChatGPT (2022), then reasoning models "
        "(GPT-5, Claude, Gemini) transform content creation, language processing, and agentic work",
        "Ch01 s8")
    A.append_notes(s[7],
        "Currency (a4): the 2020s row previously named GPT-4 as the exemplar. Reasoning models are the "
        "2025–26 development; keep this row generation-neutral so it survives the next model cycle.")

    # s18 — listing IBM Watson as a current specialized tool contradicts s22,
    # which teaches Watson Health's 2022 sale as the cautionary tale
    A.must_edit(s[17],
        "Specialized tools (Palantir, IBM Watson, Tableau) address advanced analytics and specific operational needs",
        "Specialized tools (Palantir, Databricks, Tableau) address advanced analytics and specific operational needs",
        "Ch01 s18")
    A.append_notes(s[17],
        "Correction (a4): IBM Watson was removed from this list. Slide 22 teaches Watson Health's 2022 sale "
        "as a cautionary tale — naming it here as a current specialized platform contradicted that. "
        "IBM's current AI platform is watsonx (see Ch05).")

    P.save(prs, path)
    print("  Ch01: 3 stale-example fixes")


def fix_ch02():
    path = A.deck("Ch02-Applications-Public-Data")
    prs = P.open_deck(path)
    s = list(prs.slides)

    stale = ("Share examples like Darktrace for ransomware detection and "
             "IBM Watson for insider threat management.")
    fresh = ("Share examples like Darktrace for network anomaly detection and UEBA "
             "(user and entity behaviour analytics) for insider risk.")
    for idx in (11, 12):                      # s12, s13 carry identical notes
        A.edit_notes(s[idx], stale, fresh)

    # s13 body — IBM Watson is not the insider-threat product; UEBA is the capability
    A.must_edit(s[12],
        "Example: IBM Watson detects insider threats using user behavior analysis",
        "Example: UEBA tools flag insider risk from anomalous access patterns",
        "Ch02 s13")
    A.append_notes(s[12],
        "Correction (a4): the example named IBM Watson, which is not IBM's insider-threat product and "
        "carries the retired Watson-Health branding. Reframed to the capability (UEBA); link repointed.")

    P.save(prs, path)
    print("  Ch02: 3 IBM-Watson fixes")


def fix_ch06():
    path = A.deck("Ch06-Data-for-AI")
    prs = P.open_deck(path)
    s = list(prs.slides)
    A.must_edit(s[21],
        "Examples: prominent examples of GenAI include large language models (LLMs) like ChatGPT, capable of generating human-quality text, and DALL·E, which creates realistic and imaginative images from text descriptions",
        "Examples: large language models (GPT-5, Claude, Gemini) generate human-quality text and code; "
        "image models (DALL-E 3, Imagen) create images from text descriptions",
        "Ch06 s22")
    A.edit_notes(s[21],
        "Provide clear examples of GenAI, like LLMs (ChatGPT) for text generation and DALL·E for image generation.",
        "Provide clear examples of GenAI: LLMs (GPT-5, Claude, Gemini) for text and code, image models "
        "(DALL-E 3, Imagen) for pictures.")
    P.save(prs, path)
    print("  Ch06: 1 stale-model fix")


def fix_ch08():
    path = A.deck("Ch08-Operations-Reporting")
    prs = P.open_deck(path)
    s = list(prs.slides)
    A.must_edit(s[9],
        "Training large-scale AI models like GPT-4 requires enormous computational resources",
        "Training frontier models (GPT-5, Claude, Gemini class) requires enormous computational resources",
        "Ch08 s10")
    P.save(prs, path)
    print("  Ch08: 1 stale-model fix")


def fix_appc():
    path = A.deck("AppC-Transformer-LLM-Internals")
    prs = P.open_deck(path)
    s = list(prs.slides)
    A.edit_notes(s[26],
        "For instance, OpenAI's GPT-3 has been used to write entire articles that mimic the style of human authors.",
        "For instance, GPT-class models routinely draft full articles in a requested style; the capability "
        "dates to GPT-3 and is now standard across GPT-5, Claude, and Gemini.")
    P.save(prs, path)
    print("  AppC: 1 stale-model fix")


# ------------------------------------------------------------- C. EO 14409
def add_eo_14409():
    """The decks carry EO 14179, 14319, 14365 and M-25-21/22/M-26-04 but stop
    before EO 14409 (Jun 2, 2026), which adds frontier-model cyber benchmarking
    and a voluntary pre-release evaluation framework."""
    path = A.deck("Ch05-Security-Risks-Responsible-AI")
    prs = P.open_deck(path)
    s = list(prs.slides)

    A.must_edit(s[52],
        "NIST AI RMF under revision; privacy, security, testing, transparency persist",
        "EO 14409 (Jun 2026) adds frontier-model cyber benchmarking (NSA/CISA) and pre-release review",
        "Ch05 s53")
    A.append_notes(s[52],
        "Added (a4) — EO 14409, 'Promoting Advanced Artificial Intelligence Innovation and Security' "
        "(signed June 2, 2026): directs CISA to expedite civilian-system cyber defence, creates a "
        "Treasury-led AI cybersecurity clearinghouse, and tasks NSA/CISA/Treasury with a classified "
        "benchmarking process for AI models' cyber capabilities, plus a voluntary framework giving "
        "government 30-day early access to frontier models before public release. It does not revoke "
        "EO 14179. The 'NIST AI RMF under revision' point moved into these notes to keep the slide at six "
        "bullets: AI RMF 1.0 (AI 100-1) is being revised and NIST published a Critical-Infrastructure "
        "profile concept note in April 2026.\n"
        "Source: Federal Register — https://www.federalregister.gov/documents/2026/06/05/2026-12034/"
        "promoting-advanced-artificial-intelligence-innovation-and-security (verified 2026-08-01)")

    P.save(prs, path)
    print("  Ch05: EO 14409 added to the policy-timeline slide")


if __name__ == "__main__":
    print("a4 pass 1 — correctness fixes")
    print("A. dead hyperlink targets")
    n = fix_urls()
    print(f"   total {n} hyperlinks repointed")
    fix_note_sources()
    print("B. stale examples")
    fix_ch01(); fix_ch02(); fix_ch06(); fix_ch08(); fix_appc()
    print("C. missing policy instrument")
    add_eo_14409()
    print("\nverifying decks unchanged in count and structurally sound:")
    for name in DECK_NAMES:
        n = A.verify(A.deck(name))
        print(f"   {name}: {n} slides, zip OK")
