from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Index, CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.extensions import Base


class CallRating(Base):
    __tablename__ = "call_ratings"
    
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        nullable=False
    )
    
    
    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("call_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    rater_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    rated_user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    
    rating = Column(
        Integer,
        nullable=False
        
    )
    
    feedback = Column(
        String(500),                  
        nullable=True                 
    )
    
    
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    
    
    
    
    session = relationship(
        "CallSession",
        back_populates="ratings"
    )
    
    
    rater = relationship(
        "User",
        foreign_keys=[rater_id],
        back_populates="ratings_given"
    )
    
    
    rated_user = relationship(
        "User",
        foreign_keys=[rated_user_id],
        back_populates="ratings_received"
    )
    
    
    __table_args__ = (
        
        CheckConstraint(
            "rating >= 1 AND rating <= 5",
            name="check_rating_range"
        ),
        
        
        CheckConstraint(
            "rater_id != rated_user_id",
            name="check_different_users_rating"
        ),
        
        
        UniqueConstraint(
            "session_id",
            "rater_id",
            name="unique_rater_per_session"
        ),
        
        
        Index("idx_rated_user_ratings", "rated_user_id", "created_at"),
        Index("idx_session_ratings", "session_id", "created_at"),
    )
    
    
    def __repr__(self):
        return (
            f"<CallRating(id={self.id}, "
            f"session={self.session_id}, "
            f"rater={self.rater_id}, "
            f"rated={self.rated_user_id}, "
            f"rating={self.rating})>"
        )
    
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "session_id": str(self.session_id),
            "rater_id": str(self.rater_id),
            "rated_user_id": str(self.rated_user_id),
            "rating": self.rating,
            "feedback": self.feedback,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    @staticmethod
    def is_valid_rating(rating: int) -> bool:
        return isinstance(rating, int) and 1 <= rating <= 5