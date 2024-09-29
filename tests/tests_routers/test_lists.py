import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.utils.list_utils import get_session
from sqlmodel import Session
from app.models import SecretSantaList, Participant
from httpx import WSGITransport

mock_session = MagicMock(spec=Session)
app.dependency_overrides[get_session] = lambda: mock_session

transport = WSGITransport(app=app)
client = TestClient(transport=transport)


@pytest.fixture
def reset_mock_session():
    mock_session.reset_mock()
    yield


def test_create_list(reset_mock_session):
    mock_list = SecretSantaList(id=1, name="Holiday 2024")

    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.side_effect = lambda x: x

    response = client.post("/v1/lists", json={"name": "Holiday 2024"})

    assert response.status_code == 200
    assert response.json()["name"] == "Holiday 2024"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


def test_delete_list(reset_mock_session):
    mock_list = SecretSantaList(id=1, name="Holiday 2024")

    mock_session.get.return_value = mock_list
    mock_session.delete.return_value = None
    mock_session.commit.return_value = None

    response = client.delete("/v1/lists/1")

    assert response.status_code == 200
    assert (
        response.json()["message"]
        == "List with id: 1 and all associated participants have been removed"
    )
    mock_session.delete.assert_called_once()
    mock_session.commit.assert_called_once()


def test_list_with_participants(reset_mock_session):
    mock_list = SecretSantaList(id=1, name="Holiday 2024")
    mock_participants = [
        Participant(id=1, name="User 1", list_id=1),
        Participant(id=2, name="User 2", list_id=1),
    ]

    mock_session.exec.side_effect = [
        MagicMock(all=MagicMock(return_value=[mock_list])),
        MagicMock(all=MagicMock(return_value=mock_participants)),
    ]

    response = client.get("/v1/lists/with-participants")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(response.json()[0]["participants"]) == 2
    assert response.json()[0]["participants"][0]["name"] == "User 1"
    mock_session.exec.assert_called()
