---
title: "Course 1258 — Lab Manual"
subtitle: "Applied AI for Government IT Professionals · Revision a4"
---

# Lab Manual

Every activity in this course appears here, in the order you meet it. Each chapter has **one demo** your instructor runs, **four short activities or Do Nows** you run yourself, and **one or two labs** that go deep.

## Before you start

**Your environment.** Labs marked *CloudShare VM* run in JupyterLab in your browser. There is nothing to install.

**The API key.** Labs that call a model read the key from a `.env` file that already sits beside the `labs/` folder. You will never be asked to paste a key into a notebook, and you should never do so. If a notebook reports no key, tell your instructor.

**The data.** Six public datasets ship with the course under `labs/data/`, with sources recorded in `MANIFEST.json`. They are downloaded ahead of class because data.gov retired its API in 2026 and classroom networks are unreliable.

**The one rule that never changes: public or synthetic data only.** Every dataset and document in this manual is public US government data or synthetic material written for the course. Never paste real agency, personal or sensitive data into any assistant during this class.

## The datasets

| File | What it is |
|---|---|
| `federal_ai_use_cases.csv` | OMB 2025 Federal AI Use Case Inventory — real agency AI, as data |
| `federal_ai_cots.csv` | The same inventory's commercial off-the-shelf entries |
| `chicago_311.csv` | City of Chicago 311 requests — genuinely messy operational data |
| `cdc_flu_wastewater.csv` | CDC influenza wastewater surveillance — a real time series |
| `epa_aqi_by_county.csv` | EPA annual Air Quality Index by county, 2024 |
| `nyc_air_quality.csv` | NYC air-quality indicators by neighbourhood and period |

---

# Ch00 — Course Launch and Lab Environment

### Demo 0.1 Your Lab Environment, End to End

**Objectives**

By the end of this demo, you will:

- Watch the full path from My Learning Tree to a running notebook.
- See where the class OpenAI key lives and how a notebook reads it.

**Introduction**

Before anyone touches a keyboard, your instructor walks the whole environment once so you know what 'working' looks like.

**Where this fits**

- Chapter: **Ch00 Course Launch and Lab Environment**
- Slides: see chapter deck
- Time: **10 minutes**
- Environment: CloudShare VM (JupyterLab)

**Resources**

- OpenAI API key — loaded automatically from `.env`; never paste a key into a notebook

**Steps**

1. Instructor launches the VM and opens the in-browser Viewer (never RDP).
2. Instructor opens JupyterLab and shows the `labs/` file tree.
3. Instructor shows `.env` beside `labs/`, with the key masked, and explains that notebooks read it through `lab_common.load_dotenv()` — you never paste a key into a cell.
4. Instructor runs `lab_0.1_healthcheck.ipynb` and narrates the four checks.

**Reflection questions**

- Where does the key live, and why not in the notebook?
- Which check would fail first if the network were down?

---

### DO NOW 0.1 Environment Healthcheck

**Objectives**

By the end of this activity, you will:

- Reach a running JupyterLab in your CloudShare VM.
- Prove packages, data files, the API key and network are all ready.

**Introduction**

Nothing else in the week works until this is green, so it is the first thing you do.

**Where this fits**

- Chapter: **Ch00 Course Launch and Lab Environment**
- Slides: see chapter deck
- Time: **15 minutes**
- Environment: CloudShare VM (JupyterLab)

**Resources**

- `labs/data/MANIFEST.json`
- OpenAI API key — loaded automatically from `.env`; never paste a key into a notebook

**Steps**

1. Sign in to **My Learning Tree**, open the course page, click **Launch Lab**.
2. Click the **in-browser Viewer**. Do not use the RDP button — it errors.
3. Firefox opens JupyterLab automatically; if not, double-click **Start Labs** (password `pw` if asked).
4. Open `lab_0.1_healthcheck.ipynb` and choose **Run -> Run All Cells**.
5. Confirm checks 1-3 read **PASS**. Check 4 (network) is informational — a cached copy of every dataset ships on the VM.

**Reflection questions**

- Which check proves the OpenAI key is readable from `.env`?
- If check 2 failed, what would you look at first?

---

### DO NOW 0.2 Your First Prompt (Baseline Card)

**Objectives**

By the end of this activity, you will:

- Capture how you prompt *before* any instruction, as your own baseline.

**Introduction**

Think of one real task from your own job you would hand to an AI assistant. Write the prompt exactly as you would type it today.

**Where this fits**

- Chapter: **Ch00 Course Launch and Lab Environment**
- Slides: see chapter deck
- Time: **5 minutes**
- Environment: Browser + AI assistant
- Prompting spine: rung **P0**

**Steps**

1. Write the prompt on the card in your workbook — no editing, no help.
2. Do not score it and do not show it to the room.
3. Post it to the class whiteboard face-down, or seal it in your workbook.
4. You will reopen this on Day 3 at DO NOW 9.A and rewrite it.

**Reflection questions**

- What did you assume the model already knew?

---

### DO NOW 0.3 Which Account, Which Data?

**Objectives**

By the end of this activity, you will:

- Apply the course data rule before the first lab touches an assistant.

**Introduction**

Six one-line scenarios. For each, decide which tool you may use and whether the data may go into it at all.

**Where this fits**

- Chapter: **Ch00 Course Launch and Lab Environment**
- Slides: see chapter deck
- Time: **8 minutes**
- Environment: Paper — no computer needed

**Steps**

1. Read each scenario on the workbook page.
2. Mark each: **class account / agency approved tool / neither**.
3. Mark the data: **public - synthetic - never paste**.
4. Compare with your neighbour; your instructor takes the two that split the room.

**Reflection questions**

- Which scenario was hardest, and what made it hard?
- What would you need to know about a tool before pasting anything into it?

---

### DO NOW 0.4 AI Already in Your Day

**Objectives**

By the end of this activity, you will:

- Map where the room is starting from, and seed the Day-3 roadmap.

**Introduction**

Round the room: one place AI already touches your work, or one task you wish it would take off your hands.

**Where this fits**

- Chapter: **Ch00 Course Launch and Lab Environment**
- Slides: see chapter deck
- Time: **7 minutes**  *(flex — your instructor may skip this)*
- Environment: Paper — no computer needed

**Steps**

1. Name, agency, role.
2. One AI tool you have used, or one task you wish AI could do.
3. Instructor captures the wish list on the whiteboard.
4. The board stays up all week and is reused at Lab 9.1.

**Reflection questions**

- Whose example surprised you?

---

### Lab 0.1 Course Environment and Data Tour

**Objectives**

By the end of this lab, you will:

- Navigate JupyterLab confidently: cells, run order, kernel restart.
- Confirm the six shipped datasets load, and know what each one is for.
- Make one successful call to the OpenAI API using the key from `.env`.

**Introduction**

You have a working VM. Before the course leans on it, take ten minutes to learn the room: where the notebooks are, where the data is, and how a notebook reaches the model.

**Where this fits**

- Chapter: **Ch00 Course Launch and Lab Environment**
- Slides: see chapter deck
- Time: **20 minutes**
- Environment: CloudShare VM (JupyterLab)

**Resources**

- `labs/data/MANIFEST.json`
- `labs/data/federal_ai_use_cases.csv`
- `labs/data/chicago_311.csv`
- OpenAI API key — loaded automatically from `.env`; never paste a key into a notebook
- Notebook: `labs/lab_0.1_environment_tour.ipynb`

**Steps**

1. Open `lab_0.1_environment_tour.ipynb`.
2. Run the **environment** cell. Confirm it prints the `.env` path it loaded and the model alias — but never the key itself.
3. Run the **data inventory** cell. It reads `labs/data/MANIFEST.json` and prints each dataset with its row count and one-line description.
4. Load `federal_ai_use_cases.csv` with pandas. Print `.shape` and `.columns`.
5. Answer in the notebook: how many use cases are flagged `is_high_impact`?
6. Load `chicago_311.csv` and print the five most common `sr_type` values.
7. Run the **first API call** cell: a one-sentence prompt, printing the reply and the token counts.
8. Deliberately break something: restart the kernel, then re-run only the last cell and read the error. Then **Run All** to recover.

**Reflection questions**

- Why did the last cell fail after a kernel restart?
- Which of the six datasets would you reach for to answer 'which agencies use AI for document processing?'
- What did the token counts suggest about cost at agency scale?

---

# Ch01 — AI and ML Foundations for Government

### Demo 1.1 Supervised, Unsupervised, Generative — One Dataset

**Objectives**

By the end of this demo, you will:

- See all three families of AI applied to the same federal dataset.
- Understand what changes between them: the label, the goal, the output.

**Introduction**

One EPA table, three questions. Your instructor runs each in turn so the difference is concrete rather than definitional.

**Where this fits**

- Chapter: **Ch01 AI and ML Foundations for Government**
- Slides: see chapter deck
- Time: **10 minutes**
- Environment: CloudShare VM (JupyterLab)

**Resources**

- `labs/data/epa_aqi_by_county.csv`
- OpenAI API key — loaded automatically from `.env`; never paste a key into a notebook

**Steps**

