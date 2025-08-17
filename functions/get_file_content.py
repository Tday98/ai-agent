import sys
import os

    # Add the parent directory to sys.path
    # os.path.abspath(__file__) gets the current file's absolute path
    # os.path.dirname() gets the directory of that path
    # os.path.dirname() again gets the parent directory
parent_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir_path)

    # Now, you can import config from the parent directory
import config
from google import genai
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets file content in the specified directory and returns its content, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
        required= ["directory"],
    ),
)

def get_file_content(working_directory, file_path):

    try:
        path = os.path.join(working_directory, file_path)
        abs_path = os.path.abspath(path)
        working_abs = os.path.abspath(working_directory)
        if not abs_path.startswith(working_abs): # check that abs_path contains the working directory
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(abs_path, "r") as f:
            file_content = f.read(config.MAX_CHARS)
            file_content += f'[...File "{file_path}" truncated at 10000 characters]'
            f.close()
            return file_content

    except Exception as e:
        print(f"Error: {e}")