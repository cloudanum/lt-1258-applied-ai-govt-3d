#!/usr/bin/env python3
"""build_notes_ch01.py — delivery-notes rewrite for 1258-Ch01-AI-ML-Foundations.pptx (55 slides).

Idempotent: restores the deck from decks/_bak7/, rebuilds every note as
SAY/ASK hook + KEY POINT + time cue + TRANSITION, and re-appends preserved
markers ([flex], Source lines, spine rungs, author/IG flags) extracted
verbatim from the backup notes. Slide text/layouts/counts are untouched.

Run: ../../.venv-courseware/bin/python tools/build_notes_ch01.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from notes_common import apply_notes, verify

TAG = "Ch01-AI-ML-Foundations"
COUNT = 55

FLEX_CORE = {
    36: "many slightly-different trees voting beat one deep tree — randomness decorrelates their errors (feeds DO NOW 1.A)",
}

NOTES = {
1: """SAY: "By the end of this morning you'll explain what AI actually is to your CIO — and to your neighbor — and mean the same thing both times."
KEY POINT: Chapter 1 builds the foundation: the AI/ML/deep-learning/generative taxonomy, classic ML at concept level, CRISP-DM, and what the federal adoption numbers mean for your agency.
FLEX VALVE: this chapter fills the rest of the morning — if we fall behind, the [flex] slides are the valve; I skip them first.
(~2 min)
TRANSITION: The four objectives we hold this chapter to.""",
2: """ASK: "Which of these four pays off first in your job — the vocabulary, the ML concepts, the project method, or the adoption numbers?"
KEY POINT: Objectives: distinguish AI, ML, deep learning, and generative AI; explain clustering, decision trees, and random forests at concept level; run a project with CRISP-DM; read the federal adoption numbers.
(~2 min)
TRANSITION: The path through the chapter — contents.""",
3: """SAY: "Two labs anchor this chapter: one queries the real federal AI inventory; the other clusters real EPA air-quality data."
KEY POINT: The arc — taxonomy and history, why AI matters in government, classic ML, an NLP bridge, then CRISP-DM — with a demo, four DO NOWs, and two labs.
(~2 min)
TRANSITION: The activities, with their times.""",
4: """ASK: "How much of this chapter is lecture? Less than half — 105 minutes is hands-on."
KEY POINT: Demo 1.1 plus DO NOWs 1.A-1.D plus Labs 1.1 and 1.2; full instructions live in the Lab Manual; DO NOWs 1.A and 1.C and Lab 1.2 are the [flex] items.
(~2 min — walk the list; these times are the chapter's budget)
TRANSITION: First — what it takes to work in government AI.""",
5: """SAY: "Coding, mathematics, domain expertise — the three-legged stool of government AI work, and this room already owns one leg."
KEY POINT: The skills: programming (Python, R), statistics and optimization, and domain expertise with the regulations that govern it — the third is the one no bootcamp gives you.
(~2 min)
TRANSITION: That third leg is why you matter more than the tools.""",
6: """ASK: "AI flags an anomaly in a benefits program — fraud, or a policy change? Who decides?"
KEY POINT: Domain experts validate AI insights against regulations and policy, supply the nuanced context models miss, and make solutions trustworthy — technical skill plus domain knowledge, not one replacing the other.
(~2 min)
TRANSITION: So let's demystify the technology itself — the agenda for the next stretch.""",
7: """SAY: "Three stops: demystifying AI, a deep dive into algorithms, and the machine-learning life cycle."
KEY POINT: Section agenda — the taxonomy first, the core algorithms second, the life cycle that runs a project end to end third.
(~1 min)
TRANSITION: Start at the top of the family tree: AI versus ML.""",
8: """ASK: "AI, ML — same thing? By the end of this slide you'll be correcting people at meetings."
KEY POINT: AI is the broad field of machines performing human-like reasoning; ML is the subset that learns patterns from data without explicit programming — supervised (labeled), unsupervised (unlabeled), and reinforcement (reward feedback).
(~2 min)
TRANSITION: Two more branches complete the map: deep learning and generative AI.""",
9: """SAY: "Deep learning is why 'AI' stopped meaning if-then rules; generative AI is why it showed up in your inbox."
KEY POINT: Deep learning stacks neural-network layers to find intricate patterns in vast datasets; generative AI extends it to create new text, images, and audio. Name capabilities, not one product — the leaders change between deliveries.
(~2 min)
TRANSITION: How did we get here? Seventy-plus years in one slide.""",
10: """SAY: "1956: a summer workshop at Dartmouth coins the term 'artificial intelligence' — the field is older than most of its infrastructure."
KEY POINT: Walk the timeline: Turing 1950, Dartmouth 1956, expert systems from Dendral in 1965 (not an 80s invention), Deep Blue 1997, AlphaGo 2016, generative AI mainstream 2022-2026. Keep the last row generation-neutral so it survives the next model cycle.
(~2 min)
TRANSITION: One distinction your leadership will ask about: data science versus BI.""",
11: """ASK: "Your dashboard tells you what happened last quarter. Is that AI?"
KEY POINT: Business intelligence is descriptive — summaries of past and present data: web analytics, sales metrics, product insights.
(~1 min)
TRANSITION: Data science starts where BI stops.""",
12: """SAY: "BI reads the rear-view mirror; data science tries to see around the curve."
KEY POINT: Data science is predictive and prescriptive — what will happen based on trends, and what actions optimize outcomes — forecasting demand, recommending pricing.
(~1 min)
TRANSITION: So why does this matter specifically in government?""",
13: """ASK: "What's the largest dataset your agency holds — and who gets insight from it today?"
KEY POINT: Three reasons AI matters in governance: data-driven insights for policy decisions, streamlined operations that free resources, and citizen-centric services that personalize and scale.
(~2 min)
TRANSITION: Government brings unique assets to AI — next slide.""",
14: """SAY: "Data custody, legal authority, broad reach — three things government brings to AI that no startup can match."
KEY POINT: Governments analyze sensitive datasets under custody, monitor regulatory compliance with legal authority, and deliver inclusive services to rural and underserved communities — AI amplifies all three.
(~2 min)
TRANSITION: Two concrete examples of that synergy.""",
15: """SAY: "September 2023: the IRS announced AI-driven case selection on some of the largest partnerships in the country — supervised classification, in production."
KEY POINT: Pandemic analytics and tax compliance: ML built by data scientists with tax-enforcement experts selected 75 of the largest partnerships ($10B+ average assets) for examination, and about 500 compliance letters went to partnerships with balance-sheet discrepancies — flag this for the decision-tree section.
(~2 min)
TRANSITION: The fraud numbers behind that kind of system.""",
16: """ASK: "Guess the dollars ML recovered for Treasury in FY2024 — then compare with the slide."
KEY POINT: GAO estimates $233B-$521B in annual federal fraud losses; Treasury prevented and recovered $4B+ in FY2024 — up from $652.7M, roughly sixfold — with $1B of it from ML identifying Treasury check fraud, at a scale of ~1.4B payments worth $6.9T+ a year.
(~2 min)
TRANSITION: Why is government positioned to do this at scale?""",
17: """SAY: "No private firm gets to pair classified data with a public-welfare mandate — that combination is government's alone."
KEY POINT: Government's advantages: access to classified data for security missions, a public-welfare focus rather than profit, and ethical accountability through transparency mandates and independent audits.
(~2 min)
TRANSITION: The other side of the comparison.""",
18: """ASK: "Why can't industry just do all of this for government?"
KEY POINT: Corporations can't access classified or sensitive national datasets, profit-centric goals can miss broader societal impacts, and private deployments rarely scale nationwide.
(~1 min)
TRANSITION: So what is the federal government actually running? The numbers.""",
19: """SAY: "571 to 1,110 in one year — and GAO cautions the guidance itself was significantly revised in early 2025, so the baseline keeps moving."
KEY POINT: The GAO review at chapter depth: reported use cases nearly doubled at 11 agencies, generative AI up about ninefold (32 to 282); examples include VA medical-imaging automation and HHS mining publications for polio outbreaks; barriers are privacy compliance, technical resources, and keeping policies current.
(~2 min)
TRANSITION: What platforms does that work run on?""",
20: """ASK: "TensorFlow, PyTorch, scikit-learn — who recognizes at least one? You're more technical than you think."
KEY POINT: Agencies rely on open-source frameworks, FedRAMP Certified cloud platforms (AWS GovCloud, Azure Government, Google Cloud), and specialized tools; the drivers are transparency, hybrid sovereignty, and privacy by design. Terminology: as of mid-2026, say 'FedRAMP Certified' — the 20x overhaul replaced the legacy 'Authorized' process.
(~2 min)
TRANSITION: The three frameworks, one by one.""",
21: """SAY: "TensorFlow scales to production, PyTorch wins the research lab, scikit-learn is the lightweight workhorse — and all three are free."
KEY POINT: The advantages for government: open compatibility avoids vendor lock-in, cross-platform runs cloud or on-prem, cost efficiency with optional paid enterprise support.
(~2 min)
TRANSITION: The compliance layer every one of these needs: FedRAMP.""",
22: """ASK: "Before a cloud service touches federal data, what has to happen first? One word: FedRAMP."
KEY POINT: FedRAMP standardizes security assessment for cloud services; for AI it means sensitive-data protection, faster deployment on certified platforms, and compliance. Say 'FedRAMP Certified' — and check any service's current status on the live Marketplace rather than stating it generically.
(~2 min)
TRANSITION: The major certified providers.""",
23: """SAY: "531 certified services, plus 28 through the new FedRAMP 20x path — as of mid-2026. The durable skill is the lookup, not the number."
KEY POINT: AWS GovCloud (managed AI like SageMaker, Rekognition), Azure Government (Cognitive Services, hybrid), Google Cloud for Government (natural-language API, AutoML); the figures drift — verify any service's status on the FedRAMP Marketplace.
(~2 min)
TRANSITION: Enough slides — time to query the real inventory yourselves.""",
24: """SAY: "The OMB inventory holds 1,500+ real federal AI use cases — you're about to group them yourself."
KEY POINT: Lab 1.1: load the real inventory; group by agency, development stage, and high-impact flag; write three findings, each with the code that produced it.
(30 min lab — circulate; push for findings stated in plain language; full instructions in the Lab Manual)
TRANSITION: After the lab, back to algorithms — the section agenda.""",
25: """ASK: "Ready for the deep dive? Next stop: the algorithms themselves."
KEY POINT: The middle third of the chapter: unsupervised and supervised learning, K-Means, decision trees, and random forests.
(~1 min)
TRANSITION: Start with the kind that needs no labels.""",
26: """SAY: "No labels, no answer key — unsupervised learning finds structure nobody gave it."
KEY POINT: Unsupervised learning discovers inherent structure in unlabeled data: clustering groups by similarity (market segmentation, image compression); association finds relationships (market-basket recommendations) — and a human still validates that the groupings make sense.
(~2 min)
TRANSITION: The clustering algorithm you'll run yourself today: K-Means.""",
27: """ASK: "What could your agency do with every county grouped by air quality? You'll find out in Lab 1.2."
KEY POINT: K-Means organizes data into groups based on similarity — for government that means optimizing processes, allocating resources effectively, and improving predictive analysis.
(~1 min)
TRANSITION: The algorithm itself.""",
28: """SAY: "Watch the centroids move: assign points to the nearest center, recompute the center, repeat until nothing changes."
KEY POINT: K-Means iterates assign-then-update — similarity does the grouping, no labels required.
(~2 min — walk the diagram slowly)
TRANSITION: From unlabeled to labeled data — supervised learning and its workhorse, the decision tree.""",
29: """SAY: "A decision tree is the most auditable model you'll ever meet — every prediction comes with a path of yes/no questions you can read aloud."
KEY POINT: Trees mimic human decision-making: nodes are features, thresholds split, leaves are outcomes; interpretable, versatile across classification and regression, and non-parametric — no assumed distribution.
(~2 min)
TRANSITION: The supervised family it belongs to.""",
30: """ASK: "Why does your spam filter get better the more you correct it? Labels."
KEY POINT: Supervised learning trains on labeled datasets — humans pay the labeling cost up front — to solve classification (spam vs. inbox) and regression (revenue projection); semi-supervised stretches a small labeled set across a large unlabeled one — present 'cluster then propagate labels' as one recipe, not the definition.
(~2 min)
TRANSITION: The simplest supervised model: a straight line.""",
31: """SAY: "One line through the noise: linear regression is decades old and still earns its keep."
KEY POINT: It fits a straight line to relate Y to X: an intercept, a slope, and an error term; least squares minimizes the squared residuals — it assumes a linear relationship and dislikes outliers.
(~2 min)
TRANSITION: See it on real-looking numbers.""",
32: """ASK: "Spend another $1,000 on marketing — what's it worth? This slide says about $884.50."
KEY POINT: Read the plot: blue points are actuals, the regression line approximates the relationship, deviations are residuals; the slope means ~$884.50 more sales per $1,000 spent — predict future sales by substitution.
(~2 min)
TRANSITION: Back to trees — how they actually grow.""",
33: """SAY: "Grow a tree by asking the most informative question first — then the next, and the next, until splitting stops helping."
KEY POINT: Splitting divides data to minimize impurity (Gini, entropy); recursive partitioning repeats it; stopping criteria — maximum depth, minimum samples per leaf, no further impurity reduction — halt growth; shallow trees underfit, deep trees overfit.
(~2 min)
TRANSITION: The trade-offs in one list.""",
34: """ASK: "If trees are so interpretable, why doesn't everyone stop there?"
KEY POINT: Advantages: interpretable for non-technical stakeholders, flexible across data types, feature importance for free, captures non-linearity. Limitations: overfitting, bias to dominant features, instability — small data changes, different tree — and scaling cost.
(~2 min)
TRANSITION: So we measure instead of admire — evaluation.""",
35: """SAY: "Accuracy alone can lie to you — a fraud model that's 99% accurate by flagging nothing is 100% useless."
KEY POINT: Use the metric family: accuracy, precision, recall, F1, and the confusion matrix; fight overfitting with cross-validation, pruning, and hyperparameter tuning.
(~2 min)
TRANSITION: The fix for one tree's fragility: grow a forest.""",
36: """ASK: "Why would 100 slightly-wrong experts beat one confident one? That's a random forest."
KEY POINT: Each tree trains on a bootstrap sample with a random feature subset at each split, so errors decorrelate and cancel when votes average (Breiman, 2001) — lower variance than one deep tree. Citizen version: ask 100 experts who each saw different evidence, take the majority. This feeds DO NOW 1.A.
(~2 min if taught — skippable if time is short)
TRANSITION: From rows and columns to words — NLP.""",
37: """SAY: "Most of government's knowledge is written down — in prose, not spreadsheets. NLP is how machines read it."
KEY POINT: NLP enables machines to understand, interpret, and respond to human language — combining computational linguistics with ML — and powers virtual assistants, chatbots, and recommendation systems.
(~2 min)
TRANSITION: What NLP is, technically.""",
38: """ASK: "'Apple' — fruit or company? How would a machine know?"
KEY POINT: NLP fuses linguistics, statistical methods, and ML so machines recognize, understand, and generate language — determining word identity and meaning in context — enabling chatbots, sentiment analysis, and translation.
(~1 min)
TRANSITION: The pipeline, step by step.""",
39: """SAY: "Clean the text, reduce words to roots, tag their roles, turn them into numbers, then train — that's the whole pipeline."
KEY POINT: Filtering removes punctuation and stop words; stemming reduces 'running' to 'run'; POS tagging labels grammatical roles; embeddings turn words into vectors that capture context; RNNs or transformers do the learning.
(~2 min)
TRANSITION: Why government specifically can't ignore this.""",
40: """ASK: "Policies, records, citizen letters — what format is most of government's information? Text."
KEY POINT: Governance is textual — policies, historical records, citizen interactions — and the large majority of government information is unstructured text; NLP is how it becomes usable. Keep the share qualitative — do not quote a percentage you can't cite.
(~2 min)
TRANSITION: What 'usable' looks like.""",
41: """SAY: "Traditional databases choke on free text; NLP turns it into classifications, entities, and sentiment you can act on."
KEY POINT: Most governmental data is unstructured; NLP converts it — document classification, named entity recognition, sentiment analysis — with improved decisions, faster processing, and scalability.
(~1 min)
TRANSITION: Where it's already working in government.""",
42: """ASK: "Four application areas on this slide — which would your agency deploy first?"
KEY POINT: Policy and legal analysis (summarize, flag inconsistencies), public sentiment monitoring, chatbots for common queries, and emergency-response text processing — NLP is operational, not experimental.
(~2 min)
TRANSITION: The proof at federal scale: VA claims.""",
43: """SAY: "'Ringing in my ears' — a veteran writes that on a claim form, and a model maps it to hearing loss. That's NLP doing mission work."
KEY POINT: VA's CCPS — its first ML API — classifies free-text disability descriptions: 400K+ claims processed without human intervention (a 24x increase) and $1.5M saved in direct labor, speeding benefits decisions for veterans.
(~2 min)
TRANSITION: NLP on the past as well as the present.""",
44: """SAY: "Decades of archival records hold trends no one has read — NLP reads them."
KEY POINT: NLP identifies trends from decades of archival records and extracts insights for planning — like analyzing historical voting patterns to forecast turnout — making long-term trends accessible to policymakers.
(~1 min)
TRANSITION: Under the hood: how the machine reads a sentence.""",
45: """ASK: "First step in reading a sentence like a machine? Chop it up."
KEY POINT: Tokenization splits text into words, phrases, or sentences — 'Natural Language Processing is amazing' becomes five tokens — the foundation for frequency counts and parsing.
(~1 min)
TRANSITION: Next step: finding the who, what, and where.""",
46: """SAY: "Barack Obama, President, United States, 2009-2017 — a person, a role, a location, a date. That's entity recognition."
KEY POINT: NER identifies and categorizes names, organizations, locations, and dates — simplifying extraction and improving retrieval. Classroom moment: run the same sentence through the demo next door and let students see the API type 'United States' as LOCATION.
(~2 min)
TRANSITION: Try it yourselves, right now, in the browser.""",
47: """SAY: "Browsers open — you're about to run production ML on a web page, no install."
KEY POINT: DO NOW: open the Natural Language API demo at cloud.google.com/natural-language, ANALYZE the sample text, then RESET and probe with your own — inspect the Entities, Sentiment, Moderation, and Categories tabs.
(10 min do-now — demo the tabs first, then let them probe; public text only)
TRANSITION: From text to images — vision AI.""",
48: """ASK: "What do surveillance footage, passport scans, and satellite images have in common? Government has mountains of all three."
KEY POINT: Vision AI serves public safety (threat detection), document processing (OCR for passports and licenses), and urban planning (land-use analysis) — the goal is streamlined decisions and operational efficiency.
(~2 min)
TRANSITION: Google's government-oriented offerings, as the example.""",
49: """SAY: "One vendor's stack, end to end: recognition, multimodal analysis, generation, and custom models."
KEY POINT: The Cloud Vision API covers facial recognition and content moderation; Vertex AI with Gemini handles multimodal tasks like disaster-impact analysis; Imagen supports planning imagery; custom models target defense, healthcare, and infrastructure needs.
(~1 min)
TRANSITION: Step back: how does a whole AI project run? CRISP-DM.""",
50: """SAY: "Every AI project that survives contact with reality follows the same six-phase loop — this course uses it all week."
KEY POINT: CRISP-DM: business understanding, data understanding, data preparation, modeling, evaluation, deployment — then iterate; it gives every instructor and student a shared map of the work.
(~2 min)
TRANSITION: CRISP-DM with government instincts.""",
51: """ASK: "Which phase eats most of an AI project's life? The unglamorous one: data preparation."
KEY POINT: In government practice: business understanding includes the mission need and policy constraints; evaluation must cover fairness, security, and explainability — anchor that to the NIST AI RMF — not just accuracy; deployment includes drift monitoring (Chapter 8). Keep 'largest phase' qualitative — the '80% of project time' figure is a rule of thumb, not a measurement.
(~2 min)
TRANSITION: Watch one full pass on a case you already know.""",
52: """SAY: "Six phases, one fraud problem — watch CRISP-DM stop being abstract."
KEY POINT: Treasury, phase by phase: cut improper payments without delaying legitimate ones; prepare payment and check data; classification flags high-risk transactions; precision-first evaluation — a false flag burdens an honest recipient; deploy at scale, monitor drift, iterate. The phases loop — deployment findings feed the next round.
(~2 min)
TRANSITION: Chapter wrap, then the second lab.""",
53: """ASK: "Which AI technology do you see having the biggest impact on your work?"
KEY POINT: Takeaways: ML and NLP drive innovation in governance, and the applications you saw are running today — reflect on where they integrate in your department.
(~2 min — let two or three answers surface)
TRANSITION: Last hands-on of the chapter: cluster the country's counties.""",
54: """SAY: "EPA publishes an air-quality summary for every county — nobody labels them. You're about to find the natural groupings."
KEY POINT: Lab 1.2: open lab_1.2_clustering.ipynb, load epa_aqi_by_county.csv, scale the numeric day-count columns, fit K-Means with k=3, and print each cluster's size and column means so a programme office can target outreach.
(30 min lab — this is the chapter's [flex] item: if the morning ran long, this is the valve; circulate and push plain-language cluster descriptions)
TRANSITION: One closing look at what you now know.""",
55: """SAY: "Read this list again — every item on it was new vocabulary this morning."
KEY POINT: You came for what AI is, key concepts, ML technologies, predictive analytics, NLP, and computer vision — and you now hold all six, plus the potential of AI in transforming government services.
(~1 min)
TRANSITION: Break — then Chapter 2: applications across government and public data.""",
}

if __name__ == "__main__":
    apply_notes(TAG, COUNT, NOTES, FLEX_CORE)
    verify(TAG, COUNT)
