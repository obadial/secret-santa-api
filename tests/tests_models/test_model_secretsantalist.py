import pytest
from sqlmodel import Session, SQLModel, create_engine
from app.models.secretsantalist import SecretSantaList
from app.models.participant import Participant

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, echo=True)


@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


def test_create_secret_santa_list(session: Session):
    santa_list = SecretSantaList(name="Christmas 2024")
    session.add(santa_list)
    session.commit()

    assert santa_list.id is not None
    assert santa_list.name == "Christmas 2024"


def test_add_participants_to_list(session: Session):
    santa_list = SecretSantaList(name="New Year 2024")
    session.add(santa_list)
    session.commit()

    participant1 = Participant(name="John Doe", list_id=santa_list.id)
    participant2 = Participant(name="Jane Doe", list_id=santa_list.id)
    session.add(participant1)
    session.add(participant2)
    session.commit()

    assert participant1.id is not None
    assert participant2.id is not None
    assert participant1.list_id == santa_list.id
    assert participant2.list_id == santa_list.id
