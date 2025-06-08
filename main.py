import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
verbose = False

if len(sys.argv) < 2:
    print("Missing prompt")
    exit(1)
elif len(sys.argv) == 3 and sys.argv[2] == "--verbose":
    verbose = True

contents = sys.argv[1]


messages = [
        types.Content(role="user", parts=[types.Part(text=contents)])
]


response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)

"""
print("Parts:", type(messages[0].parts))
for i in range(len(messages[0].parts)):
      print(messages[0].parts[i])
"""

if verbose:
    print("User prompt:", messages[0].parts)
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)


print(response.text)

