"""Enrich Ch02 'AI Applications Across Government and Public Data' (42 -> 52 slides).

Order of operations: (a) in-place text edits correcting fabricated/stale claims;
(b) append new slides (deepened PredPol cautionary slide, 8-slide gov-platforms
block, CISA Malware Next-Gen, Data.gov 2026); (c) ONE arrange() placing all 52
slides in final pedagogical order (old end-of-deck PredPol slide idx 41 dropped);
(d) save.

All factual claims trace to 1258/research/refs-ch02-gov-apps-platforms.md
(URLs verified live 2026-08-01).
"""
from pathlib import Path
import pptx_tools as P
import content_ch02_enrich as C

BASE = Path("/Users/iahmad/Creator/Courses_and_conferences/LT/1258")
DECK = BASE / "1258a4-author-input/decks/1258-Ch02-Applications-Public-Data.pptx"
VER = "(verified 2026-08-01)"


# --------------------------------------------------------------------------- #
# In-place edit helpers (edit run.text where possible to preserve formatting)
# --------------------------------------------------------------------------- #
def _iter_paras(slide):
    for sh in slide.shapes:
        if sh.has_text_frame:
            for p in sh.text_frame.paragraphs:
                yield p


def _set_para_text(p, new_text):
    if p.runs:
        p.runs[0].text = new_text
        for r in p.runs[1:]:
            r.text = ""
    else:
        p.add_run().text = new_text


def replace_para(prs, idx0, match, new_text):
    slide = list(prs.slides)[idx0]
    for p in _iter_paras(slide):
        if match in p.text:
            _set_para_text(p, new_text)
            return
    raise AssertionError(f"slide {idx0 + 1}: no paragraph containing {match!r}")


def delete_para(prs, idx0, match):
    slide = list(prs.slides)[idx0]
    for p in _iter_paras(slide):
        if match in p.text:
            p._p.getparent().remove(p._p)
            return
    raise AssertionError(f"slide {idx0 + 1}: no paragraph containing {match!r}")


def add_bullet_after(prs, idx0, anchor_match, new_text):
    """Append a paragraph to the text frame whose paragraphs contain the anchor."""
    slide = list(prs.slides)[idx0]
    for sh in slide.shapes:
        if sh.has_text_frame and any(anchor_match in p.text for p in sh.text_frame.paragraphs):
            p = sh.text_frame.add_paragraph()
            p.add_run().text = new_text
            return
    raise AssertionError(f"slide {idx0 + 1}: no text frame containing {anchor_match!r}")


def set_notes(prs, idx0, notes):
    list(prs.slides)[idx0].notes_slide.notes_text_frame.text = notes


