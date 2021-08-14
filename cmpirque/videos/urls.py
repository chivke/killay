from django.urls import path


from cmpirque.videos.views.video_public import video_detail_view
from cmpirque.videos.views.video_admin import (
    video_delete_view,
    video_create_view,
    video_update_view,
)

app_name = 'videos'
urlpatterns = [
    path('~create/', view=video_create_view, name='create'),
    path('<str:slug>/~delete/', view=video_delete_view, name='delete'),
    path('<str:slug>/~update/', view=video_update_view, name='update'),
    path('<str:slug>/', view=video_detail_view, name='detail'),
]
