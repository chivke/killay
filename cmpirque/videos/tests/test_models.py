import pytest

from cmpirque.videos.models import Video, VideoSequence


pytestmark = pytest.mark.django_db


def test_video_str(video: Video):
    assert str(video) == f"Video <{video.code}>"


def test_video_sequence_manager(video_sequences: VideoSequence):
    sequences = VideoSequence.objects.get_ordered_data()
    for index, sequence in enumerate(sequences):
        assert isinstance(sequence, dict)
        assert "order" in sequence
        assert sequence["order"] == index + 1
