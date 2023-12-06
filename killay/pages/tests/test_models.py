import pytest

from killay.pages.models import Page


pytestmark = pytest.mark.django_db


def test_page_str(page: Page):
    assert str(page) == f"{page.title} <{page.slug}>"


def test_page_get_absolute_url(page: Page):
    assert page.get_absolute_url() == f"/pages/{page.slug}/"
