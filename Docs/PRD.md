# Product Requirements Document (PRD)
## Gmail Search Exporter (Gemini Agent Version)
**Version:** 2.0  
**Last Updated:** October 26, 2025  
**Status:** Awaiting Approval (Phase 1 Complete)  
**Author:** AI Developer Expert Copilot (based on Dr. Yoram Segal’s Google ADK pattern)  
**Location:** `Docs/PRD.md`

---

## 🧠 System Prompt (AI Agent Definition)

You are an **Expert Gmail Data Extraction Specialist** with deep expertise in:
- Gmail API integration and Google ADK (Agent Development Kit)
- Secure OAuth 2.0 authentication protocols
- Cross-platform data formatting and UTF-8-sig encoding for Excel
- Vectorized data processing using pandas and numpy

Your **primary mission** is to:
1. Safely and efficiently extract structured Gmail metadata (Date, Subject, Labels).  
2. Maintain data privacy and security for all users.  
3. Optimize performance using vectorized operations (no Python loops).  
4. Produce Excel-compatible CSV files that display Hebrew text correctly.  
5. Operate as a **Gemini-based interactive CLI Agent**, built with the **Google MCP Server ADK**.

---

## 1. Project Overview

### 1.1 Project Name
**Gmail Search Exporter — Gemini CLI Agent**

### 1.2 Project Objective
Create an **interactive AI Agent** that:
- Runs locally in Gemini CLI (powered by Google ADK).  
- Connects to a user’s Gmail account via Gmail API.  
- Performs **natural language searches** (e.g., “emails from my boss about project updates”).  
- Extracts email data (Date, Subject, Labels).  
- Exports results as a **UTF-8-SIG encoded CSV**, Excel-compatible (supports Hebrew/RTL).  

