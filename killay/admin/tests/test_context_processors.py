import pytest

from django.conf import settings
from django.test import RequestFactory

from killay.admin.context_processors import site_context

pytestmark = pytest.mark.django_db


def test_site_context(rf: RequestFactory):
    request = rf.get("/")
    site = site_context(request)
    assert "site_conf" in site
    assert site["site_conf"].name == settings.SITE_NAME
