import pytest

from typing import List

from cmpirque.users.models import User
from cmpirque.users.tests.factories import UserFactory, UserAdminFactory

from cmpirque.pages.models import Page
from cmpirque.pages.tests.factories import PageFactory, HomePageFactory

from cmpirque.videos.models import (
    Video,
    VideoCategorization,
    VideoCategory,
    VideoKeyword,
    VideoPerson,
    VideoSequence,
)
from cmpirque.videos.tests.factories import (
    VideoFactory,
    VideoCategorizationFactory,
    VideoCategoryFactory,
    VideoKeywordFactory,
    VideoPersonFactory,
    VideoSequenceFactory,
)


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def admin_user() -> User:
    return UserAdminFactory()


@pytest.fixture
def page() -> Page:
    return PageFactory()


@pytest.fixture
def home_page() -> Page:
    return HomePageFactory()


@pytest.fixture
def video() -> Video:
    return VideoFactory()


@pytest.fixture
def video_category() -> VideoCategory:
    return VideoCategoryFactory()


@pytest.fixture
def video_person() -> VideoPerson:
    return VideoPersonFactory()


@pytest.fixture
def video_keyword() -> VideoKeyword:
    return VideoKeywordFactory()


@pytest.fixture
def video_categorization(
    video_category: VideoCategory,
    video_person: VideoPerson,
    video_keyword: VideoKeyword,
) -> VideoCategorization:
    return VideoCategorizationFactory(
        categories=(video_category,),
        people=(video_person,),
        keywortds=(video_keyword,),
    )


@pytest.fixture
def video_sequence(video: Video) -> VideoSequence:
    return VideoSequenceFactory(video_id=video.id)  # ini=5, end=15)


@pytest.fixture
def video_sequences(video: Video) -> List[VideoSequence]:
    return VideoSequenceFactory.create_batch(5, video_id=video.id)
