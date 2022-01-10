import pytest

from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from django.http.response import Http404
from django.urls import resolve

from killay.videos.models import Video, VideoCategorization


from killay.videos.views import (
    video_category_list_view,
    video_collection_list_view,
    video_detail_view,
    video_search_list_view,
)


pytestmark = pytest.mark.django_db


class TestVideoDetailView:
    def test_get_video(
        self, video_categorization: VideoCategorization, rf: RequestFactory
    ):
        video = video_categorization.video
        collection = video_categorization.collection
        url = f"/videos/c/{collection.slug}/v/{video.code}/"
        request = rf.get(url)
        request.user = AnonymousUser()
        request.resolver_match = resolve(url)
        response = video_detail_view(request, **request.resolver_match.kwargs)

        assert response.status_code == 200
        assert response.render()
        assert video.meta.title in str(response.content)

    def test_not_found(self, rf: RequestFactory):
        request = rf.get("/videos/-")
        request.user = AnonymousUser()
        with pytest.raises(Http404):
            video_detail_view(request, slug="wrong-code")


class TestVideoCategoryDetailView:
    def test_get_list(
        self, rf: RequestFactory, video_categorization: VideoCategorization
    ):
        collection = video_categorization.collection
        category = video_categorization.categories.first()
        url = f"/videos/c/{collection.slug}/c/{category.slug}/"
        request = rf.get(url)
        request.resolver_match = resolve(url)
        request.user = AnonymousUser()
        response = video_category_list_view(request, **request.resolver_match.kwargs)
        assert response.status_code == 200
        assert response.render()
        response_content = str(response.content)
        assert category.name in response_content
        assert category.videos.first().video.meta.title in str(response.content)


class TestVideoCollectionView:
    def test_get_list(
        self, rf: RequestFactory, video_categorization: VideoCategorization
    ):
        collection = video_categorization.collection
        url = f"/videos/c/{collection.slug}/"
        request = rf.get(url)
        request.resolver_match = resolve(url)
        request.user = AnonymousUser()
        response = video_collection_list_view(request, **request.resolver_match.kwargs)
        assert response.status_code == 200
        assert response.render()
        response_content = str(response.content)
        assert collection.name in response_content
        assert collection.videos.first().video.meta.title in str(response.content)


class TestVideoSearchView:
    def test_search_nothing(self, rf: RequestFactory):
        query_param = ""
        request = rf.get(f"/videos/search/?q={query_param}")
        response = video_search_list_view(request)
        assert response.status_code == 302

    def test_search_in_code(self, video: Video, rf: RequestFactory):
        request = rf.get(f"/videos/search/?q={video.code}")
        response = video_search_list_view(request)
        assert response.status_code == 200
        assert response.render()
        assert video.meta.title in str(response.content)

    def test_search_in_title(self, video: Video, rf: RequestFactory):
        video.meta.title = "the real video"
        video.meta.save()
        query_param = video.meta.title[1:-1]
        request = rf.get(f"/videos/search/?q={query_param}")
        response = video_search_list_view(request)
        assert response.status_code == 200
        assert response.render()
        assert video.meta.title in str(response.content)

    def test_in_description(self, video: Video, rf: RequestFactory):
        video.meta.description = "the real video"
        video.meta.save()
        query_param = video.meta.title[1:-1]
        request = rf.get(f"/videos/search/?q={query_param}")
        response = video_search_list_view(request)
        assert response.status_code == 200
        assert response.render()
        assert video.meta.title in str(response.content)

    def test_no_results(self, video: Video, rf_msg: RequestFactory):
        video.meta.description = "the real video"
        video.meta.title = "the real video"
        video.meta.save()
        query_param = "other crazy"
        request = rf_msg("get", f"/videos/search/?q={query_param}")
        request.session.save()
        response = video_search_list_view(request)
        assert response.status_code == 200
        assert response.render()
