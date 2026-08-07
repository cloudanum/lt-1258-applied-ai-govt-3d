# Course 1258 (rev a4) — Workbook: New and Rewritten Lab Pages

*Addendum to merge into 1258-WBa4. Author input; Pubs applies template.*

## How to Use This Addendum

These are the new and rewritten lab pages for the a3 revision. Merge them into the master workbook at the positions shown, and renumber the carried-forward labs per the Lab Registry (registry/labs.yaml). Every lab here follows the standard template: Objectives → Setup → Steps (with ✓ checkpoints) → Deliverable → Reflection → Debrief → Troubleshooting. The lab id, the notebook filename, the slide callout, and the handout section must all match (no-drift rule).

Labs whose content did not change (1.1, 1.2, 1.3, 1.4, 2.1, 5.1–5.4, 8.1–8.3, A.1, B.1) are carried forward from a2 and only renumbered; they are not reprinted here. The rename map is in labs/README.md.

## DO NOW 0.1 — Environment Healthcheck

Where: Day 1, before Chapter 1. Time: 15 minutes. Environment: CloudShare VM.

### Objectives

- Reach a running JupyterLab in your CloudShare VM.
- Confirm your environment is ready for the week’s labs.

### Setup

Your instructor will confirm the class is launched. You reach everything through your browser — there is nothing to install.

### Steps

1. Sign in to your My Learning Tree account and open the course page.
2. Click Launch Lab and wait until the VM shows ready.
3. Click the in-browser Viewer to reach the VM desktop.
    - ✓ You should see the VM desktop with Firefox.
    - Do not click the RDP button — use the in-browser Viewer only.
4. Firefox opens to JupyterLab automatically (bookmark: Course Labs). If it does not, double-click the Start Labs icon on the desktop. If asked for a password, it is pw.
    - ✓ You should see a file list of lab notebooks.
5. Open lab_0.1_healthcheck.ipynb and choose Run → Run All Cells.
    - ✓ Checks 1–3 should read PASS (green). Check 4 is informational.

### Deliverable

A healthcheck notebook showing green PASS on checks 1–3.

### Reflection

- What does each check confirm, and why would each one matter in a real project?

### Debrief (instructor-led)

Instructor confirms the whole room is green before starting Chapter 1. See the Instructor Guide for the five most common failures and their fixes.

### Troubleshooting

- Red on Check 3 (API key): tell your instructor — the class key may need a refresh.
- No file list: double-click Start Labs; if still empty, re-launch the VM.
- RDP error: you clicked the wrong button — return to the in-browser Viewer.

## Lab 3.1 — Desktop GenAI Task Relay

Where: Day 1, Chapter 3. Time: 35 minutes. Environment: Browser + approved AI assistant.

### Objectives

- Experience the four everyday work patterns with a real AI assistant.
- Judge output quality with a simple rubric.
- Apply the public-data-only rule in practice.

### Setup

Use the AI assistant account your instructor designates (your agency’s Copilot, or a class ChatGPT/Gemini/Claude account). Public or synthetic inputs only — never paste real agency or personal data. Open the class whiteboard (Mural).

### Steps — four timed micro-tasks (about 7 minutes each)

1. Summarize. Paste the provided GAO excerpt and ask for a 5-bullet summary for a non-technical manager.
    - ✓ You have a 5-bullet summary you could forward.
2. Diagram. Describe the FOIA intake process (from the Chapter 3 example) and ask the assistant to produce a Mermaid flowchart.
    - ✓ You have Mermaid text that renders as a flowchart.
3. Troubleshoot. Paste the provided broken Python snippet and ask what is wrong and how to fix it.
    - ✓ You can explain the bug in one sentence.
4. Draft. Draft a friendly reply to constituent complaint #1 (see source docs), under 120 words, plain language.
    - ✓ You have a reply you would be comfortable sending after review.

Rubric (score each output 1–3): accurate? · complete? · right format/tone?

### Deliverable

Post your best and worst output to the Mural board with its rubric score.

### Reflection

- Which task did the assistant do best? Worst?
- What in your agency’s acceptable-use policy would limit any of these?

