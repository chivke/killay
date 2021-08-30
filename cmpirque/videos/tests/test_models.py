import pytest
from time import strftime, gmtime
from typing import List

from django.utils import timezone

from cmpirque.videos.models import (
    Video,
    VideoCategory,
    VideoKeyword,
    VideoSequence,
    VideoPerson,
    VideoProvider,
)

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

    def test_has_sequences(self, video: Video, video_sequence: VideoSequence):
        assert video.has_sequences

    def test_import_from_vtt_file(self, video: Video, tmpdir):
        file = tmpdir.join("file.vtt")
        times_of_sequences = [
            {"ini": 1, "end": 70},
            {"ini": 195, "end": 612},
            {"ini": 603, "end": 4245},
        ]
        file.write(
            "WEBVTT\n"
            f"\n1\n{strftime('%H:%M:%S', gmtime(times_of_sequences[0]['ini']))}.000"
            f" --> {strftime('%H:%M:%S', gmtime(times_of_sequences[0]['end']))}.000"
            "\nContent of sequence 1\n"
            f"\n2\n{strftime('%H:%M:%S', gmtime(times_of_sequences[1]['ini']))}.000"
            f" --> {strftime('%H:%M:%S', gmtime(times_of_sequences[1]['end']))}.030"
            "\nContent of sequence 2\n"
            f"\n3\n{strftime('%H:%M:%S', gmtime(times_of_sequences[2]['ini']))}.000"
            f" --> {strftime('%H:%M:%S', gmtime(times_of_sequences[2]['end']))}.020"
            "\nContent of sequence 3\n"
        )
        assert not video.has_sequences
        sequences = video.import_from_vtt_file(file)
        assert video.has_sequences
        assert video.sequences.count() == 3
        for index, sequence in enumerate(sequences):
            sequence.ini == times_of_sequences[index]["ini"]
            sequence.end == times_of_sequences[index]["end"]


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
        assert video_provider.ply_embed_id in video_provider.video_url_for_plyr
        video_provider.plyr_provider = VideoProviderConstants.YOUTUBE
        assert video_provider.plyr_provider in video_provider.video_url
        assert video_provider.plyr_provider in video_provider.video_url_for_plyr


class TestVideoCategory:
    def test_str(self, video_category: VideoCategory):
        assert str(video_category) == video_category.name

    def test_get_absolute_url(self, video_category: VideoCategory):
        assert (
            video_category.get_absolute_url()
            == f"/videos/category/{video_category.slug}/"
        )


class TestVideoPerson:
    def test_str(self, video_person: VideoPerson):
        assert str(video_person) == video_person.name


class TestVideoKeyword:
    def test_str(self, video_keyword: VideoKeyword):
        assert str(video_keyword) == video_keyword.name
