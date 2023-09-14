from typing import Dict, List, Optional, Tuple

from django.db.models import Q, QuerySet
from django.utils.text import slugify

from killay.archives.models import (
    Archive,
    Category,
    Collection,
    Keyword,
    Person,
    Piece,
    PieceMeta,
    Place,
    Provider,
)


def bulk_create_pieces(data_list):
    instances = [Piece(**data) for data in data_list]
    objs = Piece.objects_in_site.bulk_create(instances)
    return Piece.objects_in_site.filter(code__in=[obj.code for obj in objs])


def bulk_add_piece_categories(
    pieces_categories_data: List[Tuple[int, List[int]]],
):
    instances = []
    for piece_id, categories in pieces_categories_data:
        partial_instances = [
            Piece.categories.through(
                piece_id=piece_id,
                category_id=category_id,
            )
            for category_id in categories
        ]
        instances.extend(partial_instances)
    return Piece.categories.through.objects.bulk_create(instances)


def _bulk_add_many_to_many_by_list_text(
    data_list: List[Tuple[int, List[str]]],
    parent_model,
    parent_model_field,
    related_model,
    related_model_field,
    through_field_name,
):
    unique_names = set()
    for parent_id, related_names in data_list:
        unique_names = unique_names | set(related_names)
    current_instances = related_model.objects_in_site.filter(
        name__in=list(unique_names)
    )
    current_map = {obj.name.lower(): obj for obj in current_instances}
    current_slug_map = {obj.slug: obj for obj in current_instances}
    instances_for_create = [
        related_model(name=name, slug=slugify(name))
        for name in unique_names
        if (name.lower() not in current_map and slugify(name) not in current_slug_map)
    ]
    related_model.objects_in_site.bulk_create(objs=instances_for_create)
    created_instances = related_model.objects_in_site.filter(
        slug__in=[obj.slug for obj in instances_for_create]
    )
    created_map = {obj.name.lower(): obj for obj in created_instances}
    created_slug_map = {obj.slug: obj for obj in created_instances}
    instances = []
    through_class = getattr(parent_model, through_field_name).through

    for parent_id, related_names in data_list:
        related_ids = set()
        for name in related_names:
            name_lower = name.lower()
            if name_lower in current_map:
                related_ids.add(current_map[name_lower].id)
                continue

            if name_lower in created_map:
                related_ids.add(created_map[name_lower].id)
                continue

            slug = slugify(name)
            if slug in current_slug_map:
                related_ids.add(current_slug_map[slug].id)
                continue
            if slug in created_slug_map:
                related_ids.add(created_slug_map[slug].id)
                continue
        if related_ids:
            partial_instances = [
                through_class(
                    **{
                        parent_model_field: parent_id,
                        related_model_field: _id,
                    }
                )
                for _id in related_ids
            ]
            instances.extend(partial_instances)
    if instances:
        return through_class.objects.bulk_create(objs=instances)


def bulk_add_piece_people_by_texts(piece_people_data: List[Tuple[int, List[str]]]):
    return _bulk_add_many_to_many_by_list_text(
        data_list=piece_people_data,
        parent_model=Piece,
        parent_model_field="piece_id",
        related_model=Person,
        related_model_field="person_id",
        through_field_name="people",
    )


def bulk_create_meta_pieces(piece_meta_data: List[Tuple[int, Dict]]):
    current_meta_list = PieceMeta.objects.filter(
        piece_id__in=[piece_id for piece_id, _ in piece_meta_data]
    )
    current_meta_map = {meta.piece_id: meta.id for meta in current_meta_list}
    instances = [
        PieceMeta(id=current_meta_map.get(piece_id), piece_id=piece_id, **meta_data)
        for piece_id, meta_data in piece_meta_data
    ]
    instances_for_create = [obj for obj in instances if not obj.id]
    instances_for_update = [obj for obj in instances if obj.id]
    if instances_for_create:
        PieceMeta.objects.bulk_create(objs=instances_for_create)
    if instances_for_update:
        PieceMeta.objects.bulk_update(
            objs=instances_for_update,
            fields=[
                "event",
                "description",
                "description_date",
                "location",
                "duration",
                "register_date",
                "register_author",
                "productor",
                "notes",
                "archivist_notes",
                "documentary_unit",
                "lang",
                "original_format",
            ],
        )


def bulk_add_piece_keyword_by_texts(
    piece_keyword_data,
):
    return _bulk_add_many_to_many_by_list_text(
        data_list=piece_keyword_data,
        parent_model=Piece,
        parent_model_field="piece_id",
        related_model=Keyword,
        related_model_field="keyword_id",
        through_field_name="keywords",
    )


def bulk_create_piece_video_provider(piece_video_data: List[Tuple[int, Dict]]):
    instances = [
        Provider(
            piece_id=piece_id,
            active=video_data.get("active", True),
            ply_embed_id=video_data.get("ply_embed_id"),
            plyr_provider=video_data.get("plyr_provider"),
        )
        for piece_id, video_data in piece_video_data
    ]
    return Provider.objects.bulk_create(objs=instances)


def get_pieces_fields_data():
    fields_data = {
        field.name: {"label": field.verbose_name, "description": field.help_text}
        for field in Piece._meta.fields
    }
    many_to_many_fields_data = {
        field.name: {"label": field.verbose_name, "description": field.help_text}
        for field in Piece._meta.many_to_many
    }
    return {**fields_data, **many_to_many_fields_data}


def get_meta_pieces_fields_data():
    return {
        field.name: {"label": field.verbose_name, "description": field.help_text}
        for field in PieceMeta._meta.fields
    }


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


def get_all_collections() -> list:
    return Collection.objects_in_site.all()


def get_all_categories() -> QuerySet:
    return Category.objects_in_site.all()


def get_pieces_queryset() -> QuerySet:
    return Piece.objects_in_site.all()


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
