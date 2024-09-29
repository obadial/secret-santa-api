import pytest
from sqlmodel import Session, SQLModel, create_engine
from app.models import Participant
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, echo=True)


@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


def test_create_participant(session: Session):
    participant = Participant(name="John Doe")
    session.add(participant)
    session.commit()

    assert participant.id is not None
    assert participant.name == "John Doe"


def test_delete_participant(session: Session):
    participant = Participant(name="Jane Doe")
    session.add(participant)
    session.commit()

    session.delete(participant)
    session.commit()

    deleted_participant = session.get(Participant, participant.id)
    assert deleted_participant is None
