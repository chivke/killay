from datetime import date

from django.core.exceptions import ValidationError

import pytest

from killay.admin.engine.bulk_actions.serializers import (
    PieceCreateSerializer,
    Serializer,
)
from killay.admin.lib.constants import BulkActionConstants

from killay.archives.tests import recipes as archives_recipes


@pytest.fixture
def get_fake_serializer_class():
    def _get(fields, required_fields=None):
        class FakeSerializer(Serializer):
            pass

        serializer_class = FakeSerializer
        serializer_class.fields = fields
        if required_fields:
            serializer_class.required_fields = required_fields
        return serializer_class

    return _get


class TestSerializer:
    def test_validate_all_right(self, get_fake_serializer_class):
        fields = {
            "string": str,
            "bool": bool,
            "int": int,
            "date": date,
            "str_int": (str, int),
            "list": list,
        }
        sucess_data = {
            "string": "fake string",
            "bool": "FALSE",
            "int": "123",
            "date": "2000-01-01",
            "str_int": "fake choice - [123]",
            "list": "fake,list,of,strings",
        }
        data_list = [sucess_data]
        serializer_class = get_fake_serializer_class(fields=fields)
        serializer = serializer_class(data_list=data_list)
        validated_data = serializer.validate()
        assert isinstance(validated_data[0]["bool"], bool)
        assert validated_data[0]["int"] == 123
        assert validated_data[0]["date"] == date(2000, 1, 1)
        assert validated_data[0]["list"] == ["fake", "list", "of", "strings"]

    def test_validate_required(self, get_fake_serializer_class):
        fields = {"required": str}
        serializer_class = get_fake_serializer_class(
            fields=fields, required_fields=fields
        )
        data_list = [{}, {"required": ""}]
        serializer = serializer_class(data_list=data_list)
        try:
            serializer.validate()
        except ValidationError as _error:
            error = _error
        else:
            assert False, "Must be failed"
        expected_message = "required: required field is required"
        assert 0 in error.error_dict
        assert 1 in error.error_dict
        assert error.message_dict[0][0] == expected_message
        assert error.message_dict[1][0] == expected_message

    def test_validate_type_bool(self, get_fake_serializer_class):
        fields = {"bool": bool}
        serializer_class = get_fake_serializer_class(fields=fields)
        data_list = [{"bool": "false"}, {"bool": "true"}, {"bool": "FASE"}]
        serializer = serializer_class(data_list=data_list)
        try:
            serializer.validate()
        except ValidationError as _error:
            error = _error
        else:
            assert False, "Must be failed"
        assert 2 in error.error_dict
        assert len(error.error_dict) == 1
        expected_message = 'bool: Must be "TRUE" or "FALSE"'
        assert error.message_dict[2][0] == expected_message

    def test_validate_type_list(self, get_fake_serializer_class):
        fields = {"list": list}
        data_list = [{"list": ""}, {"list": "word,wor"}, {"list": "drow"}]
        serializer_class = get_fake_serializer_class(fields=fields)
        serializer = serializer_class(data_list=data_list)
        validated_data = serializer.validate()
        assert validated_data[0]["list"] == []
        assert validated_data[1]["list"] == ["word", "wor"]
        assert validated_data[2]["list"] == ["drow"]

    def test_validate_type_int(self, get_fake_serializer_class):
        fields = {"int": int}
        serializer_class = get_fake_serializer_class(fields=fields)
        data_list = [
            {"int": "e"},
        ]
        serializer = serializer_class(data_list=data_list)
        try:
            serializer.validate()
        except ValidationError as _error:
            error = _error
        else:
            assert False, "Must be failed"
        expected_message = "int: Wrong value type for int field, must be ('int',)"
        assert 0 in error.error_dict
        assert error.message_dict[0][0] == expected_message

    def test_validate_type_date(self, get_fake_serializer_class):
        fields = {"date": date}
        serializer_class = get_fake_serializer_class(fields=fields)
        data_list = [
            {"date": "2000-01-01"},
            {"date": "2000-1-1"},
            {"date": "2000/01/01"},
            {"date": "2000/1/1"},
            {"date": "01-01-2000"},
            {"date": "1-1-2000"},
            {"date": "01/01/2000"},
            {"date": "01/01/2000"},
            {"date": "asd"},  # wrong
        ]
        serializer = serializer_class(data_list=data_list)
        try:
            serializer.validate()
        except ValidationError as _error:
            error = _error
        else:
            assert False, "Must be failed"

        assert 8 in error.error_dict
        assert len(error.error_dict) == 1
        assert all(
            data["date"] == date(2000, 1, 1) for data in serializer.validated_data
        )

        expected_message = (
            "date: date 'asd' does not match formats "
            "['%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y', '%d/%m/%Y']"
        )
        assert error.message_dict[8][0] == expected_message


