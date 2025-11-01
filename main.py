import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

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

    schema_get_files_info = types.FunctionDeclaration(
        # our harcoded function
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )

    schema_get_file_content = types.FunctionDeclaration(
        # our harcoded function
        name="get_file_content",
        description="Gets he full content of files in the specified folder, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to get files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )

    schema_run_python_file = types.FunctionDeclaration(
        # our harcoded function
        name="run_python_file",
        description="Writes python scripts, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to run files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )

    schema_write_file = types.FunctionDeclaration(
        # our harcoded function
        name="write_file",
        description="Writes content to files, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to write files to, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )              

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )

    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=config
    )

    print(response.text)


    if is_verbose:
        print("----- USAGE ------")

        print('User prompt:', input)
        print('Prompt tokens:', response.usage_metadata.prompt_token_count)
        print('Response tokens:', response.usage_metadata.candidates_token_count)

        print("------------------")

    # Print function calls if present, else print text
    if hasattr(response, 'function_calls') and response.function_calls:
        for function_call_part in response.function_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(response.text)


if __name__ == "__main__":
    main()
