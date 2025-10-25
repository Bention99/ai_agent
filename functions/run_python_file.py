import os
import subprocess
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file in the specified directory, constrained to the working directory.",
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

def run_python_file(working_directory, file_path, args=[]):

    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    cmd = ["uv", "run", abs_file_path]
    if args:
        cmd.extend(args)

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'

    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=abs_working_dir,)

        if not result.stdout:
            return "No output produced."

        result_string = f"STDOUT: {result.stdout}, STDERR: {result.stderr}"

        if result.returncode != 0:
            result_string = result_string + f"Process exited with code {result.returncode}"

        return result_string
    except Exception as e:
        return f"Error: executing Python file: {e}"