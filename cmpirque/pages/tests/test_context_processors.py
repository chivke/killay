import pytest
from django.test import RequestFactory
from django.conf import settings

from cmpirque.pages.models import Page
from cmpirque.pages.context_processors import (
    pages_context,
    site_context,
)

pytestmark = pytest.mark.django_db


class TestPagesContext:
    def test_with_normal_page(
        self, page: Page, home_page: Page, rf: RequestFactory
    ):
        request = rf.get(f"/pages/{page.slug}/")
        menu_pages = pages_context(request)["menu_pages"]

        for menu_page in menu_pages:
            if menu_page["selected"] is True:
                assert menu_page["title"] == page.title
                assert menu_page["slug"] == page.slug
                assert menu_page["url"] == page.get_absolute_url()
            else:
                assert menu_page["title"] == home_page.title
                assert menu_page["slug"] == home_page.slug
                assert menu_page["url"] == home_page.get_absolute_url()
                assert menu_page["selected"] is False

    def test_with_home_page(
        self, page: Page, home_page: Page, rf: RequestFactory
    ):
        request = rf.get("/")
        menu_pages = pages_context(request)["menu_pages"]

        for menu_page in menu_pages:
            if menu_page["selected"] is True:
                assert menu_page["title"] == home_page.title
                assert menu_page["slug"] == home_page.slug
                assert menu_page["url"] == home_page.get_absolute_url()
            else:
                assert menu_page["title"] == page.title
                assert menu_page["slug"] == page.slug
                assert menu_page["url"] == page.get_absolute_url()
                assert menu_page["selected"] is False


def test_site_context(rf: RequestFactory):
    request = rf.get('/')
    site = site_context(request)
    assert "site_name" in site
    assert site["site_name"] == settings.SITE_NAME
