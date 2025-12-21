"""Articles: Delete Tests"""

def test_유저는_자신의_게시글을_삭제할_수_있다(article_api, user1_header, article_payload):
    create_response = article_api.create(article_payload, headers=user1_header)
    slug = create_response.json()["article"]["slug"]

    delete_response = article_api.delete(slug, headers=user1_header)
    assert delete_response.status_code == 204

    get_response = article_api.get(slug, headers=user1_header)
    assert get_response.status_code == 404


def test_다른_사람의_게시글은_삭제할_수_없다(article_api, user1_header, user2_header, article_payload):
    create_response = article_api.create(article_payload, headers=user1_header)
    slug = create_response.json()["article"]["slug"]

    delete_response = article_api.delete(slug, headers=user2_header)
    assert delete_response.status_code == 403


def test_존재하지_않는_게시글은_삭제할_수_없다(article_api, user1_header):
    delete_response = article_api.delete(slug=None, headers=user1_header)
    assert delete_response.status_code == 404


def test_로그인하지_않으면_게시글을_삭제할_수_없다(article_api, user1_header, article_payload):
    create_response = article_api.create(article_payload, headers=user1_header)
    slug = create_response.json()["article"]["slug"]

    delete_response = article_api.delete(slug)
    assert delete_response.status_code == 401
