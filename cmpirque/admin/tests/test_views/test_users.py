import pytest

from django.test import RequestFactory
from django.urls import resolve

from cmpirque.users.models import User

from cmpirque.admin.views.users import user_create_view

pytestmark = pytest.mark.django_db


class TestPageCreateView:
    def test_create(self, admin_user: User, rf_msg: RequestFactory):
        data = {
            "username": "fake_user",
            "email": "fake@localhost",
            "password1": "1",
            "password2": "1",
        }
        request = rf_msg("post", "/admin/users/~create/", data)
        request.resolver_match = resolve("/admin/users/~create/")
        request.user = admin_user
        response = user_create_view(request)
        assert response.status_code == 302
        user = User.objects.get(username=data["username"])
        assert user.email == data["email"]
