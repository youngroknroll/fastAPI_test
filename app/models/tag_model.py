"""Tag Model"""

from typing import Optional

from sqlmodel import Field, SQLModel


class Tag(SQLModel, table=True):
    """Tag model"""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)


class ArticleTag(SQLModel, table=True):
    """Article-Tag association table"""

    article_id: int = Field(foreign_key="articles.id", primary_key=True)
    tag_id: int = Field(foreign_key="tag.id", primary_key=True)

