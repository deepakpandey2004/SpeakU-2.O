from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Index, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.extensions import Base


class CallSession(Base):
    
    __tablename__ = "call_sessions"
    
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        nullable=False
    )
    
    
    caller_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True                    
    )
    
    receiver_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    
    room_id = Column(
        String(100),
        unique=True,                  
        nullable=False,
        index=True                    
    )
    
    status = Column(
        String(20),
        nullable=False,
        default="active",
        index=True
        
    )
    
    
    started_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    
    ended_at = Column(
        DateTime(timezone=True),
        nullable=True                 
    )
    
    duration_sec = Column(
        Integer,
        nullable=True,                
        default=0
    )
    
    
    caller_language = Column(
        String(50),                  
        nullable=True
    )
    
    receiver_language = Column(
        String(50),                 
        nullable=True
    )
    

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    
    
    caller = relationship(
        "User",
        foreign_keys=[caller_id],
        back_populates="calls_made"
    )
    
    receiver = relationship(
        "User",
        foreign_keys=[receiver_id],
        back_populates="calls_received"
    )
    
    
    ratings = relationship(
        "CallRating",
        back_populates="session",
        cascade="all, delete-orphan"
    )
    
    
    __table_args__ = (
        CheckConstraint(
            "caller_id != receiver_id",
            name="check_different_users"
        ),
        
        
        CheckConstraint(
            "status IN ('active', 'ended', 'missed', 'rejected')",
            name="check_valid_status"
        ),
        
        
        CheckConstraint(
            "duration_sec >= 0",
            name="check_positive_duration"
        ),
        
        
        Index("idx_user_calls", "caller_id", "started_at"),
        Index("idx_active_calls", "status", "started_at"),
    )
    
    
    def __repr__(self):
        return (
            f"<CallSession(id={self.id}, "
            f"caller={self.caller_id}, "
            f"receiver={self.receiver_id}, "
            f"status='{self.status}', "
            f"duration={self.duration_sec}s)>"
        )
    

    def to_dict(self):
        return {
            "id": str(self.id),
            "caller_id": str(self.caller_id),
            "receiver_id": str(self.receiver_id),
            "room_id": self.room_id,
            "status": self.status,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "ended_at": self.ended_at.isoformat() if self.ended_at else None,
            "duration_sec": self.duration_sec,
            "caller_language": self.caller_language,
            "receiver_language": self.receiver_language
        }
    
    def is_active(self) -> bool:
        return self.status == "active"
    
    