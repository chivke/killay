import pytest
from datetime import date, time
from unittest import mock

from killay.admin.engine.bulk_actions.executors import (
    Executor,
    ExecutionError,
    PieceCreateExecutor,
)
from killay.archives.tests import recipes as archives_recipes


@pytest.mark.django_db
class TestExecutor:
    def test_run_success(self):
        executor = Executor(data_list=[True])
        assert executor.run() == [True]

    @mock.patch("killay.admin.engine.bulk_actions.executors.Executor.execute")
    def test_unexpected_error(self, execute_method_mock):
        message = "error  message"
        execute_method_mock.side_effect = ValueError(message)
        executor = Executor(data_list=[True])
        with pytest.raises(ExecutionError) as error:
            executor.run()
            assert error.data["message"] == message
            assert error.data["type"] == "unknown"


@pytest.mark.django_db
class TestPieceCreateExecutor:
    def test_happy_path(self):
        collection = archives_recipes.collection_recipe.make()
        category = archives_recipes.category_recipe.make(collection_id=collection.id)
        success_data = {
            "collection": collection,
            "category": category,
            "code": "fake-code",
            "title": "fake",
            "is_published": False,
            "kind": "VIDEO",
            "people": ["fake-person1", "fake-person2"],
            "keywords": ["fake-kw1", "fake-kw2"],
            "is_restricted": False,
            "video_url": "https://www.youtube.com/watch?v=FAKE",
            "event": "fake",
            "description": "fake",
            "description_date": "2000-1-1",
            "location": "fake",
            "duration": "00:00:01",
            "register_date": "2000-1-1",
            "register_author": "fake",
            "productor": "fake",
            "notes": "fake",
            "archivist_notes": "fake",
            "documentary_unit": "fake",
            "lang": "fake",
            "original_format": "fake",
        }
        executor = PieceCreateExecutor(data_list=[success_data])
        returned_data = executor._safe_execute(data_list=executor.data_list)
        created_piece = returned_data[0]["instance"]
        assert created_piece.code == success_data["code"]
        for field, value in success_data.items():
            if field == "collection":
                assert created_piece.collection_id == collection.id
            elif field == "category":
                assert created_piece.categories.filter(id=category.id).exists()
            elif field == "people":
                assert created_piece.people.filter(
                    name__in=success_data["people"]
                ).exists()
            elif field == "keywords":
                assert created_piece.keywords.filter(
                    name__in=success_data["keywords"]
                ).exists()
            elif "_date" in field:
                assert getattr(created_piece.meta, field) == date(2000, 1, 1)
            elif field == "duration":
                assert created_piece.meta.duration == time(0, 0, 1)
            elif "is_" in field:
                assert getattr(created_piece, field) is False
            elif field == "video_url":
                assert created_piece.providers.first().ply_embed_id == "FAKE"
                assert created_piece.providers.first().plyr_provider == "youtube"
            elif field in ["code", "kind", "title"]:
                assert getattr(created_piece, field) == value
            else:
                assert getattr(created_piece.meta, field) == value
