# Course 1258 lab test report

Date: 2026-08-07
Scope: `/home/student/1258-new/labs`
Mode: offline / no API key (`OPENAI_API_KEY=""`), using the project venv.

## Commands run

```bash
cd /home/student/1258-new/labs
OPENAI_API_KEY= bash build_notebooks.sh

cd /home/student/1258-new
OPENAI_API_KEY= .venv/bin/python tools/validate_release.py
```

Plus a static `nbformat` scan of every notebook for execution state, error outputs, stderr outputs, `# YOUR CODE` markers, hard-coded key patterns, retired OpenAI API patterns, manifest dataset presence/sizes, and transcript coverage.

Environment used by the test:

- Python: `3.12.13` (`/home/student/1258-new/.venv/bin/python`)
- JupyterLab: `4.6.2`
- Jupytext: `1.19.5`
- Kernel spec available: `1258-a4`; nbconvert was run with `--ExecutePreprocessor.kernel_name=1258-a4`
- Repo note: the working tree was already dirty before this run; `build_notebooks.sh` regenerates `.ipynb` files from `labs/src/*.py` and rewrites solution transcripts after a clean run.

## Result summary

| Check | Result |
|---|---|
| Jupytext conversion `src/*.py -> .ipynb` | PASS: 31 notebooks converted |
| Student notebook offline execution | PASS: 16/16 |
| Solution notebook offline execution | PASS: 15/15 |
| Total notebooks executed offline | PASS: 31/31 |
| Solution transcripts regenerated | PASS: 15 written |
| Stale transcripts | none |
| `tools/validate_release.py` | PASS: all checks |
| Hard-coded keys / retired API in code cells | none found |
| Notebook error outputs after execution | 0 |
| stderr stream outputs saved inside notebooks | 0 |
| Data manifest files | all present; public dataset byte sizes match |

Wall-clock: full build + smoke run completed in about 3m 29s. Smoke-log completion span for the 31 executions was about 141s. Slowest completion intervals were approximately: `lab_8.1_visualization` +7.2s, `lab_1.2_clustering` +6.4/+6.7s, and `lab_5.1_adversarial` +6.2/+6.6s.

Only warning seen: every `/tmp/1258-smoke-*.log` contains the local nbconvert kernel warning `Kernel is running over TCP without encryption`. This did not fail any lab and is a local execution/CI hygiene item, not a student-lab correctness issue.

## Notebook inventory and execution state

`cells` = total cells, `code` = code cells, `exec` = code cells with an execution count after the run, `err` = saved error outputs, `stderr` = saved stderr stream outputs, `YOUR` = `# YOUR CODE` / `your code` markers.

| notebook | cells | code | exec | err | stderr | YOUR | kernel |
|---|---:|---:|---:|---:|---:|---:|---|
| labs/lab_0.1_environment_tour.ipynb | 22 | 7 | 7 | 0 | 0 | 3 | python3 |
| labs/lab_0.1_healthcheck.ipynb | 17 | 5 | 5 | 0 | 0 | 0 | python3 |
| labs/lab_1.1_ai_inventory.ipynb | 24 | 7 | 7 | 0 | 0 | 6 | python3 |
| labs/lab_1.2_clustering.ipynb | 20 | 5 | 5 | 0 | 0 | 3 | python3 |
| labs/lab_2.1_data_expedition.ipynb | 19 | 4 | 4 | 0 | 0 | 2 | python3 |
| labs/lab_4.1_prompt_studio.ipynb | 35 | 13 | 13 | 0 | 0 | 8 | python3 |
| labs/lab_4.2_prompt_templates.ipynb | 21 | 8 | 8 | 0 | 0 | 4 | python3 |
| labs/lab_5.1_adversarial.ipynb | 19 | 5 | 5 | 0 | 0 | 4 | python3 |
| labs/lab_5.2_pii.ipynb | 21 | 5 | 5 | 0 | 0 | 4 | python3 |
| labs/lab_6.1_data_quality.ipynb | 24 | 7 | 7 | 0 | 0 | 6 | python3 |
| labs/lab_6.2_genai_cleaning.ipynb | 24 | 7 | 7 | 0 | 0 | 3 | python3 |
| labs/lab_7.1_openai_api.ipynb | 24 | 8 | 8 | 0 | 0 | 5 | python3 |
| labs/lab_7.2_rag_gov_docs.ipynb | 29 | 11 | 11 | 0 | 0 | 2 | python3 |
| labs/lab_7.3_agent.ipynb | 29 | 12 | 12 | 0 | 0 | 6 | python3 |
| labs/lab_8.1_visualization.ipynb | 23 | 5 | 5 | 0 | 0 | 3 | python3 |
| labs/lab_8.2_genai_reporting.ipynb | 21 | 8 | 8 | 0 | 0 | 5 | python3 |
| labs/solutions/lab_0.1_environment_tour_solutions.ipynb | 23 | 8 | 8 | 0 | 0 | 0 | python3 |
| labs/solutions/lab_1.1_ai_inventory_solutions.ipynb | 24 | 8 | 8 | 0 | 0 | 0 | python3 |
| labs/solutions/lab_1.2_clustering_solutions.ipynb | 21 | 6 | 6 | 0 | 0 | 0 | python3 |
| labs/solutions/lab_2.1_data_expedition_solutions.ipynb | 20 | 5 | 5 | 0 | 0 | 0 | python3 |
| labs/solutions/lab_4.1_prompt_studio_solutions.ipynb | 21 | 11 | 11 | 0 | 0 | 0 | python3 |
| labs/solutions/lab_4.2_prompt_templates_solutions.ipynb | 15 | 8 | 8 | 0 | 0 | 0 | python3 |
| labs/solutions/lab_5.1_adversarial_solutions.ipynb | 13 | 6 | 6 | 0 | 0 | 0 | python3 |
| labs/solutions/lab_5.2_pii_solutions.ipynb | 13 | 6 | 6 | 0 | 0 | 0 | python3 |
| labs/solutions/lab_6.1_data_quality_solutions.ipynb | 18 | 8 | 8 | 0 | 0 | 0 | python3 |
| labs/solutions/lab_6.2_genai_cleaning_solutions.ipynb | 15 | 7 | 7 | 0 | 0 | 0 | python3 |
| labs/solutions/lab_7.1_openai_api_solutions.ipynb | 15 | 7 | 7 | 0 | 0 | 0 | python3 |
| labs/solutions/lab_7.2_rag_gov_docs_solutions.ipynb | 14 | 7 | 7 | 0 | 0 | 0 | python3 |
| labs/solutions/lab_7.3_agent_solutions.ipynb | 16 | 8 | 8 | 0 | 0 | 0 | python3 |
| labs/solutions/lab_8.1_visualization_solutions.ipynb | 13 | 6 | 6 | 0 | 0 | 0 | python3 |
| labs/solutions/lab_8.2_genai_reporting_solutions.ipynb | 14 | 7 | 7 | 0 | 0 | 0 | python3 |

