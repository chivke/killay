from killay.admin.lib.constants import UserManagerConstants
from killay.admin.views.mixins import (
    CreateAdminView,
    DeleteAdminView,
    FormSetAdminView,
    UpdateAdminView,
)
from killay.users.forms import UserCreationForm, UserUpdateForm, UserFormSet


class UserListView(FormSetAdminView):
    main_title = UserManagerConstants.MAIN_TITLE
    formset_class = UserFormSet
    reverse_url = UserManagerConstants.PATTERN_LIST
    update_url = UserManagerConstants.PATTERN_UPDATE
    delete_url = UserManagerConstants.PATTERN_DELETE
    create_url = UserManagerConstants.PATTERN_CREATE
    breadcrumb = []
    extra_links = []


user_list_view = UserListView.as_view()


_common_bredcrumb = [
    {
        "name": UserManagerConstants.LIST_LABEL,
        "view": UserManagerConstants.PATTERN_LIST,
    },
]


class UserCreateView(CreateAdminView):
    main_title = UserManagerConstants.MAIN_TITLE
    form_class = UserCreationForm
    reverse_url = UserManagerConstants.PATTERN_UPDATE
    breadcrumb = [*_common_bredcrumb, {"name": "New User"}]
    extra_links = []
    name_field = "username"


user_create_view = UserCreateView.as_view()


class UserUpdateView(UpdateAdminView):
    main_title = UserManagerConstants.MAIN_TITLE
    form_class = UserUpdateForm
    reverse_url = UserManagerConstants.PATTERN_UPDATE
    delete_url = UserManagerConstants.PATTERN_DELETE
    extra_links = []
    name_field = "username"

    def get_breadcrumb(self) -> list:
        return [*_common_bredcrumb, {"name": self.object.username}]


user_update_view = UserUpdateView.as_view()


class UserDeleteView(DeleteAdminView):
    main_title = UserManagerConstants.MAIN_TITLE
    form_class = UserUpdateForm
    reverse_url = UserManagerConstants.PATTERN_LIST
    delete_url = UserManagerConstants.PATTERN_UPDATE
    extra_links = []
    name_field = "username"

    def get_breadcrumb(self) -> list:
        return [*_common_bredcrumb, {"name": self.object.username}]


user_delete_view = UserDeleteView.as_view()
