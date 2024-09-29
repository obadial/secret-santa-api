from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models import Blacklist, Participant
from app.utils.list_utils import get_session, get_default_list
from typing import List
import random

router = APIRouter(prefix="/draw", tags=["Draw"])


@router.get("/")
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


@router.get("/lists/{list_id}")
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
