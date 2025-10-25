import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

def inputchecker(input):
    input_string = ""
    verbose = False
    if len(input) < 2:
        print("Error: prompt not provided.")
        sys.exit(1)
    else:
        for i in range(1, len(input)):
            if input[i] == "--verbose":
                verbose = True
            else:
                input_string += input[i] + " "
        return input_string, verbose

def ask_gemini(messages):
    load_dotenv("gem.env")
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    model = "gemini-2.0-flash-001"

    return client.models.generate_content(model=model, contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))

def main():

    user_input = sys.argv
    receiver = inputchecker(user_input)
    prompt = receiver[0]
    verbose = receiver[1]

    messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    response = ask_gemini(messages)
    usage = response.usage_metadata

    if verbose == True:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_token_count}")

    if len(response.function_calls) >= 1:
        for call in response.function_calls:
            print(f"Calling function: {call.name}({call.args})")
    else:
        print(response.text)
    

    
if __name__ == "__main__":
    main()