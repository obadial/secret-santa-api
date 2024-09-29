from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from app.schemas import ParticipantCreate, BlacklistCreate
from app.models.blacklist import Blacklist
from app.models.participant import Participant
from typing import List
import random
from app.config import DATABASE_URL

from app.db import create_db_and_tables, engine
from contextlib import asynccontextmanager
import os


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


@app.post("/participants")
def create_participant(
    participant: ParticipantCreate, session: Session = Depends(get_session)
):
    new_participant = Participant(name=participant.name)
    session.add(new_participant)
    session.commit()
    session.refresh(new_participant)
    return new_participant


@app.get("/participants", response_model=List[Participant])
def get_participants(session: Session = Depends(get_session)):
    statement = select(Participant)
    results = session.exec(statement).all()
    return results


@app.post("/blacklist")
def add_to_blacklist(
    blacklist_entry: BlacklistCreate, session: Session = Depends(get_session)
):
    participant = session.get(Participant, blacklist_entry.participant_id)
    blacklisted_participant = session.get(
        Participant, blacklist_entry.blacklisted_participant_id
    )

    if not participant or not blacklisted_participant:
        raise HTTPException(status_code=404, detail="Participant not found")

    new_blacklist_entry = Blacklist(
        participant_id=blacklist_entry.participant_id,
        blacklisted_participant_id=blacklist_entry.blacklisted_participant_id,
    )
    session.add(new_blacklist_entry)
    session.commit()
    session.refresh(new_blacklist_entry)
    return new_blacklist_entry


@app.get("/draw")
def secret_santa_draw(session: Session = Depends(get_session)):
    participants = session.exec(select(Participant)).all()
    if len(participants) < 2:
        raise HTTPException(
            status_code=400, detail="Not enough participants for the draw."
        )

    blacklists = session.exec(select(Blacklist)).all()
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
