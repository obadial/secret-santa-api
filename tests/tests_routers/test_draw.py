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


def test_secret_santa_draw(reset_mock_session):
    # Créer une instance réelle de la liste par défaut
    mock_default_list = SecretSantaList(id=1, name="Default Secret Santa List")

    # Créer des instances réelles de participants
    mock_participants = [
        Participant(id=1, name="User 1", list_id=1),
        Participant(id=2, name="User 2", list_id=1),
        Participant(id=3, name="User 3", list_id=1),
    ]
    mock_blacklists = []

    with patch("app.routers.draw.get_default_list", return_value=mock_default_list):

        def mock_exec_side_effect(query):
            if "Participant" in str(query):
                mock_exec_result = MagicMock()
                mock_exec_result.all.return_value = mock_participants
                return mock_exec_result
            elif "Blacklist" in str(query):
                mock_exec_result = MagicMock()
                mock_exec_result.all.return_value = mock_blacklists
                return mock_exec_result
            else:
                mock_exec_result = MagicMock()
                mock_exec_result.first.return_value = mock_default_list
                return mock_exec_result

        mock_session.exec.side_effect = mock_exec_side_effect

        def mock_get(model, *args, **kwargs):
            id = kwargs.get("id", args[1] if len(args) > 1 else None)
            return next((p for p in mock_participants if p.id == id), None)

        mock_session.get.side_effect = mock_get

        # Effectuer la requête GET
        response = client.get("/v1/draw")

        print(response.status_code)
        print(response.json())

        assert response.status_code == 200
        assert len(response.json()) == 3
