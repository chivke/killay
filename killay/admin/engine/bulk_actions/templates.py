from typing import List, Optional

from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.worksheet.datavalidation import DataValidation

from killay.admin.lib.constants import BulkActionConstants
from killay.archives.lib.constants import PieceConstants
from killay.archives.services import get_all_categories, get_all_collections


HEADERS_PIECE_CREATE = [
    "collection",
    "category",
    "code",
    "title",
    "is_published",
    "kind",
    "people",
    "keywords",
    "is_restricted",
    "video_url",
    "event",
    "description",
    "descripion_date",
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


class BulkActionTemplateProvider:
    allowed_action_types = {BulkActionConstants.TYPE_PIECE_CREATE: HEADERS_PIECE_CREATE}

    def __init__(self, action_type: str):
        self.action_type = action_type

    def get(self) -> Workbook:
        headers = self._get_headers()
        workbook = self._get_workbook(headers=headers)
        workbook = self._add_choices(workbook=workbook)
        return workbook

    def get_filename(self) -> str:
        return BulkActionConstants.FILE_NAME_TEMPLATE.format(
            action_type=self.action_type
        )

    def _get_headers(self) -> List[str]:
        return self.allowed_action_types[self.action_type]

    def _get_workbook(self, headers: List[str]):
        wb = Workbook()
        ws = wb.active

        ws.append(headers)
        bold_font = Font(bold=True)
        for cell in ws["1:1"]:
            cell.font = bold_font
        return wb

    def _add_choices(self, workbook: Workbook) -> Workbook:
        worksheet = workbook.active
        if self.action_type == BulkActionConstants.TYPE_PIECE_CREATE:
            self._add_piece_create_choices(worksheet=worksheet)
        return workbook

    def _add_piece_create_choices(self, worksheet) -> None:
        self._add_collection_choices(worksheet, col="A", last_row=1000)
        self._add_category_choices(worksheet, col="B", last_row=1000, required=False)
        self._add_bool_choices(worksheet, col="E", last_row=1000)
        self._add_bool_choices(worksheet, col="I", last_row=1000)
        self._add_date_choices(worksheet, col="M", last_row=1000)
        self._add_date_choices(worksheet, col="P", last_row=1000)
        self._add_list_choices(
            worksheet,
            choices=PieceConstants.KIND_LIST,
            col="F",
            last_row=1000,
        )

    def _add_list_choices(self, worksheet, choices, col, last_row, required=True):
        data_validation = DataValidation(
            type="list",
            formula1='"{}"'.format(",".join(choices)),
            allow_blank=(not required),
        )
        self._add_validation(worksheet, data_validation, col, last_row)

    def _add_validation(self, worksheet, data_validation, col, last_row):
        data_validation.add("{col}2:{col}{last_row}".format(col=col, last_row=last_row))
        worksheet.add_data_validation(data_validation)

    def _add_bool_choices(
        self, worksheet, col: str, last_row: int, required: bool = True
    ):
        choices = ["TRUE", "FALSE"]
        data_validation = DataValidation(
            type="list",
            formula1='"{}"'.format(",".join(choices)),
            allow_blank=(not required),
        )
        self._add_validation(worksheet, data_validation, col, last_row)

    def _add_date_choices(
        self, worksheet, col: str, last_row: int, required: bool = True
    ):
        data_validation = DataValidation(type="date", allow_blank=(not required))
        self._add_validation(worksheet, data_validation, col, last_row)

    def _add_choices_by_queryset(
        self,
        worksheet,
        queryset,
        col: str,
        last_row: int,
        required: bool = True,
        field_name: str = "name",
        field_id: str = "id",
        field_extra_name: Optional[str] = None,
    ) -> None:
        choices = []
        for instance in queryset:
            base_name = f"{getattr(instance, field_name)}"
            if field_extra_name:
                extra_name = getattr(instance, field_extra_name)
                if extra_name:
                    base_name = f"{base_name} - ({extra_name})"
            id_string = BulkActionConstants.TEMPLATE_ID.format(
                id=getattr(instance, field_id)
            )
            choice = f"{base_name} | {id_string}"
            choices.append(choice)
        data_validation = DataValidation(
            type="list",
            formula1='"{}"'.format(",".join(choices)),
            allow_blank=(not required),
        )
        self._add_validation(worksheet, data_validation, col, last_row)

    def _add_collection_choices(
        self, worksheet, col: str, last_row: int, required: bool = True
    ) -> None:
        collections = get_all_collections()
        self._add_choices_by_queryset(
            worksheet=worksheet,
            queryset=collections,
            col=col,
            last_row=last_row,
            required=required,
        )

    def _add_category_choices(
        self, worksheet, col: str, last_row: int, required: bool = True
    ) -> None:
        categories = get_all_categories()
        self._add_choices_by_queryset(
            worksheet=worksheet,
            queryset=categories,
            col=col,
            last_row=last_row,
            required=required,
            field_extra_name="collection_slug",
        )
