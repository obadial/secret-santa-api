import pytest
from sqlmodel import Session, SQLModel, create_engine, select
from app.models import SecretSantaList, Participant

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, echo=True)


@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


def test_create_list(session: Session):
    santa_list = SecretSantaList(name="Holiday 2024")
    session.add(santa_list)
    session.commit()

    assert santa_list.id is not None
    assert santa_list.name == "Holiday 2024"


def test_delete_list(session: Session):
    santa_list = SecretSantaList(name="Holiday 2024")
    session.add(santa_list)
    session.commit()

    session.delete(santa_list)
    session.commit()

    deleted_list = session.get(SecretSantaList, santa_list.id)
    assert deleted_list is None


def test_list_with_participants(session: Session):
    santa_list = SecretSantaList(name="Holiday 2024")
    session.add(santa_list)
    session.commit()

    participant = Participant(name="John Doe", list_id=santa_list.id)
    session.add(participant)
    session.commit()

    participants = session.exec(
        select(Participant).where(Participant.list_id == santa_list.id)
    ).all()

    assert len(participants) == 1
    assert participants[0].name == "John Doe"
