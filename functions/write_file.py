def write_file(working_directory, file_path, content):
	import os
	try:
		# Resolve absolute paths
		working_directory_abs = os.path.abspath(working_directory)
		file_abs = os.path.abspath(os.path.join(working_directory, file_path))

		# Check if file_abs is within working_directory
		if not os.path.commonpath([working_directory_abs, file_abs]) == working_directory_abs:
			return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

		# Ensure parent directory exists
		parent_dir = os.path.dirname(file_abs)
		if not os.path.exists(parent_dir):
			os.makedirs(parent_dir, exist_ok=True)

		# Write content to file
		with open(file_abs, 'w', encoding='utf-8') as f:
			f.write(content)
		return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
	except OSError as e:
		return f'Error: {str(e)}'