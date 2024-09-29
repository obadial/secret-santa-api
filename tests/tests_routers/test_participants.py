import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app.main import app
from app.utils.list_utils import get_session
from sqlmodel import Session
from app.models import Participant, SecretSantaList
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

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

    response = client.post("/v1/participants", json={"name": "Test User"})

    assert response.status_code == 200
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


def test_get_participants(reset_mock_session):
    mock_default_list = SecretSantaList(id=1, name="Default List")
    mock_participants = [
        Participant(id=1, name="User 1", list_id=1),
        Participant(id=2, name="User 2", list_id=1),
    ]

    with patch("app.utils.list_utils.get_default_list", return_value=mock_default_list):
        mock_exec_result = MagicMock()
        mock_exec_result.all.return_value = mock_participants
        mock_session.exec.return_value = mock_exec_result

        response = client.get("/v1/participants")

        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]["name"] == "User 1"


def test_delete_participant(reset_mock_session):
    mock_default_list = SecretSantaList(id=1, name="Default Secret Santa List")
    mock_participant = Participant(id=1, name="User 1", list_id=1)

    with patch(
        "app.routers.participants.get_default_list", return_value=mock_default_list
    ):
        mock_session.get.return_value = mock_participant
        mock_session.delete.return_value = None
        mock_session.commit.return_value = None

        response = client.delete("/v1/participants/1")

        print(response.status_code)
        print(response.json())

        assert response.status_code == 200
        assert (
            response.json()["message"]
            == "Participant User 1 (id: 1) removed from default list"
        )
        mock_session.delete.assert_called_once()
        mock_session.commit.assert_called_once()
