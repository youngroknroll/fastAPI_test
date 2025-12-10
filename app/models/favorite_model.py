"""Favorite Model"""

from sqlmodel import Field, SQLModel


class Favorite(SQLModel, table=True):
    """Favorite model - tracks which users favorite which articles"""

    user_id: int = Field(foreign_key="users.id", primary_key=True)
    article_id: int = Field(foreign_key="articles.id", primary_key=True)

