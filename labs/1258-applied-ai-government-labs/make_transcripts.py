"""Extract expected-output transcripts from executed solution notebooks.

Run after build_notebooks.sh has executed the solution notebooks in place.
For each solutions/<name>_solutions.ipynb passed on the command line (as
<name>), write solutions/transcripts/<name>_expected_output.txt containing
the text of every stream/execute_result output, in cell order.
"""

import json
import sys
from pathlib import Path

SOL = Path(__file__).resolve().parent / "solutions"
OUT = SOL / "transcripts"


def transcript(nb_path: Path) -> str:
    nb = json.loads(nb_path.read_text())
    name = nb_path.stem.replace("_solutions", "")
    lines = [
        f"EXPECTED OUTPUT — {name} (SOLUTION)",
        'Captured by an offline run (OPENAI_API_KEY=""), so model cells show',
        "the canned fallbacks; live runs will differ in wording, not in the",
        "verified numbers. Use as the read-along fallback if the API is down.",
        "",
    ]
    for cell in nb["cells"]:
        if cell["cell_type"] != "code":
            continue
        for o in cell.get("outputs", []):
            if o["output_type"] == "stream":
                lines.append("".join(o["text"]).rstrip())
            elif o["output_type"] in ("execute_result", "display_data"):
                txt = o.get("data", {}).get("text/plain")
                if txt:
                    lines.append("".join(txt).rstrip())
    return "\n".join(lines) + "\n"


def main(names):
    OUT.mkdir(exist_ok=True)
    for name in names:
        nb_path = SOL / f"{name}_solutions.ipynb"
        if not nb_path.is_file():
            print(f"  SKIP {name} (no solutions notebook)")
            continue
        out_path = OUT / f"{name}_expected_output.txt"
        out_path.write_text(transcript(nb_path))
        print(f"  {out_path.name}")


if __name__ == "__main__":
    main(sys.argv[1:])
