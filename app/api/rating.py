from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc

from app.extensions import get_db
from app.models import User, CallSession, CallRating
from app.schemas import RatingCreate, RatingResponse
from app.dependencies import get_current_active_user
from typing import List


router = APIRouter()



@router.post(
    "/submit",
    response_model=RatingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Rate a partner after call"
)
def submit_rating(
    rating_data: RatingCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    

    session = db.query(CallSession).filter(
        CallSession.id == rating_data.session_id
    ).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Call session not found"
        )

    
    if str(current_user.id) not in [str(session.caller_id), str(session.receiver_id)]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You were not part of this call"
        )

    
    if str(current_user.id) == str(rating_data.rated_user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot rate yourself"
        )

    
    if str(rating_data.rated_user_id) not in [str(session.caller_id), str(session.receiver_id)]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rated user was not part of this call"
        )

    
    existing_rating = db.query(CallRating).filter(
        and_(
            CallRating.session_id == rating_data.session_id,
            CallRating.rater_id == current_user.id
        )
    ).first()

    if existing_rating:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already rated this session"
        )

    
    new_rating = CallRating(
        session_id=rating_data.session_id,
        rater_id=current_user.id,
        rated_user_id=rating_data.rated_user_id,
        rating=rating_data.rating,
        feedback=rating_data.feedback
    )

    db.add(new_rating)

    
    rated_user = db.query(User).filter(
        User.id == rating_data.rated_user_id
    ).first()

    if rated_user:
        total = rated_user.total_ratings
        current_avg = rated_user.avg_rating

        
        new_total = total + 1
        new_avg = ((current_avg * total) + rating_data.rating) / new_total

        rated_user.avg_rating = round(new_avg, 2)
        rated_user.total_ratings = new_total

    
    db.commit()
    db.refresh(new_rating)

    return new_rating


@router.get(
    "/my-ratings",
    response_model=List[RatingResponse],
    summary="View ratings I received"
)
def get_my_ratings(
    limit: int = 20,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):


    ratings = db.query(CallRating).filter(
        CallRating.rated_user_id == current_user.id
    ).order_by(
        desc(CallRating.created_at)
    ).limit(min(limit, 50)).all()

    return ratings