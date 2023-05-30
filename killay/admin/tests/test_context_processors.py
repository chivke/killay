import pytest
from unittest import mock

from django.conf import settings
from django.test import RequestFactory

from killay.admin.context_processors import site_context
from killay.admin.middleware import SiteConfigurationMiddleware

pytestmark = pytest.mark.django_db


def test_site_context(rf: RequestFactory):
    get_response = mock.Mock()
    request = rf.get("/")
    middleware = SiteConfigurationMiddleware(get_response)
    middleware(request)
    site = site_context(request)
    assert "site_conf" in site
    assert site["site_conf"].name == settings.SITE_NAME
