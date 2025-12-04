"""Article Schemas"""

from typing import Optional

from pydantic import BaseModel


class ArticleCreate(BaseModel):
    """Article creation request"""

    title: str
    description: str
    body: str
    tagList: Optional[list[str]] = None

