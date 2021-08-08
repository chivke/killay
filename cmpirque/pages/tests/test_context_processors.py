import pytest
from django.test import RequestFactory
from django.conf import settings

from cmpirque.pages.models import Page
from cmpirque.pages.context_processors import (
    pages_context,
    site_context,
)

pytestmark = pytest.mark.django_db


def test_pages_context(page: Page, rf: RequestFactory):
    request = rf.get('/')
    pages = pages_context(request)["menu_pages"]
    assert pages and len(pages) == 1
    assert pages[0]["title"] == page.title


def test_site_context(rf: RequestFactory):
    request = rf.get('/')
    site = site_context(request)
    assert "site_name" in site
    assert site["site_name"] == settings.SITE_NAME
