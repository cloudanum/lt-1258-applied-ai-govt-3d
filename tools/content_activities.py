"""Single source of truth for every 1258 activity, demo and lab (rev a4).

The registry contract is `id == workbook heading == slide callout == handout
section`. Nothing enforced it before, so ids drifted. Here the id is written
once and the registry, the lab manual and the slide callouts are all *generated*
from this file — drift becomes impossible rather than merely discouraged.

Shape per chapter: **1 demo + 4 activities/Do Nows + 1-2 labs.**
Ch07 carries three labs because the agent capstone is the course deliverable
and cannot be folded into the API or RAG lab.

Field notes
-----------
kind        demo | donow | lab
env         vm (Jupyter on CloudShare) | browser (assistant) | paper | none
needs_key   True when the activity calls the OpenAI API (key comes from .env)
data        files under labs/data/ the activity uses
spine       prompting-spine rung (P0-P10), or None
flex        True when the IG may cut it for time
objectives  the LT "By the end of this ... you will:" list
scenario    the LT Introduction/Scenario paragraph
steps       numbered LT Steps
reflection  LT Reflection questions
"""

# --------------------------------------------------------------------------- #
# Ch00 — Course Launch
# --------------------------------------------------------------------------- #
CH00 = [
    dict(id="Demo 0.1", kind="demo", title="Your Lab Environment, End to End",
         chapter="Ch00", env="vm", minutes=10, needs_key=True, data=[], spine=None, flex=False,
         objectives=["Watch the full path from My Learning Tree to a running notebook.",
                     "See where the class OpenAI key lives and how a notebook reads it."],
         scenario="Before anyone touches a keyboard, your instructor walks the whole "
                  "environment once so you know what 'working' looks like.",
         steps=["Instructor launches the VM and opens the in-browser Viewer (never RDP).",
                "Instructor opens JupyterLab and shows the `labs/` file tree.",
                "Instructor shows `.env` beside `labs/`, with the key masked, and explains "
                "that notebooks read it through `lab_common.load_dotenv()` — you never paste "
                "a key into a cell.",
                "Instructor runs `lab_0.1_healthcheck.ipynb` and narrates the four checks."],
         reflection=["Where does the key live, and why not in the notebook?",
                     "Which check would fail first if the network were down?"]),

    dict(id="DO NOW 0.1", kind="donow", title="Environment Healthcheck",
         chapter="Ch00", env="vm", minutes=15, needs_key=True,
         data=["MANIFEST.json"], spine=None, flex=False,
         objectives=["Reach a running JupyterLab in your CloudShare VM.",
                     "Prove packages, data files, the API key and network are all ready."],
         scenario="Nothing else in the week works until this is green, so it is the first "
                  "thing you do.",
         steps=["Sign in to **My Learning Tree**, open the course page, click **Launch Lab**.",
                "Click the **in-browser Viewer**. Do not use the RDP button — it errors.",
                "Firefox opens JupyterLab automatically; if not, double-click **Start Labs** "
                "(password `pw` if asked).",
                "Open `lab_0.1_healthcheck.ipynb` and choose **Run -> Run All Cells**.",
                "Confirm checks 1-3 read **PASS**. Check 4 (network) is informational — a "
                "cached copy of every dataset ships on the VM."],
         reflection=["Which check proves the OpenAI key is readable from `.env`?",
                     "If check 2 failed, what would you look at first?"]),

    dict(id="DO NOW 0.2", kind="donow", title="Your First Prompt (Baseline Card)",
         chapter="Ch00", env="browser", minutes=5, needs_key=False, data=[], spine="P0", flex=False,
         objectives=["Capture how you prompt *before* any instruction, as your own baseline."],
         scenario="Think of one real task from your own job you would hand to an AI "
                  "assistant. Write the prompt exactly as you would type it today.",
         steps=["Write the prompt on the card in your workbook — no editing, no help.",
                "Do not score it and do not show it to the room.",
                "Post it to the class whiteboard face-down, or seal it in your workbook.",
                "You will reopen this on Day 3 at DO NOW 9.A and rewrite it."],
         reflection=["What did you assume the model already knew?"]),

    dict(id="DO NOW 0.3", kind="donow", title="Which Account, Which Data?",
         chapter="Ch00", env="paper", minutes=8, needs_key=False, data=[], spine=None, flex=False,
         objectives=["Apply the course data rule before the first lab touches an assistant."],
         scenario="Six one-line scenarios. For each, decide which tool you may use and "
                  "whether the data may go into it at all.",
         steps=["Read each scenario on the workbook page.",
                "Mark each: **class account / agency approved tool / neither**.",
                "Mark the data: **public - synthetic - never paste**.",
                "Compare with your neighbour; your instructor takes the two that split the room."],
         reflection=["Which scenario was hardest, and what made it hard?",
                     "What would you need to know about a tool before pasting anything into it?"]),

    dict(id="DO NOW 0.4", kind="donow", title="AI Already in Your Day",
         chapter="Ch00", env="paper", minutes=7, needs_key=False, data=[], spine=None, flex=True,
         objectives=["Map where the room is starting from, and seed the Day-3 roadmap."],
         scenario="Round the room: one place AI already touches your work, or one task you "
                  "wish it would take off your hands.",
         steps=["Name, agency, role.",
                "One AI tool you have used, or one task you wish AI could do.",
                "Instructor captures the wish list on the whiteboard.",
                "The board stays up all week and is reused at Lab 9.1."],
         reflection=["Whose example surprised you?"]),

    dict(id="Lab 0.1", kind="lab", title="Course Environment and Data Tour",
         chapter="Ch00", env="vm", minutes=20, needs_key=True,
         data=["MANIFEST.json", "federal_ai_use_cases.csv", "chicago_311.csv"],
         spine=None, flex=False,
         objectives=["Navigate JupyterLab confidently: cells, run order, kernel restart.",
                     "Confirm the six shipped datasets load, and know what each one is for.",
                     "Make one successful call to the OpenAI API using the key from `.env`."],
         scenario="You have a working VM. Before the course leans on it, take ten minutes "
                  "to learn the room: where the notebooks are, where the data is, and how a "
                  "notebook reaches the model.",
         steps=["Open `lab_0.1_environment_tour.ipynb`.",
                "Run the **environment** cell. Confirm it prints the `.env` path it loaded and "
                "the model alias — but never the key itself.",
                "Run the **data inventory** cell. It reads `labs/data/MANIFEST.json` and prints "
                "each dataset with its row count and one-line description.",
                "Load `federal_ai_use_cases.csv` with pandas. Print `.shape` and `.columns`.",
                "Answer in the notebook: how many use cases are flagged `is_high_impact`?",
                "Load `chicago_311.csv` and print the five most common `sr_type` values.",
                "Run the **first API call** cell: a one-sentence prompt, printing the reply and "
                "the token counts.",
                "Deliberately break something: restart the kernel, then re-run only the last "
                "cell and read the error. Then **Run All** to recover."],
         reflection=["Why did the last cell fail after a kernel restart?",
                     "Which of the six datasets would you reach for to answer 'which agencies "
                     "use AI for document processing?'",
                     "What did the token counts suggest about cost at agency scale?"]),
]

