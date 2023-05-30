import pytest
from django.urls import resolve, reverse

from killay.videos.models import VideoCategorization

pytestmark = pytest.mark.django_db


def test_configuration():
    assert reverse("admin:site_configuration") == "/admin/conf/"
    assert resolve("/admin/").view_name == "admin:main"


def test_videos_update(video_categorization: VideoCategorization):
    video = video_categorization.video
    collection = video_categorization.collection
    assert (
        reverse(
            "admin:videos_update",
            kwargs={"slug": video.code, "collection": collection.slug},
        )
        == f"/admin/videos/c/{collection.slug}/{video.code}/~update/"
    )
    assert (
        resolve(f"/admin/videos/c/{collection.slug}/{video.code}/~update/").view_name
        == "admin:videos_update"
    )


def test_delete(video_categorization: VideoCategorization):
    video = video_categorization.video
    collection = video_categorization.collection
    assert (
        reverse(
            "admin:videos_delete",
            kwargs={"slug": video.code, "collection": collection.slug},
        )
        == f"/admin/videos/c/{collection.slug}/{video.code}/~delete/"
    )
    assert (
        resolve(f"/admin/videos/c/{collection.slug}/{video.code}/~delete/").view_name
        == "admin:videos_delete"
    )


def test_sequences_list(video_categorization: VideoCategorization):
    video = video_categorization.video
    collection = video_categorization.collection
    assert (
        reverse(
            "admin:videos_sequences_list",
            kwargs={"slug": video.code, "collection": collection.slug},
        )
        == f"/admin/videos/c/{collection.slug}/{video.code}/~sequences/"
    )
    assert (
        resolve(f"/admin/videos/c/{collection.slug}/{video.code}/~sequences/").view_name
        == "admin:videos_sequences_list"
    )


def test_categorization(video_categorization: VideoCategorization):
    video = video_categorization.video
    collection = video_categorization.collection
    assert (
        reverse(
            "admin:videos_categorization",
            kwargs={"slug": video.code, "collection": collection.slug},
        )
        == f"/admin/videos/c/{collection.slug}/{video.code}/~categorization/"
    )
    assert (
        resolve(
            f"/admin/videos/c/{collection.slug}/{video.code}/~categorization/"
        ).view_name
        == "admin:videos_categorization"
    )
