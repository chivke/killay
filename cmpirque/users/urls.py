from django.urls import path

from django.contrib.auth import views as auth_views

from cmpirque.users.views import (
    user_login_view,
    user_redirect_view,
    user_update_view,
    user_password_change_view,
    user_password_reset_view,
    user_password_reset_confirm_view,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    # path("me/", view=user_detail_view, name="me-detail"),
    path("~update/", view=user_update_view, name="update"),
    # path("auth/", include("django.contrib.auth.urls")),
    path("~login/", view=user_login_view, name="login"),
    path("~logout/", view=auth_views.LogoutView.as_view(), name="logout"),
    path("~password_change/", view=user_password_change_view, name="password_change"),
    path("~password_reset/", view=user_password_reset_view, name="password_reset"),
    path(
        "~reset/<uidb64>/<token>/",
        user_password_reset_confirm_view,
        name="password_reset_confirm",
    ),
]
