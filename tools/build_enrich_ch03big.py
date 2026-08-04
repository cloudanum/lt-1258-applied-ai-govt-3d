"""Enrich Ch03 'Desktop GenAI' from 15 -> 55 slides (the big build).

Order of operations:
  (a) in-place text edits to existing slides 4, 5, 11 (corrections) + note updates
  (b) append 40 new slides
  (c) one final arrange() with the full 55-slide permutation
  (d) save

All factual claims trace to 1258/research/refs-ch03-desktop-genai.md (verified 2026-08-01).
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
import pptx_tools as P

DECK = Path("1258/1258a4-author-input/decks/1258-Ch03-Desktop-GenAI.pptx")

SRC_FEDRAMP = "Source: FedRAMP (GSA) — FedRAMP AI Prioritization Initiative, https://www.fedramp.gov/ai/ (verified 2026-08-01)"
SRC_OPENAI_FR = "Source: OpenAI — ChatGPT Enterprise and API Platform available at FedRAMP Moderate, https://openai.com/index/openai-available-at-fedramp-moderate/ (verified 2026-08-01)"
SRC_OPENAI_PRIV = "Source: OpenAI — Enterprise Privacy, https://openai.com/enterprise-privacy/ (verified 2026-08-01)"
SRC_OPENAI_HELP = "Source: OpenAI — How Your Data Is Used to Improve Model Performance, https://help.openai.com/en/articles/5722486-how-your-data-is-used-to-improve-model-performance (verified 2026-08-01)"
SRC_OPENAI_PRICE = "Source: OpenAI — ChatGPT Pricing, https://openai.com/chatgpt/pricing/ (verified 2026-08-01)"
SRC_MS_GOV = "Source: Microsoft Learn — U.S. Government Cloud Environments for Microsoft 365 and Microsoft 365 Copilot, https://learn.microsoft.com/en-us/microsoft-365/copilot/gov-overview (verified 2026-08-01)"
SRC_GOOGLE_PS = "Source: Google Public Sector — Gemini for Government, https://publicsector.google/ai/ (verified 2026-08-01)"
SRC_ANTH_BEDROCK = "Source: Anthropic — Claude in Amazon Bedrock Approved for FedRAMP High and DoD IL4/IL5, https://www.anthropic.com/news/claude-in-amazon-bedrock-fedramp-high (verified 2026-08-01)"
SRC_ANTH_GOV = "Source: Anthropic — Expanded Claude Access Across All Three Branches of Government, https://www.anthropic.com/news/offering-expanded-claude-access-across-all-three-branches-of-government (verified 2026-08-01)"
SRC_GSA_ONEGOV = "Source: U.S. GSA — GSA Strikes OneGov Deal with Anthropic, https://www.gsa.gov/about-gsa/newsroom/news-releases/gsa-strikes-onegov-deal-with-anthropic-08122025 (verified 2026-08-01)"
SRC_ANTH_TERMS = "Source: Anthropic — Updates to Our Consumer Terms and Privacy Policy, https://www.anthropic.com/news/updates-to-our-consumer-terms (verified 2026-08-01)"
SRC_ANTH_DOCS = "Source: Anthropic Docs — Claude Models Overview, https://docs.anthropic.com/en/docs/about-claude/models/overview (verified 2026-08-01)"
SRC_M2521 = "Source: OMB — M-25-21, Accelerating Federal Use of AI through Innovation, Governance, and Public Trust, https://www.whitehouse.gov/wp-content/uploads/2025/02/M-25-21-Accelerating-Federal-Use-of-AI-through-Innovation-Governance-and-Public-Trust.pdf (verified 2026-08-01)"
SRC_GAO = "Source: U.S. GAO — Generative AI Use and Management at Federal Agencies (GAO-25-107653), https://www.gao.gov/products/gao-25-107653 (verified 2026-08-01)"
SRC_GAO_FULL = "Source: U.S. GAO — GAO-25-107653 full report, https://files.gao.gov/reports/GAO-25-107653/index.html (verified 2026-08-01)"
SRC_UPGUARD = "Source: UpGuard — The State of Shadow AI, https://www.upguard.com/resources/the-state-of-shadow-ai (verified 2026-08-01)"
SRC_PAGERDUTY = "Source: PagerDuty — Shadow AI Workplace Survey 2026, https://www.pagerduty.com/newsroom/shadow-ai-workplace-survey-2026/ (verified 2026-08-01)"
SRC_NCDIT = "Source: NCDIT — Use of Publicly Available Generative AI, https://it.nc.gov/resources/artificial-intelligence/use-publicly-available-generative-ai (verified 2026-08-01)"

# --------------------------------------------------------------------------- #
# (a) Corrections to existing slides (0-based indices into the ORIGINAL deck)
# --------------------------------------------------------------------------- #
SLIDE4_BULLETS = [
    "ChatGPT Enterprise / Gov — FedRAMP 20x Moderate certified (early 2026)",
    "Microsoft 365 Copilot (GCC / GCC High / DoD) — inside the government cloud",
    "Gemini for Government — FedRAMP High-authorized",
    "Claude for Government — FedRAMP High; $1 for a year via GSA OneGov",
    "The edition, not the brand, determines what data you may use",
]
SLIDE4_NOTES = (
    "CORRECTED (a3): adds Claude for Government (FedRAMP High; $1 OneGov deal for all three branches via GSA MAS; "
    "Claude also approved for DoD IL4/IL5 via Amazon Bedrock in AWS GovCloud); renames the muddled 'Gemini for Google "
    "Workspace (Assured/Gov)' to the actual product 'Gemini for Government' (FedRAMP High) — Assured Workloads is the "
    "GCP compliance-controls framework, not the assistant; updates ChatGPT status: ChatGPT Enterprise + API Platform "
    "received FedRAMP 20x Moderate certification in early 2026.\n"
    + SRC_FEDRAMP + "\n" + SRC_GSA_ONEGOV + "\n" + SRC_ANTH_BEDROCK + "\n" + SRC_GOOGLE_PS + "\n" + SRC_OPENAI_FR
)

SLIDE5_BULLETS = [
    "FedRAMP authorization tells you a service meets federal security requirements",
    "Public/free assistants are generally NOT authorized for nonpublic data",
    "Enterprise gov editions run inside authorized boundaries (Azure Gov, AWS GovCloud, GCP)",
    "Know your agency's authorized tool list before you paste anything sensitive",
]
SLIDE5_NOTES = (
    "Connect to the Chapter 5 compliance material and the AI acceptable-use policy. Status as of 2026-08-01 is on the "
    "scoreboard slide later in this chapter; GSA, NASA, and VA told GAO that FedRAMP timelines delay acquisition, so "
    "the authorized list keeps moving — verify on the FedRAMP Marketplace.\n"
    + SRC_FEDRAMP + "\n" + SRC_GAO_FULL
)

SLIDE11_BULLETS = [
    "Free: fine for learning and public data; consumer terms; no data agreement",
    "Paid individual: higher limits, but still consumer terms — may train unless you opt out",
    "Enterprise/Government: admin control, no training by default, FedRAMP posture",
    "The tier controls what data you may enter — not which model is 'smartest'",
]
SLIDE11_NOTES = (
    "CORRECTED (a3): makes the consumer-tier training risk concrete. As of 2026-08-01, ChatGPT consumer plans "
    "(Free/Go/Plus/Pro) may train on your chats unless you opt out (OpenAI policy); Claude consumer plans (Free/Pro/Max) "
    "train if the user allows it — a terms change effective Sept-Oct 2025, with 5-year retention for opted-in data vs. "
    "30 days opted out. 'Claude never trains on your data' is now FALSE for consumer tiers; it holds only for Claude for "
    "Work/Government/Education/API/Bedrock/Vertex. The full matrix is two slides later.\n"
    + SRC_OPENAI_HELP + "\n" + SRC_ANTH_TERMS + "\n" + SRC_OPENAI_PRIV
)

# Note-only enrichments on existing slides (appended to existing notes)
NOTE_ADDS = {
    2: (  # The Four Assistants
        "\n\nAs of mid-2026 all four now have U.S. government offerings — including Claude for Government, which the "
        "original editions slide omitted. Details on the editions and scoreboard slides.\n" + SRC_FEDRAMP
    ),
    5: (  # Pattern 1: Research
        "\n\nReinforce 'confidently wrong': five agencies told GAO that bias and hallucination are a top GenAI "
        "challenge. The verify-before-you-trust slide after the worked example makes this concrete.\n" + SRC_GAO_FULL
    ),
    6: (  # Pattern 2: Summarization
        "\n\nThe context-windows slide next explains why whole reports now fit in one prompt (Claude up to 1M tokens; "
        "ChatGPT Pro up to 400K, as of mid-2026). NCDIT cautions that reliance on summaries may mischaracterize the "
        "original — spot-check against the source.\n" + SRC_ANTH_DOCS + "\n" + SRC_NCDIT
    ),
    7: (  # Pattern 3: Drafting
        "\n\nStrengthen with the NCDIT exemplar: disclose and cite AI-drafted content (system, model, version) and use "
        "official accounts so records are retained — covered on the records-and-disclosure slide after the worked "
        "example.\n" + SRC_NCDIT
    ),
    9: (  # Pattern 5: Code
        "\n\nAdd NCDIT's rule: some agencies require written security-office approval before entering code into "
        "public GenAI tools, and AI-generated code needs review for new vulnerabilities — covered on the code-rules "
        "slide after the worked example.\n" + SRC_NCDIT
    ),
    11: (  # The Data Rule (Non-Negotiable)
        "\n\nAnchors: GSA and DHS limit commercial GenAI use to publicly available information only; VA prohibits "
        "web-based public GenAI with sensitive VA data (GAO-25-107653). OMB M-25-21 required every agency to maintain "
        "a generative-AI acceptable-use policy by ~Dec 29, 2025.\n" + SRC_GAO_FULL + "\n" + SRC_M2521
    ),
    12: (  # Shadow AI
        "\n\nNumbers for the discussion are on the 'Shadow AI by the Numbers' slide: 81% of employees use unapproved "
        "AI tools and 45% circumvent blocks (UpGuard 2026 survey); 88% have shared work information with public AI "
        "tools (PagerDuty 2026 survey). Present as vendor surveys, not government statistics.\n"
        + SRC_UPGUARD + "\n" + SRC_PAGERDUTY
    ),
}

# --------------------------------------------------------------------------- #
# (b) New slides, in APPEND order (n0..n39). Final positions set by arrange().
# --------------------------------------------------------------------------- #
NEW = [
 # n0 — after slide 2
 ("Federal GenAI Adoption by the Numbers",
  ["Across 11 agencies, AI use cases nearly doubled: 571 to 1,110 (2023 to 2024)",
   "Generative-AI use cases rose about 9x: 32 to 282 in one year",
   "61% of 2024 GenAI use cases are mission-enabling: writing, search, summarization",
   "Exactly this chapter's five patterns — your coworkers are already using these tools"],
  "GAO-25-107653 (Jul 2025) toplines. Use them to prove 'this is where staff meet AI' is documented, not anecdote. "
  "61% mission-enabling = internal operations work like writing, search, and summarization.\n" + SRC_GAO),
 # n1
 ("ChatGPT: What It's Best At",
  ["The most widely known general assistant — the tool most staff already know",
   "Strong at drafting, brainstorming, summarizing, and conversational research",
   "Frontier models (GPT-5.5 family) with context windows that grow by tier",
   "Government: ChatGPT Enterprise/API is FedRAMP 20x Moderate certified (early 2026)",
   "ChatGPT Gov lets agencies self-host inside their own Azure Government tenant"],
  "Neutral capability framing. Do not quote seat prices — unverified on official pages; check the live pricing page. "
  "FedRAMP status applies to the Enterprise/API service, not the consumer app.\n"
  + SRC_OPENAI_FR + "\n" + SRC_OPENAI_PRICE),
 # n2
 ("Microsoft 365 Copilot: What It's Best At",
  ["Works inside Word, Excel, Outlook, and Teams — no copy-paste into a chatbot",
   "Grounds answers in your work content: documents, email, and meetings",
   "Best fit when your agency already runs on Microsoft 365",
   "Available in GCC, GCC High, and DoD clouds — inside your government tenant",
   "New features arrive later in government clouds than in commercial"],
  "Key concept: prompts, responses, and generated content remain in the government cloud; Copilot inherits the "
  "environment's compliance controls. Feature-lag detail is on the government-cloud-boundaries slide.\n" + SRC_MS_GOV),
 # n3
 ("Gemini: What It's Best At",
  ["Google's assistant — in Workspace (Docs, Sheets, Gmail) and the browser",
   "Natural fit for agencies that run on Google Workspace",
   "Handles text, images, and files in one conversation",
   "Government edition is Gemini for Government — FedRAMP High-authorized",
   "Front door to Google's accredited public-sector cloud and agentic tools"],
  "Naming matters: the product is 'Gemini for Government' (FedRAMP certification confirmed early 2026); Assured "
  "Workloads is the GCP compliance-controls framework, not the assistant.\n" + SRC_GOOGLE_PS + "\n" + SRC_FEDRAMP),
 # n4
 ("Claude: What It's Best At",
  ["Strong writing, analysis, and careful long-document work",
   "Current models offer up to 1M-token context windows (as of mid-2026)",
   "Claude for Government: FedRAMP High — offered to all three branches for $1 (one year)",
   "Also approved for DoD IL4/IL5 workloads via Amazon Bedrock in AWS GovCloud"],
  "The $1 OneGov pricing was a 2025 GSA agreement for up to one year — mention it as how government is buying AI, not "
  "as a standing price. 1M-token context applies to the current Fable 5/Opus 5/Sonnet 5 family.\n"
  + SRC_ANTH_GOV + "\n" + SRC_ANTH_BEDROCK + "\n" + SRC_ANTH_DOCS),
 # n5
 ("The 2026 Authorization Scoreboard (as of mid-2026)",
  ["ChatGPT Enterprise + API Platform — FedRAMP 20x Moderate (early 2026)",
   "Microsoft 365 Copilot — GCC / GCC High / DoD (DoD environment: IL5)",
   "Gemini for Government — FedRAMP High",
   "Claude for Government — FedRAMP High; Claude IL4/IL5 via Bedrock GovCloud",
   "Perplexity Enterprise Pro for Government — FedRAMP certified (early 2026)",
   "Status changes — verify on the FedRAMP Marketplace before relying on it"],
  "Date-stamp is deliberate: this table will drift. The durable skill is the next slide (looking it up), not memorizing "
  "the table. ChatGPT's 20x Moderate covers the Enterprise/API service; M365 Copilot inherits the GCC/GCC High/DoD "
  "environment's posture.\n" + SRC_FEDRAMP + "\n" + SRC_MS_GOV + "\n" + SRC_ANTH_BEDROCK),
 # n6
 ("How to Look Up a Service on the FedRAMP Marketplace",
  ["Start at fedramp.gov and open the Marketplace; search the exact service name",
   "Editions differ: authorization for one tier may not cover another",
   "Confirm the impact level — Moderate vs. High matters for your data",
   "Match the listing against your agency's approved-tools list",
   "When in doubt, ask your security office — don't assume"],
  "Durable skill slide. Instructor: demo the live Marketplace rather than screenshots — listings are JS-rendered and "
  "change often. fedramp.gov/ai lists the AI-prioritized services certified in early 2026.\n" + SRC_FEDRAMP),
 # n7 [flex]
 ("FedRAMP 20x: Why AI Assistants Got Authorized Fast",
  ["The 2025-2026 AI Prioritization Initiative fast-tracked conversational AI",
   "FedRAMP 20x uses Key Security Indicators and automated continuous validation",
   "Criteria: enterprise controls (SSO, SCIM, RBAC), GSA MAS availability, agency demand",
   "Required: customer data must not train models outside the customer environment",
   "Result: months, not years — three assistants certified in early 2026"],
  "[flex] Depth slide — skip if the class is non-technical or time is short. Explains why the scoreboard changed so "
  "fast after years of slow authorizations. The initiative ran Aug 2025-Apr 2026 and is closed to new entrants.\n" + SRC_FEDRAMP),
 # n8 [flex]
 ("How Government Buys AI: The $1 OneGov Deals",
  ["GSA OneGov deal (Aug 2025): Claude for Enterprise + Government, $1 per agency for a year",
   "Covers executive, legislative, and judicial branches via GSA Multiple Award Schedule",
   "Explicitly supports OMB M-25-21 / M-25-22 adoption goals",
   "For you: acquisition is centralized — your agency decides which tools you get"],
  "[flex] Procurement-color slide. The point for users: watch GSA announcements; when your agency signs on, an "
  "enterprise edition with real data protections may appear at no cost to your office.\n" + SRC_GSA_ONEGOV),
 # n9 [flex]
 ("Government Cloud Boundaries: GCC, GCC High, DoD",
  ["M365 Copilot runs entirely inside your agency's government cloud tenant",
   "Prompts, responses, and generated content stay in the government cloud",
   "GCC aligns to FedRAMP Moderate; GCC High targets CUI/ITAR/FedRAMP High; DoD meets IL5",
   "Expect feature lag: new capabilities arrive later than in commercial clouds",
   "The online demo you saw may not match your agency tenant yet"],
  "[flex] Depth for M365 shops. Use it to set expectations: same product name, different feature set and compliance "
  "posture per environment.\n" + SRC_MS_GOV),
 # n10
 ("Worked Example: Research on a Public Program",
  ["Task: get oriented on a public program you just inherited (e.g., a grants program)",
   "Prompt: 'Explain this program — purpose, who it serves, key offices — in plain language'",
   "Follow up: 'What acronyms will I see in its documents?'",
   "Verify every fact against the agency's official .gov pages",
   "Public program information only — never internal case data in a public assistant"],
  "Run it live with a well-known public program. Show one follow-up question going deeper, then show one confident "
  "answer that needs verification. Public data keeps the demo inside the class rule."),
 # n11 [flex]
 ("Verify Before You Trust",
  ["Models are fluent and confident — even when wrong ('hallucination')",
   "Five agencies told GAO that bias and hallucination are a top GenAI challenge",
   "Treat output as a smart colleague's first answer, not a citation of record",
   "Check names, dates, numbers, and citations against authoritative sources"],
  "[flex] Short caution slide — fold into Pattern 1 if time is tight. The GAO finding (5 of 12 agencies flagged "
  "bias/hallucination) shows this is an institutional concern, not just a course rule.\n" + SRC_GAO_FULL),
 # n12
 ("Context Windows in Practice (as of mid-2026)",
  ["Context window = how much the model can consider at once",
   "ChatGPT tiers: about 27K tokens (Free) up to 400K (Pro reasoning models)",
   "Rough input caps: ~12 pages (Free) vs. ~250 pages (Pro)",
   "Claude's current models: up to 1M tokens — a whole IG report fits",
   "Figures change often — check the vendor's current tier table"],
  "Why whole reports now fit in one prompt. Caveat to mention verbally: system instructions and memory consume part of "
  "the window. Teach 'check the tier table on the official pricing page' as the durable skill.\n"
  + SRC_OPENAI_PRICE + "\n" + SRC_ANTH_DOCS),
 # n13
 ("Worked Example: Summarizing a Public IG Report",
  ["Pick a published report — for example, an agency inspector-general audit",
   "Prompt: 'Summarize in 5 bullets: findings, recommendations, affected programs'",
   "Then: 'Draft a 3-sentence executive paragraph for my branch chief'",
   "Spot-check: do the bullets match the report's actual findings?",
   "Watch for dropped caveats — summaries can mischaracterize the original"],
  "Uses a large-context assistant and a published (public) report. Demonstrates both requested-format prompting and "
  "the verification habit. NCDIT explicitly warns that reliance on summaries may mischaracterize the original.\n" + SRC_NCDIT),
 # n14 [flex]
 ("Summary Pitfalls",
  ["Summaries compress — caveats, dissent, and uncertainty often drop out",
   "NCDIT warns: relying on summaries may mischaracterize the original",
   "Ask the model to quote the source lines behind each claim",
   "For anything decision-relevant, read the original sections yourself"],
  "[flex] Fold into the summarization pattern if time is tight. The 'quote the source lines' prompt is a useful "
  "self-check technique students can take home.\n" + SRC_NCDIT),
 # n15
 ("Worked Example: Drafting Routine Correspondence",
  ["Task: a routine status email about a public event or deadline",
   "Prompt with role, audience, purpose, tone, and length — plus a bullet outline",
   "'Rewrite for a general audience; keep it under 150 words'",
   "Edit before sending: names, dates, and commitments are yours to get right",
   "If it documents agency business, it is a federal record — retain it properly"],
  "Show the two-step: draft, then rewrite for tone/length. Emphasize the human edit pass — the model gives a first "
  "draft, never the final word."),
 # n16
 ("AI Output, Records, and Disclosure",
  ["AI-assisted correspondence documenting agency business is a federal record",
   "NCDIT's rule: treat anything entered into a public GenAI tool as released to the public",
   "Disclose AI-drafted content where your AUP requires it (system, model, version)",
   "Use official accounts so records are retained — not personal logins"],
  "The 'released to the public' framing lands hard: anything pasted into a public tool should be treated as public "
  "record. NCDIT's citation rule: name the system, model, and version; footnote/header for documents, embedded credit "
  "for images/audio/video.\n" + SRC_NCDIT),
 # n17
 ("Worked Example: Paragraph to Diagram",
  ["Take a public process description (e.g., how a public application process works)",
   "Prompt: 'Turn this paragraph into a Mermaid flowchart'",
   "Paste the generated Mermaid into your diagram tool to render it",
   "Review the logic — models add plausible-sounding steps that don't exist",
   "Ties to the structured-output and Mermaid material in Chapter 4"],
  "Same task students do in Lab 3.1. Show one render, then deliberately ask for a layout change to show iteration. "
  "Mermaid is covered hands-on in Chapter 4."),
 # n18
 ("Multimodal and Desktop-File Workflows",
  ["Assistants now read files you attach: PDFs, slides, spreadsheets, images",
   "Ask questions about a public PDF without copying text into the chat",
   "Attach a chart or screenshot and ask for the story behind it",
   "The same data rule applies to attachments — a file full of PII is still a spill",
   "Enterprise tiers handle attached files under the same no-training terms"],
  "Attachments feel safer than pasting — they aren't. A spill is a spill whether typed, pasted, or uploaded. Demo with "
  "a public PDF (e.g., a published report). Enterprise no-training-by-default terms cover business data including "
  "uploaded files.\n" + SRC_OPENAI_PRIV),
 # n19
 ("Worked Example: Decoding an Error Message",
  ["Paste the exact error text from a script, formula, or tool",
   "Prompt: 'Explain what this error means and the two most likely causes'",
   "Ask for the fix step by step; have it explain any code it gives you",
   "Test on a copy or sample data — never first on a production system",
   "Strip hostnames, usernames, and paths that reveal internal systems"],
  "Works for Excel formulas and desktop tools, not just Python. The sanitizing habit (strip internal identifiers) is "
  "the part to drill — error text often leaks infrastructure details."),
 # n20
 ("Code Rules in Real AUPs",
  ["NCDIT requires written security-office approval before entering code into public GenAI",
   "Code can reveal internal systems, logic, and vulnerabilities",
   "AI-generated code can introduce new vulnerabilities — review before use",
   "Check your agency's rule before pasting any code, even snippets"],
  "Surprises students: code feels less sensitive than data, but agencies treat it as sensitive. NCDIT's exact rule: no "
  "code without prior written approval from the security office.\n" + SRC_NCDIT),
 # n21
 ("Tier Detail: What Paying Actually Buys",
  ["Higher usage limits and newer models — but terms stay consumer on individual plans",
   "Bigger context windows: ChatGPT Free ~27K tokens vs. Pro up to 400K",
   "Business/Enterprise add SSO, SCIM, RBAC, SOC 2, audit logs, data residency",
   "Business/Enterprise: your data is not used for training by default",
   "Seat prices change often — check official pricing pages for current figures"],
  "Do NOT quote dollar prices on slides — they were not verifiable on official pages at authoring time; demo the live "
  "pricing page instead. The admin-control list (SAML SSO, SCIM, RBAC, SOC 2, domain verification, compliance API "
  "logs, data residency) exists only on Business/Enterprise.\n" + SRC_OPENAI_PRICE + "\n" + SRC_OPENAI_PRIV),
 # n22
 ("Who Trains on Your Prompts? Consumer Tiers",
  ["ChatGPT Free/Go/Plus/Pro: chats may train models unless you opt out",
   "Claude Free/Pro/Max: may train if you allow it — policy changed Sept-Oct 2025",
   "'Claude never trains on your data' is no longer true for consumer tiers",
   "Paid individual does not mean private: consumer terms still apply",
   "Enterprise and government tiers: no training by default"],
  "The correction slide. Anthropic's change required a choice by Oct 8, 2025; it does NOT apply to Claude for Work, "
  "Government, Education, API, Bedrock, or Vertex. OpenAI's consumer default is training-eligible with opt-out.\n"
  + SRC_OPENAI_HELP + "\n" + SRC_ANTH_TERMS),
 # n23
 ("The Training-Data Matrix (as of mid-2026)",
  ["ChatGPT: consumer trains unless you opt out; Business/Enterprise never by default",
   "M365 Copilot: prompts and content stay inside your government cloud tenant",
   "Gemini: Government edition carries FedRAMP High protections; consumer terms differ — check them",
   "Claude: consumer trains if allowed (5-year retention); Work/Government tiers exempt",
   "The durable skill: find each vendor's current data-use policy page"],
  "Walk it row by row. Two vendors' consumer policies are fully documented (OpenAI trains unless opted out; Anthropic "
  "trains if allowed since the Sept-Oct 2025 terms change). Microsoft's government cloud keeps content in-tenant. For "
  "consumer Gemini, verify Google's current terms before use — don't assume.\n"
  + SRC_OPENAI_PRIV + "\n" + SRC_OPENAI_HELP + "\n" + SRC_ANTH_TERMS + "\n" + SRC_MS_GOV),
 # n24 [flex]
 ("Opt-Outs and Retention Settings",
  ["Opted-in Claude consumer chats: retained up to 5 years; opted out: 30 days",
   "Opt-out and history controls exist — but settings are not authorization",
   "NCDIT advises opting out and disabling chat history for higher-risk uses",
   "Enterprise tiers let administrators control retention centrally",
   "An opt-out is a mitigation, never permission to paste nonpublic data"],
  "[flex] Settings-tour slide. The last bullet is the point: even fully opted out, a consumer account is not an "
  "approved boundary for nonpublic agency data.\n" + SRC_ANTH_TERMS + "\n" + SRC_NCDIT),
 # n25
 ("The Data Rule in Real Agency Policy",
  ["GSA and DHS limit commercial GenAI use to publicly available information only",
   "VA prohibits web-based public GenAI with sensitive VA data",
   "All 12 agencies GAO reviewed restrict GenAI use in some capacity",
   "All 12 train staff on protecting information when using GenAI",
   "The data rule isn't this course being cautious — it's documented agency practice"],
  "Turns doctrine into documented practice (GAO-25-107653 full report). If a student says 'my agency has no rule,' "
  "the next-but-one slide's M-25-21 mandate answers it.\n" + SRC_GAO_FULL),
 # n26
 ("The Class Rule: Public or Synthetic Data Only",
  ["Every lab in this course uses public or synthetic data — no exceptions",
   "Good public sources: data.gov, published reports, Federal Register notices",
   "Synthetic = invented data that looks real but describes no real person or case",
   "If you'd hesitate to post it on your agency's public website, don't paste it",
   "This mirrors your agency's AUP — build the habit here"],
  "State it once, repeat it at every lab. The 'public website test' is the memorable heuristic. This rule holds for "
  "the whole course, including Labs 3.1 and every later assistant-based exercise."),
 # n27
 ("The Policy Driver: OMB M-25-21",
  ["OMB M-25-21 (Apr 2025) replaced M-24-10 and set agency AI governance duties",
   "Each agency must maintain a generative-AI acceptable-use policy (~Dec 2025 deadline)",
   "Agencies designate a Chief AI Officer and inventory AI use cases annually",
   "Companion M-25-22 governs AI acquisition — including no vendor training on federal data",
   "Takeaway: your agency has a GenAI policy — find it and read it"],
  "The mandate behind 'know your agency's rules': the AUP requirement landed within 270 days of Apr 3, 2025 (i.e., "
  "~Dec 29, 2025). M-25-21 also sets minimum risk practices for high-impact AI; M-25-22 pushes contract terms barring "
  "vendors from training on federal data without express permission.\n" + SRC_M2521),
 # n28
 ("Anatomy of a Real AUP (NCDIT Walkthrough)",
  ["Never enter PII or confidential data into public GenAI tools",
   "Written security-office approval before entering code",
   "Independently fact-check all output before relying on it",
   "Disclose and cite AI-drafted content: system, model, version",
   "Use official accounts; re-assess approved tools at least annually"],
  "Dissect North Carolina's published policy clause by clause as a model — it is concrete, public, and maps one-to-one "
  "to this chapter's rules. Students can compare it against their own agency's AUP in the micro-exercise.\n" + SRC_NCDIT),
 # n29 [flex]
 ("High-Impact AI vs. Everyday AI",
  ["M-25-21's 'high-impact AI': output drives decisions with legal or material effects on rights or safety",
   "High-impact uses trigger mandatory risk-management practices",
   "Desktop drafting and summarizing usually aren't high-impact — but know the line",
   "When your use case moves toward decisions about people, escalate to your CAIO"],
  "[flex] Governance-depth slide. Keep it to one message: everyday productivity use is lightly governed; "
  "decision-shaping use is heavily governed. Bridge to Chapter 5 compliance material.\n" + SRC_M2521),
 # n30
 ("Shadow AI by the Numbers (Surveys)",
  ["81% of employees use unapproved AI tools (UpGuard 2026 survey)",
   "45% of workers find workarounds to blocked applications",
   "88% have shared work information with public AI tools (PagerDuty 2026 survey)",
   "66% have used unauthorized AI tools at work",
   "Vendor surveys, not government statistics — but the pattern is consistent"],
  "Present explicitly as vendor-commissioned surveys (UpGuard: 500 security leaders + 1,000 employees; PagerDuty: "
  "1,250 office professionals, Jun 2026) — no equivalent .gov dataset exists. The 45% workarounds figure is why "
  "'just ban it' fails.\n" + SRC_UPGUARD + "\n" + SRC_PAGERDUTY),
 # n31 [flex]
 ("What People Actually Paste (PagerDuty Survey)",
  ["43% shared emails or correspondence with public AI tools",
   "40% shared meeting notes",
   "34% shared customer data; 31% shared financial or confidential documents",
   "89% used AI personally before ever using it at work",
   "81% believe leadership plays by different AI rules — a trust gap to close"],
  "[flex] The data-spill pathway, quantified. In a government room, map 'customer data' to constituent data — that is "
  "the reportable spill. Survey of 1,250 office professionals at large orgs (Jun 2026); present as a survey.\n" + SRC_PAGERDUTY),
 # n32
 ("Micro-Exercise: Find Your Agency's GenAI AUP",
  ["M-25-21 required every agency to have one by ~December 2025",
   "GAO found 11 of 12 major agencies already had GenAI use guidelines",
   "Three minutes: search '[your agency] generative AI acceptable use policy'",
   "Look for: approved tools, allowed data classes, disclosure rules",
   "Bring what you find to the Lab 3.1 debrief"],
  "Run as a 3-5 minute warm-up before Lab 3.1. Students on personal devices can still do the search — policies are "
  "public. Debrief: who found one, who couldn't, and what the approved-tools list says.\n" + SRC_M2521 + "\n" + SRC_GAO),
 # n33
 ("Choosing Which Assistant to Reach For",
  ["First: what is your agency licensed and authorized for? Start there",
   "Match the tool to the task: documents in M365 point to Copilot; Workspace to Gemini",
   "Long-document analysis favors a large-context assistant (e.g., Claude, Gemini)",
   "Drafting and general Q&A: any of the four — pick the approved one",
   "Free personal accounts are for learning — and public data only"],
  "Answers Greg Adams' 'which account do I use?' question as a decision order: authorization first, task fit second, "
  "brand preference last. Neutral on brand; the agency's license decides."),
 # n34
 ("Lab 3.1 Walkthrough: Tasks 1-2",
  ["Task 1 — Summarize: condense the provided public document into 5 bullets",
   "Task 2 — Diagram: turn a public process description into a Mermaid diagram",
   "Work in your agency-approved assistant (or the class-designated one)",
   "Public/synthetic inputs only — the class rule applies to every task",
   "Timeboxed: move on when time is called; partial output is fine"],
  "AUTHOR/IG: re-check task wording against Workbook Lab 3.1 before release — slide mirrors the four relay tasks "
  "(summarize, diagram, troubleshoot, draft) at headline level only."),
 # n35
 ("Lab 3.1 Walkthrough: Tasks 3-4",
  ["Task 3 — Troubleshoot: explain the provided error message and propose a fix",
   "Task 4 — Draft: write a short routine email, then rewrite it for tone and length",
   "Score each output with the 3-point rubric (next slide)",
   "Note where the tool struggled — that feeds the debrief"],
  "AUTHOR/IG: re-check task wording against Workbook Lab 3.1 before release."),
 # n36
 ("The 3-Point Quality Rubric",
  ["Accurate: facts check out against the source; nothing invented",
   "Fit: matches the requested format, length, and audience",
   "Safe: no nonpublic data in; no overclaiming in the output",
   "Score each task 0-2 per dimension; compare totals across tools on the board"],
  "Keep scoring fast — 30 seconds per task. The whiteboard comparison across assistants is the payoff: same prompt, "
  "different scores. AUTHOR/IG: confirm this rubric matches the one printed in Workbook Lab 3.1."),
 # n37
 ("Lab 3.1 Debrief",
  ["Where did tools differ on the same task?",
   "What did your agency's AUP allow that the class rule didn't — or vice versa?",
   "What friction did free vs. paid tiers create?",
   "Which pattern will you use first back at your desk?"],
  "Whiteboard debrief. The AUP question lands best if the micro-exercise ran earlier; the tier-friction question "
  "surfaces why agencies buy enterprise editions."),
 # n38
 ("Key Takeaways",
  ["Four capable assistants — the right one is the authorized one",
   "The edition and tier, not the brand, set your data permissions",
   "Consumer tiers may train on your chats; enterprise and gov tiers don't by default",
   "Never paste nonpublic data into an unapproved tool — ever",
   "Your agency has a GenAI AUP (OMB M-25-21) — read it and follow it"],
  "Chapter wrap. Preview: Chapter 4 goes deeper on prompting technique and structured output (P0-P10 spine); the data "
  "rule from this chapter applies everywhere."),
 # n39 [flex]
 ("Beyond the Big Four: A Broadening Landscape",
  ["Perplexity Enterprise Pro for Government also earned FedRAMP certification (early 2026)",
   "DoD's GenAI.mil is training personnel on government AI tools (2026)",
   "New services will keep arriving — the lookup skill outlasts any brand list",
   "Judge each by the same tests: authorization, data terms, your AUP"],
  "[flex] Horizon slide. The point is not the two examples — it is that 'the four assistants' is a snapshot, and the "
  "FedRAMP Marketplace lookup plus the agency AUP are the durable evaluation tools.\n" + SRC_FEDRAMP + "\n" + SRC_GOOGLE_PS),
]

# --------------------------------------------------------------------------- #
# (c) Final order. o0..o14 = original slides; n0..n39 = appended (15..54).
# --------------------------------------------------------------------------- #
ORDER_TITLES = [
    "o0",  "o1",  "n0",  "o2",  "n1",  "n2",  "n3",  "n4",  "n33", "o3",
    "n5",  "n6",  "n7",  "n8",  "o4",  "n9",  "o5",  "n10", "n11", "o6",
    "n12", "n13", "n14", "o7",  "n15", "n16", "o8",  "n17", "n18", "o9",
    "n19", "n20", "o10", "n21", "n22", "n23", "n24", "o11", "n25", "n26",
    "n27", "n28", "n29", "o12", "n30", "n31", "n32", "o13", "n39", "o14",
    "n34", "n35", "n36", "n37", "n38",
]


def set_bullets(slide, bullets):
    """Replace the body placeholder's bullets in place, preserving run formatting
    of the first run in each paragraph where possible."""
    body = P._body_placeholder(slide)
    tf = body.text_frame
    paras = list(tf.paragraphs)
    # grow
    while len(paras) < len(bullets):
        tf.add_paragraph()
        paras = list(tf.paragraphs)
    # shrink (remove extra paragraph XML)
    for p in paras[len(bullets):]:
        p._p.getparent().remove(p._p)
    paras = list(tf.paragraphs)
    for p, text in zip(paras, bullets):
        runs = list(p.runs)
        if runs:
            runs[0].text = text
            for r in runs[1:]:
                r._r.getparent().remove(r._r)
        else:
            p.add_run().text = text


def append_note(slide, extra):
    tf = slide.notes_slide.notes_text_frame
    tf.text = (tf.text or "") + extra


def purge_orphan_slides(prs):
    """Drop rels from non-presentation parts (e.g. viewProps 'last viewed' refs)
    that keep orphan slide parts alive. Orphans left over from the original
    build collide with the partnames python-pptx assigns to appended slides,
    producing duplicate zip entries."""
    live = {s.part for s in prs.slides}
    dropped = 0
    for part in list(prs.part.package.iter_parts()):
        for rId, rel in list(part.rels.items()):
            if rel.is_external:
                continue
            tgt = rel.target_part
            if str(tgt.partname).startswith("/ppt/slides/") and tgt not in live:
                part.rels.pop(rId)
                dropped += 1
    return dropped


def main():
    prs = P.open_deck(DECK)
    slides = list(prs.slides)
    assert len(slides) == 15, f"expected 15 slides, found {len(slides)}"
    print(f"purged {purge_orphan_slides(prs)} stale slide rels")

    # (a) corrections
    set_bullets(slides[3], SLIDE4_BULLETS)
    slides[3].notes_slide.notes_text_frame.text = SLIDE4_NOTES
    set_bullets(slides[4], SLIDE5_BULLETS)
    slides[4].notes_slide.notes_text_frame.text = SLIDE5_NOTES
    set_bullets(slides[10], SLIDE11_BULLETS)
    slides[10].notes_slide.notes_text_frame.text = SLIDE11_NOTES
    for idx0, extra in NOTE_ADDS.items():
        append_note(slides[idx0], extra)

    # (b) append new slides
    for title, bullets, notes in NEW:
        P.append_content(prs, title, bullets, notes)

    # (c) arrange
    def idx(tag):
        kind, n = tag[0], int(tag[1:])
        return n if kind == "o" else 15 + n
    order0 = [idx(t) for t in ORDER_TITLES]
    assert sorted(order0) == list(range(55)), "order must cover all 55 slides"
    P.arrange(prs, order0)

    # (d) save
    P.save(prs, DECK)
    print(f"saved {DECK}: {len(list(prs.slides._sldIdLst))} slides")


if __name__ == "__main__":
    main()
