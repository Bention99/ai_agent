import os
from functions.config import *

def get_files_content(working_directory, file_path):

    full_path = os.path.join(working_directory, file_path) # relative path

    absolute_path = os.path.abspath(full_path)

    if working_directory not in absolute_path:
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(absolute_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(absolute_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) >= 1000:
                file_content_string = file_content_string + "...File " + file_path + " truncated at 10000 characters"
            return file_content_string
        

    except Exception as e:
        return f"Error: reading file: {e}"