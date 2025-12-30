# Article 서비스 구조/N+1 메모

## 현재 구조 요약
- 리포지토리: 엔티티별 단순 CRUD만 제공 (`article_repository.py`, `tag_repository.py`, `favorite_repository.py`, `user_repository.py`). 관계/집계/배치 조회 없음.
- 서비스: `ArticleService`가 작성자, 태그, 즐겨찾기 카운트/여부를 각각 리포지토리로 반복 호출해 응답을 조립.
- 프리젠터: `_build_article_response`가 내부에서 즐겨찾기 카운트/여부를 다시 DB에 질의하는 순수 함수가 아님.

## N+1/불필요 DB 콜 지점
- `get_articles` 루프: 기사마다 작성자 조회, 태그 조회, `_build_article_response` 호출 시 즐겨찾기 카운트/여부 추가 조회 → 기사 수 * (작성자+태그+카운트+여부) 만큼 쿼리 증가.
- `get_article_by_slug`: 단건 조회도 작성자/태그/즐겨찾기 카운트/여부를 모두 개별 쿼리로 수행.
- `favorite_article`/`unfavorite_article`: 좋아요 처리 후 `_build_article_response`에서 다시 카운트/여부 쿼리.

## 개선 초안 (간단히)
- 리포지토리 단계에서 관계/집계를 한 번에 가져오는 배치 메서드 추가 (`get_all_with_relations`, `count_by_article_bulk`, `get_tags_for_articles`, `get_favorited_article_ids` 등).
- 서비스는 배치 조회 결과를 받아 권한/필터만 처리하고, 프리젠터는 순수 DTO 빌더로 유지(추가 DB 콜 없음).
- ORM에서 가능하면 join/annotate(또는 그룹바이)로 작성자·태그·즐겨찾기 카운트/여부를 한/소수 쿼리로 반환.

## 배치/annotate 시그니처 초안
- ArticleRepositoryInterface
  - `get_all_with_relations(author_id: int | None = None, article_ids: list[int] | None = None, current_user_id: int | None = None) -> list[ArticleWithRelations]`
  - `get_by_slug_with_relations(slug: str, current_user_id: int | None = None) -> ArticleWithRelations | None`
- FavoriteRepositoryInterface
  - `count_by_article_bulk(article_ids: list[int]) -> dict[int, int]`
  - `get_favorited_article_ids(user_id: int, article_ids: list[int] | None = None) -> set[int]`
- TagRepositoryInterface
  - `get_tags_for_articles(article_ids: list[int]) -> dict[int, list[str]]`

DTO 초안:
```python
@dataclass
class ArticleWithRelations:
    article: Article
    author: User
    tags: list[str]
    favorites_count: int
    is_favorited: bool
```

## 프리젠터/서비스 분리 계획
- `_build_article_response`는 DB 콜 없이 DTO만 조립하는 순수 함수로 유지.
- 서비스 단계에서 필요한 데이터(작성자, 태그, favorites_count, is_favorited)를 모두 확보한 뒤 프리젠터에 전달.
- 라우터 → 서비스 → 프리젠터 흐름만 남기고, 서비스가 프리젠터 내부로 Repo 인스턴스를 넘기지 않도록 한다.

서비스 리팩터링 흐름 예시:
- 목록 조회: `articles = article_repo.get_all_with_relations(...)` → 여기서 작성자/태그/카운트/즐겨찾기 여부 포함.
- 단건 조회: `get_by_slug_with_relations(slug, current_user_id)` 활용.
- 좋아요/취소: 상태 변경 후 동일한 배치 메서드(또는 단건 relations 메서드)로 갱신된 뷰 모델 재조회.

프리젠터 시그니처 예시:
```python
def build_article_response(
    article: Article,
    author: User,
    tags: list[str],
    favorites_count: int,
    is_favorited: bool,
) -> dict:
    ...
```

적용 순서 제안:
1) 인터페이스에 배치/annotate 메서드 추가 → 구현에 반영.
2) 서비스에서 `_build_article_response` 호출부를 모두 “사전 조회 값” 인자로 교체.
3) `_build_article_response`를 순수 프리젠터로 변경하거나 별도 모듈로 이동.

