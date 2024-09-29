from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.schemas.participant import ParticipantCreate
from app.models import Participant
from app.utils.list_utils import get_default_list, get_session
from typing import List

router = APIRouter(prefix="/v1/participants", tags=["Participants"])


@router.post("/")
def create_participant(
    participant: ParticipantCreate, session: Session = Depends(get_session)
):
    default_list = get_default_list(session)
    new_participant = Participant(name=participant.name, list_id=default_list.id)
    session.add(new_participant)
    session.commit()
    session.refresh(new_participant)
    return new_participant


@router.get("/", response_model=List[Participant])
def get_participants(session: Session = Depends(get_session)):
    default_list = get_default_list(session)
    statement = select(Participant).where(Participant.list_id == default_list.id)
    results = session.exec(statement).all()
    return results


@router.delete("/{participant_id}")
def delete_participant_from_default_list(
    participant_id: int, session: Session = Depends(get_session)
):
    default_list = get_default_list(session)
    participant = session.get(Participant, participant_id)
    if not participant or participant.list_id != default_list.id:
        raise HTTPException(
            status_code=404, detail="Participant not found in the default list"
        )

    session.delete(participant)
    session.commit()
    return {
        "message": f"Participant {participant.name} (id: {participant_id}) removed from default list"
    }
