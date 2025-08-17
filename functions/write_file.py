import os

from google import genai
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to a file, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written into the file that is applied via the file_path."
            ),
        },
        required=["file_path", "content"],
    ),
)

def write_file(working_directory, file_path, content):
    try:
        path = os.path.join(working_directory, file_path)
        abs_path = os.path.abspath(path)
        working_abs = os.path.abspath(working_directory)
        if not abs_path.startswith(working_abs): # check that abs_path contains the working directory
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(abs_path):
            os.makedirs(working_abs, exist_ok=True)
        
        with open(abs_path, "w") as f:
            f.write(content)
            f.close()
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        print(f"Error: {e}")