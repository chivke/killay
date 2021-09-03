from django.contrib import messages
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse, reverse_lazy

from cmpirque.admin.mixins import AdminRequiredMixin
from cmpirque.users.models import User
from cmpirque.users.forms import UserCreationForm, UserUpdateForm
from django.utils.translation import gettext


class UserCreateView(AdminRequiredMixin, CreateView):
    form_class = UserCreationForm
    template_name = "admin/users/user_create.html"

    def get_success_url(self):
        messages.info(self.request, gettext(f"User {self.object.username} was created"))
        return reverse("admin:users_update", kwargs={"slug": self.object.username})


user_create_view = UserCreateView.as_view()


class UserUpdateView(AdminRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "admin/users/user_update.html"
    slug_field = "username"

    def get_success_url(self):
        messages.info(self.request, gettext(f"User {self.object.username} was updated"))
        return reverse("admin:users_update", kwargs={"slug": self.object.username})


user_update_view = UserUpdateView.as_view()


class UserListView(AdminRequiredMixin, ListView):
    model = User
    template_name = "admin/users/user_list.html"


user_list_view = UserListView.as_view()


class UserDeleteView(AdminRequiredMixin, DeleteView):
    model = User
    template_name = "admin/users/user_delete.html"
    slug_field = "username"

    def get_success_url(self):
        messages.warning(
            self.request, gettext(f"User {self.object.username} was deleted")
        )
        return reverse("admin:users_list")


user_delete_view = UserDeleteView.as_view()
