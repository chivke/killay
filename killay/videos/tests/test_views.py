import pytest

from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from django.http.response import Http404

from killay.videos.models import Video, VideoCategorization


from killay.videos.views import (
    video_category_list_view,
    video_detail_view,
    video_search_list_view,
)


pytestmark = pytest.mark.django_db


class TestVideoDetailView:
    def test_get_video(self, video: Video, rf: RequestFactory):
        request = rf.get(f"/videos/{video.code}/")
        request.user = AnonymousUser()
        response = video_detail_view(request, slug=video.code)
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
        category = video_categorization.categories.first()
        request = rf.get(f"/videos/category/{category.slug}/")
        response = video_category_list_view(request, slug=category.slug)
        assert response.status_code == 200
        assert response.render()
        assert category.videos.first().video.meta.title in str(response.content)


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
