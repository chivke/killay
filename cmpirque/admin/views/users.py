from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse, reverse_lazy

from cmpirque.admin.mixins import (
    AdminDeleteMixin,
    AdminListMixin,
    AdminRequiredMixin,
    AdminUpdateMixin,
)
from cmpirque.users.models import User
from cmpirque.users.forms import UserCreationForm, UserUpdateForm
from django.utils.translation import gettext, gettext_lazy


class UserCreateView(AdminRequiredMixin, CreateView):
    form_class = UserCreationForm
    template_name = "admin/generic_form.html"
    extra_context = {"form_title": gettext_lazy("Create User")}

    def get_success_url(self):
        messages.info(self.request, gettext(f"User {self.object.username} was created"))
        return reverse("admin:users_update", kwargs={"slug": self.object.username})


user_create_view = UserCreateView.as_view()


class UserUpdateView(AdminUpdateMixin):
    model = User
    form_class = UserUpdateForm
    slug_field = "username"
    read_only_fields = ["date_joined", "last_login"]
    reverse_success_url = "admin:users_update"


user_update_view = UserUpdateView.as_view()


class UserListView(AdminListMixin):
    model = User
    slug_key = "username"
    list_title = gettext_lazy("Users Administration")
    list_fields = ["is_superuser", "username", "email"]
    action_links = {
        "create_object": {
            "name": gettext_lazy("Create"),
            "link": reverse_lazy("admin:users_create"),
        }
    }
    object_action_links = {
        "update_object": {"name": gettext_lazy("Update"), "link": "admin:users_update"},
        "delete_object": {"name": gettext_lazy("Delete"), "link": "admin:users_delete"},
    }


user_list_view = UserListView.as_view()


class UserDeleteView(AdminDeleteMixin):
    model = User
    slug_field = "username"
    reverse_success_url = "admin:users_list"


user_delete_view = UserDeleteView.as_view()
