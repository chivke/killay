import pytest
import re
from django.contrib.auth.models import AnonymousUser
from django.core import mail
from django.test import RequestFactory

from killay.users.models import User
from killay.users.tests.factories import UserFactory
from killay.users.views import UserRedirectView, UserUpdateView, user_update_view

pytestmark = pytest.mark.django_db


class TestUserUpdateView:
    def test_get_success_url(self, user: User, rf: RequestFactory):
        view = UserUpdateView()
        request = rf.get("/fake-url/")
        request.user = user
        view.request = request
        assert view.get_success_url() == "/users/~update/"

    def test_get_object(self, user: User, rf: RequestFactory):
        view = UserUpdateView()
        request = rf.get("/fake-url/")
        request.user = user
        view.request = request
        view.kwargs = {}
        assert view.get_object() == user

    def test_update(self, user: User, rf_msg: RequestFactory):
        data = {"email": "new@localhost"}
        request = rf_msg("post", "/users/~update/", data)
        request.user = user
        response = user_update_view(request)
        assert response.status_code == 302
        user.refresh_from_db()
        assert user.email == data["email"]


class TestUserRedirectView:
    def test_get_redirect_url(self, user: User, rf: RequestFactory):
        view = UserRedirectView()
        request = rf.get("/fake-url")
        request.user = user
        view.request = request
        assert view.get_redirect_url() == "/users/~update/"


class TestUserDetailView:
    def test_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = UserFactory()
        response = user_update_view(request, username=user.username)
        assert response.status_code == 200

    def test_not_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = AnonymousUser()  # type: ignore
        response = user_update_view(request, username=user.username)
        assert response.status_code == 302
        assert response.url == "/users/~login/?next=/fake-url/"


class TestPasswordResetView:
    def test_update(self, user: User, client):
        data = {"email": user.email}
        response = client.post("/users/~password_reset/", data)
        assert response.status_code == 302
        assert len(mail.outbox) == 1


class TestPasswordResetConfirmView:
    def test_update(self, user: User, client):
        data = {"email": user.email}
        client.post("/users/~password_reset/", data)
        url = re.findall(r"/users/~reset/.*", mail.outbox[0].body)[0]
        url = client.get(url).url
        response = client.post(url, {"new_password1": "1", "new_password2": "1"})
        assert response.status_code == 302
        assert response.url == "/users/~login/"


class TestUserPasswordChangeView:
    def test_change_password(self, user: User, client):
        old_password = "123"
        user.set_password(old_password)
        user.save()
        data = {
            "new_password1": "1",
            "new_password2": "1",
            "old_password": old_password,
        }
        client.force_login(user)
        response = client.post("/users/~password_change/", data)
        assert response.status_code == 302
        assert response.url == "/users/~update/"
