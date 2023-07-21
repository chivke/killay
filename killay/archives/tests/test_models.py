from datetime import time

import pytest

from killay.archives.tests import recipes as archives_recipes


@pytest.mark.django_db
class TestArchive:
    def test_str(self):
        archive = archives_recipes.archive_recipe.make()
        assert str(archive) == f"{archive.name} <{archive.slug}>"


@pytest.mark.django_db
class TestCollection:
    def test_str(self):
        collection = archives_recipes.collection_recipe.make()
        assert str(collection) == f"{collection.name} <{collection.slug}>"

    def test_archive_slug(self):
        collection = archives_recipes.collection_recipe.make()
        assert collection.archive_slug == collection.archive.slug


@pytest.mark.django_db
class TestCategory:
    def test_str(self):
        category = archives_recipes.category_recipe.make()
        assert str(category) == category.name

    def test_archive_slug(self):
        collection = archives_recipes.collection_recipe.make()
        category = archives_recipes.category_recipe.make(collection_id=collection.id)
        assert category.archive_slug == collection.archive.slug

    def test_collection_slug(self):
        collection = archives_recipes.collection_recipe.make()
        category = archives_recipes.category_recipe.make(collection_id=collection.id)
        assert category.collection_slug == collection.slug


@pytest.mark.django_db
class TestPerson:
    def test_str(self):
        person = archives_recipes.person_recipe.make()
        assert str(person) == person.name


@pytest.mark.django_db
class TestKeyword:
    def test_str(self):
        keyword = archives_recipes.keyword_recipe.make()
        assert str(keyword) == keyword.name


@pytest.mark.django_db
class TestPiece:
    def test_str(self):
        piece = archives_recipes.piece_recipe.make()
        assert str(piece) == f"Piece <{piece.code}>"

    def test_active_provider(self):
        piece = archives_recipes.piece_recipe.make()
        provider = archives_recipes.provider_recipe.make(active=True, piece_id=piece.id)
        assert piece.active_provider.id == provider.id


@pytest.mark.django_db
class TestSequence:
    def test_str(self):
        sequence = archives_recipes.sequence_recipe.make()
        assert str(sequence) == f"Sequence <{sequence.id}>"

    def test_ini_sec(self):
        sequence = archives_recipes.sequence_recipe.make(ini=time(1))
        assert sequence.ini_sec == 3600

    def test_end_sec(self):
        sequence = archives_recipes.sequence_recipe.make(end=time(1))
        assert sequence.ini_sec == 3600


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
        piece = archives_recipes.piece_recipe.make()
        piece.save()
        assert str(piece.meta) == f"PieceMeta <of {piece.id}>"
