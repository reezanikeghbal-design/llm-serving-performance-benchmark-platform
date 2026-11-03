from fastapi.testclient import TestClient
from app.main import app

def test_generate_validation():
    client = TestClient(app)
    response = client.post("/generate", json={"prompt": ""})
    assert response.status_code == 422

def test_docs_available():
    client = TestClient(app)
    assert client.get("/openapi.json").status_code == 200
