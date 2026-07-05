from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.extensions import get_db
from app.models import User
from app.schemas import (
    UserCreate,
    UserLogin,
    UserProfileResponse,
    Token
)
from app.utils.auth_helpers import (
    hash_password,
    verify_password,
    create_access_token
)
from app.dependencies import get_current_active_user
from app.config import settings



router = APIRouter()


@router.post(
    "/register",
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account"
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    
    
    existing_email = db.query(User).filter(
        User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    
    existing_username = db.query(User).filter(
        User.username == user_data.username
    ).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    
    hashed_pwd = hash_password(user_data.password)
    
    
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        password_hash=hashed_pwd,
        lingos_balance=settings.LINGOS_NEW_USER_BONUS  # 10 free lingos
    )
    
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  
    
    
    access_token = create_access_token(
        data={
            "user_id": str(new_user.id),
            "email": new_user.email
        }
    )
    
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": new_user
    }



@router.post(
    "/login",
    response_model=Token,
    summary="Login with email and password"
)
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    

    user = db.query(User).filter(
        User.email == credentials.email
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    

    access_token = create_access_token(
        data={
            "user_id": str(user.id),
            "email": user.email
        }
    )
    
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": user
    }



@router.post(
    "/token",
    response_model=Token,
    summary="OAuth2 compatible token endpoint (for Swagger)"
)
def login_oauth2(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    
    user = db.query(User).filter(
        User.email == form_data.username
    ).first()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    access_token = create_access_token(
        data={
            "user_id": str(user.id),
            "email": user.email
        }
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": user
    }



@router.get(
    "/me",
    response_model=UserProfileResponse,
    summary="Get current logged-in user info"
)
def get_me(
    current_user: User = Depends(get_current_active_user)
):
    
    return current_user