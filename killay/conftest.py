import pytest

from typing import List

from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.files.uploadedfile import SimpleUploadedFile

from killay.users.models import User
from killay.users.tests.factories import UserFactory, UserAdminFactory

from killay.pages.models import Page
from killay.pages.tests.factories import PageFactory, HomePageFactory

from killay.videos.models import (
    Video,
    VideoCategorization,
    VideoCategory,
    VideoCollection,
    VideoKeyword,
    VideoPerson,
    VideoProvider,
    VideoSequence,
)
from killay.videos.tests.factories import (
    VideoFactory,
    VideoCategorizationFactory,
    VideoCategoryFactory,
    VideoCollectionFactory,
    VideoKeywordFactory,
    VideoPersonFactory,
    VideoProviderFactory,
    VideoSequenceFactory,
)


@pytest.fixture
def rf_msg(rf):
    def _set_msg(request):
        middleware = SessionMiddleware()
        middleware.process_request(request)
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        return request

    def _set_rf(method, url, *args, **kwargs):
        return _set_msg(getattr(rf, method)(url, *args, **kwargs))

    return _set_rf


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
def video_provider(video: Video) -> VideoProvider:
    return VideoProviderFactory(video=video)


@pytest.fixture
def video_providers(video: Video) -> VideoProvider:
    return VideoProviderFactory.create_batch(5, video=video)


@pytest.fixture
def video_collection() -> VideoCollection:
    return VideoCollectionFactory()


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
        categories=(video_category,), people=(video_person,), keywords=(video_keyword,)
    )


@pytest.fixture
def video_sequence(video: Video) -> VideoSequence:
    return VideoSequenceFactory(video_id=video.id)  # ini=5, end=15)


@pytest.fixture
def video_sequences(video: Video) -> List[VideoSequence]:
    return VideoSequenceFactory.create_batch(5, video_id=video.id)


@pytest.fixture
def image():
    return SimpleUploadedFile("image.jpg", b"fake content", content_type="image/jpg")
