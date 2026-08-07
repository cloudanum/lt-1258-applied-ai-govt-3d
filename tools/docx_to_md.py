"""Convert an LT authoring .docx into the markdown the validators read.

`validate_registry.py` reads the workbook, handout and IG as markdown, but the
FTP check-in package ships .docx only ("No `.md` files in this package" —
1258a4 Author Input/README.md). This bridges the two without adding a pandoc or
python-docx dependency to the course image.

Style map (the styles these documents actually use):

    Title           -> # heading
    Subtitle        -> *italic line*
    Heading1        -> ## heading
    Heading2        -> ### heading
    FirstParagraph  -> paragraph
    BodyText        -> paragraph
    Compact         -> list item; ordered when its numbering is decimal,
                       bullet otherwise. ilvl=1 nests (that is where the
                       workbook's checkpoints live).

Run:  python tools/docx_to_md.py IN.docx OUT.md
"""
import html
import re
import sys
import zipfile
from pathlib import Path

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def numbering_formats(z):
    """{numId: numFmt} — 'decimal' for numbered steps, 'bullet' for bullets."""
    try:
        nx = z.read("word/numbering.xml").decode("utf-8", "replace")
    except KeyError:
        return {}
    fmts = {}
    for num_id, abs_id in re.findall(
        r'<w:num w:numId="(\d+)"[^>]*>\s*<w:abstractNumId w:val="(\d+)"', nx
    ):
        m = re.search(
            r'<w:abstractNum w:abstractNumId="%s".*?<w:numFmt w:val="([^"]+)"' % abs_id,
            nx,
            re.S,
        )
        fmts[num_id] = m.group(1) if m else "bullet"
    return fmts


def run_text(run):
    """Text of one <w:r>, carrying bold/italic across as markdown."""
    body = "".join(
        html.unescape(t) for t in re.findall(r"<w:t[^>]*>(.*?)</w:t>", run, re.S)
    )
    body = re.sub(r"<[^>]+>", "", body)
    if not body.strip():
        return body
    props = run[: run.find(">")] if "<w:rPr" not in run else run[: run.find("</w:rPr>")]
    bold = "<w:b/>" in props or '<w:b w:val="1"' in props
    ital = "<w:i/>" in props or '<w:i w:val="1"' in props
    lead = len(body) - len(body.lstrip())
    trail = len(body) - len(body.rstrip())
    core = body.strip()
    if bold:
        core = f"**{core}**"
    if ital:
        core = f"*{core}*"
    return body[:lead] + core + body[len(body) - trail:] if trail else body[:lead] + core


def para_text(p):
    p = re.sub(r"<w:tab[^>]*/>", "\t", p)
    p = re.sub(r"<w:br[^>]*/>", "\n", p)
    out = "".join(run_text(r) for r in re.findall(r"<w:r\b.*?</w:r>", p, re.S))
    if not out:
        out = html.unescape(re.sub(r"<[^>]+>", "", p))
    return re.sub(r"[ \t]+", " ", out).strip()


def convert(docx_path, md_path):
    z = zipfile.ZipFile(docx_path)
    xml = z.read("word/document.xml").decode("utf-8", "replace")
    fmts = numbering_formats(z)

    lines, ordinal, last_num = [], 0, None

    def blank():
        if lines and lines[-1] != "":
            lines.append("")

    for p in re.findall(r"<w:p\b.*?</w:p>|<w:p\b[^>]*/>", xml, re.S):
        style_m = re.search(r'<w:pStyle w:val="([^"]+)"', p)
        style = style_m.group(1) if style_m else ""
        num_m = re.search(r'<w:numId w:val="(\d+)"', p)
        ilvl_m = re.search(r'<w:ilvl w:val="(\d+)"', p)
        num_id = num_m.group(1) if num_m else None
        ilvl = int(ilvl_m.group(1)) if ilvl_m else 0
        text = para_text(p)

        if not text:
            continue

        if style == "Title":
            blank(); lines += [f"# {text}", ""]
        elif style == "Subtitle":
            lines += [f"*{text}*", ""]
        elif style == "Heading1":
            blank(); lines += [f"## {text}", ""]
            ordinal, last_num = 0, None
        elif style == "Heading2":
            blank(); lines += [f"### {text}", ""]
            ordinal, last_num = 0, None
        elif num_id is not None:
            if fmts.get(num_id) == "decimal" and ilvl == 0:
                # Only a *different decimal* list restarts the count. Nested
                # checkpoint bullets carry their own numIds and must not reset
                # the step numbering they hang off.
                if num_id != last_num:
                    ordinal = 0
                ordinal += 1
                last_num = num_id
                lines.append(f"{ordinal}. {text}")
            else:
                lines.append(f"{'    ' * ilvl}- {text}")
        else:
            blank(); lines += [text, ""]
            ordinal, last_num = 0, None

    md = "\n".join(lines).rstrip() + "\n"
    md = re.sub(r"\n{3,}", "\n\n", md)
    Path(md_path).write_text(md, encoding="utf-8")
    return md


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, dst = sys.argv[1], sys.argv[2]
    out = convert(src, dst)
    print(f"[OK] {src}\n  -> {dst}  ({len(out.splitlines())} lines, {len(out)} bytes)")
