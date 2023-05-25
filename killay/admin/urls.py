from django.urls import path
from django.views.generic.base import RedirectView

from killay.admin.views.configuration import admin_configuration_view
from killay.admin.views.content_manager.archives import (
    admin_archive_list_view,
    admin_archive_create_view,
    admin_archive_delete_view,
    admin_archive_update_view,
)
from killay.admin.views.content_manager.collections import (
    admin_collection_list_view,
    admin_collection_create_view,
    admin_collection_delete_view,
    admin_collection_update_view,
)
from killay.admin.views.content_manager.categories import (
    admin_category_list_view,
    admin_category_create_view,
    admin_category_delete_view,
    admin_category_update_view,
)
from killay.admin.views.content_manager.people import (
    admin_person_list_view,
    admin_person_create_view,
    admin_person_delete_view,
    admin_person_update_view,
)
from killay.admin.views.content_manager.keywords import (
    admin_keyword_list_view,
    admin_keyword_create_view,
    admin_keyword_delete_view,
    admin_keyword_update_view,
)
from killay.admin.views.content_manager.pieces import (
    admin_piece_list_view,
    admin_piece_create_view,
    admin_piece_delete_view,
    admin_piece_update_view,
    admin_piece_meta_update_view,
    admin_piece_provider_create_view,
    admin_piece_provider_list_view,
    admin_piece_sequence_create_view,
    admin_piece_sequence_list_view,
)


from killay.admin.views import videos as videos_views
from killay.admin.views import users as users_views
from killay.admin.views import pages as pages_views


app_name = "admin"


urlpatterns = [
    path("", view=admin_configuration_view, name="configuration"),
    path(
        "cm/",
        view=RedirectView.as_view(pattern_name="admin:archive_list"),
        name="content-manager",
    ),
]

# Content Manager - Archives

urlpatterns += [
    path("cm/archives/", view=admin_archive_list_view, name="archive_list"),
    path(
        "cm/archives/~create/",
        view=admin_archive_create_view,
        name="archive_create",
    ),
    path(
        "cm/archives/<str:slug>/delete/",
        view=admin_archive_delete_view,
        name="archive_delete",
    ),
    path(
        "cm/archives/<str:slug>/",
        view=admin_archive_update_view,
        name="archive_update",
    ),
]

# Content Manager - Collections

urlpatterns += [
    path(
        "cm/collections/",
        view=admin_collection_list_view,
        name="collection_list",
    ),
    path(
        "cm/collections/~create/",
        view=admin_collection_create_view,
        name="collection_create",
    ),
    path(
        "cm/collections/<str:slug>/delete/",
        view=admin_collection_delete_view,
        name="collection_delete",
    ),
    path(
        "cm/collections/<str:slug>/",
        view=admin_collection_update_view,
        name="collection_update",
    ),
]


# Content Manager - Pieces

urlpatterns += [
    path(
        "cm/pieces/",
        view=admin_piece_list_view,
        name="piece_list",
    ),
    path(
        "cm/pieces/~create/",
        view=admin_piece_create_view,
        name="piece_create",
    ),
    path(
        "cm/pieces/<str:slug>/delete/",
        view=admin_piece_delete_view,
        name="piece_delete",
    ),
    path(
        "cm/pieces/<str:slug>/meta/",
        view=admin_piece_meta_update_view,
        name="piece_meta_update",
    ),
    path(
        "cm/pieces/<str:slug>/providers/~create/",
        view=admin_piece_provider_create_view,
        name="piece_provider_create",
    ),
    path(
        "cm/pieces/<str:slug>/providers/",
        view=admin_piece_provider_list_view,
        name="piece_provider_list",
    ),
    path(
        "cm/pieces/<str:slug>/sequences/~create/",
        view=admin_piece_sequence_create_view,
        name="piece_sequence_create",
    ),
    path(
        "cm/pieces/<str:slug>/sequences/",
        view=admin_piece_sequence_list_view,
        name="piece_sequence_list",
    ),
    path(
        "cm/pieces/<str:slug>/",
        view=admin_piece_update_view,
        name="piece_update",
    ),
]

# Content Manager - Categories

urlpatterns += [
    path(
        "cm/categories/",
        view=admin_category_list_view,
        name="category_list",
    ),
    path(
        "cm/categories/~create/",
        view=admin_category_create_view,
        name="category_create",
    ),
    path(
        "cm/categories/<str:slug>/delete/",
        view=admin_category_delete_view,
        name="category_delete",
    ),
    path(
        "cm/categories/<str:slug>/",
        view=admin_category_update_view,
        name="category_update",
    ),
]


# Content Manager - People

urlpatterns += [
    path(
        "cm/people/",
        view=admin_person_list_view,
        name="person_list",
    ),
    path(
        "cm/people/~create/",
        view=admin_person_create_view,
        name="person_create",
    ),
    path(
        "cm/people/<str:slug>/delete/",
        view=admin_person_delete_view,
        name="person_delete",
    ),
    path(
        "cm/people/<str:slug>/",
        view=admin_person_update_view,
        name="person_update",
    ),
]

# Content Manager - Keywords

urlpatterns += [
    path(
        "cm/keywords/",
        view=admin_keyword_list_view,
        name="keyword_list",
    ),
    path(
        "cm/keywords/~create/",
        view=admin_keyword_create_view,
        name="keyword_create",
    ),
    path(
        "cm/keywords/<str:slug>/delete/",
        view=admin_keyword_delete_view,
        name="keyword_delete",
    ),
    path(
        "cm/keywords/<str:slug>/",
        view=admin_keyword_update_view,
        name="keyword_update",
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
