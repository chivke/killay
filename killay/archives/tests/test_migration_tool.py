import pytest
from model_bakery import baker

from killay.archives.migration_tool import migrate_video_data

from killay.archives.models import (
    Archive,
    Category,
    Collection,
    Keyword,
    Person,
    Piece,
    PieceMeta,
    Provider,
    Sequence,
)
from killay.videos.models import (
    Video,
    VideoCategory,
    VideoCollection,
    VideoPerson,
    VideoKeyword,
    VideoSequence,
    VideoProvider,
)


@pytest.fixture
def video_archive():
    video_collection = baker.make(VideoCollection)
    video_categories = baker.make(
        VideoCategory, _quantity=5, collection=video_collection
    )
    video_categories_ids = [category.id for category in video_categories]
    video_persons = baker.make(VideoPerson, _quantity=10, collection=video_collection)
    video_persons_ids = [person.id for person in video_persons]
    video_keywords = baker.make(VideoKeyword, _quantity=10, collection=video_collection)
    video_keywords_ids = [keyword.id for keyword in video_keywords]

    _quantity = 20

    video_metas = baker.make("VideoMeta", _quantity=_quantity)
    videos = baker.make(Video, _quantity=_quantity)
    for index, video in enumerate(videos):
        meta = video_metas[index]
        video.meta_id = meta.id
        categorization = baker.make("VideoCategorization", video_id=video.id)
        categorization.video_id = video.id
        categorization.categories.add(*video_categories_ids)
        categorization.people.add(*video_persons_ids)
        categorization.keywords.add(*video_keywords_ids)
        categorization.save()
        baker.make(VideoSequence, _quantity=10, video_id=video.id)
        baker.make(VideoProvider, _quantity=4, video_id=video.id)
        video.save()
        assert video.categorization.id == categorization.id
    return {"video_collection": video_collection, "videos": videos}


@pytest.mark.django_db()
def test_migrate_video_data(video_archive):
    name = "fake_name"
    slug = "fake_slug"
    description = "fake_description"
    migrate_video_data(slug=slug, name=name, description=description)
    archive = Archive.objects.get(slug=slug)
    assert archive.name == name
    assert archive.description == description
    assert Collection.objects.count() == VideoCollection.objects.count()
    assert Category.objects.count() == VideoCategory.objects.count()
    assert Person.objects.count() == VideoPerson.objects.count()
    assert Keyword.objects.count() == VideoKeyword.objects.count()
    assert Piece.objects.count() == Video.objects.count()
    assert Sequence.objects.count() == VideoSequence.objects.count()
    assert Provider.objects.count() == VideoProvider.objects.count()
    for piece in Piece.objects.all():
        assert piece.categories.count() == 5
        assert piece.people.count() == 10
        assert piece.keywords.count() == 10
        assert piece.sequences.count() == 10
        assert piece.providers.count() == 4
