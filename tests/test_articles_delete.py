"""Articles: Delete Tests"""

def test_article_작성자가_삭제_요청하면_해당_article이_삭제된다(client, user1_header, article_payload):
    create_response = client.post("/articles", json=article_payload, headers=user1_header)
    slug = create_response.json()["article"]["slug"]

    delete_response = client.delete(f"/articles/{slug}", headers=user1_header)
    assert delete_response.status_code == 204

    get_response = client.get(f"/articles/{slug}")
    assert get_response.status_code == 404


def test_작성자가_아니면_403을_반환한다(client, user1_header, user2_header, article_payload):
    create_response = client.post("/articles", json=article_payload, headers=user1_header)
    slug = create_response.json()["article"]["slug"]

    delete_response = client.delete(f"/articles/{slug}", headers=user2_header)
    assert delete_response.status_code == 403


def test_slug가_존재하지_않으면_404를_반환한다(client, user1_header):
    delete_response = client.delete("/articles/non-existent-slug", headers=user1_header)
    assert delete_response.status_code == 404


def test_토큰_없이_삭제_요청_시_401을_반환한다(client, user1_header, article_payload):
    create_response = client.post("/articles", json=article_payload, headers=user1_header)
    slug = create_response.json()["article"]["slug"]

    delete_response = client.delete(f"/articles/{slug}")
    assert delete_response.status_code == 401
