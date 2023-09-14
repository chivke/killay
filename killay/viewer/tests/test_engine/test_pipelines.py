from unittest import mock

import pytest

from killay.archives.tests import recipes as archives_recipes
from killay.pages.tests.recipes import page_recipe
from killay.viewer.engine.pipelines import (
    ContentPipeline,
    MenuPipeline,
    RoutePipeline,
    SiteContextPipeline,
)
from killay.viewer.lib.constants import ViewerConstants, SiteContextConstants


@pytest.mark.django_db
class TestRoutePipeline:
    def test_view_is_out_of_scope(self, get_request_with_viewer):
        request = get_request_with_viewer()
        assert not RoutePipeline.view_is_out_of_scope(request=request, out_of_scope=[])

    def test_can_see_out_of_scope(self, get_request_with_viewer):
        request = get_request_with_viewer()
        request.user.is_superuser = True
        request.user.save()
        assert not RoutePipeline.view_is_out_of_scope(
            request=request, out_of_scope=[request.viewer.scope]
        )

    def test_get_root_url(self, get_request_with_viewer):
        request = get_request_with_viewer()
        root_url = RoutePipeline.get_root_url(request=request)
        assert root_url == "/viewer/archives/"

    def test_get_root_url_with_home_page(self, get_request_with_viewer):
        request = get_request_with_viewer()
        page = page_recipe.make()
        request.viewer.home = ViewerConstants.HOME_PAGE
        request.viewer.home_page_id = page.id
        request.viewer.save()
        root_url = RoutePipeline.get_root_url(request=request)
        assert root_url == f"/pages/{page.slug}/"


