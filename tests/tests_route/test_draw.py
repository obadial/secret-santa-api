from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_draw_with_participants():
    client.post("/participants", json={"name": "John Doe"})
    client.post("/participants", json={"name": "Jane Smith"})

    response = client.get("/draw")
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    for pairing in data:
        assert "gifter_id" in pairing
        assert "gifter_name" in pairing
        assert "receiver_id" in pairing
        assert "receiver_name" in pairing


def test_draw_not_enough_participants():
    client.post("/participants", json={"name": "John Doe"})

    response = client.get("/draw")

    assert response.status_code == 400
    assert response.json() == {"detail": "Not enough participants for the draw."}
