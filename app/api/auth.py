"""Auth API Router"""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.database import get_session
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserRegister, UserResponse

router = APIRouter(tags=["auth"])


@router.post("/users", status_code=201)
def register(request: dict, session: Session = Depends(get_session)):
    """Register a new user"""
    user_data = request["user"]
    repo = UserRepository(session)

    # Check if email already exists
    existing_user = repo.get_by_email(user_data["email"])
    if existing_user:
        raise HTTPException(status_code=422, detail="Email already registered")

    # Create user
    user = repo.create(
        email=user_data["email"],
        username=user_data["username"],
        password=user_data["password"],
    )

    return {
        "user": {
            "email": user.email,
            "username": user.username,
            "token": "dummy-jwt-token",
        }
    }

