from typing import List, Optional

from django.conf import settings

from killay.pages.models import Page


def _filter_pages(
    pages: List[Page], place_id: Optional[int] = None, is_superuser: bool = False
) -> List[Page]:
    return [
        page
        for page in pages
        if (
            (is_superuser or page.is_visible)
            and not page.place_id
            or page.place_id == place_id
        )
    ]


def get_public_menu_pages(
    place: Optional["Place"] = None, is_superuser: bool = False
) -> List[Page]:
    pages = Page.objects.filter(
        site_id=settings.SITE_ID,
        archive_id__isnull=True,
        collection_id__isnull=True,
        is_visible_in_navbar=True,
    )
    place_id = place.id if place else None
    return _filter_pages(pages=pages, place_id=place_id, is_superuser=is_superuser)


def get_public_archive_menu_pages(
    archive_id: int, place: Optional["Place"] = None, is_superuser=False
) -> List[Page]:
    pages = Page.objects.filter(
        site_id=settings.SITE_ID,
        archive_id=archive_id,
        is_visible_in_navbar=True,
    )
    place_id = place.id if place else None
    return _filter_pages(pages=pages, place_id=place_id, is_superuser=is_superuser)


def get_public_collection_menu_pages(
    collection_id: int, place: Optional["Place"] = None, is_superuser: bool = False
) -> List[Page]:
    pages = Page.objects.filter(
        site_id=settings.SITE_ID,
        collection_id=collection_id,
        is_visible_in_navbar=True,
    )
    place_id = place.id if place else None
    return _filter_pages(pages=pages, place_id=place_id, is_superuser=is_superuser)
