
import os
from google import genai
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
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

def get_files_info(working_directory, directory="."):
    try:
        path = os.path.join(working_directory, directory)
        abs_path = os.path.abspath(path)
        working_abs = os.path.abspath(working_directory)
        if not abs_path.startswith(working_abs): # check that abs_path contains the working directory
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        is_dir = os.path.isdir(abs_path)
        if not is_dir:
            return f'Error: "{directory}" is not a directory'
        list_dir = os.listdir(abs_path)
        return_list = []
        for entry in list_dir:
            new_path = os.path.join(abs_path, entry)
            is_dir = os.path.isdir(new_path)
            file_size = os.path.getsize(new_path)
            return_list.append(f"- {entry}: file_size={file_size} bytes, is_dir={is_dir}")
        return return_list
    except Exception as e:
        return f"Exception: {e} raised"