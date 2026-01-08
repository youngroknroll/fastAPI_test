"""도메인 예외 클래스 정의

서비스 레이어에서는 이 예외들을 raise하고,
전역 예외 핸들러에서 HTTP 응답으로 변환합니다.
"""


class AppException(Exception):
    """애플리케이션 기본 예외"""

    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)


# ============================================================================
# 404 Not Found
# ============================================================================


class NotFoundException(AppException):
    """리소스를 찾을 수 없음 (404)"""

    pass


class ArticleNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__("Article not found")


class ProfileNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__("Profile not found")


class CommentNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__("Comment not found")


# ============================================================================
# 401 Unauthorized
# ============================================================================


class UnauthorizedException(AppException):
    """인증 실패 (401)"""

    pass


class AuthorizationHeaderMissingException(UnauthorizedException):
    def __init__(self):
        super().__init__("Authorization header missing")


class InvalidTokenException(UnauthorizedException):
    def __init__(self, detail: str = "Invalid token"):
        super().__init__(detail)


class UserNotFoundException(UnauthorizedException):
    """인증된 사용자를 찾을 수 없음"""

    def __init__(self):
        super().__init__("User not found")


# ============================================================================
# 403 Forbidden
# ============================================================================


class ForbiddenException(AppException):
    """권한 없음 (403)"""

    pass


class NotArticleAuthorException(ForbiddenException):
    def __init__(self):
        super().__init__("You are not the author of this article")


class NotCommentAuthorException(ForbiddenException):
    def __init__(self):
        super().__init__("You are not the author of this comment")


# ============================================================================
# 422 Unprocessable Entity (Validation/Business Logic Error)
# ============================================================================


class ValidationException(AppException):
    """비즈니스 로직 검증 실패 (422)"""

    pass


class EmailAlreadyRegisteredException(ValidationException):
    def __init__(self):
        super().__init__("Email already registered")


class UsernameAlreadyTakenException(ValidationException):
    def __init__(self):
        super().__init__("Username already taken")


class EmailNotFoundException(ValidationException):
    def __init__(self):
        super().__init__("Email not found")


class InvalidPasswordException(ValidationException):
    def __init__(self):
        super().__init__("Invalid password")


class CannotFollowYourselfException(ValidationException):
    def __init__(self):
        super().__init__("Cannot follow yourself")
