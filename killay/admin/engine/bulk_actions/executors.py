import re

from typing import Dict

from django.db import transaction
from django.urls import reverse

from killay.archives.lib.constants import (
    PieceConstants,
    ProviderConstants,
)
from killay.archives.services import (
    bulk_add_piece_categories,
    bulk_add_piece_keyword_by_texts,
    bulk_add_piece_people_by_texts,
    bulk_create_meta_pieces,
    bulk_create_pieces,
    bulk_create_piece_video_provider,
)


class ExecutionError(Exception):
    def __init__(self, data, *args, **kwargs):
        self.data = data
        super().__init__(*args, **kwargs)


class Executor:
    def __init__(self, data_list):
        self.data_list = data_list

    def run(self):
        try:
            processed_data_list = self._safe_execute(data_list=self.data_list)
        except Exception as error:
            raise ExecutionError({"message": str(error), "type": "uknown"})

        return processed_data_list

    def _safe_execute(self, data_list):
        with transaction.atomic():
            returned_data_list = self.execute(data_list=data_list)
        return returned_data_list

    def execute(self, data_list):
        return data_list


class PieceCreateExecutor(Executor):
    def execute(self, data_list) -> list:
        pieces_map = self._get_piece_map(data_list=data_list)
        self._add_meta(data_list=data_list, pieces_map=pieces_map)
        self._add_categories(data_list=data_list, pieces_map=pieces_map)
        self._add_people(data_list=data_list, pieces_map=pieces_map)
        self._add_keyword(data_list=data_list, pieces_map=pieces_map)
        self._add_video_provider(data_list=data_list, pieces_map=pieces_map)
        return [
            {
                "code": {
                    "label": code,
                    "link": reverse(
                        "admin:piece_update",
                        kwargs={"slug": piece.id},
                    ),
                },
                "title": piece.title,
                "kind": piece.kind,
                "collection": {
                    "label": piece.collection.name,
                    "link": reverse(
                        "admin:collection_update", kwargs={"slug": piece.collection_id}
                    ),
                },
                "category": {
                    "label": piece.categories.first().name,
                    "link": reverse(
                        "admin:collection_update",
                        kwargs={"slug": piece.categories.first().id},
                    ),
                },
                "instance": piece,
            }
            for code, piece in pieces_map.items()
        ]

    def _get_piece_map(self, data_list) -> Dict:
        instance_fields = [
            "code",
            "title",
            "is_published",
            "kind",
            "is_restricted",
        ]
        piece_data_instances = []
        for data in data_list:
            piece_data = {field: data.get(field) for field in instance_fields}
            piece_data["collection_id"] = data["collection"].pk
            piece_data_instances.append(piece_data)
        instances = bulk_create_pieces(data_list=piece_data_instances)
        return {instance.code: instance for instance in instances}

    def _add_meta(self, data_list, pieces_map):
        piece_meta_data = []
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
        for data in data_list:
            piece_instance = pieces_map[data["code"]]
            meta_data = {
                field: value for field, value in data.items() if field in meta_fields
            }

            piece_meta_data.append((piece_instance.id, meta_data))
        return bulk_create_meta_pieces(piece_meta_data=piece_meta_data)

    def _add_categories(self, data_list, pieces_map):
        pieces_categories_data = []
        for data in data_list:
            piece_instance = pieces_map[data["code"]]
            category = data.get("category")
            if category:
                piece_category_data = (
                    piece_instance.pk,
                    [category.id],
                )
                pieces_categories_data.append(piece_category_data)
        return bulk_add_piece_categories(pieces_categories_data=pieces_categories_data)

    def _add_people(self, data_list, pieces_map):
        pieces_people_data = []
        for data in data_list:
            piece_instance = pieces_map[data["code"]]
            people = data.get("people")
            if people:
                piece_person_data = (
                    piece_instance.pk,
                    people,
                )
                pieces_people_data.append(piece_person_data)
        return bulk_add_piece_people_by_texts(piece_people_data=pieces_people_data)

    def _add_keyword(self, data_list, pieces_map):
        pieces_keywords_data = []
        for data in data_list:
            piece_instance = pieces_map[data["code"]]
            keywords = data.get("keywords")
            if keywords:
                piece_keywords_data = (
                    piece_instance.pk,
                    keywords,
                )
                pieces_keywords_data.append(piece_keywords_data)
        return bulk_add_piece_keyword_by_texts(piece_keyword_data=pieces_keywords_data)

    def _add_video_provider(self, data_list, pieces_map):
        piece_video_data_list = []
        for data in data_list:
            piece_instance = pieces_map[data["code"]]
            video_url = data.get("video_url")
            if video_url and piece_instance.kind == PieceConstants.KIND_VIDEO:
                provider = (
                    ProviderConstants.VIMEO
                    if ProviderConstants.VIMEO in video_url
                    else ProviderConstants.YOUTUBE
                )
                regex = (
                    ProviderConstants.VIMEO_ID_REGEX
                    if provider == ProviderConstants.VIMEO
                    else ProviderConstants.YOUTUBE_ID_REGEX
                )
                embed_id = re.findall(regex, video_url)
                embed_id = embed_id[0] if embed_id else video_url
                video_data = {"ply_embed_id": embed_id, "plyr_provider": provider}
                piece_video_data = (piece_instance.id, video_data)
                piece_video_data_list.append(piece_video_data)
        if piece_video_data_list:
            return bulk_create_piece_video_provider(
                piece_video_data=piece_video_data_list
            )
