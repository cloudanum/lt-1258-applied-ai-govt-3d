# Course 1258 (rev a4) — Lab Notebooks

New and rewritten technical labs for the a4 roster, plus the Day-0
healthcheck. All notebooks read the OpenAI key from the `OPENAI_API_KEY`
environment variable (injected on the CloudShare VM) and pin the model via
`OPENAI_MODEL` — **no key is ever written in a notebook**.

## Contents
| File | Lab | Needs key? | Offline behavior |
|---|---|---|---|
| `lab_0.1_healthcheck.ipynb` | DONOW 0.1 | key check only | runs; reports which checks pass |
| `lab_0.1_environment_tour.ipynb` | Lab 0.1 environment & data tour | yes | canned first-call reply |
| `lab_1.1_ai_inventory.ipynb` | Lab 1.1 federal AI use case inventory | no | fully self-contained (pandas) |
| `lab_1.2_clustering.ipynb` | Lab 1.2 K-Means on EPA county AQI | no | fully self-contained (sklearn) |
| `lab_2.1_data_expedition.ipynb` | Lab 2.1 dataset profiling | no | cached data.gov snapshot fallback |
| `lab_4.1_prompt_studio.ipynb` | Lab 4.1 the four-rung prompt ladder | yes | canned outputs per rung |
| `lab_4.2_prompt_templates.ipynb` | Lab 4.2 prompt template library | yes | canned outputs built from real rows |
| `lab_5.1_adversarial.ipynb` | Lab 5.1 adversarial robustness | no | fully self-contained (sklearn) |
| `lab_5.2_pii.ipynb` | Lab 5.2 PII detect & mask | no | regex fallback (Presidio on the VM) |
| `lab_6.1_data_quality.ipynb` | Lab 6.1 311 data-quality assessment | no | fully self-contained (pandas) |
| `lab_6.2_genai_cleaning.ipynb` | Lab 6.2 GenAI cleaning, JSON schema | yes | canned mapping with validation |
| `lab_7.1_openai_api.ipynb` | Lab 7.1 (rewrite of old 6.3) | yes | canned per exercise; runs keyless |
| `lab_7.2_rag_gov_docs.ipynb` | Lab 7.2 (new) | embeddings/answer | retrieval runs offline via local embedding fallback |
| `lab_7.3_agent.ipynb` | Lab 7.3 capstone (new) | agent loop | tools run offline; loop shows canned trace |
| `lab_8.1_visualization.ipynb` | Lab 8.1 EPA charts & briefing | no | fully self-contained (matplotlib) |
| `lab_8.2_genai_reporting.ipynb` | Lab 8.2 GenAI-assisted briefing | yes | canned findings + briefing |
| `lab_common.py` | shared helpers | — | OpenAI + offline fallbacks for chat/JSON, embeddings, data.gov, PII |
| `data/` | lab data | — | six public datasets + the synthetic half (records, RAG corpus, memo, constituent feedback, Lab 3.1 and Ex 6.1 packs) — all declared in `MANIFEST.json` |
| `solutions/` | instructor copies | — | fully-worked `_solutions.ipynb` |
| `solutions/transcripts/` | expected outputs | — | read-along fallback if the API is down in class |

Student notebooks have `# YOUR CODE` cells; instructor copies in `solutions/` are
complete.

## Build & validate
```bash
bash build_notebooks.sh      # jupytext src/*.py -> *.ipynb, offline smoke, transcripts
```
The script converts every `src/*.py` (`*_SOLUTION.py` →
`solutions/*_solutions.ipynb`), then executes **all 16 student and 15 solution
notebooks** with `OPENAI_API_KEY=""`, proving the offline/canned paths work
(release-gate item 5 in the Lab Environment Plan). Solutions execute from
`solutions/`; their first cell shims cwd/`sys.path` back to `labs/`.
`make_transcripts.py` then extracts expected-output transcripts from the
executed solution notebooks, and reports any transcript no source regenerates.

The 7.x notebooks used to be excluded as "needs a live key". They are in the
smoke test now: every call site has a labelled canned fallback, and excluding
them only hid regressions in the three labs whose documented contingency *is*
the transcript.

The interpreter is picked in this order: `$VIRTUAL_ENV`, then `../.venv`, then
`python3` — it must have `jupytext` and `nbconvert`. Cells execute on the
`1258-a4` kernel when that kernelspec is registered.

## What changed from rev a2 (the Lab 6.3 fix)
The old `lab_6.3_genai.ipynb` used `openai.Completion.create(engine="text-davinci-003", …)`
— a removed API and a retired model — and asked students to paste a personal key
(`openai.api_key = "your_api_key_here"`). Both instructors who taught it (Bill
Appelbe, Jay Roy) hit this. Lab 7.1 replaces it with the current SDK, the injected
key, and the Responses/Chat API. The old lab is retired.

## Notebook rename map (fixes the a2 filename drift)
`lab_1.3_clustering.ipynb` → `lab_1.2_clustering.ipynb`;
`lab_1.4_decisiontree.ipynb` → `lab_1.3_decisiontree.ipynb`;
`lab_1.5_nlp_ner.ipynb` → `lab_1.4_nlp_ner.ipynb`;
`lab_3.4_PII.ipynb` → `lab_5.3_pii.ipynb`;
`lab_4.1_model_explanability.ipynb` → `lab_8.3_lime.ipynb`.
(Carried-forward notebooks are renamed by PD Lab during the image rebuild; the
registry `labs.yaml` is the source of truth.)