### Debrief (instructor-led)

Compare outputs across tools on the board. Discuss: where tools differed; free vs. paid friction; and the data rule (why every input here was public or synthetic).

### Troubleshooting

- No assistant access in the room: work from the printed Prompt Library and the instructor’s live demo; annotate the captured outputs.

## Lab 4.1 — Prompt Engineering Studio (rewrite of the former Lab 6.1)

Where: Day 2, Chapter 4. Time: 45 minutes. Environment: Browser assistant (API optional for technical cohorts).

### Objectives

- Measurably improve an output by iterating your prompt.
- Apply zero-shot, few-shot, role + format, and reasoning-model techniques.
- Score outputs against a rubric.

### Setup

Approved AI assistant; public/synthetic inputs only. You are provided three real source documents (in your workbook source pack): a dataset description, a policy memo, and a constituent-feedback set.

### Steps — the prompt ladder

1. Zero-shot. Ask the assistant to “summarize the policy memo.” Score it.
    - ✓ You have a baseline output and a rubric score.
2. Few-shot. Give two examples of the summary style you want, then ask again.
    - ✓ You can see how examples changed the output.
3. Role + format contract. “You are a policy analyst. Summarize the memo as a 5-row table: rule | who it affects | effective date | source line.” Score it.
    - ✓ You have a structured, role-shaped output.
4. Reasoning-model comparison. Run the hardest task — classify each constituent complaint by theme and urgency — on a standard model and on a reasoning model. Compare.
    - ✓ You can describe when the reasoning model helped.

Rubric (1–5 each): accuracy · completeness · format adherence · tone.

### Deliverable

One before/after prompt pair with its two rubric scores, and a one-line note on which rung of the ladder bought the most quality.

### Reflection

- Where did the model sound confident but get a fact wrong? How did you catch it?
- When would you stop iterating and switch approach (RAG? a different tool)?

### Debrief (instructor-led)

Collect which technique helped most. Bridge to Chapter 7’s decision matrix: prompting → RAG → fine-tuning → classic ML.

### Troubleshooting

- Output ignores the format: restate the format as the last line of the prompt.
- Model won’t classify consistently: add one worked example (few-shot).

## Exercise 6.1 — Shared-Spreadsheet Data Collection

Where: Day 2, Chapter 6. Time: 20 minutes. Environment: Shared spreadsheet (browser).

### Objectives

- Experience data-quality problems by creating them.
- Connect messy data to the quality attributes from Chapter 6.

### Setup

Your instructor shares a link (and QR code) to a shared sheet with a loose schema, e.g., columns: your role · a beverage you drank this week · when · how much. A prepared “messy” sheet is available if the room is offline.

### Steps

1. Each participant adds three rows. Do not coordinate formats.
    - ✓ The sheet fills with everyone’s entries.
2. The instructor projects the sheet. As a class, audit it against the six quality attributes: completeness, accuracy, consistency, timeliness, validity, uniqueness.
    - ✓ You have found at least five distinct defects.
3. For each defect, name one governance rule (a schema constraint, a controlled vocabulary, a required field) that would have prevented it.

### Deliverable

A top-five defect list with a preventing rule for each.

### Reflection

- Which is worse for AI: missing data or inconsistent data? Why?
- Who in an agency should own data quality for a shared dataset?

### Debrief (instructor-led)

Draw the line from “free-text convenience” to “downstream AI failure.” Optionally reuse the cleaned sheet as input for Lab 7.2/7.3.

## Lab 7.1 — First Calls with the OpenAI API (rewrite of the former Lab 6.3)

Where: Day 3, Chapter 7. Time: 30 minutes. Environment: CloudShare VM, JupyterLab.

### Objectives

- Make working chat calls with the current OpenAI SDK.
- See how the system prompt and temperature change output.
- Get structured JSON from a real memo and estimate cost.

### Setup

Open lab_7.1_openai_api.ipynb. The API key is already provided as an environment variable — there is no key to paste. The model is pinned in one config cell. (This replaces the old lab that asked for a personal key and used a retired model.)

### Steps

1. Run the setup cell — confirm it prints the model name.
    - ✓ “Using model: …” prints.
