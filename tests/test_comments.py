"""Comments Tests"""


def test_article에_댓글_작성_시_comment_객체를_반환한다(client):
    # given: 유저 등록 및 article 생성
    user_payload = {
        "user": {"email": "test@example.com", "password": "password123", "username": "testuser"}
    }
    user_response = client.post("/users", json=user_payload)
    token = user_response.json()["user"]["token"]
    headers = {"Authorization": f"Token {token}"}

    article_payload = {
        "article": {"title": "Test Article", "description": "Desc", "body": "Body"}
    }
    create_response = client.post("/articles", json=article_payload, headers=headers)
    slug = create_response.json()["article"]["slug"]

    # when: 댓글 작성
    comment_payload = {"comment": {"body": "This is a comment"}}
    response = client.post(f"/articles/{slug}/comments", json=comment_payload, headers=headers)

    # then: 200 반환 및 comment 객체 포함
    assert response.status_code == 200
    assert "comment" in response.json()
    assert response.json()["comment"]["body"] == "This is a comment"
    assert "id" in response.json()["comment"]
    assert "author" in response.json()["comment"]


def test_토큰이_없으면_comment_작성은_401을_반환한다(client):
    # given: 유저 등록 및 article 생성
    user_payload = {
        "user": {"email": "test@example.com", "password": "password123", "username": "testuser"}
    }
    user_response = client.post("/users", json=user_payload)
    token = user_response.json()["user"]["token"]
    headers = {"Authorization": f"Token {token}"}

    article_payload = {
        "article": {"title": "Test Article", "description": "Desc", "body": "Body"}
    }
    create_response = client.post("/articles", json=article_payload, headers=headers)
    slug = create_response.json()["article"]["slug"]

    # when: 토큰 없이 댓글 작성
    comment_payload = {"comment": {"body": "This is a comment"}}
    response = client.post(f"/articles/{slug}/comments", json=comment_payload)

    # then: 401 반환
    assert response.status_code == 401


def test_댓글_조회_시_comments_배열을_반환한다(client):
    # given: 유저 등록, article 생성, 댓글 작성
    user_payload = {
        "user": {"email": "test@example.com", "password": "password123", "username": "testuser"}
    }
    user_response = client.post("/users", json=user_payload)
    token = user_response.json()["user"]["token"]
    headers = {"Authorization": f"Token {token}"}

    article_payload = {
        "article": {"title": "Test Article", "description": "Desc", "body": "Body"}
    }
    create_response = client.post("/articles", json=article_payload, headers=headers)
    slug = create_response.json()["article"]["slug"]

    # 댓글 작성
    comment_payload = {"comment": {"body": "First comment"}}
    client.post(f"/articles/{slug}/comments", json=comment_payload, headers=headers)

    # when: 댓글 조회
    response = client.get(f"/articles/{slug}/comments")

    # then: 200 반환 및 comments 배열 포함
    assert response.status_code == 200
    assert "comments" in response.json()
    assert len(response.json()["comments"]) == 1
    assert response.json()["comments"][0]["body"] == "First comment"


def test_댓글_삭제_시_해당_댓글이_삭제된다(client):
    # given: 유저 등록, article 생성, 댓글 작성
    user_payload = {
        "user": {"email": "test@example.com", "password": "password123", "username": "testuser"}
    }
    user_response = client.post("/users", json=user_payload)
    token = user_response.json()["user"]["token"]
    headers = {"Authorization": f"Token {token}"}

    article_payload = {
        "article": {"title": "Test Article", "description": "Desc", "body": "Body"}
    }
    create_response = client.post("/articles", json=article_payload, headers=headers)
    slug = create_response.json()["article"]["slug"]

    # 댓글 작성
    comment_payload = {"comment": {"body": "Comment to delete"}}
    comment_response = client.post(f"/articles/{slug}/comments", json=comment_payload, headers=headers)
    comment_id = comment_response.json()["comment"]["id"]

    # when: 댓글 삭제
    response = client.delete(f"/articles/{slug}/comments/{comment_id}", headers=headers)

    # then: 204 반환
    assert response.status_code == 204

    # 댓글이 삭제되었는지 확인
    get_response = client.get(f"/articles/{slug}/comments")
    assert len(get_response.json()["comments"]) == 0


def test_다른_사용자의_댓글_삭제_시_403을_반환한다(client):
    # given: 유저1이 article 생성 및 댓글 작성, 유저2가 삭제 시도
    user1_payload = {
        "user": {"email": "user1@example.com", "password": "password123", "username": "user1"}
    }
    user1_response = client.post("/users", json=user1_payload)
    user1_token = user1_response.json()["user"]["token"]
    headers1 = {"Authorization": f"Token {user1_token}"}

    article_payload = {
        "article": {"title": "User1 Article", "description": "Desc", "body": "Body"}
    }
    create_response = client.post("/articles", json=article_payload, headers=headers1)
    slug = create_response.json()["article"]["slug"]

    # 유저1이 댓글 작성
    comment_payload = {"comment": {"body": "User1's comment"}}
    comment_response = client.post(f"/articles/{slug}/comments", json=comment_payload, headers=headers1)
    comment_id = comment_response.json()["comment"]["id"]

    # 유저2 등록
    user2_payload = {
        "user": {"email": "user2@example.com", "password": "password123", "username": "user2"}
    }
    user2_response = client.post("/users", json=user2_payload)
    user2_token = user2_response.json()["user"]["token"]
    headers2 = {"Authorization": f"Token {user2_token}"}

    # when: 유저2가 유저1의 댓글 삭제 시도
    response = client.delete(f"/articles/{slug}/comments/{comment_id}", headers=headers2)

    # then: 403 반환
    assert response.status_code == 403

