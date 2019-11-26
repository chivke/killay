from django.conf.urls import url
from . import views

# ..
# Main Views for Video Log
# ---------------------------------------
# ..

app_name = 'videolog'
urlpatterns = [
    #url('^$', views.InicioEntriesList.as_view(), name='inicio'),
    url('^todo$', views.EntriesList.as_view(), name='entrieslist'),
    url(r'^v/(?P<slug>[A-Za-z0-9-_]+)/$', views.EntryDetail.as_view(), name='entrydetail'),
    url(r'^c/(?P<category>[A-Za-z0-9-_]+)/$', views.CategoryList.as_view(), name='catentries'),
    url(r'^p/(?P<people>[A-Za-z0-9-_]+)/$', views.PeopleList.as_view(), name='popentries'),
    url(r'^k/(?P<keyword>[A-Za-z0-9-_]+)/$', views.KeywordList.as_view(), name='keyentries'),
    url(r'^buscar/', views.SearchEntries.as_view(), name='searchentries'),
]
