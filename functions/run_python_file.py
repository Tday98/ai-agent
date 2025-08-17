import os
import subprocess

from google import genai
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    try:
        path = os.path.join(working_directory, file_path)
        abs_path = os.path.abspath(path)
        working_abs = os.path.abspath(working_directory)
        if not abs_path.startswith(working_abs): # check that abs_path contains the working directory
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_path):
            return f'Error: File "{file_path}" not found'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        try:
            completed_process = subprocess.run(args=["python", file_path] + args, cwd=working_abs, timeout=30, capture_output=True, text=True)
            return_string =  f"STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}\n"

            if completed_process.returncode:
                return_string += f"Process exited with code {completed_process.returncode}"

            if completed_process.stdout == "":
                return_string += "No output produced\n"
            return return_string

        except Exception as e:
            return f"Error: exectuing Python file: {e}"
    
    except Exception as e:
        return f"Error: {e}"