from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from app.schemas import ParticipantCreate, BlacklistCreate
from app.models.blacklist import Blacklist
from app.models.participant import Participant
from app.models.secretsantalist import SecretSantaList
from typing import List, Optional
import random
import uuid
from app.config import DATABASE_URL

from app.db import create_db_and_tables, engine
from contextlib import asynccontextmanager
import os

STAR_WARS_PLANETS = ["Tatooine", "Hoth", "Endor", "Naboo", "Coruscant", "Dagobah"]
DEFAULT_LIST_NAME = "Default Secret Santa List"


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


def get_session():
    with Session(engine) as session:
        yield session


@app.exception_handler(404)
async def not_found_error_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=404, content={"message": "Resource not found"})


def get_default_list(session: Session) -> SecretSantaList:
    default_list = session.exec(
        select(SecretSantaList).where(SecretSantaList.name == DEFAULT_LIST_NAME)
    ).first()
    if not default_list:
        default_list = SecretSantaList(name=DEFAULT_LIST_NAME)
        session.add(default_list)
        session.commit()
        session.refresh(default_list)
    return default_list


@app.post("/participants")
def create_participant(
    participant: ParticipantCreate, session: Session = Depends(get_session)
):
    default_list = get_default_list(session)
    new_participant = Participant(name=participant.name, list_id=default_list.id)
    session.add(new_participant)
    session.commit()
    session.refresh(new_participant)
    return new_participant


@app.get("/participants", response_model=List[Participant])
def get_participants(session: Session = Depends(get_session)):
    default_list = get_default_list(session)
    statement = select(Participant).where(Participant.list_id == default_list.id)
    results = session.exec(statement).all()
    return results


@app.post("/blacklist")
def add_to_blacklist(
    blacklist_entry: BlacklistCreate, session: Session = Depends(get_session)
):
    default_list = get_default_list(session)

    participant = session.get(Participant, blacklist_entry.participant_id)
    blacklisted_participant = session.get(
        Participant, blacklist_entry.blacklisted_participant_id
    )

    if not participant or not blacklisted_participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    if (
        participant.list_id != default_list.id
        or blacklisted_participant.list_id != default_list.id
    ):
        raise HTTPException(
            status_code=400, detail="Participants must be in the same list"
        )

    new_blacklist_entry = Blacklist(
        participant_id=blacklist_entry.participant_id,
        blacklisted_participant_id=blacklisted_participant.id,
        list_id=default_list.id,
    )
    session.add(new_blacklist_entry)
    session.commit()
    session.refresh(new_blacklist_entry)
    return new_blacklist_entry


@app.get("/draw")
def secret_santa_draw(session: Session = Depends(get_session)):
    default_list = get_default_list(session)

    participants = session.exec(
        select(Participant).where(Participant.list_id == default_list.id)
    ).all()
    if len(participants) < 2:
        raise HTTPException(
            status_code=400, detail="Not enough participants for the draw."
        )

    blacklists = session.exec(
        select(Blacklist).where(Blacklist.list_id == default_list.id)
    ).all()
    blacklist_map = {
        entry.participant_id: entry.blacklisted_participant_id for entry in blacklists
    }

    def is_valid_draw(draw):
        for gifter, receiver in draw.items():
            if blacklist_map.get(gifter) == receiver:
                return False
        return True

    participants_ids = [p.id for p in participants]
    draw = {}

    for gifter in participants_ids:
        possible_receivers = [
            r for r in participants_ids if r != gifter and r not in draw.values()
        ]
        if not possible_receivers:
            raise HTTPException(
                status_code=500, detail="Unable to generate a valid draw."
            )
        receiver = random.choice(possible_receivers)
        draw[gifter] = receiver

    if not is_valid_draw(draw):
        raise HTTPException(status_code=400, detail="Could not generate a valid draw.")

    draw_with_names = []
    for gifter_id, receiver_id in draw.items():
        gifter = session.get(Participant, gifter_id)
        receiver = session.get(Participant, receiver_id)
        draw_with_names.append(
            {
                "gifter_id": gifter.id,
                "gifter_name": gifter.name,
                "receiver_id": receiver.id,
                "receiver_name": receiver.name,
            }
        )

    return draw_with_names


@app.post("/lists")
def create_secret_santa_list(
    name: Optional[str] = None, session: Session = Depends(get_session)
):
    if not name:
        name = f"{random.choice(STAR_WARS_PLANETS)}-{uuid.uuid4().hex[:6]}"

    new_list = SecretSantaList(name=name)
    session.add(new_list)
    session.commit()
    session.refresh(new_list)
    return new_list


@app.post("/lists/{list_id}/participants")
def create_participant_for_list(
    list_id: int,
    participant: ParticipantCreate,
    session: Session = Depends(get_session),
):
    santa_list = session.get(SecretSantaList, list_id)
    if not santa_list:
        raise HTTPException(status_code=404, detail="List not found")

    new_participant = Participant(name=participant.name, list_id=list_id)
    session.add(new_participant)
    session.commit()
    session.refresh(new_participant)
    return new_participant


@app.get("/lists/{list_id}/participants", response_model=List[Participant])
def get_participants_for_list(list_id: int, session: Session = Depends(get_session)):
    santa_list = session.get(SecretSantaList, list_id)
    if not santa_list:
        raise HTTPException(status_code=404, detail="List not found")

    statement = select(Participant).where(Participant.list_id == list_id)
    results = session.exec(statement).all()
    return results


@app.get("/lists/{list_id}/draw")
def secret_santa_draw_for_list(list_id: int, session: Session = Depends(get_session)):
    participants = session.exec(
        select(Participant).where(Participant.list_id == list_id)
    ).all()
    if len(participants) < 2:
        raise HTTPException(
            status_code=400, detail="Not enough participants for the draw."
        )

    blacklists = session.exec(select(Blacklist).where(Blacklist.list_id == list_id)).all()
    blacklist_map = {
        entry.participant_id: entry.blacklisted_participant_id for entry in blacklists
    }

    def is_valid_draw(draw):
        for gifter, receiver in draw.items():
            if blacklist_map.get(gifter) == receiver:
                return False
        return True

    participants_ids = [p.id for p in participants]
    draw = {}

    for gifter in participants_ids:
        possible_receivers = [
            r for r in participants_ids if r != gifter and r not in draw.values()
        ]
        if not possible_receivers:
            raise HTTPException(
                status_code=500, detail="Unable to generate a valid draw."
            )
        receiver = random.choice(possible_receivers)
        draw[gifter] = receiver

    if not is_valid_draw(draw):
        raise HTTPException(status_code=400, detail="Could not generate a valid draw.")

    draw_with_names = []
    for gifter_id, receiver_id in draw.items():
        gifter = session.get(Participant, gifter_id)
        receiver = session.get(Participant, receiver_id)
        draw_with_names.append(
            {
                "gifter_id": gifter.id,
                "gifter_name": gifter.name,
                "receiver_id": receiver.id,
                "receiver_name": receiver.name,
            }
        )

    return draw_with_names
