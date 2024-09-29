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


import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from sqlmodel import Session, select
from app.main import app
from app.utils.list_utils import get_session
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


def test_add_to_blacklist(reset_mock_session):
    mock_participant = Participant(id=1, name="User 1", list_id=1)
    mock_blacklisted_participant = Participant(id=2, name="User 2", list_id=1)
    mock_default_list = SecretSantaList(id=1, name="Default Secret Santa List")

    with patch("app.routers.blacklist.get_default_list", return_value=mock_default_list):

        def mock_get(model, *args, **kwargs):
            id = kwargs.get("id", args[1] if len(args) > 1 else None)
            if model == Participant and id == 1:
                return mock_participant
            elif model == Participant and id == 2:
                return mock_blacklisted_participant
            else:
                return None

        mock_session.get.side_effect = mock_get

        mock_session.add.return_value = None
        mock_session.commit.return_value = None

        response = client.post(
            "/v1/blacklist", json={"participant_id": 1, "blacklisted_participant_id": 2}
        )

        print(response.status_code)
        print(response.json())

        assert response.status_code == 200
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
