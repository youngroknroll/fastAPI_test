"""Auth API Router"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from app.core.database import get_session
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserLogin, UserRegister, UserResponse

router = APIRouter(tags=["auth"])


class UserRegisterRequest(BaseModel):
    """Register request wrapper"""

    user: UserRegister


class UserLoginRequest(BaseModel):
    """Login request wrapper"""

    user: UserLogin


@router.post("/users", status_code=201)
def register(request: UserRegisterRequest, session: Session = Depends(get_session)):
    """Register a new user"""
    user_data = request.user
    repo = UserRepository(session)

    # Check if email already exists
    existing_user = repo.get_by_email(user_data.email)
    if existing_user:
        raise HTTPException(status_code=422, detail="Email already registered")

    # Create user
    user = repo.create(
        email=user_data.email,
        username=user_data.username,
        password=user_data.password,
    )

    return {
        "user": {
            "email": user.email,
            "username": user.username,
            "token": "dummy-jwt-token",
        }
    }


@router.post("/users/login", status_code=200)
def login(request: UserLoginRequest, session: Session = Depends(get_session)):
    """Login user"""
    user_data = request.user
    repo = UserRepository(session)

    # Get user by email
    user = repo.get_by_email(user_data.email)
    if user is None:
        raise HTTPException(status_code=422, detail="Email not found")

    # Check password
    if user.hashed_password != user_data.password:
        raise HTTPException(status_code=422, detail="Invalid password")

    return {
        "user": {
            "email": user.email,
            "username": user.username,
            "token": "dummy-jwt-token",
        }
    }

