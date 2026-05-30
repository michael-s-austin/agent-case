import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

def main() -> None:
    parser = argparse.ArgumentParser(description="Case")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not found. Please check your .env file.")

    client = genai.Client(api_key=api_key)
    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]
    generate_content(client, messages)

def generate_content(client: genai.Client, messages: list[types.Content]) -> None:
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
    )
    if not response.usage_metadata:
        raise RuntimeError("There is no usage metadata available.")

    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print("Response:")  
    print(response.text)

if __name__=="__main__":
    main() 