@pytest.mark.django_db
class TestPieceCreateSerializer:
    def test_validate_all_right(self):
        collection = archives_recipes.collection_recipe.make()
        collection_string = (
            f"{collection.name} "
            f"| {BulkActionConstants.TEMPLATE_ID.format(id=collection.id)}"
        )
        category = archives_recipes.category_recipe.make(collection_id=collection.id)
        sucess_data = {
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
        serializer = PieceCreateSerializer(data_list=[sucess_data])
        validated_data = serializer.validate()
        assert validated_data[0]["collection"] == collection
        assert validated_data[0]["category"] == category

    def test_validate_bad_collection(self):
        collection = archives_recipes.collection_recipe.make()
        collection_string = (
            f"{collection.name} "
            f"| {BulkActionConstants.TEMPLATE_ID.format(id=collection.id)}"
        )
        sucess_data = {
            "collection": collection_string,
            "code": "fake-code",
            "title": "fake",
            "is_published": "TRUE",
            "kind": "VIDEO",
        }
        wrong_data = {**sucess_data, "collection": "text_with_no_id"}
        wrong_id_data = {**sucess_data, "collection": "999"}
        serializer = PieceCreateSerializer(
            data_list=[sucess_data, wrong_data, wrong_id_data]
        )
        try:
            serializer.validate()
        except ValidationError as _error:
            error = _error
        else:
            assert False, "Must be failed"

        assert 1 in error.error_dict
        assert len(error.error_dict) == 2
        expected_message = "collection: collection field is required"
        assert error.message_dict[1][0] == expected_message
        expected_message = "collection: 999 for collection field does not exist"
        assert error.message_dict[2][0] == expected_message

    def test_validate_bad_kind(self):
        collection = archives_recipes.collection_recipe.make()
        wrong_data = {
            "collection": collection.id,
            "code": "fake-code",
            "title": "fake",
            "is_published": "TRUE",
            "kind": "BIDEO",
        }
        serializer = PieceCreateSerializer(data_list=[wrong_data])
        try:
            serializer.validate()
        except ValidationError as _error:
            error = _error
        else:
            assert False, "Must be failed"

        assert 0 in error.error_dict
        expected_message = (
            "kind: BIDEO is not a valid kind, must use: "
            "['VIDEO', 'IMAGE', 'SOUND', 'DOCUMENT']"
        )
        assert error.message_dict[0][0] == expected_message

    def test_wrong_video_url(self):
        collection = archives_recipes.collection_recipe.make()
        wrong_data = {
            "collection": collection.id,
            "code": "fake-code",
            "title": "fake",
            "is_published": "TRUE",
            "kind": "VIDEO",
            "video_url": "not_url",
        }
        wrong_provider_data = {**wrong_data, "video_url": "https://no.provider"}
        serializer = PieceCreateSerializer(data_list=[wrong_data, wrong_provider_data])
        try:
            serializer.validate()
        except ValidationError as _error:
            error = _error
        else:
            assert False, "Must be failed"

        assert 0 in error.error_dict
        assert 1 in error.error_dict
        expected_message = (
            'video_url: url "not_url" is not from a '
            "known provider, must be: ['youtube', 'vimeo']"
        )
        assert error.message_dict[0][0] == expected_message
        expected_message = (
            'video_url: url "https://no.provider" is not from a known '
            "provider, must be: ['youtube', 'vimeo']"
        )
        assert error.message_dict[1][0] == expected_message

    def test_validate_wrong_category_collection(self):
        collection = archives_recipes.collection_recipe.make()
        category = archives_recipes.category_recipe.make()
        wrong_data = {
            "collection": collection.id,
            "category": category.id,
            "code": "fake-code",
            "title": "fake",
            "is_published": "TRUE",
            "kind": "VIDEO",
        }
        serializer = PieceCreateSerializer(data_list=[wrong_data])
        try:
            serializer.validate()
        except ValidationError as _error:
            error = _error
        else:
            assert False, "Must be failed"

        assert 0 in error.error_dict
        expected_message = (
            f"category: {category.name} - {category.id} category not belog "
            f"to {collection.name} - {collection.id} collection"
        )
        assert error.message_dict[0][0] == expected_message

    def test_code_repeated(self):
        collection = archives_recipes.collection_recipe.make()
        wrong_data = {
            "collection": collection.id,
            "code": "fake-code",
            "title": "fake",
            "is_published": "TRUE",
            "kind": "VIDEO",
        }
        serializer = PieceCreateSerializer(data_list=[wrong_data, wrong_data])
        try:
            serializer.validate()
        except ValidationError as _error:
            error = _error
        else:
            assert False, "Must be failed"

        assert 1 in error.error_dict
        expected_message = "code: fake-code for code is repeated"
        assert error.message_dict[1][0] == expected_message

    def test_code_already_exist(self):
        piece = archives_recipes.piece_recipe.make()
        wrong_data = {
            "collection": piece.collection_id,
            "code": piece.code,
            "title": "fake",
            "is_published": "TRUE",
            "kind": "VIDEO",
        }
        serializer = PieceCreateSerializer(data_list=[wrong_data])
        try:
            serializer.validate()
        except ValidationError as _error:
            error = _error
        else:
            assert False, "Must be failed"

        assert 0 in error.error_dict
        expected_message = f"code: {piece.code} for code field already exist"
        assert error.message_dict[0][0] == expected_message

    def test_get_headers_data(self):
        headers_data = PieceCreateSerializer.get_headers_data()
        assert headers_data
