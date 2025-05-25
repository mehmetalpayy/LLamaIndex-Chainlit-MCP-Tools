from pydantic import BaseModel
from typing import Optional


class LLMConfig(BaseModel):
    model: str
    temperature: float = 0.0
    api_key: Optional[str] = None