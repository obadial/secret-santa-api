from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.secretsantalist import SecretSantaList
from app.models.participant import Participant
from app.utils.list_utils import get_session
from typing import List, Optional
import random
import uuid

router = APIRouter(prefix="/v1/lists", tags=["Lists"])

STAR_WARS_PLANETS = ["Tatooine", "Hoth", "Endor", "Naboo", "Coruscant", "Dagobah"]


@router.post("/")
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


@router.delete("/{list_id}")
def delete_list(list_id: int, session: Session = Depends(get_session)):
    santa_list = session.get(SecretSantaList, list_id)
    if not santa_list:
        raise HTTPException(status_code=404, detail="List not found")

    participants = session.exec(
        select(Participant).where(Participant.list_id == list_id)
    ).all()
    for participant in participants:
        session.delete(participant)

    session.delete(santa_list)
    session.commit()
    return {
        "message": f"List with id: {list_id} and all associated participants have been removed"
    }


@router.get("/with-participants")
def get_all_lists_with_participants(session: Session = Depends(get_session)):
    lists = session.exec(select(SecretSantaList)).all()
    response = []

    for santa_list in lists:
        participants = session.exec(
            select(Participant).where(Participant.list_id == santa_list.id)
        ).all()
        response.append(
            {
                "list_id": santa_list.id,
                "list_name": santa_list.name,
                "participants": [{"id": p.id, "name": p.name} for p in participants],
            }
        )

    return response
