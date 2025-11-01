from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from google.genai import types

def call_function(function_call_part, verbose=False):
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }
    function_name = function_call_part.name
    args = dict(function_call_part.args)

    # If 'directory' is present but should be 'file_path', 
    # remap for run_python_file
    if function_name == "run_python_file":
        if "directory" in args and "file_path" not in args:
            args["file_path"] = args.pop("directory")

    args["working_directory"] = "calculator"

    if verbose:
        print(f"Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")

    func = function_map.get(function_name)
    if not func:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    print("function args ", args)

    result = func(**args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )