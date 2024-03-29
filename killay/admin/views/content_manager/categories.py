from killay.admin.lib.constants import ContentManagerConstants
from killay.admin.views.content_manager import get_content_manager_extra_links
from killay.admin.views.mixins import (
    CreateAdminView,
    DeleteAdminView,
    FormSetAdminView,
    UpdateAdminView,
)
from killay.admin.forms import (
    CategoryForm,
    CategoryFormSet,
)
from killay.archives.services import (
    get_archive_names_and_slugs,
    get_collection_names_and_slugs,
)


CATEGORY_SLUG = ContentManagerConstants.SLUG_CATEGORY
CATEGORY_EXTRA_LINKS = get_content_manager_extra_links(view_slug=CATEGORY_SLUG)


class CategoryListView(FormSetAdminView):
    main_title = ContentManagerConstants.MAIN_TITLE
    second_title = ContentManagerConstants.VIEWS_SECOND_TITLE[CATEGORY_SLUG]
    description = ContentManagerConstants.DESCRIPTION_CATEGORY
    formset_class = CategoryFormSet
    reverse_url = ContentManagerConstants.VIEWS_LIST[CATEGORY_SLUG]
    update_url = ContentManagerConstants.VIEWS_UPDATE[CATEGORY_SLUG]
    delete_url = ContentManagerConstants.VIEWS_DELETE[CATEGORY_SLUG]
    create_url = ContentManagerConstants.VIEWS_CREATE[CATEGORY_SLUG]
    breadcrumb = [
        ContentManagerConstants.DICT_LINK[ContentManagerConstants.SLUG_ARCHIVE]["list"],
        ContentManagerConstants.DICT_LINK[ContentManagerConstants.SLUG_COLLECTION][
            "list"
        ],
        {"name": ContentManagerConstants.VIEWS_SECOND_TITLE[CATEGORY_SLUG]},
    ]
    extra_links = CATEGORY_EXTRA_LINKS
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


admin_category_list_view = CategoryListView.as_view()


_common_bredcrumb = [
    ContentManagerConstants.DICT_LINK[ContentManagerConstants.SLUG_ARCHIVE]["list"],
    ContentManagerConstants.DICT_LINK[ContentManagerConstants.SLUG_COLLECTION]["list"],
    ContentManagerConstants.DICT_LINK[CATEGORY_SLUG]["list"],
]


class CategoryCreateView(CreateAdminView):
    main_title = ContentManagerConstants.MAIN_TITLE
    description = ContentManagerConstants.DESCRIPTION_CATEGORY
    form_class = CategoryForm
    reverse_url = ContentManagerConstants.VIEWS_UPDATE[CATEGORY_SLUG]
    breadcrumb = [*_common_bredcrumb, {"name": "New Category"}]
    extra_links = CATEGORY_EXTRA_LINKS


admin_category_create_view = CategoryCreateView.as_view()


class CategoryBreadcrumMixin:
    def get_breadcrumb(self) -> list:
        return [*_common_bredcrumb, {"name": self.object.name}]


class CategoryUpdateView(CategoryBreadcrumMixin, UpdateAdminView):
    main_title = ContentManagerConstants.MAIN_TITLE
    description = ContentManagerConstants.DESCRIPTION_CATEGORY
    form_class = CategoryForm
    reverse_url = ContentManagerConstants.VIEWS_UPDATE[CATEGORY_SLUG]
    delete_url = ContentManagerConstants.VIEWS_DELETE[CATEGORY_SLUG]
    extra_links = CATEGORY_EXTRA_LINKS


admin_category_update_view = CategoryUpdateView.as_view()


class CategoryDeleteView(CategoryBreadcrumMixin, DeleteAdminView):
    main_title = ContentManagerConstants.MAIN_TITLE
    description = ContentManagerConstants.DESCRIPTION_CATEGORY
    form_class = CategoryForm
    reverse_url = ContentManagerConstants.VIEWS_LIST[CATEGORY_SLUG]
    extra_links = CATEGORY_EXTRA_LINKS
    delete_url = ContentManagerConstants.VIEWS_UPDATE[CATEGORY_SLUG]


admin_category_delete_view = CategoryDeleteView.as_view()
