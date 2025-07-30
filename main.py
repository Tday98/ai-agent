import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def main():
    print("Hello from ai-agent!")
    if len(sys.argv) > 1:
        response = client.models.generate_content(model='gemini-2.0-flash-001', contents=str(sys.argv[2]))
        print(response.text)
        print("Prompt tokens: " + str(response.usage_metadata.prompt_token_count) + "\n" + "Response tokens: " + str(response.usage_metadata.candidates_token_count))
    else:
        print("No prompt provided use uv run main.py {prompt}")
        return 1
    
if __name__ == "__main__":
    main()