# --------------------------------------------------------------------------- #
# Ch01 — AI & ML Foundations
# --------------------------------------------------------------------------- #
CH01 = [
    dict(id="Demo 1.1", kind="demo", title="Supervised, Unsupervised, Generative — One Dataset",
         chapter="Ch01", env="vm", minutes=10, needs_key=True,
         data=["epa_aqi_by_county.csv"], spine=None, flex=False,
         objectives=["See all three families of AI applied to the same federal dataset.",
                     "Understand what changes between them: the label, the goal, the output."],
         scenario="One EPA table, three questions. Your instructor runs each in turn so the "
                  "difference is concrete rather than definitional.",
         steps=["**Supervised:** predict a county's `Max AQI` from its day counts — there is a "
                "right answer to learn from.",
                "**Unsupervised:** cluster counties by air-quality profile — no labels, the "
                "structure is discovered.",
                "**Generative:** ask the model to write the county's air-quality summary in "
                "plain English for a public webpage.",
                "Instructor names what changed each time: the label, the goal, the output type."],
         reflection=["Which of the three needed labelled data, and why does that matter for cost?",
                     "Which one could you not verify by looking at the data alone?"]),

    dict(id="DO NOW 1.A", kind="donow", title="Explain It to a CIO, Then to a Citizen",
         chapter="Ch01", env="browser", minutes=10, needs_key=False, data=[], spine="P1", flex=True,
         objectives=["Use role and audience framing to change an explanation's register."],
         scenario="Same fact, two audiences. This is the first rung of the prompting spine.",
         steps=["Ask an assistant to explain **random forests to a CIO deciding on funding**.",
                "Ask it again for **a citizen reading an agency FAQ**.",
                "Underline the three biggest differences between the two answers.",
                "Post the better opening line to the whiteboard."],
         reflection=["Which framing worked better, and what exactly in your prompt caused it?"]),

    dict(id="DO NOW 1.B", kind="donow", title="Classic ML or GenAI?",
         chapter="Ch01", env="paper", minutes=7, needs_key=False, data=[], spine=None, flex=False,
         objectives=["Choose the right tool class for a task before choosing a product."],
         scenario="Eight real agency tasks. For each, decide whether classic ML, generative "
                  "AI, or neither is the right instrument.",
         steps=["Read the eight tasks on the workbook page.",
                "Mark each **ML / GenAI / neither**, and add one word of justification.",
                "Compare with a neighbour; argue any you disagree on.",
                "Instructor resolves the three designed to be genuinely ambiguous."],
         reflection=["Which tasks were ambiguous, and what extra fact would settle them?",
                     "Which ones would be cheaper *without* AI at all?"]),

    dict(id="DO NOW 1.C", kind="donow", title="Prompt It or Train It?",
         chapter="Ch01", env="browser", minutes=10, needs_key=True,
         data=["chicago_311.csv"], spine=None, flex=True,
         objectives=["Feel the difference between prompting a general model and training a "
                     "specific one, on the same classification problem."],
         scenario="Chicago 311 requests carry a `sr_type` label. That is a classification "
                  "problem you could train — or just describe.",
         steps=["Take ten `sr_type` values from `chicago_311.csv`.",
                "Ask an assistant to classify five unlabelled request descriptions into those "
                "categories, with no examples.",
                "Compare its answers with the real labels.",
                "Discuss: how many labelled rows would you need to train a classifier to match?"],
         reflection=["When is 'just prompt it' the right engineering answer?",
                     "What would make you switch to training a model?"]),

    dict(id="DO NOW 1.D", kind="donow", title="Find Your Agency in the Inventory",
         chapter="Ch01", env="vm", minutes=8, needs_key=False,
         data=["federal_ai_use_cases.csv"], spine=None, flex=False,
         objectives=["Locate real, published AI use cases from your own organisation."],
         scenario="Every agency publishes its AI use cases annually under OMB M-25-21. Yours "
                  "is in the file on your VM.",
         steps=["Open `federal_ai_use_cases.csv` in a notebook or spreadsheet.",
                "Filter `agency_name` to your agency, or the closest one to your work.",
                "Read three `use_case_name` and `problem_solved` entries.",
                "Note one you did not know existed."],
         reflection=["Did anything surprise you about what your agency has already deployed?",
                     "How many of your agency's use cases are flagged high-impact?"]),

    dict(id="Lab 1.1", kind="lab", title="Exploring the Federal AI Use Case Inventory",
         chapter="Ch01", env="vm", minutes=30, needs_key=False,
         data=["federal_ai_use_cases.csv", "federal_ai_cots.csv"], spine=None, flex=False,
         objectives=["Load, filter, group and summarise a real federal dataset with pandas.",
                     "Answer substantive questions about federal AI adoption from evidence.",
                     "Practise the analysis habits every later lab depends on."],
         scenario="You have been asked to brief your CIO on what other agencies are actually "
                  "doing with AI. The OMB inventory is public and sitting on your VM. No AI "
                  "is needed for this lab — this is the data literacy underneath it.",
         steps=["Open `lab_1.1_ai_inventory.ipynb` and run the setup cell.",
                "Print the shape and columns. How many use cases, how many agencies?",
                "Group by `agency_name` and produce the top 10 agencies by use-case count.",
                "Group by `development_stage`. What share is actually in production?",
                "Filter `is_high_impact`. Which agencies report the most high-impact AI?",
                "Cross-tabulate `topic_area` against `development_stage` and read one row aloud.",
                "Join the COTS file. Which commercial tools appear most often?",
                "Write three findings in the notebook, each with the line of code that "
                "produced it."],
         reflection=["Which single number would most change your CIO's mind?",
                     "What does this dataset *not* tell you about how well any of it works?",
                     "Where would a chart have been clearer than a table?"]),

    dict(id="Lab 1.2", kind="lab", title="Clustering Counties by Air Quality (K-Means)",
         chapter="Ch01", env="vm", minutes=30, needs_key=False,
         data=["epa_aqi_by_county.csv"], spine=None, flex=True,
         objectives=["Run K-Means on a real EPA dataset and interpret the clusters.",
                     "Choose k deliberately rather than by default.",
                     "Explain an unsupervised result to a non-technical stakeholder."],
         scenario="EPA publishes an annual air-quality summary for every county. Nobody has "
                  "labelled them. You want to find the natural groupings so a programme "
                  "office can target outreach.",
         steps=["Open `lab_1.2_clustering.ipynb` and load `epa_aqi_by_county.csv`.",
                "Select the numeric day-count columns and scale them.",
                "Fit K-Means with k=3. Print each cluster's size and column means.",
                "Name each cluster in plain English from those means.",
                "Sweep k from 2 to 8, plot inertia, and choose a k you can defend.",
                "List the counties in the worst cluster and sanity-check against the raw rows.",
                "Write two sentences a programme director could act on."],
         reflection=["What changed when you changed k?",
                     "Why did scaling matter here?",
                     "What would you tell someone who asked 'is this cluster correct?'"]),
]

