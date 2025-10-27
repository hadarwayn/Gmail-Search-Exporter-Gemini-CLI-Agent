# File: agent.py (ROOT DIRECTORY)
# Smart version with automatic model fallback and encoding safety

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
import google.generativeai as genai

# Set UTF-8 encoding for Python
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

# Add the current directory to Python's path so it can find 'src'
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Import our custom tool functions
from src.tools.gmail_search_tool import search_gmail
from src.tools.csv_export_tool import export_to_csv

# System instruction for the agent
SYSTEM_INSTRUCTION = """
You are an Expert Gmail Data Extraction Specialist.

Your mission is to help users find emails and export them to a CSV file.

**Your Process:**
1. **Understand:** User gives you a natural language prompt (e.g., "emails about travel abroad")
2. **Convert to Gmail Query:** Transform it into Gmail search syntax
   Examples:
   - "last email" or "most recent email" → "" (empty query gets recent emails)
   - "emails from bob@example.com" → "from:bob@example.com"
   - "urgent emails" → "label:urgent"
   - "emails about invoices" → "invoice"
   - "travel emails" → "travel"
   - "emails from last week" → "newer_than:7d"
3. **Search:** Call the search_gmail function with your query string
4. **Export:** Pass the results to export_to_csv function
5. **Confirm:** Tell the user where the CSV file was saved (the exact file path)

Always be helpful and provide clear confirmations with the exact file path.
"""

# List of model names to try, in order of preference (best to fallback)
# NOTE: Only including models that ADK actually supports
MODEL_PRIORITY = [
    "gemini-1.5-pro-002",             # Best paid model (no models/ prefix for ADK)
    "gemini-1.5-pro-001",             # Previous Pro version
    "gemini-1.5-pro",                 # Generic Pro
    "gemini-1.5-flash-002",           # Fast but smart
    "gemini-1.5-flash-001",           # Previous Flash
    "gemini-1.5-flash",               # Generic Flash
    "gemini-pro",                     # Older Pro
    "gemini-flash",                   # Older Flash
]

def get_available_model():
    """
    Try to find a working model from our priority list.
    Returns the first model that exists and is supported by ADK.
    """
    print("[INFO] Checking available Gemini models for ADK compatibility...")
    
    # Known ADK-compatible models (based on google.adk.models registry)
    ADK_COMPATIBLE_MODELS = [
        "gemini-1.5-pro-002",
        "gemini-1.5-pro-001", 
        "gemini-1.5-pro",
        "gemini-1.5-flash-002",
        "gemini-1.5-flash-001",
        "gemini-1.5-flash",
        "gemini-pro",
    ]
    
    # Try to list available models from Gemini API
    try:
        available_models = genai.list_models()
        available_names = [m.name for m in available_models if 'generateContent' in m.supported_generation_methods]
        print(f"[INFO] Found {len(available_names)} models in Gemini API")
        
        # Try each model in our priority list
        for model_name in MODEL_PRIORITY:
            # First check if it's ADK-compatible
            if model_name not in ADK_COMPATIBLE_MODELS:
                print(f"[SKIP] {model_name} - Not ADK compatible")
                continue
                
            # Check if it exists in Gemini API (with or without models/ prefix)
            model_exists = False
            for available_name in available_names:
                if model_name in available_name or available_name.endswith(model_name):
                    model_exists = True
                    break
            
            if model_exists:
                print(f"[SUCCESS] Using model: {model_name}")
                return model_name
            else:
                print(f"[SKIP] {model_name} - Not available in your account")
        
        # If we couldn't find any, use the first compatible one as fallback
        fallback = MODEL_PRIORITY[0]
        print(f"[FALLBACK] Using default model: {fallback}")
        return fallback
        
    except Exception as e:
        print(f"[WARNING] Could not list models: {e}")
        fallback = MODEL_PRIORITY[0]
        print(f"[FALLBACK] Using default model: {fallback}")
        return fallback

# Get the best available model
selected_model = get_available_model()

# CRITICAL: This MUST be named "root_agent" for ADK to find it
root_agent = LlmAgent(
    name="gmail_search_agent",
    model=selected_model,  # Automatically selected best model
    description="An agent that searches Gmail and exports results to CSV files",
    instruction=SYSTEM_INSTRUCTION,
    tools=[search_gmail, export_to_csv]
)

print(f"[INFO] Agent initialized with model: {selected_model}")