import logging
import time
import uuid
from datetime import datetime, timezone
from app.benchmark.metrics import throughput, summarize
from app.benchmark.resources import resource_snapshot

logger = logging.getLogger(__name__)

async def run_benchmark(provider, prompt, models, repeats, temperature, max_tokens):
    experiment_id = str(uuid.uuid4())
    results = []
    for model in models:
        runs = []
        for _ in range(repeats):
            resources_before = resource_snapshot()
            started = time.perf_counter()
            try:
                result = await provider.generate(prompt, model, temperature, max_tokens)
                latency = (time.perf_counter() - started) * 1000
                resources_after = resource_snapshot()
                runs.append({
                    "success": True, "latency_ms": round(latency, 3),
                    "prompt_tokens": result["prompt_tokens"],
                    "generated_tokens": result["generated_tokens"],
                    "throughput_tokens_per_second": throughput(
                        result["generated_tokens"], result["generation_duration_ns"]),
                    "resources_before": resources_before,
                    "resources_after": resources_after,
                })
            except Exception:
                logger.exception("Benchmark generation failed for model %s", model)
                runs.append({"success": False, "error": "generation_failed"})
        latencies = [r["latency_ms"] for r in runs if r["success"]]
        summary = summarize(latencies)
        successes = [r for r in runs if r["success"]]
        rates = [r["throughput_tokens_per_second"] for r in successes
                 if r["throughput_tokens_per_second"] is not None]
        results.append({
            "model": model, "temperature": temperature, "max_tokens": max_tokens,
            **summary, "successful_requests": len(successes),
            "failed_requests": len(runs) - len(successes),
            "success_rate": len(successes) / len(runs) if runs else 0,
            "average_throughput_tokens_per_second": sum(rates) / len(rates) if rates else None,
            "runs": runs,
        })
    return {
        "experiment_id": experiment_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "prompt": prompt, "results": results,
    }
