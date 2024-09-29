import pytest
from sqlmodel import Session, SQLModel, create_engine
from app.models.blacklist import Blacklist
from app.models.participant import Participant
from app.models.secretsantalist import SecretSantaList

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, echo=True)


@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


def test_create_blacklist(session: Session):
    santa_list = SecretSantaList(name="Test List")
    session.add(santa_list)
    session.commit()

    participant1 = Participant(name="Alice", list_id=santa_list.id)
    participant2 = Participant(name="Bob", list_id=santa_list.id)
    session.add(participant1)
    session.add(participant2)
    session.commit()

    blacklist_entry = Blacklist(
        participant_id=participant1.id,
        blacklisted_participant_id=participant2.id,
        list_id=santa_list.id,
    )
    session.add(blacklist_entry)
    session.commit()

    assert blacklist_entry.id is not None
    assert blacklist_entry.participant_id == participant1.id
    assert blacklist_entry.blacklisted_participant_id == participant2.id
    assert blacklist_entry.list_id == santa_list.id
