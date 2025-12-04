"""Database configuration"""

from sqlmodel import Session, SQLModel, create_engine

# Import models to ensure they are registered
from app.models.article_model import Article  # noqa: F401
from app.models.follow_model import Follow  # noqa: F401
from app.models.user_model import User  # noqa: F401

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get database session"""
    with Session(engine) as session:
        yield session

