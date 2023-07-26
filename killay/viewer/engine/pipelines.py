from typing import Dict, List, Optional

from django.contrib import messages
from django.http import HttpRequest
from django.urls import reverse

from killay.archives.lib.constants import PieceConstants
from killay.archives.services import (
    get_archive_filter_options,
    get_collection_filter_options,
    get_category_filter_options,
    get_person_filter_options,
    get_keyword_filter_options,
    get_category_by_slug,
    get_keyword_by_slug,
    get_person_by_slug,
    get_public_archives,
    get_public_archive_by_slug,
    get_public_collection_by_slug,
    get_public_collections_by_archive_id,
    get_public_piece,
    get_public_pieces,
)
from killay.viewer.engine.base import PipelineBase
from killay.viewer.engine.content import ContentSerializer
from killay.viewer.engine.menu import (
    MenuBase,
    MenuOneArchiveBase,
    MenuOneCollectionBase,
    MenuAllBase,
)
from killay.viewer.lib.constants import (
    SiteContextConstants,
    ViewerConstants,
    ViewerMessageConstants,
    ViewerPatternConstants,
)


class RoutePipeline:
    @classmethod
    def view_is_out_of_scope(
        cls, request: HttpRequest, out_of_scope: Optional[list] = None
    ) -> bool:
        out_of_scope = out_of_scope or []
        viewer = request.viewer
        is_out_of_scope = viewer.scope in out_of_scope
        if is_out_of_scope and cls._can_see_out_of_scope(user=request.user):
            message = ViewerMessageConstants.VIEW_OUT_OF_SCOPE.format(
                scope=viewer.scope
            )
            messages.warning(request, message)
            return False
        return viewer.scope in out_of_scope

    @staticmethod
    def _can_see_out_of_scope(user: "User") -> bool:
        return user and user.is_superuser

    @staticmethod
    def get_root_url(request: HttpRequest) -> str:
        url_kwargs = {}
        viewer = request.viewer
        if viewer.home == ViewerConstants.HOME_DEFAULT:
            app_name = ViewerPatternConstants.APP_NAME
            pattern = ViewerPatternConstants.HOME_BY_SCOPE[viewer.scope]
            if viewer.scope == ViewerConstants.SCOPE_ONE_ARCHIVE:
                url_kwargs["slug"] = viewer.scope_archive.slug
        elif viewer.home == ViewerConstants.HOME_PAGE:
            app_name = "pages"
            pattern = "detail"
            url_kwargs["slug"] = viewer.home_page.slug
        return reverse(f"{app_name}:{pattern}", kwargs=url_kwargs)


class MenuPipeline(
    MenuBase,
    MenuOneArchiveBase,
    MenuOneCollectionBase,
    MenuAllBase,
):
    def get_main_menu(self) -> List[Dict]:
        if not self._can_access():
            return []
        elif self.viewer.scope == ViewerConstants.SCOPE_ONE_ARCHIVE:
            return self._get_one_archive_main_menu()
        elif self.viewer.scope == ViewerConstants.SCOPE_ONE_COLLECTION:
            return self._get_one_collection_main_menu()
        elif self.viewer.scope == ViewerConstants.SCOPE_ALL:
            return self._get_all_main_menu()

    def get_submenus(self) -> List[List[Dict]]:
        if not self._can_access():
            return []
        elif self.viewer.scope == ViewerConstants.SCOPE_ONE_ARCHIVE:
            return self._get_one_archive_submenus()
        elif self.viewer.scope == ViewerConstants.SCOPE_ONE_COLLECTION:
            return self._get_one_collection_submenus()
        elif self.viewer.scope == ViewerConstants.SCOPE_ALL:
            return self._get_all_submenus()

    def get_user_menu(self) -> List:
        menu_list = []
        view_name = self.request.resolver_match.view_name
        if self.user.is_authenticated:
            user_update_pattern = "users:update"
            update_user = {"name": f"@{self.user.username}"}
            if view_name != user_update_pattern:
                update_user["link"] = reverse(SiteContextConstants.PATTERN_USER_UPDATE)
            menu_list.append(update_user)
            logout = {
                "name": SiteContextConstants.NAME_LOGOUT,
                "link": reverse(SiteContextConstants.PATTERN_LOGOUT),
            }
            menu_list.append(logout)
        else:
            login = {
                "name": SiteContextConstants.NAME_LOGIN,
                "link": reverse(SiteContextConstants.PATTERN_LOGIN),
            }
            menu_list.append(login)
        return menu_list

    def get_search(self) -> Dict:
        query_search = self._get_url_param(key=ViewerConstants.KEY_SEARCH)
        base_url = self._get_piece_list_base_url()
        return {
            "query": query_search,
            "url": base_url,
            "key": ViewerConstants.KEY_SEARCH,
            "placeholder": ViewerMessageConstants.SEARCH_ACTION_NAME,
        }


