# File: src/tools/gmail_search_tool.py
# Fixed version - Now fetches READABLE label names!

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from src.tools.auth_tool import get_gmail_credentials
from src.utils import print_log, PREFIX_TOOL

MAX_RESULTS = 500

def search_gmail(gmail_query: str) -> list[dict]:
    """
    Searches Gmail for emails matching a query.
    
    Args:
        gmail_query: A valid Gmail search query string 
                    (e.g., "from:user@example.com is:unread")
                           
    Returns:
        A list of dictionaries, where each dict is an email with Date, Subject, and Labels.
    """
    print_log(PREFIX_TOOL, f"Received search query: '{gmail_query}'")
    
    try:
        # Get credentials and build service
        creds = get_gmail_credentials()
        service = build("gmail", "v1", credentials=creds)
        print_log(PREFIX_TOOL, "Gmail API service built successfully.")

        # ===== NEW: Get ALL label names from Gmail =====
        print_log(PREFIX_TOOL, "Fetching label names from Gmail...")
        labels_response = service.users().labels().list(userId='me').execute()
        labels = labels_response.get('labels', [])
        
        # Create a dictionary mapping label ID to label name
        label_map = {}
        for label in labels:
            label_id = label['id']
            label_name = label['name']
            label_map[label_id] = label_name
        
        print_log(PREFIX_TOOL, f"Loaded {len(label_map)} label mappings")
        # ================================================

        # Get list of message IDs matching the query
        result = service.users().messages().list(
            userId="me", 
            q=gmail_query, 
            maxResults=MAX_RESULTS
        ).execute()

        messages = result.get("messages", [])
        
        if not messages:
            print_log(PREFIX_TOOL, "No emails found matching the query.")
            return []

        print_log(PREFIX_TOOL, f"Found {len(messages)} matching email(s). Fetching details...")
        
        email_data_list = []

        # Get details for each message
        for msg in messages:
            msg_id = msg["id"]
            email = service.users().messages().get(
                userId="me", id=msg_id, format="metadata"
            ).execute()
            
            payload = email.get("payload", {})
            headers = payload.get("headers", [])
            
            # Get label IDs from the email
            label_ids = email.get("labelIds", [])
            
            # ===== NEW: Convert label IDs to readable names =====
            readable_labels = []
            for label_id in label_ids:
                # Get the readable name from our map
                label_name = label_map.get(label_id, label_id)  # Use ID if name not found
                readable_labels.append(label_name)
            # ====================================================
            
            # Extract Date, Subject, and Labels (now with readable names!)
            email_details = {
                "Date": "",
                "Subject": "",
                "Labels": readable_labels  # Now contains actual label names!
            }
            
            for header in headers:
                name = header["name"]
                if name == "Date":
                    email_details["Date"] = header["value"]
                elif name == "Subject":
                    email_details["Subject"] = header["value"]
            
            email_data_list.append(email_details)

        print_log(PREFIX_TOOL, f"Successfully fetched details for {len(email_data_list)} emails with labels.")
        return email_data_list

    except HttpError as error:
        print_log(PREFIX_TOOL, f"An API error occurred: {error}")
        return []
    except Exception as e:
        print_log(PREFIX_TOOL, f"An unexpected error occurred: {e}")
        return []