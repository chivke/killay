from django.urls import path
from django.views.generic.base import RedirectView


from killay.admin.views import configuration as conf_views
from killay.admin.views.content_manager import bulk_actions as bulk_views

from killay.admin.views.content_manager import archives as archives_views
from killay.admin.views.content_manager import collections as collections_views
from killay.admin.views.content_manager import categories as categories_views
from killay.admin.views.content_manager import people as people_views
from killay.admin.views.content_manager import keywords as keywords_views
from killay.admin.views.content_manager import pieces as pieces_views
from killay.admin.views.content_manager import places as places_views

from killay.admin.views import users as users_views
from killay.admin.views import pages as pages_views


app_name = "admin"


# Configuration

urlpatterns = [
    path(
        "",
        view=RedirectView.as_view(pattern_name="admin:site_configuration"),
        name="main",
    ),
    path(
        "conf/",
        view=conf_views.admin_site_configuration_view,
        name="site_configuration",
    ),
    path(
        "conf/viewer/",
        view=conf_views.admin_site_viewer_view,
        name="site_viewer",
    ),
    path(
        "conf/social-medias/",
        view=conf_views.admin_site_social_media_list_view,
        name="site_social_media_list",
    ),
    path(
        "conf/social-medias/~create/",
        view=conf_views.admin_site_social_media_create_view,
        name="site_social_media_create",
    ),
    path(
        "conf/logos/",
        view=conf_views.admin_site_logo_list_view,
        name="site_logo_list",
    ),
    path(
        "conf/logos/~create/",
        view=conf_views.admin_site_logo_create_view,
        name="site_logo_create",
    ),
]

# Content Manager

urlpatterns += [
    path(
        "cm/",
        view=RedirectView.as_view(pattern_name="admin:bulk_action_list"),
        name="content_manager",
    ),
    path(
        "cm/bulk-actions/",
        view=bulk_views.bulk_action_list_view,
        name="bulk_action_list",
    ),
    path(
        "cm/bulk-actions/<str:action>/",
        view=bulk_views.bulk_action_view,
        name="bulk_action",
    ),
    path(
        "cm/bulk-actions/<str:action>/template/",
        view=bulk_views.bulk_action_template_view,
        name="bulk_action_template",
    ),
]

# Content Manager - Archives

urlpatterns += [
    path(
        "cm/archives/", view=archives_views.admin_archive_list_view, name="archive_list"
    ),
    path(
        "cm/archives/~create/",
        view=archives_views.admin_archive_create_view,
        name="archive_create",
    ),
    path(
        "cm/archives/<str:slug>/delete/",
        view=archives_views.admin_archive_delete_view,
        name="archive_delete",
    ),
    path(
        "cm/archives/<str:slug>/",
        view=archives_views.admin_archive_update_view,
        name="archive_update",
    ),
]

# Content Manager - Places

urlpatterns += [
    path("cm/places/", view=places_views.admin_place_list_view, name="place_list"),
    path(
        "cm/places/~create/",
        view=places_views.admin_place_create_view,
        name="place_create",
    ),
    path(
        "cm/places/<str:slug>/delete/",
        view=places_views.admin_place_delete_view,
        name="place_delete",
    ),
    path(
        "cm/places/<str:slug>/addresses/~create/",
        view=places_views.admin_place_address_create_view,
        name="place_address_create",
    ),
    path(
        "cm/places/<str:slug>/adresses/",
        view=places_views.admin_place_address_list_view,
        name="place_address_list",
    ),
    path(
        "cm/places/<str:slug>/",
        view=places_views.admin_place_update_view,
        name="place_update",
    ),
]

# Content Manager - Collections

urlpatterns += [
    path(
        "cm/collections/",
        view=collections_views.admin_collection_list_view,
        name="collection_list",
    ),
    path(
        "cm/collections/~create/",
        view=collections_views.admin_collection_create_view,
        name="collection_create",
    ),
    path(
        "cm/collections/<str:slug>/delete/",
        view=collections_views.admin_collection_delete_view,
        name="collection_delete",
    ),
    path(
        "cm/collections/<str:slug>/",
        view=collections_views.admin_collection_update_view,
        name="collection_update",
    ),
]


# Content Manager - Pieces

urlpatterns += [
    path(
        "cm/pieces/",
        view=pieces_views.admin_piece_list_view,
        name="piece_list",
    ),
    path(
        "cm/pieces/~create/",
        view=pieces_views.admin_piece_create_view,
        name="piece_create",
    ),
    path(
        "cm/pieces/<str:slug>/delete/",
        view=pieces_views.admin_piece_delete_view,
        name="piece_delete",
    ),
    path(
        "cm/pieces/<str:slug>/meta/",
        view=pieces_views.admin_piece_meta_update_view,
        name="piece_meta_update",
    ),
    path(
        "cm/pieces/<str:slug>/providers/~create/",
        view=pieces_views.admin_piece_provider_create_view,
        name="piece_provider_create",
    ),
    path(
        "cm/pieces/<str:slug>/providers/",
        view=pieces_views.admin_piece_provider_list_view,
        name="piece_provider_list",
    ),
    path(
        "cm/pieces/<str:slug>/sequences/~create/",
        view=pieces_views.admin_piece_sequence_create_view,
        name="piece_sequence_create",
    ),
    path(
        "cm/pieces/<str:slug>/sequences/",
        view=pieces_views.admin_piece_sequence_list_view,
        name="piece_sequence_list",
    ),
    path(
        "cm/pieces/<str:slug>/",
        view=pieces_views.admin_piece_update_view,
        name="piece_update",
    ),
]

# Content Manager - Categories

urlpatterns += [
    path(
        "cm/categories/",
        view=categories_views.admin_category_list_view,
        name="category_list",
    ),
    path(
        "cm/categories/~create/",
        view=categories_views.admin_category_create_view,
        name="category_create",
    ),
    path(
        "cm/categories/<str:slug>/delete/",
        view=categories_views.admin_category_delete_view,
        name="category_delete",
    ),
    path(
        "cm/categories/<str:slug>/",
        view=categories_views.admin_category_update_view,
        name="category_update",
    ),
]


# Content Manager - People

urlpatterns += [
    path(
        "cm/people/",
        view=people_views.admin_person_list_view,
        name="person_list",
    ),
    path(
        "cm/people/~create/",
        view=people_views.admin_person_create_view,
        name="person_create",
    ),
    path(
        "cm/people/<str:slug>/delete/",
        view=people_views.admin_person_delete_view,
        name="person_delete",
    ),
    path(
        "cm/people/<str:slug>/",
        view=people_views.admin_person_update_view,
        name="person_update",
    ),
]

# Content Manager - Keywords

urlpatterns += [
    path(
        "cm/keywords/",
        view=keywords_views.admin_keyword_list_view,
        name="keyword_list",
    ),
    path(
        "cm/keywords/~create/",
        view=keywords_views.admin_keyword_create_view,
        name="keyword_create",
    ),
    path(
        "cm/keywords/<str:slug>/delete/",
        view=keywords_views.admin_keyword_delete_view,
        name="keyword_delete",
    ),
    path(
        "cm/keywords/<str:slug>/",
        view=keywords_views.admin_keyword_update_view,
        name="keyword_update",
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
