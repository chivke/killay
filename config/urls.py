from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views import defaults as default_views

from killay.pages.views import home_page_view


urlpatterns = [
    path("", view=home_page_view, name="home"),
    path("admin/", include("killay.admin.urls", namespace="admin")),
    path("pages/", include("killay.pages.urls", namespace="pages")),
    path("users/", include("killay.users.urls", namespace="users")),
    path("videos/", include("killay.videos.urls", namespace="videos")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# debug toolbar

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
