from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import RedirectView, UpdateView
from django.utils.translation import gettext

from killay.users.forms import UserChangeForm

User = get_user_model()


class MySelfMixin(LoginRequiredMixin):
    model = User

    def get_object(self):
        self.kwargs["pk"] = self.request.user.pk
        return super().get_object()


class UserUpdateView(MySelfMixin, UpdateView):
    model = User
    form_class = UserChangeForm

    def get_success_url(self):
        return reverse("users:update")

    def form_valid(self, *args, **kwargs):
        messages.info(self.request, gettext(f"User {self.object.username} updated"))
        return super().form_valid(*args, **kwargs)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:update")


user_redirect_view = UserRedirectView.as_view()


class UserLoginView(auth_views.LoginView):
    redirect_authenticated_user = True
    template_name = "users/login.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.pop("site")
        return context


user_login_view = UserLoginView.as_view()


class UserPasswordResetView(auth_views.PasswordResetView):
    success_url = reverse_lazy("users:password_reset")
    template_name = "users/password_reset_form.html"

    def form_valid(self, *args, **kwargs):
        messages.info(
            self.request, gettext("We have sent you an e-mail with your reset link")
        )
        return super().form_valid(*args, **kwargs)


user_password_reset_view = UserPasswordResetView.as_view()


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    success_url = reverse_lazy("users:login")
    template_name = "users/password_reset_confirm.html"

    def form_valid(self, *args, **kwargs):
        messages.info(self.request, gettext("Your password is now changed."))
        return super().form_valid(*args, **kwargs)


user_password_reset_confirm_view = UserPasswordResetConfirmView.as_view()


class UserPasswordChangeView(auth_views.PasswordChangeView):
    success_url = reverse_lazy("users:update")
    template_name = "users/password_change_form.html"

    def form_valid(self, *args, **kwargs):
        messages.info(self.request, gettext("Your password is now changed."))
        return super().form_valid(*args, **kwargs)


user_password_change_view = UserPasswordChangeView.as_view()
