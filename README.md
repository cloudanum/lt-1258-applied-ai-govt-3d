# LT-1258 — Applied AI for Government IT Professionals (3 days)

Hands-on lab code and build tooling for Learning Tree Course 1258, rev a4 —
a three-day applied AI course for government IT professionals. Sixteen
Jupyter labs take the room from an environment healthcheck through data
quality, prompt engineering, security, and on to calling the OpenAI API,
building RAG over government documents, and shipping a guarded
citizen-services triage agent as the capstone.

The labs are written for a **non-programmer audience**: every step is a
single plain-English helper call (`labs/lab_helpers.py` hides the pandas /
scikit-learn / OpenAI SDK machinery), and students only edit simple values —
prompt text, a number, a keyword — in cells marked `# YOUR TURN`. The
original code-forward versions, where participants write the Python
themselves, are preserved in `labs/For_Python_Programmers/` for rooms with
programming experience. Same datasets, same steps, same outputs.

Every lab **executes end-to-end with no API key**: API-backed steps degrade
to labelled canned outputs, so the course survives a dead key, a quota-exhausted
account, or a no-internet classroom.

## Repository structure

```
LT-1258-govt-3-days/
├── labs/                       All student lab code
│   ├── lab_0.1_healthcheck.ipynb        DO NOW 0.1 — Environment Healthcheck
│   ├── lab_0.1_environment_tour.ipynb   Lab 0.1 — Course Environment and Data Tour
│   ├── lab_1.1_ai_inventory.ipynb       Lab 1.1 — Federal AI Use Case Inventory
│   ├── lab_1.2_clustering.ipynb         Lab 1.2 — Clustering Counties by Air Quality (K-Means)
│   ├── lab_2.1_data_expedition.ipynb    Lab 2.1 — Public Data Expedition
│   ├── lab_4.1_prompt_studio.ipynb      Lab 4.1 — Prompt Engineering Studio
│   ├── lab_4.2_prompt_templates.ipynb   Lab 4.2 — Reusable Prompt Template Library
│   ├── lab_5.1_adversarial.ipynb        Lab 5.1 — Adversarial Examples & Robustness
│   ├── lab_5.2_pii.ipynb                Lab 5.2 — Detect and Mask PII in Citizen Records
│   ├── lab_6.1_data_quality.ipynb       Lab 6.1 — Data Quality Assessment (Chicago 311)
│   ├── lab_6.2_genai_cleaning.ipynb     Lab 6.2 — GenAI-Assisted Cleaning
│   ├── lab_7.1_openai_api.ipynb         Lab 7.1 — First Calls with the OpenAI API
│   ├── lab_7.2_rag_gov_docs.ipynb       Lab 7.2 — RAG over Government Documents
│   ├── lab_7.3_agent.ipynb              Lab 7.3 — Build an AI Agent (capstone)
│   ├── lab_8.1_visualization.ipynb      Lab 8.1 — Visualization & Reporting (EPA)
│   ├── lab_8.2_genai_reporting.ipynb    Lab 8.2 — GenAI-Assisted Analysis & Briefing
│   ├── src/                    Jupytext sources (notebooks are generated from these)
│   ├── solutions/              Instructor solution notebooks + expected-output transcripts
│   ├── data/                   Public/synthetic datasets (see MANIFEST.json)
│   ├── lab_helpers.py          Plain-English one-call-per-step functions the student
│   │                           notebooks run (the non-programmer facade over lab_common)
│   ├── lab_common.py           Shared helpers: key/.env loading, chat wrappers, fallbacks
│   ├── For_Python_Programmers/ The original code-forward labs (frozen snapshot) for
│   │                           participants comfortable writing Python
│   └── build_notebooks.sh      Jupytext -> .ipynb + forced-offline smoke test
├── registry/                   activities.yaml / labs.yaml — the canonical activity registry
│                               (id == workbook heading == slide callout == handout section)
├── tools/                      Course build & QA tooling (deck branding, enrichment,
│                             notes injection, timing, validate_registry.py gate)
├── .env.example                API-key template (copy to .env; never commit the real one)
├── start_jupyter_labs.sh       Classroom-VM launcher behind the Desktop icon
├── sync_key.sh                 Copies the class key from /home/student/Keys/keys.txt to .env
└── README.md
```

## Prerequisites

- Python 3.10+ (pandas, matplotlib, scikit-learn, openai, jupyter, jupytext).
  `labs/build_notebooks.sh` finds an interpreter via `$VIRTUAL_ENV`, then
  `./.venv`, then `python3`. To build one:

  ```sh
  uv venv --python 3.12 .venv
  uv pip install --python .venv/bin/python jupyterlab jupytext openai \
      pandas scikit-learn matplotlib pyyaml nbformat nbconvert ipykernel
  .venv/bin/python -m ipykernel install --user --name 1258-a4 \
      --display-name "Python 3.12 (1258 a4)"
  ```
- An OpenAI API key — **optional**. With no key, or `OPENAI_API_KEY=""`,
  every lab runs fully offline on canned fallbacks; a present-but-dead key is
  survived the same way (every call site has a guarded fallback).

## Getting started

