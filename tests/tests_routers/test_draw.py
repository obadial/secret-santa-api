import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.utils.list_utils import get_session
from sqlmodel import Session
from app.models import Participant
from httpx import WSGITransport

mock_session = MagicMock(spec=Session)
app.dependency_overrides[get_session] = lambda: mock_session

transport = WSGITransport(app=app)
client = TestClient(transport=transport)


@pytest.fixture
def reset_mock_session():
    mock_session.reset_mock()
    yield


def test_secret_santa_draw(reset_mock_session):
    mock_participants = [
        Participant(id=1, name="User 1"),
        Participant(id=2, name="User 2"),
        Participant(id=3, name="User 3"),
    ]
    mock_blacklists = []

    mock_session.exec.side_effect = [
        MagicMock(all=MagicMock(return_value=mock_participants)),
        MagicMock(all=MagicMock(return_value=mock_blacklists)),
    ]

    response = client.get("/v1/draw")

    assert response.status_code == 200
    assert len(response.json()) == 3
    mock_session.exec.assert_called()
