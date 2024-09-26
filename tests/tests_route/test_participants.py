from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_valid_participant():
    response = client.post("/participants", json={"name": "John Doe"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    assert "id" in data


def test_create_invalid_participant_name_too_long():
    response = client.post(
        "/participants", json={"name": "A" * 51}
    )  # Name exceeds 50 characters
    assert response.status_code == 422  # Unprocessable entity (validation error)
