import pytest

from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

from cmpirque.videos.models import Video
from cmpirque.videos.views.video_admin import (
    AdminRequiredMixin,
    video_create_view,
    video_delete_view,
    video_update_view,
)
from cmpirque.users.models import User


pytestmark = pytest.mark.django_db


class TestAdminRequiredMixin:
    def test_is_not_superuser(
        self, video: Video, rf: RequestFactory
    ):
        request = rf.get(f"/videos/{video.code}/")
        request.user = AnonymousUser()
        mixin = AdminRequiredMixin()
        mixin.request = request
        response = mixin.dispatch(request)
        assert response.status_code == 302
        assert "login" in response.url

    def test_is_superuser(
        self, admin_user: User, video: Video, rf: RequestFactory
    ):
        request = rf.get(f"/videos/{video.code}/")
        request.user = admin_user
        mixin = AdminRequiredMixin()
        mixin.request = request
        attribute_error = None
        with pytest.raises(AttributeError) as error:
            attribute_error = error
            mixin.dispatch(request)
        assert "dispatch" in attribute_error.value.args[0]


class TestVideoCreateView:
    def test_get(self, admin_user: User, rf: RequestFactory):
        request = rf.get("/videos/~create/")
        request.user = admin_user
        response = video_create_view(request)
        assert response.render()
        assert response.status_code == 200

    def test_create(self, admin_user: User, rf: RequestFactory):
        data = {"code": "fake", "title": "fake"}
        request = rf.post("/videos/~create/", data)
        request.user = admin_user
        response = video_create_view(request)
        assert response.status_code == 302
        video = Video.objects.get(code="fake")
        assert video.code == data["code"]
        assert video.meta.title == data["title"]

    def test_fail_create(self, admin_user: User, rf: RequestFactory):
        data = {"code": "fake"}
        request = rf.post("/videos/~create/", data)
        request.user = admin_user
        response = video_create_view(request)
        assert response.status_code == 200
        assert "title" in response.context_data["meta_form"].errors


class TestVideoUpdateView:
    def test_get(self, admin_user: User, video: Video, rf: RequestFactory):
        request = rf.get(f"/videos/{video.code}/~update/")
        request.user = admin_user
        response = video_update_view(request, slug=video.code)
        assert response.status_code == 200
        assert response.render()
        assert video.meta.title in str(response.content)

    def test_update(self, admin_user: User, video: Video, rf: RequestFactory):
        data = {"code": "fake", "title": "fake"}
        request = rf.post(f"/videos/{video.code}/~update/", data)
        request.user = admin_user
        response = video_update_view(request, slug=video.code)
        video.refresh_from_db()
        assert response.status_code == 302
        assert video.code == data["code"]
        assert video.meta.title == data["title"]

    def test_fail_update(
            self, admin_user: User, video: Video, rf: RequestFactory
    ):
        data = {"code": "fake"}
        request = rf.post(f"/videos/{video.code}/~update/", data)
        request.user = admin_user
        response = video_update_view(request, slug=video.code)
        assert response.status_code == 200
        assert "title" in response.context_data["meta_form"].errors


class TestVideoDeleteView:
    def test_get(self,  admin_user: User, video: Video, rf: RequestFactory):
        request = rf.get(f"/videos/{video.code}/~delete/")
        request.user = admin_user
        response = video_delete_view(request, slug=video.code)
        assert response.status_code == 200
        assert response.render()
        assert video.code in str(response.content)

    def test_delete(self, admin_user: User, video: Video, rf: RequestFactory):
        data = {"code": "fake", "title": "fake"}
        request = rf.post(f"/videos/{video.code}/~update/", data)
        request.user = admin_user
        response = video_delete_view(request, slug=video.code)
        with pytest.raises(Video.DoesNotExist):
            video.refresh_from_db()
        assert response.status_code == 302
