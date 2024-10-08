from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List


class SecretSantaList(SQLModel, table=True):
    __tablename__ = "secret_santa_list"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class Participant(SQLModel, table=True):
    __tablename__ = "participant"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    list_id: Optional[int] = Field(default=None, foreign_key="secret_santa_list.id")


class Blacklist(SQLModel, table=True):
    __tablename__ = "blacklist"

    id: Optional[int] = Field(default=None, primary_key=True)
    participant_id: Optional[int] = Field(default=None, foreign_key="participant.id")
    blacklisted_participant_id: Optional[int] = Field(
        default=None, foreign_key="participant.id"
    )
    list_id: Optional[int] = Field(default=None, foreign_key="secret_santa_list.id")


SecretSantaList.participants = Relationship(
    back_populates="list",
    sa_relationship_kwargs={
        "cascade": "all, delete-orphan",
    },
)
SecretSantaList.blacklists = Relationship(
    back_populates="list",
    sa_relationship_kwargs={
        "cascade": "all, delete-orphan",
    },
)

Participant.list = Relationship(
    back_populates="participants",
)
Participant.blacklists = Relationship(
    back_populates="participant",
    sa_relationship_kwargs={
        "foreign_keys": "[Blacklist.participant_id]",
    },
)
Participant.blacklisted_by = Relationship(
    back_populates="blacklisted_participant",
    sa_relationship_kwargs={
        "foreign_keys": "[Blacklist.blacklisted_participant_id]",
    },
)

Blacklist.participant = Relationship(
    back_populates="blacklists",
    sa_relationship_kwargs={
        "foreign_keys": "[Blacklist.participant_id]",
    },
)
Blacklist.blacklisted_participant = Relationship(
    back_populates="blacklisted_by",
    sa_relationship_kwargs={
        "foreign_keys": "[Blacklist.blacklisted_participant_id]",
    },
)
Blacklist.list = Relationship(
    back_populates="blacklists",
)

if TYPE_CHECKING:
    from typing import List

    SecretSantaList.participants: List[Participant]
    SecretSantaList.blacklists: List[Blacklist]

    Participant.list: SecretSantaList
    Participant.blacklists: List[Blacklist]
    Participant.blacklisted_by: List[Blacklist]

    Blacklist.participant: Participant
    Blacklist.blacklisted_participant: Participant
    Blacklist.list: SecretSantaList
