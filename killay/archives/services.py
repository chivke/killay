from typing import Dict, List, Optional

from django.db.models import Q

from killay.archives.models import (
    Archive,
    Category,
    Collection,
    Keyword,
    Person,
    Piece,
    Place,
)


def get_archive_names_and_slugs() -> List[Dict]:
    return list(Archive.objects_in_site.values("name", "slug"))


def get_archive_related_field_data(archive_id: int) -> dict:
    total_collections = Collection.objects.filter(archive_id=archive_id).count()
    total_pieces = Piece.objects.filter(collection__archive_id=archive_id).count()
    return {
        Collection._meta.verbose_name_plural.capitalize(): total_collections,
        Piece._meta.verbose_name_plural.capitalize(): total_pieces,
    }


def _get_allowed_archive_ids_by_place(place: Place) -> list:
    return list(place.allowed_archives.values_list("id", flat=True)) if place else []


def _can_see_the_archive(archive, allowed_archive_ids) -> bool:
    return archive.is_visible and (
        not archive.is_restricted or archive.id in allowed_archive_ids
    )


def get_public_archives(
    place: Optional[Place] = None,
    is_superuser: bool = False,
) -> List[Archive]:
    allowed_archive_ids = _get_allowed_archive_ids_by_place(place=place)
    filters = {}
    if not is_superuser:
        filters["is_visible"] = True

    queryset = Archive.objects_in_site.filter(**filters)
    filtered = []
    for archive in queryset:
        if is_superuser or _can_see_the_archive(
            archive=archive, allowed_archive_ids=allowed_archive_ids
        ):
            filtered.append(archive)
    return filtered


def get_public_archive_by_slug(
    slug: str, place: Optional[Place] = None, is_superuser: bool = False
) -> Optional[Archive]:
    allowed_archive_ids = _get_allowed_archive_ids_by_place(place=place)
    filters = {"slug": slug}
    if not is_superuser:
        filters["is_visible"] = True
    archive = Archive.objects_in_site.filter(**filters).first()
    if (
        is_superuser
        or not archive
        or _can_see_the_archive(
            archive=archive, allowed_archive_ids=allowed_archive_ids
        )
    ):
        return archive


def get_collection_related_field_data(collection_id: int) -> dict:
    total_pieces = Piece.objects.filter(collection_id=collection_id).count()
    return {
        Piece._meta.verbose_name_plural.capitalize(): total_pieces,
    }


def get_collection_names_and_slugs() -> list:
    return list(Collection.objects_in_site.values("name", "slug"))


def _get_allowed_collection_ids_by_place(place: Place) -> list:
    return list(place.allowed_collections.values_list("id", flat=True)) if place else []


def get_place_from_ip_address(ip_address: str) -> Optional[Place]:
    return Place.objects.filter(addresses__ipv4=ip_address).first()


def _can_see_the_collection(
    collection,
    allowed_archive_ids,
    allowed_collection_ids,
) -> bool:
    archive = collection.archive
    can_see_the_archive = _can_see_the_archive(
        archive=archive, allowed_archive_ids=allowed_archive_ids
    )
    return can_see_the_archive and (
        not collection.is_restricted or collection.id in allowed_collection_ids
    )


def get_public_collections_by_archive_id(
    archive_id: int, place: Optional[Place] = None, is_superuser: bool = False
) -> List[Collection]:
    allowed_archive_ids = _get_allowed_archive_ids_by_place(place=place)
    allowed_collection_ids = _get_allowed_collection_ids_by_place(place=place)
    filters = {"archive_id": archive_id}
    if not is_superuser:
        filters["is_visible"] = True
    collections = Collection.objects_in_site.filter(**filters)
    filtered = []
    for collection in collections:
        if is_superuser or _can_see_the_collection(
            collection=collection,
            allowed_archive_ids=allowed_archive_ids,
            allowed_collection_ids=allowed_collection_ids,
        ):
            filtered.append(collection)
    return filtered


def get_public_collection_by_slug(
    slug: str,
    archive_id: Optional[int] = None,
    place: Optional[Place] = None,
    is_superuser: bool = False,
) -> Optional[Collection]:
    filters = {"slug": slug}
    allowed_archive_ids = _get_allowed_archive_ids_by_place(place=place)
    allowed_collection_ids = _get_allowed_collection_ids_by_place(place=place)
    if not is_superuser:
        filters["is_visible"] = True
    if archive_id:
        filters["archive_id"] = archive_id
    collection = Collection.objects_in_site.filter(**filters).first()
    if is_superuser or not collection:
        return collection
    if _can_see_the_collection(
        collection=collection,
        allowed_archive_ids=allowed_archive_ids,
        allowed_collection_ids=allowed_collection_ids,
    ):
        return collection


def get_category_by_slug(slug: str, collection_id: int) -> Optional[Category]:
    return Category.objects_in_site.filter(
        slug=slug, collection_id=collection_id
    ).first()


def get_person_by_slug(slug: str) -> Optional[Person]:
    return Person.objects_in_site.filter(slug=slug).first()


def get_keyword_by_slug(slug: str) -> Optional[Keyword]:
    return Keyword.objects_in_site.filter(slug=slug).first()


def _get_allowed_piece_ids_by_place(place: Place) -> list:
    return list(place.allowed_pieces.values_list("id", flat=True)) if place else []


def _can_see_the_piece(
    piece: Piece,
    allowed_archive_ids: Optional[List[int]],
    allowed_collection_ids: Optional[List[int]],
    allowed_piece_ids: Optional[List[int]],
) -> bool:
    allowed_collection = _can_see_the_collection(
        collection=piece.collection,
        allowed_archive_ids=allowed_archive_ids,
        allowed_collection_ids=allowed_collection_ids,
    )
    return (
        allowed_collection
        and piece.is_published
        and (not piece.is_restricted or piece.id in allowed_piece_ids)
    )


