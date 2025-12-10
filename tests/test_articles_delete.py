"""Articles: Delete Tests"""

def test_article_작성자가_삭제_요청하면_해당_article이_삭제된다(client, user1_token):
    headers = {"Authorization": f"Token {user1_token}"}

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


def test_작성자가_아니면_403을_반환한다(client, user1_token, user2_token):
    headers1 = {"Authorization": f"Token {user1_token}"}

    article_payload = {
        "article": {"title": "User1 Article", "description": "Desc", "body": "Body"}
    }
    create_response = client.post("/articles", json=article_payload, headers=headers1)
    slug = create_response.json()["article"]["slug"]

    headers2 = {"Authorization": f"Token {user2_token}"}

    # when: 유저2가 유저1의 article 삭제 시도
    response = client.delete(f"/articles/{slug}", headers=headers2)

    # then: 403 반환
    assert response.status_code == 403


def test_slug가_존재하지_않으면_404를_반환한다(client, user1_token):
    headers = {"Authorization": f"Token {user1_token}"}

    # when: 존재하지 않는 slug로 삭제 요청
    response = client.delete("/articles/non-existent-slug", headers=headers)

    # then: 404 반환
    assert response.status_code == 404


def test_토큰_없이_삭제_요청_시_401을_반환한다(client, user1_token):
    headers = {"Authorization": f"Token {user1_token}"}

    article_payload = {
        "article": {"title": "Article to Delete", "description": "Desc", "body": "Body"}
    }
    create_response = client.post("/articles", json=article_payload, headers=headers)
    slug = create_response.json()["article"]["slug"]

    # when: 토큰 없이 삭제 요청
    response = client.delete(f"/articles/{slug}")

    # then: 401 반환
    assert response.status_code == 401

