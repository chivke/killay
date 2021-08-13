import pytest
from django.urls import resolve, reverse

from cmpirque.videos.models import Video

pytestmark = pytest.mark.django_db


def test_detail(video: Video):
    assert (
        reverse('videos:detail', kwargs={'slug': video.code})
        == f'/videos/{video.code}/'
    )
    assert resolve(f'/videos/{video.code}/').view_name == 'videos:detail'
