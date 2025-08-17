import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

import config
from functions import get_files_info
from functions.get_files_info import schema_get_files_info 
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
model_name = 'gemini-2.0-flash-001'

full_config = types.GenerateContentConfig(tools=[available_functions], system_instruction=config.SYSTEM_PROMPT)

def main():
    print("Hello from ai-agent!")
    if len(sys.argv) > 1:
        user_prompt = sys.argv[1]
        messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)])
        ] 

        if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
            response = client.models.generate_content(model=model_name, contents=messages, config=full_config)
            function_call_part = response.function_calls
            if function_call_part:
                print(f"Calling function: {function_call_part.name}({function_call_part.args})")
            else:
                print(response.text)
            prompt_tokens = str(response.usage_metadata.prompt_token_count)
            response_tokens = str(response.usage_metadata.candidates_token_count)
            print(f"""User prompt: {user_prompt}
                  Prompt tokens: {prompt_tokens}
                  Response tokens: {response_tokens}""")
        response = client.models.generate_content(model=model_name, contents=messages, config=full_config)
        function_call_part_list = response.function_calls
        if function_call_part_list:
            for function_call_part in function_call_part_list:
                print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        else:
            print(response.text)
    else:
        print("No prompt provided use uv run main.py {prompt}")
        exit(1)
    exit(0)
    
if __name__ == "__main__":
    main()
