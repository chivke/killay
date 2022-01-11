import pytest

from killay.pages.models import Page


pytestmark = pytest.mark.django_db


def test_page_str(page: Page):
    assert str(page) == f"{page.title} <{page.slug}>"


def test_page_get_absoolute_url(page: Page, home_page: Page):
    assert page.get_absolute_url() == f"/pages/{page.slug}/"
    assert home_page.get_absolute_url() == "/"