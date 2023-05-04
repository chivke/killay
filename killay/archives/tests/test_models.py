import pytest

from killay.archives.tests import recipes as archives_recipes


@pytest.mark.django_db
class TestArchive:
    def test_str(self):
        archive = archives_recipes.archive_recipe.make()
        assert str(archive) == f"Archive <{archive.name}>"


@pytest.mark.django_db
class TestCollection:
    def test_str(self):
        collection = archives_recipes.collection_recipe.make()
        assert str(collection) == f"Collection <{collection.name}>"


@pytest.mark.django_db
class TestCategory:
    def test_str(self):
        category = archives_recipes.category_recipe.make()
        assert str(category) == f"Category <{category.name}>"


@pytest.mark.django_db
class TestPerson:
    def test_str(self):
        person = archives_recipes.person_recipe.make()
        assert str(person) == f"Person <{person.name}>"


@pytest.mark.django_db
class TestKeyword:
    def test_str(self):
        keyword = archives_recipes.keyword_recipe.make()
        assert str(keyword) == f"Keyword <{keyword.name}>"


@pytest.mark.django_db
class TestPiece:
    def test_str(self):
        piece = archives_recipes.piece_recipe.make()
        assert str(piece) == f"Piece <{piece.code}>"


@pytest.mark.django_db
class TestSequence:
    def test_str(self):
        sequence = archives_recipes.sequence_recipe.make()
        assert str(sequence) == f"Sequence <{sequence.id}>"


@pytest.mark.django_db
class TestProvider:
    def test_str(self):
        provider = archives_recipes.provider_recipe.make()
        assert (
            str(provider)
            == f"Provider <{provider.ply_embed_id}, {provider.plyr_provider}>"
        )


@pytest.mark.django_db
class TestPieceMeta:
    def test_str(self):
        meta = archives_recipes.piece_meta_recipe.make()
        assert str(meta) == f"PieceMeta <of {meta.piece_id}>"
