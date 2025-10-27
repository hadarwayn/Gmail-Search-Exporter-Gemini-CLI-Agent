# File: src/tools/auth_tool.py
# This tool handles getting permission to access a user's Gmail account.
# It uses the "credentials.json" file and creates a "token.json" file.

import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Import our custom print function from the utils.py file
from src.utils import print_log, PREFIX_TOOL

# --- Configuration ---

# Define the directory for private files
PRIVATE_DIR = "Private"

# This is where your secret file is stored
CREDENTIALS_FILE = os.path.join(PRIVATE_DIR, "credentials.json") 

# This is where we'll save the "permission slip"
TOKEN_FILE = os.path.join(PRIVATE_DIR, "token.json") 

# This tells Google what we want to do.
# We are only asking to *read* emails, not send or delete them.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# --- Main Function ---

def get_gmail_credentials() -> Credentials:
    """
    Gets valid Google credentials for the Gmail API.
    It will handle the login pop-up, save the token, and refresh it.
    
    Returns:
        Credentials: A valid Google credentials object.
    """
    print_log(PREFIX_TOOL, "Starting authentication process...")
    creds = None

    # Ensure the Private directory exists
    if not os.path.exists(PRIVATE_DIR):
        os.makedirs(PRIVATE_DIR)
        print_log(PREFIX_TOOL, f"Created directory: {PRIVATE_DIR}")
    
    # --- 1. Check if "permission slip" (token.json) already exists ---
    if os.path.exists(TOKEN_FILE):
        print_log(PREFIX_TOOL, f"Found existing token: {TOKEN_FILE}")
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # --- 2. If no valid "permission slip", get a new one ---
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # If the slip is just "expired", we can "refresh" it without a new login
            print_log(PREFIX_TOOL, "Credentials expired. Refreshing token...")
            creds.refresh(Request())
        else:
            # This is for the VERY first time. It will open the login pop-up.
            print_log(PREFIX_TOOL, "No valid credentials. Starting new user login flow...")
            if not os.path.exists(CREDENTIALS_FILE):
                print_log(PREFIX_TOOL, f"CRITICAL ERROR: 'credentials.json' not found in '{CREDENTIALS_FILE}'")
                print_log(PREFIX_TOOL, "Please get your credentials from Google Cloud Console and save it there.")
                raise FileNotFoundError("credentials.json not found.")
                
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
            print_log(PREFIX_TOOL, "Login successful!")

        # --- 3. Save the new "permission slip" for next time ---
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
            print_log(PREFIX_TOOL, f"Credentials saved to {TOKEN_FILE} for future use.")

    print_log(PREFIX_TOOL, "Authentication successful. Credentials ready.")
    return creds