# --------------------------------------------------------------------------- #
# Ch02 — Applications Across Government & Public Data
# --------------------------------------------------------------------------- #
CH02 = [
    dict(id="Demo 2.1", kind="demo", title="Finding Government Data in 2026",
         chapter="Ch02", env="browser", minutes=10, needs_key=False,
         data=["MANIFEST.json"], spine=None, flex=False,
         objectives=["See how federal data is actually located now that data.gov's API is gone.",
                     "Learn the agency-portal route the labs rely on."],
         scenario="data.gov retired its CKAN Action API in 2026 and the rebuilt catalogue "
                  "exposes no JSON API at all. Your instructor shows what still works.",
         steps=["Search catalog.data.gov in the browser for 'air quality'.",
                "Follow one result through to the hosting agency portal.",
                "Show the Socrata pattern: `/resource/<id>.csv?$limit=...`.",
                "Show `labs/data/MANIFEST.json` — the same datasets, already downloaded, with "
                "their source URLs recorded."],
         reflection=["Why does an offline copy matter for a classroom?",
                     "How would you cite one of these datasets in an agency brief?"]),

    dict(id="DO NOW 2.A", kind="donow", title="Ask for Datasets, Then Verify",
         chapter="Ch02", env="browser", minutes=10, needs_key=False, data=[], spine="P2", flex=False,
         objectives=["Experience model fabrication on a checkable claim, early and safely."],
         scenario="You need three datasets for a stated need. Ask an assistant, then check "
                  "every one. At least one will not exist.",
         steps=["Ask an assistant for **three data.gov datasets** relevant to a need you name.",
                "For each, search catalog.data.gov and record: found / not found / different.",
                "Mark which were real, which were plausible-but-wrong.",
                "Introduce the rubric: accuracy, completeness, format, tone. Score the answer."],
         reflection=["What did the fabricated one have in common with the real ones?",
                     "What prompt change would have reduced the risk?"]),

    dict(id="DO NOW 2.B", kind="donow", title="Source That Claim",
         chapter="Ch02", env="browser", minutes=8, needs_key=False, data=[], spine=None, flex=True,
         objectives=["Practise tracing a confident statistic back to a primary source."],
         scenario="Five AI-in-government claims of the kind that circulate in slide decks. "
                  "Some are real, some are not.",
         steps=["Read the five claims on the workbook page.",
                "For each, spend 90 seconds trying to find a primary source.",
                "Mark **sourced / unsourceable**, and name the source where you found one.",
                "Instructor reveals which two have no traceable origin."],
         reflection=["What made the unsourceable ones believable?",
                     "What is the cost of one of these reaching a public briefing?"]),

    dict(id="DO NOW 2.C", kind="donow", title="Which Pattern Is This?",
         chapter="Ch02", env="paper", minutes=7, needs_key=False,
         data=["federal_ai_use_cases.csv"], spine=None, flex=False,
         objectives=["Recognise the small number of repeating patterns behind most gov AI."],
         scenario="Six real use cases pulled from the federal inventory. Each is an instance "
                  "of a pattern you have now seen.",
         steps=["Read the six `use_case_name` / `problem_solved` pairs.",
                "Label each: early warning, document processing, triage, forecasting, "
                "anomaly detection, or content generation.",
                "Find one more example of your assigned pattern in the CSV.",
                "Report the pattern, not the product."],
         reflection=["Which pattern appears most often across the inventory?",
                     "Which pattern would be easiest to start in your own office?"]),

    dict(id="DO NOW 2.D", kind="donow", title="Bookmark a Dataset for Day 3",
         chapter="Ch02", env="vm", minutes=5, needs_key=False,
         data=["MANIFEST.json"], spine=None, flex=False,
         objectives=["Choose the dataset you will hand to an agent on Day 3."],
         scenario="Lab 7.3 builds an agent that answers questions about a dataset. Pick yours now.",
         steps=["Open `labs/data/MANIFEST.json` and read all six descriptions.",
                "Pick the one closest to your own work.",
                "Write its filename and one question you want answered about it on your card.",
                "Keep the card — Lab 7.3 uses it."],
         reflection=["Why that dataset?"]),

    dict(id="Lab 2.1", kind="lab", title="Public Data Expedition — Profile an Agency Dataset",
         chapter="Ch02", env="vm", minutes=30, needs_key=False,
         data=["cdc_flu_wastewater.csv", "nyc_air_quality.csv", "chicago_311.csv"],
         spine=None, flex=False,
         objectives=["Profile an unfamiliar public dataset from scratch.",
                     "Read metadata critically and state what the data cannot answer.",
                     "Produce a one-paragraph dataset briefing another analyst could use."],
         scenario="A programme office hands you a dataset and asks 'can we use this?'. That "
                  "question is answered by profiling, not by opinion. You will do it three "
                  "times, quickly, on three real datasets.",
         steps=["Open `lab_2.1_data_expedition.ipynb`.",
                "For **each** of the three datasets: load it and print shape, columns, dtypes.",
                "Report per column: null count, distinct count, and an example value.",
                "Identify the grain — what does one row actually represent?",
                "Identify the time column and print the date range.",
                "Name one question the dataset answers well and one it cannot answer.",
                "Write a four-sentence briefing for the CDC wastewater file, including its "
                "grain, coverage, and one caveat."],
         reflection=["Which dataset was hardest to establish a grain for?",
                     "What would you ask the data owner before using any of these in a decision?",
                     "The Ch02 slides describe wastewater surveillance as an early-warning "
                     "system. Does this file support that claim on its own?"]),
]

# --------------------------------------------------------------------------- #
# Ch03 — Desktop GenAI
# --------------------------------------------------------------------------- #
CH03 = [
    dict(id="Demo 3.1", kind="demo", title="Four Assistants, One Task",
         chapter="Ch03", env="browser", minutes=10, needs_key=False,
         data=["gov_memo.txt"], spine=None, flex=False,
         objectives=["See the same government task run against different assistants.",
                     "Notice that prompt quality moves the answer more than brand does."],
         scenario="Your instructor gives one identical prompt to the assistants available in "
                  "the room and projects the answers side by side.",
         steps=["Instructor pastes the same summarise-this-memo prompt into each assistant.",
                "Room calls out differences in structure, length, hedging and tone.",
                "Instructor improves the prompt once and re-runs the weakest performer.",
                "Room compares the improvement against the gap between products."],
         reflection=["Did the prompt change or the product change do more for quality?",
                     "Which differences would actually matter in your work?"]),

    dict(id="DO NOW 3.A", kind="donow", title="Summarize for a Named Reader",
         chapter="Ch03", env="browser", minutes=8, needs_key=False,
         data=["gov_memo.txt"], spine="P3", flex=False,
         objectives=["Run the summarisation pattern and score it against the rubric."],
         scenario="A two-page agency memo, and two very different readers.",
         steps=["Summarise `gov_memo.txt` in five bullets **for a programme manager**.",
                "Re-run it **for a congressional staffer with two minutes**.",
                "Score both on the rubric: accuracy, completeness, format, tone.",
                "Keep the better prompt on your Prompt Card."],
         reflection=["Which rubric dimension moved most between the two?"]),

    dict(id="DO NOW 3.B", kind="donow", title="Text to Diagram",
         chapter="Ch03", env="browser", minutes=8, needs_key=False,
         data=["corpus/foia_processing_guidance.md"], spine=None, flex=False,
         objectives=["Turn prose into a diagram you can paste into a document."],
         scenario="The FOIA processing guidance describes a workflow in paragraphs. Nobody "
                  "reads paragraphs.",
         steps=["Paste the FOIA guidance into an assistant.",
                "Ask for a **Mermaid flowchart** of the process, and nothing else.",
                "Paste the result into a Mermaid preview and check every branch.",
                "Fix one thing the model got wrong by editing your prompt, not the diagram."],
         reflection=["What did the model invent that the source did not say?"]),

    dict(id="DO NOW 3.C", kind="donow", title="Can I Paste This?",
         chapter="Ch03", env="paper", minutes=10, needs_key=False, data=[], spine=None, flex=False,
         objectives=["Build the reflex the data rule depends on."],
         scenario="Six realistic items land on your desk. For each, decide what may go where.",
         steps=["Sort each item into **share / redact first / never**.",
                "Then repeat per tool tier: public chatbot, enterprise Copilot, on-prem.",
                "Draft the redaction prompt for the one item you marked 'redact first'.",
                "Instructor runs the room's best redaction prompt on a synthetic memo."],
         reflection=["Which item changed category between tool tiers, and why?"]),

    dict(id="DO NOW 3.D", kind="donow", title="Shadow AI Inventory",
         chapter="Ch03", env="paper", minutes=7, needs_key=False, data=[], spine=None, flex=True,
         objectives=["Surface unapproved tool use as a problem to manage, not to punish."],
         scenario="Shadow AI is what staff reach for when the approved path is slower.",
         steps=["List, anonymously, AI tools you have seen used for work.",
                "Mark each **approved / unknown / definitely not approved**.",
                "For one 'not approved', name the legitimate need behind it.",
                "Propose the approved path that would win."],
         reflection=["What would make the approved tool the easier choice?"]),

    dict(id="Lab 3.1", kind="lab", title="Desktop GenAI Task Relay",
         chapter="Ch03", env="browser", minutes=30, needs_key=False,
         data=["gov_memo.txt", "corpus/ai_acceptable_use_policy.md", "citizen_records.json"],
         spine="P3", flex=False,
         objectives=["Run the five everyday desktop-GenAI patterns on real agency material.",
                     "Score every output against the shared rubric.",
                     "Leave with five prompts you will reuse on Monday."],
         scenario="This is the 'what you actually do Monday' lab. Five timed micro-tasks, "
                  "each a pattern you will use every week. Public and synthetic material only.",
         steps=["**Research and explain** — ask for a plain-English explanation of a term from "
                "the acceptable-use policy, for a named audience. (7 min)",
                "**Summarize** — five bullets from `gov_memo.txt` for a programme manager. (7 min)",
                "**Draft and rewrite** — draft a citizen reply from one synthetic record, then "
                "rewrite it two reading levels lower. (10 min)",
                "**Diagram** — a Mermaid flowchart of the memo's approval chain. (7 min)",
                "**Troubleshoot** — paste the broken snippet from your workbook and ask for the "
                "fix *and the reason*. (7 min)",
                "Score all five on the rubric and copy your two best prompts onto your Prompt "
                "Card. (7 min)"],
         reflection=["Which pattern will you use first, and on what?",
                     "Where did the assistant sound confident and be wrong?",
                     "Which task would you never delegate without review?"]),
]

