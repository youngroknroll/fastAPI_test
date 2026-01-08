from app.repositories.interfaces import TagRepositoryInterface


class TagService:
    def __init__(self, tag_repo: TagRepositoryInterface):
        self._tag_repo = tag_repo

    def get_all_tags(self) -> list[str]:
        return self._tag_repo.get_all_tags()
