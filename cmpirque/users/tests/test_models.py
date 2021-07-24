import pytest

from cmpirque.users.models import User, Profile

pytestmark = pytest.mark.django_db


def test_user_str(user: User):
    assert str(user) == str(user.profile)
    other = User(username='usertest')
    assert str(other) == other.username


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f'/users/{user.username}/'


def test_user_create_profile(user: User):
    assert isinstance(user.create_profile(), Profile)


def test_usermanager_create():
    user = User.objects.create()
    assert isinstance(user, User)
    assert isinstance(user.profile, Profile)


def test_usermanager_get_or_create():
    user, created = User.objects.get_or_create()
    assert isinstance(user, User)
    assert isinstance(user.profile, Profile)


def test_profile_str(user: User):
    assert str(user.profile) == f'{user.username} <{user.profile.role}>'


def test_profile_is_nora(user: User):
    assert not user.profile.is_nora
