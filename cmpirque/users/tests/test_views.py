import pytest
from django.contrib.auth.models import AnonymousUser
from django.http.response import Http404
from django.test import RequestFactory

from cmpirque.users.models import User
from cmpirque.users.tests.factories import UserFactory
from cmpirque.users.views import UserRedirectView, UserUpdateView, user_update_view

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
