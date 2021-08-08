from django.urls import path


from cmpirque.pages.views import (
    page_detail_view,
)

app_name = 'pages'
urlpatterns = [
    path('<str:slug>/', view=page_detail_view, name='detail'),
]
