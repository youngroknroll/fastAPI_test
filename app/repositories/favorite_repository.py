"""Favorite Repository"""

from sqlmodel import Session, select

from app.models.favorite_model import Favorite


class FavoriteRepository:
    """Repository for Favorite operations"""

    def __init__(self, session: Session):
        self.session = session

    def create(self, user_id: int, article_id: int) -> Favorite:
        """Create a favorite"""
        favorite = Favorite(user_id=user_id, article_id=article_id)
        self.session.add(favorite)
        self.session.commit()
        self.session.refresh(favorite)
        return favorite

    def delete(self, user_id: int, article_id: int) -> None:
        """Delete a favorite"""
        statement = select(Favorite).where(
            Favorite.user_id == user_id, Favorite.article_id == article_id
        )
        favorite = self.session.exec(statement).first()
        if favorite:
            self.session.delete(favorite)
            self.session.commit()

    def get_article_ids_by_user(self, user_id: int) -> list[int]:
        """Get all article IDs favorited by a user"""
        statement = select(Favorite.article_id).where(Favorite.user_id == user_id)
        return list(self.session.exec(statement).all())

    def is_favorited(self, user_id: int, article_id: int) -> bool:
        """Check if user has favorited an article"""
        statement = select(Favorite).where(
            Favorite.user_id == user_id, Favorite.article_id == article_id
        )
        return self.session.exec(statement).first() is not None

    def count_by_article(self, article_id: int) -> int:
        """Count favorites for an article"""
        statement = select(Favorite).where(Favorite.article_id == article_id)
        return len(list(self.session.exec(statement).all()))

