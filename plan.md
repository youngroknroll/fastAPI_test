# RealWorld API 기반 Test List (TDD 스타일)

---

# 1. Auth: Register

* [x] 올바른 요청을 보내면 새 유저 객체를 반환한다
* [x] 반환된 유저 객체는 email을 포함한다
* [x] 반환된 유저 객체는 username을 포함한다
* [x] 반환된 유저 객체는 token을 포함한다
* [x] 이미 존재하는 이메일이면 422를 반환한다
* [x] 비밀번호가 없으면 422를 반환한다
* [x] username이 비어 있으면 422를 반환한다

---

# 2. Auth: Login

* [x] 올바른 email + password로 로그인하면 유저 객체를 반환한다
* [x] 잘못된 password면 422를 반환한다
* [x] 존재하지 않는 email이면 422를 반환한다

---

# 3. Auth: Get Current User

* [x] Authorization 토큰이 있으면 현재 유저 정보를 반환한다
* [x] Authorization 토큰이 없으면 401을 반환한다

---

# 4. Auth: Update User

* [x] 올바른 토큰으로 user 정보를 수정할 수 있다
* [x] 수정된 필드는 응답에서도 반영된다
* [x] 토큰 없이 요청하면 401을 반환한다

---

# 5. Profiles

* [x] 존재하는 username으로 프로필을 조회하면 profile 객체를 반환한다
* [x] 로그인하지 않아도 프로필 조회가 가능하다
* [ ] follow 요청을 보내면 following: true를 반환한다
* [ ] unfollow 요청을 보내면 following: false를 반환한다
* [ ] 자신을 follow 하려고 하면 422를 반환한다

---

# 6. Articles: Read

* [ ] GET /articles 호출 시 articles 배열을 반환한다
* [ ] articlesCount를 반환한다
* [ ] 단일 article 조회 시 slug에 해당하는 article을 반환한다
* [ ] 존재하지 않는 slug이면 404를 반환한다

---

# 7. Articles: Filter

* [ ] author=username으로 필터링하면 해당 author 글만 반환한다
* [ ] tag=…로 필터링하면 해당 tag가 있는 글만 반환한다
* [ ] favorited=username으로 필터링하면 해당 유저가 좋아한 글만 반환한다

---

# 8. Articles: Create

* [ ] 토큰이 있으면 새 article을 생성할 수 있다
* [ ] 생성된 article은 title을 포함한다
* [ ] 생성된 article은 slug를 포함한다
* [ ] 생성된 article은 author 정보를 포함한다
* [ ] 토큰 없이 article 생성 시 401을 반환한다

---

# 9. Articles: Update

* [ ] article 작성자가 수정 요청하면 해당 article이 수정된다
* [ ] 작성자가 아니면 403을 반환한다
* [ ] slug가 존재하지 않으면 404를 반환한다

---

# 10. Articles: Favorite

* [ ] favorite 요청 시 favoritesCount가 증가한다
* [ ] unfavorite 요청 시 favoritesCount가 감소한다
* [ ] 토큰 없이 favorite 요청 시 401을 반환한다

---

# 11. Comments

* [ ] article에 댓글 작성 시 comment 객체를 반환한다
* [ ] 토큰이 없으면 comment 작성은 401을 반환한다
* [ ] 댓글 조회 시 comments 배열을 반환한다
* [ ] 댓글 삭제 시 해당 댓글이 삭제된다
* [ ] 다른 사용자의 댓글 삭제 시 403을 반환한다

---

# 12. Tags

* [ ] GET /tags 요청 시 문자열 배열을 반환한다
* [ ] tag가 없으면 빈 배열을 반환한다

