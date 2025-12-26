from typing import Optional

from pydantic import BaseModel


class ArticleCreate(BaseModel):

    title: str
    description: str
    body: str
    tagList: Optional[list[str]] = None


class ArticleUpdate(BaseModel):

    title: Optional[str] = None
    description: Optional[str] = None
    body: Optional[str] = None

