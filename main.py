# File: main.py
# This is the main entry point for our project.
# We run this file from the terminal to start the agent.

# Import our agent "brain" and helper functions
from src.agent_runner import run_agent_turn
from src.utils import print_log, PREFIX_USER, PREFIX_AGENT
import sys

def run_interactive_mode():
    """
    Runs the main interactive chat loop for the agent.
    """
    print_log(PREFIX_AGENT, "Gmail Search Exporter Agent is online.")
    
    # --- Print Example Prompts (as requested) ---
    print("\n" + "="*50)
    print(" What emails are you looking for? Here are some examples:")
    print(" 1. Emails from 'david@example.com' with the subject 'Project Update'")
    print(" 2. Messages with the label 'Urgent' or 'Inbox'")
    print(" 3. All emails received after '2024-10-01'")
    print(" 4. Emails containing the words 'invoice' or 'receipt'")
    print(" 5. Messages about 'travel abroad to countries outside Israel'")
    print("="*50 + "\n")

    try:
        while True:
            # --- 1. Get User Input ---
            # The "flush=True" helps make sure the input prompt appears correctly
            print(f"{PREFIX_USER} Enter your search prompt (or 'exit' to quit): ", end="", flush=True)
            user_input = sys.stdin.readline().strip()

            if user_input.lower() in ["exit", "quit"]:
                print_log(PREFIX_AGENT, "Shutting down. Goodbye!")
                break
                
            if not user_input:
                continue

            # --- 2. Run Agent Turn ---
            # Send the input to the agent and let it do its work
            # The agent_runner.py will print all the [LLM] and [TOOL] logs
            agent_response = run_agent_turn(user_input)
            
            # --- 3. Print Final Response ---
            # This prints the agent's final confirmation, e.g., "File saved!"
            print_log(PREFIX_AGENT, agent_response)
            print("-" * 50) # Add a separator for clarity

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n") # Move to a new line after the ^C
        print_log(PREFIX_AGENT, "User interrupted. Shutting down...")
    except Exception as e:
        print_log(PREFIX_AGENT, f"An unexpected error occurred: {e}")
        print_log(PREFIX_AGENT, "Please try again.")

if __name__ == "__main__":
    run_interactive_mode()