1. **Supervised:** predict a county's `Max AQI` from its day counts — there is a right answer to learn from.
2. **Unsupervised:** cluster counties by air-quality profile — no labels, the structure is discovered.
3. **Generative:** ask the model to write the county's air-quality summary in plain English for a public webpage.
4. Instructor names what changed each time: the label, the goal, the output type.

**Reflection questions**

- Which of the three needed labelled data, and why does that matter for cost?
- Which one could you not verify by looking at the data alone?

---

### DO NOW 1.A Explain It to a CIO, Then to a Citizen

**Objectives**

By the end of this activity, you will:

- Use role and audience framing to change an explanation's register.

**Introduction**

Same fact, two audiences. This is the first rung of the prompting spine.

**Where this fits**

- Chapter: **Ch01 AI and ML Foundations for Government**
- Slides: see chapter deck
- Time: **10 minutes**  *(flex — your instructor may skip this)*
- Environment: Browser + AI assistant
- Prompting spine: rung **P1**

**Steps**

1. Ask an assistant to explain **random forests to a CIO deciding on funding**.
2. Ask it again for **a citizen reading an agency FAQ**.
3. Underline the three biggest differences between the two answers.
4. Post the better opening line to the whiteboard.

**Reflection questions**

- Which framing worked better, and what exactly in your prompt caused it?

---

### DO NOW 1.B Classic ML or GenAI?

**Objectives**

By the end of this activity, you will:

- Choose the right tool class for a task before choosing a product.

**Introduction**

Eight real agency tasks. For each, decide whether classic ML, generative AI, or neither is the right instrument.

**Where this fits**

- Chapter: **Ch01 AI and ML Foundations for Government**
- Slides: see chapter deck
- Time: **7 minutes**
- Environment: Paper — no computer needed

**Steps**

1. Read the eight tasks on the workbook page.
2. Mark each **ML / GenAI / neither**, and add one word of justification.
3. Compare with a neighbour; argue any you disagree on.
4. Instructor resolves the three designed to be genuinely ambiguous.

**Reflection questions**

- Which tasks were ambiguous, and what extra fact would settle them?
- Which ones would be cheaper *without* AI at all?

---

### DO NOW 1.C Prompt It or Train It?

**Objectives**

By the end of this activity, you will:

- Feel the difference between prompting a general model and training a specific one, on the same classification problem.

**Introduction**

Chicago 311 requests carry a `sr_type` label. That is a classification problem you could train — or just describe.

**Where this fits**

- Chapter: **Ch01 AI and ML Foundations for Government**
- Slides: see chapter deck
- Time: **10 minutes**  *(flex — your instructor may skip this)*
- Environment: Browser + AI assistant

**Resources**

- `labs/data/chicago_311.csv`
- OpenAI API key — loaded automatically from `.env`; never paste a key into a notebook

**Steps**

1. Take ten `sr_type` values from `chicago_311.csv`.
2. Ask an assistant to classify five unlabelled request descriptions into those categories, with no examples.
3. Compare its answers with the real labels.
4. Discuss: how many labelled rows would you need to train a classifier to match?

**Reflection questions**

- When is 'just prompt it' the right engineering answer?
- What would make you switch to training a model?

---

### DO NOW 1.D Find Your Agency in the Inventory

**Objectives**

By the end of this activity, you will:

- Locate real, published AI use cases from your own organisation.

**Introduction**

Every agency publishes its AI use cases annually under OMB M-25-21. Yours is in the file on your VM.

**Where this fits**

- Chapter: **Ch01 AI and ML Foundations for Government**
- Slides: see chapter deck
- Time: **8 minutes**
- Environment: CloudShare VM (JupyterLab)

**Resources**

- `labs/data/federal_ai_use_cases.csv`

**Steps**

1. Open `federal_ai_use_cases.csv` in a notebook or spreadsheet.
2. Filter `agency_name` to your agency, or the closest one to your work.
3. Read three `use_case_name` and `problem_solved` entries.
4. Note one you did not know existed.

**Reflection questions**

- Did anything surprise you about what your agency has already deployed?
- How many of your agency's use cases are flagged high-impact?

---

### Lab 1.1 Exploring the Federal AI Use Case Inventory

**Objectives**

By the end of this lab, you will:

- Load, filter, group and summarise a real federal dataset with pandas.
- Answer substantive questions about federal AI adoption from evidence.
- Practise the analysis habits every later lab depends on.

**Introduction**

You have been asked to brief your CIO on what other agencies are actually doing with AI. The OMB inventory is public and sitting on your VM. No AI is needed for this lab — this is the data literacy underneath it.

**Where this fits**

- Chapter: **Ch01 AI and ML Foundations for Government**
- Slides: see chapter deck
- Time: **30 minutes**
- Environment: CloudShare VM (JupyterLab)

**Resources**

- `labs/data/federal_ai_use_cases.csv`
- `labs/data/federal_ai_cots.csv`
- Notebook: `labs/lab_1.1_ai_inventory.ipynb`

**Steps**

1. Open `lab_1.1_ai_inventory.ipynb` and run the setup cell.
2. Print the shape and columns. How many use cases, how many agencies?
3. Group by `agency_name` and produce the top 10 agencies by use-case count.
4. Group by `development_stage`. What share is actually in production?
5. Filter `is_high_impact`. Which agencies report the most high-impact AI?
6. Cross-tabulate `topic_area` against `development_stage` and read one row aloud.
7. Join the COTS file. Which commercial tools appear most often?
8. Write three findings in the notebook, each with the line of code that produced it.

**Reflection questions**

- Which single number would most change your CIO's mind?
- What does this dataset *not* tell you about how well any of it works?
- Where would a chart have been clearer than a table?

---

### Lab 1.2 Clustering Counties by Air Quality (K-Means)

**Objectives**

By the end of this lab, you will:

- Run K-Means on a real EPA dataset and interpret the clusters.
- Choose k deliberately rather than by default.
- Explain an unsupervised result to a non-technical stakeholder.

**Introduction**

EPA publishes an annual air-quality summary for every county. Nobody has labelled them. You want to find the natural groupings so a programme office can target outreach.

**Where this fits**

- Chapter: **Ch01 AI and ML Foundations for Government**
- Slides: see chapter deck
- Time: **30 minutes**  *(flex — your instructor may skip this)*
- Environment: CloudShare VM (JupyterLab)

**Resources**

- `labs/data/epa_aqi_by_county.csv`
- Notebook: `labs/lab_1.2_clustering.ipynb`

**Steps**

1. Open `lab_1.2_clustering.ipynb` and load `epa_aqi_by_county.csv`.
2. Select the numeric day-count columns and scale them.
3. Fit K-Means with k=3. Print each cluster's size and column means.
4. Name each cluster in plain English from those means.
5. Sweep k from 2 to 8, plot inertia, and choose a k you can defend.
6. List the counties in the worst cluster and sanity-check against the raw rows.
7. Write two sentences a programme director could act on.

**Reflection questions**

- What changed when you changed k?
- Why did scaling matter here?
- What would you tell someone who asked 'is this cluster correct?'

---

# Ch02 — AI Applications Across Government and Public Data

### Demo 2.1 Finding Government Data in 2026

**Objectives**

By the end of this demo, you will:

- See how federal data is actually located now that data.gov's API is gone.
- Learn the agency-portal route the labs rely on.

**Introduction**

data.gov retired its CKAN Action API in 2026 and the rebuilt catalogue exposes no JSON API at all. Your instructor shows what still works.

**Where this fits**

- Chapter: **Ch02 AI Applications Across Government and Public Data**
- Slides: see chapter deck
- Time: **10 minutes**
- Environment: Browser + AI assistant

**Resources**

- `labs/data/MANIFEST.json`

**Steps**

1. Search catalog.data.gov in the browser for 'air quality'.
2. Follow one result through to the hosting agency portal.
3. Show the Socrata pattern: `/resource/<id>.csv?$limit=...`.
4. Show `labs/data/MANIFEST.json` — the same datasets, already downloaded, with their source URLs recorded.

**Reflection questions**

- Why does an offline copy matter for a classroom?
- How would you cite one of these datasets in an agency brief?

---

### DO NOW 2.A Ask for Datasets, Then Verify

**Objectives**

By the end of this activity, you will:

- Experience model fabrication on a checkable claim, early and safely.

**Introduction**

You need three datasets for a stated need. Ask an assistant, then check every one. At least one will not exist.

**Where this fits**

- Chapter: **Ch02 AI Applications Across Government and Public Data**
- Slides: see chapter deck
- Time: **10 minutes**
- Environment: Browser + AI assistant
- Prompting spine: rung **P2**

**Steps**

1. Ask an assistant for **three data.gov datasets** relevant to a need you name.
2. For each, search catalog.data.gov and record: found / not found / different.
3. Mark which were real, which were plausible-but-wrong.
4. Introduce the rubric: accuracy, completeness, format, tone. Score the answer.

**Reflection questions**

- What did the fabricated one have in common with the real ones?
- What prompt change would have reduced the risk?

---

### DO NOW 2.B Source That Claim

**Objectives**

By the end of this activity, you will:

- Practise tracing a confident statistic back to a primary source.

**Introduction**

Five AI-in-government claims of the kind that circulate in slide decks. Some are real, some are not.

