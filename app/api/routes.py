from fastapi import APIRouter, HTTPException
from app.api.schemas import GenerateRequest, BenchmarkRequest
from app.services.ollama_service import OllamaService
from app.core.config import settings
from app.core.exceptions import OllamaUnavailable, ModelNotFound
from app.benchmark.runner import run_benchmark
from app.benchmark.reporter import save_report

router = APIRouter()
provider = OllamaService()
benchmark_history = []

@router.get("/health")
async def health():
    try:
        models = await provider.list_models()
        return {"status": "ok", "ollama": "connected", "available_models": len(models)}
    except OllamaUnavailable:
        raise HTTPException(status_code=503, detail={"error": "ollama_unavailable"})

@router.get("/models")
async def models():
    try:
        return {"models": await provider.list_models()}
    except OllamaUnavailable:
        raise HTTPException(status_code=503, detail={"error": "ollama_unavailable"})

@router.post("/generate")
async def generate(request: GenerateRequest):
    model = request.model or settings.default_model
    try:
        return await provider.generate(request.prompt, model, request.temperature,
                                       request.max_tokens, request.stream)
    except ModelNotFound as exc:
        raise HTTPException(status_code=404, detail={"error": "model_not_found", "message": str(exc)})
    except TimeoutError as exc:
        raise HTTPException(status_code=504, detail={"error": "ollama_timeout", "message": str(exc)})
    except OllamaUnavailable:
        raise HTTPException(status_code=503, detail={"error": "ollama_unavailable"})

@router.post("/benchmark")
async def benchmark(request: BenchmarkRequest):
    report = await run_benchmark(provider, request.prompt, request.models, request.repeats,
                                 request.temperature, request.max_tokens)
    paths = save_report(report)
    report["report_files"] = paths
    benchmark_history.append(report)
    return report

@router.get("/benchmark/results")
async def benchmark_results():
    return {"experiments": benchmark_history}
