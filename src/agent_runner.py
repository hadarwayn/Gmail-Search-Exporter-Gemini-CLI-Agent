# File: src/agent_runner.py
# REVERTED AND FIXED VERSION - Uses google-generativeai, with corrected model selection and robust error handling.

import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

from src.tools.gmail_search_tool import search_gmail
from src.tools.csv_export_tool import export_to_csv
from src.utils import print_log, PREFIX_AGENT, PREFIX_LLM, PREFIX_TOOL

# Load API Key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    # This is a critical error, but for the sake of running, we'll configure a client anyway
    # The user is expected to have this set up in their environment.
    print_log(PREFIX_AGENT, "Warning: GEMINI_API_KEY not found in .env file. Running might fail.")

try:
    genai.configure(api_key=GEMINI_API_KEY)
except Exception as e:
    print_log(PREFIX_AGENT, f"Error configuring Gemini API: {e}")

# System Instruction
SYSTEM_INSTRUCTION = """
You are an Expert Gmail Data Extraction Specialist.

Your job is to:
1. Understand the user's natural language request
2. Convert it to a Gmail search query
3. Call search_gmail with that query
4. Call export_to_csv with the results
5. Tell the user where the file was saved

Examples of converting queries:
- "last email" → "" (empty for recent)
- "emails from bob@example.com" → "from:bob@example.com"
- "urgent emails" → "label:urgent" 
- "emails about travel" → "travel"
- "emails from last week" → "newer_than:7d"

Always call BOTH tools in order: search_gmail, then export_to_csv.
"""


# List models and find the best one
print_log(PREFIX_AGENT, "Finding available Gemini model...")
try:
    # Prioritize the user's paid model, or a fast, capable one
    preferred_models = [
        "gemini-2.5-pro",
        "gemini-2.5-flash",
        "gemini-1.5-pro-001",
        "gemini-1.5-flash-001",
        "gemini-pro", # The model that was failing due to quota
    ]
    
    # Check which models are available to the user's key
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    selected_model = None
    for pref in preferred_models:
        if pref in available_models:
            selected_model = pref
            break
    
    if not selected_model:
        # Fallback to a default if none of the preferred are available
        selected_model = available_models[0] if available_models else "gemini-2.5-flash"
        
    print_log(PREFIX_AGENT, f"Using model: {selected_model}")
    
except Exception as e:
    # Catching general Exception for robustness across different library versions
    print_log(PREFIX_AGENT, f"Could not list models due to an error: {e}. Falling back to default model.")
    selected_model = "gemini-2.5-flash"
    print_log(PREFIX_AGENT, f"Using fallback model: {selected_model}")


# Create the model
model = genai.GenerativeModel(
    model_name=selected_model,
    system_instruction=SYSTEM_INSTRUCTION,
    tools=[search_gmail, export_to_csv]
)

# Start chat
chat = model.start_chat()
print_log(PREFIX_AGENT, "Agent initialized successfully")


def run_agent_turn(user_input: str) -> str:
    """
    Runs one turn of the conversation.
    """
    try:
        print_log(PREFIX_LLM, "Processing request...")
        
        # Send message
        response = chat.send_message(user_input)
        
        # Handle function calls
        max_iterations = 5
        iteration = 0
        
        while iteration < max_iterations:
            # Check if there's a function call
            if not response.candidates:
                return "I encountered an error. Please try again."
            
            part = response.candidates[0].content.parts[0]
            
            # If it's text, we're done
            if hasattr(part, 'text') and part.text:
                return part.text
            
            # If it's a function call, execute it
            if hasattr(part, 'function_call'):
                fc = part.function_call
                func_name = fc.name
                
                # Parse arguments
                # The Gemini SDK uses a different structure for arguments than OpenAI
                # We need to extract the args dictionary correctly from the function call object
                args = dict(fc.args) if fc.args else {}
                
                print_log(PREFIX_TOOL, f"Calling {func_name} with args: {args}")
                
                # Execute the function
                if func_name == "search_gmail":
                    # The function search_gmail expects a keyword argument 'gmail_query'
                    # We must ensure the LLM provides this key
                    if 'gmail_query' not in args:
                        result = {"error": "LLM failed to provide 'gmail_query' argument."}
                    else:
                        result = search_gmail(**args)
                elif func_name == "export_to_csv":
                    # The function export_to_csv expects a keyword argument 'email_data'
                    # This is the second step, and the data should come from the previous tool call result
                    # The LLM is expected to pass the result of the previous tool call here.
                    if 'email_data' not in args:
                        result = {"error": "LLM failed to provide 'email_data' argument from previous tool call."}
                    else:
                        result = export_to_csv(**args)
                else:
                    result = {"error": f"Unknown function: {func_name}"}
                
                print_log(PREFIX_TOOL, f"Function completed. Result: {str(result)[:100]}...")
                
                # Send result back to model
                response = chat.send_message(
                    genai.types.content_types.to_content({
                        "parts": [{
                            "function_response": {
                                "name": func_name,
                                "response": {"result": result}
                            }
                        }]
                    })
                )
                
                iteration += 1
            else:
                break
        
        # If we get here, return whatever we have
        if response.text:
            return response.text
        else:
            return "Task completed successfully!"
            
    except Exception as e:
        print_log(PREFIX_AGENT, f"Error: {e}")
        return f"I encountered an error: {e}"