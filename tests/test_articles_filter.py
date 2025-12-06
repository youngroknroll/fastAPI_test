"""Articles: Filter Tests"""


def test_author_username으로_필터링하면_해당_author_글만_반환한다(client):
    # given: 두 명의 유저가 각각 article 생성
    # 유저1 등록 및 article 생성
    user1_payload = {
        "user": {"email": "user1@example.com", "password": "password123", "username": "user1"}
    }
    user1_response = client.post("/users", json=user1_payload)
    user1_token = user1_response.json()["user"]["token"]

    headers1 = {"Authorization": f"Token {user1_token}"}
    article1_payload = {
        "article": {"title": "User1 Article", "description": "Desc1", "body": "Body1"}
    }
    client.post("/articles", json=article1_payload, headers=headers1)

    # 유저2 등록 및 article 생성
    user2_payload = {
        "user": {"email": "user2@example.com", "password": "password123", "username": "user2"}
    }
    user2_response = client.post("/users", json=user2_payload)
    user2_token = user2_response.json()["user"]["token"]

    headers2 = {"Authorization": f"Token {user2_token}"}
    article2_payload = {
        "article": {"title": "User2 Article", "description": "Desc2", "body": "Body2"}
    }
    client.post("/articles", json=article2_payload, headers=headers2)

    # when: author=user1로 필터링
    response = client.get("/articles?author=user1")

    # then: user1의 글만 반환
    assert response.status_code == 200
    data = response.json()
    assert len(data["articles"]) == 1
    assert data["articles"][0]["author"]["username"] == "user1"
    assert data["articlesCount"] == 1


def test_tag로_필터링하면_해당_tag가_있는_글만_반환한다(client):
    # given: 유저 등록 후 다른 태그를 가진 article 생성
    user_payload = {
        "user": {"email": "user@example.com", "password": "password123", "username": "testuser"}
    }
    user_response = client.post("/users", json=user_payload)
    token = user_response.json()["user"]["token"]
    headers = {"Authorization": f"Token {token}"}

    # python 태그가 있는 article
    article1_payload = {
        "article": {
            "title": "Python Article",
            "description": "Desc1",
            "body": "Body1",
            "tagList": ["python", "programming"],
        }
    }
    client.post("/articles", json=article1_payload, headers=headers)

    # javascript 태그가 있는 article
    article2_payload = {
        "article": {
            "title": "JavaScript Article",
            "description": "Desc2",
            "body": "Body2",
            "tagList": ["javascript", "programming"],
        }
    }
    client.post("/articles", json=article2_payload, headers=headers)

    # when: tag=python으로 필터링
    response = client.get("/articles?tag=python")

    # then: python 태그가 있는 글만 반환
    assert response.status_code == 200
    data = response.json()
    assert len(data["articles"]) == 1
    assert "python" in data["articles"][0]["tagList"]
    assert data["articlesCount"] == 1


def test_favorited_username으로_필터링하면_해당_유저가_좋아한_글만_반환한다(client):
    # given: 유저1이 article을 생성하고, 유저2가 그 중 하나를 좋아요
    # 유저1 등록 및 article 2개 생성
    user1_payload = {
        "user": {"email": "user1@example.com", "password": "password123", "username": "user1"}
    }
    user1_response = client.post("/users", json=user1_payload)
    user1_token = user1_response.json()["user"]["token"]
    headers1 = {"Authorization": f"Token {user1_token}"}

    article1_payload = {
        "article": {"title": "Article One", "description": "Desc1", "body": "Body1"}
    }
    article1_response = client.post("/articles", json=article1_payload, headers=headers1)
    article1_slug = article1_response.json()["article"]["slug"]

    article2_payload = {
        "article": {"title": "Article Two", "description": "Desc2", "body": "Body2"}
    }
    client.post("/articles", json=article2_payload, headers=headers1)

    # 유저2 등록 및 article1 좋아요
    user2_payload = {
        "user": {"email": "user2@example.com", "password": "password123", "username": "user2"}
    }
    user2_response = client.post("/users", json=user2_payload)
    user2_token = user2_response.json()["user"]["token"]
    headers2 = {"Authorization": f"Token {user2_token}"}

    # user2가 article1을 좋아요
    client.post(f"/articles/{article1_slug}/favorite", headers=headers2)

    # when: favorited=user2로 필터링
    response = client.get("/articles?favorited=user2")

    # then: user2가 좋아한 글만 반환
    assert response.status_code == 200
    data = response.json()
    assert len(data["articles"]) == 1
    assert data["articles"][0]["slug"] == article1_slug
    assert data["articlesCount"] == 1

