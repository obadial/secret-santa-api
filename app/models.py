from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List
    from app.models import Participant, Blacklist, SecretSantaList


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
    sa_relationship_kwargs={
        "back_populates": "list",
        "cascade": "all, delete-orphan",
    },
    back_populates="list",
    default_factory=list,
)
SecretSantaList.blacklists = Relationship(
    sa_relationship_kwargs={
        "back_populates": "list",
        "cascade": "all, delete-orphan",
    },
    back_populates="list",
    default_factory=list,
)

Participant.list = Relationship(
    sa_relationship_kwargs={
        "back_populates": "participants",
    },
    back_populates="participants",
)
Participant.blacklists = Relationship(
    sa_relationship_kwargs={
        "back_populates": "participant",
        "foreign_keys": "[Blacklist.participant_id]",
    },
    back_populates="participant",
    default_factory=list,
)
Participant.blacklisted_by = Relationship(
    sa_relationship_kwargs={
        "back_populates": "blacklisted_participant",
        "foreign_keys": "[Blacklist.blacklisted_participant_id]",
    },
    back_populates="blacklisted_participant",
    default_factory=list,
)

Blacklist.participant = Relationship(
    sa_relationship_kwargs={
        "back_populates": "blacklists",
        "foreign_keys": "[Blacklist.participant_id]",
    },
    back_populates="blacklists",
)
Blacklist.blacklisted_participant = Relationship(
    sa_relationship_kwargs={
        "back_populates": "blacklisted_by",
        "foreign_keys": "[Blacklist.blacklisted_participant_id]",
    },
    back_populates="blacklisted_by",
)
Blacklist.list = Relationship(
    sa_relationship_kwargs={
        "back_populates": "blacklists",
    },
    back_populates="blacklists",
)
