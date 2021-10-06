from django.urls import path

from killay.videos import views


app_name = "videos"


urlpatterns = [
    path("search/", view=views.video_search_list_view, name="search"),
    path("c/<str:slug>/", view=views.video_collection_list_view, name="collection"),
    path(
        "c/<str:collection>/c/<str:slug>/",
        view=views.video_category_list_view,
        name="category",
    ),
    path(
        "c/<str:collection>/p/<str:slug>/",
        view=views.video_person_list_view,
        name="person",
    ),
    path(
        "c/<str:collection>/k/<str:slug>/",
        view=views.video_keyword_list_view,
        name="keyword",
    ),
    path(
        "c/<str:collection>/v/<str:slug>/", view=views.video_detail_view, name="detail"
    ),
]
