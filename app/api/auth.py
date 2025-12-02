"""Auth API Router"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.core.security import create_access_token
from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserLogin, UserRegister, UserResponse, UserUpdate

router = APIRouter(tags=["auth"])


class UserRegisterRequest(BaseModel):
    """Register request wrapper"""

    user: UserRegister


class UserLoginRequest(BaseModel):
    """Login request wrapper"""

    user: UserLogin


class UserUpdateRequest(BaseModel):
    """Update request wrapper"""

    user: UserUpdate


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

    # Generate JWT token
    token = create_access_token(user_id=user.id, username=user.username)

    return {
        "user": {
            "email": user.email,
            "username": user.username,
            "token": token,
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

    # Generate JWT token
    token = create_access_token(user_id=user.id, username=user.username)

    return {
        "user": {
            "email": user.email,
            "username": user.username,
            "token": token,
        }
    }


@router.get("/user", status_code=200)
def get_current_user_endpoint(current_user: User = Depends(get_current_user)):
    """Get current user"""
    # Generate new token for response
    token = create_access_token(user_id=current_user.id, username=current_user.username)

    return {
        "user": {
            "email": current_user.email,
            "username": current_user.username,
            "token": token,
        }
    }


@router.put("/user", status_code=200)
def update_user(
    request: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Update user"""
    update_data = request.user

    # Update user fields
    if update_data.email is not None:
        current_user.email = update_data.email
    if update_data.username is not None:
        current_user.username = update_data.username
    if update_data.password is not None:
        current_user.hashed_password = update_data.password
    if update_data.bio is not None:
        current_user.bio = update_data.bio
    if update_data.image is not None:
        current_user.image = update_data.image

    # Save changes
    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    # Generate new token
    token = create_access_token(user_id=current_user.id, username=current_user.username)

    return {
        "user": {
            "email": current_user.email,
            "username": current_user.username,
            "token": token,
        }
    }

