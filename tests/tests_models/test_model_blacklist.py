import pytest
from sqlmodel import Session, SQLModel, create_engine
from app.models.blacklist import Blacklist
from app.models.participant import Participant

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, echo=True)


@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


def test_create_blacklist(session: Session):
    participant1 = Participant(name="Alice")
    participant2 = Participant(name="Bob")
    session.add(participant1)
    session.add(participant2)
    session.commit()

    blacklist_entry = Blacklist(
        participant_id=participant1.id, blacklisted_participant_id=participant2.id
    )
    session.add(blacklist_entry)
    session.commit()

    assert blacklist_entry.id is not None
    assert blacklist_entry.participant_id == participant1.id
    assert blacklist_entry.blacklisted_participant_id == participant2.id
