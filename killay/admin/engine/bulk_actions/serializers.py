import re

from datetime import date, datetime, time
from typing import Any, Dict, List, Optional

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from killay.admin.lib.constants import BulkActionConstants, BulkActionMessageConstants
from killay.archives.lib.constants import PieceConstants, ProviderConstants
from killay.archives.services import (
    get_all_categories,
    get_all_collections,
    get_meta_pieces_fields_data,
    get_pieces_fields_data,
    get_pieces_queryset,
)


class Serializer:
    fields = {}
    required_fields = []

    def __init__(self, data_list) -> None:
        self._data_list = data_list

    def validate(self) -> List[Dict[str, Any]]:
        self.fetch_data()
        self.errors = {}
        self.validated_data = []
        for row, data in enumerate(self._data_list):
            try:
                val_data = self._validate_data(data=data)
            except ValidationError as error:
                summary = [
                    f"{field}: {';'.join(messages)}"
                    for field, messages in error.message_dict.items()
                ]
                self.errors[row] = summary
            else:
                val_data["row"] = row
                self.validated_data.append(val_data)
        self.validated_data = self.db_validation(validated_data=self.validated_data)
        if self.errors:
            raise ValidationError(self.errors)
        return self.validated_data

    def fetch_data(self) -> None:
        pass

    def db_validation(self, validated_data) -> List:
        return validated_data

    @classmethod
    def get_headers_data(cls) -> Dict[str, Dict]:
        return {
            field: {
                "name": field,
                "is_required": field in cls.required_fields,
                "label": None,
                "description": None,
                "format": BulkActionConstants.FILE_FORMAT_FIELD_DESCRIPTIONS[
                    cls.fields[field]
                ],
            }
            for field in list(cls.fields)
        }

    def _validate_data(self, data: Dict) -> Dict:
        validated_data = {}
        for field, value in data.items():
            if field not in self.fields:
                continue
            value_is_empty = value is None or value == ""
            if value_is_empty and field in self.required_fields:
                self._raise_field_is_required(field=field)
            validated_value = self._validate_field_type(field=field, value=value)
            if hasattr(self, f"validate_{field}"):
                validation_method = getattr(self, f"validate_{field}")
                validated_value = validation_method(value=validated_value)
            value_is_empty = validated_value is None or validated_value == ""
            if value_is_empty and field in self.required_fields:
                self._raise_field_is_required(field=field)
            validated_data[field] = validated_value
        for field in self.required_fields:
            if field not in validated_data:
                self._raise_field_is_required(field=field)
        return validated_data

    def _raise_field_is_required(self, field):
        message = BulkActionConstants.ERROR_FIELD_IS_REQUIRED.format(field=field)
        raise ValidationError({field: message})

    def _validate_field_type(self, field, value):
        field_types = (
            tuple(self.fields[field])
            if isinstance(self.fields[field], (tuple, list))
            else (self.fields[field],)
        )
        if bool in field_types and isinstance(value, str):
            if value.upper() not in BulkActionConstants.BOOL_KEYS:
                message = BulkActionConstants.ERROR_FIELD_BOOL
                raise ValidationError({field: message})
            value = value.upper() != BulkActionConstants.KEY_FALSE
        if list in field_types and isinstance(value, str):
            value = value.split(",") if value else []
        if date in field_types and isinstance(value, str):
            value = self._validate_date(field=field, value=value)
        if time in field_types and isinstance(value, str):
            value = self._validate_time(field=field, value=value)
        if int in field_types and isinstance(value, str) and value.isnumeric():
            value = int(value)
        if value and not isinstance(value, field_types):
            message = BulkActionConstants.ERROR_WRONG_VALUE_TYPE.format(
                field=field, field_types=tuple(_type.__name__ for _type in field_types)
            )
            raise ValidationError({field: message})
        return value

    def _validate_date(self, field: str, value: str):
        def _try_strptime(_value: str, _format: str) -> Optional[date]:
            try:
                returned_value = datetime.strptime(_value, _format)
            except ValueError:
                returned_value = None
            return returned_value

        for date_format in BulkActionConstants.FORMAT_DATES_ALLOWED:
            datetime_value = _try_strptime(_value=value, _format=date_format)
            if datetime_value:
                return datetime_value.date()
        message = BulkActionConstants.ERROR_DATE_WRONG_FORMAT.format(
            value=value, formats=BulkActionConstants.FORMAT_DATES_ALLOWED
        )
        raise ValidationError({field: message})

    def _validate_time(self, field: str, value: str):
        try:
            returned_value = datetime.strptime(value, "%H:%M:%S")
        except ValueError:
            message = BulkActionConstants.ERROR_DATE_WRONG_FORMAT.format(value=value)
            raise ValidationError({field: message})
        return returned_value.time()

    def get_id_from_string(self, value) -> Optional[int]:
        if isinstance(value, int) or value is None:
            return value
        regex = (
            BulkActionConstants.TEMPLATE_ID.replace("[", r"\[")
            .replace("]", r"\]")
            .format(id=r"(\d+)")
        )
        founded = re.findall(regex, value)
        return int(founded[0]) if founded else None

    def _validate_slug(self, field, value) -> bool:
        if bool(re.match(r"^[a-zA-Z][a-zA-Z0-9-_]*[a-zA-Z0-9]$", value)):
            return value
        message = BulkActionConstants.ERROR_FIELD_NOT_SLUG.format(field=field)
        raise ValidationError({"code": message})

    def _get_obj_map(self, field, field_lookup, queryset, data_list):
        obj_values = [data[field] for data in data_list if data.get(field) is not None]
        obj_values = list(set(obj_values))
        filtered = queryset.filter(**{f"{field_lookup}__in": obj_values})
        return {getattr(obj, field_lookup): obj for obj in filtered}

    def _validate_if_exists(self, field, field_lookup, queryset, data_list):
        obj_map = self._get_obj_map(field, field_lookup, queryset, data_list)
        validated_data_list = []
        for row, data in enumerate(data_list):
            value = data.get(field)
            if value and value in obj_map:
                data[field] = obj_map[value]
            elif value:
                message = BulkActionMessageConstants.ERROR_DOES_NOT_EXIST.format(
                    field=field, value=value
                )
                row = data.get("row", row)
                self.errors[row] = self.errors.get(row, []) + [f"{field}: {message}"]
            else:
                data[field] = None
            validated_data_list.append(data)
        return validated_data_list

    def _validate_if_already_exists(self, field, field_lookup, queryset, data_list):
        obj_map = self._get_obj_map(field, field_lookup, queryset, data_list)
        validated_data_list = []
        for row, data in enumerate(data_list):
            value = data.get(field)
            if value and value not in obj_map:
                data[field] = value
            else:
                message = BulkActionMessageConstants.ERROR_ALREADY_EXIST.format(
                    field=field, value=value
                )
                row = data.get("row", row)
                self.errors[row] = self.errors.get(row, []) + [f"{field}: {message}"]

            validated_data_list.append(data)
        return validated_data_list

    def _validate_if_is_repeated(self, field, data_list):
        code_set = set()
        validated_data_list = []
        for row, data in enumerate(data_list):
            value = data.get(field)
            if value and value in code_set:
                message = BulkActionMessageConstants.ERROR_IS_REPEATED.format(
                    field=field, value=value
                )
                row = data.get("row", row)
                self.errors[row] = self.errors.get(row, []) + [f"{field}: {message}"]
            else:
                code_set.add(value)
            validated_data_list.append(data)
        return validated_data_list