class SiteContextPipeline:
    def __init__(self, request: HttpRequest):
        menu_cursor = getattr(request, "menu_cursor", {})
        self.menu_pipeline = MenuPipeline(request=request, cursor=menu_cursor)
        self.request = request

    def get_site_context(self) -> Dict:
        site_title = self.get_site_title()
        root_url = RoutePipeline.get_root_url(request=self.request)
        user_menu = self.menu_pipeline.get_user_menu()
        main_menu = self.menu_pipeline.get_main_menu()
        submenus = self.menu_pipeline.get_submenus()
        menu_search = self.menu_pipeline.get_search()
        return {
            "title": site_title,
            "root_url": root_url,
            "user_menu": user_menu,
            "main_menu": main_menu,
            "submenus": submenus,
            "menu_search": menu_search,
            "in_root_url": self.request.path == root_url,
        }

    def get_site_title(self) -> str:
        viewer = self.request.viewer
        if viewer.scope == ViewerConstants.SCOPE_ONE_ARCHIVE:
            site_title = viewer.scope_archive.name
        elif viewer.scope == ViewerConstants.SCOPE_ONE_COLLECTION:
            site_title = viewer.scope_collection.name
        else:
            site_title = self.request.site_configuration.name
        return site_title


class ContentPipeline(ContentSerializer, PipelineBase):
    def init_prepare(self):
        self._archives = None
        self._archive_by_slug = None
        self._category = None
        self._person = None
        self._keyword = None

    def get_archives(self):
        assert self.viewer.scope == ViewerConstants.SCOPE_ALL
        if self._archives:
            return self._serialize_archives(archives=self._archives)
        self._archives = get_public_archives(
            place=self.place,
            is_superuser=self.user.is_superuser,
        )
        return self._serialize_archives(archives=self._archives)

    def get_archive_by_slug(self):
        assert self.viewer.scope != ViewerConstants.SCOPE_ONE_COLLECTION
        if self._archive_by_slug:
            return self._serialize_archive(archive=self._archive_by_slug)
        slug = self.request.resolver_match.kwargs.get("slug")
        self._archive_by_slug = get_public_archive_by_slug(
            slug=slug,
            place=self.place,
            is_superuser=self.user.is_superuser,
        )
        return self._serialize_archive(archive=self._archive_by_slug)

    def get_archive(
        self,
        collection=None,
        category=None,
    ):
        if category and category.collection_id:
            collection = category.collection
        if collection:
            return collection.archive
        scope = self.viewer.scope
        if scope == ViewerConstants.SCOPE_ONE_ARCHIVE:
            return self.viewer.scope_archive
        elif scope == ViewerConstants.SCOPE_ONE_COLLECTION:
            return self.viewer.scope_collection.archive

        archive_slug = self._get_url_param(key=ViewerConstants.KEY_ARCHIVE)
        if archive_slug:
            return get_public_archive_by_slug(
                slug=archive_slug,
                place=self.place,
                is_superuser=self.user.is_superuser,
            )

    def get_collections_by_archive_id(self, archive_id: int):
        assert self.viewer.scope != ViewerConstants.SCOPE_ONE_COLLECTION
        return get_public_collections_by_archive_id(
            archive_id=archive_id,
            place=self.place,
            is_superuser=self.user.is_superuser,
        )

    def get_collection(self, archive_id: Optional[int] = None):
        scope = self.viewer.scope
        if scope == ViewerConstants.SCOPE_ONE_COLLECTION:
            return self.viewer.scope_collection
        collection_slug = self._get_url_param(key=ViewerConstants.KEY_COLLECTION)
        if collection_slug:
            return get_public_collection_by_slug(
                slug=collection_slug,
                place=self.place,
                is_superuser=self.user.is_superuser,
                archive_id=archive_id,
            )

    def get_category(self, collection_id: int) -> Optional["Category"]:
        if self._category:
            return self._category
        category_slug = self._get_url_param(key=ViewerConstants.KEY_CATEGORY)
        if category_slug:
            self._category = get_category_by_slug(
                slug=category_slug, collection_id=collection_id
            )
            return self._category

    def get_person(self) -> Optional["Person"]:
        if self._person:
            return self._person
        person_slug = self._get_url_param(key=ViewerConstants.KEY_PERSON)
        if person_slug:
            self._person = get_person_by_slug(slug=person_slug)
            return self._person

    def get_keyword(self) -> Optional["Keyword"]:
        if self._keyword:
            return self._keyword
        keyword_slug = self._get_url_param(key=ViewerConstants.KEY_KEYWORD)
        if keyword_slug:
            self._keyword = get_keyword_by_slug(slug=keyword_slug)
            return self._keyword

    def get_query_search(self) -> Optional[str]:
        return self._get_url_param(key=ViewerConstants.KEY_SEARCH)

    def get_kind(self) -> Optional[str]:
        return self._get_url_param(key=ViewerConstants.KEY_KIND)

    def get_pieces(
        self,
        archive=None,
        collection=None,
        category=None,
    ):
        if category:
            collection = category.collection
            archive = collection.archive
        archive = archive or self.get_archive(collection=collection)
        collection = collection or self.get_collection(
            archive_id=archive.id if archive else None
        )
        person = self.get_person()
        keyword = self.get_keyword()
        kind = self.get_kind()
        query_search = self.get_query_search()
        categorization = {
            "category": category,
            "person": person,
            "keyword": keyword,
        }
        return get_public_pieces(
            archive=archive,
            collection=collection,
            categorization=categorization,
            place=self.place,
            is_superuser=self.user.is_superuser,
            query_search=query_search,
            kind=kind,
        )

    def get_kind_options(self) -> Dict:
        kind = self.get_kind()

        items = [
            {
                "label": label,
                "value": value,
                "active": kind == value,
            }
            for value, label in PieceConstants.KIND_CHOICES
        ]
        return {
            "label": ViewerMessageConstants.LABEL_KIND,
            "items": items,
            "field": ViewerConstants.KEY_KIND,
        }

    def get_filter_options(self, archive=None, collection=None, category=None):
        if category:
            collection = category.collection
            archive = collection.archive
        archive = archive or self.get_archive(collection=collection)
        collection = collection or self.get_collection(
            archive_id=archive.id if archive else None
        )
        filter_options = {}
        if self.viewer.scope == ViewerConstants.SCOPE_ALL:
            active_archive_id = archive.id if archive else None
            archive_options = get_archive_filter_options(
                place=self.place,
                is_superuser=self.user.is_superuser,
                active_archive_id=active_archive_id,
            )
            label = ViewerMessageConstants.LABEL_ARCHIVES
            filter_options[ViewerConstants.KEY_ARCHIVE] = {
                "items": archive_options,
                "label": label,
            }
        archive_id = (
            archive.id
            if self.viewer.scope == ViewerConstants.SCOPE_ONE_ARCHIVE
            else None
        )
        if self.viewer.scope in [
            ViewerConstants.SCOPE_ALL,
            ViewerConstants.SCOPE_ONE_ARCHIVE,
        ]:
            active_collection_id = collection.id if collection else None
            collection_options = get_collection_filter_options(
                place=self.place,
                is_superuser=self.user.is_superuser,
                active_collection_id=active_collection_id,
                archive_id=archive_id,
            )
            label = ViewerMessageConstants.LABEL_COLLECTIONS
            filter_options[ViewerConstants.KEY_COLLECTION] = {
                "items": collection_options,
                "label": label,
            }
        active_category_id = category.id if category else None
        collection_id = (
            collection.id
            if self.viewer.scope == ViewerConstants.SCOPE_ONE_COLLECTION
            else None
        )
        category_options = get_category_filter_options(
            place=self.place,
            is_superuser=self.user.is_superuser,
            active_category_id=active_category_id,
            collection_id=collection_id,
            archive_id=archive_id,
        )
        filter_options[ViewerConstants.KEY_CATEGORY] = {
            "items": category_options,
            "label": ViewerMessageConstants.LABEL_CATEGORIES,
        }

        person = self.get_person()
        active_person_id = person.id if person else None
        person_options = get_person_filter_options(
            place=self.place,
            is_superuser=self.user.is_superuser,
            active_person_id=active_person_id,
        )
        filter_options[ViewerConstants.KEY_PERSON] = {
            "items": person_options,
            "label": ViewerMessageConstants.LABEL_PEOPLE,
        }

        keyword = self.get_keyword()
        active_keyword_id = keyword.id if keyword else None
        keyword_options = get_keyword_filter_options(
            place=self.place,
            is_superuser=self.user.is_superuser,
            active_keyword_id=active_keyword_id,
        )
        filter_options[ViewerConstants.KEY_KEYWORD] = {
            "items": keyword_options,
            "label": ViewerMessageConstants.LABEL_KEYWORDS,
        }

        return filter_options

    def get_piece(self, piece_code: str) -> Optional[Dict]:
        piece = get_public_piece(
            piece_code=piece_code,
            place=self.place,
            is_superuser=self.user.is_superuser,
        )
        if not piece:
            return
        piece_data = piece.__dict__
        piece_data["instance"] = piece
        piece_data["collection"] = self._serialize_collection(
            collection=piece.collection
        )
        piece_data["categorization"] = self._get_categorization(piece=piece)
        if piece.kind == PieceConstants.KIND_VIDEO:
            piece_data["sequences"] = self._serialize_sequences(piece=piece)
        piece_data["provider"] = self._serialize_provider(piece=piece)
        piece_data["meta"] = self._serialize_meta(piece=piece)
        return piece_data
