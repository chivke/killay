import pytest
from django.urls import resolve, reverse

from killay.videos.models import Video

pytestmark = pytest.mark.django_db


def test_configuration():
    assert reverse("admin:configuration") == "/admin/"
    assert resolve("/admin/").view_name == "admin:configuration"


def test_update(video: Video):
    assert (
        reverse("admin:videos_update", kwargs={"slug": video.code})
        == f"/admin/videos/{video.code}/~update/"
    )
    assert (
        resolve(f"/admin/videos/{video.code}/~update/").view_name
        == "admin:videos_update"
    )


def test_delete(video: Video):
    assert (
        reverse("admin:videos_delete", kwargs={"slug": video.code})
        == f"/admin/videos/{video.code}/~delete/"
    )
    assert (
        resolve(f"/admin/videos/{video.code}/~delete/").view_name
        == "admin:videos_delete"
    )


def test_sequences_list(video: Video):
    assert (
        reverse("admin:videos_sequences_list", kwargs={"slug": video.code})
        == f"/admin/videos/{video.code}/~sequences/"
    )
    assert (
        resolve(f"/admin/videos/{video.code}/~sequences/").view_name
        == "admin:videos_sequences_list"
    )


def test_categorization(video: Video):
    assert (
        reverse("admin:videos_categorization", kwargs={"slug": video.code})
        == f"/admin/videos/{video.code}/~categorization/"
    )
    assert (
        resolve(f"/admin/videos/{video.code}/~categorization/").view_name
        == "admin:videos_categorization"
    )