class PieceCreateSerializer(Serializer):
    fields = {
        "collection": (str, int),
        "category": (str, int),
        "code": str,
        "title": str,
        "is_published": bool,
        "kind": str,
        "people": list,
        "keywords": list,
        "is_restricted": bool,
        "video_url": str,
        "event": str,
        "description": str,
        "description_date": date,
        "location": str,
        "duration": str,
        "register_date": date,
        "register_author": str,
        "productor": str,
        "notes": str,
        "archivist_notes": str,
        "documentary_unit": str,
        "lang": str,
        "original_format": str,
    }
    required_fields = [
        "collection",
        "code",
        "title",
        "is_published",
        "kind",
    ]

    def validate_collection(self, value):
        return self.get_id_from_string(value=value)

    def validate_category(self, value):
        return self.get_id_from_string(value=value)

    def validate_code(self, value):
        return self._validate_slug(field="code", value=value)

    def validate_kind(self, value):
        if value not in PieceConstants.KIND_LIST:
            message = BulkActionMessageConstants.ERROR_WRONG_KIND.format(
                value=value, kinds=PieceConstants.KIND_LIST
            )
            raise ValidationError({"kind": message})
        return value

    def validate_video_url(self, value):
        if not value:
            return
        try:
            URLValidator(value)
        except ValidationError:
            message = BulkActionMessageConstants.ERROR_WRONG_URL.format(value=value)
            raise ValidationError({"video_url": message})
        if not any(
            provider_name in value
            for provider_name in ProviderConstants.PLYR_PROVIDER_LIST
        ):
            message = BulkActionMessageConstants.ERROR_UNKNOWN_PROVIDER.format(
                value=value, providers=ProviderConstants.PLYR_PROVIDER_LIST
            )
            raise ValidationError({"video_url": message})
        return value

    def db_validation(self, validated_data) -> List:
        validated_data = self._validate_if_exists(
            field="collection",
            field_lookup="id",
            queryset=get_all_collections(),
            data_list=validated_data,
        )
        validated_data = self._validate_if_exists(
            field="category",
            field_lookup="id",
            queryset=get_all_categories(),
            data_list=validated_data,
        )
        validated_data = self._validate_if_is_repeated(
            field="code",
            data_list=validated_data,
        )
        validated_data = self._validate_if_already_exists(
            field="code",
            field_lookup="code",
            queryset=get_pieces_queryset(),
            data_list=validated_data,
        )
        for row, data in enumerate(validated_data):
            collection = data["collection"]
            category = data.get("category")
            if category and collection.id != category.collection_id:
                message = BulkActionMessageConstants.ERROR_NOT_BELONG_TO.format(
                    value=f"{category.name} - {category.id}",
                    type="category",
                    other_value=f"{collection.name} - {collection.id}",
                    other_type="collection",
                )
                row = data.get("row", row)
                self.errors[row] = self.errors.get(row, []) + [f"category: {message}"]

        return validated_data

    @classmethod
    def get_headers_data(cls) -> dict:
        headers_data = super().get_headers_data()
        piece_fields_data = get_pieces_fields_data()
        piece_meta_fields_data = get_meta_pieces_fields_data()
        for column_name, data in headers_data.items():
            field_piece_data = piece_fields_data.get(column_name)
            if field_piece_data:
                data["label"] = field_piece_data.get("label")
                data["description"] = field_piece_data.get("description")
            field_meta_piece_data = piece_meta_fields_data.get(column_name)
            if field_meta_piece_data:
                data["label"] = field_meta_piece_data.get("label")
                data["description"] = field_meta_piece_data.get("description")
        headers_data["category"]["label"] = piece_fields_data["categories"]["label"]
        headers_data["category"]["description"] = piece_fields_data["categories"][
            "description"
        ]
        headers_data["video_url"]["label"] = BulkActionConstants.VIDEO_URL_LABEL
        headers_data["video_url"][
            "description"
        ] = BulkActionConstants.VIDEO_URL_DESCRIPTION
        return headers_data
