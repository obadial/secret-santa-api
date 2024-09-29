from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.schemas.blacklist import BlacklistCreate
from app.models import Blacklist, Participant
from app.utils.list_utils import get_default_list, get_session

router = APIRouter(prefix="/blacklist", tags=["Blacklist"])


@router.post("/")
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


@router.post("/lists/{list_id}")
def add_to_blacklist_for_list(
    list_id: int,
    blacklist_entry: BlacklistCreate,
    session: Session = Depends(get_session),
):
    participant = session.get(Participant, blacklist_entry.participant_id)
    blacklisted_participant = session.get(
        Participant, blacklist_entry.blacklisted_participant_id
    )

    if not participant or not blacklisted_participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    if participant.list_id != list_id or blacklisted_participant.list_id != list_id:
        raise HTTPException(
            status_code=400, detail="Participants must be in the same list"
        )

    new_blacklist_entry = Blacklist(
        participant_id=blacklist_entry.participant_id,
        blacklisted_participant_id=blacklisted_participant.id,
        list_id=list_id,
    )
    session.add(new_blacklist_entry)
    session.commit()
    session.refresh(new_blacklist_entry)
    return new_blacklist_entry
