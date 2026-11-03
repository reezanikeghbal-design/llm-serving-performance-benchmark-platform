import statistics

def throughput(tokens: int | None, duration_ns: int | None) -> float | None:
    if tokens is None or not duration_ns or duration_ns <= 0:
        return None
    return tokens / (duration_ns / 1_000_000_000)

def percentile(values: list[float], p: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, int((p / 100) * len(ordered) + 0.999999) - 1))
    return ordered[index]

def summarize(latencies: list[float]) -> dict:
    return {
        "request_count": len(latencies),
        "average_latency_ms": statistics.mean(latencies) if latencies else None,
        "p95_latency_ms": percentile(latencies, 95),
    }
