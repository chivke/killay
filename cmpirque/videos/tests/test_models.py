import pytest

from typing import List

from django.utils import timezone

from cmpirque.videos.models import Video, VideoSequence, VideoProvider

from cmpirque.videos.lib.constants import VideoProviderConstants


pytestmark = pytest.mark.django_db


def test_video_sequence_manager(video_sequences: VideoSequence):
    sequences = VideoSequence.objects.get_ordered_data()
    for index, sequence in enumerate(sequences):
        assert isinstance(sequence, dict)
        assert "order" in sequence
        assert sequence["order"] == index + 1


class TestVideoModel:
    def test_str(self, video: Video):
        assert str(video) == f"Video <{video.code}>"

    def test_get_absolute_url(self, video: Video):
        assert video.get_absolute_url() == f"/videos/{video.code}/"

    def test_active_provider(self, video: Video, video_provider: VideoProvider):
        assert video.active_provider == video_provider


class TestVideoProvider:
    def test_save(self, video_providers: List[VideoProvider]):
        video_provider = video_providers[0]
        assert all([provider.active for provider in video_providers])
        video_provider.save()
        assert video_provider.active is True
        for provider in video_providers:
            provider.refresh_from_db()
        assert not any([provider.active for provider in video_providers[1:]])
        video_provider.online = True
        video_provider.checked_at = timezone.now()
        video_provider.save()
        assert video_provider.online is True

    def test_video_url(self, video_provider: VideoProvider):
        assert video_provider.ply_embed_id in video_provider.video_url
        video_provider.plyr_provider = VideoProviderConstants.YOUTUBE
        assert video_provider.plyr_provider in video_provider.video_url
