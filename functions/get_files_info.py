import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory) # relative path

    absolute_path = os.path.abspath(full_path)

    if working_directory not in absolute_path:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        

    if not os.path.isdir(absolute_path):
        return f'Error: "{directory}" is not a directory'

    if os.path.isfile(absolute_path):
        return f'Error: "{directory}" is not a directory its a file'
        

    try:
        files_in_dir = os.listdir(full_path)
        file_list = []

        for file in files_in_dir:
            title = file
            file_path = os.path.join(full_path, file)
            size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
            file_list.append(f"- {title}: file_size={size} bytes, is_dir={is_dir}")

        return "\n".join(file_list)
    except Exception as e:
        return f"Error listing files: {e}"