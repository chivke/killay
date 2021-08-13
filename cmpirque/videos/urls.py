from django.urls import path


from cmpirque.videos.views import (
    video_detail_view,
)

app_name = 'videos'
urlpatterns = [
    path('<str:slug>/', view=video_detail_view, name='detail'),
]
