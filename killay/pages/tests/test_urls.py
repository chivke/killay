import pytest
from django.urls import resolve, reverse

from killay.pages.models import Page

pytestmark = pytest.mark.django_db


def test_detail(page: Page):
    assert reverse("pages:detail", kwargs={"slug": page.slug}) == f"/pages/{page.slug}/"
    assert resolve(f"/pages/{page.slug}/").view_name == "pages:detail"


def test_home():
    assert reverse("home") == "/"
    assert resolve("/").view_name == "home"
