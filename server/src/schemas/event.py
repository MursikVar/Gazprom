from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

class InterestBase(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
class EventBase(BaseModel):
    name: str
    description: Optional[str] = None
    event_type: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status_event: Optional[str] = None
    organizator: Optional[str] = None
    place: Optional[str] = None


class EventCreate(EventBase):
    interests: List[str]
    pass

class EventUpdate(EventBase):
    name: Optional[str] = None
    description: Optional[str] = None
    event_type: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class Event(EventBase):
    id: int
    interests: List[str] = []
    model_config = ConfigDict(from_attributes=True)

class EventInterestCreate(BaseModel):
    event_id: int
    interest_id: int
    model_config = ConfigDict(from_attributes=True)
class EventParticipantCreate(BaseModel):
    event_id: int
    user_id: int
    priority_id: Optional[int] = None
    is_present: bool
    model_config = ConfigDict(from_attributes=True)

class EventParticipantUpdate(BaseModel):
    is_present: bool = False

class EventParticipantWithPriority(BaseModel):
    event_id: int
    user_id: int
    priority_id: Optional[int] = None
    is_present: bool
    model_config = ConfigDict(from_attributes=True)

