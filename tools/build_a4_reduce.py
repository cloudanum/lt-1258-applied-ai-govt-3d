"""a4 pass 2 — reduce five over-long chapters to a teachable pace.

a3 enrichment brought every chapter into a 50-60 band, which put the core at
533 slides ~= 178/day. That is above the ~170/day that produced the July 2026
evaluations this revision exists to fix, and above the ~125/day the Revision
Plan commits to. This pass takes the core to 446 (~149/day).

The rule is the plan's own: MERGE and DEMOTE, never silently delete.
  - Every dropped slide's substance is either folded into a surviving slide as a
    bullet, or moved to the workbook, and the surviving slide's notes say so.
  - Chapters that are at or under their plan target (Ch03, Ch05, Ch07) are not
    touched. Ch05 is the protected security content.

Run:  python tools/build_a4_reduce.py
"""
import a4_common as A
import pptx_tools as P

MERGE_TAG = "Merged in a4: "


def _reduce(name, keep_1based, merges, expect, label):
    """merges: {surviving_1based: (bullets_to_add, note_text)} applied BEFORE arrange."""
    path = A.deck(name)
    prs = P.open_deck(path)
    A.clean_orphan_slides(prs)
    P.save(prs, path)
    prs = P.open_deck(path)
    s = list(prs.slides)

    for idx, (bullets, note) in merges.items():
        for b in bullets:
            A.add_bullet(s[idx - 1], b)
        if note:
            A.append_notes(s[idx - 1], MERGE_TAG + note)

    P.arrange(prs, [i - 1 for i in keep_1based])
    P.save(prs, path)
    n = A.verify(path, expect)
    print(f"  {label}: {n} slides")
    return n


# ---------------------------------------------------------------- Ch00 50 -> 25
def ch00():
    keep = [1, 2, 3, 4, 5, 8, 12, 14, 16, 18, 19, 20, 21, 22, 23,
            24, 25, 28, 31, 33, 36, 38, 42, 49, 50]
    merges = {
        5: (["It will not make you a data scientist or ML engineer, train models from scratch, "
             "or replace your agency's own AI acceptable-use training"],
            "old s6 'What This Course Won't Do' folded in as the second half of the "
            "expectations contract; old s7 'How to Get the Most Out' [flex] dropped — the advice "
            "repeats implicitly all week."),
        8: (["Generative-AI use cases rose about ninefold in the same period: 32 (2023) to 282 (2024)"],
            "old s9 'Ninefold Growth' folded in — one GAO numbers slide, not two. Old s10/s11 "
            "'Federal AI Wins' dropped here because Ch09 s9 delivers the same quantified wins at "
            "the point learners can act on them; old s13 'Support Ecosystem' [flex] dropped — "
            "Ch09 carries the same links on its resource slides."),
        16: (["Appendices A-D: ML Life Cycle - Security Deep Dive - Transformer Internals - Classic ML"],
             "old s17 (appendix TOC) folded in."),
        24: (["Firefox opens JupyterLab automatically; if not, double-click 'Start Labs' on the desktop "
              "(if prompted for a password it is: pw)"],
             "old s27 'Starting the Labs' folded in; old s26 'The RDP Button' dropped as a slide — "
             "the warning already appears on this slide's predecessor and in the five-failures slide."),
        28: (["Notebook names match lab numbers (lab_1.2 = Lab 1.2); all data is public or synthetic; "
              "solution notebooks ship on the VM"],
             "old s29 'Notebooks and Data Files' folded in."),
        31: (["The four checks: packages installed - data files readable - class API key works - "
              "data.gov reachable (informational)"],
             "old s30 'What the Four Checks Prove' folded in."),
        36: (["In class use only the assistant your instructor designates; at work use your agency's "
              "approved licensed tool, never a personal account",
              "Public chatbots may store what you paste — a constituent record pasted into one is a "
              "reportable data spill"],
             "old s34 'AI Accounts and Data Rules', s35 'Which AI Account', and s37 'Why the Data Rule "
             "Exists' all folded in. The rule is now stated once, with the account decision and the "
             "rationale attached."),
        38: (["The ladder: Remember - Understand - Apply - Analyze - Evaluate - Create",
              "Day 1 Understand/Apply - Day 2 Apply/Analyze - Day 3 Evaluate/Create (capstone)"],
             "old s15 'Objectives and Bloom's Levels', s39 'Six Levels in Plain Words' [flex] and "
             "s40 'How Each Day Moves You Up' folded in. Sequence is the Anderson & Krathwohl (2001) "
             "revision. Old s41 'How Adults Learn' [flex] dropped."),
        42: (["One idea per sticky note; everyone posts; we review the board after each activity and "
              "return to it on Day 3"],
             "old s43 'Activity Rhythm' and s44 'Whiteboard Norms' folded in. Old s45 'Course Roadmap' "
             "dropped as a duplicate of the Course Map slide; old s46 'Logistics' dropped (instructor "
             "delivers verbally)."),
        50: (["You are done when: notebook list visible, healthcheck open and run, checks 1-3 green"],
             "old s32 'You're Done When You See This' folded in. Old s47/s48 'Key Terms (1 of 2, 2 of 2)' "
             "MOVED TO THE WORKBOOK — Ch09 already shipped an eight-slide A-Z glossary, so the course "
             "now has one glossary, in the workbook, referenced from both chapters."),
    }
    return _reduce("Ch00-Course-Launch", keep, merges, 25, "Ch00 Course Launch (was 50)")


