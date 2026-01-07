# FastAPI RealWorld 프로젝트 구조 분석

---

## 1. 프로젝트 개요

RealWorld API 명세를 FastAPI와 SQLModel로 구현한 백엔드 프로젝트이다.  
TDD(Test-Driven Development) 방식으로 개발되었으며, 계층형 아키텍처(Layered Architecture)를 적용했다.

### 기술 스택

| 구분 | 기술 |
|------|------|
| 웹 프레임워크 | FastAPI |
| ORM | SQLModel (SQLAlchemy + Pydantic) |
| 데이터베이스 | SQLite |
| 인증 | JWT (PyJWT) |
| 비밀번호 해싱 | Argon2 |
| 패키지 관리 | uv |
| 테스트 | pytest |
| 린터 | ruff |

---

## 2. 아키텍처 구조

### 계층형 아키텍처 (Layered Architecture)

```
[Client Request]
       |
       v
+------------------+
|   API Layer      |  <- FastAPI Router (엔드포인트 정의)
+------------------+
       |
       v
+------------------+
|  Service Layer   |  <- 비즈니스 로직 처리
+------------------+
       |
       v
+------------------+
| Repository Layer |  <- 데이터 접근 추상화
+------------------+
       |
       v
+------------------+
|   Model Layer    |  <- SQLModel ORM 정의
+------------------+
       |
       v
   [Database]
```

### 의존성 주입 (Dependency Injection)

- FastAPI의 `Depends`를 활용한 의존성 주입
- Repository Interface를 통한 의존성 역전 원칙(DIP) 적용
- `app/core/dependencies.py`에서 모든 의존성 관리

---

## 3. 디렉토리 구조

```
fastAPI_realworld/
|-- app/
|   |-- api/                    # API 라우터 레이어
|   |   |-- article.py          # 게시글 관련 엔드포인트
|   |   |-- auth.py             # 인증 관련 엔드포인트
|   |   |-- comment.py          # 댓글 관련 엔드포인트
|   |   |-- profile.py          # 프로필 관련 엔드포인트
|   |   |-- tag.py              # 태그 관련 엔드포인트
|   |
|   |-- services/               # 서비스 레이어 (비즈니스 로직)
|   |   |-- article_service.py  # 게시글 비즈니스 로직
|   |   |-- comment_service.py  # 댓글 비즈니스 로직
|   |   |-- profile_service.py  # 프로필 비즈니스 로직
|   |   |-- user_service.py     # 유저 비즈니스 로직
|   |
|   |-- repositories/           # 리포지토리 레이어 (데이터 접근)
|   |   |-- interfaces.py       # 리포지토리 인터페이스 (Protocol)
|   |   |-- article_repository.py
|   |   |-- comment_repository.py
|   |   |-- favorite_repository.py
|   |   |-- follow_repository.py
|   |   |-- tag_repository.py
|   |   |-- user_repository.py
|   |
|   |-- models/                 # ORM 모델 레이어
|   |   |-- base.py             # 공통 모델 (TimestampModel)
|   |   |-- article_model.py
|   |   |-- comment_model.py
|   |   |-- favorite_model.py
|   |   |-- follow_model.py
|   |   |-- tag_model.py
|   |   |-- user_model.py
|   |
|   |-- schemas/                # Pydantic 스키마 (입력 검증용)
|   |   |-- article_schema.py   # ArticleCreate, ArticleUpdate
|   |   |-- user_schema.py      # UserRegister, UserLogin, UserUpdate
|   |
|   |-- dtos/                   # 데이터 전송 객체
|   |   |-- request.py          # API 요청 DTO
|   |   |-- response.py         # API 응답 DTO
|   |
|   |-- core/                   # 핵심 설정
|   |   |-- database.py         # DB 연결 및 세션 관리
|   |   |-- dependencies.py     # 의존성 주입 함수
|   |   |-- security.py         # JWT, 비밀번호 해싱
|   |   |-- error_handlers.py   # 공통 에러 핸들러
|   |
|   |-- main.py                 # FastAPI 앱 진입점
|
|-- tests/                      # 테스트 파일
|   |-- conftest.py             # pytest 설정 및 공통 fixture
|   |-- fixtures/               # 테스트 fixture 모음
|   |-- test_*.py               # 테스트 파일들
|
|-- pyproject.toml              # 프로젝트 설정
|-- uv.lock                     # 의존성 잠금 파일
```

---

## 4. 레이어별 상세 설명

### 4.1 API Layer (app/api/)

FastAPI 라우터를 정의하며, HTTP 요청을 받아 서비스 레이어에 전달한다.

**주요 역할:**
- HTTP 요청/응답 처리
- 요청 데이터 검증 (Pydantic)
- 인증된 사용자 정보 주입
- 서비스 레이어 호출

**엔드포인트 목록:**

| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | /users | 회원가입 |
| POST | /users/login | 로그인 |
| GET | /user | 현재 유저 조회 |
| PUT | /user | 유저 정보 수정 |
| GET | /profiles/{username} | 프로필 조회 |
| POST | /profiles/{username}/follow | 팔로우 |
| DELETE | /profiles/{username}/follow | 언팔로우 |
| GET | /articles | 게시글 목록 조회 |
| POST | /articles | 게시글 작성 |
| GET | /articles/{slug} | 게시글 상세 조회 |
| PUT | /articles/{slug} | 게시글 수정 |
| DELETE | /articles/{slug} | 게시글 삭제 |
| POST | /articles/{slug}/favorite | 좋아요 |
| DELETE | /articles/{slug}/favorite | 좋아요 취소 |
| GET | /articles/{slug}/comments | 댓글 목록 조회 |
| POST | /articles/{slug}/comments | 댓글 작성 |
| DELETE | /articles/{slug}/comments/{id} | 댓글 삭제 |
| GET | /tags | 태그 목록 조회 |

### 4.2 Service Layer (app/services/)

비즈니스 로직을 처리하며, 리포지토리를 통해 데이터를 조회/수정한다.

**주요 역할:**
- 비즈니스 규칙 적용
- 여러 리포지토리 조합
- DTO 빌드 및 반환
- 권한 검증

**서비스 목록:**

| 서비스 | 설명 |
|--------|------|
| UserService | 회원가입, 로그인, 유저 정보 관리 |
| ArticleService | 게시글 CRUD, 좋아요, 필터링 |
| CommentService | 댓글 CRUD |
| ProfileService | 프로필 조회, 팔로우/언팔로우 |

### 4.3 Repository Layer (app/repositories/)

데이터베이스 접근을 추상화한다. Protocol을 사용한 인터페이스를 정의하여 의존성 역전을 구현했다.

**인터페이스 목록:**

| 인터페이스 | 설명 |
|------------|------|
| UserRepositoryInterface | 유저 CRUD |
| ArticleRepositoryInterface | 게시글 CRUD |
| TagRepositoryInterface | 태그 관리 |
| FavoriteRepositoryInterface | 좋아요 관리 |
| CommentRepositoryInterface | 댓글 CRUD |
| FollowRepositoryInterface | 팔로우 관계 관리 |

### 4.4 Model Layer (app/models/)

SQLModel을 사용한 ORM 모델을 정의한다.

**모델 목록:**

| 모델 | 테이블명 | 설명 |
|------|----------|------|
| User | users | 사용자 정보 |
| Article | articles | 게시글 정보 |
| Comment | comments | 댓글 정보 |
| Tag | tag | 태그 정보 |
| ArticleTag | articletag | 게시글-태그 다대다 관계 |
| Favorite | favorite | 좋아요 관계 (유저-게시글) |
| Follow | follows | 팔로우 관계 (유저-유저) |

### 4.5 DTO Layer (app/dtos/)

API 요청/응답에 사용되는 데이터 전송 객체를 정의한다.

**Request DTO:**
- UserRegisterRequest, UserLoginRequest, UserUpdateRequest
- ArticleCreateRequest, ArticleUpdateRequest
- CommentCreateRequest

**Response DTO:**
- UserResponse, ProfileResponse, AuthorResponse
- ArticleResponse
- CommentResponse

---

## 5. 데이터 모델 (ERD)

```
+------------+       +-------------+       +------------+
|   User     |       |   Article   |       |    Tag     |
+------------+       +-------------+       +------------+
| id (PK)    |<------| author_id   |       | id (PK)    |
| email      |       | id (PK)     |------>| name       |
| username   |       | slug        |       +------------+
| hashed_pwd |       | title       |            |
| bio        |       | description |            |
| image      |       | body        |       +------------+
+------------+       | created_at  |       | ArticleTag |
      |              | updated_at  |       +------------+
      |              +-------------+       | article_id |
      |                    |               | tag_id     |
      |                    |               +------------+
+------------+       +-------------+
|  Follow    |       |  Favorite   |
+------------+       +-------------+
| id (PK)    |       | user_id     |
| follower_id|       | article_id  |
| followee_id|       +-------------+
+------------+
      |
+------------+
|  Comment   |
+------------+
| id (PK)    |
| body       |
| author_id  |
| article_id |
| created_at |
| updated_at |
+------------+
```

---

## 6. 인증 구조

### JWT 토큰 인증

```
[Client] ---> Authorization: Token {jwt} ---> [Server]
                                                  |
                                          verify_token()
                                                  |
                                          get_user_by_id()
                                                  |
                                          [Authenticated User]
```

### 인증 관련 함수

| 함수 | 위치 | 설명 |
|------|------|------|
| create_access_token | security.py | JWT 토큰 생성 |
| verify_token | security.py | JWT 토큰 검증 |
| hash_password | security.py | Argon2 비밀번호 해싱 |
| verify_password | security.py | 비밀번호 검증 |
| get_current_user | dependencies.py | 현재 로그인 유저 조회 |
| get_current_user_optional | dependencies.py | 선택적 인증 (비로그인 허용) |

