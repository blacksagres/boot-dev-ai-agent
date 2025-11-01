import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.call_function import call_function


load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

Before starting, scan this folder structure (the working directory) to obtain full context of the application.
Indicate when your scan is complete even before addressing any prompts from a user. This step is unskippable.

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


    # NOTE: For Gemini function schemas, use types.Type.OBJECT, types.Type.STRING, types.Type.ARRAY, etc. for the 'type' parameter, not string literals like 'object' or 'string'.

    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself."
                )
            }
        )
    )

    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Gets the full content of a file in the specified folder, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file path to get content from, relative to the working directory."
                )
            }
        )
    )

    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Executes a Python file with optional arguments, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The Python file to execute, relative to the working directory."
                ),
                "args": types.Schema(
                    type=types.Type.ARRAY,
                    items=types.Schema(type=types.Type.STRING, description="Argument to pass to the Python file."),
                    description="Arguments to pass to the Python file."
                )
            }
        )
    )

    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Writes content to files, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file path to write to, relative to the working directory."
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content to write to the file."
                )
            }
        )
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


    for i in range(0, 20):
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=config
        )

        if response.candidates:
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)


        # Print function calls if present, else print text
        if hasattr(response, 'function_calls') and response.function_calls:
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, verbose=is_verbose)
                # Check for .parts[0].function_response.response
                try:
                    function_response = function_call_result.parts[0].function_response.response

                    print("FUNCTION LOOP -", function_call_part)

                    response_string = (", ".join([f"{tuple[0]}: {tuple[1]}" for tuple in function_response.items()]))

                    if is_verbose:
                        print("FUNCTION RESPONSE -", response_string)
                    
                    # messages.append(types.Content(role="user", parts=[types.Part(text=function_response)]))

                except (AttributeError, IndexError):
                    raise RuntimeError("Fatal: No function response found in call_function result.")


        if response.text is None:
            print("That should be it for your request.")
            break

        print(response.text)



if __name__ == "__main__":
    main()