**Where this fits**

- Chapter: **Ch02 AI Applications Across Government and Public Data**
- Slides: see chapter deck
- Time: **8 minutes**  *(flex — your instructor may skip this)*
- Environment: Browser + AI assistant

**Steps**

1. Read the five claims on the workbook page.
2. For each, spend 90 seconds trying to find a primary source.
3. Mark **sourced / unsourceable**, and name the source where you found one.
4. Instructor reveals which two have no traceable origin.

**Reflection questions**

- What made the unsourceable ones believable?
- What is the cost of one of these reaching a public briefing?

---

### DO NOW 2.C Which Pattern Is This?

**Objectives**

By the end of this activity, you will:

- Recognise the small number of repeating patterns behind most gov AI.

**Introduction**

Six real use cases pulled from the federal inventory. Each is an instance of a pattern you have now seen.

**Where this fits**

- Chapter: **Ch02 AI Applications Across Government and Public Data**
- Slides: see chapter deck
- Time: **7 minutes**
- Environment: Paper — no computer needed

**Resources**

- `labs/data/federal_ai_use_cases.csv`

**Steps**

1. Read the six `use_case_name` / `problem_solved` pairs.
2. Label each: early warning, document processing, triage, forecasting, anomaly detection, or content generation.
3. Find one more example of your assigned pattern in the CSV.
4. Report the pattern, not the product.

**Reflection questions**

- Which pattern appears most often across the inventory?
- Which pattern would be easiest to start in your own office?

---

### DO NOW 2.D Bookmark a Dataset for Day 3

**Objectives**

By the end of this activity, you will:

- Choose the dataset you will hand to an agent on Day 3.

**Introduction**

Lab 7.3 builds an agent that answers questions about a dataset. Pick yours now.

**Where this fits**

- Chapter: **Ch02 AI Applications Across Government and Public Data**
- Slides: see chapter deck
- Time: **5 minutes**
- Environment: CloudShare VM (JupyterLab)

**Resources**

- `labs/data/MANIFEST.json`

**Steps**

1. Open `labs/data/MANIFEST.json` and read all six descriptions.
2. Pick the one closest to your own work.
3. Write its filename and one question you want answered about it on your card.
4. Keep the card — Lab 7.3 uses it.

**Reflection questions**

- Why that dataset?

---

### Lab 2.1 Public Data Expedition — Profile an Agency Dataset

**Objectives**

By the end of this lab, you will:

- Profile an unfamiliar public dataset from scratch.
- Read metadata critically and state what the data cannot answer.
- Produce a one-paragraph dataset briefing another analyst could use.

**Introduction**

A programme office hands you a dataset and asks 'can we use this?'. That question is answered by profiling, not by opinion. You will do it three times, quickly, on three real datasets.

**Where this fits**

- Chapter: **Ch02 AI Applications Across Government and Public Data**
- Slides: see chapter deck
- Time: **30 minutes**
- Environment: CloudShare VM (JupyterLab)

**Resources**

- `labs/data/cdc_flu_wastewater.csv`
- `labs/data/nyc_air_quality.csv`
- `labs/data/chicago_311.csv`
- Notebook: `labs/lab_2.1_data_expedition.ipynb`

**Steps**

1. Open `lab_2.1_data_expedition.ipynb`.
2. For **each** of the three datasets: load it and print shape, columns, dtypes.
3. Report per column: null count, distinct count, and an example value.
4. Identify the grain — what does one row actually represent?
5. Identify the time column and print the date range.
6. Name one question the dataset answers well and one it cannot answer.
7. Write a four-sentence briefing for the CDC wastewater file, including its grain, coverage, and one caveat.

**Reflection questions**

- Which dataset was hardest to establish a grain for?
- What would you ask the data owner before using any of these in a decision?
- The Ch02 slides describe wastewater surveillance as an early-warning system. Does this file support that claim on its own?

---

# Ch03 — Desktop GenAI: Everyday AI for Government Staff

### Demo 3.1 Four Assistants, One Task

**Objectives**

By the end of this demo, you will:

- See the same government task run against different assistants.
- Notice that prompt quality moves the answer more than brand does.

**Introduction**

Your instructor gives one identical prompt to the assistants available in the room and projects the answers side by side.

**Where this fits**

- Chapter: **Ch03 Desktop GenAI: Everyday AI for Government Staff**
- Slides: see chapter deck
- Time: **10 minutes**
- Environment: Browser + AI assistant

**Resources**

- `labs/data/gov_memo.txt`

**Steps**

1. Instructor pastes the same summarise-this-memo prompt into each assistant.
2. Room calls out differences in structure, length, hedging and tone.
3. Instructor improves the prompt once and re-runs the weakest performer.
4. Room compares the improvement against the gap between products.

**Reflection questions**

- Did the prompt change or the product change do more for quality?
- Which differences would actually matter in your work?

---

### DO NOW 3.A Summarize for a Named Reader

**Objectives**

By the end of this activity, you will:

- Run the summarisation pattern and score it against the rubric.

**Introduction**

A two-page agency memo, and two very different readers.

**Where this fits**

- Chapter: **Ch03 Desktop GenAI: Everyday AI for Government Staff**
- Slides: see chapter deck
- Time: **8 minutes**
- Environment: Browser + AI assistant
- Prompting spine: rung **P3**

**Resources**

- `labs/data/gov_memo.txt`

**Steps**

1. Summarise `gov_memo.txt` in five bullets **for a programme manager**.
2. Re-run it **for a congressional staffer with two minutes**.
3. Score both on the rubric: accuracy, completeness, format, tone.
4. Keep the better prompt on your Prompt Card.

**Reflection questions**

- Which rubric dimension moved most between the two?

---

### DO NOW 3.B Text to Diagram

**Objectives**

By the end of this activity, you will:

- Turn prose into a diagram you can paste into a document.

**Introduction**

The FOIA processing guidance describes a workflow in paragraphs. Nobody reads paragraphs.

**Where this fits**

- Chapter: **Ch03 Desktop GenAI: Everyday AI for Government Staff**
- Slides: see chapter deck
- Time: **8 minutes**
- Environment: Browser + AI assistant

**Resources**

- `labs/data/corpus/foia_processing_guidance.md`

**Steps**

1. Paste the FOIA guidance into an assistant.
2. Ask for a **Mermaid flowchart** of the process, and nothing else.
3. Paste the result into a Mermaid preview and check every branch.
4. Fix one thing the model got wrong by editing your prompt, not the diagram.

**Reflection questions**

- What did the model invent that the source did not say?

---

### DO NOW 3.C Can I Paste This?

**Objectives**

By the end of this activity, you will:

- Build the reflex the data rule depends on.

**Introduction**

Six realistic items land on your desk. For each, decide what may go where.

**Where this fits**

- Chapter: **Ch03 Desktop GenAI: Everyday AI for Government Staff**
- Slides: see chapter deck
- Time: **10 minutes**
- Environment: Paper — no computer needed

**Steps**

1. Sort each item into **share / redact first / never**.
2. Then repeat per tool tier: public chatbot, enterprise Copilot, on-prem.
3. Draft the redaction prompt for the one item you marked 'redact first'.
4. Instructor runs the room's best redaction prompt on a synthetic memo.

**Reflection questions**

- Which item changed category between tool tiers, and why?

---

### DO NOW 3.D Shadow AI Inventory

**Objectives**

By the end of this activity, you will:

- Surface unapproved tool use as a problem to manage, not to punish.

**Introduction**

Shadow AI is what staff reach for when the approved path is slower.

**Where this fits**

- Chapter: **Ch03 Desktop GenAI: Everyday AI for Government Staff**
- Slides: see chapter deck
- Time: **7 minutes**  *(flex — your instructor may skip this)*
- Environment: Paper — no computer needed

**Steps**

1. List, anonymously, AI tools you have seen used for work.
2. Mark each **approved / unknown / definitely not approved**.
3. For one 'not approved', name the legitimate need behind it.
4. Propose the approved path that would win.

**Reflection questions**

- What would make the approved tool the easier choice?

---

### Lab 3.1 Desktop GenAI Task Relay

**Objectives**

By the end of this lab, you will:

- Run the five everyday desktop-GenAI patterns on real agency material.
- Score every output against the shared rubric.
- Leave with five prompts you will reuse on Monday.

**Introduction**

This is the 'what you actually do Monday' lab. Five timed micro-tasks, each a pattern you will use every week. Public and synthetic material only.

**Where this fits**

- Chapter: **Ch03 Desktop GenAI: Everyday AI for Government Staff**
- Slides: see chapter deck
- Time: **30 minutes**
- Environment: Browser + AI assistant
- Prompting spine: rung **P3**

**Resources**

- `labs/data/gov_memo.txt`
- `labs/data/corpus/ai_acceptable_use_policy.md`
- `labs/data/citizen_records.json`

**Steps**

