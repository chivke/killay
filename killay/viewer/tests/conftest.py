from unittest import mock

from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware

import pytest

from killay.admin.middleware import SiteConfigurationMiddleware
from killay.admin.services import get_site_configuration


@pytest.fixture
def get_request_with_viewer(rf, user):
    def _get_request(path=None, ipv4=None, is_superuser=False, *args, **kwargs):
        if is_superuser:
            user.is_superuser = True
            user.save()
        path = path or "/"
        get_response = mock.Mock()
        request = rf.get(path, *args, **kwargs)
        middleware = SessionMiddleware(get_response)
        middleware.process_request(request)
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        middleware = SiteConfigurationMiddleware(get_response)
        request.user = user
        ipv4 = ipv4 or "127.0.0.1"
        request.META["REMOTE_ADDR"] = ipv4
        middleware(request=request)
        return request

    return _get_request


@pytest.fixture
def site_configuration():
    return get_site_configuration()
