"""Tag API Router"""

from fastapi import APIRouter, Depends

from app.core.dependencies import get_tag_service
from app.services.tag_service import TagService

router = APIRouter(tags=["tags"])


@router.get("/tags", status_code=200)
def get_tags(service: TagService = Depends(get_tag_service)):
    """Get all tags"""
    tags = service.get_all_tags()
    return {"tags": tags}