@pytest.mark.django_db
class TestMenuPipeline:
    def test_get_main_menu(self, get_request_with_viewer):
        archive = archives_recipes.archive_recipe.make()
        request = get_request_with_viewer()
        request.viewer.scope = ViewerConstants.SCOPE_ALL
        request.viewer.save()
        pipeline = MenuPipeline(request=request)
        main_menu = pipeline.get_main_menu()
        assert main_menu[0]["name"] == archive.name

    def test_get_main_menu_cant_access(self, get_request_with_viewer):
        request = get_request_with_viewer()
        request.site_configuration.is_published = False
        request.site_configuration.save()
        pipeline = MenuPipeline(request=request)
        main_menu = pipeline.get_main_menu()
        assert main_menu == []

    def test_get_main_menu_one_archive(self, get_request_with_viewer):
        collection = archives_recipes.collection_recipe.make()
        request = get_request_with_viewer()
        request.viewer.scope = ViewerConstants.SCOPE_ONE_ARCHIVE
        request.viewer.scope_archive_id = collection.archive.id
        request.viewer.save()
        pipeline = MenuPipeline(request=request)
        main_menu = pipeline.get_main_menu()
        assert main_menu[0]["name"] == collection.name

    def test_get_main_menu_one_collection(self, get_request_with_viewer):
        collection = archives_recipes.collection_recipe.make()
        category = archives_recipes.category_recipe.make(collection_id=collection.id)
        request = get_request_with_viewer()
        request.viewer.scope = ViewerConstants.SCOPE_ONE_COLLECTION
        request.viewer.scope_collection_id = collection.id
        request.viewer.save()
        pipeline = MenuPipeline(request=request)
        main_menu = pipeline.get_main_menu()
        assert main_menu[0]["name"] == category.name

    def test_get_submenus(self, get_request_with_viewer):
        collection = archives_recipes.collection_recipe.make()
        request = get_request_with_viewer()
        request.viewer.scope = ViewerConstants.SCOPE_ALL
        request.viewer.save()
        pipeline = MenuPipeline(request=request)
        pipeline.cursor["archive"] = collection.archive
        main_menu = pipeline.get_submenus()
        assert main_menu[0][0]["name"] == collection.name

    def test_get_submenus_cant_access(self, get_request_with_viewer):
        request = get_request_with_viewer()
        request.site_configuration.is_published = False
        request.site_configuration.save()
        pipeline = MenuPipeline(request=request)
        main_menu = pipeline.get_submenus()
        assert main_menu == []

    def test_get_submenus_one_archive(self, get_request_with_viewer):
        collection = archives_recipes.collection_recipe.make()
        category = archives_recipes.category_recipe.make(collection_id=collection.id)
        request = get_request_with_viewer()
        request.viewer.scope = ViewerConstants.SCOPE_ONE_ARCHIVE
        request.viewer.scope_archive_id = collection.archive_id
        request.viewer.save()
        pipeline = MenuPipeline(request=request)
        pipeline.cursor["archive"] = collection.archive
        pipeline.cursor["collection"] = collection
        main_menu = pipeline.get_submenus()
        assert main_menu[0][0]["name"] == category.name

    def test_get_submenus_one_collection(self, get_request_with_viewer):
        collection = archives_recipes.collection_recipe.make()
        request = get_request_with_viewer()
        request.viewer.scope = ViewerConstants.SCOPE_ONE_COLLECTION
        request.viewer.scope_collection_id = collection.id
        request.viewer.save()
        pipeline = MenuPipeline(request=request)
        pipeline.cursor["archive"] = collection.archive
        pipeline.cursor["collection"] = collection
        main_menu = pipeline.get_submenus()
        assert main_menu == []

    def test_get_user_menu(self, get_request_with_viewer):
        request = get_request_with_viewer()
        request.resolver_match = mock.Mock()
        pipeline = MenuPipeline(request=request)
        user_menu = pipeline.get_user_menu()
        assert user_menu[0]["name"] == f"@{request.user.username}"

    def test_get_user_menu_unauthenticated(self, get_request_with_viewer):
        request = get_request_with_viewer()
        request.resolver_match = mock.Mock()
        request.user = mock.Mock()
        request.user.is_authenticated = False
        pipeline = MenuPipeline(request=request)
        user_menu = pipeline.get_user_menu()
        assert user_menu[0]["name"] == SiteContextConstants.NAME_LOGIN

    def test_get_search(self, get_request_with_viewer):
        key = "search"
        value = "fake"
        request = get_request_with_viewer(f"/?{key}={value}")
        pipeline = MenuPipeline(request=request)
        search = pipeline.get_search()
        assert search["query"] == value


@pytest.mark.django_db
class TestSiteContextPipeline:
    def test_get_site_context(self, get_request_with_viewer):
        request = get_request_with_viewer()
        request.resolver_match = mock.Mock()
        pipeline = SiteContextPipeline(request=request)
        site_context = pipeline.get_site_context()
        assert "title" in site_context
        assert "root_url" in site_context
        assert "user_menu" in site_context
        assert "main_menu" in site_context
        assert "submenus" in site_context
        assert "menu_search" in site_context
        assert "in_root_url" in site_context

    def test_get_site_title(self, get_request_with_viewer):
        request = get_request_with_viewer()
        pipeline = SiteContextPipeline(request=request)
        site_title = pipeline.get_site_title()
        assert site_title == request.site_configuration.name

    def test_get_site_title_on_archive(self, get_request_with_viewer):
        archive = archives_recipes.archive_recipe.make()
        request = get_request_with_viewer()
        request.viewer.scope = ViewerConstants.SCOPE_ONE_ARCHIVE
        request.viewer.scope_archive_id = archive.id
        request.viewer.save()
        pipeline = SiteContextPipeline(request=request)
        site_title = pipeline.get_site_title()
        assert site_title == archive.name

    def test_get_site_title_on_collection(self, get_request_with_viewer):
        collection = archives_recipes.collection_recipe.make()
        request = get_request_with_viewer()
        request.viewer.scope = ViewerConstants.SCOPE_ONE_COLLECTION
        request.viewer.scope_collection_id = collection.id
        request.viewer.save()
        pipeline = SiteContextPipeline(request=request)
        site_title = pipeline.get_site_title()
        assert site_title == collection.name


