from django.urls import path

from killay.videos import views

# from killay.videos.views import (
#     video_category_list_view,
#     video_collection_list_view,
#     video_detail_view,
#     video_keyword_list_view,
#     video_list_view,
#     video_person_list_view,
#     video_search_list_view,
# )

app_name = "videos"
# urlpatterns = [
#     # path("", view=video_list_view, name="list"),
#     path("search/", view=video_search_list_view, name="search"),
#     path(
#         "collection/<str:slug>/",
#         view=video_collection_list_view,
#         name="collection-list",
#     ),
#     path("category/<str:slug>/", view=video_category_list_view, name="category-list"),
#     path("person/<str:slug>/", view=video_person_list_view, name="person-list"),
#     path("keyword/<str:slug>/", view=video_keyword_list_view, name="keyword-list"),
#     path("<str:slug>/", view=video_detail_view, name="detail"),
# ]

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
    # path("<str:slug>/", view=video_detail_view, name="detail"),
]
