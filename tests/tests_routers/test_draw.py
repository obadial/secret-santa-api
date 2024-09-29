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
    mock_default_list = SecretSantaList(id=1, name="Default List")
    mock_participants = [
        Participant(id=1, name="User 1", list_id=1),
        Participant(id=2, name="User 2", list_id=1),
        Participant(id=3, name="User 3", list_id=1),
    ]
    mock_blacklists = []

    with patch("app.routers.draw.get_default_list", return_value=mock_default_list):
        mock_session.exec.side_effect = [
            MagicMock(all=MagicMock(return_value=mock_participants)),
            MagicMock(all=MagicMock(return_value=mock_blacklists)),
        ]

        response = client.get("/v1/draw")

        assert response.status_code == 200
        assert len(response.json()) == 3