@pytest.mark.django_db
class TestContentPipeline:
    def test_get_archives(self, get_request_with_viewer):
        collection = archives_recipes.collection_recipe.make()
        request = get_request_with_viewer()
        pipeline = ContentPipeline(request=request)
        archives = pipeline.get_archives()
        assert archives[0]["slug"] == collection.archive.slug

    def test_get_archive_by_slug(self, get_request_with_viewer):
        collection = archives_recipes.collection_recipe.make()
        request = get_request_with_viewer()
        request.resolver_match = mock.Mock()
        request.resolver_match.kwargs = {"slug": collection.archive.slug}
        pipeline = ContentPipeline(request=request)
        returned_archive = pipeline.get_archive_by_slug()
        assert returned_archive["id"] == collection.archive_id

    def test_get_archive(self, get_request_with_viewer):
        collection = archives_recipes.collection_recipe.make()
        request = get_request_with_viewer(f"/?archive={collection.archive.slug}")
        pipeline = ContentPipeline(request=request)
        instance = pipeline.get_archive()
        assert instance.id == collection.archive_id

    def test_get_archive_with_category(self, get_request_with_viewer):
        request = get_request_with_viewer()
        collection = archives_recipes.collection_recipe.make()
        category = archives_recipes.category_recipe.make(collection_id=collection.id)
        pipeline = ContentPipeline(request=request)
        instance = pipeline.get_archive(category=category)
        assert instance.id == category.collection.archive_id

    def test_get_archive_with_collection(self, get_request_with_viewer):
        request = get_request_with_viewer()
        collection = archives_recipes.collection_recipe.make()
        pipeline = ContentPipeline(request=request)
        instance = pipeline.get_archive(collection=collection)
        assert instance.id == collection.archive_id

    def test_get_archive_with_one_archive(self, get_request_with_viewer):
        request = get_request_with_viewer()
        collection = archives_recipes.collection_recipe.make()
        request.viewer.scope = ViewerConstants.SCOPE_ONE_ARCHIVE
        request.viewer.scope_archive_id = collection.archive_id
        request.viewer.save()
        pipeline = ContentPipeline(request=request)
        instance = pipeline.get_archive()
        assert instance.id == collection.archive_id

    def test_get_archive_with_one_collection(self, get_request_with_viewer):
        request = get_request_with_viewer()
        collection = archives_recipes.collection_recipe.make()
        request.viewer.scope = ViewerConstants.SCOPE_ONE_COLLECTION
        request.viewer.scope_collection_id = collection.id
        request.viewer.save()
        pipeline = ContentPipeline(request=request)
        instance = pipeline.get_archive()
        assert instance.id == collection.archive_id

    def test_get_collections_by_archive_id(self, get_request_with_viewer):
        request = get_request_with_viewer()
        collection = archives_recipes.collection_recipe.make()
        pipeline = ContentPipeline(request=request)
        collections = pipeline.get_collections_by_archive_id(
            archive_id=collection.archive_id
        )
        assert collections[0].id == collection.id

    def test_get_collection(self, get_request_with_viewer):
        collection = archives_recipes.collection_recipe.make()
        request = get_request_with_viewer(f"/?collection={collection.slug}")
        pipeline = ContentPipeline(request=request)
        returned_collection = pipeline.get_collection(archive_id=collection.archive_id)
        assert returned_collection.id == collection.id

    def test_get_collection_with_one_collection(self, get_request_with_viewer):
        collection = archives_recipes.collection_recipe.make()
        request = get_request_with_viewer(f"/?collection={collection.slug}")
        request.viewer.scope = ViewerConstants.SCOPE_ONE_COLLECTION
        request.viewer.scope_collection_id = collection.id
        request.viewer.save()
        pipeline = ContentPipeline(request=request)
        returned_collection = pipeline.get_collection(archive_id=collection.archive_id)
        assert returned_collection.id == collection.id

    def test_get_category(self, get_request_with_viewer):
        collection = archives_recipes.collection_recipe.make()
        category = archives_recipes.category_recipe.make(collection_id=collection.id)
        request = get_request_with_viewer(f"/?category={category.slug}")
        pipeline = ContentPipeline(request=request)
        returned_category = pipeline.get_category(collection_id=collection.id)
        assert returned_category.id == category.id
        # cache
        returned_category = pipeline.get_category(collection_id=collection.id)
        assert returned_category.id == category.id

    def test_get_person(self, get_request_with_viewer):
        person = archives_recipes.person_recipe.make()
        request = get_request_with_viewer(f"/?person={person.slug}")
        pipeline = ContentPipeline(request=request)
        returned_person = pipeline.get_person()
        assert returned_person.id == person.id
        # cache
        returned_person = pipeline.get_person()
        assert returned_person.id == person.id

    def test_get_keyword(self, get_request_with_viewer):
        keyword = archives_recipes.keyword_recipe.make()
        request = get_request_with_viewer(f"/?keyword={keyword.slug}")
        pipeline = ContentPipeline(request=request)
        returned_keyword = pipeline.get_keyword()
        assert returned_keyword.id == keyword.id
        # cache
        returned_keyword = pipeline.get_keyword()
        assert returned_keyword.id == keyword.id

    def test_get_query_search(self, get_request_with_viewer):
        query_search = "query"
        request = get_request_with_viewer(f"/?search={query_search}")
        pipeline = ContentPipeline(request=request)
        assert query_search == pipeline.get_query_search()

    def test_get_kind(self, get_request_with_viewer):
        fake_kind = "fake_kind"
        request = get_request_with_viewer(f"/?kind={fake_kind}")
        pipeline = ContentPipeline(request=request)
        assert fake_kind == pipeline.get_kind()

    def test_get_pieces(self, get_request_with_viewer):
        piece = archives_recipes.piece_recipe.make()
        request = get_request_with_viewer()
        pipeline = ContentPipeline(request=request)
        returned_pieces = pipeline.get_pieces()
        assert returned_pieces[0].id == piece.id

    def test_get_piece(self, get_request_with_viewer):
        piece = archives_recipes.piece_recipe.make()
        request = get_request_with_viewer()
        pipeline = ContentPipeline(request=request)
        returned_piece = pipeline.get_piece(piece_code=piece.code)
        assert returned_piece["id"] == piece.id

    def test_get_kind_options(self, get_request_with_viewer):
        request = get_request_with_viewer()
        pipeline = ContentPipeline(request=request)
        kind_options = pipeline.get_kind_options()
        assert len(kind_options["items"]) == 4

    def test_get_filter_options(self, get_request_with_viewer):
        collection = archives_recipes.collection_recipe.make()
        category = archives_recipes.category_recipe.make(collection_id=collection.id)
        person = archives_recipes.person_recipe.make()
        keyword = archives_recipes.keyword_recipe.make()
        request = get_request_with_viewer()
        pipeline = ContentPipeline(request=request)
        filter_options = pipeline.get_filter_options()
        assert "archive" in filter_options
        assert filter_options["archive"]["items"][0]["slug"] == collection.archive.slug
        assert "collection" in filter_options
        assert filter_options["collection"]["items"][0]["slug"] == collection.slug
        assert "category" in filter_options
        assert filter_options["category"]["items"][0]["slug"] == category.slug
        assert (
            filter_options["category"]["items"][0]["collection_slug"]
            == category.collection.slug
        )
        assert "person" in filter_options
        assert filter_options["person"]["items"][0]["slug"] == person.slug
        assert "keyword" in filter_options
        assert filter_options["keyword"]["items"][0]["slug"] == keyword.slug