1. **Research and explain** — ask for a plain-English explanation of a term from the acceptable-use policy, for a named audience. (7 min)
2. **Summarize** — five bullets from `gov_memo.txt` for a programme manager. (7 min)
3. **Draft and rewrite** — draft a citizen reply from one synthetic record, then rewrite it two reading levels lower. (10 min)
4. **Diagram** — a Mermaid flowchart of the memo's approval chain. (7 min)
5. **Troubleshoot** — paste the broken snippet from your workbook and ask for the fix *and the reason*. (7 min)
6. Score all five on the rubric and copy your two best prompts onto your Prompt Card. (7 min)

**Reflection questions**

- Which pattern will you use first, and on what?
- Where did the assistant sound confident and be wrong?
- Which task would you never delegate without review?

---

# Ch04 — Modern GenAI and Prompt Engineering

### Demo 4.1 Zero-Shot, Few-Shot, Reasoning — Same Task

**Objectives**

By the end of this demo, you will:

- See what each prompting technique is actually worth on one task.
- See where a reasoning model makes manual chain-of-thought redundant.

**Introduction**

One classification task, three techniques, run live so the differences are measured rather than asserted.

**Where this fits**

- Chapter: **Ch04 Modern GenAI and Prompt Engineering**
- Slides: see chapter deck
- Time: **10 minutes**
- Environment: CloudShare VM (JupyterLab)

**Resources**

- `labs/data/chicago_311.csv`
- OpenAI API key — loaded automatically from `.env`; never paste a key into a notebook

**Steps**

1. Instructor classifies ten 311 descriptions **zero-shot** and counts errors.
2. Adds **three examples** and re-runs. Counts errors again.
3. Asks the model to **think step by step**, then runs the same task on a **reasoning model** with no such instruction.
4. Room compares accuracy against tokens and latency.

**Reflection questions**

- Which step bought the most accuracy per token?
- When is 'think step by step' now redundant?

---

### DO NOW 4.A Add Two Examples

**Objectives**

By the end of this activity, you will:

- Measure the effect of few-shot examples on your own task.

**Introduction**

Few-shot prompting is the cheapest accuracy you can buy — when the examples are representative.

**Where this fits**

- Chapter: **Ch04 Modern GenAI and Prompt Engineering**
- Slides: see chapter deck
- Time: **10 minutes**
- Environment: CloudShare VM (JupyterLab)

**Resources**

- `labs/data/chicago_311.csv`
- OpenAI API key — loaded automatically from `.env`; never paste a key into a notebook

**Steps**

1. Classify five 311 descriptions zero-shot into `sr_type` categories.
2. Record how many match the real label.
3. Add two well-chosen examples to the prompt and re-run.
4. Record again. Then add two *badly chosen* examples and re-run.

**Reflection questions**

- What did the bad examples do to the output?
- How would you choose examples for a task with 40 categories?

---

### DO NOW 4.B Give the Model a Job

**Objectives**

By the end of this activity, you will:

- Use role prompting to change what the model attends to.

**Introduction**

Same document, three roles.

**Where this fits**

- Chapter: **Ch04 Modern GenAI and Prompt Engineering**
- Slides: see chapter deck
- Time: **8 minutes**
- Environment: Browser + AI assistant

**Resources**

- `labs/data/corpus/foia_processing_guidance.md`

**Steps**

1. Ask about the FOIA guidance as **a FOIA officer**.
2. Then as **a requester**. Then as **an agency attorney**.
3. Note what each role surfaced that the others missed.
4. Keep the most useful role line on your Prompt Card.

**Reflection questions**

- Did the role change the facts, or only the emphasis? How would you check?

---

### DO NOW 4.C Ask for the Shape You Need

**Objectives**

By the end of this activity, you will:

- Get output you can use directly, not output you must retype.

**Introduction**

Prose is a bad interface between a model and a spreadsheet.

**Where this fits**

- Chapter: **Ch04 Modern GenAI and Prompt Engineering**
- Slides: see chapter deck
- Time: **10 minutes**
- Environment: CloudShare VM (JupyterLab)

**Resources**

- `labs/data/citizen_records.json`
- OpenAI API key — loaded automatically from `.env`; never paste a key into a notebook

**Steps**

1. Ask for three synthetic citizen records extracted as **prose**.
2. Re-ask for a **JSON array with a named schema and required fields**.
3. Parse the JSON in Python. Fix any failure by tightening the prompt.
4. Re-run twice and confirm the shape is stable.

**Reflection questions**

- What in your prompt made the shape reliable?
- Schema-correct is not the same as correct — what would you still check?

---

### DO NOW 4.D Answer Only From This Document

**Objectives**

By the end of this activity, you will:

- Constrain a model to a source — the manual ancestor of RAG.

**Introduction**

Grounding is a prompt instruction before it is an architecture.

**Where this fits**

- Chapter: **Ch04 Modern GenAI and Prompt Engineering**
- Slides: see chapter deck
- Time: **8 minutes**
- Environment: Browser + AI assistant

**Resources**

- `labs/data/corpus/records_retention_policy.md`

**Steps**

1. Paste the retention policy and ask a question it **does** answer.
2. Ask one it **does not** answer, with no grounding instruction.
3. Re-ask with: *answer only from the text; if it is not there, say 'not stated'; quote the sentence you used*.
4. Compare the two failures.

**Reflection questions**

- Did the grounding instruction stop the invention entirely?
- What does this predict about how RAG will behave on Day 3?

---

### Lab 4.1 Prompt Engineering Studio

**Objectives**

By the end of this lab, you will:

- Apply the seven prompt patterns to real government material.
- Score every output against the rubric and improve the weakest.
- Leave with a personal, tested prompt library.

**Introduction**

This is the consolidation lab. You have already climbed rungs P0-P3, so the ladder here names skills you have been using since Day 1.

**Where this fits**

- Chapter: **Ch04 Modern GenAI and Prompt Engineering**
- Slides: see chapter deck
- Time: **30 minutes**
- Environment: CloudShare VM (JupyterLab)
- Prompting spine: rung **P4**

**Resources**

- `labs/data/gov_memo.txt`
- `labs/data/chicago_311.csv`
- `labs/data/corpus/ai_acceptable_use_policy.md`
- OpenAI API key — loaded automatically from `.env`; never paste a key into a notebook
- Notebook: `labs/lab_4.1_prompt_studio.ipynb`

**Steps**

1. Open `lab_4.1_prompt_studio.ipynb`.
2. **Zero-shot:** summarise the GAO-style excerpt. Score it. (5 min)
3. **Few-shot:** add two exemplars to a 311 classification. Score it. (5 min)
4. **Reasoning:** run the hardest item on a reasoning model, no CoT instruction. (5 min)
5. **Iterate:** take your worst output and improve it in three rounds, keeping each version. (6 min)
6. **Role:** 'You are a FOIA officer...' on the acceptable-use policy. (5 min)
7. **Structured output:** extract entities from a press release into a table. (6 min)
8. **Grounding:** answer only from the policy, with the quoted sentence. (6 min)
9. Copy your best prompt from each pattern onto your Prompt Card. (7 min)

**Reflection questions**

- Which pattern gave the biggest jump in rubric score?
- Which of your three iteration rounds actually helped, and why?
- Which prompt would you hand to a colleague unchanged?

---

### Lab 4.2 Build a Reusable Prompt Template Library

**Objectives**

By the end of this lab, you will:

- Turn one-off prompts into parameterised templates.
- Test a template against inputs it was not written for.
- Ship something your team can adopt.

**Introduction**

A prompt that works once is a trick. A template that works on inputs you have not seen is a tool.

**Where this fits**

- Chapter: **Ch04 Modern GenAI and Prompt Engineering**
- Slides: see chapter deck
- Time: **30 minutes**  *(flex — your instructor may skip this)*
- Environment: CloudShare VM (JupyterLab)

**Resources**

- `labs/data/federal_ai_use_cases.csv`
- OpenAI API key — loaded automatically from `.env`; never paste a key into a notebook
- Notebook: `labs/lab_4.2_prompt_templates.ipynb`

**Steps**

1. Open `lab_4.2_prompt_templates.ipynb`.
2. Take your best prompt from Lab 4.1 and replace the specifics with `[BRACKETED]` slots.
3. Write it as a Python function taking those slots as arguments.
4. Run it over five different rows of `federal_ai_use_cases.csv`.
5. Find the input that breaks it and fix the template, not the input.
6. Add a second template for a different pattern and test it the same way.
7. Export both to `my_prompt_library.md`.

**Reflection questions**

- What broke first when the input varied?
- Which slot turned out to matter most?
- What would you need to add before handing this to your team?

---

# Ch05 — AI Security, Risks, and Responsible AI

### Demo 5.1 Prompt Injection, Live

**Objectives**

By the end of this demo, you will:

- Watch a guarded system prompt fall over.
- See why injection through a *tool result* is the harder problem.

**Introduction**

Your instructor runs a small assistant with a system prompt that forbids revealing an internal note, then defeats it.

**Where this fits**

- Chapter: **Ch05 AI Security, Risks, and Responsible AI**
- Slides: see chapter deck
- Time: **10 minutes**
- Environment: CloudShare VM (JupyterLab)

**Resources**

- `labs/data/corpus/data_governance_standard.md`
- OpenAI API key — loaded automatically from `.env`; never paste a key into a notebook

**Steps**

