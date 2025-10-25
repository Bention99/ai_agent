import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import *
from functions.get_file_content import *
from functions.run_python_file import *
from functions.write_file import *

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

def call_function(function_call_part, verbose=False):
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    FUNCTIONS = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
    }

    args = function_call_part.args
    function = function_call_part.name

    callable_fn = FUNCTIONS.get(function)

    if callable_fn == None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function,
                    response={"error": f"Unknown function: {function}"},
                )
            ],
        )

    kwargs = args.copy()
    kwargs["working_directory"] = "./calculator"
    answer = callable_fn(**kwargs)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function,
                response={"result": answer},
            )
        ],
    )

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

            function_response = call_function(call, verbose)

            if not function_response.parts or not getattr(function_response.parts[0], "function_response", None):
                raise Exception(f"Fatal exception for Function: {call.name} ")
            
            resp = function_response.parts[0].function_response.response
            out = resp.get("result") if isinstance(resp, dict) else resp
            
            print(f"-> {out}")

    else:
        print(response.text)
    

    
if __name__ == "__main__":
    main()