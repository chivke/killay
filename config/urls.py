from django.conf import settings
from django.contrib import admin 
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.conf.urls.static import static

from cmpirque.pages.views import home_page_view


urlpatterns = [
    path('', view=home_page_view, name="home"),
    path('pages/', include('cmpirque.pages.urls', namespace='pages')),
    path('users/', include('cmpirque.users.urls', namespace='users')),
    path('videos/', include('cmpirque.videos.urls', namespace='videos')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# debug toolbar

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [path('__debug__/', include(
            debug_toolbar.urls))] + urlpatterns
