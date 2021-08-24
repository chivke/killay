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
        assert len(menu_categories) == 1
        assert menu_categories[0]["name"] == video_category.name
        assert menu_categories[0]["slug"] == video_category.slug
        assert menu_categories[0]["url"] == video_category.get_absolute_url()
        assert menu_categories[0]["selected"]

    def test_not_selected(self, rf: RequestFactory, video_category: VideoCategory):
        second_category = VideoCategoryFactory()
        request = rf.get(f"/videos/category/{video_category.slug}/")
        menu_categories = categories_context(request)["menu_categories"]
        assert len(menu_categories) == 2
        assert menu_categories[0]["name"] == video_category.name
        assert menu_categories[0]["slug"] == video_category.slug
        assert menu_categories[0]["url"] == video_category.get_absolute_url()
        assert menu_categories[0]["selected"]
        assert menu_categories[1]["name"] == second_category.name
        assert menu_categories[1]["slug"] == second_category.slug
        assert menu_categories[1]["url"] == second_category.get_absolute_url()
        assert not menu_categories[1]["selected"]
