import pytest

from django.test import RequestFactory
from django.urls import resolve

from killay.pages.models import Page
from killay.users.models import User

from killay.admin.views.pages import page_create_view

pytestmark = pytest.mark.django_db


class TestPageCreateView:
    def test_create(self, admin_user: User, rf_msg: RequestFactory):
        data = {"title": "fake page", "slug": "fake-page"}
        request = rf_msg("post", "/admin/pages/~create/", data)
        request.resolver_match = resolve("/admin/pages/~create/")
        request.user = admin_user
        response = page_create_view(request)
        assert response.status_code == 302
        page = Page.objects.get(slug=data["slug"])
        assert page.title == data["title"]
