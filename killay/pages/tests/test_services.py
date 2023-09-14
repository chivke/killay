import pytest

from killay.archives.tests import recipes as archives_recipes
from killay.pages.tests.recipes import page_recipe
from killay.pages import services as page_services


@pytest.mark.django_db
def test_get_public_menu_pages():
    page = page_recipe.make(
        archive_id=None,
        collection_id=None,
        is_visible_in_navbar=True,
    )
    result = page_services.get_public_menu_pages()
    assert result[0].id == page.id


@pytest.mark.django_db
def test_get_public_archive_menu_pages():
    archive = archives_recipes.archive_recipe.make()
    page = page_recipe.make(
        archive_id=archive.id,
        is_visible_in_navbar=True,
    )
    result = page_services.get_public_archive_menu_pages(archive_id=archive.id)
    assert result[0].id == page.id


@pytest.mark.django_db
def test_get_public_collection_menu_pages():
    collection = archives_recipes.collection_recipe.make()
    page = page_recipe.make(
        collection_id=collection.id,
        is_visible_in_navbar=True,
    )
    result = page_services.get_public_collection_menu_pages(
        collection_id=collection.id,
    )
    assert result[0].id == page.id