# --------------------------------------------------------------------------- #
# Ch04 — Modern GenAI & Prompt Engineering
# --------------------------------------------------------------------------- #
CH04 = [
    dict(id="Demo 4.1", kind="demo", title="Zero-Shot, Few-Shot, Reasoning — Same Task",
         chapter="Ch04", env="vm", minutes=10, needs_key=True,
         data=["chicago_311.csv"], spine=None, flex=False,
         objectives=["See what each prompting technique is actually worth on one task.",
                     "See where a reasoning model makes manual chain-of-thought redundant."],
         scenario="One classification task, three techniques, run live so the differences "
                  "are measured rather than asserted.",
         steps=["Instructor classifies ten 311 descriptions **zero-shot** and counts errors.",
                "Adds **three examples** and re-runs. Counts errors again.",
                "Asks the model to **think step by step**, then runs the same task on a "
                "**reasoning model** with no such instruction.",
                "Room compares accuracy against tokens and latency."],
         reflection=["Which step bought the most accuracy per token?",
                     "When is 'think step by step' now redundant?"]),

    dict(id="DO NOW 4.A", kind="donow", title="Add Two Examples",
         chapter="Ch04", env="vm", minutes=10, needs_key=True,
         data=["chicago_311.csv"], spine=None, flex=False,
         objectives=["Measure the effect of few-shot examples on your own task."],
         scenario="Few-shot prompting is the cheapest accuracy you can buy — when the "
                  "examples are representative.",
         steps=["Classify five 311 descriptions zero-shot into `sr_type` categories.",
                "Record how many match the real label.",
                "Add two well-chosen examples to the prompt and re-run.",
                "Record again. Then add two *badly chosen* examples and re-run."],
         reflection=["What did the bad examples do to the output?",
                     "How would you choose examples for a task with 40 categories?"]),

    dict(id="DO NOW 4.B", kind="donow", title="Give the Model a Job",
         chapter="Ch04", env="browser", minutes=8, needs_key=False,
         data=["corpus/foia_processing_guidance.md"], spine=None, flex=False,
         objectives=["Use role prompting to change what the model attends to."],
         scenario="Same document, three roles.",
         steps=["Ask about the FOIA guidance as **a FOIA officer**.",
                "Then as **a requester**. Then as **an agency attorney**.",
                "Note what each role surfaced that the others missed.",
                "Keep the most useful role line on your Prompt Card."],
         reflection=["Did the role change the facts, or only the emphasis? How would you check?"]),

    dict(id="DO NOW 4.C", kind="donow", title="Ask for the Shape You Need",
         chapter="Ch04", env="vm", minutes=10, needs_key=True,
         data=["citizen_records.json"], spine=None, flex=False,
         objectives=["Get output you can use directly, not output you must retype."],
         scenario="Prose is a bad interface between a model and a spreadsheet.",
         steps=["Ask for three synthetic citizen records extracted as **prose**.",
                "Re-ask for a **JSON array with a named schema and required fields**.",
                "Parse the JSON in Python. Fix any failure by tightening the prompt.",
                "Re-run twice and confirm the shape is stable."],
         reflection=["What in your prompt made the shape reliable?",
                     "Schema-correct is not the same as correct — what would you still check?"]),

    dict(id="DO NOW 4.D", kind="donow", title="Answer Only From This Document",
         chapter="Ch04", env="browser", minutes=8, needs_key=False,
         data=["corpus/records_retention_policy.md"], spine=None, flex=False,
         objectives=["Constrain a model to a source — the manual ancestor of RAG."],
         scenario="Grounding is a prompt instruction before it is an architecture.",
         steps=["Paste the retention policy and ask a question it **does** answer.",
                "Ask one it **does not** answer, with no grounding instruction.",
                "Re-ask with: *answer only from the text; if it is not there, say 'not stated'; "
                "quote the sentence you used*.",
                "Compare the two failures."],
         reflection=["Did the grounding instruction stop the invention entirely?",
                     "What does this predict about how RAG will behave on Day 3?"]),

    dict(id="Lab 4.1", kind="lab", title="Prompt Engineering Studio",
         chapter="Ch04", env="vm", minutes=30, needs_key=True,
         data=["gov_memo.txt", "chicago_311.csv", "corpus/ai_acceptable_use_policy.md"],
         spine="P4", flex=False,
         objectives=["Apply the seven prompt patterns to real government material.",
                     "Score every output against the rubric and improve the weakest.",
                     "Leave with a personal, tested prompt library."],
         scenario="This is the consolidation lab. You have already climbed rungs P0-P3, so "
                  "the ladder here names skills you have been using since Day 1.",
         steps=["Open `lab_4.1_prompt_studio.ipynb`.",
                "**Zero-shot:** summarise the GAO-style excerpt. Score it. (5 min)",
                "**Few-shot:** add two exemplars to a 311 classification. Score it. (5 min)",
                "**Reasoning:** run the hardest item on a reasoning model, no CoT instruction. (5 min)",
                "**Iterate:** take your worst output and improve it in three rounds, keeping "
                "each version. (6 min)",
                "**Role:** 'You are a FOIA officer...' on the acceptable-use policy. (5 min)",
                "**Structured output:** extract entities from a press release into a table. (6 min)",
                "**Grounding:** answer only from the policy, with the quoted sentence. (6 min)",
                "Copy your best prompt from each pattern onto your Prompt Card. (7 min)"],
         reflection=["Which pattern gave the biggest jump in rubric score?",
                     "Which of your three iteration rounds actually helped, and why?",
                     "Which prompt would you hand to a colleague unchanged?"]),

    dict(id="Lab 4.2", kind="lab", title="Build a Reusable Prompt Template Library",
         chapter="Ch04", env="vm", minutes=30, needs_key=True,
         data=["federal_ai_use_cases.csv"], spine=None, flex=True,
         objectives=["Turn one-off prompts into parameterised templates.",
                     "Test a template against inputs it was not written for.",
                     "Ship something your team can adopt."],
         scenario="A prompt that works once is a trick. A template that works on inputs you "
                  "have not seen is a tool.",
         steps=["Open `lab_4.2_prompt_templates.ipynb`.",
                "Take your best prompt from Lab 4.1 and replace the specifics with "
                "`[BRACKETED]` slots.",
                "Write it as a Python function taking those slots as arguments.",
                "Run it over five different rows of `federal_ai_use_cases.csv`.",
                "Find the input that breaks it and fix the template, not the input.",
                "Add a second template for a different pattern and test it the same way.",
                "Export both to `my_prompt_library.md`."],
         reflection=["What broke first when the input varied?",
                     "Which slot turned out to matter most?",
                     "What would you need to add before handing this to your team?"]),
]

