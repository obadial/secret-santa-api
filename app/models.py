from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional


class SecretSantaList(SQLModel, table=True):
    __tablename__ = "secret_santa_list"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    participants: List["Participant"] = Relationship(back_populates="list")
    blacklists: List["Blacklist"] = Relationship(back_populates="list")


class Participant(SQLModel, table=True):
    __tablename__ = "participant"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    list_id: Optional[int] = Field(default=None, foreign_key="secret_santa_list.id")

    list: "SecretSantaList" = Relationship(back_populates="participants")
    blacklists: List["Blacklist"] = Relationship(
        back_populates="participant",
        sa_relationship_kwargs={"foreign_keys": "[Blacklist.participant_id]"},
    )
    blacklisted_by: List["Blacklist"] = Relationship(
        back_populates="blacklisted_participant",
        sa_relationship_kwargs={"foreign_keys": "[Blacklist.blacklisted_participant_id]"},
    )


class Blacklist(SQLModel, table=True):
    __tablename__ = "blacklist"

    id: Optional[int] = Field(default=None, primary_key=True)
    participant_id: Optional[int] = Field(default=None, foreign_key="participant.id")
    blacklisted_participant_id: Optional[int] = Field(
        default=None, foreign_key="participant.id"
    )
    list_id: Optional[int] = Field(default=None, foreign_key="secret_santa_list.id")

    participant: "Participant" = Relationship(
        back_populates="blacklists",
        sa_relationship_kwargs={"foreign_keys": "[Blacklist.participant_id]"},
    )
    blacklisted_participant: "Participant" = Relationship(
        back_populates="blacklisted_by",
        sa_relationship_kwargs={"foreign_keys": "[Blacklist.blacklisted_participant_id]"},
    )
    list: "SecretSantaList" = Relationship(back_populates="blacklists")
