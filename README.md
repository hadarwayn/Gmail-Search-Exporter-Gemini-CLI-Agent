# Gmail Search Exporter - Gemini CLI Agent

### **Author:** [Your Name Here]
### **License:** Feel free to use this code for your projects

---

## 1. 📖 Abstract

The **Gmail Search Exporter** is an interactive AI Agent that runs in a local command-line interface (CLI). It uses Google's Gemini AI model to understand natural language requests (like "emails from my boss last week"). It then securely connects to your Gmail account, finds the matching emails, and exports their **Date**, **Subject**, and **Labels** to a CSV file.

The project is built using the **Google Agent Development Kit (ADK)**, following the "Dr. Yoram Segal" agent pattern `[USER] -> [LLM] -> [TOOL] -> [AGENT]`.

## 2. 🎯 Applications & Use Cases

This tool is for anyone who needs to quickly export structured data from their inbox without complex filters:
* **Accountants:** "Export all emails with the word 'invoice' from last month."
* **Project Managers:** "Find all messages from 'client@example.com' about 'Project X'."
* **Students/Researchers:** "Get all emails from my professor with the label 'thesis'."
* **Personal Archiving:** "Save all emails related to 'travel' or 'vacation'."

The key feature is its ability to export a clean CSV file that is **fully compatible with Microsoft Excel on Windows**, including perfect support for **Hebrew (RTL) characters**.

## 3. ✨ Features

* **Natural Language Search:** No need for complex Gmail queries. Just ask the agent what you want.
* **Gemini AI Brain:** Uses a Gemini model (like `gemini-1.5-flash`) to understand your intent and call the right tools.
* **Secure Authentication:** Uses Google's official OAuth 2.0 flow to get read-only permission. Your credentials are never hard-coded and never leave your computer.
* **ADK Operation Trace:** Watch the agent "think" in real-time with clear `[USER]`, `[LLM]`, and `[TOOL]` logs.
* **Excel (UTF-8-sig) Export:** Creates a CSV file with `utf-8-sig` encoding, which is required for Microsoft Excel to correctly display Hebrew and other non-English characters.
* **Readable Labels:** Automatically converts Gmail's internal label IDs (e.g., `Label_123`) into their readable names (e.g., `Inbox`, `My-Project`).

## 4. 💻 Environment & Requirements

* **OS:** Windows 11 (with WSL), Linux, or macOS
* **Python:** 3.12+
* **Virtual Environment:** **UV** (preferred)
* **Core Libraries:** `google-generativeai`, `google-adk`, `google-api-python-client`, `google-auth-oauthlib`, `pandas`

---

## 5. 🚀 Installation Instructions

Follow these steps to set up the project on your machine.

### Step 1: Clone the Repository

```bash
git clone [YOUR_GITHUB_REPO_URL_HERE]
cd Gmail-Search-Exporter
```

### Step 2: Install UV (Python Environment Manager)

If you don't have `uv`, install it once:
```bash
# On WSL/Linux/macOS
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
# On Windows (PowerShell)
pip install uv
```
(You may need to close and re-open your terminal after this step.)

### Step 3: Set Up Virtual Environment & Install Packages

```bash
# 1. Create the virtual environment
uv venv

# 2. Activate the environment (you must do this every time)
# On WSL/Linux/macOS:
source .venv/bin/activate
# On Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# 3. Install all required packages
uv pip install -r requirements.txt
```

### Step 4: CRITICAL - Get Your API Credentials

This project needs **TWO** sets of keys to work.

**Part A: Get Your Gemini API Key (for the AI "Brain")**

