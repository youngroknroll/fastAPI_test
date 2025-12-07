# 🔧 리팩토링 체크리스트

> 작성일: 2025-12-01
> 목적: TDD 원칙 유지하면서 아키텍처 개선 및 인증 시스템 수정

---

## 🔴 Phase 1: 인증 시스템 수정 (필수)

### 1.1 JWT 토큰 구현
- [x] JWT 라이브러리 추가 (`PyJWT`)
- [x] 토큰 생성 함수 작성 (`create_access_token`)
- [x] 토큰 검증 함수 작성 (`verify_token`)
- [x] `app/core/security.py` 파일 생성

### 1.2 인증 의존성 함수 생성
- [x] `get_current_user` 의존성 함수 작성 (토큰에서 user 추출)
- [x] `app/core/dependencies.py` 파일 생성
- [x] 모든 엔드포인트에서 `get_first_user()` 제거
- [x] `Depends(get_current_user)` 사용

### 1.3 기존 코드 수정
- [x] `register`: JWT 토큰 생성하여 반환
- [x] `login`: JWT 토큰 생성하여 반환
- [x] `get_current_user`: 의존성 함수로 변경
- [x] `update_user`: 의존성 사용
- [x] `follow_user`: 의존성 사용
- [x] `unfollow_user`: 의존성 사용

---

## 🟡 Phase 2: Service 레이어 추가 (강력 추천)

### 2.1 Service 파일 생성
- [x] `app/services/user_service.py` 생성
- [x] `app/services/profile_service.py` 생성

### 2.2 비즈니스 로직 이동

**UserService:**
- [x] `register_user(email, username, password)` - 중복 체크 포함
- [x] `login_user(email, password)` - 인증 로직
- [x] `update_user(user_id, update_data)` - 업데이트 로직
- [x] `get_user_by_id(user_id)` - 조회

**ProfileService:**
- [x] `get_profile(username, current_user_id=None)` - following 상태 체크
- [x] `follow_user(follower_id, followee_username)` - 팔로우 로직
- [x] `unfollow_user(follower_id, followee_username)` - 언팔로우 로직

### 2.3 Repository 확장

**FollowRepository 생성:**
- [x] `app/repositories/follow_repository.py` 생성
- [x] `create_follow(follower_id, followee_id)` 메서드
- [x] `delete_follow(follower_id, followee_id)` 메서드
- [x] `is_following(follower_id, followee_id)` 메서드

**UserRepository 확장:**
- [x] `get_by_id(user_id)` 메서드 추가
- [ ] `update(user, **kwargs)` 메서드 추가

### 2.4 API 레이어 수정
- [x] `auth.py`: Service 호출로 변경
- [x] `profile.py`: Service 호출로 변경
- [x] 직접 DB 쿼리 제거 (profile.py line 90-96)

---

## 🟢 Phase 3: 코드 품질 개선 (선택적, 나중에 가능)

### 3.1 비밀번호 해싱
- [ ] `bcrypt` 또는 `passlib` 추가
- [ ] `hash_password()` 함수
- [ ] `verify_password()` 함수
- [ ] 모든 비밀번호 저장/검증 로직 수정

### 3.2 Response 모델 사용
- [ ] API 엔드포인트에 `response_model` 지정
- [ ] 딕셔너리 반환 → Pydantic 모델 반환으로 변경

### 3.3 중복 코드 제거
- [ ] 공통 에러 처리 함수
- [ ] 공통 응답 포맷 함수

---

## 📊 우선순위 정리

### 🎯 지금 반드시 해야 할 것:
- ✅ Phase 1: 인증 시스템 (JWT + 의존성)
- ✅ Phase 2: Service 레이어 + FollowRepository

### ⏳ 나중에 해도 되는 것:
- ⏸️ Phase 3: 비밀번호 해싱, Response 모델, 중복 코드 정리

---

## 🎬 작업 순서

