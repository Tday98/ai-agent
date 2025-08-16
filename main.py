import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

import config

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
model_name = 'gemini-2.0-flash-001' 

def main():
    print("Hello from ai-agent!")
    if len(sys.argv) > 1:
        user_prompt = sys.argv[1]
        messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)])
        ] 

        if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
            response = client.models.generate_content(model=model_name, contents=messages, config=types.GenerateContentConfig(system_instruction=config.SYSTEM_PROMPT))
            print(response.text)
            prompt_tokens = str(response.usage_metadata.prompt_token_count)
            response_tokens = str(response.usage_metadata.candidates_token_count)
            print(f"""User prompt: {user_prompt}
                  Prompt tokens: {prompt_tokens}
                  Response tokens: {response_tokens}""")
        response = client.models.generate_content(model=model_name, contents=messages, config=types.GenerateContentConfig(system_instruction=config.SYSTEM_PROMPT))
        print(response.text) 
    else:
        print("No prompt provided use uv run main.py {prompt}")
        exit(1)
    exit(0)
    
if __name__ == "__main__":
    main()
