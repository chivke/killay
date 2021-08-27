from django.urls import path

from cmpirque.admin.views.configuration import admin_configuration_view

from cmpirque.admin.views.videos import (
    video_categories_view,
    video_categorization,
    video_create_view,
    video_delete_view,
    video_keywords_view,
    video_people_view,
    video_update_view,
    video_sequences_list,
)


app_name = "admin"
urlpatterns = [
    path("", view=admin_configuration_view, name="configuration"),
    path("videos/~create/", view=video_create_view, name="videos_create"),
    path("videos/~categories/", view=video_categories_view, name="videos_categories"),
    path("videos/~people/", view=video_people_view, name="videos_people"),
    path("videos/~keywords/", view=video_keywords_view, name="videos_keywords"),
    path(
        "videos/<str:slug>/~sequences/",
        view=video_sequences_list,
        name="videos_sequences_list",
    ),
    path(
        "videos/<str:slug>/~categorization/",
        view=video_categorization,
        name="videos_categorization",
    ),
    path("videos/<str:slug>/~delete/", view=video_delete_view, name="videos_delete"),
    path("videos/<str:slug>/~update/", view=video_update_view, name="videos_update"),
]
