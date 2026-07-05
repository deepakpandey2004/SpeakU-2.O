from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.extensions import Base


class User(Base):
    
    __tablename__ = "users"
    
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,           
        index=True,                   
        nullable=False
    )
    
    
    email = Column(
        String(255),
        unique=True,              
        nullable=False,                
        index=True                   
    )
    
    username = Column(
        String(50),
        unique=True,                  
        nullable=False,
        index=True
    )
    
    password_hash = Column(
        String(255),                  
        nullable=False
    )
    
    
    native_lang = Column(
        String(50),
        nullable=True,                
        index=True                   
    )
    
    learning_lang = Column(
        String(50),
        nullable=True,
        index=True                    
    )
    
    proficiency = Column(
        String(20),                   
        nullable=True,
        default="beginner"
    )
    
    
    lingos_balance = Column(
        Integer,
        default=10,                   
        nullable=False
    )
    
    avg_rating = Column(
        Float,
        default=0.0,
        nullable=False
    )
    
    total_ratings = Column(
        Integer,
        default=0,
        nullable=False
    )
    
    total_calls = Column(
        Integer,
        default=0,
        nullable=False
    )
    
    
    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )
    
    is_verified = Column(
        Boolean,
        default=False,
        nullable=False
    )
    
    
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),    
        nullable=False
    )
    
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),           
        nullable=False
    )
    
    
    
    calls_made = relationship(
        "CallSession",
        foreign_keys="CallSession.caller_id",
        back_populates="caller",
        cascade="all, delete-orphan"
    )
    
    
    calls_received = relationship(
        "CallSession",
        foreign_keys="CallSession.receiver_id",
        back_populates="receiver",
        cascade="all, delete-orphan"
    )
    
    
    ratings_given = relationship(
        "CallRating",
        foreign_keys="CallRating.rater_id",
        back_populates="rater",
        cascade="all, delete-orphan"
    )
    
    
    ratings_received = relationship(
        "CallRating",
        foreign_keys="CallRating.rated_user_id",
        back_populates="rated_user",
        cascade="all, delete-orphan"
    )
    
    __table_args__ = (
        Index("idx_languages", "native_lang", "learning_lang"),
        Index("idx_active_users", "is_active", "native_lang", "learning_lang"),
    )
    

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "email": self.email,
            "username": self.username,
            "native_lang": self.native_lang,
            "learning_lang": self.learning_lang,
            "proficiency": self.proficiency,
            "lingos_balance": self.lingos_balance,
            "avg_rating": round(self.avg_rating, 2),
            "total_ratings": self.total_ratings,
            "total_calls": self.total_calls,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    def is_profile_complete(self) -> bool:
        return bool(self.native_lang and self.learning_lang)