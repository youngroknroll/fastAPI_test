from sqlmodel import Session, select

from app.models.favorite_model import Favorite


class FavoriteRepository:

    def __init__(self, session: Session):
        self._session = session

    def create(self, user_id: int, article_id: int) -> Favorite:
        favorite = Favorite(user_id=user_id, article_id=article_id)
        self._session.add(favorite)
        self._session.commit()
        self._session.refresh(favorite)
        return favorite

    def delete(self, user_id: int, article_id: int) -> None:
        statement = select(Favorite).where(
            Favorite.user_id == user_id, Favorite.article_id == article_id
        )
        favorite = self._session.exec(statement).first()
        if favorite:
            self._session.delete(favorite)
            self._session.commit()

    def get_article_ids_by_user(self, user_id: int) -> list[int]:
        statement = select(Favorite.article_id).where(Favorite.user_id == user_id)
        return list(self._session.exec(statement).all())

    def is_favorited(self, user_id: int, article_id: int) -> bool:
        statement = select(Favorite).where(
            Favorite.user_id == user_id, Favorite.article_id == article_id
        )
        return self._session.exec(statement).first() is not None

    def count_by_article(self, article_id: int) -> int:
        statement = select(Favorite).where(Favorite.article_id == article_id)
        return len(list(self._session.exec(statement).all()))
