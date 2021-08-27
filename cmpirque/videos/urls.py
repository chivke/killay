from django.urls import path


from cmpirque.videos.views import (
    video_category_list_view,
    video_detail_view,
    video_keyword_list_view,
    video_list_view,
    video_person_list_view,
)

app_name = "videos"
urlpatterns = [
    path("", view=video_list_view, name="list"),
    path("category/<str:slug>/", view=video_category_list_view, name="category-list"),
    path("person/<str:slug>/", view=video_person_list_view, name="person-list"),
    path("keyword/<str:slug>/", view=video_keyword_list_view, name="keyword-list"),
    path("<str:slug>/", view=video_detail_view, name="detail"),
]
