import os
import sys
from dotenv import load_dotenv
from google import genai

def inputchecker(input):
    input_string = ""
    if len(input) < 2:
        print("Error: prompt not provided.")
        sys.exit(1)
    else:
        for i in range(1, len(input)):
            input_string += input[i] + " "
        print(f"input is: {input_string}")
        return input_string

def ask_gemini(prompt):
    load_dotenv("gem.env")
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    model = "gemini-2.0-flash-001"

    return client.models.generate_content(model=model, contents=prompt)

def main():

    user_input = sys.argv
    prompt = inputchecker(user_input)

    response = ask_gemini(prompt)

    print(response.text)
    usage = response.usage_metadata
    print(f"Prompt tokens: {usage.prompt_token_count}")
    print(f"Response tokens: {usage.candidates_token_count}")

if __name__ == "__main__":
    main()