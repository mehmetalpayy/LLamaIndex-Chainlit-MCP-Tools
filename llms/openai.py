from llama_index.llms.openai import OpenAI
from .base import LLMConfig


def get_openai_llm(config: LLMConfig = LLMConfig(model="gpt-4o")):
    return OpenAI(
        model=config.model,
        temperature=config.temperature,
        api_key=config.api_key
    )