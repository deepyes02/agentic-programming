import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from pydantic import SecretStr
import dotenv

dotenv.load_dotenv()


def main():
    llm = ChatOpenAI(
        base_url=os.environ.get("INFERENCE_API_URL"),
        model=os.environ.get("TRANSLATION_MODEL"),
        api_key=SecretStr(os.environ.get("OPENAI_API_KEY") or "EMPTY"),
        temperature=0.0,
        top_p=0.80,
        presence_penalty=0.0,
        frequency_penalty=0.0,
        max_tokens=int(os.environ.get("MAX_TOKENS", 4096)),  # Convert to int
    )

    def translate(q, source_lang, source_code, target_lang, target_code):
        translate_prompt = f"""
        You are a professional {source_lang} ({source_code}) to {target_lang} ({target_code}) translator. Your goal is to accurately convey the meaning and nuances of the original {source_lang} text while adhering to {target_lang} meaning, grammar, vocabulary, and conversational relevance. Produce only the {target_lang} translation, without any additional explanations or commentary. Please translate the following {source_lang} text into {target_lang}:\n\n{q}
        """
        return llm.invoke([HumanMessage(content=translate_prompt)]).content

    language_pack = [
        {"name": "Japanese", "code": "ja"},
        {"name": "Nepali", "code": "ne"},
        {"name": "Hindi", "code": "hi"},
        {"name": "Indonesian", "code": "id"},
        {"name": "Tagalog", "code": "tl"},
        {"name": "Vietnamese", "code": "vi"},
    ]

    text_to_translate = "We will be closed this Christmas for a week."

    output_lines = []

    output_lines.append(text_to_translate)

    # Iterating through language pack
    for lang in language_pack:
        res = translate(text_to_translate, "English", "en", lang["name"], lang["code"])
        output = f"Translation in {lang['name']}:\n{res}\n"
        print(output)
        output_lines.append(output)

    # Writing to file
    with open("results.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))


if __name__ == "__main__":
    main()