1. Instructor shows the system prompt and the guard it contains.
2. Room suggests attacks; instructor runs them until one lands.
3. Instructor then hides the same attack inside a *document* the assistant retrieves — the indirect case.
4. Instructor shows which defences would have stopped each.

**Reflection questions**

- Why is the indirect case harder to defend?
- Which of these would your agency actually detect?

---

### DO NOW 5.A Rank These Risks

**Objectives**

By the end of this activity, you will:

- Order AI risks by likelihood and impact for your own context.

**Introduction**

Eight risks from the chapter. Your agency cannot mitigate all of them at once.

**Where this fits**

- Chapter: **Ch05 AI Security, Risks, and Responsible AI**
- Slides: see chapter deck
- Time: **8 minutes**
- Environment: Paper — no computer needed

**Steps**

1. Place each risk on a likelihood/impact grid on the workbook page.
2. Circle the two you would fund first.
3. Compare with a neighbour from a different agency.
4. Instructor collects the two most-circled.

**Reflection questions**

- Where did you and your neighbour disagree, and why?

---

### DO NOW 5.B Confidentiality, Integrity, or Availability?

**Objectives**

By the end of this activity, you will:

- Map AI-specific failures onto the security model you already use.

**Introduction**

Six AI incidents. Each breaks one leg of the CIA triad — or more.

**Where this fits**

- Chapter: **Ch05 AI Security, Risks, and Responsible AI**
- Slides: see chapter deck
- Time: **7 minutes**  *(flex — your instructor may skip this)*
- Environment: Paper — no computer needed

**Steps**

1. Read the six incidents.
2. Mark each **C / I / A**, allowing more than one.
3. For the two you marked with several, say which matters most.
4. Instructor resolves the contested ones.

**Reflection questions**

- Which leg does hallucination actually attack?

---

### DO NOW 5.C Injection Red Team

**Objectives**

By the end of this activity, you will:

- Write an attack, then write the defence that stops your own attack.

**Introduction**

Seven minutes attacking, six defending. The sandbox bot is synthetic.

**Where this fits**

- Chapter: **Ch05 AI Security, Risks, and Responsible AI**
- Slides: see chapter deck
- Time: **10 minutes**  *(flex — your instructor may skip this)*
- Environment: CloudShare VM (JupyterLab)
- Prompting spine: rung **P5**

**Resources**

- OpenAI API key — loaded automatically from `.env`; never paste a key into a notebook

**Steps**

1. Read the sandbox bot's system prompt in the notebook.
2. Spend 7 minutes writing prompts that make it break its own rule.
3. Swap with a neighbour and try to defeat theirs.
4. Spend 6 minutes rewriting the system prompt so your own attack fails.

**Reflection questions**

- Which defence held, and what did it cost in usefulness?
- Could you have defended without knowing the attack?

---

### DO NOW 5.D Is This High-Impact AI?

**Objectives**

By the end of this activity, you will:

- Apply the M-25-21 high-impact definition to real inventory entries.

**Introduction**

'High-impact AI' is a term of art that triggers mandatory practices. The inventory records how agencies themselves classified each use case.

**Where this fits**

- Chapter: **Ch05 AI Security, Risks, and Responsible AI**
- Slides: see chapter deck
- Time: **8 minutes**
- Environment: CloudShare VM (JupyterLab)

**Resources**

- `labs/data/federal_ai_use_cases.csv`

**Steps**

1. Pull five use cases from `federal_ai_use_cases.csv` with the flag hidden.
2. Decide for each: high-impact or not, using the definition on the slide.
3. Reveal `is_high_impact` and compare.
4. Read the `HI_justification` for any you got wrong.

**Reflection questions**

- Where did your judgement differ from the agency's?
- What obligations follow once something is labelled high-impact?

---

### Lab 5.1 Adversarial Examples and Model Robustness

**Objectives**

By the end of this lab, you will:

- Craft inputs that flip a model's prediction.
- Measure how much perturbation it actually takes.
- Name the defences that would have helped.

**Introduction**

You are testing a classifier before it goes anywhere near a decision. Your job is to break it on purpose, in a sandbox, and report honestly.

**Where this fits**

- Chapter: **Ch05 AI Security, Risks, and Responsible AI**
- Slides: see chapter deck
- Time: **30 minutes**  *(flex — your instructor may skip this)*
- Environment: CloudShare VM (JupyterLab)

**Resources**

- `labs/data/epa_aqi_by_county.csv`
- Notebook: `labs/lab_5.1_adversarial.ipynb`

**Steps**

1. Open `lab_5.1_adversarial.ipynb` and train the small classifier provided.
2. Record its baseline accuracy on the held-out set.
3. Perturb one feature at a time and find the smallest change that flips a prediction.
4. Plot flip rate against perturbation size.
5. Apply one defence from the chapter and re-measure.
6. Write what you would tell a system owner in three sentences.

**Reflection questions**

- How small was the smallest successful perturbation?
- Would the defence have survived an attacker who knew about it?
- Which of the MITRE ATLAS tactics does this correspond to?

---

### Lab 5.2 Detect and Mask PII in Citizen Records

**Objectives**

By the end of this lab, you will:

- Find PII in structured and free-text government data.
- Mask it without destroying the record's analytic value.
- Measure what your detector misses.

**Introduction**

Before any dataset leaves your boundary — to a vendor, a portal, or a model — someone has to find the PII. Today that is you. All records here are synthetic.

**Where this fits**

- Chapter: **Ch05 AI Security, Risks, and Responsible AI**
- Slides: see chapter deck
- Time: **30 minutes**
- Environment: CloudShare VM (JupyterLab)

**Resources**

- `labs/data/citizen_records.json`
- `labs/data/chicago_311.csv`
- Notebook: `labs/lab_5.2_pii.ipynb`

**Steps**

1. Open `lab_5.2_pii.ipynb`.
2. Run the regex detector over `citizen_records.json`. Record hits by type.
3. Run it over the free-text fields of `chicago_311.csv`.
4. Find three items it **missed** by reading rows yourself.
5. Improve one pattern and re-run; confirm you did not create false positives.
6. Mask rather than delete, keeping the field analysable.
7. Write the residual risk you would report.

**Reflection questions**

- What did the detector miss, and why is that class hard?
- What did masking cost you analytically?
- Would you certify this file as safe to share? On what basis?

---

# Ch06 — Data for AI: Collection, Quality, and Governance

### Demo 6.1 Profiling Real Data, Warts and All

**Objectives**

By the end of this demo, you will:

- Watch a real dataset fail the six quality dimensions in under ten minutes.

**Introduction**

Chicago 311 is genuine operational data. Your instructor profiles it live and the defects find themselves.

**Where this fits**

- Chapter: **Ch06 Data for AI: Collection, Quality, and Governance**
- Slides: see chapter deck
- Time: **10 minutes**
- Environment: CloudShare VM (JupyterLab)

**Resources**

- `labs/data/chicago_311.csv`

**Steps**

1. Instructor loads the file and prints nulls per column.
2. Shows inconsistent casing and whitespace in a categorical column.
3. Shows duplicate service-request numbers.
4. Shows a date column with impossible values.
5. Names each defect against its dimension.

**Reflection questions**

- Which defect would silently corrupt a model rather than crash it?

---

### DO NOW 6.A Six Dimensions on Ten Rows

**Objectives**

By the end of this activity, you will:

- Apply the six quality dimensions by hand before automating them.

**Introduction**

Ten printed rows with defects planted in them.

**Where this fits**

- Chapter: **Ch06 Data for AI: Collection, Quality, and Governance**
- Slides: see chapter deck
- Time: **8 minutes**
- Environment: Paper — no computer needed

**Resources**

- `labs/data/chicago_311.csv`

**Steps**

1. Mark every defect you can find on the printed extract.
2. Label each with its dimension: accuracy, completeness, consistency, timeliness, validity, uniqueness.
3. Count how many you found; the sheet says how many there are.
4. Compare with a neighbour.

**Reflection questions**

- Which dimension was hardest to judge from ten rows alone?

---

### DO NOW 6.B Propose the Schema

**Objectives**

By the end of this activity, you will:

- Design a collection schema before data exists, with the model's help.

**Introduction**

Your office is about to start collecting something new in a shared sheet. Get the schema right now, not after 400 rows.

**Where this fits**

- Chapter: **Ch06 Data for AI: Collection, Quality, and Governance**
- Slides: see chapter deck
- Time: **10 minutes**
- Environment: CloudShare VM (JupyterLab)
- Prompting spine: rung **P6**

**Resources**

- OpenAI API key — loaded automatically from `.env`; never paste a key into a notebook

**Steps**

1. Describe the collection need to an assistant in two sentences.
2. Ask for a schema: field, type, required, allowed values, one example.
3. Ask it to name the three defects most likely to appear anyway.
4. Compare with the class schema on the whiteboard.

**Reflection questions**

- Which field would you have forgotten?
- Which constraint would have prevented the most defects?

---

### DO NOW 6.C Real, Synthetic, or Neither?

**Objectives**

By the end of this activity, you will:

- Decide when synthetic data is the right — or wrong — answer.

**Introduction**

Six situations. Synthetic data solves some of them and quietly ruins others.

**Where this fits**