def get_public_pieces(
    archive: Optional[Archive] = None,
    collection: Optional[Collection] = None,
    categorization: Optional[Dict] = None,
    place: Optional[Place] = None,
    is_superuser: bool = False,
    query_search: Optional[str] = None,
    kind: Optional[str] = None,
) -> List[Piece]:
    allowed_archive_ids = _get_allowed_archive_ids_by_place(place=place)
    allowed_collection_ids = _get_allowed_collection_ids_by_place(place=place)
    allowed_piece_ids = _get_allowed_piece_ids_by_place(place=place)
    filters = {}
    categorization = categorization or {}
    category = categorization.get("category")
    if category:
        filters["categories"] = category.id
        collection = category.collection
    person = categorization.get("person")
    if person:
        filters["people"] = person.id
    keyword = categorization.get("keyword")
    if keyword:
        filters["keywords"] = keyword.id
    if collection:
        filters["collection_id"] = collection.id
    elif archive:
        filters["collection__archive_id"] = archive.id
    if kind:
        filters["kind"] = kind
    queryset = Piece.objects_in_site.select_related("collection__archive").filter(
        **filters
    )

    if query_search:
        queryset = queryset.filter(
            Q(code__icontains=query_search)
            | Q(title__icontains=query_search)
            | Q(meta__description__icontains=query_search)
        )

    allowed_pieces = []
    for piece in queryset:
        if is_superuser or _can_see_the_piece(
            piece=piece,
            allowed_archive_ids=allowed_archive_ids,
            allowed_collection_ids=allowed_collection_ids,
            allowed_piece_ids=allowed_piece_ids,
        ):
            allowed_pieces.append(piece)
    return allowed_pieces


def get_public_piece(
    piece_code: str, place: Optional[Place] = None, is_superuser: bool = False
) -> Optional[Piece]:
    allowed_archive_ids = _get_allowed_archive_ids_by_place(place=place)
    allowed_collection_ids = _get_allowed_collection_ids_by_place(place=place)
    allowed_piece_ids = _get_allowed_piece_ids_by_place(place=place)
    piece = Piece.objects_in_site.filter(code=piece_code).first()
    if is_superuser or not piece:
        return piece
    if _can_see_the_piece(
        piece=piece,
        allowed_archive_ids=allowed_archive_ids,
        allowed_collection_ids=allowed_collection_ids,
        allowed_piece_ids=allowed_piece_ids,
    ):
        return piece


def get_archive_filter_options(
    place: Optional[Place] = None,
    is_superuser: bool = False,
    active_archive_id: Optional[int] = None,
) -> List[Dict]:
    archives = get_public_archives(place=place, is_superuser=is_superuser)
    return [
        {
            "label": archive.name,
            "slug": archive.slug,
            "active": archive.id == active_archive_id,
        }
        for archive in archives
    ]


def get_collection_filter_options(
    place: Optional[Place] = None,
    is_superuser: bool = False,
    active_collection_id: Optional[int] = None,
    archive_id: Optional[int] = None,
) -> List[Dict]:
    allowed_archive_ids = _get_allowed_archive_ids_by_place(place=place)
    allowed_collection_ids = _get_allowed_collection_ids_by_place(place=place)
    filters = {}
    if not is_superuser:
        filters["is_visible"] = True
    if archive_id:
        filters["archive_id"] = archive_id
    queryset = Collection.objects_in_site.select_related("archive").filter(**filters)
    return [
        {
            "label": collection.name,
            "slug": collection.slug,
            "archive_slug": collection.archive.slug,
            "active": collection.id == active_collection_id,
        }
        for collection in queryset
        if is_superuser
        or _can_see_the_collection(
            collection=collection,
            allowed_archive_ids=allowed_archive_ids,
            allowed_collection_ids=allowed_collection_ids,
        )
    ]


def get_category_filter_options(
    place: Optional[Place] = None,
    is_superuser: bool = False,
    active_category_id: Optional[int] = None,
    archive_id: Optional[int] = None,
    collection_id: Optional[int] = None,
):
    allowed_archive_ids = _get_allowed_archive_ids_by_place(place=place)
    allowed_collection_ids = _get_allowed_collection_ids_by_place(place=place)

    queryset = Category.objects_in_site.select_related("collection__archive")
    if collection_id:
        queryset.filter(collection_id=collection_id)
    elif archive_id:
        queryset.filter(collection__archive_id=collection_id)
    category_filter_options = []
    for category in queryset:
        if is_superuser or (
            not category.collection
            or _can_see_the_collection(
                collection=category.collection,
                allowed_archive_ids=allowed_archive_ids,
                allowed_collection_ids=allowed_collection_ids,
            )
        ):
            category_option = {
                "label": category.name,
                "slug": category.slug,
                "active": category.id == active_category_id,
            }
            if category.collection:
                category_option["collection_slug"] = category.collection_slug
                category_option["archive_slug"] = category.collection.archive.slug
            category_filter_options.append(category_option)
    return category_filter_options


def get_person_filter_options(
    place: Optional[Place] = None,
    is_superuser: bool = False,
    active_person_id: Optional[int] = None,
):
    queryset = Person.objects_in_site.all()
    return [
        {
            "label": person.name,
            "slug": person.slug,
            "active": person.id == active_person_id,
        }
        for person in queryset
    ]


def get_keyword_filter_options(
    place: Optional[Place] = None,
    is_superuser: bool = False,
    active_keyword_id: Optional[int] = None,
):
    queryset = Keyword.objects_in_site.all()
    return [
        {
            "label": keyword.name,
            "slug": keyword.slug,
            "active": keyword.id == active_keyword_id,
        }
        for keyword in queryset
    ]
