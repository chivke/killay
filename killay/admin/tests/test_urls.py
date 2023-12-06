import pytest
from django.urls import resolve, reverse


pytestmark = pytest.mark.django_db


def test_configuration():
    assert reverse("admin:site_configuration") == "/admin/conf/"
    assert resolve("/admin/").view_name == "admin:main"
