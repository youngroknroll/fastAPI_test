"""Auth API Router"""

from fastapi import APIRouter, Depends, Header, HTTPException
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


@router.get("/user", status_code=200)
def get_current_user(
    authorization: str = Header(None), session: Session = Depends(get_session)
):
    """Get current user"""
    # Check if authorization header exists
    if authorization is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # For now, just extract email from token (dummy implementation)
    # Token format: "Token dummy-jwt-token"
    token = authorization.replace("Token ", "")

    # Get first user (dummy implementation)
    repo = UserRepository(session)
    user = repo.get_first_user()

    return {
        "user": {
            "email": user.email,
            "username": user.username,
            "token": token,
        }
    }

