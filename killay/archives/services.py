from typing import Optional

from killay.archives.models import Archive, Collection, Piece, Place


def get_archive_related_field_data(archive_id: int) -> dict:
    total_collections = Collection.objects.filter(archive_id=archive_id).count()
    total_pieces = Piece.objects.filter(collection__archive_id=archive_id).count()
    return {
        Collection._meta.verbose_name_plural.capitalize(): total_collections,
        Piece._meta.verbose_name_plural.capitalize(): total_pieces,
    }


def get_collection_related_field_data(collection_id: int) -> dict:
    total_pieces = Piece.objects.filter(collection_id=collection_id).count()
    return {
        Piece._meta.verbose_name_plural.capitalize(): total_pieces,
    }


def get_archive_names_and_slugs() -> list:
    return list(Archive.objects_in_site.values("name", "slug"))


def get_collection_names_and_slugs() -> list:
    return list(Collection.objects_in_site.values("name", "slug"))


def get_place_from_ip_address(ip_address: str) -> Optional[Place]:
    return Place.objects.filter(addresses__ipv4=ip_address).first()
