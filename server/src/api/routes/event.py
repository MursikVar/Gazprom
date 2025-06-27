from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import src.schemas.event as schemas
import src.database as models
from src.api.dependecies.database import get_db_session
from src.api.dependecies.user import get_current_user
import src.crud.event as crud
from src.crud.dict_table import dict_crud
from src.schemas.event import Event
from src.schemas.auth import Message

router = APIRouter(
    tags=["event"],
    # dependencies=[Depends(get_current_user)]
)

# Эндпоинт для создания события
@router.post("/events/", response_model=schemas.Event)
async def create_event(event: schemas.EventCreate, db: Session = Depends(get_db_session)):
    event_bd = await crud.create_event(db=db, event=event)
    event_type = await dict_crud.get_event_types(db=db)
    dict_event_type = {key[1]: value[1] for key, value in dict(event_type).items()}
    # breakpoint()
    return schemas.Event(
            id=event_bd.id,
            name=event_bd.name,
            description=event_bd.description,
            event_type = dict_event_type[event_bd.event_type_id],
            start_time = event_bd.start_time,
            end_time = event_bd.end_time,
            status_event = "Активно",
            place = event_bd.place,
            organizator = event_bd.organizator,
            interests = [interest for interest in event.interests]
    )

# Эндпоинт для получения события по ID
@router.get("/events/{event_id}", response_model=schemas.Event)
async def get_event(event_id: int, db: Session = Depends(get_db_session)):
    event = await crud.get_event(db=db, event_id=event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    event_type = await dict_crud.get_event_types(db=db)
    event_type = {key[1]: value[1] for key,value in dict(event_type).items()}
    status_type = await dict_crud.get_status_types(db=db)
    status_type = {key[1]: value[1] for key, value in dict(status_type).items()}
    return schemas.Event(
            id=event.id,
            name=event.name,
            description=event.description,
            event_type=event_type[event.event_type_id],
            start_time=event.start_time,
            end_time=event.end_time,
            status_event=status_type[event.status_id],
            place=event.place,
            organizator=event.organizator,
            interests=[interest.interest.name for interest in event.interests])

# Эндпоинт для получения списка событий
@router.get("/events/", response_model=List[schemas.Event])
async def get_events(
    skip: int = 0,
    limit: int = 100,
    event_type: Optional[str] = None,
    is_past: Optional[bool] = False,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    sort_by: str = "date",  # "date" или "popularity"
    db = Depends(get_db_session)
):
    events_data = []
    event_types = await dict_crud.get_event_types(db=db)
    dict_event_type = {key[1]: value[1] for key, value in dict(event_types).items()}
    dict_event_type_to_id = {value[1]: key[1] for key, value in dict(event_types).items()}
    status_types = await dict_crud.get_status_types(db=db)
    dict_status_type = {key[1]: value[1] for key, value in dict(status_types).items()}
    if event_type:
        events = await crud.get_events(
            db=db,
            skip=skip,
            limit=limit,
            event_type_id=dict_event_type_to_id[event_type],
            is_past=is_past,
            start_date=start_date,
            end_date=end_date,
            sort_by=sort_by
        )
    else:
        events = await crud.get_events(
        db=db,
        skip=skip,
        limit=limit,
        event_type_id=None,
        is_past=is_past,
        start_date=start_date,
        end_date=end_date,
        sort_by=sort_by
    )

    for event in events:
        # breakpoint()
        # event.interests[0].interest.name
        event_data = Event(
            id=event.id,
            name=event.name,
            description=event.description,
            event_type=dict_event_type[event.event_type_id],
            start_time=event.start_time,
            end_time=event.end_time,
            status_event=dict_status_type[event.status_id],
            place=event.place,
            organizator=event.organizator,
            interests=[interest.interest.name for interest in event.interests])
        events_data.append(event_data)
    return events_data

# Эндпоинт для обновления события
@router.put("/events/{event_id}")
async def update_event(event_id: int, event: schemas.EventUpdate, db: Session = Depends(get_db_session)):
    await crud.update_event(db=db, event_id=event_id, event=event)
    return Message(message="Event updated successfully")

# Эндпоинт для удаления события
@router.delete("/events/{event_id}")
async def delete_event(event_id: int, db: Session = Depends(get_db_session)):
    await crud.delete_event(db=db, event_id=event_id)
    return Message(message="Event deleted successfully")

@router.get("/events/{event_id}/participants", response_model=List[schemas.EventParticipantWithPriority])
async def get_event_participants(event_id: int, db: Session = Depends(get_db_session)):
    participants = await crud.get_event_participants(db, event_id)
    if not participants:
        raise HTTPException(status_code=404, detail="No participants found for this event")
    return participants

# Эндпоинт для добавления участника к событию

@router.patch("/events/{event_id}/subscribe")
async def update_event_participant_endpoint(event_id: int, user=Depends(get_current_user), db = Depends(get_db_session)):
    return await crud.update_event_participant(db, event_id, user)
@router.patch("/events/{event_id}/interests", response_model=List[schemas.EventInterestCreate])
async def add_event_interests(event_id: int, interests: List[schemas.EventInterestCreate], db: Session = Depends(get_db_session)):
    result = await crud.add_event_interests(db, event_id, interests)
    if not result:
        raise HTTPException(status_code=404, detail="Could not add interests to the event")
    return result

