from pydantic import BaseModel
from typing import Optional
from datetime import date, time, datetime

class HCPInteractionBase(BaseModel):
    hcp_name: str
    interaction_type: str
    interaction_date: date
    interaction_time: time
    attendees: Optional[str] = None
    topics_discussed: Optional[str] = None
    materials_shared: Optional[str] = None
    samples_distributed: Optional[str] = None
    sentiment: Optional[str] = None
    outcomes: Optional[str] = None
    follow_up_actions: Optional[str] = None

class HCPInteractionCreate(HCPInteractionBase):
    pass

class HCPInteractionUpdate(BaseModel):
    hcp_name: Optional[str] = None
    interaction_type: Optional[str] = None
    interaction_date: Optional[date] = None
    interaction_time: Optional[time] = None
    attendees: Optional[str] = None
    topics_discussed: Optional[str] = None
    materials_shared: Optional[str] = None
    samples_distributed: Optional[str] = None
    sentiment: Optional[str] = None
    outcomes: Optional[str] = None
    follow_up_actions: Optional[str] = None

class HCPInteraction(HCPInteractionBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ChatMessageRequest(BaseModel):
    message: str
    history: list[dict] = [] # list of {"role": "user"|"assistant", "content": "..."}
