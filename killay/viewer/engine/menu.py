from typing import Dict, List

from django.urls import reverse

from killay.archives.services import (
    get_public_archives,
    get_public_archive_by_slug,
    get_public_collection_by_slug,
    get_public_collections_by_archive_id,
)
from killay.pages.services import (
    get_public_archive_menu_pages,
    get_public_collection_menu_pages,
    get_public_menu_pages,
)
from killay.viewer.engine.base import PipelineBase
from killay.viewer.lib.constants import (
    ViewerConstants,
    ViewerPatternConstants,
    SiteContextConstants,
)


class MenuBase(PipelineBase):
    def _get_initial_main_menu(self) -> List[Dict]:
        main_menu = []
        pages = get_public_menu_pages(
            place=self.place, is_superuser=self.user.is_superuser
        )
        page_links = self._parse_page_links(pages=pages)
        main_menu.extend(page_links)
        return main_menu

    def _get_archive_links(self, archives, selected_archive=None):
        pattern = ViewerPatternConstants.pattern_by_name(
            name=ViewerPatternConstants.ARCHIVE_DETAIL
        )
        return [
            {
                "name": archive.name,
                "link": reverse(pattern, kwargs={"slug": archive.slug}),
                "active": (selected_archive and archive.slug == selected_archive.slug),
            }
            for archive in archives
        ]

    def _get_collection_links(self, collections, selected_collection=None):
        base_url = self._get_piece_list_base_url()
        return [
            {
                "name": collection.name,
                "link": f"{base_url}?collection={collection.slug}",
                "active": (
                    selected_collection
                    and collection.slug == selected_collection.slug
                    and collection.archive_id == selected_collection.archive_id
                ),
            }
            for collection in collections
        ]

    def _get_category_links(self, categories, selected_category=None):
        base_url = self._get_piece_list_base_url()
        category_links = []
        for category in categories:
            collection = (
                f"&collection={category.collection.slug}" if category.collection else ""
            )
            link = f"{base_url}?category={category.slug}{collection}"
            is_active = (
                selected_category
                and category.slug == selected_category.slug
                and category.collection_id == selected_category.collection_id
            )
            category_link = {
                "name": category.name,
                "link": link,
                "active": is_active,
            }
            category_links.append(category_link)
        collection = self.cursor.get("collection")
        all_pieces = {
            "name": SiteContextConstants.NAME_ALL,
            "link": (
                base_url
                if not collection
                else f"{base_url}?collection={collection.slug}"
            ),
            "active": (
                collection
                and not selected_category
                and not self.cursor.get("type") == "page"
            ),
        }
        if category_links:
            category_links.append(all_pieces)
        return category_links

    def _get_archive_page_links(self, archive_id: int) -> List[Dict]:
        pages = get_public_archive_menu_pages(
            archive_id=archive_id,
            place=self.place,
            is_superuser=self.user.is_superuser,
        )
        return self._parse_page_links(pages=pages)

    def _get_collection_page_links(self, collection_id: int) -> List[Dict]:
        pages = get_public_collection_menu_pages(
            collection_id=collection_id,
            place=self.place,
            is_superuser=self.user.is_superuser,
        )
        return self._parse_page_links(pages=pages)

    def _parse_page_links(self, pages):
        page_links = []
        for page in pages:
            link = page.get_absolute_url()
            page_link = {
                "name": page.title,
                "link": link,
                "active": link == self.request.path,
            }
            page_links.append(page_link)
        return page_links


class MenuOneArchiveBase:
    def _get_one_archive_main_menu(self) -> List[Dict]:
        assert self.viewer.scope == ViewerConstants.SCOPE_ONE_ARCHIVE
        main_menu = self._get_initial_main_menu()
        archive = get_public_archive_by_slug(
            slug=self.viewer.scope_archive.slug,
            place=self.place,
            is_superuser=self.user.is_superuser,
        )
        if not archive:
            return main_menu
        collections = get_public_collections_by_archive_id(
            archive_id=archive.id,
            place=self.place,
            is_superuser=self.user.is_superuser,
        )
        archive_page_links = self._get_archive_page_links(archive_id=archive.id)
        main_menu.extend(archive_page_links)
        selected_collection = self.cursor.get("collection")
        collection_links = self._get_collection_links(
            collections=collections,
            selected_collection=selected_collection,
        )
        main_menu.extend(collection_links)
        return main_menu

    def _get_one_archive_submenus(self) -> List[List[Dict]]:
        assert self.viewer.scope == ViewerConstants.SCOPE_ONE_ARCHIVE
        selected_collection = self.cursor.get("collection")
        if not selected_collection:
            return []
        category_links = self._get_category_links(
            categories=selected_collection.categories.all(),
            selected_category=self.cursor.get("category"),
        )
        collection_page_links = self._get_collection_page_links(
            collection_id=selected_collection.id
        )
        return [[*collection_page_links, *category_links]]


class MenuOneCollectionBase:
    def _get_one_collection_main_menu(self) -> List[Dict]:
        assert self.viewer.scope == ViewerConstants.SCOPE_ONE_COLLECTION
        main_menu = self._get_initial_main_menu()
        collection = get_public_collection_by_slug(
            slug=self.viewer.scope_collection.slug,
            place=self.place,
            is_superuser=self.user.is_superuser,
            archive_id=self.viewer.scope_collection.archive_id,
        )
        if not collection:
            return main_menu
        category_links = self._get_category_links(
            categories=collection.categories.all(),
            selected_category=self.cursor.get("category"),
        )
        collection_page_links = self._get_collection_page_links(
            collection_id=collection.id
        )
        main_menu = [*collection_page_links, *category_links]
        return main_menu

    def _get_one_collection_submenus(self) -> List[List[Dict]]:
        assert self.viewer.scope == ViewerConstants.SCOPE_ONE_COLLECTION
        return []


class MenuAllBase:
    def _get_all_main_menu(self) -> List[Dict]:
        assert self.viewer.scope == ViewerConstants.SCOPE_ALL
        main_menu = self._get_initial_main_menu()
        archives = get_public_archives(
            place=self.place,
            is_superuser=self.user.is_superuser,
        )
        selected_archive = self.cursor.get("archive")
        archive_links = self._get_archive_links(
            archives=archives, selected_archive=selected_archive
        )
        main_menu.extend(archive_links)
        return main_menu

    def _get_all_submenus(self) -> List[List[Dict]]:
        assert self.viewer.scope == ViewerConstants.SCOPE_ALL
        submenus = []
        selected_archive = self.cursor.get("archive")
        selected_collection = self.cursor.get("collection")
        if selected_archive:
            collections = get_public_collections_by_archive_id(
                archive_id=selected_archive.id,
                place=self.place,
                is_superuser=self.user.is_superuser,
            )
            collection_links = self._get_collection_links(
                collections=collections,
                selected_collection=selected_collection,
            )
            archive_page_links = self._get_archive_page_links(
                archive_id=selected_archive.id
            )
            submenus.append([*archive_page_links, *collection_links])
        if selected_archive and selected_collection:
            category_links = self._get_category_links(
                categories=selected_collection.categories.all(),
                selected_category=self.cursor.get("category"),
            )
            collection_page_links = self._get_collection_page_links(
                collection_id=selected_collection.id
            )
            submenus.append([*collection_page_links, *category_links])
        return submenus
