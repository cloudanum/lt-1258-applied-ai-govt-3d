"""Restore the 50-60 slide band for Ch00 (Course Launch), rev a4.

The a4 reduction halved Ch00 (50 -> 25/27) by collapsing the data-rule block,
Bloom's taxonomy block, whiteboard/Mural block and other launch content. This
script ports the dropped CONTENT slides back from the enriched a3 deck
(`1258a3-author-input/decks/_bak2/`), keeping the a4 deck's own activity slides
("Activities in This Chapter", "Lab 0.1") in place.

Idempotent: reads the pristine a4 deck from `decks/_bak2/` and the source deck
from the a3 package, writes `decks/1258-Ch00-Course-Launch.pptx`.

Run:  .venv-courseware/bin/python tools/build_restore_band_ch00.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import pptx_tools as T

DEST_BAK = ROOT / "decks" / "_bak2" / "1258-Ch00-Course-Launch.pptx"
SRC = (ROOT.parent / "1258a3-author-input" / "decks" / "_bak2"
       / "1258-Ch00-Course-Launch.pptx")
OUT = ROOT / "decks" / "1258-Ch00-Course-Launch.pptx"

# Final order as (deck, 1-based slide) tokens: "a4" = pristine a4 deck,
# "src" = enriched a3 _bak2 deck. Activity-format slides in src (DONOW
# launchers etc.) are deliberately NOT ported — a4 has its own.
PLAN = [
    ("a4", 1),   # Introduction and Overview
    ("a4", 2),   # Course Launch: Objectives
    ("a4", 3),   # Activities in This Chapter          [a4 activity roster]
    ("a4", 4),   # Welcome: Who This Course Is For
    ("a4", 5),   # Introductions: Who's in the Room
    ("a4", 6),   # What This Course Will Do
    ("src", 6),  # What This Course Won't Do
    ("src", 7),  # How to Get the Most Out of These Three Days
    ("a4", 7),   # AI in Government Today: The Numbers
    ("src", 9),  # Generative AI in Government: Ninefold Growth
    ("src", 10), # Federal AI Wins with Numbers: Mission
    ("src", 11), # Federal AI Wins with Numbers: Operations
    ("a4", 8),   # Your Policy Landscape: OMB M-25-21 in One Slide
    ("src", 13), # You Are Not Alone: The Federal AI Support Ecosystem
    ("a4", 9),   # Course Objectives
    ("src", 15), # Course Objectives and Bloom's Levels
    ("a4", 10),  # Course Contents
    ("src", 17), # Course Contents (second layout)
    ("a4", 11),  # Course Conventions: DO NOWs, Exercises, Labs, and Flex
    ("a4", 12),  # Course Map: Three Days at a Glance
    ("a4", 13),  # The Prompting Spine: P0 to P10
    ("a4", 14),  # Your Prompt Card: The Take-Home Artifact
    ("a4", 15),  # Your Lab Environment: CloudShare
    ("a4", 16),  # DO NOW 0.1: The Next 15 Minutes
    ("a4", 17),  # Getting In
    ("a4", 18),  # While Your VM Boots: Your First Prompt (P0)
    ("src", 26), # The RDP Button — Do Not Use
    ("src", 27), # Starting the Labs
    ("a4", 19),  # Lab Environment Tour: JupyterLab
    ("src", 29), # Lab Environment Tour: Notebooks and Data Files
    ("src", 30), # Healthcheck: What the Four Checks Prove
    ("a4", 20),  # DO NOW: Run the Healthcheck
    ("src", 32), # You're Done When You See This
    ("a4", 21),  # If Something Goes Wrong: The Five Common Failures
    ("src", 34), # AI Accounts and Data Rules This Week
    ("src", 35), # Which AI Account Should You Use?
    ("a4", 22),  # The Data Rule, Up Front
    ("src", 37), # Why the Data Rule Exists
    ("a4", 23),  # How We Learn: Bloom's Taxonomy
    ("src", 39), # The Six Levels in Plain Words
    ("src", 40), # How Each Day Moves You Up the Ladder
    ("src", 41), # Why This Course Is Hands-On: How Adults Learn
    ("a4", 24),  # Working Together: The Class Whiteboard
    ("src", 43), # The Activity Rhythm: Learn, Do, Debrief
    ("src", 44), # Whiteboard Norms: Getting Value from Mural
    ("src", 45), # Course Roadmap
    ("src", 46), # Logistics for the Week
    ("src", 47), # Key Terms for the Week (1 of 2)
    ("src", 48), # Key Terms for the Week (2 of 2)
    ("a4", 25),  # Chapter Summary: Course Launch
    ("a4", 26),  # Lab 0.1: Course Environment and Data Tour  [a4 lab launcher]
    ("a4", 27),  # Checkpoint: What You Should Have Right Now
]

EXPECT_A4 = {
    1: "Introduction and Overview", 2: "Course Launch: Objectives",
    3: "Activities in This Chapter", 6: "What This Course Will Do",
    7: "AI in Government Today", 9: "Course Objectives",
    12: "Course Map: Three Days", 13: "The Prompting Spine",
    16: "DO NOW 0.1", 20: "DO NOW: Run the Healthcheck",
    22: "The Data Rule, Up Front", 23: "How We Learn: Bloom",
    25: "Chapter Summary", 26: "Lab 0.1", 27: "Checkpoint",
}
EXPECT_SRC = {
    6: "What This Course Won't Do", 7: "How to Get the Most Out",
    9: "Generative AI in Government: Ninefold",
    10: "Federal AI Wins with Numbers: Mission",
    11: "Federal AI Wins with Numbers: Operations",
    13: "You Are Not Alone", 15: "Course Objectives and Bloom's Levels",
    17: "Course Contents", 26: "The RDP Button", 27: "Starting the Labs",
    29: "Lab Environment Tour: Notebooks",
    30: "Healthcheck: What the Four Checks",
    32: "You're Done When You See This",
    34: "AI Accounts and Data Rules", 35: "Which AI Account Should You Use",
    37: "Why the Data Rule Exists", 39: "The Six Levels in Plain Words",
    40: "How Each Day Moves You Up", 41: "Why This Course Is Hands-On",
    43: "The Activity Rhythm", 44: "Whiteboard Norms", 45: "Course Roadmap",
    46: "Logistics for the Week", 47: "Key Terms for the Week (1",
    48: "Key Terms for the Week (2",
}


def titles(path):
    return [t for _, t, _ in T.inventory(str(path))]


def main():
    a4_t = titles(DEST_BAK)
    src_t = titles(SRC)
    for idx, frag in EXPECT_A4.items():
        assert frag in a4_t[idx - 1], f"a4 slide {idx}: expected {frag!r}, got {a4_t[idx-1]!r}"
    for idx, frag in EXPECT_SRC.items():
        assert frag in src_t[idx - 1], f"src slide {idx}: expected {frag!r}, got {src_t[idx-1]!r}"

    dst = T.open_deck(str(DEST_BAK))
    src = T.open_deck(str(SRC))
    src_slides = list(src.slides)
    order, clone_pos = [], {}
    for kind, idx in PLAN:
        if kind == "a4":
            order.append(idx - 1)
        else:
            if idx not in clone_pos:
                T.clone_slide(dst, src_slides[idx - 1])
                clone_pos[idx] = len(dst.slides._sldIdLst) - 1
            order.append(clone_pos[idx])
    T.arrange(dst, order)
    T.save(dst, str(OUT))
    print(f"Ch00 restored: {len(PLAN)} slides "
          f"({sum(1 for k, _ in PLAN if k == 'a4')} kept + "
          f"{sum(1 for k, _ in PLAN if k == 'src')} ported) -> {OUT}")


if __name__ == "__main__":
    main()