# --------------------------------------------------------------------------- #
# Ch05 — AI Security, Risks & Responsible AI
# --------------------------------------------------------------------------- #
CH05 = [
    dict(id="Demo 5.1", kind="demo", title="Prompt Injection, Live",
         chapter="Ch05", env="vm", minutes=10, needs_key=True,
         data=["corpus/data_governance_standard.md"], spine=None, flex=False,
         objectives=["Watch a guarded system prompt fall over.",
                     "See why injection through a *tool result* is the harder problem."],
         scenario="Your instructor runs a small assistant with a system prompt that forbids "
                  "revealing an internal note, then defeats it.",
         steps=["Instructor shows the system prompt and the guard it contains.",
                "Room suggests attacks; instructor runs them until one lands.",
                "Instructor then hides the same attack inside a *document* the assistant "
                "retrieves — the indirect case.",
                "Instructor shows which defences would have stopped each."],
         reflection=["Why is the indirect case harder to defend?",
                     "Which of these would your agency actually detect?"]),

    dict(id="DO NOW 5.A", kind="donow", title="Rank These Risks",
         chapter="Ch05", env="paper", minutes=8, needs_key=False, data=[], spine=None, flex=False,
         objectives=["Order AI risks by likelihood and impact for your own context."],
         scenario="Eight risks from the chapter. Your agency cannot mitigate all of them at once.",
         steps=["Place each risk on a likelihood/impact grid on the workbook page.",
                "Circle the two you would fund first.",
                "Compare with a neighbour from a different agency.",
                "Instructor collects the two most-circled."],
         reflection=["Where did you and your neighbour disagree, and why?"]),

    dict(id="DO NOW 5.B", kind="donow", title="Confidentiality, Integrity, or Availability?",
         chapter="Ch05", env="paper", minutes=7, needs_key=False, data=[], spine=None, flex=True,
         objectives=["Map AI-specific failures onto the security model you already use."],
         scenario="Six AI incidents. Each breaks one leg of the CIA triad — or more.",
         steps=["Read the six incidents.",
                "Mark each **C / I / A**, allowing more than one.",
                "For the two you marked with several, say which matters most.",
                "Instructor resolves the contested ones."],
         reflection=["Which leg does hallucination actually attack?"]),

    dict(id="DO NOW 5.C", kind="donow", title="Injection Red Team",
         chapter="Ch05", env="vm", minutes=10, needs_key=True,
         data=[], spine="P5", flex=True,
         objectives=["Write an attack, then write the defence that stops your own attack."],
         scenario="Seven minutes attacking, six defending. The sandbox bot is synthetic.",
         steps=["Read the sandbox bot's system prompt in the notebook.",
                "Spend 7 minutes writing prompts that make it break its own rule.",
                "Swap with a neighbour and try to defeat theirs.",
                "Spend 6 minutes rewriting the system prompt so your own attack fails."],
         reflection=["Which defence held, and what did it cost in usefulness?",
                     "Could you have defended without knowing the attack?"]),

    dict(id="DO NOW 5.D", kind="donow", title="Is This High-Impact AI?",
         chapter="Ch05", env="vm", minutes=8, needs_key=False,
         data=["federal_ai_use_cases.csv"], spine=None, flex=False,
         objectives=["Apply the M-25-21 high-impact definition to real inventory entries."],
         scenario="'High-impact AI' is a term of art that triggers mandatory practices. The "
                  "inventory records how agencies themselves classified each use case.",
         steps=["Pull five use cases from `federal_ai_use_cases.csv` with the flag hidden.",
                "Decide for each: high-impact or not, using the definition on the slide.",
                "Reveal `is_high_impact` and compare.",
                "Read the `HI_justification` for any you got wrong."],
         reflection=["Where did your judgement differ from the agency's?",
                     "What obligations follow once something is labelled high-impact?"]),

    dict(id="Lab 5.1", kind="lab", title="Adversarial Examples and Model Robustness",
         chapter="Ch05", env="vm", minutes=30, needs_key=False,
         data=["epa_aqi_by_county.csv"], spine=None, flex=True,
         objectives=["Craft inputs that flip a model's prediction.",
                     "Measure how much perturbation it actually takes.",
                     "Name the defences that would have helped."],
         scenario="You are testing a classifier before it goes anywhere near a decision. "
                  "Your job is to break it on purpose, in a sandbox, and report honestly.",
         steps=["Open `lab_5.1_adversarial.ipynb` and train the small classifier provided.",
                "Record its baseline accuracy on the held-out set.",
                "Perturb one feature at a time and find the smallest change that flips a "
                "prediction.",
                "Plot flip rate against perturbation size.",
                "Apply one defence from the chapter and re-measure.",
                "Write what you would tell a system owner in three sentences."],
         reflection=["How small was the smallest successful perturbation?",
                     "Would the defence have survived an attacker who knew about it?",
                     "Which of the MITRE ATLAS tactics does this correspond to?"]),

    dict(id="Lab 5.2", kind="lab", title="Detect and Mask PII in Citizen Records",
         chapter="Ch05", env="vm", minutes=30, needs_key=False,
         data=["citizen_records.json", "chicago_311.csv"], spine=None, flex=False,
         objectives=["Find PII in structured and free-text government data.",
                     "Mask it without destroying the record's analytic value.",
                     "Measure what your detector misses."],
         scenario="Before any dataset leaves your boundary — to a vendor, a portal, or a "
                  "model — someone has to find the PII. Today that is you. All records here "
                  "are synthetic.",
         steps=["Open `lab_5.2_pii.ipynb`.",
                "Run the regex detector over `citizen_records.json`. Record hits by type.",
                "Run it over the free-text fields of `chicago_311.csv`.",
                "Find three items it **missed** by reading rows yourself.",
                "Improve one pattern and re-run; confirm you did not create false positives.",
                "Mask rather than delete, keeping the field analysable.",
                "Write the residual risk you would report."],
         reflection=["What did the detector miss, and why is that class hard?",
                     "What did masking cost you analytically?",
                     "Would you certify this file as safe to share? On what basis?"]),
]

