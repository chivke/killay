
import factory

# from factory import Faker, Sequence, SubFactory, RelatedFactory, post_generation
from factory.django import DjangoModelFactory

from cmpirque.videos.models import (
    Video,
    VideoCategory,
    VideoCategorization,
    VideoKeyword,
    VideoMeta,
    VideoPerson,
    VideoSequence,
)


class VideoMetaFactory(DjangoModelFactory):
    class Meta:
        model = VideoMeta
    title = factory.Faker("name")
    description = factory.Faker("text")


class VideoFactory(DjangoModelFactory):
    code = factory.Faker('slug')
    meta = VideoMetaFactory

    class Meta:
        model = Video
        django_get_or_create = ['code']


class VideoCategoryFactory(DjangoModelFactory):
    class Meta:
        model = VideoCategory


class VideoPersonFactory(DjangoModelFactory):
    class Meta:
        model = VideoPerson


class VideoKeywordFactory(DjangoModelFactory):
    class Meta:
        model = VideoKeyword


class VideoCategorizationFactory(DjangoModelFactory):
    class Meta:
        model = VideoCategorization

    video = factory.SubFactory(VideoFactory)

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
                self.categories.add(person)

    @factory.post_generation
    def keywords(self, create, keywords, **kwargs):
        if not create:
            return
        if keywords:
            for keyword in keywords:
                self.categories.add(keyword)


class VideoSequenceFactory(DjangoModelFactory):
    class Meta:
        model = VideoSequence

    video = factory.RelatedFactory(VideoFactory)
    ini = factory.Sequence(lambda n: n + 5)
    end = factory.Sequence(lambda n: n + 10)
