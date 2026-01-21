import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_chat_endpoint():
    """Test the chat endpoint with valid input"""
    response = client.post("/chat", json={"message": "J'ai mal à la tête"})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert isinstance(data["response"], str)
    assert len(data["response"]) > 0

def test_chat_endpoint_empty_message():
    """Test chat endpoint with empty message"""
    response = client.post("/chat", json={"message": ""})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data

def test_chat_endpoint_invalid_data():
    """Test chat endpoint with invalid data"""
    response = client.post("/chat", json={})
    assert response.status_code == 422  # Validation error

def test_chat_medical_responses():
    """Test specific medical responses"""
    test_cases = [
        ("mal à la tête", "repos"),
        ("fièvre", "température"),
        ("toux", "hydratation"),
        ("douleur", "consultez")
    ]

    for symptom, expected_keyword in test_cases:
        response = client.post("/chat", json={"message": f"J'ai {symptom}"})
        assert response.status_code == 200
        data = response.json()
        assert expected_keyword.lower() in data["response"].lower()