- Chapter: **Ch06 Data for AI: Collection, Quality, and Governance**
- Slides: see chapter deck
- Time: **7 minutes**  *(flex — your instructor may skip this)*
- Environment: Paper — no computer needed

**Steps**

1. Mark each **use real / use synthetic / do not use AI here**.
2. For each 'synthetic', say what property must be preserved.
3. Identify the one where synthetic data would hide the very thing you need.
4. Instructor reveals that case.

**Reflection questions**

- What does synthetic data cost you that nobody mentions?

---

### DO NOW 6.D Write the Cleaning Prompt

**Objectives**

By the end of this activity, you will:

- Get a model to normalise messy values reliably and checkably.

**Introduction**

One column, many spellings of the same thing.

**Where this fits**

- Chapter: **Ch06 Data for AI: Collection, Quality, and Governance**
- Slides: see chapter deck
- Time: **10 minutes**
- Environment: CloudShare VM (JupyterLab)

**Resources**

- `labs/data/chicago_311.csv`
- OpenAI API key — loaded automatically from `.env`; never paste a key into a notebook

**Steps**

1. Take 20 raw values from a messy 311 column.
2. Write a prompt that maps them to a **fixed** list of canonical values.
3. Require JSON out, with an `unmapped` list for anything that does not fit.
4. Run it and check every mapping by eye.

**Reflection questions**

- What did it map wrongly but confidently?
- Why does forcing an `unmapped` list matter?

---

### Ex 6.1 Shared-Spreadsheet Data Collection

**Objectives**

By the end of this lab, you will:

- Experience data-quality problems by creating them.
- Connect messy data to the quality attributes from Chapter 6.

**Introduction**

Your instructor shares a link (and QR code) to a shared sheet with a loose schema, e.g., columns: your role · a beverage you drank this week · when · how much. A prepared “messy” sheet is available if the room is offline.

**Where this fits**

- Chapter: **Ch06 Data for AI: Collection, Quality, and Governance**
- Slides: see chapter deck
- Time: **20 minutes**
- Environment: Browser + AI assistant

**Resources**

- `labs/data/ex6.1/beverage_sheet_template.csv`
- `labs/data/ex6.1/beverage_sheet_messy.csv`

**Steps**

1. Each participant adds three rows. Do not coordinate formats.
2. The instructor projects the sheet. As a class, audit it against the six quality attributes: completeness, accuracy, consistency, timeliness, validity, uniqueness.
3. For each defect, name one governance rule (a schema constraint, a controlled vocabulary, a required field) that would have prevented it.

**Reflection questions**

- Which is worse for AI: missing data or inconsistent data? Why?
- Who in an agency should own data quality for a shared dataset?

---

### Lab 6.1 Data Quality Assessment of Chicago 311

**Objectives**

By the end of this lab, you will:

- Assess a real dataset against all six quality dimensions.
- Quantify each defect rather than describing it.
- Produce a go / no-go recommendation with evidence.

**Introduction**

A programme office wants to use 311 data to target service improvements. You have been asked whether the data supports that. Answer with numbers.

**Where this fits**

- Chapter: **Ch06 Data for AI: Collection, Quality, and Governance**
- Slides: see chapter deck
- Time: **30 minutes**
- Environment: CloudShare VM (JupyterLab)

**Resources**

- `labs/data/chicago_311.csv`
- Notebook: `labs/lab_6.1_data_quality.ipynb`

**Steps**

1. Open `lab_6.1_data_quality.ipynb` and load the file.
2. **Completeness:** null rate per column; flag anything above 20%.
3. **Uniqueness:** duplicate `sr_number` count; inspect a duplicate pair.
4. **Consistency:** case and whitespace variants in categorical columns.
5. **Validity:** dates outside a plausible range; closed-before-created rows.
6. **Timeliness:** distribution of `created_date`; how current is it?
7. **Accuracy:** pick one column and say honestly how you would even test it.
8. Build a one-table scorecard: dimension, metric, value, pass/fail.
9. Write a go / no-go recommendation with the two numbers that drive it.

**Reflection questions**

- Which dimension could you *not* assess from the data alone?
- What is the single cheapest fix at the point of collection?
- Would you sign the recommendation you just wrote?

---

### Lab 6.2 GenAI-Assisted Cleaning with Structured Outputs

**Objectives**

By the end of this lab, you will:

- Use a model to normalise messy categorical data at volume.
- Enforce a schema so the output is machine-usable.
- Audit the model's work and measure what it got wrong.

**Introduction**

Lab 6.1 found the defects. Now fix a class of them with GenAI — and then check the fixer, because schema-correct is not the same as correct.

**Where this fits**

- Chapter: **Ch06 Data for AI: Collection, Quality, and Governance**
- Slides: see chapter deck
- Time: **30 minutes**
- Environment: CloudShare VM (JupyterLab)

**Resources**

- `labs/data/chicago_311.csv`
- OpenAI API key — loaded automatically from `.env`; never paste a key into a notebook
- Notebook: `labs/lab_6.2_genai_cleaning.ipynb`

**Steps**

1. Open `lab_6.2_genai_cleaning.ipynb`.
2. Extract 60 raw values from a messy categorical column.
3. Call the model with a **strict JSON schema**: `{raw, canonical, confidence}`.
4. Parse the response; fail loudly if it does not validate.
5. Sample 20 mappings and check them by hand. Record the error rate.
6. Find one high-confidence wrong mapping and explain what misled it.
7. Re-run the failures with a tightened prompt and compare.
8. State the human-review rate you would require in production.

**Reflection questions**

- What error rate would you accept, and who decides?
- Did confidence correlate with correctness?
- Which defects from Lab 6.1 can GenAI *not* fix?

---

# Ch07 — Building with LLMs: APIs, RAG, and Agents

### Demo 7.1 One API Call, Dissected

**Objectives**

By the end of this demo, you will:

- See what the chat box was doing all along.
- Identify roles, tokens, temperature and cost in a single call.

**Introduction**

Your instructor makes one call and stops on every part of it.

**Where this fits**

- Chapter: **Ch07 Building with LLMs: APIs, RAG, and Agents**
- Slides: see chapter deck
- Time: **10 minutes**
- Environment: CloudShare VM (JupyterLab)

**Resources**

- OpenAI API key — loaded automatically from `.env`; never paste a key into a notebook

**Steps**

1. Instructor shows the key arriving from `.env`, never from a cell.
2. Sends a call with a system and a user message; shows the role structure.
3. Prints the full response object: content, finish reason, usage.
4. Re-runs at temperature 0 and 1.2 to show determinism change.
5. Multiplies the token count out to agency scale on the whiteboard.

**Reflection questions**

- Which field would you log for auditability?
- What would temperature 0 buy you in a government workflow?

---

### DO NOW 7.A Hugging Face Tour

**Objectives**

By the end of this activity, you will:

- Navigate the open-model ecosystem and read a model card.

**Introduction**

Not every model is behind an API. Some you can download and run inside your own boundary.

**Where this fits**

- Chapter: **Ch07 Building with LLMs: APIs, RAG, and Agents**
- Slides: see chapter deck
- Time: **10 minutes**  *(flex — your instructor may skip this)*
- Environment: Browser + AI assistant

**Steps**

1. Open huggingface.co and find an open-weight instruction model.
2. Read its model card: licence, size, intended use, limitations.
3. Find one model you could *not* legally deploy at your agency, and say why.
4. Note the download size and what hardware it would need.

**Reflection questions**

- What would make an on-prem model worth the operational cost?

---

### DO NOW 7.B Cost at Agency Scale

**Objectives**

By the end of this activity, you will:

- Turn token counts into a budget line.

**Introduction**

Someone will ask 'what will this cost?'. Be able to answer.

**Where this fits**

- Chapter: **Ch07 Building with LLMs: APIs, RAG, and Agents**
- Slides: see chapter deck
- Time: **8 minutes**
- Environment: CloudShare VM (JupyterLab)

**Resources**

- OpenAI API key — loaded automatically from `.env`; never paste a key into a notebook

**Steps**

1. Run one representative call and record prompt and completion tokens.
2. Multiply out to 1,000, 100,000 and 1,000,000 documents a year.
3. Look up current per-token pricing and compute all three.
4. Compare against the staff hours the task takes today.

**Reflection questions**

- At what volume does the model stop being the expensive part?
- Which assumption in your estimate is weakest?

---

### DO NOW 7.C Prompt as Code

**Objectives**

By the end of this activity, you will:

- Move a prompt from a chat box into a parameterised system message.

**Introduction**

The payoff of the whole prompting spine: the chat box was an API call all along, and now you control every part of it.

**Where this fits**

- Chapter: **Ch07 Building with LLMs: APIs, RAG, and Agents**
- Slides: see chapter deck
- Time: **10 minutes**
- Environment: CloudShare VM (JupyterLab)
- Prompting spine: rung **P7**

**Resources**

- OpenAI API key — loaded automatically from `.env`; never paste a key into a notebook

**Steps**

1. Take your best Prompt Card entry and move it into the `system` message.
2. Send three different user inputs against that one system prompt.
3. Change temperature and observe the variance across repeats.
4. Pin the version that behaves consistently.

**Reflection questions**

