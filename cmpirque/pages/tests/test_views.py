import pytest
from django.http.response import Http404
from django.test import RequestFactory

from cmpirque.pages.models import Page
from cmpirque.pages.views import (
    home_page_view,
    page_detail_view,
)

pytestmark = pytest.mark.django_db


class TestPageDetailView:
    def test_get_page(self, page: Page, rf: RequestFactory):
        request = rf.get('/fake-url')
        response = page_detail_view(request, slug=page.slug)
        assert response.status_code == 200
        assert response.render()
        assert page.title in str(response.content)

    def test_not_found(self, rf: RequestFactory):
        request = rf.get('/fake-url')
        with pytest.raises(Http404):
            page_detail_view(request, slug="wrong-slug")


class TestHomeView:
    def test_get_with_home_page(
        self, home_page: Page, rf: RequestFactory
    ):
        request = rf.get('/fake-url')
        response = home_page_view(request)
        assert response.render()
        assert home_page.title in str(response.content)

    def test_get_without_home_page(
        self, rf: RequestFactory
    ):
        request = rf.get('/fake-url')
        response = home_page_view(request)
        assert response.render()
