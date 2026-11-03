from pydantic import BaseModel, Field

class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=20000)
    model: str | None = None
    temperature: float = Field(default=0.2, ge=0, le=2)
    max_tokens: int = Field(default=128, ge=1, le=4096)
    stream: bool = False

class BenchmarkRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=20000)
    models: list[str] = Field(min_length=1)
    repeats: int = Field(default=2, ge=1, le=20)
    temperature: float = Field(default=0.2, ge=0, le=2)
    max_tokens: int = Field(default=128, ge=1, le=4096)