# --------------------------------------------------------------------------- #
# Ch06 — Data for AI
# --------------------------------------------------------------------------- #
CH06 = [
    dict(id="Demo 6.1", kind="demo", title="Profiling Real Data, Warts and All",
         chapter="Ch06", env="vm", minutes=10, needs_key=False,
         data=["chicago_311.csv"], spine=None, flex=False,
         objectives=["Watch a real dataset fail the six quality dimensions in under ten minutes."],
         scenario="Chicago 311 is genuine operational data. Your instructor profiles it live "
                  "and the defects find themselves.",
         steps=["Instructor loads the file and prints nulls per column.",
                "Shows inconsistent casing and whitespace in a categorical column.",
                "Shows duplicate service-request numbers.",
                "Shows a date column with impossible values.",
                "Names each defect against its dimension."],
         reflection=["Which defect would silently corrupt a model rather than crash it?"]),

    dict(id="DO NOW 6.A", kind="donow", title="Six Dimensions on Ten Rows",
         chapter="Ch06", env="paper", minutes=8, needs_key=False,
         data=["chicago_311.csv"], spine=None, flex=False,
         objectives=["Apply the six quality dimensions by hand before automating them."],
         scenario="Ten printed rows with defects planted in them.",
         steps=["Mark every defect you can find on the printed extract.",
                "Label each with its dimension: accuracy, completeness, consistency, "
                "timeliness, validity, uniqueness.",
                "Count how many you found; the sheet says how many there are.",
                "Compare with a neighbour."],
         reflection=["Which dimension was hardest to judge from ten rows alone?"]),

    dict(id="DO NOW 6.B", kind="donow", title="Propose the Schema",
         chapter="Ch06", env="vm", minutes=10, needs_key=True,
         data=[], spine="P6", flex=False,
         objectives=["Design a collection schema before data exists, with the model's help."],
         scenario="Your office is about to start collecting something new in a shared sheet. "
                  "Get the schema right now, not after 400 rows.",
         steps=["Describe the collection need to an assistant in two sentences.",
                "Ask for a schema: field, type, required, allowed values, one example.",
                "Ask it to name the three defects most likely to appear anyway.",
                "Compare with the class schema on the whiteboard."],
         reflection=["Which field would you have forgotten?",
                     "Which constraint would have prevented the most defects?"]),

    dict(id="DO NOW 6.C", kind="donow", title="Real, Synthetic, or Neither?",
         chapter="Ch06", env="paper", minutes=7, needs_key=False, data=[], spine=None, flex=True,
         objectives=["Decide when synthetic data is the right — or wrong — answer."],
         scenario="Six situations. Synthetic data solves some of them and quietly ruins others.",
         steps=["Mark each **use real / use synthetic / do not use AI here**.",
                "For each 'synthetic', say what property must be preserved.",
                "Identify the one where synthetic data would hide the very thing you need.",
                "Instructor reveals that case."],
         reflection=["What does synthetic data cost you that nobody mentions?"]),

    dict(id="DO NOW 6.D", kind="donow", title="Write the Cleaning Prompt",
         chapter="Ch06", env="vm", minutes=10, needs_key=True,
         data=["chicago_311.csv"], spine=None, flex=False,
         objectives=["Get a model to normalise messy values reliably and checkably."],
         scenario="One column, many spellings of the same thing.",
         steps=["Take 20 raw values from a messy 311 column.",
                "Write a prompt that maps them to a **fixed** list of canonical values.",
                "Require JSON out, with an `unmapped` list for anything that does not fit.",
                "Run it and check every mapping by eye."],
         reflection=["What did it map wrongly but confidently?",
                     "Why does forcing an `unmapped` list matter?"]),

    dict(id="Lab 6.1", kind="lab", title="Data Quality Assessment of Chicago 311",
         chapter="Ch06", env="vm", minutes=30, needs_key=False,
         data=["chicago_311.csv"], spine=None, flex=False,
         objectives=["Assess a real dataset against all six quality dimensions.",
                     "Quantify each defect rather than describing it.",
                     "Produce a go / no-go recommendation with evidence."],
         scenario="A programme office wants to use 311 data to target service improvements. "
                  "You have been asked whether the data supports that. Answer with numbers.",
         steps=["Open `lab_6.1_data_quality.ipynb` and load the file.",
                "**Completeness:** null rate per column; flag anything above 20%.",
                "**Uniqueness:** duplicate `sr_number` count; inspect a duplicate pair.",
                "**Consistency:** case and whitespace variants in categorical columns.",
                "**Validity:** dates outside a plausible range; closed-before-created rows.",
                "**Timeliness:** distribution of `created_date`; how current is it?",
                "**Accuracy:** pick one column and say honestly how you would even test it.",
                "Build a one-table scorecard: dimension, metric, value, pass/fail.",
                "Write a go / no-go recommendation with the two numbers that drive it."],
         reflection=["Which dimension could you *not* assess from the data alone?",
                     "What is the single cheapest fix at the point of collection?",
                     "Would you sign the recommendation you just wrote?"]),

    dict(id="Lab 6.2", kind="lab", title="GenAI-Assisted Cleaning with Structured Outputs",
         chapter="Ch06", env="vm", minutes=30, needs_key=True,
         data=["chicago_311.csv"], spine=None, flex=False,
         objectives=["Use a model to normalise messy categorical data at volume.",
                     "Enforce a schema so the output is machine-usable.",
                     "Audit the model's work and measure what it got wrong."],
         scenario="Lab 6.1 found the defects. Now fix a class of them with GenAI — and then "
                  "check the fixer, because schema-correct is not the same as correct.",
         steps=["Open `lab_6.2_genai_cleaning.ipynb`.",
                "Extract 60 raw values from a messy categorical column.",
                "Call the model with a **strict JSON schema**: `{raw, canonical, confidence}`.",
                "Parse the response; fail loudly if it does not validate.",
                "Sample 20 mappings and check them by hand. Record the error rate.",
                "Find one high-confidence wrong mapping and explain what misled it.",
                "Re-run the failures with a tightened prompt and compare.",
                "State the human-review rate you would require in production."],
         reflection=["What error rate would you accept, and who decides?",
                     "Did confidence correlate with correctness?",
                     "Which defects from Lab 6.1 can GenAI *not* fix?"]),
]

# --------------------------------------------------------------------------- #
# Ch07 — Building with LLMs: APIs, RAG & Agents
# --------------------------------------------------------------------------- #
CH07 = [
    dict(id="Demo 7.1", kind="demo", title="One API Call, Dissected",
         chapter="Ch07", env="vm", minutes=10, needs_key=True, data=[], spine=None, flex=False,
         objectives=["See what the chat box was doing all along.",
                     "Identify roles, tokens, temperature and cost in a single call."],
         scenario="Your instructor makes one call and stops on every part of it.",
         steps=["Instructor shows the key arriving from `.env`, never from a cell.",
                "Sends a call with a system and a user message; shows the role structure.",
                "Prints the full response object: content, finish reason, usage.",
                "Re-runs at temperature 0 and 1.2 to show determinism change.",
                "Multiplies the token count out to agency scale on the whiteboard."],
         reflection=["Which field would you log for auditability?",
                     "What would temperature 0 buy you in a government workflow?"]),

    dict(id="DO NOW 7.A", kind="donow", title="Hugging Face Tour",
         chapter="Ch07", env="browser", minutes=10, needs_key=False, data=[], spine=None, flex=True,
         objectives=["Navigate the open-model ecosystem and read a model card."],
         scenario="Not every model is behind an API. Some you can download and run inside "
                  "your own boundary.",
         steps=["Open huggingface.co and find an open-weight instruction model.",
                "Read its model card: licence, size, intended use, limitations.",
                "Find one model you could *not* legally deploy at your agency, and say why.",
                "Note the download size and what hardware it would need."],
         reflection=["What would make an on-prem model worth the operational cost?"]),

    dict(id="DO NOW 7.B", kind="donow", title="Cost at Agency Scale",
         chapter="Ch07", env="vm", minutes=8, needs_key=True, data=[], spine=None, flex=False,
         objectives=["Turn token counts into a budget line."],
         scenario="Someone will ask 'what will this cost?'. Be able to answer.",
         steps=["Run one representative call and record prompt and completion tokens.",
                "Multiply out to 1,000, 100,000 and 1,000,000 documents a year.",
                "Look up current per-token pricing and compute all three.",
                "Compare against the staff hours the task takes today."],
         reflection=["At what volume does the model stop being the expensive part?",
                     "Which assumption in your estimate is weakest?"]),

    dict(id="DO NOW 7.C", kind="donow", title="Prompt as Code",
         chapter="Ch07", env="vm", minutes=10, needs_key=True, data=[], spine="P7", flex=False,
         objectives=["Move a prompt from a chat box into a parameterised system message."],
         scenario="The payoff of the whole prompting spine: the chat box was an API call all "
                  "along, and now you control every part of it.",
         steps=["Take your best Prompt Card entry and move it into the `system` message.",
                "Send three different user inputs against that one system prompt.",
                "Change temperature and observe the variance across repeats.",
                "Pin the version that behaves consistently."],
         reflection=["What became easier once the prompt was code?",
                     "What became easier to get wrong?"]),

    dict(id="DO NOW 7.D", kind="donow", title="Where Would RAG Fail?",
         chapter="Ch07", env="paper", minutes=8, needs_key=False, data=[], spine=None, flex=True,
         objectives=["Predict retrieval failure modes before building anything."],
         scenario="Six questions against the four-document policy corpus you will use in "
                  "Lab 7.2.",
         steps=["For each question, predict: will retrieval find the answer?",
                "Mark the two you expect to fail and say why — wrong chunk, wrong wording, "
                "answer spread across documents, or simply absent.",
                "Keep the sheet; check your predictions after Lab 7.2.",
                "Instructor collects the most common predicted failure."],
         reflection=["Which failure mode would be invisible to the user?"]),

    dict(id="Lab 7.1", kind="lab", title="First Calls with the OpenAI API",
         chapter="Ch07", env="vm", minutes=30, needs_key=True,
         data=["gov_memo.txt"], spine="P7", flex=False,
         objectives=["Make working chat calls from Python with the current SDK.",
                     "Control behaviour with system prompts and temperature.",
                     "Get structured JSON out of a real government memo and read the cost."],
         scenario="This replaces the old Lab 6.3, which asked for a personal key and called a "
                  "retired endpoint. The key now comes from `.env`, and the SDK is current.",
         steps=["Open `lab_7.1_openai_api.ipynb`. Run the setup cell and confirm it reports "
                "the key loaded from `.env` without printing it.",
                "Make a first call with a user message only. Print the reply.",
                "Add a system message that fixes the register. Re-run and compare.",
                "Run the same prompt three times at temperature 0, then at 1.0.",
                "Extract `{title, date, decision, owner}` from `gov_memo.txt` as JSON.",
                "Parse it in Python; tighten the prompt until it validates every time.",
                "Print prompt, completion and total tokens; estimate cost per 1,000 memos."],
         reflection=["What did the system message change that the user message could not?",
                     "Where would temperature 0 still not give you identical output?",
                     "What is the first thing you would log if this ran in production?"]),

    dict(id="Lab 7.2", kind="lab", title="RAG over Government Documents",
         chapter="Ch07", env="vm", minutes=30, needs_key=True,
         data=["corpus/ai_acceptable_use_policy.md", "corpus/data_governance_standard.md",
               "corpus/foia_processing_guidance.md", "corpus/records_retention_policy.md"],
         spine="P8", flex=False,
         objectives=["Build a working retrieval pipeline over real policy documents.",
                     "Force citations and verify them.",
                     "Diagnose retrieval failure rather than blaming the model."],
         scenario="Four agency policy documents and a question the answer is buried in. This "
                  "is the pattern behind every 'chat with our documents' pilot.",
         steps=["Open `lab_7.2_rag_gov_docs.ipynb`.",
                "Load the four corpus documents and chunk them; print chunk count and sizes.",
                "Embed the chunks (the notebook falls back to a local embedding offline).",
                "Ask a question **without** retrieval and note what the model invents.",
                "Retrieve the top 3 chunks and inspect them before generating.",
                "Generate with the instruction to answer only from the chunks and quote the "
                "sentence used.",
                "Check every citation against the source file.",
                "Take one of your DO NOW 7.D failure predictions and confirm or refute it.",
                "Change chunk size and re-run the failing question."],
         reflection=["Did chunking or prompting fix your failing question?",
                     "How would you detect a wrong citation at scale?",
                     "What would you tell a programme office promised '95% accuracy'?"]),

    dict(id="Lab 7.3", kind="lab", title="Citizen Services Triage Agent (Capstone)",
         chapter="Ch07", env="vm", minutes=45, needs_key=True,
         data=["citizen_records.json", "chicago_311.csv", "MANIFEST.json"],
         spine="P9", flex=False,
         objectives=["Build an agent that plans, calls tools, and acts under supervision.",
                     "Add guardrails: allow-lists, approval gates, step and spend limits.",
                     "Survive a prompt-injection attempt arriving through a tool result."],
         scenario="The course capstone. You build a triage agent for a citizen-services "
                  "queue: it looks up records, masks PII, searches datasets, and drafts a "
                  "notification — but never sends anything without you.",
         steps=["**Stage A — tools (15 min).** Open `lab_7.3_agent.ipynb` and read the four "
                "provided tools: `search_datasets`, `lookup_citizen_record`, `mask_pii`, "
                "`send_status_notification`. Call each directly once.",
                "**Stage B — the loop (20 min).** Wire the tools into a function-calling loop. "
                "Give it one request and watch it choose. Print every tool call.",
                "**Stage C — guardrails (20 min).** Add a tool allow-list, a maximum step "
                "count, and an approval gate before `send_status_notification`. Confirm the "
                "agent stops and asks.",
                "**Stage C2 — injection (10 min).** Run the poisoned dataset description "
                "supplied in the notebook. It instructs the agent to exfiltrate a record. "
                "Confirm your guardrail holds; if it does not, fix it.",
                "**Stage D — instructing the agent (15 min).** Edit the system instructions to "
                "change its planning behaviour: make it always mask before drafting. Re-run.",
                "**Stage E — your dataset (10 min).** Point `search_datasets` at the dataset "
                "you bookmarked in DO NOW 2.D and ask your own question."],
         reflection=["Which guardrail would you consider mandatory before any real deployment?",
                     "Where did the agent make a choice you did not expect?",
                     "What is the difference between prompting a chatbot and instructing an agent?",
                     "Which part of this would your agency's review board question first?"]),
]

