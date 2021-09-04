import pytest
from django.test import RequestFactory

from cmpirque.videos.context_processors import categories_context
from cmpirque.videos.models import VideoCategory
from cmpirque.videos.tests.factories import VideoCategoryFactory

pytestmark = pytest.mark.django_db


class TestCategoriesContext:
    def test_selected(self, rf: RequestFactory, video_category: VideoCategory):
        request = rf.get(f"/videos/category/{video_category.slug}/")
        menu_categories = categories_context(request)["menu_categories"]
        assert len(menu_categories) == 2
        assert menu_categories[0]["name"] == video_category.name
        assert menu_categories[0]["slug"] == video_category.slug
        assert menu_categories[0]["url"] == video_category.get_absolute_url()
        assert menu_categories[0]["selected"]

    def test_not_selected(self, rf: RequestFactory, video_category: VideoCategory):
        VideoCategoryFactory()
        request = rf.get(f"/videos/category/{video_category.slug}/")
        menu_categories = categories_context(request)["menu_categories"]
        assert len(menu_categories) == 3
        for menu_categoy in menu_categories:
            if "slug" in menu_categoy and menu_categoy["slug"] == video_category.slug:
                assert menu_categoy["selected"]
            else:
                assert not menu_categoy["selected"]