### Step 1: 인증 인프라 구축 (예상: 20분)
1. `app/core/security.py` - JWT 함수
2. `app/core/dependencies.py` - get_current_user 의존성
3. `pyproject.toml`에 PyJWT 추가

### Step 2: 인증 적용 (예상: 15분)
4. auth.py 수정 (register, login에서 JWT 생성)
5. 모든 엔드포인트에서 get_first_user() → Depends(get_current_user)

### Step 3: Service 레이어 생성 (예상: 20분)
6. UserService 생성 및 비즈니스 로직 이동
7. ProfileService 생성
8. FollowRepository 생성

### Step 4: API 레이어 정리 (예상: 10분)
9. auth.py에서 Service 호출
10. profile.py에서 Service 호출

### Step 5: 테스트 확인 (예상: 5분)
11. 전체 테스트 실행
12. 깨진 테스트 수정

**총 예상 시간: 약 70분**

---

## 🚨 현재 발견된 주요 문제점

### 0. Null 체크 누락 (잠재적 버그)
```python
# ❌ 문제 코드 (comment_service.py, article_service.py)
for comment in comments:
    author = self.user_repo.get_by_id(comment.author_id)  # author가 None일 수 있음
    comments_data.append(self._format_comment_response(comment, author)["comment"])
    # author.username 접근 시 AttributeError 발생 가능

# ✅ 수정 방안
# 1. author가 None인 경우 건너뛰기
# 2. author가 None인 경우 기본값 사용
# 3. FK CASCADE로 유저 삭제 시 댓글도 삭제
```

### 1. 레이어드 아키텍처 위반
```
현재: API Router → Repository (직접 호출) ❌
수정: API Router → Service → Repository ✅
```

### 2. Dummy 인증 구현
```python
# ❌ 문제 코드
follower = repo.get_first_user()  # 항상 첫 번째 유저 반환

# ✅ 수정 후
current_user = Depends(get_current_user)  # 토큰에서 실제 유저 식별
```

### 3. 비밀번호 평문 저장
```python
# ❌ 문제 코드
password=user_data.password  # 평문 저장
if user.hashed_password != user_data.password:  # 평문 비교

# ✅ 수정 후 (Phase 3)
hashed_password = hash_password(user_data.password)
verify_password(user_data.password, user.hashed_password)
```

### 4. API 레이어에서 직접 DB 쿼리
```python
# ❌ 문제 코드 (profile.py)
statement = select(Follow).where(...)
follow = session.exec(statement).first()

# ✅ 수정 후
follow_repo.delete_follow(follower_id, followee_id)
```

### 5. 중복된 인증 로직
```python
# ❌ 문제 코드 (여러 파일에서 반복)
if authorization is None:
    raise HTTPException(status_code=401, detail="Unauthorized")

# ✅ 수정 후
def some_endpoint(current_user: User = Depends(get_current_user)):
    # 자동으로 인증 체크
```

---

## 📝 진행 상황

- [x] Phase 1: 인증 시스템 수정
- [x] Phase 2: Service 레이어 추가
- [ ] Phase 3: 코드 품질 개선 (선택)

---

## ✅ 완료 후 확인사항

- [x] 모든 기존 테스트 통과 (49개)
- [x] 새로운 버그 없음
- [x] 레이어드 아키텍처 준수
- [x] 인증이 올바르게 작동 (여러 유저 시나리오)
- [ ] 코드 중복 최소화

---

## 💡 참고사항

### TDD 리팩토링 원칙
> "리팩토링은 테스트가 통과한 상태에서 시작하고, 테스트가 통과한 상태로 끝나야 한다"

### Kent Beck의 "Tidy First" 원칙
> "구조적 변경(리팩토링)과 행동적 변경(새 기능)을 분리하라"

### 현재 전략
1. 구조적 변경: 지금 리팩토링 (Phase 1, 2)
2. 행동적 변경: 나중에 Articles 개발

---

**마지막 업데이트:** 2025-12-07  
**상태:** Phase 1, 2 완료 / Phase 3 진행 가능

