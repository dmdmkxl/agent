"""LLM client helpers."""

import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL") or os.getenv("OPENAI_API_BASE")

    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY in .env")

    return OpenAI(api_key=api_key, base_url=base_url)


def get_model_name() -> str:
    return os.getenv("MODEL_NAME", "gpt-4.1-mini")

