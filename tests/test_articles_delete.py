"""Articles: Delete Tests"""


def test_article_작성자가_삭제_요청하면_해당_article이_삭제된다(client):
    # given: 유저 등록 및 article 생성
    user_payload = {
        "user": {"email": "test@example.com", "password": "password123", "username": "testuser"}
    }
    user_response = client.post("/users", json=user_payload)
    token = user_response.json()["user"]["token"]
    headers = {"Authorization": f"Token {token}"}

    article_payload = {
        "article": {"title": "Article to Delete", "description": "Desc", "body": "Body"}
    }
    create_response = client.post("/articles", json=article_payload, headers=headers)
    slug = create_response.json()["article"]["slug"]

    # when: article 삭제
    response = client.delete(f"/articles/{slug}", headers=headers)

    # then: 204 반환 (No Content)
    assert response.status_code == 204

    # article이 실제로 삭제되었는지 확인
    get_response = client.get(f"/articles/{slug}")
    assert get_response.status_code == 404


def test_작성자가_아니면_403을_반환한다(client):
    # given: 유저1이 article 생성, 유저2가 삭제 시도
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

    # 유저2 등록
    user2_payload = {
        "user": {"email": "user2@example.com", "password": "password123", "username": "user2"}
    }
    user2_response = client.post("/users", json=user2_payload)
    user2_token = user2_response.json()["user"]["token"]
    headers2 = {"Authorization": f"Token {user2_token}"}

    # when: 유저2가 유저1의 article 삭제 시도
    response = client.delete(f"/articles/{slug}", headers=headers2)

    # then: 403 반환
    assert response.status_code == 403


def test_slug가_존재하지_않으면_404를_반환한다(client):
    # given: 유저 등록
    user_payload = {
        "user": {"email": "test@example.com", "password": "password123", "username": "testuser"}
    }
    user_response = client.post("/users", json=user_payload)
    token = user_response.json()["user"]["token"]
    headers = {"Authorization": f"Token {token}"}

    # when: 존재하지 않는 slug로 삭제 요청
    response = client.delete("/articles/non-existent-slug", headers=headers)

    # then: 404 반환
    assert response.status_code == 404


def test_토큰_없이_삭제_요청_시_401을_반환한다(client):
    # given: 유저 등록 및 article 생성
    user_payload = {
        "user": {"email": "test@example.com", "password": "password123", "username": "testuser"}
    }
    user_response = client.post("/users", json=user_payload)
    token = user_response.json()["user"]["token"]
    headers = {"Authorization": f"Token {token}"}

    article_payload = {
        "article": {"title": "Article to Delete", "description": "Desc", "body": "Body"}
    }
    create_response = client.post("/articles", json=article_payload, headers=headers)
    slug = create_response.json()["article"]["slug"]

    # when: 토큰 없이 삭제 요청
    response = client.delete(f"/articles/{slug}")

    # then: 401 반환
    assert response.status_code == 401

