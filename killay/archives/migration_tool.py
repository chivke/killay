from typing import List

from django.db import transaction

from killay.archives.lib.constants import PieceConstants
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
)


class VideoMigrator:
    meta_fields = [
        "event",
        "description",
        "description_date",
        "location",
        "duration",
        "register_date",
        "register_author",
        "productor",
        "notes",
        "archivist_notes",
        "documentary_unit",
        "lang",
        "original_format",
    ]

    def __init__(self, name: str, slug: str, description: str) -> None:
        self._archive = Archive(name=name, slug=slug, description=description)

    def migrate(self) -> None:
        self._fetch_video_data()
        with transaction.atomic():
            returned_data = self._execute_migration()
        return returned_data

    def _fetch_video_data(self) -> None:
        self._video_collections = list(VideoCollection.objects.all())
        self._video_categories = list(VideoCategory.objects.all())
        self._video_persons = list(VideoPerson.objects.all())
        self._video_keywords = list(VideoKeyword.objects.all())
        self._videos = list(
            Video.objects.select_related("meta", "categorization__collection").all()
        )

    def _execute_migration(self) -> List[Piece]:
        self._archive.save()
        categorization_fields = ["name", "slug", "description", "position"]
        self._collection_map = self._create_from(
            previous_instances=self._video_collections,
            model_class=Collection,
            fields=categorization_fields,
            archive_id=self._archive.id,
        )
        self._category_map = self._create_from(
            previous_instances=self._video_categories,
            model_class=Category,
            fields=categorization_fields,
        )
        self._person_map = self._create_from(
            previous_instances=self._video_persons,
            model_class=Person,
            fields=categorization_fields,
        )
        self._keyword_map = self._create_from(
            previous_instances=self._video_keywords,
            model_class=Keyword,
            fields=categorization_fields,
        )
        meta_instances = []
        pieces = []
        for video in self._videos:
            piece = self._create_piece_with_categorization(video=video)
            self._create_from(
                previous_instances=video.sequences.all(),
                model_class=Sequence,
                fields=["title", "content", "ini", "end"],
                piece_id=piece.id,
                index="id",
            )
            self._create_from(
                previous_instances=video.providers.all(),
                model_class=Provider,
                fields=[
                    "active",
                    "online",
                    "checked_at",
                    "ply_embed_id",
                    "plyr_provider",
                ],
                piece_id=piece.id,
                index="id",
            )
            meta = self._get_meta(video=video, piece=piece)
            meta.id = piece.meta.id
            meta_instances.append(meta)
            pieces.append(piece)
        PieceMeta.objects.bulk_update(meta_instances, fields=self.meta_fields)
        return pieces

    def _create_piece_with_categorization(self, video) -> Piece:
        collection = self._collection_map[video.categorization.collection.slug]
        piece = Piece(
            code=video.code,
            title=video.meta.title,
            is_published=video.is_visible,
            kind=PieceConstants.KIND_VIDEO,
            thumb=video.thumb,
            collection_id=collection.id,
        )
        piece.save()
        category_ids = [
            self._category_map[category.slug].id
            for category in video.categorization.categories.all()
        ]
        piece.categories.add(*category_ids)
        person_ids = [
            self._person_map[person.slug].id
            for person in video.categorization.people.all()
        ]
        piece.people.add(*person_ids)
        keyword_ids = [
            self._keyword_map[keyword.slug].id
            for keyword in video.categorization.keywords.all()
        ]
        piece.keywords.add(*keyword_ids)
        return piece

    def _get_meta(self, video, piece) -> PieceMeta:
        kwargs = {field: getattr(video.meta, field) for field in self.meta_fields}
        return PieceMeta(**kwargs, piece_id=piece.id)

    def _create_from(
        self, previous_instances, model_class, fields, index="slug", **kwargs
    ) -> dict:
        instances = [
            model_class.objects.create(
                **{field: getattr(instance, field) for field in fields},
                **kwargs,
            )
            for instance in previous_instances
        ]
        return {getattr(instance, index): instance for instance in instances}


def migrate_video_data(
    name: str,
    slug: str,
    description: str,
) -> None:
    migrator = VideoMigrator(name=name, slug=slug, description=description)
    return migrator.migrate()
