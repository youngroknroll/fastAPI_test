"""Auth API Router"""

from fastapi import APIRouter

router = APIRouter(tags=["auth"])


@router.post("/users", status_code=201)
def register():
    """Register a new user"""
    return {"user": {}}

