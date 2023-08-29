from killay.admin.forms import PageForm, PageFormSet
from killay.admin.lib.constants import PageManagerConstants
from killay.admin.views.mixins import (
    CreateAdminView,
    DeleteAdminView,
    FormSetAdminView,
    UpdateAdminView,
)


class PageListView(FormSetAdminView):
    main_title = PageManagerConstants.MAIN_TITLE
    formset_class = PageFormSet
    reverse_url = PageManagerConstants.PATTERN_LIST
    update_url = PageManagerConstants.PATTERN_UPDATE
    delete_url = PageManagerConstants.PATTERN_DELETE
    create_url = PageManagerConstants.PATTERN_CREATE
    breadcrumb = []
    extra_links = []


page_list_view = PageListView.as_view()


_common_bredcrumb = [
    {
        "name": PageManagerConstants.PAGE_LIST_LABEL,
        "view": PageManagerConstants.PATTERN_LIST,
    },
]


class PageCreateView(CreateAdminView):
    main_title = PageManagerConstants.MAIN_TITLE
    form_class = PageForm
    reverse_url = PageManagerConstants.PATTERN_UPDATE
    breadcrumb = [*_common_bredcrumb, {"name": "New Page"}]
    extra_links = []
    name_field = "title"
    html_fields = ["body"]


page_create_view = PageCreateView.as_view()


class PageUpdateView(UpdateAdminView):
    main_title = PageManagerConstants.MAIN_TITLE
    form_class = PageForm
    reverse_url = PageManagerConstants.PATTERN_UPDATE
    delete_url = PageManagerConstants.PATTERN_DELETE
    extra_links = []
    name_field = "title"
    html_fields = ["body"]

    def get_breadcrumb(self) -> list:
        return [*_common_bredcrumb, {"name": self.object.title}]


page_update_view = PageUpdateView.as_view()


class PageDeleteView(DeleteAdminView):
    main_title = PageManagerConstants.MAIN_TITLE
    form_class = PageForm
    reverse_url = PageManagerConstants.PATTERN_LIST
    delete_url = PageManagerConstants.PATTERN_UPDATE
    extra_links = []
    name_field = "title"

    def get_breadcrumb(self) -> list:
        return [*_common_bredcrumb, {"name": self.object.title}]


page_delete_view = PageDeleteView.as_view()
