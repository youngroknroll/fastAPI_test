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

