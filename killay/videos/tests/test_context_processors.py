import pytest
from django.test import RequestFactory

from killay.videos.context_processors import collections_context
from killay.videos.models import VideoCategory, VideoCollection
from killay.videos.tests.factories import VideoCategoryFactory, VideoCollectionFactory

pytestmark = pytest.mark.django_db


class TestCollectionsContext:
    def test_selected(self, rf: RequestFactory, video_collection: VideoCollection):
        request = rf.get(f"/videos/c/{video_collection.slug}/")
        menu_collections = collections_context(request)["menu_collections"]
        assert menu_collections[0]["slug"] == video_collection.slug
        assert menu_collections[0]["selected"] is True

    def test_not_selected(self, rf: RequestFactory, video_collection: VideoCollection):
        VideoCollectionFactory()
        request = rf.get(f"/videos/c/{video_collection.slug}/")
        menu_collections = collections_context(request)["menu_collections"]
        for menu_collection in menu_collections:
            if menu_collection.get("slug") == video_collection.slug:
                assert menu_collection["selected"] is True
            else:
                assert menu_collection["selected"] is False

    def test_category_selected(self, rf: RequestFactory, video_category: VideoCategory):
        VideoCollectionFactory()
        collection = video_category.collection
        VideoCategoryFactory(collection=collection)
        request = rf.get(f"/videos/c/{collection.slug}/c/{video_category.slug}/")
        menu_collections = collections_context(request)["menu_collections"]
        for menu_collection in menu_collections:
            if menu_collection.get("slug") == video_category.collection.slug:
                assert menu_collection["selected"] is True
            else:
                assert menu_collection["selected"] is False
            for category in menu_collection["categories"]:
                if category["slug"] == video_category.slug:
                    assert category["selected"] is True
                else:
                    assert category["selected"] is False
