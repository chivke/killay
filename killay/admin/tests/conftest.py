import pytest
from openpyxl import Workbook

from killay.admin.lib.constants import BulkActionConstants
from killay.archives.tests import recipes as archives_recipes


@pytest.fixture
def bulk_action_piece_create_success_wb():
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
    return workbook
