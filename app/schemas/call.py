from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID



class MatchRequest(BaseModel):
    native_lang: str = Field(..., examples=["Hindi"])
    learning_lang: str = Field(..., examples=["English"])



class CallSessionCreate(BaseModel):
    caller_id: UUID
    receiver_id: UUID
    room_id: str = Field(..., min_length=10, max_length=100)
    caller_language: Optional[str] = None
    receiver_language: Optional[str] = None


class CallEndRequest(BaseModel):
    room_id: str = Field(..., description="Room ID of active call")


class CallSessionResponse(BaseModel):
    id: UUID
    caller_id: UUID
    receiver_id: UUID
    room_id: str
    status: str
    started_at: datetime
    ended_at: Optional[datetime]
    duration_sec: Optional[int]
    caller_language: Optional[str]
    receiver_language: Optional[str]
    
    model_config = {
        "from_attributes": True
    }