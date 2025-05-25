from llama_index.llms.gemini import Gemini
from .base import LLMConfig


def get_gemini_llm(config: LLMConfig = LLMConfig(model="gemini-1.5-flash")):
    return Gemini(
        model=config.model,
        temperature=config.temperature,
        api_key=config.api_key
    )