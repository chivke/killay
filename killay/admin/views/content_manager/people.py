from killay.admin.lib.constants import ContentManagerConstants
from killay.admin.views.content_manager import get_content_manager_extra_links
from killay.admin.views.mixins import (
    CreateAdminView,
    DeleteAdminView,
    FormSetAdminView,
    UpdateAdminView,
)
from killay.admin.forms import (
    PersonForm,
    PersonFormSet,
)


PERSON_SLUG = ContentManagerConstants.SLUG_PERSON
PERSON_EXTRA_LINKS = get_content_manager_extra_links(view_slug=PERSON_SLUG)


class PersonListView(FormSetAdminView):
    main_title = ContentManagerConstants.MAIN_TITLE
    second_title = ContentManagerConstants.VIEWS_SECOND_TITLE[PERSON_SLUG]
    description = ContentManagerConstants.DESCRIPTION_PERSON
    formset_class = PersonFormSet
    reverse_url = ContentManagerConstants.VIEWS_LIST[PERSON_SLUG]
    update_url = ContentManagerConstants.VIEWS_UPDATE[PERSON_SLUG]
    delete_url = ContentManagerConstants.VIEWS_DELETE[PERSON_SLUG]
    create_url = ContentManagerConstants.VIEWS_CREATE[PERSON_SLUG]

    extra_links = PERSON_EXTRA_LINKS


admin_person_list_view = PersonListView.as_view()


_common_bredcrumb = [
    ContentManagerConstants.DICT_LINK[PERSON_SLUG]["list"],
]


class PersonCreateView(CreateAdminView):
    main_title = ContentManagerConstants.MAIN_TITLE
    description = ContentManagerConstants.DESCRIPTION_PERSON
    form_class = PersonForm
    reverse_url = ContentManagerConstants.VIEWS_UPDATE[PERSON_SLUG]
    breadcrumb = [*_common_bredcrumb, {"name": "New Person"}]
    extra_links = PERSON_EXTRA_LINKS


admin_person_create_view = PersonCreateView.as_view()


class PersonBreadcrumMixin:
    def get_breadcrumb(self) -> list:
        return [*_common_bredcrumb, {"name": self.object.name}]


class PersonUpdateView(PersonBreadcrumMixin, UpdateAdminView):
    main_title = ContentManagerConstants.MAIN_TITLE
    description = ContentManagerConstants.DESCRIPTION_PERSON
    form_class = PersonForm
    reverse_url = ContentManagerConstants.VIEWS_UPDATE[PERSON_SLUG]
    delete_url = ContentManagerConstants.VIEWS_DELETE[PERSON_SLUG]
    extra_links = PERSON_EXTRA_LINKS


admin_person_update_view = PersonUpdateView.as_view()


class PersonDeleteView(PersonBreadcrumMixin, DeleteAdminView):
    main_title = ContentManagerConstants.MAIN_TITLE
    description = ContentManagerConstants.DESCRIPTION_PERSON
    form_class = PersonForm
    reverse_url = ContentManagerConstants.VIEWS_LIST[PERSON_SLUG]
    delete_url = ContentManagerConstants.VIEWS_UPDATE[PERSON_SLUG]
    extra_links = PERSON_EXTRA_LINKS


admin_person_delete_view = PersonDeleteView.as_view()