# --------------------------------------------------------------------------- #
# (a) TEXT EDITS — corrections to existing slides (indices are 0-based, pre-arrange)
# --------------------------------------------------------------------------- #
def apply_text_edits(prs):
    # Slide 6 (idx 5) speaker notes: delete fabricated '$300M saved annually'.
    set_notes(prs, 5,
        "Speaker Notes:\n"
        "Provide an anecdote about how AI in grant application processing enabled faster fund "
        "allocation to disaster-hit regions.\n"
        "For real adoption scale, cite GAO's baseline review: about 1,200 federal AI use cases "
        "cataloged across 20 of 23 CFO Act agencies even in FY2022, with 35 recommendations for "
        "completing key requirements. (The earlier '$300 million saved annually' figure was "
        "unverifiable and has been removed.)\n"
        "Source: U.S. GAO — Artificial Intelligence: Agencies Have Begun Implementation but Need "
        "to Complete Key Requirements (GAO-24-105980), https://www.gao.gov/products/gao-24-105980 "
        f"{VER}")

    # Slide 11 (idx 10): replace Medium-cited '10x faster' and fabricated '15% fewer
    # diagnostic errors' with the FDA AI-enabled device list.
    replace_para(prs, 10, "10x faster than human radiologists",
        "Hundreds of AI-enabled medical devices are FDA-authorized for US marketing")
    replace_para(prs, 10, "medium.com",
        "https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-enabled-medical-devices")
    replace_para(prs, 10, "15% reduction in diagnostic errors",
        "Radiology leads the FDA list, with cardiology and neurology next")
    delete_para(prs, 10, "rcsed.ac.uk")
    set_notes(prs, 10,
        "Replaced two unsourced claims: '10x faster than radiologists' (cited only to a Medium "
        "post) and '15% fewer diagnostic errors at federal health centers' (no supporting source "
        "anywhere). The defensible, government-sourced evidence is the FDA's official list of "
        "AI-enabled medical devices authorized for marketing in the US — hundreds of devices, "
        "overwhelmingly radiology, with cardiology and neurology next; each entry carries an "
        "authorization date, submission number, and manufacturer. Regulation is the scaling "
        "mechanism: point students to the list rather than quoting accuracy stats.\n"
        "Source: U.S. FDA — Artificial Intelligence-Enabled Medical Devices, "
        "https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-enabled-medical-devices "
        f"{VER}")

    # Slide 14 (idx 13): delete fabricated '70% improvement in response times';
    # substitute CISA Malware Next-Gen pilot metrics.
    replace_para(prs, 13, "Enhanced response times", "A federal example")
    replace_para(prs, 13, "70% improvement",
        "CISA's Malware Next-Gen triaged 1,600 pilot submissions; about 200 proved malicious")
    set_notes(prs, 13,
        "Deleted the fabricated '70% improvement in federal response times with AI automation' "
        "claim — no federal source exists. Substituted the CISA Malware Next-Gen pilot metrics "
        "(about 200 of 1,600 submissions confirmed suspicious or malicious); the next slide "
        "tells the full CISA story.\n"
        "Source: BleepingComputer — CISA makes its Malware Next-Gen analysis system publicly "
        "available, https://www.bleepingcomputer.com/news/security/cisa-makes-its-malware-next-gen-analysis-system-publicly-available/ "
        f"{VER}")

    # Slide 16 (idx 15): DeepMind cooling 'up to 40% of cooling energy', not 15% of costs.
    replace_para(prs, 15, "cooling costs by 15%",
        "Example: DeepMind cut Google's data center cooling energy use by up to 40%*")
    replace_para(prs, 15, "deepmind.com/energy-efficiency",
        "*https://deepmind.google/discover/blog/deepmind-ai-reduces-google-data-centre-cooling-bill-by-40/")
    set_notes(prs, 15,
        "Detail how predictive maintenance uses IoT and AI to prevent costly repairs.\n"
        "Showcase how AI improves energy efficiency, reducing carbon footprints.\n"
        "Highlight AI's role in creating greener, smarter urban environments like Barcelona.\n"
        "Correction: the DeepMind figure is 'up to 40% of cooling energy' in live deployment "
        "(the deck previously said 15% of cooling costs; Google separately cited ~15% overall "
        "PUE-overhead improvement).\n"
        "Source: Google DeepMind — DeepMind AI reduces Google data centre cooling bill by 40%, "
        f"https://deepmind.google/discover/blog/deepmind-ai-reduces-google-data-centre-cooling-bill-by-40/ {VER}")

    # Slide 19 (idx 18): delete SF EMS dispatch example (nonexistent source).
    replace_para(prs, 18, "San Francisco",
        "Real federal crisis-AI use cases are listed in the DHS AI Use Case Inventory*")
    replace_para(prs, 18, "sanfranciscoems.com", "*https://www.dhs.gov/ai/use-case-inventory")
    set_notes(prs, 18,
        "Discuss AI's role in coordinating emergency response across data sources (911 calls, "
        "social media, traffic sensors, hospital capacity).\n"
        "Correction: the earlier 'AI-guided EMS dispatch reduced response times in San Francisco' "
        "example had no real source (sanfranciscoems.com does not exist) and has been removed. "
        "Predictive policing is no longer presented as a success story — it is taught as a "
        "cautionary case study later in this block.\n"
        "The authoritative way to check what agencies actually do with AI is the DHS AI Use Case "
        "Inventory.\n"
        "Source: U.S. Department of Homeland Security — AI Use Case Inventory, "
        f"https://www.dhs.gov/ai/use-case-inventory {VER}")

    # Slide 20 (idx 19) notes: drop the 'PredPol success story' framing.
    set_notes(prs, 19,
        "Discuss the capabilities and limits of video analytics in public spaces, including "
        "privacy and civil-liberties considerations.\n"
        "Public-space monitoring is high-stakes: pair this discussion with the predictive-policing "
        "cautionary case study that follows in this block.")

    # Slide 24 (idx 23): recast USCIS to PAiTH per the DHS inventory.
    P.retitle(prs, 23, "Administrative Automation: USCIS PAiTH GenAI Assistant")
    replace_para(prs, 23, "employs AI-powered tools to review visa applications",
        "PAiTH (Private AI Tech Hub): USCIS's internal, persona-based generative-AI assistant for staff")
    replace_para(prs, 23, "shorter processing times",
        "Personas support legal research, contracts, translation, developers, and security compliance")
    add_bullet_after(prs, 23, "Personas support legal research",
        "Deployed in a private cloud with PII and data-sovereignty controls")
    add_bullet_after(prs, 23, "Personas support legal research",
        "Mandatory human review before any AI output is used officially")
    set_notes(prs, 23,
        "Recast to match the official record: the documented USCIS AI story is PAiTH (Private AI "
        "Tech Hub), an internal persona-based generative-AI workforce assistant — not AI screening "
        "visa applications for completeness or fraud. Personas cover legal research, contracts, "
        "translation, developer, security-compliance, and CFO work. Guardrails: private-cloud "
        "deployment, PII/data-sovereignty controls, and mandatory human review before official "
        "use. Teach it as a model 'good government GenAI deployment.'\n"
        "Source: U.S. Department of Homeland Security — AI Use Case Inventory: USCIS, "
        f"https://www.dhs.gov/ai/use-case-inventory/uscis {VER}")

    # Slide 30 (idx 29): Data.gov scale + post-CKAN catalog.
    replace_para(prs, 29, "300,000 datasets",
        "Hosts 548,327 datasets (as of August 2026) from 120+ publishing organizations")
    replace_para(prs, 29, "Features tools for developers",
        "Rebuilt catalog (2025); programmatic access via DCAT/data.json feeds")
    set_notes(prs, 29,
        "Corrected scale: 548,327 datasets as of 2026-08-01 (was 'over 300,000'), from 120+ "
        "publishing organizations across federal, state, local, tribal, and university sources. "
        "The catalog was rebuilt in 2025 as a custom Flask/OpenSearch application that replaced "
        "the legacy CKAN system; the CKAN Action API no longer exists at catalog.data.gov, and "
        "the legacy CKAN catalog runs at catalog-old.data.gov only through fall 2026.\n"
        "AUTHOR FLAG: Lab 2.1's verification steps must be re-checked against the new catalog UI "
        "and the DCAT/data.json feeds before the next delivery.\n"
        "Source: GSA / Data.gov — catalog.data.gov homepage, https://catalog.data.gov/ " f"{VER}\n"
        "Source: GSA data.gov team — catalog.data.gov architecture wiki, "
        f"https://github.com/GSA/data.gov/wiki/catalog.data.gov {VER}")

    # Slide 38 (idx 37): keep Lab 2.1 launcher; add forward-pointer to Lab 7.3.
    add_bullet_after(prs, 37, "In your Workbook",
        "Bookmark a dataset you find — you will query it with an agent in Lab 7.3")
    set_notes(prs, 37,
        "Launcher. Keep the forward-pointer: students bookmark one dataset now and query it with "
        "their agent in Lab 7.3 (Citizen Services Triage Agent capstone). Note: Lab 2.1's "
        "verification steps were written against the legacy CKAN catalog and must be re-checked "
        "against the rebuilt catalog (see the 'Data.gov in 2026' slide).")


