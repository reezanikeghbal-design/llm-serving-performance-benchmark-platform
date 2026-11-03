from fastapi import FastAPI
from app.api.routes import router
from app.core.logging import configure_logging
from app.monitoring.prometheus import instrumentator

configure_logging()
app = FastAPI(title="LLM Serving & Performance Benchmark Platform", version="1.0.0")
app.include_router(router)
instrumentator.instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)
