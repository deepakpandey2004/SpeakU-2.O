from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from uuid import UUID


class RatingCreate(BaseModel):
    
    session_id: UUID = Field(..., description="Call session ID")
    rated_user_id: UUID = Field(..., description="User being rated")
    rating: int = Field(..., ge=1, le=5, description="Rating 1-5 stars")
    feedback: Optional[str] = Field(
        None,
        max_length=500,
        description="Optional feedback text"
    )
    
    @field_validator("rating")
    @classmethod
    def validate_rating_range(cls, value: int) -> int:
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5")
        return value



class RatingResponse(BaseModel):
    id: UUID
    session_id: UUID
    rater_id: UUID
    rated_user_id: UUID
    rating: int
    feedback: Optional[str]
    created_at: datetime
    
    model_config = {
        "from_attributes": True
    }