# --------------------------------------------------------------------------- #
def main():
    prs = P.open_deck(DECK)
    apply_text_edits(prs)

    # (b) append new slides (indices 42..52 at arrange time)
    t, b, n = C.PREDPOL
    P.append_content(prs, t, b, n)                    # idx 42
    for t, b, n in C.PLATFORM_SLIDES:
        P.append_content(prs, t, b, n)                # idx 43..50
    t, b, n = C.CISA_SLIDE
    P.append_content(prs, t, b, n)                    # idx 51
    t, b, n = C.DATAGOV_SLIDE
    P.append_content(prs, t, b, n)                    # idx 52

    # (c) one final arrange: every slide in its pedagogical position.
    # Old idx 41 (appended end-of-deck PredPol slide) is intentionally dropped;
    # its rebuilt replacement (idx 42) moves into the public-safety block.
    order0 = (
        list(range(0, 14))        # slides 1-14 (14 corrected)
        + [51]                    # CISA Malware Next-Gen
        + list(range(14, 20))     # slides 15-20 (16, 19, 20 corrected)
        + [42]                    # PredPol cautionary (moved into public-safety block)
        + list(range(20, 24))     # slides 21-24 (24 -> PAiTH)
        + list(range(43, 51))     # gov-platforms block (8 slides)
        + list(range(24, 30))     # slides 25-30 (30 corrected)
        + [52]                    # Data.gov in 2026
        + list(range(30, 41))     # slides 31-41 (Lab 2.1 launcher at 38)
    )
    assert len(order0) == 52, len(order0)
    assert sorted(order0) == [i for i in range(53) if i != 41]
    P.arrange(prs, order0)

    # (d) save
    P.save(prs, DECK)
    return len(list(prs.slides._sldIdLst))


if __name__ == "__main__":
    import zipfile
    n = main()
    assert zipfile.ZipFile(DECK).testzip() is None
    print(f"{DECK.name}: {n} slides, zip OK")
    for idx, title, w in P.inventory(DECK):
        print(f"{idx:>3}  {w:>4}w  {title}")
