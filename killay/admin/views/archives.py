from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse
from django.utils.translation import gettext, gettext_lazy

from killay.admin.lib.constants import ArchivesViewConstants
from killay.admin.mixins import AdminRequiredMixin, AdminUpdateMixin, FormSetMixin
from killay.admin.views.mixins import (
    CreateAdminView,
    DeleteAdminView,
    FormSetAdminView,
    UpdateAdminView,
)
from killay.admin.forms import (
    ArchiveForm,
    ArchiveFormSet,
    CategoryForm,
    CategoryFormSet,
    CollectionForm,
    CollectionFormSet,
)
from killay.archives.models import Archive, Category, Collection
from killay.archives.services import get_archive_related_field_data


class ArchivesMainView(FormSetAdminView):
    main_title = ArchivesViewConstants.MAIN_TITLE
    second_title = gettext_lazy("Archives")
    formset_class = ArchiveFormSet
    reverse_url = "admin:archives"
    update_url = "admin:archive_update"
    delete_url = "admin:archive_delete"
    create_url = "admin:archive_create"
    extra_links = [
        {"view": "admin:collection_list", "name": gettext_lazy("Collections")}
    ]


admin_archives_main_view = ArchivesMainView.as_view()


class ArchiveCreateView(CreateAdminView):
    form_class = ArchiveForm
    main_title = ArchivesViewConstants.MAIN_TITLE
    second_title = gettext_lazy("Create Archive")
    breadcrumb = ([{"view": "admin:archives", "name": gettext_lazy("Archives")}],)
    reverse_url = "admin:archive_update"


admin_archive_create_view = ArchiveCreateView.as_view()


class ArchiveUpdateView(UpdateAdminView):
    form_class = ArchiveForm
    main_title = ArchivesViewConstants.MAIN_TITLE
    reverse_url = "admin:archive_update"
    delete_url = "admin:archive_delete"
    breadcrumb = [{"view": "admin:archives", "name": gettext_lazy("Archives")}]

    def get_extra_data(self) -> list:
        return get_archive_related_field_data(archive_id=self.object.id)


admin_archive_update_view = ArchiveUpdateView.as_view()


class ArchiveDeleteView(DeleteAdminView):
    form_class = ArchiveForm
    main_title = ArchivesViewConstants.MAIN_TITLE
    reverse_url = "admin:archives"
    breadcrumb = [{"view": "admin:archives", "name": gettext_lazy("Archives")}]

    def get_extra_data(self) -> list:
        return get_archive_related_field_data(archive_id=self.object.id)


admin_archive_delete_view = ArchiveDeleteView.as_view()


class CollectionListView(FormSetAdminView):
    main_title = ArchivesViewConstants.MAIN_TITLE
    second_title = gettext_lazy("Collections")
    formset_class = CollectionFormSet
    reverse_url = "admin:collections"
    update_url = "admin:collection_update"
    delete_url = "admin:collection_delete"
    create_url = "admin:collection_create"
    breadcrumb = [{"view": "admin:archives", "name": gettext_lazy("Archives")}]
    extra_links = [{"view": "admin:category_list", "name": gettext_lazy("Categories")}]
    filters = {"archive": "archive__slug"}

    def get_filter_options(self) -> dict:
        archive_options = {}
        for slug, name in self.model.objects.all().values_list(
            "archive__slug", "archive__name"
        ):
            if slug not in archive_options:
                archive_options[slug] = name
        archive_options = [
            {"name": name, "value": slug} for slug, name in archive_options.items()
        ]
        return {"archive": archive_options}


admin_collection_list_view = CollectionListView.as_view()


class CollectionCreateView(AdminRequiredMixin, CreateView):
    form_class = CollectionForm
    template_name = "admin/generic_form.html"
    extra_context = {
        "form_title": gettext_lazy("Create Collection"),
        "main_title": ArchivesViewConstants.MAIN_TITLE,
        "breadcrumb": [
            {"view": "admin:archives", "name": gettext_lazy("Archives")},
            {"view": "admin:collection_list", "name": gettext_lazy("Collections")},
        ],
    }

    def get_success_url(self):
        messages.info(self.request, gettext(f'Collection "{self.object}" was created'))
        return reverse("admin:collection_update", kwargs={"slug": self.object.slug})


admin_collection_create_view = CollectionCreateView.as_view()


class CollectionUpdateView(AdminUpdateMixin):
    model = Collection
    form_class = CollectionForm
    reverse_success_url = "admin:collection_update"
    extra_context = {
        "main_title": ArchivesViewConstants.MAIN_TITLE,
        "breadcrumb": [
            {"view": "admin:archives", "name": gettext_lazy("Archives")},
            {"view": "admin:collection_list", "name": gettext_lazy("Collections")},
        ],
    }


admin_collection_update_view = CollectionUpdateView.as_view()


class CategoryListView(FormSetMixin):
    model = Category
    formset_class = CategoryFormSet
    reverse_url = "admin:category_list"
    title = gettext_lazy("Categories")
    create_reverse_link = "admin:category_create"
    extra_context = {
        "main_title": ArchivesViewConstants.MAIN_TITLE,
        "breadcrumb": [{"view": "admin:archives", "name": gettext_lazy("Archives")}],
        "extra_links": [
            {"view": "admin:collection_list", "name": gettext_lazy("Collections")}
        ],
    }


admin_category_list_view = CategoryListView.as_view()


class CategoryCreateView(AdminRequiredMixin, CreateView):
    form_class = CategoryFormSet
    template_name = "admin/generic_form.html"
    extra_context = {
        "form_title": gettext_lazy("Create Category"),
        "main_title": ArchivesViewConstants.MAIN_TITLE,
        "breadcrumb": [
            {"view": "admin:archives", "name": gettext_lazy("Archives")},
            {"view": "admin:category_list", "name": gettext_lazy("Categories")},
        ],
    }

    def get_success_url(self):
        messages.info(self.request, gettext(f'Category "{self.object}" was created'))
        return reverse("admin:category_update", kwargs={"slug": self.object.slug})


admin_category_create_view = CategoryCreateView.as_view()


class CategoryUpdateView(AdminUpdateMixin):
    model = Category
    form_class = CategoryForm
    reverse_success_url = "admin:category_update"
    extra_context = {
        "main_title": ArchivesViewConstants.MAIN_TITLE,
        "breadcrumb": [
            {"view": "admin:archives", "name": gettext_lazy("Archives")},
            {"view": "admin:category_list", "name": gettext_lazy("Categories")},
        ],
    }


admin_category_update_view = CategoryUpdateView.as_view()
