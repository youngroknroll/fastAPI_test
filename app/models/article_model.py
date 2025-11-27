from sqlmodel import SQLModel, Field


class Article(SQLModel, table=True):
    """Article 모델 - 게시글 데이터"""
    
    __tablename__ = "articles"
    
    id: int | None = Field(default=None, primary_key=True)
    title: str
    author: str
    slug: str