1.  Go to [Google AI Studio](https://aistudio.google.com/).
2.  Click **"Get API key"** and create a new project.
3.  Copy your new API key.
4.  In the project's root folder, create a file named `.env`
5.  Paste your key into the file like this:

    ```ini
    # File: .env
    GEMINI_API_KEY=your_actual_api_key_goes_here
    ```

**Part B: Get Your Gmail API Credentials (for Email Access)**

1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a **New Project**.
3.  Go to **"APIs & Services" > "Dashboard"** and click **"+ ENABLE APIS AND SERVICES"**.
4.  Search for **"Gmail API"** and **Enable** it.
5.  Go to **"APIs & Services" > "OAuth consent screen"**:
    * Select **"External"** and click **"Create"**.
    * App name: `Gmail Exporter` (or any name)
    * User support email: Your email
    * Developer contact: Your email
    * Click **"SAVE AND CONTINUE"**.
    * **Scopes:** Click "Add or Remove Scopes". Search for `gmail.readonly` and check the box for `.../auth/gmail.readonly`. Click "Update".
    * Click **"SAVE AND CONTINUE"**.
    * **Test users:** Click **"+ ADD USERS"** and add the email address of the Gmail account you want to search. Click **"SAVE AND CONTINUE"**.
6.  Go to **"APIs & Services" > "Credentials"**:
    * Click **"+ CREATE CREDENTIALS"** > **"OAuth client ID"**.
    * Application type: **"Desktop app"**.
    * Name: `Gmail Agent Credentials`
    * Click **"Create"**.
    * A pop-up will appear. Click **"DOWNLOAD JSON"**.
7.  **Final Step:**
    * You now have a downloaded `.json` file.
    * Rename this file to **`credentials.json`**.
    * Place this file inside the **`Private/`** folder in your project.

---

## 6. ▶️ How to Run

After completing all installation steps, make sure your virtual environment is active (you see `(.venv)` in your terminal).

Then, just run `main.py`:

```bash
python main.py
```

### First-Time Login
The very first time you run this, a browser window will open, asking you to "Allow" the app to access your Gmail (this is the `gmail.readonly` scope we set up). This is normal.
1.  Click **"Advanced"**.
2.  Click **"Go to (your app name) (unsafe)"**.
3.  Click **"Allow"**.

You will only need to do this once! The app saves a `Private/token.json` file so you stay logged in.

---

## 7. 🗂️ Files and Structure

```
Gmail-Search-Exporter/
│
├─ Docs/
│ ├─ PRD.md              # The Product Requirements Document
│ └─ tasks.json          # The full breakdown of project tasks
│
├─ src/
│ ├─ tools/
│ │ ├─ auth_tool.py      # Handles Google OAuth 2.0 login flow
│ │ ├─ gmail_search_tool.py # Fetches emails from the Gmail API
│ │ └─ csv_export_tool.py   # Saves data to a UTF-8-sig CSV
│ ├─ agent_runner.py     # The "brain": connects Gemini AI to the tools
│ └─ utils.py            # Helper functions for logging
│
├─ results/
│ └─ examples/           # Example CSV output files
│
├─ Private/
│ ├─ credentials.json    # (You must add this) Gmail API key
│ └─ token.json          # (Created automatically) Your login token
│
├─ .env                  # (You must add this) Your Gemini API key
├─ main.py               # The main file you run
├─ requirements.txt      # List of all Python packages
└─ .gitignore            # Tells Git to ignore secret files
```

---

## 8. 📊 Examples & Results

Here is what you will see in your terminal when you run the agent.

### Example 1: Simple Search

You type in a simple query. The agent translates it, calls the tools, and confirms the file is saved.

```
(L12-AIAgent-GMailSearch) $ python main.py
... (example list) ...

[USER] Enter your search prompt (or 'exit' to quit): emails from last week

[2025-10-27 13:30:01] [LLM] Processing request...
[2025-10-27 13:30:02] [LLM] Thought: The user wants emails from the last week. I need to convert this to a Gmail query. "newer_than:7d" is the correct syntax. I will now call the search_gmail tool.
[2025-10-27 13:30:02] [TOOL] CALLING: search_gmail(gmail_query="newer_than:7d")
[2025-10-27 13:30:02] [TOOL] Starting authentication process...
[2025-10-27 13:30:02] [TOOL] Found existing token: Private/token.json
[2025-10-27 13:30:03] [TOOL] Authentication successful. Credentials ready.
[2025-10-27 13:30:03] [TOOL] Gmail API service built successfully.
[2025-10-27 13:30:03] [TOOL] Fetching label names from Gmail...
[2025-10-27 13:30:04] [TOOL] Loaded 58 label mappings
[2025-10-27 13:30:04] [TOOL] Received search query: 'newer_than:7d'
[2025-10-27 13:30:06] [TOOL] Found 112 matching email(s). Fetching details...
[2025-10-27 13:30:09] [TOOL] Successfully fetched details for 112 emails with labels.
[2025-10-27 13:30:09] [TOOL] RESULT: [list of 112 email dicts]
[2025-10-27 13:30:09] [LLM] Thought: The search returned 112 emails. I will now pass this list to the export_to_csv tool.
[2025-10-27 13:30:10] [TOOL] CALLING: export_to_csv(email_data=[...list...])
[2025-10-27 13:30:10] [TOOL] Preparing to export 112 emails to CSV...
[2025-10-27 13:30:10] [TOOL] SUCCESS! Data exported to: results/gmail_export_2025-10-27_133010.csv
[2025-10-27 13:30:10] [TOOL] RESULT: "results/gmail_export_2025-10-27_133010.csv"
[2025-10-27 13:30:11] [AGENT] I have successfully exported 112 emails. Your file is saved at: results/gmail_export_2025-10-27_133010.csv
--------------------------------------------------
[USER] Enter your search prompt (or 'exit' to quit):
```

### Example 2: Hebrew / RTL Support

You search for an email with Hebrew. The agent finds it and saves it.

`[USER] Enter your search prompt (or 'exit' to quit): emails with 'חשבונית'`

The resulting file, `results/gmail_export_2025-10-27_133205.csv`, looks like this when opened in **Microsoft Excel**:


| Date | Subject | Labels |
| :--- | :--- | :--- |
| Tue, 21 Oct 2025 ... | חשבונית מס קבלה עבור שירותי ייעוץ | INBOX, Receipts, Finance |
| Mon, 20 Oct 2025 ... | Re: פגישת סיכום פרויקט | INBOX, Work, Project-X |

(The key is that the Hebrew text is perfectly readable, not scrambled.)

### Example 3: No Results Found

The agent correctly handles cases where no emails are found.

`[USER] Enter your search prompt (or 'exit' to quit): emails from 'santa@northpole.com'`
...
`[TOOL] CALLING: search_gmail(gmail_query="from:santa@northpole.com")`
...
`[TOOL] No emails found matching the query.`
...
`[AGENT] I searched for "from:santa@northpole.com" but did not find any matching emails.`

---

## 9. 🧠 Learning Demonstration

This agent demonstrates the power of **tool-based Gemini models**. The AI model itself *does not* search Gmail. It is a "brain" that *decides which tool to use*.

* When you type **"emails from david"**, the LLM's system prompt guides it to convert that to the query string `"from:david"` and call `search_gmail`.
* When you type **"urgent messages"**, the LLM knows to convert that to `"label:urgent"` before calling the *same* tool.
* After the search tool returns data, the agent's logic knows it *must* then call `export_to_csv` with that data.

This separation of "thinking" (LLM) from "doing" (Python tools) makes the agent powerful, predictable, and easy to maintain.

---

## 10. 📦 GitHub Repository Setup

To upload this project to your GitHub account:

1.  Create a new, empty, **private** repository on GitHub.
2.  Copy its HTTPS URL (e.g., `https://github.com/YourUser/YourRepo.git`).
3.  In your WSL terminal, from the project's root folder:

```bash
# 1. Initialize a new git repository
git init

# 2. Add ALL files to staging (our .gitignore will protect secrets)
git add .

# 3. Create your first commit
git commit -m "Initial commit: Gmail Exporter Agent v1.0"

# 4. Link your local repo to the GitHub remote
git remote add origin [PASTE_YOUR_GITHUB_REPO_URL_HERE]

# 5. Push your code to GitHub
git push -u origin main
```