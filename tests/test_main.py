import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app, get_session
from sqlmodel import Session, select
from app.models.participant import Participant


mock_session = MagicMock(spec=Session)
app.dependency_overrides[get_session] = lambda: mock_session

client = TestClient(app)


@pytest.fixture
def reset_mock_session():
    mock_session.reset_mock()
    yield


def test_create_participant(reset_mock_session):
    mock_participant = Participant(id=1, name="Test User")

    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.side_effect = lambda x: x

    response = client.post("/participants", json={"name": "Test User"})

    assert response.status_code == 200
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


def test_get_participants(reset_mock_session):
    mock_participants = [
        Participant(id=1, name="User 1"),
        Participant(id=2, name="User 2"),
    ]

    # Simule l'objet retourné par session.exec().all()
    mock_exec_result = MagicMock()
    mock_exec_result.all.return_value = mock_participants
    mock_session.exec.return_value = mock_exec_result

    response = client.get("/participants")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "User 1"
    mock_session.exec.assert_called_once()


def test_add_to_blacklist(reset_mock_session):
    mock_participant = Participant(id=1, name="User 1")
    mock_blacklisted_participant = Participant(id=2, name="User 2")

    mock_session.get.side_effect = lambda model, id: (
        mock_participant if id == 1 else mock_blacklisted_participant
    )
    mock_session.add.return_value = None
    mock_session.commit.return_value = None

    response = client.post(
        "/blacklist", json={"participant_id": 1, "blacklisted_participant_id": 2}
    )

    assert response.status_code == 200
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


def test_secret_santa_draw(reset_mock_session):
    mock_participants = [
        Participant(id=1, name="User 1"),
        Participant(id=2, name="User 2"),
        Participant(id=3, name="User 3"),
    ]
    mock_blacklists = []

    mock_exec_result_participants = MagicMock()
    mock_exec_result_participants.all.return_val
