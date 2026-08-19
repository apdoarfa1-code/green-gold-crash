import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "Green Gold Crash Engine"}


def test_recent_rounds_endpoint():
    response = client.get("/api/v1/rounds/recent?count=10")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