# --------------------------------------------------------------------------- #
# Ch08 — AI Operations & Reporting
# --------------------------------------------------------------------------- #
CH08 = [
    dict(id="Demo 8.1", kind="demo", title="Watching a Model Drift",
         chapter="Ch08", env="vm", minutes=10, needs_key=False,
         data=["cdc_flu_wastewater.csv"], spine=None, flex=False,
         objectives=["See drift in real seasonal data, and see the monitor catch it."],
         scenario="Wastewater surveillance is strongly seasonal. A model trained in one "
                  "season degrades in the next — visibly.",
         steps=["Instructor fits a simple model on an early slice of the series.",
                "Scores it on a later slice; error rises.",
                "Plots the input distribution for both periods side by side.",
                "Shows the threshold that would have raised an alert, and when."],
         reflection=["Was this data drift or concept drift?",
                     "Who should receive that alert, and what should they do?"]),

    dict(id="DO NOW 8.A", kind="donow", title="Which Metric Catches This?",
         chapter="Ch08", env="paper", minutes=7, needs_key=False, data=[], spine=None, flex=False,
         objectives=["Match monitoring metrics to the failures they actually detect."],
         scenario="Six production failures. Each is caught by a different signal — or by none.",
         steps=["Read the six failure descriptions.",
                "Name the metric or monitor that would catch each first.",
                "Mark the one that no standard metric catches.",
                "Say what you would add to catch it."],
         reflection=["Which failure would reach the public before anyone noticed?"]),

    dict(id="DO NOW 8.B", kind="donow", title="Pilot to Production Readiness",
         chapter="Ch08", env="paper", minutes=8, needs_key=False, data=[], spine=None, flex=True,
         objectives=["Apply a readiness checklist to a pilot that wants to go live."],
         scenario="A pilot has 'great results' and a sponsor in a hurry.",
         steps=["Read the one-page pilot description.",
                "Score it against the readiness factors from the chapter.",
                "Circle the two gaps you would block on.",
                "Write the one sentence you would say to the sponsor."],
         reflection=["Which gap is most often waved through in real life?"]),

    dict(id="DO NOW 8.C", kind="donow", title="Critique This Dashboard",
         chapter="Ch08", env="paper", minutes=7, needs_key=False, data=[], spine=None, flex=False,
         objectives=["Apply visualization guidelines to a deliberately poor chart."],
         scenario="A dashboard panel that is technically accurate and practically useless.",
         steps=["List everything wrong with the printed chart.",
                "Name the guideline each violation breaks.",
                "Sketch the replacement in the workbook margin.",
                "State the one question your version answers at a glance."],
         reflection=["Which flaw was misleading rather than merely ugly?"]),

    dict(id="DO NOW 8.D", kind="donow", title="Ask, Then Verify",
         chapter="Ch08", env="vm", minutes=10, needs_key=True,
         data=["epa_aqi_by_county.csv"], spine=None, flex=True,
         objectives=["Use an assistant for analysis, then check every number it produced."],
         scenario="Uploading a CSV and asking for findings is fast. Verifying is the job.",
         steps=["Ask an assistant for three findings from `epa_aqi_by_county.csv`.",
                "Ask it to show the rows or the computation behind each.",
                "Recompute all three yourself in pandas.",
                "Record which survived unchanged."],
         reflection=["Which finding was subtly wrong?",
                     "What phrasing made it show its working most usefully?"]),

    dict(id="Lab 8.1", kind="lab", title="Visualization and Reporting from EPA Data",
         chapter="Ch08", env="vm", minutes=30, needs_key=False,
         data=["epa_aqi_by_county.csv"], spine=None, flex=False,
         objectives=["Build charts that answer a stated question.",
                     "Apply the visualization guidelines deliberately.",
                     "Turn three charts into a one-page briefing."],
         scenario="A deputy director asks: which counties have the worst air quality, is it "
                  "getting better, and where should we focus? Answer in one page.",
         steps=["Open `lab_8.1_visualization.ipynb` and load the EPA file.",
                "Rank counties by unhealthy-day count; chart the top 15.",
                "Chart the distribution of `Median AQI` across all counties.",
                "Chart one state's counties against the national median.",
                "Apply the guidelines: sorted bars, labelled axes, no decoration, honest scale.",
                "Write a three-sentence finding under each chart.",
                "Assemble a one-page briefing: question, three charts, recommendation."],
         reflection=["Which chart would survive being screenshotted without its caption?",
                     "What did sorting change about the reader's conclusion?",
                     "What did you choose *not* to plot, and why?"]),

    dict(id="Lab 8.2", kind="lab", title="GenAI-Assisted Analysis and Briefing",
         chapter="Ch08", env="vm", minutes=30, needs_key=True,
         data=["epa_aqi_by_county.csv", "cdc_flu_wastewater.csv"], spine=None, flex=True,
         objectives=["Use GenAI to accelerate analysis without outsourcing judgement.",
                     "Verify every generated figure against the source.",
                     "Produce a briefing you would put your name on."],
         scenario="Same deliverable as Lab 8.1, but with an assistant. The difference is the "
                  "verification step, which is now yours.",
         steps=["Open `lab_8.2_genai_reporting.ipynb`.",
                "Send a profile of the EPA data and ask for five candidate findings.",
                "Pick the three most decision-relevant.",
                "Recompute each in pandas. Mark **confirmed / wrong / unverifiable**.",
                "Ask the assistant to draft the briefing using only your confirmed findings.",
                "Edit it for accuracy and tone; remove every hedge you cannot support.",
                "Note in the notebook which figures you had to correct."],
         reflection=["How many of the five candidate findings survived verification?",
                     "Where did the assistant save you real time?",
                     "What would have happened if you had skipped the recompute step?"]),
]

