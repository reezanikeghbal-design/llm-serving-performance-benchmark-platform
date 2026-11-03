import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.config import settings


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(settings, "api_key", "test-secret")
    return TestClient(app)


def test_health_is_public(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.parametrize("path,method", [
    ("/models", "get"),
    ("/generate", "post"),
    ("/benchmark", "post"),
    ("/benchmark/results", "get"),
])
def test_operational_endpoints_require_api_key(client, path, method):
    kwargs = {"json": {"prompt": "test"}} if method == "post" else {}
    response = getattr(client, method)(path, **kwargs)
    assert response.status_code == 401


def test_operational_endpoint_accepts_api_key(client, monkeypatch):
    async def fake_models():
        return []
    from app.api import routes
    monkeypatch.setattr(routes.provider, "list_models", fake_models)
    response = client.get("/models", headers={"X-API-Key": "test-secret"})
    assert response.status_code == 200


def test_docs_available(client):
    assert client.get("/openapi.json").status_code == 200
