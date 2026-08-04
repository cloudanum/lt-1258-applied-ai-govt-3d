"""Repoint the four slides that still cite activity ids retired by the a4
activity redesign (Lab 1.3, Lab 1.4, Lab 5.4, Exercise 6.1)."""
import a4_common as A
import pptx_tools as P

FIXES = [
    ("AppD-Classic-ML-DeepDive", 4,
     "Lab 1.3", "Lab 1.2",
     "Repointed in a4: Lab 1.3 was retired when the activity set was rebuilt. The "
     "clustering work now lives in Lab 1.2 (Ch01), which uses the EPA county file."),
    ("AppD-Classic-ML-DeepDive", 8,
     "Lab 1.4", "Lab 1.1",
     "Repointed in a4: Lab 1.4 (NER) was retired. The equivalent text work is now the "
     "free-text columns of the federal AI inventory in Lab 1.1 (Ch01)."),
    ("Ch05-Security-Risks-Responsible-AI", 48,
     "Lab 5.4", "DO NOW 5.C",
     "Repointed in a4: the scenario-card lab became DO NOW 5.C, the injection red team, "
     "which carries prompting-spine rung P5."),
    ("Ch06-Data-for-AI", 8,
     "Exercise 6.1", "DO NOW 6.B",
     "Repointed in a4: Exercise 6.1 became DO NOW 6.B 'Propose the Schema' (spine rung P6)."),
]


def run():
    for deck, idx, old, new, note in FIXES:
        path = A.deck(deck)
        prs = P.open_deck(path)
        s = list(prs.slides)[idx - 1]
        if A.edit_bullet(s, old, new, all_matches=True):
            A.append_notes(s, note)
            P.save(prs, path)
            print(f"  {deck} s{idx}: {old} -> {new}")
        else:
            print(f"  {deck} s{idx}: MISS ({old!r} not found)")


if __name__ == "__main__":
    print("a4 — repoint retired activity callouts")
    run()
