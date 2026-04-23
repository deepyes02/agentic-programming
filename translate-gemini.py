import os
import json
import dotenv
from google import genai

dotenv.load_dotenv()


def main():
    client = genai.Client(api_key=os.environ.get("GOOGLE_AI_STUDIO_KEY"))

    language_pack = [
        {"name": "English", "code": "en"},
        {"name": "Japanese", "code": "ja"},
        {"name": "Nepali", "code": "ne"},
        {"name": "Hindi", "code": "hi"},
        {"name": "Indonesian", "code": "id"},
        {"name": "Tagalog", "code": "tl"},
        {"name": "Vietnamese", "code": "vi"},
    ]

    target_languages_str = ", ".join([lang["name"] for lang in language_pack])
    text_to_translate = "Please note that server maintenance is going be held on 4/20 from 15:00 to 16:00. Change the payment limit for SG Better error code handling for PNB PNB SG Credentials"

    prompt = f"""
    You are a professional translator. 
    Translate the following text from English into the following languages: {target_languages_str}. When translating, also translate numbers if digits exist in local language.
    
    Text: {text_to_translate}

    Return the result as a JSON object where the keys are the language names and the values are the translations. 
    Ensure the translations accurately convey the meaning and nuances of the original text while adhering to each language's grammar, vocabulary, and conversational relevance.
    Produce ONLY the JSON object.
    """

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-preview",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
        },
    )

    try:
        translations = json.loads(response.text)
    except json.JSONDecodeError:
        print("Error: Model did not return valid JSON.")
        print(response.text)
        return

    output_lines = [text_to_translate]

    for lang in language_pack:
        res = translations.get(lang["name"], "Translation missing")
        output = f"Translation in {lang['name']}:\n{res}\n"
        print(output)
        output_lines.append(output)

    # Writing to file
    with open("results.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(translations, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