# ---------------------------------------------------------------- Ch09 50 -> 30
def ch09():
    drop = {4, 16, 17, 18, 19, 20, 24, 25, 34, 36, 37, 38, 42, 43, 44, 45, 46, 47, 48, 49}
    keep = [i for i in range(1, 51) if i not in drop]
    merges = {
        23: (["Score the Day-1 prompt and the rewrite against the same rubric — accuracy, "
              "completeness, format, tone",
              "Debrief: what does the delta tell you about which rung moved the needle?"],
             "old s24 'Score Both Against the Rubric' and s25 'Debrief: What the Delta Teaches' "
             "folded into the P10 close."),
        15: ([],
             "old s16-s19 (multimodal, open-weight/on-prem, 2026-by-the-numbers, Gartner) dropped — "
             "all four were [flex] and the three kept trend slides carry the argument. Old s20 "
             "'Any other relevant topic' was an unfilled placeholder and is gone."),
        33: ([],
             "old s34 'Your 90-Day Agency AI Roadmap' dropped — the 30/60/90 template plus the three "
             "phase slides already deliver it."),
        35: (["Analyst: pick one recurring report, ground it in a document set, verify every figure",
              "IT operations: inventory shadow AI, then offer an approved path — see Ch03 and Ch05"],
             "old s36 'Next Steps if You Are an Analyst' and s37 'Next Steps if You Are in IT "
             "Operations' folded into one three-role slide. Old s38 'Final Recap' dropped as a "
             "duplicate of the What-You-Can-Now-Do trio."),
        41: ([],
             "old s42-s49 — the eight-slide A-Z course glossary — MOVED TO THE WORKBOOK "
             "(1258-WBa4-Glossary.md), together with Ch00's 'Key Terms' pair. A glossary is reference "
             "material: it is unreadable projected and invaluable at the desk. Old s4 'Recap of Key "
             "AI Concepts' dropped — superseded by the three What-You-Can-Now-Do slides."),
    }
    return _reduce("Ch09-Summary-Roadmap", keep, merges, 30, "Ch09 Summary & Roadmap (was 50)")


# ---------------------------------------------------------------- Ch06 52 -> 38
def ch06():
    drop = {13, 14, 15, 16, 19, 20, 28, 30, 34, 37, 40, 41, 48, 49}
    keep = [i for i in range(1, 53) if i not in drop]
    merges = {
        11: (["Consistency: same formats, units and codes across systems and over time",
              "Timeliness: current enough for the decision it supports"],
             "old s13 'Consistency' and s14 'Timeliness' folded in."),
        12: (["Validity: values conform to the schema, ranges and code lists",
              "Uniqueness: one real-world entity, one record — no duplicates"],
             "old s15 'Validity' and s16 'Uniqueness' folded in. The plan called for the quality "
             "attributes to land in ~4 slides; six one-per-dimension slides became two."),
        18: (["Then audit the sheet against all six dimensions and compare with the model's audit"],
             "old s19 'Audit the Sheet' and s20 'Which Defects Did the Model Miss' folded into the "
             "walkthrough; the debrief question lives in the IG."),
        27: (["Data Wrangler adds visual feature engineering and a path into SageMaker training"],
             "old s28 (DataBrew gov use cases) and s30 (Data Wrangler gov use cases) dropped; the "
             "plan specifies the tool catalogue collapses to two survey slides."),
        33: ([],
             "old s34 'Storage Choices' [flex] and s37 'ONS Synthetic Data Spectrum' [flex] dropped; "
             "the lake-vs-warehouse comparison also appears in Ch08."),
        39: (["Also: policy research and analysis, and citizen-feedback triage at scale"],
             "old s40 and s41 (gov use cases 2 and 3) folded into one use-case slide."),
        47: (["Organization and people: CDO, data stewards, and a governance body with real authority"],
             "old s48 'Strategy' and s49 'Organization and People' folded into the framework slides."),
    }
    return _reduce("Ch06-Data-for-AI", keep, merges, 38, "Ch06 Data for AI (was 52)")


