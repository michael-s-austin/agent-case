import argparse
import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt

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
    generate_content(client, messages, args.verbose, args.user_prompt)

def generate_content(client: genai.Client, messages: list[types.Content], verbose: bool, user_prompt: str) -> None:
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )
    if not response.usage_metadata:
        raise RuntimeError("There is no usage metadata available.")

    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    print("Response:")  
    print(response.text)
        
if __name__=="__main__":
    main() 
