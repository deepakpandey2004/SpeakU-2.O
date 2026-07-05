from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
from uuid import UUID
import re



class UserCreate(BaseModel):
    """
    Schema for user registration request
    
    POST /auth/register
    Body: { "email": "...", "username": "...", "password": "..." }
    """
    
    email: EmailStr = Field(
        ...,                              
        description="User's email address",
        examples=["rahul@gmail.com"]
    )
    
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Unique username (3-50 chars)",
        examples=["rahul22"]
    )
    
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Password (min 8 chars, must have letter + number)",
        examples=["MyPass@123"]
    )
    
    
    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        
        if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", value):
            raise ValueError(
                
            )
        return value.lower()             
    
    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
    
        if not re.search(r"[a-zA-Z]", value):
            raise ValueError("Password must contain at least one letter")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one number")
        return value



class UserLogin(BaseModel):
    
    email: EmailStr = Field(..., description="Registered email")
    password: str = Field(..., min_length=1, description="User password")


class UserUpdate(BaseModel):
    
    username: Optional[str] = Field(
        None,
        min_length=3,
        max_length=50
    )
    
    native_lang: Optional[str] = Field(
        None,
        max_length=50,
        examples=["Hindi"]
    )
    
    learning_lang: Optional[str] = Field(
        None,
        max_length=50,
        examples=["English"]
    )
    
    proficiency: Optional[str] = Field(
        None,
        examples=["beginner"]
    )
    
    @field_validator("proficiency")
    @classmethod
    def validate_proficiency(cls, value: Optional[str]) -> Optional[str]:
        
        if value is None:
            return value
        
        valid_levels = ["beginner", "intermediate", "advanced"]
        if value.lower() not in valid_levels:
            raise ValueError(f"Proficiency must be one of: {valid_levels}")
        return value.lower()
    
    @field_validator("native_lang", "learning_lang")
    @classmethod
    def validate_language(cls, value: Optional[str]) -> Optional[str]:

        if value is None:
            return value
        return value.strip().capitalize()


class UserResponse(BaseModel):
    
    id: UUID
    username: str
    native_lang: Optional[str]
    learning_lang: Optional[str]
    proficiency: Optional[str]
    avg_rating: float
    total_calls: int
    
    
    model_config = {
        "from_attributes": True          
    }


class UserProfileResponse(BaseModel):
    
    id: UUID
    email: EmailStr
    username: str
    native_lang: Optional[str]
    learning_lang: Optional[str]
    proficiency: Optional[str]
    lingos_balance: int
    avg_rating: float
    total_ratings: int
    total_calls: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    
    model_config = {
        "from_attributes": True
    }



class Token(BaseModel):
    
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Expiry in seconds")
    user: UserProfileResponse = Field(..., description="User info")


class TokenData(BaseModel):
    
    user_id: Optional[UUID] = None
    email: Optional[str] = None