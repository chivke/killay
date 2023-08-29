from django.urls import reverse

from killay.admin.lib.constants import ContentManagerConstants
from killay.admin.forms import (
    ArchiveForm,
    ArchiveFormSet,
)
from killay.admin.views.content_manager import get_content_manager_extra_links
from killay.admin.views.mixins import (
    CreateAdminView,
    DeleteAdminView,
    FormSetAdminView,
    UpdateAdminView,
)
from killay.archives.services import get_archive_related_field_data


ARCHIVE_SLUG = ContentManagerConstants.SLUG_ARCHIVE
ARCHIVE_EXTRA_LINKS = get_content_manager_extra_links(view_slug=ARCHIVE_SLUG)


class ArchiveListView(FormSetAdminView):
    main_title = ContentManagerConstants.MAIN_TITLE
    second_title = ContentManagerConstants.VIEWS_SECOND_TITLE[ARCHIVE_SLUG]
    description = ContentManagerConstants.DESCRIPTION_ARCHIVE
    formset_class = ArchiveFormSet
    reverse_url = ContentManagerConstants.VIEWS_LIST[ARCHIVE_SLUG]
    update_url = ContentManagerConstants.VIEWS_UPDATE[ARCHIVE_SLUG]
    delete_url = ContentManagerConstants.VIEWS_DELETE[ARCHIVE_SLUG]
    create_url = ContentManagerConstants.VIEWS_CREATE[ARCHIVE_SLUG]
    extra_links = ARCHIVE_EXTRA_LINKS


admin_archive_list_view = ArchiveListView.as_view()


_common_bredcrumb = [ContentManagerConstants.DICT_LINK[ARCHIVE_SLUG]["list"]]


class ArchiveCreateView(CreateAdminView):
    main_title = ContentManagerConstants.MAIN_TITLE
    description = ContentManagerConstants.DESCRIPTION_ARCHIVE
    form_class = ArchiveForm
    reverse_url = ContentManagerConstants.VIEWS_UPDATE[ARCHIVE_SLUG]
    extra_links = ARCHIVE_EXTRA_LINKS
    breadcrumb = [*_common_bredcrumb, {"name": "New Archive"}]


admin_archive_create_view = ArchiveCreateView.as_view()


class ArchiveUpdateView(UpdateAdminView):
    main_title = ContentManagerConstants.MAIN_TITLE
    description = ContentManagerConstants.DESCRIPTION_ARCHIVE
    form_class = ArchiveForm
    reverse_url = ContentManagerConstants.VIEWS_UPDATE[ARCHIVE_SLUG]
    delete_url = ContentManagerConstants.VIEWS_DELETE[ARCHIVE_SLUG]
    extra_links = ARCHIVE_EXTRA_LINKS

    def get_extra_data(self) -> list:
        return get_archive_related_field_data(archive_id=self.object.id)

    def get_breadcrumb(self) -> list:
        return [*_common_bredcrumb, {"name": self.object.name}]

    def get_extra_actions(self) -> list:
        create_collection_pattern_name = ContentManagerConstants.VIEWS_CREATE[
            ContentManagerConstants.SLUG_COLLECTION
        ]
        create_collection_link = reverse(create_collection_pattern_name)
        create_collection_name = "Create Collection"
        create_collection_link = f"{create_collection_link}?archive={self.object.id}"
        return [{"name": create_collection_name, "link": create_collection_link}]


admin_archive_update_view = ArchiveUpdateView.as_view()


class ArchiveDeleteView(DeleteAdminView):
    main_title = ContentManagerConstants.MAIN_TITLE
    description = ContentManagerConstants.DESCRIPTION_ARCHIVE
    form_class = ArchiveForm
    reverse_url = ContentManagerConstants.VIEWS_LIST[ARCHIVE_SLUG]
    delete_url = ContentManagerConstants.VIEWS_UPDATE[ARCHIVE_SLUG]
    extra_links = ARCHIVE_EXTRA_LINKS

    def get_extra_data(self) -> list:
        return get_archive_related_field_data(archive_id=self.object.id)

    def get_breadcrumb(self) -> list:
        return [*_common_bredcrumb, {"name": self.object.name}]


admin_archive_delete_view = ArchiveDeleteView.as_view()
