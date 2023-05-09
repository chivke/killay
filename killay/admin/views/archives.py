from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse
from django.utils.translation import gettext, gettext_lazy

from killay.admin.lib.constants import ArchivesViewConstants
from killay.admin.mixins import AdminRequiredMixin, AdminUpdateMixin, FormSetMixin
from killay.admin.forms import (
    ArchiveForm,
    ArchiveFormSet,
    CategoryForm,
    CategoryFormSet,
    CollectionForm,
    CollectionFormSet,
)
from killay.archives.models import Archive, Category, Collection


class ArchivesMainView(FormSetMixin):
    model = Archive
    formset_class = ArchiveFormSet
    reverse_url = "admin:archives"
    title = gettext_lazy("Archives")
    create_reverse_link = "admin:archive_create"
    extra_context = {
        "main_title": ArchivesViewConstants.MAIN_TITLE,
        "breadcrumb": [{"view": "", "name": ""}],
        "extra_links": [
            {"view": "admin:collection_list", "name": gettext_lazy("Collections")}
        ],
    }


admin_archives_main_view = ArchivesMainView.as_view()


class ArchiveCreateView(AdminRequiredMixin, CreateView):
    form_class = ArchiveForm
    template_name = "admin/generic_form.html"
    extra_context = {
        "form_title": gettext_lazy("Create Archive"),
        "main_title": ArchivesViewConstants.MAIN_TITLE,
        "breadcrumb": [{"view": "admin:archives", "name": gettext_lazy("Archives")}],
    }

    def get_success_url(self):
        messages.info(self.request, gettext(f'Archive "{self.object}" was created'))
        return reverse("admin:archive_update", kwargs={"slug": self.object.slug})


admin_archive_create_view = ArchiveCreateView.as_view()


class ArchiveUpdateView(AdminUpdateMixin):
    model = Archive
    form_class = ArchiveForm
    reverse_success_url = "admin:archive_update"
    extra_context = {
        "main_title": ArchivesViewConstants.MAIN_TITLE,
        "breadcrumb": [{"view": "admin:archives", "name": gettext_lazy("Archives")}],
    }


admin_archive_update_view = ArchiveUpdateView.as_view()


class CollectionListView(FormSetMixin):
    model = Collection
    formset_class = CollectionFormSet
    reverse_url = "admin:collections"
    title = gettext_lazy("Collections")
    create_reverse_link = "admin:collection_create"
    extra_context = {
        "main_title": ArchivesViewConstants.MAIN_TITLE,
        "breadcrumb": [{"view": "admin:archives", "name": gettext_lazy("Archives")}],
        "extra_links": [
            {"view": "admin:category_list", "name": gettext_lazy("Categories")}
        ],
    }
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
