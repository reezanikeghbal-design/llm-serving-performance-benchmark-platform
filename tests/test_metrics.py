from app.benchmark.metrics import throughput, summarize

def test_throughput():
    assert throughput(20, 2_000_000_000) == 10

def test_throughput_missing_duration():
    assert throughput(20, None) is None

def test_summary():
    result = summarize([100, 200, 300])
    assert result["request_count"] == 3
    assert result["average_latency_ms"] == 200
