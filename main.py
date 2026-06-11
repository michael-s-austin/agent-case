import argparse
import os

from dotenv import load_dotenv
from generate_content import generate_content
from google import genai
from google.genai import types

def main() -> None:
    parser = argparse.ArgumentParser(description="Case")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not found. Please check your .env file.")

    client = genai.Client(api_key=api_key)
    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]
    
    content = generate_content(client, messages, args.verbose, args.user_prompt)
    print(content)
        
if __name__=="__main__":
    main() 
