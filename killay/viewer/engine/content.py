from typing import Dict

from django.urls import reverse
from django.templatetags.static import static

from killay.archives.lib.constants import PieceConstants
from killay.viewer.lib.constants import ContentConstants, ViewerPatternConstants


class ContentSerializer:
    def _serialize_archives(self, archives):
        archive_list = []
        for archive in archives:
            archive_data = self._serialize_archive(archive=archive)
            archive_list.append(archive_data)
        return archive_list

    def _serialize_archive(self, archive):
        pattern = ViewerPatternConstants.pattern_by_name(
            name=ViewerPatternConstants.ARCHIVE_DETAIL
        )
        default_image = static("images/default-background.svg")
        archive_data = {
            **archive.__dict__,
            "image": archive.image or default_image,
            "link": reverse(pattern, kwargs={"slug": archive.slug}),
        }
        collections = self.get_collections_by_archive_id(archive_id=archive.id)
        archive_data["collections"] = self._serialize_collections(
            collections=collections,
        )
        return archive_data

    def _serialize_collections(self, collections):
        link_template = "{base_url}?archive={archive_slug}&collection={slug}"
        default_image = static("images/default-background.svg")
        collections_data = self._serialize_categorization(
            instances=collections,
            link_template=link_template,
            link_fields=["archive_slug", "slug"],
        )
        for data in collections_data["items"]:
            data["image"] = data["image"] or default_image
        return collections_data

    def _serialize_collection(self, collection):
        collection_data = collection.__dict__
        base_url = self._get_piece_list_base_url()
        collection_data["link"] = f"{base_url}?collection={collection.slug}"
        return collection_data

    def _get_categorization(self, piece) -> Dict:
        categorization = {}
        categories = piece.categories.all()
        if categories:
            categorization["categories"] = self._serialize_categories(
                categories=categories
            )
        people = piece.people.all()
        if people:
            categorization["people"] = self._serialize_people(people=people)
        keywords = piece.keywords.all()
        if keywords:
            categorization["keywords"] = self._serialize_keywords(keywords=keywords)
        return categorization

    def _serialize_categorization(self, instances, link_template, link_fields):
        base_url = self._get_piece_list_base_url()
        instances_data = []
        for instance in instances:
            instance_data = instance.__dict__
            kwargs = {field: getattr(instance, field) for field in link_fields}
            instance_data["link"] = link_template.format(base_url=base_url, **kwargs)
            instances_data.append(instance_data)
        label = instances[0]._meta.verbose_name_plural.capitalize()
        return {
            "total": len(instances),
            "items": instances_data,
            "label": label,
        }

    def _serialize_categories(self, categories):
        link_template = (
            "{base_url}?archive={archive_slug}&collection={collection_slug}"
            "&category={slug}"
        )
        return self._serialize_categorization(
            instances=categories,
            link_template=link_template,
            link_fields=["archive_slug", "collection_slug", "slug"],
        )

    def _serialize_people(self, people):
        link_template = "{base_url}?person={slug}"
        return self._serialize_categorization(
            instances=people,
            link_template=link_template,
            link_fields=["slug"],
        )

    def _serialize_keywords(self, keywords):
        link_template = "{base_url}?keyword={slug}"
        return self._serialize_categorization(
            instances=keywords,
            link_template=link_template,
            link_fields=["slug"],
        )

    def _serialize_sequences(self, piece):
        sequences = []
        for index, sequence in enumerate(piece.sequences.all()):
            order = index + 1
            ini_sec = sequence.ini_sec
            end_sec = sequence.end_sec
            sequence_id = f"sequence-{order}-{ini_sec}-{end_sec}"
            sequence_data = {
                "id": sequence_id,
                "order": order,
                "title": sequence.title or order,
                "content": sequence.content,
                "ini_sec": ini_sec,
                "end_sec": end_sec,
            }
            sequences.append(sequence_data)
        return sequences

    def _serialize_field(self, instance, field):
        return {
            "value": getattr(instance, field),
            "label": instance._meta.get_field(field).verbose_name,
        }

    def _serialize_meta(self, piece):
        meta_data = [
            self._serialize_field(instance=piece, field="code"),
            self._serialize_field(instance=piece, field="title"),
        ]
        meta_data = {
            "code": self._serialize_field(instance=piece, field="code"),
            "title": self._serialize_field(instance=piece, field="title"),
        }
        for field in ContentConstants.PIECE_META_FIELDS:
            field_data = self._serialize_field(instance=piece.meta, field=field)
            if field_data["value"]:
                meta_data[field] = field_data
        return meta_data

    def _serialize_provider(self, piece):
        provider = piece.active_provider
        if not provider or not provider.is_ready:
            message = ContentConstants.PROVIDER_MESSAGES["no_provider"]
            return {
                "active": False,
                "message": message,
            }
        provider_data = {"active": True}
        if piece.kind == PieceConstants.KIND_VIDEO:
            provider_data["player_url"] = provider.video_url_for_plyr
        elif piece.kind == PieceConstants.KIND_IMAGE:
            provider_data["image"] = provider.image
        elif piece.kind in [
            PieceConstants.KIND_SOUND,
            PieceConstants.KIND_DOCUMENT,
        ]:
            provider_data["file"] = provider.file
        return provider_data
