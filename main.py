import os
from dotenv import load_dotenv
from google import genai
import sys

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():

    input = ""

    # without an input, throw an error
    try:
        input = sys.argv[1]
    except:
        return sys.exit(1)
    
    print("Hello from boot-dev-ai-agent!")

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=input
    )

    print(response.text)
    print("----- USAGE ------")

    print('Prompt tokens:', response.usage_metadata.prompt_token_count)
    print('Response tokens:', response.usage_metadata.candidates_token_count)

    print("------------------")



if __name__ == "__main__":
    main()