# --------------------------------------------------------------------------- #
# Ch09 — Summary & Your Agency AI Roadmap
# --------------------------------------------------------------------------- #
CH09 = [
    dict(id="Demo 9.1", kind="demo", title="A Prompt, Three Days Apart",
         chapter="Ch09", env="browser", minutes=8, needs_key=False, data=[], spine=None, flex=False,
         objectives=["See the week's progress made concrete on one volunteer's prompt."],
         scenario="A volunteer's Day-1 baseline card, rewritten live with everything the room "
                  "has learned.",
         steps=["Volunteer reads their sealed DO NOW 0.2 prompt aloud.",
                "Instructor runs it and projects the output.",
                "Room rebuilds it: role, context, format, grounding, constraints.",
                "Instructor re-runs and both outputs are scored on the rubric."],
         reflection=["Which single change moved the score most?"]),

    dict(id="DO NOW 9.A", kind="donow", title="Rewrite Your Baseline Prompt",
         chapter="Ch09", env="browser", minutes=10, needs_key=False, data=[], spine="P10", flex=False,
         objectives=["Close the spine: rewrite your own Day-1 prompt and score both."],
         scenario="Unseal the card you wrote before any instruction.",
         steps=["Read your original prompt without editing it.",
                "Rewrite it using the ladder: role, context, examples, format, grounding.",
                "Run both. Score both on the rubric.",
                "Record the delta on your Prompt Card."],
         reflection=["Which rung of the ladder did you use without thinking about it?",
                     "What would you still not trust this output to do?"]),

    dict(id="DO NOW 9.B", kind="donow", title="Pick Your First Use Case",
         chapter="Ch09", env="paper", minutes=8, needs_key=False,
         data=["federal_ai_use_cases.csv"], spine=None, flex=False,
         objectives=["Choose one realistic starting point from your own work."],
         scenario="Not the most exciting idea — the one you could actually start in 30 days.",
         steps=["List three candidate tasks from your own job.",
                "Score each on impact, feasibility and risk, 1-5.",
                "Search the federal inventory for anyone already doing it.",
                "Circle the one you will take into Lab 9.1."],
         reflection=["Did finding a precedent change your confidence?"]),

    dict(id="DO NOW 9.C", kind="donow", title="Name Your Guardrail",
         chapter="Ch09", env="paper", minutes=7, needs_key=False, data=[], spine=None, flex=False,
         objectives=["Attach a concrete control to your chosen use case."],
         scenario="Every use case needs the one control that makes it safe enough to start.",
         steps=["Write your use case in one sentence.",
                "Name the single failure that would matter most.",
                "Write the guardrail that prevents it — human gate, allow-list, data rule, log.",
                "Say who owns that guardrail."],
         reflection=["Would your guardrail survive a busy Friday afternoon?"]),

    dict(id="DO NOW 9.D", kind="donow", title="Who Do You Need?",
         chapter="Ch09", env="paper", minutes=7, needs_key=False, data=[], spine=None, flex=True,
         objectives=["Identify the governance cast your use case has to pass through."],
         scenario="Nothing ships alone. Map the people before you need them.",
         steps=["List the roles your use case must clear: CAIO, privacy, security, records, "
                "programme owner.",
                "Mark which you have already met.",
                "Write the one question you would ask each.",
                "Identify the one whose 'no' would end it."],
         reflection=["Who did you forget the first time?"]),

    dict(id="Lab 9.1", kind="lab", title="Your 90-Day Agency AI Roadmap",
         chapter="Ch09", env="browser", minutes=30, needs_key=True,
         data=["federal_ai_use_cases.csv"], spine="P10", flex=False,
         objectives=["Turn the week into a dated, specific 30/60/90 plan.",
                     "Ground it in a real precedent from the federal inventory.",
                     "Leave with a one-page brief you can hand to your manager."],
         scenario="The course deliverable. One page your manager can read in two minutes and "
                  "act on — problem, approach, data, guardrails, first step.",
         steps=["Start from the use case you circled in DO NOW 9.B.",
                "Find one precedent in `federal_ai_use_cases.csv` and note the agency.",
                "**Days 1-30:** define the problem, confirm the data exists, name the owner.",
                "**Days 31-60:** prototype with the guardrail from DO NOW 9.C.",
                "**Days 61-90:** evaluate against the rubric, document, brief the decision-maker.",
                "Use your Prompt Card template to draft the one-pager with an assistant.",
                "Edit every claim you cannot support. Delete every sentence you would not say "
                "aloud to your CIO.",
                "Share the first line with the room."],
         reflection=["What is the first thing you will do on Monday?",
                     "Which part of your plan is most likely to slip, and what would you do?",
                     "What did you leave out on purpose?"]),
]

CHAPTERS = [("Ch00", CH00), ("Ch01", CH01), ("Ch02", CH02), ("Ch03", CH03), ("Ch04", CH04),
            ("Ch05", CH05), ("Ch06", CH06), ("Ch07", CH07), ("Ch08", CH08), ("Ch09", CH09)]

ALL = [a for _, items in CHAPTERS for a in items]

CHAPTER_TITLES = {
    "Ch00": "Course Launch and Lab Environment",
    "Ch01": "AI and ML Foundations for Government",
    "Ch02": "AI Applications Across Government and Public Data",
    "Ch03": "Desktop GenAI: Everyday AI for Government Staff",
    "Ch04": "Modern GenAI and Prompt Engineering",
    "Ch05": "AI Security, Risks, and Responsible AI",
    "Ch06": "Data for AI: Collection, Quality, and Governance",
    "Ch07": "Building with LLMs: APIs, RAG, and Agents",
    "Ch08": "AI Operations and Reporting in Government",
    "Ch09": "Course Summary and Your Agency AI Roadmap",
}

DECK_OF = {
    "Ch00": "Ch00-Course-Launch", "Ch01": "Ch01-AI-ML-Foundations",
    "Ch02": "Ch02-Applications-Public-Data", "Ch03": "Ch03-Desktop-GenAI",
    "Ch04": "Ch04-ModernGenAI-PromptEng", "Ch05": "Ch05-Security-Risks-Responsible-AI",
    "Ch06": "Ch06-Data-for-AI", "Ch07": "Ch07-Building-with-LLMs",
    "Ch08": "Ch08-Operations-Reporting", "Ch09": "Ch09-Summary-Roadmap",
}
