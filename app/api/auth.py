"""Auth API Router"""

from fastapi import APIRouter

from app.schemas.user_schema import UserRegister, UserResponse

router = APIRouter(tags=["auth"])


@router.post("/users", status_code=201)
def register(request: dict):
    """Register a new user"""
    user_data = request["user"]
    return {
        "user": {
            "email": user_data["email"],
            "username": user_data["username"],
            "token": "dummy-jwt-token",
        }
    }