- What became easier once the prompt was code?
- What became easier to get wrong?

---

### DO NOW 7.D Where Would RAG Fail?

**Objectives**

By the end of this activity, you will:

- Predict retrieval failure modes before building anything.

**Introduction**

Six questions against the four-document policy corpus you will use in Lab 7.2.

**Where this fits**

- Chapter: **Ch07 Building with LLMs: APIs, RAG, and Agents**
- Slides: see chapter deck
- Time: **8 minutes**  *(flex — your instructor may skip this)*
- Environment: Paper — no computer needed

**Steps**

1. For each question, predict: will retrieval find the answer?
2. Mark the two you expect to fail and say why — wrong chunk, wrong wording, answer spread across documents, or simply absent.
3. Keep the sheet; check your predictions after Lab 7.2.
4. Instructor collects the most common predicted failure.

**Reflection questions**

- Which failure mode would be invisible to the user?

---

### Lab 7.1 First Calls with the OpenAI API

**Objectives**

By the end of this lab, you will:

- Make working chat calls from Python with the current SDK.
- Control behaviour with system prompts and temperature.
- Get structured JSON out of a real government memo and read the cost.

**Introduction**

This replaces the old Lab 6.3, which asked for a personal key and called a retired endpoint. The key now comes from `.env`, and the SDK is current.

**Where this fits**

- Chapter: **Ch07 Building with LLMs: APIs, RAG, and Agents**
- Slides: see chapter deck
- Time: **30 minutes**
- Environment: CloudShare VM (JupyterLab)
- Prompting spine: rung **P7**

**Resources**

- `labs/data/gov_memo.txt`
- OpenAI API key — loaded automatically from `.env`; never paste a key into a notebook
- Notebook: `labs/lab_7.1_openai_api.ipynb`

**Steps**

1. Open `lab_7.1_openai_api.ipynb`. Run the setup cell and confirm it reports the key loaded from `.env` without printing it.
2. Make a first call with a user message only. Print the reply.
3. Add a system message that fixes the register. Re-run and compare.
4. Run the same prompt three times at temperature 0, then at 1.0.
5. Extract `{title, date, decision, owner}` from `gov_memo.txt` as JSON.
6. Parse it in Python; tighten the prompt until it validates every time.
7. Print prompt, completion and total tokens; estimate cost per 1,000 memos.

**Reflection questions**

- What did the system message change that the user message could not?
- Where would temperature 0 still not give you identical output?
- What is the first thing you would log if this ran in production?

---

### Lab 7.2 RAG over Government Documents

**Objectives**

By the end of this lab, you will:

- Build a working retrieval pipeline over real policy documents.
- Force citations and verify them.
- Diagnose retrieval failure rather than blaming the model.

**Introduction**

Four agency policy documents and a question the answer is buried in. This is the pattern behind every 'chat with our documents' pilot.

**Where this fits**

- Chapter: **Ch07 Building with LLMs: APIs, RAG, and Agents**
- Slides: see chapter deck
- Time: **30 minutes**
- Environment: CloudShare VM (JupyterLab)
- Prompting spine: rung **P8**

**Resources**

- `labs/data/corpus/ai_acceptable_use_policy.md`
- `labs/data/corpus/data_governance_standard.md`
- `labs/data/corpus/foia_processing_guidance.md`
- `labs/data/corpus/records_retention_policy.md`
- OpenAI API key — loaded automatically from `.env`; never paste a key into a notebook
- Notebook: `labs/lab_7.2_rag_gov_docs.ipynb`

**Steps**

1. Open `lab_7.2_rag_gov_docs.ipynb`.
2. Load the four corpus documents and chunk them; print chunk count and sizes.
3. Embed the chunks (the notebook falls back to a local embedding offline).
4. Ask a question **without** retrieval and note what the model invents.
5. Retrieve the top 3 chunks and inspect them before generating.
6. Generate with the instruction to answer only from the chunks and quote the sentence used.
7. Check every citation against the source file.
8. Take one of your DO NOW 7.D failure predictions and confirm or refute it.
9. Change chunk size and re-run the failing question.

**Reflection questions**

- Did chunking or prompting fix your failing question?
- How would you detect a wrong citation at scale?
- What would you tell a programme office promised '95% accuracy'?

---

### Lab 7.3 Citizen Services Triage Agent (Capstone)

**Objectives**

By the end of this lab, you will:

- Build an agent that plans, calls tools, and acts under supervision.
- Add guardrails: allow-lists, approval gates, step and spend limits.
- Survive a prompt-injection attempt arriving through a tool result.

**Introduction**

The course capstone. You build a triage agent for a citizen-services queue: it looks up records, masks PII, searches datasets, and drafts a notification — but never sends anything without you.

**Where this fits**

- Chapter: **Ch07 Building with LLMs: APIs, RAG, and Agents**
- Slides: see chapter deck
- Time: **45 minutes**
- Environment: CloudShare VM (JupyterLab)
- Prompting spine: rung **P9**

**Resources**

- `labs/data/citizen_records.json`
- `labs/data/cached_datagov.json`
- `labs/data/chicago_311.csv`
- `labs/data/MANIFEST.json`
- OpenAI API key — loaded automatically from `.env`; never paste a key into a notebook
- Notebook: `labs/lab_7.3_agent.ipynb`

**Steps**

1. **Stage A — tools (15 min).** Open `lab_7.3_agent.ipynb` and read the four provided tools: `search_datasets`, `lookup_citizen_record`, `mask_pii`, `send_status_notification`. Call each directly once.
2. **Stage B — the loop (20 min).** Wire the tools into a function-calling loop. Give it one request and watch it choose. Print every tool call.
3. **Stage C — guardrails (20 min).** Add a tool allow-list, a maximum step count, and an approval gate before `send_status_notification`. Confirm the agent stops and asks.
4. **Stage C2 — injection (10 min).** Run the poisoned dataset description supplied in the notebook. It instructs the agent to exfiltrate a record. Confirm your guardrail holds; if it does not, fix it.
5. **Stage D — instructing the agent (15 min).** Edit the system instructions to change its planning behaviour: make it always mask before drafting. Re-run.
6. **Stage E — your dataset (10 min).** Point `search_datasets` at the dataset you bookmarked in DO NOW 2.D and ask your own question.

**Reflection questions**

- Which guardrail would you consider mandatory before any real deployment?
- Where did the agent make a choice you did not expect?
- What is the difference between prompting a chatbot and instructing an agent?
- Which part of this would your agency's review board question first?

---

# Ch08 — AI Operations and Reporting in Government

### Demo 8.1 Watching a Model Drift

**Objectives**

By the end of this demo, you will:

- See drift in real seasonal data, and see the monitor catch it.

**Introduction**

Wastewater surveillance is strongly seasonal. A model trained in one season degrades in the next — visibly.

**Where this fits**

- Chapter: **Ch08 AI Operations and Reporting in Government**
- Slides: see chapter deck
- Time: **10 minutes**
- Environment: CloudShare VM (JupyterLab)

**Resources**

- `labs/data/cdc_flu_wastewater.csv`

**Steps**

1. Instructor fits a simple model on an early slice of the series.
2. Scores it on a later slice; error rises.
3. Plots the input distribution for both periods side by side.
4. Shows the threshold that would have raised an alert, and when.

**Reflection questions**

- Was this data drift or concept drift?
- Who should receive that alert, and what should they do?

---

### DO NOW 8.A Which Metric Catches This?

**Objectives**

By the end of this activity, you will:

- Match monitoring metrics to the failures they actually detect.

**Introduction**

Six production failures. Each is caught by a different signal — or by none.

**Where this fits**

- Chapter: **Ch08 AI Operations and Reporting in Government**
- Slides: see chapter deck
- Time: **7 minutes**
- Environment: Paper — no computer needed

**Steps**

1. Read the six failure descriptions.
2. Name the metric or monitor that would catch each first.
3. Mark the one that no standard metric catches.
4. Say what you would add to catch it.

**Reflection questions**

- Which failure would reach the public before anyone noticed?

---

### DO NOW 8.B Pilot to Production Readiness

**Objectives**

By the end of this activity, you will:

- Apply a readiness checklist to a pilot that wants to go live.

**Introduction**

A pilot has 'great results' and a sponsor in a hurry.

**Where this fits**

- Chapter: **Ch08 AI Operations and Reporting in Government**
- Slides: see chapter deck
- Time: **8 minutes**  *(flex — your instructor may skip this)*
- Environment: Paper — no computer needed

**Steps**

1. Read the one-page pilot description.
2. Score it against the readiness factors from the chapter.
3. Circle the two gaps you would block on.
4. Write the one sentence you would say to the sponsor.

**Reflection questions**

- Which gap is most often waved through in real life?

---

### DO NOW 8.C Critique This Dashboard

**Objectives**

By the end of this activity, you will:

- Apply visualization guidelines to a deliberately poor chart.

**Introduction**

A dashboard panel that is technically accurate and practically useless.

**Where this fits**

- Chapter: **Ch08 AI Operations and Reporting in Government**
- Slides: see chapter deck
- Time: **7 minutes**
- Environment: Paper — no computer needed

**Steps**

