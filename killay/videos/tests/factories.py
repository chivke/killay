import factory
from datetime import time

# from factory import Faker, Sequence, SubFactory, RelatedFactory, post_generation
from factory.django import DjangoModelFactory

from killay.videos.lib.constants import VideoProviderConstants

from killay.videos.models import (
    Video,
    VideoCategory,
    VideoCategorization,
    VideoCollection,
    VideoKeyword,
    VideoMeta,
    VideoPerson,
    VideoProvider,
    VideoSequence,
)


class VideoMetaFactory(DjangoModelFactory):
    class Meta:
        model = VideoMeta

    title = factory.Faker("name")
    description = factory.Faker("text")


class VideoFactory(DjangoModelFactory):
    code = factory.Faker("slug")
    meta = VideoMetaFactory
    is_visible = True

    class Meta:
        model = Video
        django_get_or_create = ["code"]


class VideoProviderFactory(DjangoModelFactory):
    class Meta:
        model = VideoProvider

    video = VideoFactory
    active = True
    plyr_provider = VideoProviderConstants.VIMEO


class VideoCollectionFactory(DjangoModelFactory):
    class Meta:
        model = VideoCollection

    name = factory.Faker("name")
    slug = factory.Faker("slug")
    description = factory.Faker("text")


class VideoCategoryFactory(DjangoModelFactory):
    class Meta:
        model = VideoCategory

    name = factory.Faker("name")
    slug = factory.Faker("slug")
    description = factory.Faker("text")
    collection = factory.SubFactory(VideoCollectionFactory)


class VideoPersonFactory(DjangoModelFactory):
    class Meta:
        model = VideoPerson

    name = factory.Faker("name")
    slug = factory.Faker("slug")
    description = factory.Faker("text")
    collection = factory.SubFactory(VideoCollectionFactory)


class VideoKeywordFactory(DjangoModelFactory):
    class Meta:
        model = VideoKeyword

    name = factory.Faker("name")
    slug = factory.Faker("slug")
    description = factory.Faker("text")
    collection = factory.SubFactory(VideoCollectionFactory)


class VideoCategorizationFactory(DjangoModelFactory):
    class Meta:
        model = VideoCategorization

    video = factory.SubFactory(VideoFactory)
    collection = factory.SubFactory(VideoCollectionFactory)

    @factory.post_generation
    def categories(self, create, categories, **kwargs):
        if not create:
            return
        if categories:
            for category in categories:
                self.categories.add(category)

    @factory.post_generation
    def people(self, create, people, **kwargs):
        if not create:
            return
        if people:
            for person in people:
                self.people.add(person)

    @factory.post_generation
    def keywords(self, create, keywords, **kwargs):
        if not create:
            return
        if keywords:
            for keyword in keywords:
                self.keywords.add(keyword)


class VideoSequenceFactory(DjangoModelFactory):
    class Meta:
        model = VideoSequence

    video = factory.RelatedFactory(VideoFactory)
    ini = time(0, 1)
    end = time(0, 2)
