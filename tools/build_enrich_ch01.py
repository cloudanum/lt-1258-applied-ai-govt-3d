"""Enrich 1258-Ch01-AI-ML-Foundations.pptx (a3 revision).

(a) In-place text corrections per 1258/research/refs-ch01-foundations.md:
    - slide 8:  MYCIN/expert-systems misdate; Britannica links -> primary sources
    - slide 16/18/19: FedRAMP language -> 'FedRAMP Certified' / FedRAMP 20x
    - slide 20: IBM Watson Health stale -> overhype cautionary tale
    - slide 17/19/20: unsourced agency-adoption claims -> capability statements
    - slide 27: semi-supervised speaker note framing (IBM Think)
    - slide 36: drop unverifiable '90%' unstructured-text figure
    - slide 41: NER example 'United States' Organization -> Location
(b) Append 5 new research-grounded slides.
(c) One final arrange() with the full 53-slide permutation: CRISP-DM block
    (47-48 + new worked pass) moves before the Summary/objectives close.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pptx_tools as P

DECK = Path(__file__).resolve().parents[1] / "decks" / "1258-Ch01-AI-ML-Foundations.pptx"
V = "(verified 2026-08-01)"


# ---------------------------------------------------------------- helpers
def move_orphan_slide_parts(prs):
    """Rename slide parts that are reachable but NOT in sldIdLst (dead orphans).

    python-pptx renumbers all sldIdLst slide parts to slide1..N the first time
    `Presentation.slides` is accessed (a lazyproperty that calls
    rename_slide_parts), so a reachable orphan part named slide48.xml collides
    with the real 48th slide and produces duplicate zip entries. Move orphans
    above the max partname. NOTE: read sldIdLst from the part element directly —
    touching `prs.slides` here would trigger the renumber early and compact the
    name space before we measure it."""
    import re
    from pptx.oxml.ns import qn
    from pptx.opc.packuri import PackURI

    sldIdLst = prs.part._element.get_or_add_sldIdLst()
    keep = {id(prs.part.rels[e.get(qn("r:id"))].target_part) for e in sldIdLst}
    pat = re.compile(r"/ppt/slides/slide(\d+)\.xml$")
    parts = [p for p in prs.part.package.iter_parts() if pat.match(str(p.partname))]
    used = {int(pat.match(str(p.partname)).group(1)) for p in parts}
    nxt = max(used) + 1
    moved = 0
    for p in parts:
        if id(p) not in keep:
            p.partname = PackURI(f"/ppt/slides/slide{nxt}.xml")
            nxt += 1
            moved += 1
    return moved


def edit_run(slide, match, new_text):
    """Replace the text of the single run containing `match` (keeps formatting)."""
    hits = 0
    for sh in slide.shapes:
        if not sh.has_text_frame:
            continue
        for para in sh.text_frame.paragraphs:
            for run in para.runs:
                if match in run.text:
                    run.text = new_text
                    hits += 1
    assert hits == 1, f"edit_run {match!r}: {hits} hits"


def edit_para(slide, match, new_text):
    """Replace a whole paragraph's text, preserving the first run's formatting."""
    hits = 0
    for sh in slide.shapes:
        if not sh.has_text_frame:
            continue
        for para in sh.text_frame.paragraphs:
            if match in para.text and para.runs:
                para.runs[0].text = new_text
                for run in para.runs[1:]:
                    run.text = ""
                hits += 1
    assert hits == 1, f"edit_para {match!r}: {hits} hits"


def set_notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def append_notes(slide, text):
    tf = slide.notes_slide.notes_text_frame
    tf.text = (tf.text.rstrip() + "\n\n" + text) if tf.text.strip() else text


# ---------------------------------------------------------------- new slides
NEW = [
    # appended first -> index 48 (0-based); final position 14 (after slide 13)
    ("Case Study: ML Fraud Detection at Treasury",
     ["GAO estimates federal fraud losses of $233B–$521B per year (FY2018–2022 data)",
      "Treasury prevented and recovered $4B+ in fraud and improper payments in FY2024",
      "Up from $652.7M in FY2023 — roughly a sixfold increase in one year",
      "$1B of the FY2024 total came from ML identification of Treasury check fraud",
      "Scale: Treasury disburses about 1.4B payments worth $6.9T+ annually"],
     "This is the compelling, citable statistic the 'Why AI Matters in Governance' notes ask for. "
     "Walk the numbers: the GAO range shows the size of the problem; the Treasury result shows ML "
     "working at federal scale. Point out that $1B of the total is specifically ML identifying "
     "Treasury check fraud — a supervised classification/ranking use case students will meet "
     "again in the decision-tree section.\n"
     "Source: U.S. Department of the Treasury — 'Treasury Announces New Efforts to Combat "
     "Fraud and Improper Payments Using Enhanced Technology' (Oct. 2024), "
     "https://home.treasury.gov/news/press-releases/jy2650 " + V + "; "
     "U.S. GAO — GAO-24-105833, Federal Fraud estimate, "
     "https://www.gao.gov/products/gao-24-105833 " + V),
    # appended second -> index 49; final position 17 (after slide 15)
    ("Federal AI Adoption: The Numbers",
     ["Reported AI use cases at 11 selected agencies: 571 (2023) to 1,110 (2024)",
      "Generative AI use cases rose about ninefold: 32 to 282 in one year",
      "Examples: VA medical-imaging automation; HHS mining publications for polio outbreaks",
      "Reported barriers: privacy compliance, technical resources, keeping policies current",
      "Every agency publishes an AI use-case inventory — look up your own agency"],
     "As of GAO's July 2025 report. This gives students the real scale of federal adoption with "
     "citable numbers — reported use cases at the 11 selected agencies nearly doubled in one "
     "year, and generative AI roughly nine-x'ed. Note GAO's caveat that executive-branch AI "
     "guidance was significantly revised in early 2025. Activity idea: have each student find "
     "their own agency's public AI use-case inventory.\n"
     "Source: U.S. GAO — GAO-25-107653, 'Generative AI Use and Management at Federal Agencies' "
     "(July 2025), https://www.gao.gov/products/gao-25-107653 " + V),
    # appended third -> index 50; final position 34 (after slide 32, decision trees)
    ("From One Tree to a Forest: Random Forests",
     ["A single deep tree overfits — it memorizes the training data",
      "A random forest trains many trees and combines their votes (Breiman, 2001)",
      "Two randomness sources: bootstrap data samples and random feature subsets",
      "Errors decorrelate, so averaging cancels them — lower variance than one tree",
      "DN 1.A: explain this to your CIO, then to a citizen — same idea, different words"],
     "[flex] Depth slide supporting Do-Now 1.A (explain random forests to a CIO vs. a citizen); "
     "skippable if time is short — the takeaway is one line: many slightly-different trees voting "
     "beat one tree. Mechanics: each tree is grown on a bootstrap sample of the data, and only a "
     "random subset of features is considered at each split, so tree errors decorrelate and "
     "cancel when averaged. Citizen version: ask 100 experts who each saw a different subset of "
     "the evidence, then take the majority. CIO version: variance reduction, feature importances, "
     "and when to prefer gradient boosting (shallow sequential error-correcting trees). "
     "Breiman (UC Berkeley) invented random forests in 2001.\n"
     "Source: L. Breiman — 'Random Forests', Machine Learning 45 (2001), "
     "https://link.springer.com/article/10.1023/A:1010933404324 " + V + "; "
     "scikit-learn developers — User Guide 1.11.2 Ensemble Methods, "
     "https://scikit-learn.org/stable/modules/ensemble.html " + V),
    # appended fourth -> index 51; final position 41 (after slide 38)
    ("Case Study: VA Classifies Veterans' Claims with NLP",
     ["VA receives 1.5M+ disability claims per year; 65–80% arrive by mail or fax",
      "CCPS — VA's first ML API — classifies free-text disability descriptions",
      "'Ringing in my ears' maps to hearing loss — text classification at mission scale",
      "400K+ claims processed without human intervention — a 24x increase",
      "$1.5M saved in direct labor, speeding benefits decisions for veterans"],
     "The NLP section's mission anchor: connect tokenization and classification (the pipeline "
     "slides) to a real outcome — faster benefits for veterans. CCPS (Content Classification "
     "Predictive Service) reads the free-text disability description a veteran writes on a claim "
     "form and classifies it, so claims route without manual sorting. A sister effort applies "
     "OCR to handwritten PDFs. Emphasize the human impact: this is NLP as a citizen-centric "
     "service, not a demo.\n"
     "Source: Presidential Innovation Fellows / VA Office of the CTO — 'VA: Using Machine "
     "Learning to Deliver Veterans Benefits Faster' (2020), "
     "https://presidentialinnovationfellows.gov/projects/va-using-machine-learning-to-deliver-veterans-benefits-faster/ " + V),
    # appended fifth -> index 52; final position 51 (after slide 48, before Summary)
    ("CRISP-DM Worked Pass: Payment Fraud Detection",
     ["Business understanding: cut improper payments without delaying legitimate ones",
      "Data understanding and preparation: payment records, check data, confirmed fraud cases",
      "Modeling: classification flags high-risk transactions and checks",
      "Evaluation: precision matters — false flags burden honest recipients",
      "Deployment: screen at scale, monitor for drift, iterate (Treasury FY2024, slide 14)"],
     "One concrete pass through the CRISP-DM cycle using the Treasury case study from earlier "
     "in the chapter, so the six phases stop being abstract. Stress that the phases iterate — "
     "deployment findings feed the next round of business understanding — and that the sequence "
     "is not rigid. In evaluation, connect 'precision matters' back to the metrics slide: a "
     "false positive here is an honest citizen's payment delayed.\n"
     "Source: Data Science Process Alliance — 'CRISP-DM' (guide: Chapman et al., 2000), "
     "https://www.datascience-pm.com/crisp-dm-2/ " + V + "; "
     "U.S. Department of the Treasury — press release (Oct. 2024), "
     "https://home.treasury.gov/news/press-releases/jy2650 " + V),
]


# ---------------------------------------------------------------- text edits
def apply_edits(prs):
    s = list(prs.slides)

    # --- Slide 8: history milestones (MYCIN misdate + primary sources) ---
    edit_run(s[7], "1980s Expert systems such as MYCIN and XCON emerge",
           "1965–1980s Expert systems (Dendral 1965; MYCIN early 1970s; XCON 1980) "
           "encode expert rules for medicine and computing ")
    edit_run(s[7], "britannica.com/event/Dartmouth-Conference",
           "https://home.dartmouth.edu/about/artificial-intelligence-ai-coined-dartmouth")
    edit_run(s[7], "britannica.com/topic/Deep-Blue",
           "https://www.ibm.com/history/deep-blue")
    edit_run(s[7], "https://openai.com/research", "")  # unverified URL — drop link
    set_notes(s[7],
        "Corrected timeline: expert systems did not emerge in the 1980s — Dendral dates to 1965 "
        "and MYCIN to the early 1970s (Stanford); XCON/R1 (DEC, deployed 1980) is the genuine "
        "1980s example. Instructor aside: Turing proposed the imitation game *instead of* "
        "answering 'Can machines think?', which he considered too meaningless to discuss. "
        "Deep Blue enrichment: 200M positions/second on 32 processors; Kasparov won the 1996 "
        "match 4–2 before losing the 1997 rematch 3.5–2.5.\n"
        "Source: Encyclopaedia Britannica — 'expert system', "
        "https://www.britannica.com/technology/expert-system " + V + "; "
        "Dartmouth College — 'Artificial Intelligence (AI) Coined at Dartmouth', "
        "https://home.dartmouth.edu/about/artificial-intelligence-ai-coined-dartmouth " + V + "; "
        "IBM — 'Deep Blue', https://www.ibm.com/history/deep-blue " + V + "; "
        "Google DeepMind — 'AlphaGo', https://deepmind.google/research/breakthroughs/alphago/ " + V)

    # --- Slide 13: tax compliance -> real IRS case in the notes ---
    set_notes(s[12],
        "Make the tax-compliance example concrete with a dated, official case: in September "
        "2023 the IRS announced AI and improved technology to detect tax cheating and improve "
        "case selection — ML built by data scientists working with tax-enforcement experts "
        "selected 75 of the largest U.S. partnerships (averaging $10B+ in assets each) for "
        "examination, and about 500 compliance letters went to partnerships with $10M+ assets "
        "and balance-sheet discrepancies. This is supervised classification/ranking in "
        "production — flag it for reuse in the decision-tree section. The next slide (Treasury "
        "FY2024) gives the fraud-detection numbers.\n"
        "Source: IRS — IR-2023-166 (Sept. 2023), "
        "https://www.irs.gov/newsroom/irs-announces-sweeping-effort-to-restore-fairness-to-tax-system-with-inflation-reduction-act-funding-new-compliance-efforts " + V)

    # --- Slide 16: FedRAMP terminology in the tools survey ---
    edit_run(s[15], "FedRAMP-compliant", "FedRAMP Certified cloud platforms")
    append_notes(s[15],
        "Terminology update (a3): as of mid-2026 the program uses 'FedRAMP Certified' (the "
        "FedRAMP 20x overhaul replaced the legacy 'Authorized' process).\n"
        "Source: GSA FedRAMP PMO — https://www.fedramp.gov/ " + V)

    # --- Slide 17: unsourced agency/framework claims -> capability statements ---
    edit_para(s[16], "NASA leverages TensorFlow",
              "TensorFlow scales from research prototypes to production predictive models")
    edit_para(s[16], "NIH applies PyTorch",
              "PyTorch is the framework of choice for fast-moving research, including medical imaging")
    append_notes(s[16],
        "Sourcing note (a3): the previous NASA/NIH adoption claims had no authoritative source "
        "and were replaced with verifiable capability statements. If you want agency examples, "
        "source them individually before printing.")

    # --- Slide 18: FedRAMP Certified / 20x ---
    P.retitle(prs, 17, "FedRAMP Certified Cloud Platforms for AI Solutions")
    edit_run(s[17], "faster deployment using pre-authorized platforms",
             ":\xa0faster deployment using FedRAMP Certified platforms")
    edit_para(s[17], "Examples of FedRAMP-compliant platforms",
              "Examples of platforms offering FedRAMP Certified services")
    set_notes(s[17],
        "Currency update (as of mid-2026): the program now certifies services — say 'FedRAMP "
        "Certified', not 'compliant' or 'pre-authorized'. The FedRAMP 20x overhaul replaced the "
        "legacy authorization path; per-service status changes, so check the live Marketplace "
        "(marketplace.fedramp.gov) rather than stating it generically.\n"
        "Source: GSA FedRAMP PMO — https://www.fedramp.gov/ " + V)

    # --- Slide 19: FedRAMP Certified / 20x + unsourced adoption claims ---
    P.retitle(prs, 18, "FedRAMP Certified Platforms: Major Providers")
    edit_run(s[18], "FedRAMP compliance ensures robust safeguards",
             ": FedRAMP Certified status signals robust safeguards for sensitive data")
    edit_para(s[18], "Examples of adoption", "Verify before you buy (as of mid-2026)")
    edit_para(s[18], "DoD utilizes AWS GovCloud",
              "531 FedRAMP Certified services, plus 28 via the new FedRAMP 20x path")
    edit_para(s[18], "VA relies on Azure",
              "Confirm any service's current status on the FedRAMP Marketplace")
    append_notes(s[18],
        "Correction (a3): the DoD/AWS GovCloud and VA/Azure adoption claims were unsourced and "
        "were replaced with the certified-service counts and a verify-on-the-Marketplace habit. "
        "The 531 + 28 figures are as of mid-2026 and will drift — re-check before each class.\n"
        "Source: GSA FedRAMP PMO — https://www.fedramp.gov/ " + V)

    # --- Slide 20: Watson Health stale -> overhype cautionary tale ---
    edit_run(s[19], "used for health analytics (e.g., HHS)",
             " Health: sold in 2022 after years of overpromise — the cautionary tale of AI overhype")
    edit_para(s[19], "DHS leverages Palantir",
              "Watson Health lesson: demand evidence of outcomes before adopting vendor AI")
    edit_para(s[19], "Tableau aids agencies",
              "Agencies use visualization tools such as Tableau for public data dashboards")
    set_notes(s[20 - 1],
        "Watson Health is the canonical AI-overhype lesson: heavily marketed, clinically "
        "overpromised, and sold by IBM to Francisco Partners in January 2022 (the assets became "
        "Merative; IBM kept the broader Watson brand). Teaching point for government buyers: "
        "evaluate vendor AI on demonstrated outcomes, not brand reputation. The DHS/Palantir "
        "and Tableau/CDC adoption claims had no authoritative source and were softened.\n"
        "Source: IBM Newsroom — 'Francisco Partners to Acquire IBM's Healthcare Data and "
        "Analytics Assets' (Jan. 2022), "
        "https://newsroom.ibm.com/2022-01-21-Francisco-Partners-to-Acquire-IBMs-Healthcare-Data-and-Analytics-Assets " + V)

    # --- Slide 27: semi-supervised note — one recipe is not the definition ---
    set_notes(s[26],
        "Supervised learning model can predict how long your commute will be based on the time "
        "of day, weather conditions and so on. But first, you'll have to train it to know that "
        "rainy weather extends the driving time.\n\n"
        "The disadvantage of supervised learning is that the dataset has to be hand-labeled — a "
        "costly process at volume. Semi-supervised learning addresses this broadly: train with "
        "a small amount of labeled data plus a large amount of unlabeled data. Note that "
        "'cluster similar data, then propagate the labels' is just one pseudo-labeling recipe, "
        "not the definition — present it as an example, not the meaning of the term.\n"
        "Source: IBM Think — 'What Is Supervised Learning?', "
        "https://www.ibm.com/think/topics/supervised-learning " + V)

    # --- Slide 36: drop unverifiable '90%' figure ---
    edit_para(s[35], "90% of government-held data is unstructured text",
              "Data growth: the large majority of government information is unstructured text")
    append_notes(s[35],
        "Correction (a3): the '90% of government-held data is unstructured text' figure had no "
        "authoritative source (unverifiable in two research passes) and was replaced with a "
        "qualitative claim. Do not quote a percentage in class unless you can cite it.")

    # --- Slide 41: 'United States' is a LOCATION, not an Organization ---
    edit_para(s[40], "Organization: United States", "Location: United States")
    set_notes(s[40],
        "Correction (a3): the example output mislabeled 'United States' as an Organization; "
        "NER systems — including the Google Natural Language API used in the next slide's demo — "
        "type it as LOCATION. Good classroom moment: run the same sentence through the demo and "
        "let students see the API's entity types live.\n"
        "Source: Google Cloud — 'Natural Language API basics', "
        "https://cloud.google.com/natural-language/docs/basics " + V)

    # --- Slide 48: anchor evaluation point to NIST AI RMF ---
    set_notes(s[47],
        "Anchor 'fairness, security, and explainability' to the NIST AI Risk Management "
        "Framework (AI RMF 1.0, Jan. 2023; Generative AI Profile, July 2024) — the voluntary "
        "Govern / Map / Measure / Manage framework is the authoritative U.S. government "
        "reference for what responsible AI evaluation means in practice. As of mid-2026, "
        "AI RMF 1.0 is under revision and NIST has issued a critical-infrastructure profile "
        "concept note (April 2026). Keep 'data preparation is usually the largest phase' "
        "qualitative — the '80% of project time' figure circulating with CRISP-DM is a rule of "
        "thumb, not a measurement.\n"
        "Source: NIST — 'AI Risk Management Framework', "
        "https://www.nist.gov/itl/ai-risk-management-framework " + V + "; "
        "Data Science Process Alliance — 'CRISP-DM', https://www.datascience-pm.com/crisp-dm-2/ " + V)

    # --- Slide 11: point the 'compelling statistic' note at the Treasury slide ---
    append_notes(s[10],
        "For the compelling statistic, use the Treasury case-study slide later in this section: "
        "$4B+ in fraud and improper payments prevented or recovered in FY2024, against a GAO "
        "estimate of $233B–$521B in annual federal fraud losses.")


# ---------------------------------------------------------------- build
def main():
    prs = P.open_deck(DECK)
    # must run before ANY access of prs.slides (the .slides lazyproperty
    # renumbers slide parts and would compact the name space first)
    n_orphans = move_orphan_slide_parts(prs)
    print(f"orphan slide parts moved out of the way: {n_orphans}")
    assert len(list(prs.slides)) == 48, "expected the original 48-slide deck"
    apply_edits(prs)
    for title, bullets, notes in NEW:
        P.append_content(prs, title, bullets, notes)
    # full permutation: Treasury case after 13; adoption after 15; random forests
    # after 32; VA case after 38; CRISP-DM block (47,48 + worked pass) before the
    # Summary/objectives close (45,46).
    order = (list(range(0, 13)) + [48] + [13, 14] + [49]
             + list(range(15, 32)) + [50]
             + list(range(32, 38)) + [51]
             + list(range(38, 44)) + [46, 47, 52, 44, 45])
    assert len(order) == 53
    P.arrange(prs, order)
    P.save(prs, DECK)
    print(f"saved {DECK.name}: {len(list(P.open_deck(DECK).slides))} slides")


if __name__ == "__main__":
    main()
