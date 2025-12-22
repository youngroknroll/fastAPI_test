"""all fixtures"""

# DB and Client fixtures
from tests.fixtures.db_client_fixtures import session_fixture, client_fixture

# User fixtures
from tests.fixtures.user_fixtures import (
    로그인_유저1_api,
    로그인_유저2_api,
    게스트_api,
)

# Article fixtures
from tests.fixtures.article_fixtures import (
    article_api,
)


class Status:
    """API 응답 상태"""
    SUCCESS = "성공"
    CREATED = "생성됨"
    DELETED = "삭제됨"
    NOT_FOUND = "찾을 수 없음"
    FORBIDDEN = "권한 없음"
    UNAUTHORIZED = "인증 필요"
    
    _CODE_MAP = {
        200: "성공",
        201: "생성됨",
        204: "삭제됨",
        401: "인증 필요",
        403: "권한 없음",
        404: "찾을 수 없음",
    }
    
    @classmethod
    def of(cls, response):
        """Response 객체에서 상태 문자열 반환"""
        return cls._CODE_MAP.get(response.status_code, f"알 수 없음({response.status_code})")


ARTICLE_PAYLOAD = {
    "article": {"title": "Test Article", "description": "Test Desc", "body": "Test Body"}
}