# ---------------------------------------------------------------- Ch08 52 -> 44
def ch08():
    drop = {6, 12, 15, 21, 28, 29, 39, 50}
    keep = [i for i in range(1, 53) if i not in drop]
    merges = {
        5: ([],
            "old s6 'ML-Pipeline' dropped — s16 'Introduction to ML Pipelines' and s17-s19 cover the "
            "pipeline properly."),
        11: (["Agencies pair FedRAMP-authorized cloud with on-prem/HPC for sensitive workloads"],
             "old s12 (second 'Current Government Implementations') folded in."),
        14: (["Benefits: reproducibility, faster iteration, and auditable model lineage"],
             "old s15 (second 'ML-Ops: Key Features and Benefits') folded in."),
        27: (["Drift detection and retraining triggers: monitor input distributions and outcome "
              "quality, and define the retirement condition before deployment"],
             "old s28 'Drift Deep Dive' [flex] and s29 'Retraining Triggers and Model Retirement' "
             "[flex] folded into the production-monitoring slide. Old s21 'Contextual Bandits' "
             "dropped — a niche example for this audience."),
        49: (["In an assistant: upload the CSV, ask for the profile, the trend, and the chart — "
              "then verify every figure against the source"],
             "old s50 'ChatGPT for Data Analysis' folded in; old s39 'Understanding the Data "
             "Landscape' dropped as a content-free transition."),
    }
    return _reduce("Ch08-Operations-Reporting", keep, merges, 44, "Ch08 Operations & Reporting (was 52)")


# ---------------------------------------------------------------- Ch02 52 -> 46
def ch02():
    drop = {17, 21, 25, 36, 42, 50}
    keep = [i for i in range(1, 53) if i not in drop]
    merges = {
        16: (["Energy and buildings: AI tuning of HVAC and grid load — see the DeepMind cooling result"],
             "old s17 (second 'Smart Infrastructure and Operations') folded in."),
        20: (["AI also triages incoming 911 and emergency reports to route the right resource first"],
             "old s21 (second 'Public Safety and Emergency Response') folded in."),
        24: (["Document processing at scale: extraction, classification, and routing with human review"],
             "old s25 (second 'Process Automation and Workflow Efficiency') folded in."),
        35: (["Public datasets are the raw material for every lab in this course"],
             "old s36 'Introduction to Public Datasets' folded in — the section already opens with "
             "'Public Datasets'."),
        39: ([],
             "old s42 'Data.gov: A Cornerstone of Open Government' folded in here — it repeated this "
             "slide's argument. Old s50 was a stray slide whose only content was a bare URL "
             "(bruceclay.com); removed."),
    }
    return _reduce("Ch02-Applications-Public-Data", keep, merges, 46, "Ch02 Applications & Public Data (was 52)")


if __name__ == "__main__":
    print("a4 pass 2 — reduce to a teachable pace")
    total = ch00() + ch09() + ch06() + ch08() + ch02()
    untouched = {"Ch01-AI-ML-Foundations": 53, "Ch03-Desktop-GenAI": 55,
                 "Ch04-ModernGenAI-PromptEng": 55, "Ch05-Security-Risks-Responsible-AI": 58,
                 "Ch07-Building-with-LLMs": 56}
    for k, v in untouched.items():
        A.verify(A.deck(k), v)
        total += v
    print(f"\ncore total: {total} slides  (~{total/3:.0f}/day across 3 days)")
