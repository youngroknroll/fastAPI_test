from tests.conftest import ARTICLE_PAYLOAD, Status


def test_좋아요를_누르면_좋아요_수가_증가한다(로그인_유저1_api):
    created_article = 로그인_유저1_api.create(ARTICLE_PAYLOAD).json()["article"]
    slug = created_article["slug"]

    좋아요_결과 = 로그인_유저1_api.favorite(slug)

    assert Status.of(좋아요_결과) == Status.SUCCESS
    assert 좋아요_결과.json()["article"]["favoritesCount"] == 1
    assert 좋아요_결과.json()["article"]["favorited"] == True


def test_좋아요를_취소하면_좋아요_수가_감소한다(로그인_유저1_api):
    created_article = 로그인_유저1_api.create(ARTICLE_PAYLOAD).json()["article"]
    slug = created_article["slug"]

    # 좋아요 추가
    로그인_유저1_api.favorite(slug)

    # 좋아요 취소
    취소_결과 = 로그인_유저1_api.unfavorite(slug)

    assert Status.of(취소_결과) == Status.SUCCESS
    assert 취소_결과.json()["article"]["favoritesCount"] == 0
    assert 취소_결과.json()["article"]["favorited"] == False


def test_로그인하지_않으면_좋아요를_누를_수_없다(로그인_유저1_api, 게스트_api):
    created_article = 로그인_유저1_api.create(ARTICLE_PAYLOAD).json()["article"]
    slug = created_article["slug"]

    좋아요_결과 = 게스트_api.favorite(slug)

    assert Status.of(좋아요_결과) == Status.UNAUTHORIZED
