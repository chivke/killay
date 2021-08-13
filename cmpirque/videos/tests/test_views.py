import pytest
from django.test import RequestFactory
from django.http.response import Http404

from cmpirque.videos.models import Video
from cmpirque.videos.views import (
    video_detail_view,
)


pytestmark = pytest.mark.django_db


class TestVideoDetailView:
    def test_get_video(self, video: Video, rf: RequestFactory):
        request = rf.get(f"/videos/{video.code}/")
        response = video_detail_view(request, slug=video.code)
        assert response.status_code == 200
        assert response.render()
        assert video.meta.title in str(response.content)

    def test_not_found(self, rf: RequestFactory):
        request = rf.get("/videos/-")
        with pytest.raises(Http404):
            video_detail_view(request, slug="wrong-code")
