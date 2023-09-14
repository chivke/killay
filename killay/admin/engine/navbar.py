from typing import Dict, List, Optional

from django.urls import reverse

from killay.admin.lib.constants import (
    AdminNavConstants,
    ContentManagerConstants,
    SiteConfigurationConstants,
)


class AdminNavContext:
    def __init__(self, request):
        self.request = request

    def get(self) -> Dict:
        return {
            "root": self._get_root(),
            "general": self._get_general(),
            "specific": self._get_specific(),
        }

    def _get_root(self) -> Dict:
        link = reverse(AdminNavConstants.ROOT_PATTERN)
        view_name = self.request.resolver_match.view_name
        return {
            "label": AdminNavConstants.ROOT_LABEL,
            "link": link,
            "active": view_name == AdminNavConstants.ROOT_PATTERN,
        }

    def _get_general(self) -> List:
        configuration = self._get_configuration()
        content_manager = self._get_content_manager()
        pages = self._get_basic_item(
            pattern=SiteConfigurationConstants.PATTERN_PAGE_LIST,
            label=SiteConfigurationConstants.NAME_PAGES,
            icon="bookmark",
        )
        users = self._get_basic_item(
            pattern=SiteConfigurationConstants.PATTERN_USER_LIST,
            label=SiteConfigurationConstants.NAME_USERS,
            icon="users",
        )
        return [users, pages, content_manager, configuration]

    def _get_specific(self) -> List:
        location = self._get_location()
        specific = [location]
        menu_cursor = getattr(self.request, "menu_cursor", None)
        if menu_cursor:
            piece = menu_cursor.get("piece")
            archive = menu_cursor.get("archive")
            collection = menu_cursor.get("collection")
            category = menu_cursor.get("category")
            person = menu_cursor.get("person")
            keyword = menu_cursor.get("keyword")
            item = None
            if piece:
                item = self._get_specific_piece(piece=piece)
            elif person:
                item = self._get_specific_person(person=person)
            elif keyword:
                item = self._get_specific_keyword(keyword=keyword)
            elif category:
                item = self._get_specific_category(category=category)
            elif collection:
                item = self._get_specific_collection(collection=collection)
            elif archive:
                item = self._get_specific_archive(archive=archive)
            if item:
                specific.append(item)
        return specific

    def _get_specific_archive(self, archive) -> Dict:
        return self._get_basic_item(
            label=AdminNavConstants.UPDATE_ARCHIVE_LABEL.format(slug=archive.slug),
            pattern=ContentManagerConstants.VIEWS_UPDATE[
                ContentManagerConstants.SLUG_ARCHIVE
            ],
            icon="archive",
            pattern_kwargs={"slug": archive.id},
        )

    def _get_specific_collection(self, collection) -> Dict:
        return self._get_basic_item(
            label=AdminNavConstants.UPDATE_COLLECTION_LABEL.format(
                slug=collection.slug
            ),
            pattern=ContentManagerConstants.VIEWS_UPDATE[
                ContentManagerConstants.SLUG_COLLECTION
            ],
            icon="circle outline",
            pattern_kwargs={"slug": collection.id},
        )

    def _get_specific_category(self, category) -> Dict:
        return self._get_basic_item(
            label=AdminNavConstants.UPDATE_CATEGORY_LABEL.format(slug=category.slug),
            pattern=ContentManagerConstants.VIEWS_UPDATE[
                ContentManagerConstants.SLUG_CATEGORY
            ],
            icon="tag",
            pattern_kwargs={"slug": category.id},
        )

    def _get_specific_person(self, person) -> Dict:
        return self._get_basic_item(
            label=AdminNavConstants.UPDATE_PERSON_LABEL.format(slug=person.slug),
            pattern=ContentManagerConstants.VIEWS_UPDATE[
                ContentManagerConstants.SLUG_PERSON
            ],
            icon="male",
            pattern_kwargs={"slug": person.id},
        )

    def _get_specific_keyword(self, keyword) -> Dict:
        return self._get_basic_item(
            label=AdminNavConstants.UPDATE_KEYWORD_LABEL.format(slug=keyword.slug),
            pattern=ContentManagerConstants.VIEWS_UPDATE[
                ContentManagerConstants.SLUG_KEYWORD
            ],
            icon="font",
            pattern_kwargs={"slug": keyword.id},
        )

    def _get_specific_piece(self, piece):
        icon_by_kind = {
            "VIDEO": "film",
            "IMAGE": "image",
            "DOCUMENT": "file alternate",
            "SOUND": "music",
        }
        return self._get_basic_item(
            label=AdminNavConstants.UPDATE_PIECE_LABEL.format(code=piece.code),
            pattern=ContentManagerConstants.VIEWS_UPDATE[
                ContentManagerConstants.SLUG_PIECE
            ],
            icon=icon_by_kind[piece.kind],
            pattern_kwargs={"slug": piece.id},
        )

    def _get_configuration(self):
        general_item = self._get_basic_item(
            pattern=SiteConfigurationConstants.PATTERN_GENERAL,
            label=SiteConfigurationConstants.NAME_GENERAL,
            icon="circle",
        )
        viewer_item = self._get_basic_item(
            pattern=SiteConfigurationConstants.PATTERN_VIEWER,
            label=SiteConfigurationConstants.NAME_VIEWER,
            icon="eye",
        )
        social_media_item = self._get_basic_item(
            pattern=SiteConfigurationConstants.PATTERN_SOCIAL_MEDIA,
            label=SiteConfigurationConstants.NAME_SOCIAL_MEDIA,
            icon="thumbs up",
        )
        logo_item = self._get_basic_item(
            pattern=SiteConfigurationConstants.PATTERN_LOGO,
            label=SiteConfigurationConstants.NAME_LOGO,
            icon="images",
        )
        return {
            "label": SiteConfigurationConstants.MAIN_TITLE,
            "items": [general_item, viewer_item, social_media_item, logo_item],
            "icon": "cog",
        }

    def _get_basic_item(self, pattern, label, icon, pattern_kwargs=None):
        if pattern_kwargs:
            link = reverse(pattern, kwargs=pattern_kwargs)
        else:
            link = reverse(pattern)
        return {
            "label": label,
            "link": link,
            "active": self.request.path == link,
            "icon": icon,
            "items": False,
        }

    def _get_content_manager(self):
        bulk_action_item = self._get_basic_item(
            pattern=ContentManagerConstants.VIEWS_LIST[
                ContentManagerConstants.SLUG_BULK_ACTION
            ],
            label=ContentManagerConstants.NAME_BULK_ACTION,
            icon="cloud upload",
        )
        place_item = self._get_basic_item(
            pattern=ContentManagerConstants.VIEWS_LIST[
                ContentManagerConstants.SLUG_PLACE
            ],
            label=ContentManagerConstants.NAME_PLACE,
            icon="map marker",
        )
        archive_item = self._get_basic_item(
            pattern=ContentManagerConstants.VIEWS_LIST[
                ContentManagerConstants.SLUG_ARCHIVE
            ],
            label=ContentManagerConstants.NAME_ARCHIVE,
            icon="archive",
        )
        collection_item = self._get_basic_item(
            pattern=ContentManagerConstants.VIEWS_LIST[
                ContentManagerConstants.SLUG_COLLECTION
            ],
            label=ContentManagerConstants.NAME_COLLECTION,
            icon="circle outline",
        )
        piece_item = self._get_basic_item(
            pattern=ContentManagerConstants.VIEWS_LIST[
                ContentManagerConstants.SLUG_PIECE
            ],
            label=ContentManagerConstants.NAME_PIECE,
            icon="file",
        )
        category_item = self._get_basic_item(
            pattern=ContentManagerConstants.VIEWS_LIST[
                ContentManagerConstants.SLUG_CATEGORY
            ],
            label=ContentManagerConstants.NAME_CATEGORY,
            icon="tag",
        )
        person_item = self._get_basic_item(
            pattern=ContentManagerConstants.VIEWS_LIST[
                ContentManagerConstants.SLUG_PERSON
            ],
            label=ContentManagerConstants.NAME_PERSON,
            icon="male",
        )
        keyword_item = self._get_basic_item(
            pattern=ContentManagerConstants.VIEWS_LIST[
                ContentManagerConstants.SLUG_KEYWORD
            ],
            label=ContentManagerConstants.NAME_KEYWORD,
            icon="font",
        )
        return {
            "label": ContentManagerConstants.MAIN_TITLE,
            "items": [
                bulk_action_item,
                place_item,
                archive_item,
                collection_item,
                piece_item,
                category_item,
                person_item,
                keyword_item,
            ],
            "icon": "book",
        }

    def _get_location(self) -> Dict:
        place = self.request.place
        place_item = self._get_place_item(place=place)
        items = [place_item]
        if place:
            ip_item = self._get_ip_item(place=place)
            items.append(ip_item)
        return {
            "label": AdminNavConstants.LOCATION_LABEL,
            "items": items,
            "icon": "map marker",
        }

    def _get_ip_item(self, place) -> Dict:
        link = reverse(
            AdminNavConstants.LOCATION_UPDATE_ADDRESS_PATTERN,
            kwargs={"slug": place.id},
        )
        return {
            "label": AdminNavConstants.LOCATION_UPDATE_ADDRESS_LABEL,
            "header": self.request.ip_address,
            "link": link,
            "active": self.request.path == link,
            "icon": "edit",
        }

    def _get_place_item(self, place: Optional = None):
        if place:
            link = reverse(
                AdminNavConstants.LOCATION_UPDATE_PLACE_PATTERN,
                kwargs={"slug": place.id},
            )
            label = AdminNavConstants.LOCATION_UPDATE_PLACE_LABEL
            header = place.name
            icon = "edit"
        else:
            link = reverse(
                AdminNavConstants.LOCATION_CREATE_PLACE_PATTERN,
            )
            label = AdminNavConstants.LOCATION_CREATE_PLACE_LABEL
            header = self.request.ip_address
            icon = "plus"
        return {
            "header": header,
            "label": label,
            "link": link,
            "active": self.request.path == link,
            "icon": icon,
        }
