"""Articles: Update Tests"""


def test_slug가_존재하지_않으면_404를_반환한다(client):
    # given: 유저 등록
    user_payload = {
        "user": {"email": "test@example.com", "password": "password123", "username": "testuser"}
    }
    user_response = client.post("/users", json=user_payload)
    token = user_response.json()["user"]["token"]
    headers = {"Authorization": f"Token {token}"}

    # when: 존재하지 않는 slug로 수정 요청
    update_payload = {"article": {"title": "Updated Title"}}
    response = client.put("/articles/non-existent-slug", json=update_payload, headers=headers)

    # then: 404 반환
    assert response.status_code == 404


def test_article_작성자가_수정_요청하면_해당_article이_수정된다(client):
    # given: 유저 등록 및 article 생성
    user_payload = {
        "user": {"email": "test@example.com", "password": "password123", "username": "testuser"}
    }
    user_response = client.post("/users", json=user_payload)
    token = user_response.json()["user"]["token"]
    headers = {"Authorization": f"Token {token}"}

    article_payload = {
        "article": {"title": "Original Title", "description": "Desc", "body": "Body"}
    }
    create_response = client.post("/articles", json=article_payload, headers=headers)
    slug = create_response.json()["article"]["slug"]

    # when: article 수정
    update_payload = {"article": {"title": "Updated Title"}}
    response = client.put(f"/articles/{slug}", json=update_payload, headers=headers)

    # then: 200 반환 및 title 수정됨
    assert response.status_code == 200
    assert response.json()["article"]["title"] == "Updated Title"


def test_작성자가_아니면_403을_반환한다(client):
    # given: 유저1이 article 생성, 유저2가 수정 시도
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

    # when: 유저2가 유저1의 article 수정 시도
    update_payload = {"article": {"title": "Hacked Title"}}
    response = client.put(f"/articles/{slug}", json=update_payload, headers=headers2)

    # then: 403 반환
    assert response.status_code == 403

