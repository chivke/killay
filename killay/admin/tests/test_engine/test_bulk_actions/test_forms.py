from tempfile import NamedTemporaryFile

import pytest
from openpyxl import Workbook

from django.core.files import File

from killay.admin.engine.bulk_actions.forms import BulkActionForm
from killay.admin.lib.constants import BulkActionConstants
from killay.archives.tests import recipes as archives_recipes


@pytest.mark.django_db
class TestBulkActionForm:
    def test_clean_all_right(self, bulk_action_piece_create_success_wb):
        collection = archives_recipes.collection_recipe.make()
        collection_string = (
            f"{collection.name} "
            f"| {BulkActionConstants.TEMPLATE_ID.format(id=collection.id)}"
        )
        category = archives_recipes.category_recipe.make(collection_id=collection.id)
        success_data = {
            "collection": collection_string,
            "category": category.id,
            "code": "fake-code",
            "title": "fake",
            "is_published": "TRUE",
            "kind": "VIDEO",
            "people": "fake-person1, fake-person2",
            "keywords": "fake-kw1, fake-kw2",
            "is_restricted": "FALSE",
            "video_url": "https://www.youtube.com/watch?v=FAKE",
            "event": "fake",
            "description": "fake",
            "description_date": "2000-1-1",
            "location": "fake",
            "duration": "00:00:01",
            "register_date": "2000-1-2",
            "register_author": "fake",
            "productor": "fake",
            "notes": "fake",
            "archivist_notes": "fake",
            "documentary_unit": "fake",
            "lang": "fake",
            "original_format": "fake",
        }

        workbook = Workbook()
        worksheet = workbook.active
        worksheet.append(list(success_data))
        worksheet.append(list(success_data.values()))
        action_type = BulkActionConstants.TYPE_PIECE_CREATE

        with NamedTemporaryFile() as tmp_file:
            workbook.save(tmp_file.name)
            data = {"xls_file": File(tmp_file)}
            form = BulkActionForm(action_type=action_type, files=data)
            assert form.is_valid()
        cleaned_data = form.cleaned_data
        assert cleaned_data["xls_file_data"][0]["collection"] == collection
        assert cleaned_data["xls_file_data"][0]["category"] == category

    def test_with_serializer_errors(self):
        collection = archives_recipes.collection_recipe.make()
        collection_string = (
            f"{collection.name} "
            f"| {BulkActionConstants.TEMPLATE_ID.format(id=collection.id)}"
        )
        success_data = {
            "collection": collection_string,
            "code": "fake-code",
            "title": "fake",
            "is_published": "TRUE",
            "kind": "VIDEO",
        }
        fields = [
            "collection",
            "code",
            "title",
            "is_published",
            "kind",
        ]
        data_list = [
            success_data,
            {**success_data, "code": "fake-code-2", "collection": "99"},
            {**success_data, "code": "wrong code"},
        ]

        workbook = Workbook()
        worksheet = workbook.active
        worksheet.append(fields)
        for data in data_list:
            worksheet.append([data.get(field) for field in fields])
        action_type = BulkActionConstants.TYPE_PIECE_CREATE

        with NamedTemporaryFile() as tmp_file:
            workbook.save(tmp_file.name)
            data = {"xls_file": File(tmp_file)}
            form = BulkActionForm(action_type=action_type, files=data)
            assert not form.is_valid()
        assert form.errors["__all__"][0] == (
            "Row 2: collection: 99 for collection field does not exist"
        )
        assert form.errors["__all__"][1] == (
            'Row 3: code: code field must be slug (only letters, numbers and "-" or "_").'
        )

    def test_with_empty_file(self):
        action_type = BulkActionConstants.TYPE_PIECE_CREATE
        with NamedTemporaryFile() as tmp_file:
            data = {"xls_file": File(tmp_file)}
            form = BulkActionForm(action_type=action_type, files=data)
            assert not form.is_valid()
        assert form.errors["xls_file"] == ["The submitted file is empty."]

    def test_without_file(self):
        form = BulkActionForm(
            action_type=BulkActionConstants.TYPE_PIECE_CREATE, files={}
        )
        assert not form.is_valid()
        assert form.errors["xls_file"] == ["This field is required."]

    def test_get_file_headers_context(self):
        form = BulkActionForm(
            action_type=BulkActionConstants.TYPE_PIECE_CREATE, files={}
        )
        assert form.get_file_headers_context()
