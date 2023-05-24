from django.urls import reverse
from killay.admin.lib.constants import ContentManagerConstants
from killay.admin.views.content_manager import get_content_manager_extra_links
from killay.admin.views.mixins import (
    CreateAdminView,
    DeleteAdminView,
    FormSetAdminView,
    UpdateAdminView,
)
from killay.admin.forms import (
    CollectionForm,
    CollectionFormSet,
)
from killay.archives.services import (
    get_archive_names_and_slugs,
    get_collection_related_field_data,
)


COLLECTION_SLUG = ContentManagerConstants.SLUG_COLLECTION
COLLECTION_EXTRA_LINKS = get_content_manager_extra_links(view_slug=COLLECTION_SLUG)


class CollectionListView(FormSetAdminView):
    main_title = ContentManagerConstants.MAIN_TITLE
    second_title = ContentManagerConstants.VIEWS_SECOND_TITLE[COLLECTION_SLUG]
    formset_class = CollectionFormSet
    reverse_url = ContentManagerConstants.VIEWS_LIST[COLLECTION_SLUG]
    update_url = ContentManagerConstants.VIEWS_UPDATE[COLLECTION_SLUG]
    delete_url = ContentManagerConstants.VIEWS_DELETE[COLLECTION_SLUG]
    create_url = ContentManagerConstants.VIEWS_CREATE[COLLECTION_SLUG]
    breadcrumb = [
        ContentManagerConstants.DICT_LINK[ContentManagerConstants.SLUG_ARCHIVE]["list"],
        {"name": ContentManagerConstants.VIEWS_SECOND_TITLE[COLLECTION_SLUG]},
    ]
    extra_links = COLLECTION_EXTRA_LINKS
    filters = {ContentManagerConstants.SLUG_ARCHIVE: "archive__slug"}

    def get_filter_options(self) -> dict:
        archive_options = [
            {"name": data["name"], "value": data["slug"]}
            for data in get_archive_names_and_slugs()
        ]
        return {ContentManagerConstants.SLUG_ARCHIVE: archive_options}


admin_collection_list_view = CollectionListView.as_view()


_common_bredcrumb = [
    ContentManagerConstants.DICT_LINK[ContentManagerConstants.SLUG_ARCHIVE]["list"],
    ContentManagerConstants.DICT_LINK[COLLECTION_SLUG]["list"],
]


class CollectionCreateView(CreateAdminView):
    main_title = ContentManagerConstants.MAIN_TITLE
    form_class = CollectionForm
    reverse_url = ContentManagerConstants.VIEWS_UPDATE[COLLECTION_SLUG]
    extra_links = COLLECTION_EXTRA_LINKS
    breadcrumb = [*_common_bredcrumb, {"name": "New Collection"}]


admin_collection_create_view = CollectionCreateView.as_view()


class CollectionBreadcrumMixin:
    def get_breadcrumb(self) -> list:
        archive = self._get_archive_bread()
        return [archive, {"name": self.object.name}]

    def _get_archive_bread(self) -> dict:
        archive_view = ContentManagerConstants.VIEWS_UPDATE[
            ContentManagerConstants.SLUG_ARCHIVE
        ]
        archive_link = reverse(archive_view, kwargs={"slug": self.object.archive.id})
        return {
            "name": self.object.archive.name,
            "link": archive_link,
        }


class CollectionUpdateView(CollectionBreadcrumMixin, UpdateAdminView):
    main_title = ContentManagerConstants.MAIN_TITLE
    form_class = CollectionForm
    reverse_url = ContentManagerConstants.VIEWS_UPDATE[COLLECTION_SLUG]
    delete_url = ContentManagerConstants.VIEWS_DELETE[COLLECTION_SLUG]
    extra_links = COLLECTION_EXTRA_LINKS
    breadcrumb = [*_common_bredcrumb]

    def get_extra_data(self) -> list:
        extra_data = super().get_extra_data()
        related_field_data = get_collection_related_field_data(
            collection_id=self.object.id
        )
        return {**extra_data, **related_field_data}

    def get_extra_actions(self) -> list:
        create_piece_pattern_name = ContentManagerConstants.VIEWS_CREATE[
            ContentManagerConstants.SLUG_PIECE
        ]
        create_piece_link = reverse(create_piece_pattern_name)
        create_piece_name = "Create piece"
        create_piece_link = f"{create_piece_link}?collection={self.object.id}"
        return [{"name": create_piece_name, "link": create_piece_link}]


admin_collection_update_view = CollectionUpdateView.as_view()


class CollectionDeleteView(CollectionBreadcrumMixin, DeleteAdminView):
    form_class = CollectionForm
    main_title = ContentManagerConstants.MAIN_TITLE
    reverse_url = ContentManagerConstants.VIEWS_LIST[COLLECTION_SLUG]
    delete_url = ContentManagerConstants.VIEWS_UPDATE[COLLECTION_SLUG]
    extra_links = COLLECTION_EXTRA_LINKS
    breadcrumb = [*_common_bredcrumb]

    def get_extra_data(self) -> list:
        return get_collection_related_field_data(collection_id=self.object.id)


admin_collection_delete_view = CollectionDeleteView.as_view()
