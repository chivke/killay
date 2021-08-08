import pytest

from cmpirque.users.models import User
from cmpirque.users.tests.factories import UserFactory, UserAdminFactory
from cmpirque.pages.models import Page
from cmpirque.pages.tests.factories import PageFactory, HomePageFactory


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

