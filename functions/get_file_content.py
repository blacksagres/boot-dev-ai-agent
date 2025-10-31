import os
from functions.config import MAX_FILE_CONTENT_LENGTH

def get_file_content(working_directory, file_path):
	
	try:
		# Resolve absolute paths
		working_directory_abs = os.path.abspath(working_directory)
		file_abs = os.path.abspath(os.path.join(working_directory, file_path))

		# Check if file_abs is within working_directory
		if not os.path.commonpath([working_directory_abs, file_abs]) == working_directory_abs:
			return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

		# Check if file_abs is a file
		if not os.path.isfile(file_abs):
			return f'Error: File not found or is not a regular file: "{file_path}"'

		# Read file content
		with open(file_abs, 'r', encoding='utf-8') as f:
			content = f.read()
			if len(content) > MAX_FILE_CONTENT_LENGTH:
				return content[:MAX_FILE_CONTENT_LENGTH] + f'\n[...File "{file_path}" truncated at {MAX_FILE_CONTENT_LENGTH} characters]'
			return content
	except OSError as e:
		return f'Error: {str(e)}'