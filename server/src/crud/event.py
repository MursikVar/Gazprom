from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from src.schemas.event import EventCreate, EventUpdate, EventParticipantCreate, EventInterestCreate, EventParticipantUpdate
from src.database import Event, EventInterest, EventParticipantWithPriority
from src.schemas.event import Event as EventSchema
from src.crud.dict_table import dict_crud
from src.crud.user import user_crud

# CRUD-операции для Event
async def create_event(db: AsyncSession, event: EventCreate):
    if event.start_time and event.start_time.tzinfo is not None:
        event.start_time = event.start_time.replace(tzinfo=None)

    if event.end_time and event.end_time.tzinfo is not None:
        event.end_time = event.end_time.replace(tzinfo=None)

    event_type = await dict_crud.get_event_types(db=db)
    dict_event_type = {value[1]: key[1] for key, value in dict(event_type).items()}
    db_event = Event(
        name=event.name,
        description=event.description,
        event_type_id=dict_event_type[event.event_type],
        start_time=event.start_time,
        end_time=event.end_time,
        organizator=event.organizator,
        place=event.place
    )
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    
    # Добавление интересов к событию, если они указаны
    if event.interests:
        interest_type = await dict_crud.get_interests(db=db)
        dict_interest_type = {value[1]: key[1] for key, value in dict(interest_type).items()}
        for interest_id in event.interests:
            event_interest = EventInterest(event_id=db_event.id, interest_id=dict_interest_type[interest_id])
            db.add(event_interest)
        await db.commit()
    
    # Добавление всех пользователей к событию с приоритетом 1
    from src.database import User
    result = await db.execute(select(User))
    users = result.scalars().all()
    
    for user in users:
        participant = EventParticipantWithPriority(
            event_id=db_event.id,
            user_id=user.id,
            priority_id=1,
            is_present=False
        )
        db.add(participant)
    
    await db.commit()
    
    return db_event

# Получение события по id
async def get_event(db: AsyncSession, event_id: int):
    result = await db.execute(
        select(Event)
        .options(selectinload(Event.interests).selectinload(EventInterest.interest))
        .filter(Event.id == event_id)
    )
    db_event = result.scalars().first()
    return db_event

# Получение списка событий
async def get_events(
            db: AsyncSession,
            skip: int = 0,
            limit: int = 100,
            event_type_id: Optional[int] = None,
            is_past: bool  = False,
            start_date: datetime = None,
            end_date: datetime  = None,
            sort_by: str = "date"  # "date" или "popularity"
    ):
    query = select(Event)        \
        .options(selectinload(Event.interests).selectinload(EventInterest.interest)) # Загружаем интересы


    # Фильтрация по типу события
    if event_type_id is not None:
        query = query.where(Event.event_type_id == event_type_id)

    # Фильтрация по пройденности (прошло/не прошло)
    now = datetime.now()
    if is_past is True:
        query = query.where(Event.end_time <= now)
    elif is_past is False:
        query = query.where(Event.start_time > now)

    # Фильтрация по диапазону дат
    if start_date:
        query = query.where(Event.start_time >= start_date)
    if end_date:
        query = query.where(Event.end_time <= end_date)

    # Сортировка
    # if sort_by == "popularity":
    #     query = query.outerjoin(EventParticipantWithPriority).group_by(Event.id)
    #     query = query.order_by(func.count(EventParticipantWithPriority.user_id).desc())  # Количество участников
    # else:
    #     query = query.order_by(Event.start_time.asc())  # По дате (по умолчанию)

    # Ограничение и смещение
    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    return result.scalars().all()

# Обновление события
async def update_event(db: AsyncSession, event_id: int, event: EventUpdate):
    result = await db.execute(select(Event).filter(Event.id == event_id))
    db_event = result.scalars().first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.start_time and event.start_time.tzinfo is not None:
        event.start_time = event.start_time.replace(tzinfo=None)
    if event.end_time and event.end_time.tzinfo is not None:
        event.end_time = event.end_time.replace(tzinfo=None)
    for key, value in event.dict(exclude_unset=True).items():
        setattr(db_event, key, value)
    await db.commit()
    await db.refresh(db_event)
    return db_event

# Удаление события
async def delete_event(db: AsyncSession, event_id: int):
    result = await db.execute(select(Event).filter(Event.id == event_id))
    db_event = result.scalars().first()
    if db_event:
        await db.delete(db_event)
        await db.commit()
        return db_event
    raise HTTPException(status_code=404, detail="Event not found")

async def get_event_participants(db: AsyncSession, event_id: int):
    result = await db.execute(select(EventParticipantWithPriority).filter(EventParticipantWithPriority.event_id == event_id))
    return result.scalars().all()

# Получение приоритета события для текущего пользователя
async def get_event_priority(db: AsyncSession, event_id: int, user_id: int):
    result = await db.execute(
        select(EventParticipantWithPriority).filter(
            EventParticipantWithPriority.event_id == event_id,
            EventParticipantWithPriority.user_id == user_id
        )
    )
    return result.scalars().first()

# Добавление участника к событию
async def update_event_participant(db: AsyncSession, event_id: int, user):
    stmt = select(EventParticipantWithPriority).where(
        EventParticipantWithPriority.event_id == event_id,
        EventParticipantWithPriority.user_id == user.id
    )
    result = await db.execute(stmt)
    participant = result.scalars().first()

    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")

    participant.is_present = not participant.is_present  # Инвертируем is_present
    await db.commit()
    await db.refresh(participant)


    return participant

# Добавление интересов к событию
async def add_event_interests(db: AsyncSession, event_id: int, interests: List[EventInterestCreate]):
    event_interests = []
    for interest in interests:
        event_interest = EventInterest(event_id=event_id, interest_id=interest.interest_id)
        db.add(event_interest)
        event_interests.append(event_interest)
    await db.commit()
    return event_interests

async def get_events_by_user_id(db: AsyncSession, user_id: int):
    """
    Get all events that a user is registered for.
    """
    result = await db.execute(
        select(Event)
        .join(EventParticipantWithPriority, Event.id == EventParticipantWithPriority.event_id)
        .options(selectinload(Event.interests).selectinload(EventInterest.interest))
        .filter(EventParticipantWithPriority.user_id == user_id and EventParticipantWithPriority.is_present)
    )
    return result.scalars().all()