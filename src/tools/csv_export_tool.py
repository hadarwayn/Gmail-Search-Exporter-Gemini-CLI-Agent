# File: src/tools/csv_export_tool.py
# Simple version - NO @tool decorator needed
# IMPORTANT: Do NOT import this file into itself!

import pandas as pd
import os
from src.utils import print_log, get_timestamped_filename, PREFIX_TOOL

OUTPUT_DIR = "results"

def export_to_csv(email_data: list[dict]) -> str:
    """
    Exports a list of email data to a timestamped CSV file.
    
    Args:
        email_data: The list of email dictionaries from the search_gmail tool,
                   where each dictionary has Date, Subject, and Labels fields.
                                 
    Returns:
        The path to the saved CSV file.
    """
    if not email_data:
        print_log(PREFIX_TOOL, "No email data provided to export.")
        return "No data to export."

    print_log(PREFIX_TOOL, f"Preparing to export {len(email_data)} emails to CSV...")
    
    # Create the 'results' directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Use pandas to create a DataFrame (vectorized, no loops!)
    df = pd.DataFrame(email_data)
    
    # Format the data for readability
    # Convert list of labels into a single string
    if "Labels" in df.columns:
        df["Labels"] = df["Labels"].apply(lambda x: ", ".join(x) if isinstance(x, list) else "")
        
    # Re-order columns for nice output
    df = df[["Date", "Subject", "Labels"]]

    # Generate filename and save
    filename = get_timestamped_filename("gmail_export", "csv")
    file_path = os.path.join(OUTPUT_DIR, filename)
    
    # UTF-8-sig encoding is CRITICAL for Hebrew/RTL support in Excel
    encoding = "utf-8-sig" 
    
    df.to_csv(file_path, index=False, encoding=encoding)
    
    print_log(PREFIX_TOOL, f"SUCCESS! Data exported to: {file_path}")
    return file_path
