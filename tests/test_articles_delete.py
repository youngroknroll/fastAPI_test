"""Articles: Delete Tests"""

def test_article_작성자가_삭제_요청하면_해당_article이_삭제된다(article_api, user1_header, article_payload):
    create_response = article_api.create(article_payload, headers=user1_header)
    slug = create_response.json()["article"]["slug"]

    delete_response = article_api.delete(slug, headers=user1_header)
    assert delete_response.status_code == 204

    get_response = article_api.get(slug, headers=user1_header)
    assert get_response.status_code == 404


def test_작성자가_아니면_403을_반환한다(article_api, user1_header, user2_header, article_payload):
    create_response = article_api.create(article_payload, headers=user1_header)
    slug = create_response.json()["article"]["slug"]

    delete_response = article_api.delete(slug, headers=user2_header)
    assert delete_response.status_code == 403


def test_slug가_존재하지_않으면_404를_반환한다(article_api, user1_header):
    delete_response = article_api.delete(slug=None, headers=user1_header)
    assert delete_response.status_code == 404


def test_토큰_없이_삭제_요청_시_401을_반환한다(article_api, user1_header, article_payload):
    create_response = article_api.create(article_payload, headers=user1_header)
    slug = create_response.json()["article"]["slug"]

    delete_response = article_api.delete(slug)
    assert delete_response.status_code == 401
