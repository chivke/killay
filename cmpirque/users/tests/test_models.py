import pytest

from cmpirque.users.models import User

pytestmark = pytest.mark.django_db


def test_user_str(user: User, admin_user: User):
    assert str(user) == f"{user.username}"
    assert str(admin_user) == f"{admin_user.username} (admin)"


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f'/users/{user.username}/'