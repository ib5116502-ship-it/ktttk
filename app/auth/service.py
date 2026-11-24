from sqlalchemy.orm import Session

from app.models import User
from app.auth.schemas import UserRegister
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


def register_user(db: Session, user_data: UserRegister):

    existing_user = db.query(User).filter(
        (User.email == user_data.email) |
        (User.username == user_data.username)
    ).first()

    if existing_user:
        return None

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def authenticate_user(
    db: Session,
    email: str,
    password: str
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        return None

    if not verify_password(
        password,
        user.hashed_password
    ):
        return None

    return user


def create_user_token(user: User):

    return create_access_token({
        "sub": str(user.id),
        "role": user.role
    })