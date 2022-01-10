import pytest

from killay.users.models import User

pytestmark = pytest.mark.django_db


def test_user_str(user: User, admin_user: User):
    assert str(user) == f"{user.username}"
    assert str(admin_user) == f"{admin_user.username} (admin)"
