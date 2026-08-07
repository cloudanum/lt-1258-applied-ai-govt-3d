# Lab 3.1 — Printed Prompt Library

*Fallback for a room with no assistant access. Work from these prompts and the
instructor's live demo, then annotate the captured outputs against
`rubric_1to3.md`. You still score; you just score someone else's run.*

This file is **not** `labs/my_prompt_library.md` — that one is an artifact you
build in Lab 4.2. This one is printed and handed out.

---

## 1. Summarize

**Source:** `gao_style_excerpt.md`

> Summarize the report excerpt below in exactly 5 bullets for a non-technical
> programme manager who has 30 seconds. No jargon. Lead with what changed, not
> with methodology. If a number is load-bearing, keep it.
>
> ---
> [paste the excerpt]

**Watch for:** bullets that restate the headings instead of the findings; numbers
dropped or invented.

---

## 2. Diagram

**Source:** `foia_intake_ch03.md`

> Turn the process description below into a Mermaid flowchart. Use `flowchart TD`.
> Show the three intake routes converging, the fee-category decision as a branch,
> and the three-way determination outcome. Output only the Mermaid code block.
>
> ---
> [paste the description]

**Watch for:** a straight line with no branches; redaction placed after release;
Mermaid that will not render because the label text contains unescaped brackets.

---

## 3. Troubleshoot

**Source:** `broken_snippet.py`

> The Python below fails. Tell me (a) what is wrong, in one sentence a
> non-programmer would understand, and (b) the fix, with the corrected lines.
> Explain why it fails this way rather than just handing me code.
>
> ---
> [paste the snippet]

**Watch for:** a fix with no explanation; a rewrite of the whole function when
two lines were the problem; missing the second defect once it has found the
first.

---

## 4. Draft

**Source:** `constituent_complaints.md`, complaint #1

> Draft a reply to the constituent message below. Under 120 words. Plain
> language, 8th-grade reading level. Acknowledge the specific thing they raised,
> say what happens next and by when, and do not promise an outcome we cannot
> guarantee. Sign off as the constituent services team.
>
> ---
> [paste complaint #1]

**Watch for:** the form-letter tone the constituent explicitly asked us not to
send; a promised deadline nobody committed to; the specific detail (the
interchange, the inhaler) dropped in favour of generalities.

---

## The data rule, every time

Everything in this lab is public or synthetic. Nothing you paste into a browser
assistant in this room may contain a real constituent's name, address, case
number, or any other identifier. If you are tempted to try it with something from
work, that is exactly the moment the rule exists for.
