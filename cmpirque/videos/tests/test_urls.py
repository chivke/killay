import pytest
from django.urls import resolve, reverse

from cmpirque.videos.models import Video

pytestmark = pytest.mark.django_db


def test_create():
    assert reverse("videos:create") == "/videos/~create/"
    assert resolve("/videos/~create/").view_name == "videos:create"


def test_detail(video: Video):
    assert (
        reverse("videos:detail", kwargs={"slug": video.code})
        == f"/videos/{video.code}/"
    )
    assert resolve(f"/videos/{video.code}/").view_name == "videos:detail"


def test_update(video: Video):
    assert (
        reverse("videos:update", kwargs={"slug": video.code})
        == f"/videos/{video.code}/~update/"
    )
    assert resolve(f"/videos/{video.code}/~update/").view_name == "videos:update"


def test_delete(video: Video):
    assert (
        reverse("videos:delete", kwargs={"slug": video.code})
        == f"/videos/{video.code}/~delete/"
    )
    assert resolve(f"/videos/{video.code}/~delete/").view_name == "videos:delete"


def test_sequences_list(video: Video):
    assert (
        reverse("videos:sequences_list", kwargs={"slug": video.code})
        == f"/videos/{video.code}/~sequences/"
    )
    assert (
        resolve(f"/videos/{video.code}/~sequences/").view_name
        == "videos:sequences_list"
    )
