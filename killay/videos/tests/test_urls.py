import pytest
from django.urls import resolve, reverse

from killay.videos.models import (
    Video,
    VideoCategory,
    VideoCollection,
    VideoKeyword,
    VideoPerson,
)

pytestmark = pytest.mark.django_db


def test_detail(video_categorization: Video):
    video = video_categorization.video
    collection = video_categorization.collection
    assert (
        reverse(
            "videos:detail", kwargs={"slug": video.code, "collection": collection.slug}
        )
        == f"/videos/c/{collection.slug}/v/{video.code}/"
    )
    assert (
        resolve(f"/videos/c/{collection.slug}/v/{video.code}/").view_name
        == "videos:detail"
    )


def test_collection(video_collection: VideoCollection):
    assert (
        reverse("videos:collection", kwargs={"slug": video_collection.slug})
        == f"/videos/c/{video_collection.slug}/"
    )
    assert (
        resolve(f"/videos/c/{video_collection.slug}/").view_name == "videos:collection"
    )


def test_category(video_category: VideoCategory):
    assert (
        reverse(
            "videos:category",
            kwargs={
                "collection": video_category.collection.slug,
                "slug": video_category.slug,
            },
        )
        == f"/videos/c/{video_category.collection.slug}/c/{video_category.slug}/"
    )
    assert (
        resolve(
            f"/videos/c/{video_category.collection.slug}/c/{video_category.slug}/"
        ).view_name
        == "videos:category"
    )


def test_person(video_person: VideoPerson):
    assert (
        reverse(
            "videos:person",
            kwargs={
                "collection": video_person.collection.slug,
                "slug": video_person.slug,
            },
        )
        == f"/videos/c/{video_person.collection.slug}/p/{video_person.slug}/"
    )
    assert (
        resolve(
            f"/videos/c/{video_person.collection.slug}/p/{video_person.slug}/"
        ).view_name
        == "videos:person"
    )


def test_keyword(video_keyword: VideoKeyword):
    assert (
        reverse(
            "videos:keyword",
            kwargs={
                "collection": video_keyword.collection.slug,
                "slug": video_keyword.slug,
            },
        )
        == f"/videos/c/{video_keyword.collection.slug}/k/{video_keyword.slug}/"
    )
    assert (
        resolve(
            f"/videos/c/{video_keyword.collection.slug}/k/{video_keyword.slug}/"
        ).view_name
        == "videos:keyword"
    )
