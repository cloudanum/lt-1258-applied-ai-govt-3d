# Applied AI for Government IT Professionals — Lab Notebooks

Hands-on Jupyter labs for **Learning Tree Course 1258** (rev a4). Twenty
notebooks take IT professionals from an environment healthcheck to
clustering, decision trees, named-entity recognition, prompt engineering,
PII detection, RAG over government documents, and a small agent capstone —
every example grounded in **real US government data** (Chicago 311, EPA air
quality, the federal AI use-case inventory, GAO-style memos) or
clearly-labelled synthetic training records.

**Runs anywhere.** Every notebook reads `OPENAI_API_KEY` from the
environment (never written into a notebook) and every AI call has a
**canned offline fallback**, so the labs execute end-to-end with no key and
no network — proven by the build script's offline smoke test. Instructor
copies with fully-worked solutions live in `solutions/`, with
expected-output transcripts in `solutions/transcripts/` for API-down days
in class.

## Spotlight — the newest labs

| Notebook | What it teaches |
|---|---|
| **`lab_1.3_decisiontree.ipynb`** | **The auditable classifier.** Train a decision tree on real EPA county air-quality data, **draw the tree** and read its rules aloud, then watch an uncapped tree memorize (train 1.00 / test 0.85) on a depth-sweep overfitting curve. Five charts, including the full tree diagram and feature importances. |
| **`lab_1.4_nlp_ner.ipynb`** | **NER on unstructured text.** Extract organizations, people, places, dates, money, and laws from five synthetic agency press releases — via spaCy when installed, or the built-in rule+gazetteer extractor — and render **displaCy-style inline highlighting** plus by-type and per-document charts. Students extend the extractor with a rule of their own. |
| **`lab_3.2_bloom_taxonomy.ipynb`** | **Prompt the Ladder.** Bloom's revised taxonomy mapped onto GenAI tasks: six levels (Remember → Create), each with an explainer (signature verbs, output space, characteristic risk, temperature band) and **three government prompt examples** — 18 prompts in all. Closes by decomposing a Create-level task into a six-stage pipeline. Framework: neurals.ca agent-concepts, Bloom's Taxonomy (Anderson & Krathwohl, 2001). |
| **`lab_4.3_ptcf_bloom.ipynb`** | **The PTCF Upgrade.** The same 18 tasks rebuilt as **Persona · Task · Context · Format** contracts. Students run naive one-line prompts vs their PTCF versions, score both on the course rubric, and diagnose a deliberately misaligned contract. PTCF from *The Art of Agent Prompting* (30 Agents, Ch. 3). |

## Full roster

| Notebook | Lab | Needs key? | Offline behavior |
|---|---|---|---|
| `lab_0.1_healthcheck.ipynb` | DONOW 0.1 | key check only | runs; reports which checks pass |
| `lab_0.1_environment_tour.ipynb` | Lab 0.1 environment & data tour | yes | canned first-call reply |
| `lab_1.1_ai_inventory.ipynb` | Lab 1.1 federal AI use-case inventory | no | fully self-contained (pandas) |
| `lab_1.2_clustering.ipynb` | Lab 1.2 K-Means on EPA county AQI | no | fully self-contained (sklearn) |
| `lab_1.3_decisiontree.ipynb` | Lab 1.3 decision tree — unhealthy-air counties; tree + overfitting graphics | no | fully self-contained (sklearn) |
| `lab_1.4_nlp_ner.ipynb` | Lab 1.4 NER on press releases — inline highlighting + charts | no | rule+gazetteer extractor; uses spaCy if installed |
| `lab_2.1_data_expedition.ipynb` | Lab 2.1 dataset profiling | no | cached data.gov snapshot fallback |
| `lab_3.2_bloom_taxonomy.ipynb` | Lab 3.2 Bloom's ladder — 6 levels × 3 gov examples | yes | canned outputs per level |
| `lab_4.1_prompt_studio.ipynb` | Lab 4.1 seven prompt patterns | yes | canned outputs per pattern |
| `lab_4.2_prompt_templates.ipynb` | Lab 4.2 prompt template library | yes | canned outputs built from real rows |
| `lab_4.3_ptcf_bloom.ipynb` | Lab 4.3 PTCF upgrade of the Lab 3.2 ladder | yes | canned base + PTCF outputs |
| `lab_5.1_adversarial.ipynb` | Lab 5.1 adversarial robustness | no | fully self-contained (sklearn) |
| `lab_5.2_pii.ipynb` | Lab 5.2 PII detect & mask | no | regex fallback (Presidio optional) |
| `lab_6.1_data_quality.ipynb` | Lab 6.1 311 data-quality assessment | no | fully self-contained (pandas) |
| `lab_6.2_genai_cleaning.ipynb` | Lab 6.2 GenAI cleaning, JSON schema | yes | canned mapping with validation |
| `lab_7.1_openai_api.ipynb` | Lab 7.1 OpenAI API fundamentals | yes | cells guard on key; use transcript |
| `lab_7.2_rag_gov_docs.ipynb` | Lab 7.2 RAG over government documents | embeddings/answer | retrieval runs offline via local embedding fallback |
| `lab_7.3_agent.ipynb` | Lab 7.3 agent capstone | agent loop | tools run offline; loop needs key |
| `lab_8.1_visualization.ipynb` | Lab 8.1 EPA charts & briefing | no | fully self-contained (matplotlib) |
| `lab_8.2_genai_reporting.ipynb` | Lab 8.2 GenAI-assisted briefing | yes | canned findings + briefing |

Student notebooks have `# YOUR CODE` cells; instructor copies in
`solutions/` are complete.

## Quick start

```bash
pip install jupyterlab pandas scikit-learn matplotlib openai jupytext
export OPENAI_API_KEY=sk-...        # optional — labs fall back to canned outputs
export OPENAI_MODEL=gpt-5-mini      # optional — sensible default built in
jupyter lab                          # open any lab_*.ipynb and Run All
```

Run every notebook from the repository root (the notebooks expect
`lab_common.py` and `data/` beside them). With no key, a banner tells you
the lab is in offline mode and every step still runs.

## Repository layout

```
lab_*.ipynb          student notebooks (run from repo root)
lab_common.py        shared helpers: chat/JSON + embeddings with offline fallbacks
data/                six public US gov datasets + synthetic records, RAG corpus,
                     GAO-style memo (sources documented in data/MANIFEST.json)
solutions/           instructor *_solutions.ipynb (fully worked)
solutions/transcripts/  expected outputs if the API is down in class
src/                 jupytext sources — the notebooks are generated from these
build_notebooks.sh   src -> ipynb + offline smoke test + transcripts
```

## Rebuilding from source

Notebooks are authored as jupytext percent-format files in `src/`
(`*_SOLUTION.py` → `solutions/`). To regenerate and validate everything:

```bash
bash build_notebooks.sh
```

The script converts every source, then executes all student and solution
notebooks with `OPENAI_API_KEY=""` — proving the offline/canned paths work —
and extracts the expected-output transcripts.

## Data rule

Every file under `data/` is either genuinely public US government data
(documented in `data/MANIFEST.json`) or synthetic material written for
training. The synthetic `citizen_records.json` PII is fake by construction.
Never paste real agency data containing PII into these notebooks — or into
any AI tool.
