import pytest
from django.urls import resolve, reverse

from cmpirque.pages.models import Page

pytestmark = pytest.mark.django_db


def test_detail(page: Page):
    assert (
        reverse('pages:detail', kwargs={'slug': page.slug})
        == f'/pages/{page.slug}/'
    )
    assert resolve(f'/pages/{page.slug}/').view_name == 'pages:detail'
