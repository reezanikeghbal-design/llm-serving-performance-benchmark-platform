from typing import Annotated
from pydantic import BaseModel, Field

class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=20000)
    model: str | None = None
    temperature: float = Field(default=0.2, ge=0, le=2)
    max_tokens: int = Field(default=128, ge=1, le=4096)
    stream: bool = False

class BenchmarkRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=20000)
    models: list[Annotated[str, Field(min_length=1, max_length=128)]] = Field(min_length=1, max_length=5)
    repeats: int = Field(default=2, ge=1, le=10)
    temperature: float = Field(default=0.2, ge=0, le=2)
    max_tokens: int = Field(default=128, ge=1, le=4096)
