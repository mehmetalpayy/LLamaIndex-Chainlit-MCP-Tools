from llama_index.llms.anthropic import Anthropic
from .base import LLMConfig


def get_claude_llm(config: LLMConfig = LLMConfig(model="claude-3-5-sonnet-20241022")):
    return Anthropic(
        model=config.model,
        temperature=config.temperature,
        api_key=config.api_key
    )