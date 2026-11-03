import logging

from fastapi import APIRouter, Depends, HTTPException
from app.api.schemas import GenerateRequest, BenchmarkRequest
from app.services.ollama_service import OllamaService
from app.core.config import settings
from app.core.exceptions import OllamaUnavailable, ModelNotFound
from app.benchmark.runner import run_benchmark
from app.benchmark.reporter import save_report
from app.core.security import require_api_key

logger = logging.getLogger(__name__)

router = APIRouter()
provider = OllamaService()
benchmark_history = []

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.get("/models", dependencies=[Depends(require_api_key)])
async def models():
    try:
        return {"models": await provider.list_models()}
    except OllamaUnavailable:
        raise HTTPException(status_code=503, detail={"error": "ollama_unavailable"})

@router.post("/generate", dependencies=[Depends(require_api_key)])
async def generate(request: GenerateRequest):
    model = request.model or settings.default_model
    try:
        return await provider.generate(request.prompt, model, request.temperature,
                                       request.max_tokens, request.stream)
    except ModelNotFound:
        raise HTTPException(status_code=404, detail={"error": "model_not_found"})
    except TimeoutError:
        raise HTTPException(status_code=504, detail={"error": "ollama_timeout"})
    except OllamaUnavailable:
        raise HTTPException(status_code=503, detail={"error": "ollama_unavailable"})

@router.post("/benchmark", dependencies=[Depends(require_api_key)])
async def benchmark(request: BenchmarkRequest):
    report = await run_benchmark(provider, request.prompt, request.models, request.repeats,
                                 request.temperature, request.max_tokens)
    paths = save_report(report)
    report["report_files"] = paths
    benchmark_history.append(report)
    return report

@router.get("/benchmark/results", dependencies=[Depends(require_api_key)])
async def benchmark_results():
    return {"experiments": benchmark_history}