1. List everything wrong with the printed chart.
2. Name the guideline each violation breaks.
3. Sketch the replacement in the workbook margin.
4. State the one question your version answers at a glance.

**Reflection questions**

- Which flaw was misleading rather than merely ugly?

---

### DO NOW 8.D Ask, Then Verify

**Objectives**

By the end of this activity, you will:

- Use an assistant for analysis, then check every number it produced.

**Introduction**

Uploading a CSV and asking for findings is fast. Verifying is the job.

**Where this fits**

- Chapter: **Ch08 AI Operations and Reporting in Government**
- Slides: see chapter deck
- Time: **10 minutes**  *(flex — your instructor may skip this)*
- Environment: CloudShare VM (JupyterLab)

**Resources**

- `labs/data/epa_aqi_by_county.csv`
- OpenAI API key — loaded automatically from `.env`; never paste a key into a notebook

**Steps**

1. Ask an assistant for three findings from `epa_aqi_by_county.csv`.
2. Ask it to show the rows or the computation behind each.
3. Recompute all three yourself in pandas.
4. Record which survived unchanged.

**Reflection questions**

- Which finding was subtly wrong?
- What phrasing made it show its working most usefully?

---

### Lab 8.1 Visualization and Reporting from EPA Data

**Objectives**

By the end of this lab, you will:

- Build charts that answer a stated question.
- Apply the visualization guidelines deliberately.
- Turn three charts into a one-page briefing.

**Introduction**

A deputy director asks: which counties have the worst air quality, is it getting better, and where should we focus? Answer in one page.

**Where this fits**

- Chapter: **Ch08 AI Operations and Reporting in Government**
- Slides: see chapter deck
- Time: **30 minutes**
- Environment: CloudShare VM (JupyterLab)

**Resources**

- `labs/data/epa_aqi_by_county.csv`
- Notebook: `labs/lab_8.1_visualization.ipynb`

**Steps**

1. Open `lab_8.1_visualization.ipynb` and load the EPA file.
2. Rank counties by unhealthy-day count; chart the top 15.
3. Chart the distribution of `Median AQI` across all counties.
4. Chart one state's counties against the national median.
5. Apply the guidelines: sorted bars, labelled axes, no decoration, honest scale.
6. Write a three-sentence finding under each chart.
7. Assemble a one-page briefing: question, three charts, recommendation.

**Reflection questions**

- Which chart would survive being screenshotted without its caption?
- What did sorting change about the reader's conclusion?
- What did you choose *not* to plot, and why?

---

### Lab 8.2 GenAI-Assisted Analysis and Briefing

**Objectives**

By the end of this lab, you will:

- Use GenAI to accelerate analysis without outsourcing judgement.
- Verify every generated figure against the source.
- Produce a briefing you would put your name on.

**Introduction**

Same deliverable as Lab 8.1, but with an assistant. The difference is the verification step, which is now yours.

**Where this fits**

- Chapter: **Ch08 AI Operations and Reporting in Government**
- Slides: see chapter deck
- Time: **30 minutes**  *(flex — your instructor may skip this)*
- Environment: CloudShare VM (JupyterLab)

**Resources**

- `labs/data/epa_aqi_by_county.csv`
- `labs/data/cdc_flu_wastewater.csv`
- OpenAI API key — loaded automatically from `.env`; never paste a key into a notebook
- Notebook: `labs/lab_8.2_genai_reporting.ipynb`

**Steps**

1. Open `lab_8.2_genai_reporting.ipynb`.
2. Send a profile of the EPA data and ask for five candidate findings.
3. Pick the three most decision-relevant.
4. Recompute each in pandas. Mark **confirmed / wrong / unverifiable**.
5. Ask the assistant to draft the briefing using only your confirmed findings.
6. Edit it for accuracy and tone; remove every hedge you cannot support.
7. Note in the notebook which figures you had to correct.

**Reflection questions**

- How many of the five candidate findings survived verification?
- Where did the assistant save you real time?
- What would have happened if you had skipped the recompute step?

---

# Ch09 — Course Summary and Your Agency AI Roadmap

### Demo 9.1 A Prompt, Three Days Apart

**Objectives**

By the end of this demo, you will:

- See the week's progress made concrete on one volunteer's prompt.

**Introduction**

A volunteer's Day-1 baseline card, rewritten live with everything the room has learned.

**Where this fits**

- Chapter: **Ch09 Course Summary and Your Agency AI Roadmap**
- Slides: see chapter deck
- Time: **8 minutes**
- Environment: Browser + AI assistant

**Steps**

1. Volunteer reads their sealed DO NOW 0.2 prompt aloud.
2. Instructor runs it and projects the output.
3. Room rebuilds it: role, context, format, grounding, constraints.
4. Instructor re-runs and both outputs are scored on the rubric.

**Reflection questions**

- Which single change moved the score most?

---

### DO NOW 9.A Rewrite Your Baseline Prompt

**Objectives**

By the end of this activity, you will:

- Close the spine: rewrite your own Day-1 prompt and score both.

**Introduction**

Unseal the card you wrote before any instruction.

**Where this fits**

- Chapter: **Ch09 Course Summary and Your Agency AI Roadmap**
- Slides: see chapter deck
- Time: **10 minutes**
- Environment: Browser + AI assistant
- Prompting spine: rung **P10**

**Steps**

1. Read your original prompt without editing it.
2. Rewrite it using the ladder: role, context, examples, format, grounding.
3. Run both. Score both on the rubric.
4. Record the delta on your Prompt Card.

**Reflection questions**

- Which rung of the ladder did you use without thinking about it?
- What would you still not trust this output to do?

---

### DO NOW 9.B Pick Your First Use Case

**Objectives**

By the end of this activity, you will:

- Choose one realistic starting point from your own work.

**Introduction**

Not the most exciting idea — the one you could actually start in 30 days.

**Where this fits**

- Chapter: **Ch09 Course Summary and Your Agency AI Roadmap**
- Slides: see chapter deck
- Time: **8 minutes**
- Environment: Paper — no computer needed

**Resources**

- `labs/data/federal_ai_use_cases.csv`

**Steps**

1. List three candidate tasks from your own job.
2. Score each on impact, feasibility and risk, 1-5.
3. Search the federal inventory for anyone already doing it.
4. Circle the one you will take into Lab 9.1.

**Reflection questions**

- Did finding a precedent change your confidence?

---

### DO NOW 9.C Name Your Guardrail

**Objectives**

By the end of this activity, you will:

- Attach a concrete control to your chosen use case.

**Introduction**

Every use case needs the one control that makes it safe enough to start.

**Where this fits**

- Chapter: **Ch09 Course Summary and Your Agency AI Roadmap**
- Slides: see chapter deck
- Time: **7 minutes**
- Environment: Paper — no computer needed

**Steps**

1. Write your use case in one sentence.
2. Name the single failure that would matter most.
3. Write the guardrail that prevents it — human gate, allow-list, data rule, log.
4. Say who owns that guardrail.

**Reflection questions**

- Would your guardrail survive a busy Friday afternoon?

---

### DO NOW 9.D Who Do You Need?

**Objectives**

By the end of this activity, you will:

- Identify the governance cast your use case has to pass through.

**Introduction**

Nothing ships alone. Map the people before you need them.

**Where this fits**

- Chapter: **Ch09 Course Summary and Your Agency AI Roadmap**
- Slides: see chapter deck
- Time: **7 minutes**  *(flex — your instructor may skip this)*
- Environment: Paper — no computer needed

**Steps**

1. List the roles your use case must clear: CAIO, privacy, security, records, programme owner.
2. Mark which you have already met.
3. Write the one question you would ask each.
4. Identify the one whose 'no' would end it.

**Reflection questions**

- Who did you forget the first time?

---

### Lab 9.1 Your 90-Day Agency AI Roadmap

**Objectives**

By the end of this lab, you will:

- Turn the week into a dated, specific 30/60/90 plan.
- Ground it in a real precedent from the federal inventory.
- Leave with a one-page brief you can hand to your manager.

**Introduction**

The course deliverable. One page your manager can read in two minutes and act on — problem, approach, data, guardrails, first step.

**Where this fits**

- Chapter: **Ch09 Course Summary and Your Agency AI Roadmap**
- Slides: see chapter deck
- Time: **30 minutes**
- Environment: Browser + AI assistant
- Prompting spine: rung **P10**

**Resources**

- `labs/data/federal_ai_use_cases.csv`
- OpenAI API key — loaded automatically from `.env`; never paste a key into a notebook

**Steps**

1. Start from the use case you circled in DO NOW 9.B.
2. Find one precedent in `federal_ai_use_cases.csv` and note the agency.
3. **Days 1-30:** define the problem, confirm the data exists, name the owner.
4. **Days 31-60:** prototype with the guardrail from DO NOW 9.C.
5. **Days 61-90:** evaluate against the rubric, document, brief the decision-maker.
6. Use your Prompt Card template to draft the one-pager with an assistant.
7. Edit every claim you cannot support. Delete every sentence you would not say aloud to your CIO.
8. Share the first line with the room.

**Reflection questions**

- What is the first thing you will do on Monday?
- Which part of your plan is most likely to slip, and what would you do?
- What did you leave out on purpose?

---
