import pytest
from sqlmodel import Session, SQLModel, create_engine
from app.models.participant import Participant

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