2. Complete Exercise 2: two calls with different system prompts, same question.
    - ✓ Two answers in different voices, same facts.
3. Complete Exercise 3: the same prompt at temperature 0.0 and 1.0.
    - ✓ You can see focused vs. varied output.
4. Complete Exercise 4: extract subject, effective_date, key_rules from the memo as JSON with response_format={"type":"json_object"}.
    - ✓ json.loads succeeds and the keys are present.
5. Complete Exercise 5: print token usage and estimate the cost of 1,000 calls.
    - ✓ You have a dollar estimate.

### Deliverable

A completed notebook with all five exercises run.

### Reflection

- Which changed the output more — the system prompt or the temperature?
- Why is JSON output more useful in a real system than prose?

### Debrief (instructor-led)

Cost math at agency scale; what changes when this runs on Azure OpenAI (FedRAMP) in production. See the expected-output transcript if the API is unavailable.

### Troubleshooting

- 401/429 errors: tell your instructor (see the IG “API is down” page). You can read along with the solution transcript.

## Lab 7.2 — RAG over Government Documents

Where: Day 3, Chapter 7. Time: 40 minutes. Environment: CloudShare VM, JupyterLab.

### Objectives

- Build a retrieval pipeline over public agency documents.
- Compare a grounded, cited answer to an ungrounded one.

### Setup

Open lab_7.2_rag_gov_docs.ipynb. A small corpus of public agency documents is provided on the VM. Retrieval works even offline (a local embedding fallback); answer generation uses the class model.

### Steps

1. Run the load + chunk cells.
    - ✓ You see “N documents → M chunks.”
2. Run the embed cell.
    - ✓ “embedded M chunks.”
3. Complete retrieve() — embed the question and return the top-k chunks.
    - ✓ The retrieved chunks are about the question.
4. Complete the grounding instruction so the model answers only from the context and cites the source file.
    - ✓ The grounded answer carries [filename] citations.
5. Run the ungrounded comparison.
    - ✓ You can see the difference.

### Deliverable

The grounded vs. ungrounded answers side by side.

### Reflection

- Which answer would you put in front of a constituent?
- What breaks if chunks are too big? Too small?

### Debrief (instructor-led)

When RAG fails; what a FedRAMP production stack looks like (documents, vector store, model).

## Lab 7.3 — Build an AI Agent (Capstone)

Where: Day 3, Chapter 7. Time: 75–90 minutes. Environment: CloudShare VM, JupyterLab.

### Objectives

- Define a tool and trace a single tool call.
- Run an agent loop that chains tools.
- Add guardrails: PII masking, a human-approval gate, and injection defense.

### Setup

Open lab_7.3_agent.ipynb. The tools, mock data, and agent runtime are provided. You author the tool schemas and guardrail wiring in the marked cells.

### Steps

1. Stage A — one tool, one call. Complete the search_datasets schema; run it.
    - ✓ The model calls the tool with a query argument.
2. Stage B — the agent loop. Add the lookup_citizen_record tool; run a task that chains a record lookup with a dataset search.
    - ✓ The printed trace shows the agent calling both tools in order.
3. Stage C — guardrails. Run case C-1005 with mask=True and gate=True.
    - ✓ The SSN is redacted before the model sees it.
    - ✓ The embedded “ignore your rules” instruction is refused.
    - ✓ Nothing is sent until you type y.
4. (Stretch) Stage D — change the system instructions and run the mini-eval.

### Deliverable

An agent transcript that answers “find a dataset about X, compute Y, draft a summary — but ask me before submitting,” with the guardrails visibly working.

### Reflection

- Which guardrail stopped the C-1005 injection — masking, the system prompt, the gate, or all three? How would you prove it?
- When is an agent the wrong tool (a plain prompt or a fixed workflow is safer)?

### Debrief (instructor-led)

Which guardrails your agency would require before an agent touches a real record. Agent vs. workflow vs. prompt. See the expected-output transcript for the guarded run.

### Troubleshooting

- Network blocked / key down: the tools fall back to cached data; read the solution transcript for the agent loop.