### 1.3 Based On
Inspired by Dr. Yoram Segal’s [Interactive Capital City Agent](https://github.com/rmisegal/google_ai_agent_adk) —  
this project follows the same ADK structure and operation flow:
[USER] → [MEMORY] → [LLM] → [TOOL] → [AGENT]

markdown
Copy code

---

## 2. Supported AI Stack

| Platform | Usage | Account Type |
|-----------|--------|---------------|
| **Gemini (Paid)** | Primary execution model (`gemini-1.5-flash`) | ✅ Paid |
| **Perplexity (Paid)** | Optional secondary query engine for reference checks | ✅ Paid |
| **ChatGPT / Claude / menus.im** | Optional external free assistants | ⚪ Free |

The core **agent runtime** executes inside the **Gemini CLI (ADK environment)**.

---

## 3. Functional Requirements

### FR-1: Authentication
- Gmail API via OAuth 2.0.  
- Credentials stored in `Private/credentials.json`.  
- Gemini API key loaded via `.env` (`GEMINI_API_KEY`).
- All sensitive files excluded via `.gitignore`.

### FR-2: Natural Language Search
- Accepts single free-text input like:  
  “emails about travel abroad to countries outside Israel”
- Agent converts query into Gmail API `q` parameter.  
- Agent logs `[USER]`, `[MEMORY]`, `[LLM]`, `[TOOL]`, `[AGENT]` stages.

### FR-3: Gmail Search Execution
- Tool: `gmail_search_tool(query:str) -> list[dict]`
- Fetches metadata for up to 500 messages per request.  
- Includes pagination handling via `nextPageToken`.

### FR-4: Data Extraction
- Extracts Date, Subject, Labels from Gmail message objects.  
- Uses **pandas** DataFrame for vectorized manipulation.  
- Formats dates: `YYYY-MM-DD HH:MM:SS`.

### FR-5: CSV Export
- Tool: `export_to_csv(dataframe, filename)`  
- Writes CSV with **UTF-8-SIG** encoding.  
- Auto-creates `results/` folder.  
- Verifies correct Hebrew display in Excel.

---

## 4. Technical Architecture

### 4.1 Core Stack
| Component | Technology |
|------------|-------------|
| LLM Engine | Gemini 1.5-Flash (via `google-generativeai`) |
| Agent Runtime | Google MCP Server ADK |
| Interface | Gemini CLI |
| Data Handling | pandas + numpy |
| Environment | Python 3.12.3 (WSL recommended) |
| Secrets Management | `.env` (python-dotenv) |

### 4.2 Directory Layout
Gmail-Search-Exporter/
│
├─ Docs/
│ ├─ PRD.md
│ └─ tasks.json
│
├─ src/
│ ├─ tools/
│ │ ├─ gmail_search_tool.py
│ │ ├─ csv_export_tool.py
│ │ └─ auth_tool.py
│ ├─ agent_runner.py
│ └─ utils.py
│
├─ results/
│ └─ examples/
│
├─ Private/
│ ├─ credentials.json
│ └─ token.json
│
├─ .env
├─ main.py
├─ requirements.txt
└─ .gitignore

yaml
Copy code

---

## 5. Operation Flow (Gemini CLI)

[USER] INPUT: "emails from my boss about project X"
[MEMORY] Saving user message
[LLM] Interpreting user intent
[TOOL] CALLED: gmail_search_tool(query)
[TOOL] RESULT: 135 messages found
[LLM] Generating extraction summary
[TOOL] CALLED: export_to_csv(dataframe, 'gmail_export_2025-10-26_135022.csv')
[AGENT] FINAL: Your CSV file has been saved in results/

yaml
Copy code

---

## 6. Logging and Demo Mode
Following Dr. Segal’s style, the agent supports:
- **Demo Mode:** Automated run with 3 pre-defined Gmail queries (non-sensitive).  
- **Operation Trace:**  
  Every step printed with `[USER]`, `[LLM]`, `[TOOL]`, `[AGENT]` prefix.  
- **Error Handling:** Graceful fallback and friendly messages.

---

## 7. Security and Privacy

- `.env` contains:  
GEMINI_API_KEY=your_actual_api_key

markdown
Copy code
- `.gitignore` includes:
Private/
.env
*.json
token
credentials

yaml
Copy code
- Gmail and Gemini credentials **never uploaded** to GitHub.

---

## 8. Example Scenario

**User Prompt:**  
“emails containing the word ‘invoice’ received last month”

**Agent Flow:**
1. Detects intent: billing / invoice search.  
2. Calls `gmail_search_tool()` with generated query.  
3. Retrieves 250 results.  
4. Extracts Date, Subject, Labels.  
5. Saves CSV as: `results/gmail_export_2025-10-26_142355.csv`.  
6. Displays:  
 > `[AGENT] Export complete. File saved successfully!`

---

## 9. Success Criteria

| Area | Metric |
|-------|--------|
| **Authentication** | Gmail and Gemini APIs connect securely |
| **Search Accuracy** | ≥95% relevant email matches |
| **Encoding** | Hebrew displays correctly in Excel |
| **Performance** | ≤30 seconds for 100 emails |
| **UX** | Clear `[USER]→[TOOL]→[AGENT]` logs |
| **Maintainability** | Each module ≤200 lines |
| **Security** | No credential exposure |

---

## 10. Future Enhancements
- Add `Perplexity` secondary research integration.  
- Build web dashboard (Streamlit).  
- Add semantic search (vector store).  
- Summarize emails via Gemini 1.5 Pro.

---

## 11. Deliverables

### Phase 1
- [x] `Docs/PRD.md`  
- [x] `Docs/tasks.json`

### Phase 2+
- [ ] Gemini Agent & Tools under `src/tools/`  
- [ ] `.env` and `.gitignore` security setup  
- [ ] Operation logging as in Dr. Segal’s demo  
- [ ] `README.md` with full setup instructions  
- [ ] 3 sample CSV exports under `results/examples/`

---

**Document Version:** 2.0  
**Location:** `Docs/PRD.md`  
**Author:** AI Developer Expert Copilot  
**Based on:** Dr. Yoram Segal’s Google ADK Agent Framework (2025)