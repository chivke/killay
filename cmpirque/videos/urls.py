from django.urls import path


from cmpirque.videos.views.video_public import video_detail_view, video_list_view
from cmpirque.videos.views.video_admin import (
    video_categories_view,
    video_categorization,
    video_create_view,
    video_delete_view,
    video_keywords_view,
    video_people_view,
    video_update_view,
    video_sequences_list,
)

app_name = "videos"
urlpatterns = [
    path("", view=video_list_view, name="list"),
    path("~create/", view=video_create_view, name="create"),
    path("~categories/", view=video_categories_view, name="categories"),
    path("~people/", view=video_people_view, name="people"),
    path("~keywords/", view=video_keywords_view, name="keywords"),
    path("<str:slug>/~sequences/", view=video_sequences_list, name="sequences_list"),
    path(
        "<str:slug>/~categorization/", view=video_categorization, name="categorization"
    ),
    path("<str:slug>/~delete/", view=video_delete_view, name="delete"),
    path("<str:slug>/~update/", view=video_update_view, name="update"),
    path("<str:slug>/", view=video_detail_view, name="detail"),
]
