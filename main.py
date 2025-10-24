import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

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

    return client.models.generate_content(model=model, contents=messages)

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

    print(response.text)
    

    
if __name__ == "__main__":
    main()