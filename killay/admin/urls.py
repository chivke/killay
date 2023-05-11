from django.urls import path

from killay.admin.views.configuration import admin_configuration_view

from killay.admin.views import archives as archives_views
from killay.admin.views import videos as videos_views
from killay.admin.views import users as users_views
from killay.admin.views import pages as pages_views


app_name = "admin"


urlpatterns = [path("", view=admin_configuration_view, name="configuration")]

# Video Views

urlpatterns += [
    path("archives/", view=archives_views.admin_archives_main_view, name="archives"),
    path(
        "archives/archive/~create/",
        view=archives_views.admin_archive_create_view,
        name="archive_create",
    ),
    path(
        "archives/archive/<str:slug>/delete",
        view=archives_views.admin_archive_delete_view,
        name="archive_delete",
    ),
    path(
        "archives/archive/<str:slug>/",
        view=archives_views.admin_archive_update_view,
        name="archive_update",
    ),
    path(
        "archives/collections/",
        view=archives_views.admin_collection_list_view,
        name="collection_list",
    ),
    path(
        "archives/collections/~create/",
        view=archives_views.admin_collection_create_view,
        name="collection_create",
    ),
    path(
        "archives/collections/<str:slug>/",
        view=archives_views.admin_collection_update_view,
        name="collection_update",
    ),
    path(
        "archives/categories/",
        view=archives_views.admin_category_list_view,
        name="category_list",
    ),
    path(
        "archives/categories/~create/",
        view=archives_views.admin_category_create_view,
        name="category_create",
    ),
    path(
        "archives/categories/<str:slug>/",
        view=archives_views.admin_category_update_view,
        name="category_update",
    ),
]


urlpatterns += [
    path("videos/~create/", view=videos_views.video_create_view, name="videos_create"),
    path(
        "videos/~collections/",
        view=videos_views.video_collections_view,
        name="videos_collections",
    ),
    path(
        "videos/~collections/create/",
        view=videos_views.video_collection_create_view,
        name="videos_collection_create",
    ),
    path(
        "videos/~collections/<str:slug>/",
        view=videos_views.video_collection_update_view,
        name="videos_collection_update",
    ),
    path(
        "videos/~categories/",
        view=videos_views.video_categories_view,
        name="videos_categories",
    ),
    path(
        "videos/~categories/create/",
        view=videos_views.video_category_create_view,
        name="videos_category_create",
    ),
    path(
        "videos/~categories/c/<str:collection>/<str:slug>/",
        view=videos_views.video_category_update_view,
        name="videos_category_update",
    ),
    path("videos/~people/", view=videos_views.video_people_view, name="videos_people"),
    path(
        "videos/~people/create/",
        view=videos_views.video_person_create_view,
        name="videos_person_create",
    ),
    path(
        "videos/~people/c/<str:collection>/<str:slug>/",
        view=videos_views.video_person_update_view,
        name="videos_person_update",
    ),
    path(
        "videos/~keywords/",
        view=videos_views.video_keywords_view,
        name="videos_keywords",
    ),
    path(
        "videos/~keywords/create/",
        view=videos_views.video_keyword_create_view,
        name="videos_keyword_create",
    ),
    path(
        "videos/~keywords/c/<str:collection>/<str:slug>/",
        view=videos_views.video_keyword_update_view,
        name="videos_keyword_update",
    ),
    path(
        "videos/c/<str:collection>/<str:slug>/~sequences/create/",
        view=videos_views.video_sequences_create_view,
        name="videos_sequences_create",
    ),
    path(
        "videos/c/<str:collection>/<str:slug>/~sequences/",
        view=videos_views.video_sequences_list_view,
        name="videos_sequences_list",
    ),
    path(
        "videos/c/<str:collection>/<str:slug>/~categorization/",
        view=videos_views.video_categorization_view,
        name="videos_categorization",
    ),
    path(
        "videos/c/<str:collection>/<str:slug>/~delete/",
        view=videos_views.video_delete_view,
        name="videos_delete",
    ),
    path(
        "videos/c/<str:collection>/<str:slug>/~update/",
        view=videos_views.video_update_view,
        name="videos_update",
    ),
]

# Users Views

urlpatterns += [
    path("users/", view=users_views.user_list_view, name="users_list"),
    path("users/~create/", view=users_views.user_create_view, name="users_create"),
    path("users/<str:slug>/", view=users_views.user_update_view, name="users_update"),
    path(
        "users/<str:slug>/~delete/",
        view=users_views.user_delete_view,
        name="users_delete",
    ),
]

# Pages Views

urlpatterns += [
    path("pages/", view=pages_views.page_list_view, name="pages_list"),
    path("pages/~create/", view=pages_views.page_create_view, name="pages_create"),
    path("pages/<str:slug>/", view=pages_views.page_update_view, name="pages_update"),
    path(
        "pages/<str:slug>/~delete/",
        view=pages_views.page_delete_view,
        name="pages_delete",
    ),
]
