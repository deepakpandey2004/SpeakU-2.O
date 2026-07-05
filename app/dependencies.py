from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from uuid import UUID

from app.extensions import get_db
from app.models import User
from app.utils.auth_helpers import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token",    
    auto_error=True
)



def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    
    user_id_str = payload.get("user_id")
    if user_id_str is None:
        raise credentials_exception
    
    
    try:
        user_id = UUID(user_id_str)
    except ValueError:
        raise credentials_exception
    
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    return user



def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    return current_user



def get_verified_user(
    current_user: User = Depends(get_current_active_user)
) -> User:

    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email verification required"
        )
    
    return current_user