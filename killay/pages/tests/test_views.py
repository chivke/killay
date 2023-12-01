import pytest
from django.http.response import Http404
from django.test import RequestFactory, Client

from killay.pages.models import Page
from killay.pages.views import page_detail_view

pytestmark = pytest.mark.django_db


class TestPageDetailView:
    def test_get_page(self, page: Page, client: Client):
        response = client.get(f"/pages/{page.slug}/")
        assert response.status_code == 200
        assert response.render()
        assert page.title in str(response.content)

    def test_not_found(self, rf: RequestFactory):
        request = rf.get("/pages/X")
        with pytest.raises(Http404):
            page_detail_view(request, slug="wrong-slug")
