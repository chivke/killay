import pytest

from typing import List

from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.files.uploadedfile import SimpleUploadedFile

from killay.users.models import User
from killay.users.tests.factories import UserFactory, UserAdminFactory

from killay.pages.models import Page
from killay.pages.tests.factories import PageFactory, HomePageFactory


@pytest.fixture
def rf_msg(rf):
    def _set_msg(request):
        middleware = SessionMiddleware()
        middleware.process_request(request)
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        return request

    def _set_rf(method, url, *args, **kwargs):
        return _set_msg(getattr(rf, method)(url, *args, **kwargs))

    return _set_rf


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def admin_user() -> User:
    return UserAdminFactory()


@pytest.fixture
def page() -> Page:
    return PageFactory()


@pytest.fixture
def home_page() -> Page:
    return HomePageFactory()


@pytest.fixture
def image():
    return SimpleUploadedFile("image.jpg", b"fake content", content_type="image/jpg")