---

## 7. 테스트 현황

### 테스트 결과: 48개 테스트 모두 통과

```
tests/test_articles_create.py      - 5 tests
tests/test_articles_delete.py      - 4 tests
tests/test_articles_favorite.py    - 3 tests
tests/test_articles_filter.py      - 3 tests
tests/test_articles_read.py        - 3 tests
tests/test_articles_update.py      - 3 tests
tests/test_auth_current_user.py    - 2 tests
tests/test_auth_login.py           - 3 tests
tests/test_auth_register.py        - 7 tests
tests/test_auth_update_user.py     - 3 tests
tests/test_comments.py             - 5 tests
tests/test_profiles.py             - 5 tests
tests/test_tags.py                 - 2 tests
------------------------------------
Total: 48 passed
```

### 테스트 Fixture 구조

| 파일 | 설명 |
|------|------|
| db_client_fixtures.py | DB 세션 및 테스트 클라이언트 |
| user_fixtures.py | 로그인 유저, 게스트 유저 |
| article_fixtures.py | 게시글 관련 fixture |
| auth_fixtures.py | 인증 관련 fixture |

---

## 8. 구현 완료된 기능

### Auth (인증)
- [x] 회원가입 (POST /users)
- [x] 로그인 (POST /users/login)
- [x] 현재 유저 조회 (GET /user)
- [x] 유저 정보 수정 (PUT /user)

### Profile (프로필)
- [x] 프로필 조회 (GET /profiles/{username})
- [x] 팔로우 (POST /profiles/{username}/follow)
- [x] 언팔로우 (DELETE /profiles/{username}/follow)

### Article (게시글)
- [x] 게시글 목록 조회 (GET /articles)
- [x] 게시글 필터링 (author, tag, favorited)
- [x] 게시글 상세 조회 (GET /articles/{slug})
- [x] 게시글 작성 (POST /articles)
- [x] 게시글 수정 (PUT /articles/{slug})
- [x] 게시글 삭제 (DELETE /articles/{slug})
- [x] 좋아요 (POST /articles/{slug}/favorite)
- [x] 좋아요 취소 (DELETE /articles/{slug}/favorite)

### Comment (댓글)
- [x] 댓글 목록 조회 (GET /articles/{slug}/comments)
- [x] 댓글 작성 (POST /articles/{slug}/comments)
- [x] 댓글 삭제 (DELETE /articles/{slug}/comments/{id})

### Tag (태그)
- [x] 태그 목록 조회 (GET /tags)

---

## 9. 현재까지 수정/구현한 내용

### 아키텍처 설계
- 계층형 아키텍처 적용 (API -> Service -> Repository -> Model)
- Repository Interface를 통한 의존성 역전 원칙 적용
- FastAPI Depends를 활용한 의존성 주입 구현

### 코드 구조화
- DTO 분리 (Request/Response)
- Schema 분리 (입력 검증용 Pydantic 모델)
- 공통 에러 핸들러 유틸리티 작성 (error_handlers.py)
- TimestampModel 베이스 클래스 작성

### 데이터 모델
- User, Article, Comment, Tag, Follow, Favorite 모델 구현
- 다대다 관계 테이블 (ArticleTag) 구현

### 보안
- JWT 토큰 기반 인증 구현
- Argon2 비밀번호 해싱 적용
- 권한 검증 로직 구현 (작성자 확인)

### 테스트
- pytest 기반 테스트 환경 구축
- 한글 테스트 함수명 사용 (가독성 향상)
- Fixture 모듈화 (fixtures/ 디렉토리)
- 48개 테스트 케이스 작성 및 통과

---

## 10. 알려진 이슈 및 개선 사항

### N+1 쿼리 문제 (refactoring_plan.md 참조)

**현재 상태:**
- 게시글 목록 조회 시 각 게시글마다 작성자, 태그, 좋아요 수를 개별 쿼리로 조회
- 단건 조회도 작성자/태그/좋아요를 모두 개별 쿼리로 수행

**개선 방안:**
- 리포지토리 레벨에서 배치 조회 메서드 추가
- JOIN/GROUP BY를 활용한 쿼리 최적화
- 서비스 레이어에서 순수 DTO 빌더 유지 (추가 DB 호출 제거)

### 미구현 기능
- 페이지네이션 (limit, offset)
- Feed 엔드포인트 (팔로우한 유저의 게시글)
- 환경변수 기반 설정 관리

---

## 11. 실행 방법

```bash
# 의존성 설치
uv sync

# 테스트 실행
uv run pytest

# 서버 실행
uv run uvicorn app.main:app --reload

# 린터 실행
uv run ruff check app/
```

---

## 12. 참고 문서

- plan.md: TDD 스타일 테스트 리스트
- refactoring_plan.md: N+1 쿼리 문제 분석 및 개선 방안
- README.md: 프로젝트 소개

---

작성일: 2026-01-07

