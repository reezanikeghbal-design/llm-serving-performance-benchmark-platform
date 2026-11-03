import pytest
from app.benchmark.runner import run_benchmark

class FakeProvider:
    async def generate(self, prompt, model, temperature, max_tokens, stream=False):
        return {"prompt_tokens": 4, "generated_tokens": 8, "generation_duration_ns": 1_000_000_000}

@pytest.mark.asyncio
async def test_runner():
    report = await run_benchmark(FakeProvider(), "hello", ["fake"], 2, 0.2, 32)
    assert report["results"][0]["successful_requests"] == 2
    assert report["results"][0]["average_throughput_tokens_per_second"] == 8
