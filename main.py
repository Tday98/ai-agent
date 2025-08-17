import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

import config
from functions.get_files_info import schema_get_files_info 
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function, available_functions

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
            if (response.function_calls == None):
                print(response.text)
                exit(3)
            function_responses = []
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, True)
                if (
                    not function_call_result.parts
                    or not function_call_result.parts[0].function_response
                ):
                    raise Exception("empty function call result")
                print(f"-> {function_call_result.parts[0].function_response.response}")
                function_responses.append(function_call_result.parts[0])

            if not function_responses:
                raise Exception("no function responses generated, exiting.")
            prompt_tokens = str(response.usage_metadata.prompt_token_count)
            response_tokens = str(response.usage_metadata.candidates_token_count)
            print(f"""User prompt: {user_prompt}
                  Prompt tokens: {prompt_tokens}
                  Response tokens: {response_tokens}""")
        response = client.models.generate_content(model=model_name, contents=messages, config=full_config)
        if (response.function_calls == None):
            print(response.text)
            exit(3)
        function_call_part_list = response.function_calls
        if function_call_part_list:
            for function_call_part in function_call_part_list:
                function_call_result = call_function(function_call_part)
                print(f"-> {function_call_result.parts[0].function_response.response}")
        else:
            print(response.text)
    else:
        print("No prompt provided use uv run main.py {prompt}")
        exit(1)
    exit(0)
    
if __name__ == "__main__":
    main()
