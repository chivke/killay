import pytest

from killay.archives.tests import recipes as archives_recipes
from killay.pages.tests.recipes import page_recipe
from killay.viewer.engine.menu import MenuBase
from killay.viewer.engine.pipelines import MenuPipeline
from killay.viewer.lib.constants import ViewerConstants


@pytest.mark.django_db
class TestMenuBase:
    def test_get_initial_main_menu(self, get_request_with_viewer):
        page = page_recipe.make(
            is_visible_in_navbar=True,
        )
        request = get_request_with_viewer()
        pipeline = MenuBase(request=request)
        initial_main_menu = pipeline._get_initial_main_menu()
        assert initial_main_menu[0]["name"] == page.title

    def test_get_archive_links(self, get_request_with_viewer):
        archive = archives_recipes.archive_recipe.make()
        request = get_request_with_viewer()
        pipeline = MenuBase(request=request)
        archive_links = pipeline._get_archive_links(archives=[archive])
        assert archive_links[0]["name"] == archive.name

    def test_get_collection_links(self, get_request_with_viewer):
        collection = archives_recipes.collection_recipe.make()
        request = get_request_with_viewer()
        pipeline = MenuBase(request=request)
        collection_links = pipeline._get_collection_links(collections=[collection])
        assert collection_links[0]["name"] == collection.name

    def test_get_category_links(self, get_request_with_viewer):
        category = archives_recipes.category_recipe.make()
        request = get_request_with_viewer()
        pipeline = MenuBase(request=request)
        category_links = pipeline._get_category_links(categories=[category])
        assert category_links[0]["name"] == category.name

    def test_get_archive_page_links(self, get_request_with_viewer):
        archive = archives_recipes.archive_recipe.make()
        page = page_recipe.make(is_visible_in_navbar=True, archive_id=archive.id)
        request = get_request_with_viewer()
        pipeline = MenuBase(request=request)
        page_links = pipeline._get_archive_page_links(archive_id=archive.id)
        assert page_links[0]["name"] == page.title

    def test_get_collection_page_links(self, get_request_with_viewer):
        collection = archives_recipes.collection_recipe.make()
        page = page_recipe.make(is_visible_in_navbar=True, collection_id=collection.id)
        request = get_request_with_viewer()
        pipeline = MenuBase(request=request)
        page_links = pipeline._get_collection_page_links(collection_id=collection.id)
        assert page_links[0]["name"] == page.title


@pytest.mark.django_db
class TestMenuOneArchiveBase:
    def get_request(self, get_request_with_viewer):
        collection = archives_recipes.collection_recipe.make()
        archive = collection.archive
        request = get_request_with_viewer()
        request.viewer.scope = ViewerConstants.SCOPE_ONE_ARCHIVE
        request.viewer.scope_archive_id = archive.id
        request.viewer.save()
        return request

    def test_get_one_archive_main_menu(self, get_request_with_viewer):
        request = self.get_request(get_request_with_viewer)
        collection = request.viewer.scope_archive.collections.first()
        pipeline = MenuPipeline(request=request)
        main_menu = pipeline._get_one_archive_main_menu()
        assert main_menu[0]["name"] == collection.name

    def test_get_one_archive_submenus(self, get_request_with_viewer):
        request = self.get_request(get_request_with_viewer)
        collection = request.viewer.scope_archive.collections.first()
        category = archives_recipes.category_recipe.make(collection_id=collection.id)
        pipeline = MenuPipeline(request=request)
        pipeline.cursor["collection"] = collection
        submenus = pipeline._get_one_archive_submenus()
        assert submenus[0][0]["name"] == category.name


@pytest.mark.django_db
class TestMenuOneCollectionBase:
    def get_request(self, get_request_with_viewer):
        collection = archives_recipes.collection_recipe.make()
        request = get_request_with_viewer()
        request.viewer.scope = ViewerConstants.SCOPE_ONE_COLLECTION
        request.viewer.scope_collection_id = collection.id
        request.viewer.save()
        return request

    def test_get_one_collection_main_menu(self, get_request_with_viewer):
        request = self.get_request(get_request_with_viewer)
        collection = request.viewer.scope_collection
        category = archives_recipes.category_recipe.make(collection_id=collection.id)
        pipeline = MenuPipeline(request=request)
        main_menu = pipeline._get_one_collection_main_menu()
        assert main_menu[0]["name"] == category.name


@pytest.mark.django_db
class TestMenuAllBase:
    def get_request(self, get_request_with_viewer):
        request = get_request_with_viewer()
        request.viewer.scope = ViewerConstants.SCOPE_ALL
        request.viewer.save()
        return request

    def test_get_all_main_menu(self, get_request_with_viewer):
        collection = archives_recipes.collection_recipe.make()
        archive = collection.archive
        request = self.get_request(get_request_with_viewer)
        pipeline = MenuPipeline(request=request)
        main_menu = pipeline._get_all_main_menu()
        assert main_menu[0]["name"] == archive.name

    def test_get_all_submenus(self, get_request_with_viewer):
        collection = archives_recipes.collection_recipe.make()
        category = archives_recipes.category_recipe.make(collection_id=collection.id)
        request = self.get_request(get_request_with_viewer)
        pipeline = MenuPipeline(request=request)
        pipeline.cursor = {
            "archive": collection.archive,
            "collection": collection,
        }
        submenus = pipeline._get_all_submenus()
        assert submenus[0][0]["name"] == collection.name
        assert submenus[1][0]["name"] == category.name
