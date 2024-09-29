import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.utils.list_utils import get_session
from sqlmodel import Session, select
from app.models import SecretSantaList, Participant
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

mock_session = MagicMock(spec=Session)
app.dependency_overrides[get_session] = lambda: mock_session

client = TestClient(app)


@pytest.fixture
def reset_mock_session():
    mock_session.reset_mock()
    yield


def test_create_list(reset_mock_session):
    mock_list = SecretSantaList(name="Holiday 2024")

    mock_session.add.side_effect = lambda obj: setattr(
        obj, "id", 1
    )  # Simuler l'assignation de l'ID
    mock_session.commit.return_value = None

    response = client.post("/v1/lists", params={"name": "Holiday 2024"})

    print(response.status_code)
    print(response.json())

    assert response.status_code == 200
    assert response.json()["name"] == "Holiday 2024"
    assert response.json()["id"] == 1
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


def test_delete_list(reset_mock_session):
    mock_list = SecretSantaList(id=1, name="Holiday 2024")
    mock_participant = Participant(id=1, name="User 1", list_id=1)

    mock_session.get.return_value = mock_list

    def mock_exec_side_effect(query):
        if "Participant" in str(query):
            mock_exec_result = MagicMock()
            mock_exec_result.all.return_value = [mock_participant]
            return mock_exec_result
        else:
            mock_exec_result = MagicMock()
            mock_exec_result.first.return_value = mock_list
            return mock_exec_result

    mock_session.exec.side_effect = mock_exec_side_effect
    mock_session.delete.return_value = None
    mock_session.commit.return_value = None

    response = client.delete("/v1/lists/1")

    print(response.status_code)
    print(response.json())

    assert response.status_code == 200
    assert (
        response.json()["message"]
        == "List with id: 1 and all associated participants have been removed"
    )
    assert mock_session.delete.call_count == 2
    mock_session.commit.assert_called_once()


def test_list_with_participants(reset_mock_session):
    mock_list = SecretSantaList(id=1, name="Holiday 2024")
    mock_participants = [
        Participant(id=1, name="User 1", list_id=1),
        Participant(id=2, name="User 2", list_id=1),
    ]

    def mock_exec_side_effect(query):
        if "select secretsantalist" in str(query).lower():
            mock_exec_result = MagicMock()
            mock_exec_result.all.return_value = [mock_list]
            return mock_exec_result
        elif "select participant" in str(query).lower():
            mock_exec_result = MagicMock()
            mock_exec_result.all.return_value = mock_participants
            return mock_exec_result
        else:
            return MagicMock()

    mock_session.exec.side_effect = mock_exec_side_effect

    response = client.get("/v1/lists/with-participants")

    print(response.status_code)
    print(response.json())

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(response.json()[0]["participants"]) == 2
    assert response.json()[0]["participants"][0]["name"] == "User 1"
