import os

def get_files_info(working_directory, directory="."):
    try:
        # Resolve absolute paths
        working_directory_abs = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, directory))

        # Check if full_path is within working_directory
        if not os.path.commonpath([working_directory_abs, full_path]) == working_directory_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if full_path is a directory
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'

        # List directory contents
        entries = []
        for entry in os.listdir(full_path):
            entry_path = os.path.join(full_path, entry)
            try:
                is_dir = os.path.isdir(entry_path)
                file_size = os.path.getsize(entry_path)
                entries.append(f'- {entry}: file_size={file_size} bytes, is_dir={is_dir}')
            except OSError as e:
                entries.append(f'- {entry}: Error: {str(e)}')
        return '\n'.join(entries)
    except OSError as e:
        return f'Error: {str(e)}'

