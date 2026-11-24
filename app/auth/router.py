from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.database import get_db
from app.auth.schemas import UserRegister, UserResponse, TokenResponse
from app.auth.service import (
    register_user,
    authenticate_user,
    create_user_token
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

limiter = Limiter(key_func=get_remote_address)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    user = register_user(db, user_data)

    if user is None:
        raise HTTPException(
            status_code=409,
            detail="Username or email already exists"
        )

    return user


@router.post(
    "/login",
    response_model=TokenResponse
)
@limiter.limit("5/minute")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(
        db,
        form_data.username,
        form_data.password
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_user_token(user)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }