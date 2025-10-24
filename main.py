import os
from dotenv import load_dotenv
from google import genai


def main():
    load_dotenv("gem.env")
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    model = "gemini-2.0-flash-001"
    contents = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

    response = client.models.generate_content(model=model, contents=contents)

    print(response.text)
    usage = prompt.usage_metadata
    print(f"Prompt tokens: {usage.prompt_token_count}")
    print(f"Response tokens: {usage.candidates_token_count}")


if __name__ == "__main__":
    main()
