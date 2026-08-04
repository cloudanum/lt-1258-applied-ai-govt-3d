"""Build new Ch04 and Ch07 by splitting old Ch06 and interleaving new slides.

Plan tokens: ("K", old_1based_index) keep a source slide; ("N", i) insert new slide
i from the chapter's content module. The driver keeps the source slides, appends
all new slides, then reorders to the exact plan sequence.
"""
import sys
from pathlib import Path
import pptx_tools as P
import content_ch04, content_ch07

SRC = Path("/Users/iahmad/Creator/Courses_and_conferences/LT/1258/1258-Chap/1258-Ch06.pptx")
OUT = Path("/Users/iahmad/Creator/Courses_and_conferences/LT/1258/1258a4-author-input/decks")


def _assert_no_dupes(path):
    import zipfile
    names = zipfile.ZipFile(path).namelist()
    dupes = {n for n in names if names.count(n) > 1}
    assert not dupes, f"duplicate partnames in {path}: {dupes}"


def build(src, plan, new_slides, out_path, title_text):
    """append-before-delete: open the full source, append every new slide (unique
    partnames guaranteed while all originals are present), then ARRANGE to the
    exact plan order (which also drops the unreferenced originals)."""
    prs = P.open_deck(src)
    n_orig = len(list(prs.slides._sldIdLst))
    # append new slides in the order they first appear in the plan
    new_refs = [ref for tag, ref in plan if tag == "N"]
    new_pos = {}
    for k, ref in enumerate(new_refs):
        t, b, n = new_slides[ref]
        P.append_content(prs, t, b, n)
        new_pos[ref] = n_orig + k
    # final order as current 0-based positions
    order = []
    for tag, ref in plan:
        order.append((ref - 1) if tag == "K" else new_pos[ref])
    P.arrange(prs, order)
    P.retitle(prs, 0, title_text)
    P.save(prs, out_path)
    _assert_no_dupes(out_path)
    return len(order)


# ---- Ch04: Modern GenAI & Prompt Engineering ----
# New-slide indices in content_ch04.NEW_SLIDES:
#  0-4 = 4.2 model landscape ; 5-8 = 4.4 reasoning ; 9-13 = 4.6 role/format ;
#  14-16 = 4.8 eval ; 17 = Lab 4.1 launcher
CH04_PLAN = (
    [("K", 1)] +                                   # title (retitled)
    [("K", 3), ("K", 4), ("K", 5)] +               # 4.1 refresher
    [("N", i) for i in range(0, 5)] +              # 4.2 model landscape
    [("K", i) for i in [7,8,9,10,11,12,13,14,15,16,17,19,21]] +   # 4.3 core prompt
    [("K", 22), ("K", 23), ("K", 24)] +            # 4.4 CoT (historical)
    [("N", i) for i in range(5, 9)] +              # 4.4 reasoning models
    [("K", i) for i in [25,26,27,28,29,30]] +      # 4.5 advanced
    [("N", i) for i in range(9, 14)] +             # 4.6 role/format/structured
    [("K", 31), ("K", 33), ("K", 34), ("K", 35)] + # 4.7 templates
    [("K", 83), ("K", 84)] +                       # 4.8 bias/hallucination (kept)
    [("N", 14), ("N", 15), ("N", 16)] +            # 4.8 evaluation (new)
    [("N", 17)] +                                  # Lab 4.1 launcher
    [("K", 86)]                                    # summary
)

# ---- Ch07: Building with LLMs: APIs, RAG & Agents ----
# content_ch07.NEW_SLIDES indices:
# 0=timeline; 1-9=7.2 APIs(+launcher); 10-13=7.3 frameworks/MCP;
# 14-21=7.4 RAG(+launcher); 22-36=7.5 agents(+launcher); 37-41=7.6 fine-tune;
# 42-43=7.7 HF + summary
CH07_PLAN = (
    [("K", 1)] +                                   # title (retitled)
    [("N", 0)] +                                   # 7.1 timeline
    [("K", 37), ("K", 49)] +                       # 7.1 kept GPT/BERT + future (bridge)
    [("N", i) for i in range(1, 10)] +             # 7.2 APIs + Lab 7.1 launcher
    [("K", 51)] +                                  # LLM app architecture (kept)
    [("N", i) for i in range(10, 14)] +            # 7.3 frameworks + MCP
    [("K", 69), ("K", 70), ("K", 71)] +            # 7.4 RAG on-ramp (kept)
    [("N", i) for i in range(14, 22)] +            # 7.4 RAG technical + Lab 7.2 launcher
    [("N", i) for i in range(22, 37)] +            # 7.5 agents + Lab 7.3 launcher
    [("N", i) for i in range(37, 42)] +            # 7.6 fine-tuning
    [("N", 42), ("N", 43)]                         # 7.7 HF + summary
)

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    n4 = build(SRC, CH04_PLAN, content_ch04.NEW_SLIDES,
               OUT / "1258-Ch04-ModernGenAI-PromptEng.pptx",
               "Modern GenAI and Prompt Engineering")
    print(f"Ch04 built: {n4} slides")
    n7 = build(SRC, CH07_PLAN, content_ch07.NEW_SLIDES,
               OUT / "1258-Ch07-Building-with-LLMs.pptx",
               "Building with LLMs: APIs, RAG, and Agents")
    print(f"Ch07 built: {n7} slides")
