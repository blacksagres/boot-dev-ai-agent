import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    try:
        # Resolve absolute paths
        working_directory_abs = os.path.abspath(working_directory)
        file_abs = os.path.abspath(os.path.join(working_directory, file_path))

        # Check if file_abs is within working_directory
        if not os.path.commonpath([working_directory_abs, file_abs]) == working_directory_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Check if file exists
        if not os.path.isfile(file_abs):
            return f'Error: File "{file_path}" not found.'

        # Check if file is a Python file
        if not file_abs.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'

        # Build command
        cmd = ['python3', file_abs] + args
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=working_directory_abs,
            timeout=30
        )
        output = []
        if result.stdout:
            output.append(f'STDOUT:\n{result.stdout}')
        if result.stderr:
            output.append(f'STDERR:\n{result.stderr}')
        if result.returncode != 0:
            output.append(f'Process exited with code {result.returncode}')
        if not output:
            return 'No output produced.'
        return '\n'.join(output)
    except Exception as e:
        return f'Error: executing Python file: {e}'