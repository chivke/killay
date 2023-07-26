from django.urls import path

from killay.viewer.lib.constants import ViewerPatternConstants
from killay.viewer.views.archives import (
    archive_list_view,
    archive_detail_view,
)
from killay.viewer.views.pieces import piece_detail_view, piece_list_view
from killay.viewer.views.root import root_view


app_name = ViewerPatternConstants.APP_NAME


urlpatterns = [
    path(
        "",
        view=root_view,
        name=ViewerPatternConstants.ROOT,
    ),
    path(
        "archives/",
        view=archive_list_view,
        name=ViewerPatternConstants.ARCHIVE_LIST,
    ),
    path(
        "archives/<str:slug>/",
        view=archive_detail_view,
        name=ViewerPatternConstants.ARCHIVE_DETAIL,
    ),
    path(
        "pieces/",
        view=piece_list_view,
        name=ViewerPatternConstants.PIECE_LIST,
    ),
    path(
        "pieces/<str:slug>/",
        view=piece_detail_view,
        name=ViewerPatternConstants.PIECE_DETAIL,
    ),
]
