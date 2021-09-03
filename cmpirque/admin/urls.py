from django.urls import path

from cmpirque.admin.views.configuration import admin_configuration_view

from cmpirque.admin.views import videos as videos_views
from cmpirque.admin.views import users as users_views


app_name = "admin"


urlpatterns = [path("", view=admin_configuration_view, name="configuration")]

# Video Views

urlpatterns += [
    path("videos/~create/", view=videos_views.video_create_view, name="videos_create"),
    path(
        "videos/~categories/",
        view=videos_views.video_categories_view,
        name="videos_categories",
    ),
    path("videos/~people/", view=videos_views.video_people_view, name="videos_people"),
    path(
        "videos/~keywords/",
        view=videos_views.video_keywords_view,
        name="videos_keywords",
    ),
    path(
        "videos/<str:slug>/~sequences/",
        view=videos_views.video_sequences_list,
        name="videos_sequences_list",
    ),
    path(
        "videos/<str:slug>/~categorization/",
        view=videos_views.video_categorization,
        name="videos_categorization",
    ),
    path(
        "videos/<str:slug>/~delete/",
        view=videos_views.video_delete_view,
        name="videos_delete",
    ),
    path(
        "videos/<str:slug>/~update/",
        view=videos_views.video_update_view,
        name="videos_update",
    ),
]

# Users Views

urlpatterns += [
    path("users/", view=users_views.user_list_view, name="users_list"),
    path("users/~create/", view=users_views.user_create_view, name="users_create"),
    path("users/<str:slug>/", view=users_views.user_update_view, name="users_update"),
    path(
        "users/<str:slug>/~delete/",
        view=users_views.user_delete_view,
        name="users_delete",
    ),
]