```sh
git clone https://github.com/cloudanum/LT-1258-govt-3-days.git
cd LT-1258-govt-3-days/labs
cp ../.env.example .env     # fill in OPENAI_API_KEY (author machine only)
jupyter lab                 # or open the notebooks in VS Code
```

`lab_common.load_dotenv()` searches for `.env` from the labs directory upward,
and `lab_common.load_keys_file()` reads the classroom key file first
(`/home/student/Keys/keys.txt`, override with `$COURSE_KEYS_FILE`). Precedence
is **real environment variable > key file > `.env`** — an `OPENAI_API_KEY`
exported from your shell shadows both files, so unset it if the labs seem to
ignore `.env`. The key is never printed.

On the classroom VM nothing is edited by hand: IT fills in
`/home/student/Keys/keys.txt` and `sync_key.sh` — run by the Desktop launcher
on every start — copies that key into the `OPENAI_API_KEY` line of `.env`,
leaving the model aliases and comments alone. See the VM's
`Desktop/WHERE_TO_PUT_OPENAI_KEY.txt`. After editing sources in `labs/src/`,
rebuild:

```sh
./build_notebooks.sh        # jupytext + offline smoke run + transcripts
```

## Course map

| Day | Labs | Theme |
|---|---|---|
| 1 | 0.1 (x2), 1.1, 1.2, 2.1 | Environment, AI/ML foundations, public data |
| 2 | 4.1, 4.2, 5.1, 5.2, 6.1, 6.2 | Prompt engineering, security & PII, data quality |
| 3 | 7.1, 7.2, 7.3, 8.1, 8.2 | APIs, RAG, the agent capstone, ops & reporting |

(Labs 3.1, Ex 6.1 and 9.1 are browser-based by design — no notebooks. Their
student-facing material ships as assets: `labs/data/lab3.1/` holds the source
pack and printed prompt library for the Desktop GenAI relay, and
`labs/data/ex6.1/` holds the shared-sheet template plus the prepared messy
sheet used when the room is offline.)

## The labs

- **Lab 0.1 (healthcheck + tour)** — verify the VM, datasets, and (optionally)
  the API key before Chapter 1; tour the environment and data pack.
- **Lab 1.1 / 1.2** — explore the federal AI use-case inventory with pandas;
  cluster counties by air quality with K-Means and name the clusters in plain
  English.
- **Lab 2.1** — profile an agency dataset end to end (shape, dtypes, missing
  values, per-column profiler) with a cached data.gov fallback.
- **Lab 4.1 / 4.2** — the four-rung prompt ladder on a government memo
  (zero-shot → few-shot → role + format contract → reasoning-model comparison)
  with rubric scoring; then package the winners as a reusable, versioned
  prompt-template library.
- **Lab 5.1 / 5.2** — adversarial inputs and model robustness (flip-rate
  analysis); detect and mask PII in synthetic citizen records (regex first,
  NLP optional).
- **Lab 6.1 / 6.2** — score a real 311 extract on the six data-quality
  dimensions with a go/no-go call; then clean it with structured GenAI output
  and verify the result.
- **Lab 7.1** — first OpenAI API calls: temperature experiments, JSON
  extraction matching the memo, token-usage cost math.
- **Lab 7.2** — chunk, embed, retrieve, and ground answers over four
  government documents, with a citation-verification step that checks quoted
  sentences against the corpus.
- **Lab 7.3 (capstone)** — a citizen-services triage agent with a tool
  allow-list, step cap, and human-approval gate; includes a poisoned-catalog
  red-team run asserting no SSN ever reaches the outbox.
- **Lab 8.1 / 8.2** — build a one-page EPA briefing (four charts) and a
  GenAI-assisted analysis whose every finding is verified against the data.

## Cross-cutting design

- **Public/synthetic data only** — every dataset in `labs/data/` is public or
  synthetic and documented in `MANIFEST.json`.
- **Workbook correspondence** — numbered, timed steps match the student
  workbook 1:1 (Objectives → Setup → Steps → Deliverable → Reflection →
  Debrief → Troubleshooting); the registry holds the canonical contract.
- **Offline-first** — keyless and dead-key runs degrade to labelled canned
  outputs, so a classroom never blocks on API health.
- **Two audiences, one lab pack** — the root notebooks are the guided,
  low-code versions (one helper call per step, `# YOUR TURN` value edits);
  `labs/For_Python_Programmers/` keeps the code-forward originals. Both run
  the same data through the same steps. `tools/check_friendly.py` guards the
  contract: no scary constructs in student cells and every `# YOUR TURN`
  cell pre-filled with a working value.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `OPENAI_API_KEY not set` note | Expected off the VM — canned outputs are used. To run live, copy `.env.example` to `.env` and add your key. On the VM, check `/home/student/Keys/keys.txt` and run `./sync_key.sh`. |
| Notebook out of date after editing `src/` | Re-run `./build_notebooks.sh`; notebooks are generated artifacts. |
| A dataset file is missing | Re-clone or check `labs/data/MANIFEST.json` for the expected pack. |
| API calls fail with 429/quota errors | The lab keeps working on canned fallbacks; nothing else to do. |

Course 1258 — Applied AI for Government IT Professionals (rev a4).
