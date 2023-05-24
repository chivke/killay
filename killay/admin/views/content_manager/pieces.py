from django.urls import reverse

from killay.admin.lib.constants import ContentManagerConstants
from killay.admin.forms import (
    PieceForm,
    PieceFormSet,
    PieceMetaForm,
)
from killay.admin.views.content_manager import get_content_manager_extra_links
from killay.admin.views.mixins import (
    CreateAdminView,
    DeleteAdminView,
    FormSetAdminView,
    UpdateAdminView,
)
from killay.archives.services import (
    get_archive_names_and_slugs,
    get_collection_names_and_slugs,
)


PIECE_SLUG = ContentManagerConstants.SLUG_PIECE
PIECE_EXTRA_LINKS = get_content_manager_extra_links(view_slug=PIECE_SLUG)


class PieceListView(FormSetAdminView):
    main_title = ContentManagerConstants.MAIN_TITLE
    second_title = ContentManagerConstants.VIEWS_SECOND_TITLE[PIECE_SLUG]
    formset_class = PieceFormSet
    reverse_url = ContentManagerConstants.VIEWS_LIST[PIECE_SLUG]
    update_url = ContentManagerConstants.VIEWS_UPDATE[PIECE_SLUG]
    delete_url = ContentManagerConstants.VIEWS_DELETE[PIECE_SLUG]
    create_url = ContentManagerConstants.VIEWS_CREATE[PIECE_SLUG]
    search_field = "title"
    image_fields = ["thumb"]
    breadcrumb = [
        ContentManagerConstants.DICT_LINK[ContentManagerConstants.SLUG_ARCHIVE]["list"],
        {"name": ContentManagerConstants.VIEWS_SECOND_TITLE[PIECE_SLUG]},
    ]
    extra_links = PIECE_EXTRA_LINKS
    filters = {
        ContentManagerConstants.SLUG_ARCHIVE: "collection__archive__slug",
        ContentManagerConstants.SLUG_COLLECTION: "collection__slug",
    }

    def get_filter_options(self) -> dict:
        archive_options = [
            {"name": data["name"], "value": data["slug"]}
            for data in get_archive_names_and_slugs()
        ]
        collection_options = [
            {"name": data["name"], "value": data["slug"]}
            for data in get_collection_names_and_slugs()
        ]
        return {
            ContentManagerConstants.SLUG_ARCHIVE: archive_options,
            ContentManagerConstants.SLUG_COLLECTION: collection_options,
        }


admin_piece_list_view = PieceListView.as_view()


_common_bredcrumb = [
    ContentManagerConstants.DICT_LINK[ContentManagerConstants.SLUG_ARCHIVE]["list"],
    ContentManagerConstants.DICT_LINK[PIECE_SLUG]["list"],
]


class PieceCreateView(CreateAdminView):
    main_title = ContentManagerConstants.MAIN_TITLE
    form_class = PieceForm
    reverse_url = ContentManagerConstants.VIEWS_UPDATE[PIECE_SLUG]
    breadcrumb = [*_common_bredcrumb, {"name": "New Piece"}]
    extra_links = PIECE_EXTRA_LINKS


admin_piece_create_view = PieceCreateView.as_view()


