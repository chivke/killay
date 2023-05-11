from django.utils.translation import gettext

from killay.archives.models import Archive, Category, Collection, Piece


def get_archive_related_field_data(archive_id: int) -> dict:
    total_collections = Collection.objects.filter(archive_id=archive_id).count()
    total_pieces = Piece.objects.filter(collection__archive_id=archive_id).count()
    return {
        gettext("Collections"): total_collections,
        gettext("Pieces"): total_pieces,
    }
