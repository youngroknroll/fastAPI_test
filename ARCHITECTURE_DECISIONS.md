# Architecture Decision Record (ADR)

## N+1 쿼리 제거를 위한 배치 조회 기반 아키텍처 도입

---

## 1. 배경 (Context)

게시글 목록 조회 API에서 성능 저하가 발생하고 있음을 확인했다.
단순 기능 구현 단계에서는 문제가 드러나지 않았으나, 게시글 수가 증가하면서 **쿼리 수가 선형적으로 증가하는 구조(N+1)** 가 명확해졌다.

### 1.1 문제 상황

게시글 100개 조회 시 실제 발생하던 쿼리 수는 다음과 같다.

```
- Article 조회: 1
- 작성자 조회: 100
- 태그 조회: 100
- 즐겨찾기 카운트 조회: 100
- 즐겨찾기 여부 조회: 100

총 401 쿼리
```

### 1.2 근본 원인 분석

문제의 원인은 단순히 ORM 사용 방식이 아니라 **계층 책임 붕괴**에 있었다.

* Service 계층이 DB 접근 로직을 직접 수행
* `_build_article_response()` 내부에서 반복적인 DB 조회 발생
* Presenter 성격의 코드가 비즈니스/영속성 로직을 함께 포함
* Repository가 단순 CRUD만 제공하여 조회 최적화 불가

즉, **배치 조회가 불가능한 구조적 문제**였다.

---

## 2. 결정 (Decision)

다음과 같은 방향으로 아키텍처를 수정한다.

1. Repository 계층의 책임을 “단순 CRUD”가 아닌 **조회 최적화 단위**까지 확장한다.
2. Service 계층은 **배치 조회 결과를 받아 조율**만 수행한다.
3. Presenter 역할을 제거하고, DTO를 **순수 변환 계층**으로 한정한다.
4. dict 기반 반환을 제거하고 **명시적 DTO 타입**을 반환한다.

---

## 3. Repository 계층 개선

### 3.1 기존 구조의 한계

```python
articles = article_repo.get_all()
for article in articles:
    author = user_repo.get_by_id(article.author_id)
    tags = tag_repo.get_tags_for_article(article.id)
    count = favorite_repo.count_by_article(article.id)
```

* Repository는 개별 엔티티만 조회
* Service가 반복적으로 Repository를 호출
* 배치 조회 불가능

### 3.2 개선된 접근

```python
articles_data = article_repo.get_all_with_relations()
```

Repository는 **Article + Author + Tags + Favorite 정보**를 한 번에 조회한다.

반환 구조 예시:

```python
{
  "article": Article,
  "author": User,
  "tag_list": list[str],
  "favorites_count": int,
  "favorited": bool
}
```

### 3.3 구현 전략

* 작성자: `IN` 절 기반 배치 조회
* 태그: 조인 테이블 JOIN
* 즐겨찾기 카운트: `GROUP BY`
* 즐겨찾기 여부: 조건 기반 조회
* DB 왕복 최소화

### 3.4 결과

```
총 쿼리 수
- Before: 401
- After: 5
- 감소율: 약 98%
```

---

## 4. Service 계층 책임 재정의

### 4.1 기존 문제점

```python
def get_articles(...):
    articles = self._article_repo.get_all()
    for article in articles:
        self._build_article_response(article)
```

* Service 내부에서 반복 조회
* 응답 생성 로직이 DB 접근에 의존

### 4.2 개선된 구조

```python
def get_articles(...):
    article_ids = self._get_filtered_article_ids(...)
    articles_data = self._article_repo.get_all_with_relations(
        author_id=author_id,
        article_ids=article_ids
    )

    return {
        "articles": [
            ArticleResponse.from_article_data(data)
            for data in articles_data
        ],
        "articlesCount": len(articles_data)
    }
```

Service의 책임은 다음으로 한정된다.

* 필터 조건 조율
* 비즈니스 규칙 검증
* DTO 변환 흐름 제어

DB 접근은 Repository에서만 수행한다.

---

## 5. Presenter 제거 및 DTO 순수화

### 5.1 기존 문제

```python
def _build_article_response(...):
    favorites_count = self._favorite_repo.count_by_article(...)
```

* Presenter가 DB에 의존
* 테스트 불가
* 부수 효과 발생

### 5.2 개선 후

```python
@classmethod
def from_article_data(cls, data: dict) -> "ArticleResponse":
    return cls(...)
```

DTO는 다음 조건을 만족한다.

* DB 접근 없음
* 입력 → 출력이 결정적인 순수 함수
* 테스트 가능

---

## 6. 타입 안전성 강화

### 6.1 dict 반환의 문제

* IDE 자동완성 불가
* 타입 체커 무력화
* 응답 구조가 암묵적

### 6.2 명시적 DTO 반환

```python
def register_user(...) -> UserResponse:
    return UserResponse(...)
```

효과:

* IDE 자동완성 지원
* mypy 타입 검증 가능
* 코드 자체가 문서 역할 수행

### 6.3 응답 Wrapper 도입

```python
class UserResponseWrapper(BaseModel):
    user: UserResponse
```

* FastAPI response_model과 결합
* Swagger 스키마 자동 생성
* API 계약 명확화

---

## 7. 계층별 책임 정리

### Before

* Service / Presenter / Repository 경계 불분명
* DB 접근 분산
* 최적화 불가능

### After

```
API        : 요청/응답 포장, 검증
Service    : 비즈니스 조율
Repository : 배치 조회 및 최적화
DTO        : 순수 데이터 변환
```

---

## 8. 효과

### 성능

* 쿼리 수: 401 → 5
* 응답 시간: 수 초 → 수십 ms 수준

### 개발 경험

* 자동완성 및 타입 추론 가능
* 리팩터링 안정성 향상
* Swagger 문서 신뢰도 상승

### 유지보수성

* 계층 간 결합도 감소
* 테스트 범위 축소
* N+1 재발 가능성 제거

---

## 9. 확장 패턴

다른 도메인(Comment 등)에도 동일 패턴 적용 가능.

1. Repository 배치 메서드 추가
2. DTO `from_*_data()` 추가
3. Service에서 조율만 수행
4. API는 Wrapper DTO로 응답

---

* **아키텍처 책임 재정의**
* **계층 간 의존성 정리**
* **타입 기반 설계로의 전환**


