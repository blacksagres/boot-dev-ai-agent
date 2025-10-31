import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():

    input = ""
    is_verbose = False

    
    # - If no input, we throw.
    # - Then check for arguments.
    try:
        input = sys.argv[1]
        arguments = sys.argv[2:]

        is_verbose = "--verbose" in arguments

    except IndexError:
        print('Error processing the input and/or arguments.')
        return sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return sys.exit(1)
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=input)])
    ]
    
    print("Hello from boot-dev-ai-agent!")

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
    )

    print(response.text)


    if is_verbose:
        print("----- USAGE ------")

        print('User prompt:', input)
        print('Prompt tokens:', response.usage_metadata.prompt_token_count)
        print('Response tokens:', response.usage_metadata.candidates_token_count)

        print("------------------")



if __name__ == "__main__":
    main()
