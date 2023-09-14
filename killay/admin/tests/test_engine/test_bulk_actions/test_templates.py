import pytest


from killay.admin.engine.bulk_actions.templates import BulkActionTemplateProvider
from killay.admin.lib.constants import BulkActionConstants
from killay.archives.tests import recipes as archives_recipes


@pytest.mark.django_db
def test_piece_create():
    collection = archives_recipes.collection_recipe.make()
    archives_recipes.category_recipe.make(collection_id=collection.id)

    action_type = BulkActionConstants.TYPE_PIECE_CREATE
    provider = BulkActionTemplateProvider(action_type=action_type)
    expected_headers = provider._get_headers()
    workbook = provider.get()
    worksheet = workbook.active
    for index, header in enumerate(expected_headers):
        assert worksheet.cell(1, index + 1).value == header

    assert provider.get_filename() == f"template_{action_type}.xlsx"
