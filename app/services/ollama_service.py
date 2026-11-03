import httpx
from app.core.config import settings
from app.core.exceptions import OllamaUnavailable, ModelNotFound
from app.services.model_provider import ModelProvider

class OllamaService(ModelProvider):
    def __init__(self):
        self.base_url = settings.ollama_base_url.rstrip("/")
        self.timeout = settings.request_timeout

    async def list_models(self):
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                response.raise_for_status()
                return response.json().get("models", [])
        except httpx.HTTPError as exc:
            raise OllamaUnavailable("Could not connect to Ollama") from exc

    async def generate(self, prompt, model, temperature, max_tokens, stream=False):
        payload = {
            "model": model, "prompt": prompt, "stream": False,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        }
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(f"{self.base_url}/api/generate", json=payload)
                if response.status_code == 404:
                    raise ModelNotFound(f"Model '{model}' was not found")
                response.raise_for_status()
                data = response.json()
                return {
                    "model": model,
                    "response": data.get("response", ""),
                    "total_duration_ns": data.get("total_duration"),
                    "load_duration_ns": data.get("load_duration"),
                    "prompt_tokens": data.get("prompt_eval_count"),
                    "generated_tokens": data.get("eval_count"),
                    "generation_duration_ns": data.get("eval_duration"),
                    "done": data.get("done", True),
                }
        except ModelNotFound:
            raise
        except httpx.TimeoutException as exc:
            raise TimeoutError("Ollama request timed out") from exc
        except httpx.HTTPError as exc:
            raise OllamaUnavailable("Could not connect to Ollama") from exc
