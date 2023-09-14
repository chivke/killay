from killay.admin.lib.constants import ContentManagerConstants
from killay.admin.views.content_manager import get_content_manager_extra_links
from killay.admin.views.mixins import (
    CreateAdminView,
    DeleteAdminView,
    FormSetAdminView,
    UpdateAdminView,
)
from killay.admin.forms import (
    KeywordForm,
    KeywordFormSet,
)


KEYWORD_SLUG = ContentManagerConstants.SLUG_KEYWORD
KEYWORD_EXTRA_LINKS = get_content_manager_extra_links(view_slug=KEYWORD_SLUG)


class KeywordListView(FormSetAdminView):
    main_title = ContentManagerConstants.MAIN_TITLE
    second_title = ContentManagerConstants.VIEWS_SECOND_TITLE[KEYWORD_SLUG]
    description = ContentManagerConstants.DESCRIPTION_KEYWORD
    formset_class = KeywordFormSet
    reverse_url = ContentManagerConstants.VIEWS_LIST[KEYWORD_SLUG]
    update_url = ContentManagerConstants.VIEWS_UPDATE[KEYWORD_SLUG]
    delete_url = ContentManagerConstants.VIEWS_DELETE[KEYWORD_SLUG]
    create_url = ContentManagerConstants.VIEWS_CREATE[KEYWORD_SLUG]
    extra_links = KEYWORD_EXTRA_LINKS


admin_keyword_list_view = KeywordListView.as_view()


_common_bredcrumb = [
    ContentManagerConstants.DICT_LINK[KEYWORD_SLUG]["list"],
]


class KeywordCreateView(CreateAdminView):
    main_title = ContentManagerConstants.MAIN_TITLE
    description = ContentManagerConstants.DESCRIPTION_KEYWORD
    form_class = KeywordForm
    reverse_url = ContentManagerConstants.VIEWS_UPDATE[KEYWORD_SLUG]
    breadcrumb = [*_common_bredcrumb, {"name": "New Keyword"}]
    extra_links = KEYWORD_EXTRA_LINKS


admin_keyword_create_view = KeywordCreateView.as_view()


class KeywordBreadcrumMixin:
    def get_breadcrumb(self) -> list:
        return [*_common_bredcrumb, {"name": self.object.name}]


class KeywordUpdateView(KeywordBreadcrumMixin, UpdateAdminView):
    main_title = ContentManagerConstants.MAIN_TITLE
    description = ContentManagerConstants.DESCRIPTION_KEYWORD
    form_class = KeywordForm
    reverse_url = ContentManagerConstants.VIEWS_UPDATE[KEYWORD_SLUG]
    delete_url = ContentManagerConstants.VIEWS_DELETE[KEYWORD_SLUG]
    extra_links = KEYWORD_EXTRA_LINKS


admin_keyword_update_view = KeywordUpdateView.as_view()


class KeywordDeleteView(KeywordBreadcrumMixin, DeleteAdminView):
    main_title = ContentManagerConstants.MAIN_TITLE
    description = ContentManagerConstants.DESCRIPTION_KEYWORD
    form_class = KeywordForm
    reverse_url = ContentManagerConstants.VIEWS_LIST[KEYWORD_SLUG]
    extra_links = KEYWORD_EXTRA_LINKS
    delete_url = ContentManagerConstants.VIEWS_UPDATE[KEYWORD_SLUG]


admin_keyword_delete_view = KeywordDeleteView.as_view()