There are 16 student notebooks and 15 solution notebooks; `lab_0.1_healthcheck` intentionally has no separate solution notebook.

## Detailed findings

1. All authored student and solution notebooks execute end-to-end with no OpenAI key. This confirms the documented offline/canned fallback design works for the current VM.
2. `tools/validate_release.py` passed: registry loads, authored artifacts exist, no hard-coded keys or retired API calls in code cells, and `lab_common` offline paths work (`datagov=cached`, RAG corpus=4 docs, PII masking OK).
3. `labs/data/MANIFEST.json` is consistent with the files on disk: no missing dataset/synthetic files and no public-dataset byte-size mismatches.
4. Saved notebooks contain no error outputs and no captured stderr outputs after execution. The only warning is outside the notebooks, in the nbconvert smoke logs: local kernels run over TCP without encryption.
5. Notebook metadata still says `kernelspec.name=python3` even though execution used the registered `1258-a4` kernel. This is harmless when launched through the course venv, but less clear if a student opens the same notebook with a different Jupyter installation.

## Suggested changes / optimizations

Priority order:

1. Make data.gov cached-first by default. `MANIFEST.json` says the catalog.data.gov JSON API is gone as of 2026-08-01, but `lab_common.search_datasets()` still tries live CKAN first with an 8s timeout. Flip to cached-first and only try live when an explicit opt-in such as `DATAGOV_LIVE=1` is set. This removes avoidable offline delay and matches the manifest.
2. Align the healthcheck wording with that reality. `lab_0.1_healthcheck` still has a “data.gov reachable” check; keep it as an optional diagnostic, but label the cached snapshot as the expected classroom path so an offline room does not look broken.
3. Constrain `.env` discovery to the course root. `lab_common.load_dotenv()` currently searches a few parents of `labs/`; stop at the repo/course root (for example, the directory containing `.git` or `labs/`) so a stray parent `.env` outside the course cannot be picked up accidentally.
4. Cache Presidio engines if Presidio is present. `mask_pii()` builds `AnalyzerEngine()` and `AnonymizerEngine()` on every call. Use lazy module-level singletons so Lab 5.2/7.3 stay fast on VM images that include Presidio.
5. Use a FIPS-friendlier hash for the local embedding fallback. `_local_embed()` uses MD5 for non-security hashing; prefer `hashlib.blake2b`/`sha256` or `md5(..., usedforsecurity=False)` where supported. This is a small government-environment robustness improvement.
6. Add a machine-readable smoke result. Keep the human PASS/FAIL output, but also write JSON or JUnit XML (notebook, status, duration, log path). That makes CI/release-gate reporting easier without changing the student workflow.
7. Add `nbformat.validate()` after Jupytext conversion and fail the build on invalid notebooks. Execution already catches most problems, but validation catches malformed notebook JSON before the slower execute stage.
8. Make the smoke timeout and parallelism configurable. Current timeout is fixed at 180s and execution is sequential. Keep sequential as the safe default, but support `SMOKE_TIMEOUT` and an optional CI-only `SMOKE_JOBS` for changed-notebook or nightly runs. Measured notebooks are ~4–7s each, so the default timeout could be lower for CI while remaining generous for classroom VMs.
9. Consider setting notebook kernelspec metadata to the course kernel during build when `1258-a4` is registered. At minimum, document that the Desktop launcher uses the project venv, so the `python3` kernel shown in JupyterLab is the venv Python.
10. Consolidate registry inputs. Both `registry/labs.yaml` and `registry/activities.yaml` exist, and different validators read different files. Keep one canonical file and generate the other, or add a CI check that fails when they drift.
11. Treat the nbconvert TCP-encryption warning explicitly. Either run local CI kernels with IPC/CurveZMQ where practical, or document the warning as benign for local offline execution so future testers do not confuse it with a lab failure.
12. Add a changed-notebook fast path for authors. A `--changed` mode using `git diff --name-only` against the last release tag would let authors test only edited labs during development, while keeping the current full 31-notebook run as the release gate.

## Bottom line

The lab pack is in good shape: every student and solution notebook passes offline, the release gate passes, data files match the manifest, and transcripts are current. The highest-value improvements are cached-first data.gov behavior, clearer healthcheck wording, tighter `.env` discovery, Presidio engine caching, and machine-readable CI output.
