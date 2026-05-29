import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("GEMINI_API_KEY environment variable not found. Please check your .env file.")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(model='gemini-2.5-flash', contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")

if response.usage_metadata is None:
    raise RuntimeError("There is no usage metadata available.")

print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
print(response.text)
