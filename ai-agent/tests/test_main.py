"""
Example tests for the AI Agent
"""
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Fixture for test client"""
    from ai_agent.main import app
    return TestClient(app)


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_chat_endpoint(client):
    """Test chat endpoint"""
    payload = {"query": "What is 2 + 2?"}
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    assert "response" in response.json()


def test_metrics_endpoint(client):
    """Test metrics endpoint"""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "agent_requests_total" in response.json()
