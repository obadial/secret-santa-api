from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_add_valid_blacklist():
    client.post("/participants", json={"name": "Alice"})
    client.post("/participants", json={"name": "Bob"})

    response = client.post(
        "/blacklist", json={"participant_id": 1, "blacklisted_participant_id": 2}
    )
    assert response.status_code == 200


def test_add_invalid_blacklist_ids():
    response = client.post(
        "/blacklist", json={"participant_id": -1, "blacklisted_participant_id": -2}
    )
    assert response.status_code == 422