class PieceBreadcrumMixin:
    def _get_obj_piece(self):
        return self.object

    def _get_archive_bread(self) -> dict:
        piece = self._get_obj_piece()
        archive_view = ContentManagerConstants.VIEWS_UPDATE[
            ContentManagerConstants.SLUG_ARCHIVE
        ]
        archive_kwargs = {"slug": piece.collection.archive_id}
        archive_link = reverse(archive_view, kwargs=archive_kwargs)
        return {
            "name": piece.collection.archive.name,
            "link": archive_link,
        }

    def _get_collection_bread(self) -> dict:
        piece = self._get_obj_piece()
        collection_view = ContentManagerConstants.VIEWS_UPDATE[
            ContentManagerConstants.SLUG_COLLECTION
        ]
        collection_kwargs = {"slug": piece.collection_id}
        collection_link = reverse(collection_view, kwargs=collection_kwargs)
        return {
            "name": piece.collection.name,
            "link": collection_link,
        }

    def _get_pieces_bread(self) -> dict:
        piece = self._get_obj_piece()
        slug = ContentManagerConstants.SLUG_PIECE
        pieces_view = ContentManagerConstants.VIEWS_LIST[slug]
        pieces_name = ContentManagerConstants.VIEWS_SECOND_TITLE[slug]
        pieces_link = reverse(pieces_view)
        pieces_link = f"{pieces_link}?collection={piece.collection.slug}"
        return {
            "name": pieces_name,
            "link": pieces_link,
        }

    def _get_piece_bread(self) -> dict:
        piece = self._get_obj_piece()
        slug = ContentManagerConstants.SLUG_PIECE
        piece_view = ContentManagerConstants.VIEWS_UPDATE[slug]
        piece_kwargs = {"slug": piece.id}
        piece_link = reverse(piece_view, kwargs=piece_kwargs)
        piece_name = piece.code
        return {
            "name": piece_name,
            "link": piece_link,
        }


class PieceUpdateView(PieceBreadcrumMixin, UpdateAdminView):
    main_title = ContentManagerConstants.MAIN_TITLE
    form_class = PieceForm
    name_field = "title"
    reverse_url = ContentManagerConstants.VIEWS_UPDATE[PIECE_SLUG]
    delete_url = ContentManagerConstants.VIEWS_DELETE[PIECE_SLUG]
    extra_links = PIECE_EXTRA_LINKS

    def get_breadcrumb(self) -> list:
        archive = self._get_archive_bread()
        collection = self._get_collection_bread()
        pieces = self._get_pieces_bread()
        return [archive, collection, pieces, {"name": self.object.code}]

    def get_extra_actions(self):
        meta_kwargs = {"slug": self.object.meta.id}
        meta_link = reverse("admin:piece_meta_update", kwargs=meta_kwargs)
        return [
            {"name": "General"},
            {"name": "Meta", "link": meta_link},
        ]


admin_piece_update_view = PieceUpdateView.as_view()


class PieceDeleteView(PieceBreadcrumMixin, DeleteAdminView):
    form_class = PieceForm
    name_field = "title"
    main_title = ContentManagerConstants.MAIN_TITLE
    reverse_url = ContentManagerConstants.VIEWS_LIST[PIECE_SLUG]
    delete_url = ContentManagerConstants.VIEWS_UPDATE[PIECE_SLUG]
    extra_links = PIECE_EXTRA_LINKS

    def get_breadcrumb(self) -> list:
        archive = self._get_archive_bread()
        collection = self._get_collection_bread()
        pieces = self._get_pieces_bread()
        update = self._get_piece_bread()
        return [archive, collection, pieces, update, {"name": "Delete"}]


admin_piece_delete_view = PieceDeleteView.as_view()


class PieceMetaUpdateView(PieceBreadcrumMixin, UpdateAdminView):
    main_title = ContentManagerConstants.MAIN_TITLE
    form_class = PieceMetaForm
    name_field = "piece"
    reverse_url = ContentManagerConstants.VIEWS_UPDATE[PIECE_SLUG]
    extra_links = PIECE_EXTRA_LINKS

    def get_breadcrumb(self) -> list:
        archive = self._get_archive_bread()
        collection = self._get_collection_bread()
        pieces = self._get_pieces_bread()
        update = self._get_piece_bread()
        return [archive, collection, pieces, update, {"name": "Meta"}]

    def _get_obj_piece(self):
        return self.object.piece

    def get_extra_actions(self):
        update = self._get_piece_bread()
        return [
            {"name": "General", "link": update["link"]},
            {"name": "Meta"},
        ]


admin_piece_meta_update_view = PieceMetaUpdateView.as_view()
