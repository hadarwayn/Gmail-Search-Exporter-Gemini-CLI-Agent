# File: src/utils.py
# This file holds helper functions that other files can use.
# Keeping them here makes our code clean and avoids repeating ourselves.

from datetime import datetime

# Define our special log prefixes, as seen in the PRD
PREFIX_USER = "[USER]"
PREFIX_LLM = "[LLM]"
PREFIX_TOOL = "[TOOL]"
PREFIX_AGENT = "[AGENT]"

def print_log(prefix: str, message: str) -> None:
    """
    Prints a formatted log message to the console.
    
    Args:
        prefix (str): The prefix (e.g., "[TOOL]")
        message (str): The message to print.
    """
    # Get the current time for our timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} {prefix} {message}")

def get_timestamped_filename(base_name: str, extension: str) -> str:
    """
    Creates a unique, timestamped filename.
    e.g., "gmail_export_2025-10-26_164530.csv"
    
    Args:
        base_name (str): The base name of the file (e.g., "gmail_export")
        extension (str): The file extension (e.g., "csv")
    
    Returns:
        str: The full, unique filename.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    return f"{base_name}_{timestamp}.{extension}"