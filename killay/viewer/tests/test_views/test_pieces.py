import pytest

from killay.archives.lib.constants import PieceConstants
from killay.archives.tests import recipes as archives_recipes


@pytest.mark.django_db
class TestPieceListView:
    path = "/viewer/pieces/"

    def test_default(self, client):
        piece = archives_recipes.piece_recipe.make()
        response = client.get(self.path)
        assert response.status_code == 200
        assert response.context["page_obj"][0].id == piece.id
        assert response.context["specific_context"] is None

    def test_with_query_search(self, client):
        piece = archives_recipes.piece_recipe.make()
        response = client.get(f"{self.path}?search={piece.title}")
        assert response.status_code == 200
        assert response.context["page_obj"][0].id == piece.id
        assert response.context["specific_context"] is None

    def test_with_keyword(self, client):
        piece = archives_recipes.piece_recipe.make()
        keyword = piece.keywords.first()
        response = client.get(f"{self.path}?keyword={keyword.slug}")
        assert response.context["page_obj"][0].id == piece.id
        assert response.context["specific_context"]["title"] == keyword.name

    def test_with_person(self, client):
        piece = archives_recipes.piece_recipe.make()
        person = piece.people.first()
        response = client.get(f"{self.path}?person={person.slug}")
        assert response.context["page_obj"][0].id == piece.id
        assert response.context["specific_context"]["title"] == person.name

    def test_with_category(self, client):
        piece = archives_recipes.piece_recipe.make()
        category = piece.categories.first()
        category.collection_id = piece.collection_id
        category.save()
        response = client.get(
            f"{self.path}?category={category.slug}"
            f"&collection={piece.collection.slug}"
        )
        assert response.context["page_obj"][0].id == piece.id
        assert response.context["specific_context"]["title"] == category.name


@pytest.mark.django_db
class TestPieceDetailView:
    path = "/viewer/pieces/{slug}/"

    def test_video(self, client):
        piece = archives_recipes.piece_recipe.make(kind=PieceConstants.KIND_VIDEO)
        response = client.get(self.path.format(slug=piece.code))
        assert response.status_code == 200
        assert response.context["piece"]["code"] == piece.code

    def test_image(self, client):
        piece = archives_recipes.piece_recipe.make(kind=PieceConstants.KIND_IMAGE)
        response = client.get(self.path.format(slug=piece.code))
        assert response.status_code == 200
        assert response.context["piece"]["code"] == piece.code

    def test_sound(self, client):
        piece = archives_recipes.piece_recipe.make(kind=PieceConstants.KIND_SOUND)
        response = client.get(self.path.format(slug=piece.code))
        assert response.status_code == 200
        assert response.context["piece"]["code"] == piece.code

    def test_document(self, client):
        piece = archives_recipes.piece_recipe.make(kind=PieceConstants.KIND_DOCUMENT)
        response = client.get(self.path.format(slug=piece.code))
        assert response.status_code == 200
        assert response.context["piece"]["code"] == piece.code

    def test_not_found(self, client):
        piece = archives_recipes.piece_recipe.make(is_published=False)
        response = client.get(self.path.format(slug=piece.code))
        assert response.status_code == 404
