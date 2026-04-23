from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from pydantic import SecretStr
import dotenv

dotenv.load_dotenv()


def load_model():
    model_name = os.environ.get("MODEL", "qwen2.5-coder:latest")
    google_api_key = os.environ.get("GOOGLE_AI_STUDIO_KEY")
    deepseek_api_key = os.environ.get("DEEPSEEK_API_KEY")

    if deepseek_api_key and model_name.startswith("deepseek"):
        return ChatOpenAI(
            base_url="https://api.deepseek.com/v1",
            model=model_name,
            api_key=SecretStr(deepseek_api_key),
            temperature=0.2,
            max_tokens=int(os.environ.get("MAX_TOKENS", 4096)),
        )

    if google_api_key and model_name.startswith("gemini"):
        return ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=SecretStr(google_api_key),
            temperature=0.2,
            max_output_tokens=int(os.environ.get("MAX_TOKENS", 4096)),
        )

    return ChatOpenAI(
        base_url=os.environ.get("INFERENCE_API_URL"),
        model=model_name,
        api_key=SecretStr(os.environ.get("OPENAI_API_KEY") or "EMPTY"),
        temperature=0.2,
        top_p=0.95,
        presence_penalty=1.1,
        frequency_penalty=1.0,
        max_tokens=int(os.environ.get("MAX_TOKENS", 4096)),
    )
