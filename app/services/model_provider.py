from abc import ABC, abstractmethod

class ModelProvider(ABC):
    @abstractmethod
    async def list_models(self) -> list[dict]: ...

    @abstractmethod
    async def generate(self, prompt: str, model: str, temperature: float,
                       max_tokens: int, stream: bool = False) -> dict: ...
