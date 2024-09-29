import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app, get_session
from sqlmodel import Session
from app.models.participant import Participant
from app.models.secretsantalist import SecretSantaList
from app.models.blacklist import Blacklist


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

    # Création de participant dans la liste par défaut
    response = client.post("/participants", json={"name": "Test User"})

    assert response.status_code == 200
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


def test_get_participants(reset_mock_session):
    mock_participants = [
        Participant(id=1, name="User 1"),
        Participant(id=2, name="User 2"),
    ]

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
    mock_exec_result_participants.all.return_value = mock_participants
    mock_exec_result_blacklists = MagicMock()
    mock_exec_result_blacklists.all.return_value = mock_blacklists

    mock_session.exec.side_effect = [
        mock_exec_result_participants,  # First call for participants
        mock_exec_result_blacklists,  # Second call for blacklists
    ]

    response = client.get("/draw")

    assert response.status_code == 200
    assert len(response.json()) == 3
    mock_session.exec.assert_called()


# Tests for new Secret Santa List routes
def test_create_secret_santa_list(reset_mock_session):
    mock_list = SecretSantaList(id=1, name="Tatooine-123456")

    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.side_effect = lambda x: x

    response = client.post("/lists", json={})

    assert response.status_code == 200
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


def test_create_participant_for_list(reset_mock_session):
    mock_list = SecretSantaList(id=1, name="Tatooine-123456")
    mock_participant = Participant(id=1, name="Test User", list_id=mock_list.id)

    mock_session.get.return_value = mock_list
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.side_effect = lambda x: x

    response = client.post("/lists/1/participants", json={"name": "Test User"})

    assert response.status_code == 200
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


def test_get_participants_for_list(reset_mock_session):
    mock_list = SecretSantaList(id=1, name="Tatooine-123456")
    mock_participants = [
        Participant(id=1, name="User 1", list_id=mock_list.id),
        Participant(id=2, name="User 2", list_id=mock_list.id),
    ]

    mock_session.get.return_value = mock_list
    mock_exec_result = MagicMock()
    mock_exec_result.all.return_value = mock_participants
    mock_session.exec.return_value = mock_exec_result

    response = client.get("/lists/1/participants")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "User 1"
    mock_session.exec.assert_called_once()


def test_secret_santa_draw_for_list(reset_mock_session):
    mock_list = SecretSantaList(id=1, name="Tatooine-123456")
    mock_participants = [
        Participant(id=1, name="User 1", list_id=mock_list.id),
        Participant(id=2, name="User 2", list_id=mock_list.id),
        Participant(id=3, name="User 3", list_id=mock_list.id),
    ]
    mock_blacklists = []

    mock_session.get.return_value = mock_list
    mock_exec_result_participants = MagicMock()
    mock_exec_result_participants.all.return_value = mock_participants
    mock_exec_result_blacklists = MagicMock()
    mock_exec_result_blacklists.all.return_value = mock_blacklists

    mock_session.exec.side_effect = [
        mock_exec_result_participants,  # First call for participants
        mock_exec_result_blacklists,  # Second call for blacklists
    ]

    response = client.get("/lists/1/draw")

    assert response.status_code == 200
    assert len(response.json()) == 3
    mock_session.exec.assert_called()
