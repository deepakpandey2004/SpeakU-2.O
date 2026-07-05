from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from typing import List

from app.extensions import get_db
from app.models import User
from app.schemas import (
    UserUpdate,
    UserResponse,
    UserProfileResponse
)
from app.dependencies import get_current_active_user


router = APIRouter()



@router.get(
    "/me",
    response_model=UserProfileResponse,
    summary="Get my profile (with private info)"
)
def get_my_profile(
    current_user: User = Depends(get_current_active_user)
):
    
    return current_user



@router.put(
    "/update",
    response_model=UserProfileResponse,
    summary="Update my profile"
)
def update_profile(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    
    
    if update_data.username and update_data.username != current_user.username:
        
        existing = db.query(User).filter(
            and_(
                User.username == update_data.username,
                User.id != current_user.id
            )
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    
    update_dict = update_data.model_dump(exclude_unset=True)
    
    for field, value in update_dict.items():
        setattr(current_user, field, value)
    
    
    db.commit()
    db.refresh(current_user)
    
    return current_user



@router.get(
    "/{username}",
    response_model=UserResponse,
    summary="Get public profile of any user"
)
def get_public_profile(
    username: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    
    user = db.query(User).filter(
        User.username == username.lower()
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User '{username}' not found"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not available"
        )
    
    return user



@router.get(
    "/leaderboard/top",
    response_model=List[UserResponse],
    summary="Get top users by rating"
)
def get_leaderboard(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    
    

    if limit < 1 or limit > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit must be between 1 and 50"
        )
    
    
    top_users = db.query(User).filter(
        and_(
            User.is_active == True,
            User.total_ratings > 0
        )
    ).order_by(
        desc(User.avg_rating),
        desc(User.total_calls)
    ).limit(limit).all()
    
    return top_users



@router.get(
    "/search/by-language",
    response_model=List[UserResponse],
    summary="Search users by language preference"
)
def search_by_language(
    native: str = None,
    learning: str = None,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    
    
    query = db.query(User).filter(
        and_(
            User.is_active == True,
            User.id != current_user.id  # Exclude self
        )
    )
    
    if native:
        query = query.filter(User.native_lang == native.capitalize())
    
    if learning:
        query = query.filter(User.learning_lang == learning.capitalize())
    
    
    users = query.limit(min(limit, 50)).all()
    
    return users