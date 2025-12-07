"""Tag API Router"""

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.database import get_session
from app.repositories.tag_repository import TagRepository

router = APIRouter(tags=["tags"])


@router.get("/tags", status_code=200)
def get_tags(session: Session = Depends(get_session)):
    """Get all tags"""
    repo = TagRepository(session)
    tags = repo.get_all_tags()
    return {"tags": tags}

