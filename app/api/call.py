from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc

from app.extensions import get_db
from app.models import User, CallSession
from app.schemas import CallSessionResponse
from app.dependencies import get_current_active_user
from app.config import settings
from typing import List


router = APIRouter()



@router.get(
    "/history",
    response_model=List[CallSessionResponse],
    summary="Get my call history"
)
def get_call_history(
    limit: int = 20,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    

    calls = db.query(CallSession).filter(
        or_(
            CallSession.caller_id == current_user.id,
            CallSession.receiver_id == current_user.id
        )
    ).order_by(
        desc(CallSession.started_at)
    ).limit(min(limit, 50)).all()

    return calls



@router.post(
    "/end/{room_id}",
    response_model=CallSessionResponse,
    summary="End an active call"
)
def end_call(
    room_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    

   
    session = db.query(CallSession).filter(
        and_(
            CallSession.room_id == room_id,
            CallSession.status == "active"
        )
    ).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active call session not found"
        )

    
    if str(current_user.id) not in [str(session.caller_id), str(session.receiver_id)]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not part of this call"
        )

    
    session.end_call()

    
    caller = db.query(User).filter(User.id == session.caller_id).first()
    receiver = db.query(User).filter(User.id == session.receiver_id).first()

    if caller:
        caller.lingos_balance += settings.LINGOS_PER_CALL_REWARD
        caller.total_calls += 1

    if receiver:
        receiver.lingos_balance += settings.LINGOS_PER_CALL_REWARD
        receiver.total_calls += 1

    
    db.commit()
    db.refresh(session)

    return session



@router.get(
    "/lingos/balance",
    summary="Check Lingos balance"
)
def get_lingos_balance(
    current_user: User = Depends(get_current_active_user)
):
    
    return {
        "user_id": str(current_user.id),
        "username": current_user.username,
        "lingos_balance": current_user.lingos_balance,
        "total_calls": current_user.total_calls,
        "avg_rating": current_user.avg_rating
    }