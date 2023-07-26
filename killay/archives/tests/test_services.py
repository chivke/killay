import pytest

from killay.archives import services as archives_services
from killay.archives.tests import recipes as archives_recipes
from killay.archives.models import Collection


@pytest.fixture
def archive():
    return archives_recipes.archive_recipe.make()


@pytest.fixture
def collection():
    return archives_recipes.collection_recipe.make()


@pytest.fixture
def place():
    return archives_recipes.place_address_recipe.make().place


@pytest.fixture
def piece():
    return archives_recipes.piece_recipe.make()


@pytest.mark.django_db
def test_get_archive_names_and_slugs(archive):
    archives_names_and_slugs = archives_services.get_archive_names_and_slugs()
    assert_fields = ["slug", "name"]
    for field in assert_fields:
        assert getattr(archive, field) == archives_names_and_slugs[0][field]


@pytest.mark.django_db
def test_get_archive_related_field_data(archive):
    related_field_data = archives_services.get_archive_related_field_data(
        archive_id=archive.id
    )
    collection_field = Collection._meta.verbose_name_plural.capitalize()
    assert related_field_data[collection_field] == archive.collections.count()


@pytest.mark.django_db
class TestGetPublicArchives:
    def test_without_place_and_not_superuser(self, archive):
        public_archives = archives_services.get_public_archives()
        assert public_archives[0].id == archive.id

    def test_not_is_visible(self, archive):
        archive.is_visible = False
        archive.save()
        public_archives = archives_services.get_public_archives()
        assert not public_archives

    def test_not_is_visible_superuser(self, archive):
        archive.is_visible = False
        archive.save()
        public_archives = archives_services.get_public_archives(is_superuser=True)
        assert public_archives[0].id == archive.id

    def test_is_restricted(self, archive):
        archive.is_restricted = True
        archive.save()
        public_archives = archives_services.get_public_archives()
        assert not public_archives

    def test_is_restricted_with_superuser(self, archive):
        archive.is_restricted = True
        archive.save()
        public_archives = archives_services.get_public_archives(is_superuser=True)
        assert public_archives[0].id == archive.id

    def test_is_restricted_with_place(self, archive, place):
        archive.is_restricted = True
        archive.save()
        place.allowed_archives.add(archive.id)
        public_archives = archives_services.get_public_archives(place=place)
        assert public_archives[0].id == archive.id


@pytest.mark.django_db
class TestGetPublicArchiveBySlug:
    def test_without_place_and_not_superuser(self, archive):
        public_archive = archives_services.get_public_archive_by_slug(slug=archive.slug)
        assert public_archive.id == archive.id

    def test_not_is_visible(self, archive):
        archive.is_visible = False
        archive.save()
        public_archive = archives_services.get_public_archive_by_slug(slug=archive.slug)
        assert not public_archive

    def test_not_is_visible_superuser(self, archive):
        archive.is_visible = False
        archive.save()
        public_archive = archives_services.get_public_archive_by_slug(
            slug=archive.slug,
            is_superuser=True,
        )
        assert public_archive.id == archive.id

    def test_is_restricted(self, archive):
        archive.is_restricted = True
        archive.save()
        public_archive = archives_services.get_public_archive_by_slug(slug=archive.slug)
        assert not public_archive

    def test_is_restricted_with_superuser(self, archive):
        archive.is_restricted = True
        archive.save()
        public_archive = archives_services.get_public_archive_by_slug(
            slug=archive.slug,
            is_superuser=True,
        )
        assert public_archive.id == archive.id

    def test_is_restricted_with_place(self, archive, place):
        archive.is_restricted = True
        archive.save()
        place.allowed_archives.add(archive.id)
        public_archive = archives_services.get_public_archive_by_slug(
            slug=archive.slug,
            place=place,
        )
        assert public_archive.id == archive.id


@pytest.mark.django_db
class TestGetPublicCollectionsByArchiveID:
    def test_without_place_and_not_superuser(self, collection):
        public_collections = archives_services.get_public_collections_by_archive_id(
            archive_id=collection.archive_id
        )
        assert public_collections[0].id == collection.id

    def test_not_is_visible(self, collection):
        collection.is_visible = False
        collection.save()
        public_collections = archives_services.get_public_collections_by_archive_id(
            archive_id=collection.archive_id
        )
        assert not public_collections

    def test_not_is_visible_superuser(self, collection):
        collection.is_visible = False
        collection.save()
        public_collections = archives_services.get_public_collections_by_archive_id(
            archive_id=collection.archive_id, is_superuser=True
        )
        assert public_collections[0].id == collection.id

    def test_is_restricted(self, collection):
        collection.is_restricted = True
        collection.save()
        public_collections = archives_services.get_public_collections_by_archive_id(
            archive_id=collection.archive_id
        )
        assert not public_collections

    def test_is_restricted_with_superuser(self, collection):
        collection.is_restricted = True
        collection.save()
        public_collections = archives_services.get_public_collections_by_archive_id(
            archive_id=collection.archive_id,
            is_superuser=True,
        )
        assert public_collections[0].id == collection.id

    def test_is_restricted_with_place(self, collection, place):
        collection.is_restricted = True
        collection.save()
        place.allowed_collections.add(collection.id)
        public_collections = archives_services.get_public_collections_by_archive_id(
            archive_id=collection.archive_id, place=place
        )
        assert public_collections[0].id == collection.id

    def test_archive_is_restricted(self, collection):
        collection.archive.is_restricted = True
        collection.archive.save()
        public_collections = archives_services.get_public_collections_by_archive_id(
            archive_id=collection.archive_id
        )
        assert not public_collections

    def test_archive_is_restricted_with_superuser(self, collection):
        collection.archive.is_restricted = True
        collection.archive.save()
        public_collections = archives_services.get_public_collections_by_archive_id(
            archive_id=collection.archive_id,
            is_superuser=True,
        )
        assert public_collections[0].id == collection.id

    def test_archive_is_restricted_with_place(self, collection, place):
        collection.archive.is_restricted = True
        collection.archive.save()
        place.allowed_archives.add(collection.archive_id)
        public_collections = archives_services.get_public_collections_by_archive_id(
            archive_id=collection.archive_id, place=place
        )
        assert public_collections[0].id == collection.id


@pytest.mark.django_db
class TestGetPublicCollectionBySlug:
    def test_without_place_and_not_superuser(self, collection):
        public_collection = archives_services.get_public_collection_by_slug(
            slug=collection.slug
        )
        assert public_collection.id == collection.id

    def test_not_is_visible(self, collection):
        collection.is_visible = False
        collection.save()
        public_collection = archives_services.get_public_collection_by_slug(
            slug=collection.slug,
            archive_id=collection.archive_id,
        )
        assert not public_collection

    def test_not_is_visible_superuser(self, collection):
        collection.is_visible = False
        collection.save()
        public_collection = archives_services.get_public_collection_by_slug(
            slug=collection.slug,
            archive_id=collection.archive_id,
            is_superuser=True,
        )
        assert public_collection.id == collection.id

    def test_is_restricted(self, collection):
        collection.is_restricted = True
        collection.save()
        public_collection = archives_services.get_public_collection_by_slug(
            archive_id=collection.archive_id, slug=collection.slug
        )
        assert not public_collection

    def test_is_restricted_with_superuser(self, collection):
        collection.is_restricted = True
        collection.save()
        public_collection = archives_services.get_public_collection_by_slug(
            slug=collection.slug,
            archive_id=collection.archive_id,
            is_superuser=True,
        )
        assert public_collection.id == collection.id

    def test_is_restricted_with_place(self, collection, place):
        collection.is_restricted = True
        collection.save()
        place.allowed_collections.add(collection.id)
        public_collection = archives_services.get_public_collection_by_slug(
            slug=collection.slug,
            archive_id=collection.archive_id,
            place=place,
        )
        assert public_collection.id == collection.id

    def test_archive_is_restricted(self, collection):
        collection.archive.is_restricted = True
        collection.archive.save()
        public_collection = archives_services.get_public_collection_by_slug(
            archive_id=collection.archive_id, slug=collection.slug
        )
        assert not public_collection

    def test_archive_is_restricted_with_superuser(self, collection):
        collection.archive.is_restricted = True
        collection.archive.save()
        public_collection = archives_services.get_public_collection_by_slug(
            slug=collection.slug,
            archive_id=collection.archive_id,
            is_superuser=True,
        )
        assert public_collection.id == collection.id

    def test_archive_is_restricted_with_place(self, collection, place):
        collection.archive.is_restricted = True
        collection.archive.save()
        place.allowed_archives.add(collection.archive_id)
        public_collection = archives_services.get_public_collection_by_slug(
            slug=collection.slug,
            archive_id=collection.archive_id,
            place=place,
        )
        assert public_collection.id == collection.id


@pytest.mark.django_db
def test_get_category():
    category = archives_recipes.category_recipe.make()
    result = archives_services.get_category_by_slug(
        slug=category.slug, collection_id=category.collection_id
    )
    assert category.id == result.id


@pytest.mark.django_db
def test_get_person():
    person = archives_recipes.person_recipe.make()
    result = archives_services.get_person_by_slug(slug=person.slug)
    assert person.id == result.id


@pytest.mark.django_db
def test_get_keyword():
    keyword = archives_recipes.keyword_recipe.make()
    result = archives_services.get_keyword_by_slug(slug=keyword.slug)
    assert keyword.id == result.id


@pytest.mark.django_db
class TestGetPublicPieces:
    def test_without_params(self, piece):
        public_pieces = archives_services.get_public_pieces()
        assert public_pieces[0].id == piece.id

    def test_with_category(self, piece):
        category = archives_recipes.category_recipe.make(
            collection_id=piece.collection_id
        )
        piece.categories.add(category.id)
        categorization = {"category": category}
        public_pieces = archives_services.get_public_pieces(
            categorization=categorization
        )
        assert public_pieces[0].id == piece.id

    def test_with_person(self, piece):
        person = archives_recipes.person_recipe.make()
        piece.people.add(person.id)
        categorization = {"person": person}
        public_pieces = archives_services.get_public_pieces(
            categorization=categorization
        )
        assert public_pieces[0].id == piece.id

    def test_with_keyword(self, piece):
        keyword = archives_recipes.keyword_recipe.make()
        piece.keywords.add(keyword.id)
        categorization = {"keyword": keyword}
        public_pieces = archives_services.get_public_pieces(
            categorization=categorization
        )
        assert public_pieces[0].id == piece.id

    def test_with_collection(self, piece):
        public_pieces = archives_services.get_public_pieces(collection=piece.collection)
        assert public_pieces[0].id == piece.id

    def test_with_archive(self, piece):
        public_pieces = archives_services.get_public_pieces(
            archive=piece.collection.archive
        )
        assert public_pieces[0].id == piece.id

    def test_with_kind(self, piece):
        public_pieces = archives_services.get_public_pieces(kind=piece.kind)
        assert public_pieces[0].id == piece.id

    def test_with_query_search(self, piece):
        public_pieces = archives_services.get_public_pieces(
            query_search=piece.title[:-1]
        )
        assert public_pieces[0].id == piece.id

    def test_is_not_pusblished(seld, piece):
        piece.is_published = False
        piece.save()
        public_pieces = archives_services.get_public_pieces()
        assert not public_pieces

    def test_is_not_pusblished_with_superuser(seld, piece):
        piece.is_published = False
        piece.save()
        public_pieces = archives_services.get_public_pieces(is_superuser=True)
        assert public_pieces[0].id == piece.id

    def test_is_restricted(self, piece):
        piece.is_restricted = True
        piece.save()
        public_pieces = archives_services.get_public_pieces()
        assert not public_pieces

    def test_is_restricted_with_superuser(self, piece):
        piece.is_restricted = True
        piece.save()
        public_pieces = archives_services.get_public_pieces(is_superuser=True)
        assert public_pieces[0].id == piece.id

    def test_is_restricted_with_place(self, piece, place):
        piece.is_restricted = True
        piece.save()
        place.allowed_pieces.add(piece.id)
        public_pieces = archives_services.get_public_pieces(place=place)
        assert public_pieces[0].id == piece.id

    def test_archive_is_restricted(self, piece):
        piece.collection.archive.is_restricted = True
        piece.collection.archive.save()
        public_pieces = archives_services.get_public_pieces()
        assert not public_pieces

    def test_archive_is_restricted_with_superuser(self, piece):
        piece.collection.archive.is_restricted = True
        piece.collection.archive.save()
        public_pieces = archives_services.get_public_pieces(is_superuser=True)
        assert public_pieces[0].id == piece.id

    def test_archive_is_restricted_with_place(self, piece, place):
        piece.collection.archive.is_restricted = True
        piece.collection.archive.save()
        place.allowed_archives.add(piece.collection.archive_id)
        public_pieces = archives_services.get_public_pieces(place=place)
        assert public_pieces[0].id == piece.id

    def test_collection_is_restricted(self, piece):
        piece.collection.is_restricted = True
        piece.collection.save()
        public_pieces = archives_services.get_public_pieces()
        assert not public_pieces

    def test_collection_is_restricted_with_superuser(self, piece):
        piece.collection.is_restricted = True
        piece.collection.save()
        public_pieces = archives_services.get_public_pieces(is_superuser=True)
        assert public_pieces[0].id == piece.id

    def test_collection_is_restricted_with_place(self, piece, place):
        piece.collection.is_restricted = True
        piece.collection.save()
        place.allowed_collections.add(piece.collection_id)
        public_pieces = archives_services.get_public_pieces(place=place)
        assert public_pieces[0].id == piece.id


@pytest.mark.django_db
class TestGetPublicPiece:
    def test_normal(self, piece):
        public_piece = archives_services.get_public_piece(piece_code=piece.code)
        assert public_piece.id == piece.id

    def test_is_not_pusblished(seld, piece):
        piece.is_published = False
        piece.save()
        public_piece = archives_services.get_public_piece(piece_code=piece.code)
        assert not public_piece

    def test_is_not_pusblished_with_superuser(seld, piece):
        piece.is_published = False
        piece.save()
        public_piece = archives_services.get_public_piece(
            piece_code=piece.code, is_superuser=True
        )
        assert public_piece.id == piece.id

    def test_is_restricted(self, piece):
        piece.is_restricted = True
        piece.save()
        public_piece = archives_services.get_public_piece(piece_code=piece.code)
        assert not public_piece

    def test_is_restricted_with_superuser(self, piece):
        piece.is_restricted = True
        piece.save()
        public_piece = archives_services.get_public_piece(
            piece_code=piece.code,
            is_superuser=True,
        )
        assert public_piece.id == piece.id

    def test_is_restricted_with_place(self, piece, place):
        piece.is_restricted = True
        piece.save()
        place.allowed_pieces.add(piece.id)
        public_piece = archives_services.get_public_piece(
            piece_code=piece.code,
            place=place,
        )
        assert public_piece.id == piece.id

    def test_archive_is_restricted(self, piece):
        piece.collection.archive.is_restricted = True
        piece.collection.archive.save()
        public_piece = archives_services.get_public_piece(
            piece_code=piece.code,
        )
        assert not public_piece

    def test_archive_is_restricted_with_superuser(self, piece):
        piece.collection.archive.is_restricted = True
        piece.collection.archive.save()
        public_piece = archives_services.get_public_piece(
            piece_code=piece.code, is_superuser=True
        )
        assert public_piece.id == piece.id

    def test_archive_is_restricted_with_place(self, piece, place):
        piece.collection.archive.is_restricted = True
        piece.collection.archive.save()
        place.allowed_archives.add(piece.collection.archive_id)
        public_piece = archives_services.get_public_piece(
            piece_code=piece.code,
            place=place,
        )
        assert public_piece.id == piece.id

    def test_collection_is_restricted(self, piece):
        piece.collection.is_restricted = True
        piece.collection.save()
        public_piece = archives_services.get_public_piece(
            piece_code=piece.code,
        )
        assert not public_piece

    def test_collection_is_restricted_with_superuser(self, piece):
        piece.collection.is_restricted = True
        piece.collection.save()
        public_piece = archives_services.get_public_piece(
            piece_code=piece.code, is_superuser=True
        )
        assert public_piece.id == piece.id

    def test_collection_is_restricted_with_place(self, piece, place):
        piece.collection.is_restricted = True
        piece.collection.save()
        place.allowed_collections.add(piece.collection_id)
        public_piece = archives_services.get_public_piece(
            piece_code=piece.code,
            place=place,
        )
        assert public_piece.id == piece.id


@pytest.mark.django_db
def test_get_archive_filter_options(archive):
    result = archives_services.get_archive_filter_options()
    assert result[0]["label"] == archive.name
    assert result[0]["slug"] == archive.slug
    assert result[0]["active"] is False


@pytest.mark.django_db
def test_get_collection_filter_options(collection):
    result = archives_services.get_collection_filter_options()
    assert result[0]["label"] == collection.name
    assert result[0]["slug"] == collection.slug
    assert result[0]["archive_slug"] == collection.archive.slug
    assert result[0]["active"] is False


@pytest.mark.django_db
def test_get_category_filter_options():
    category = archives_recipes.category_recipe.make()
    result = archives_services.get_category_filter_options()
    assert result[0]["label"] == category.name
    assert result[0]["slug"] == category.slug
    assert result[0]["active"] is False


@pytest.mark.django_db
def test_get_person_filter_options():
    person = archives_recipes.person_recipe.make()
    result = archives_services.get_person_filter_options()
    assert result[0]["label"] == person.name
    assert result[0]["slug"] == person.slug
    assert result[0]["active"] is False


@pytest.mark.django_db
def test_get_keyword_filter_options():
    keyword = archives_recipes.keyword_recipe.make()
    result = archives_services.get_keyword_filter_options()
    assert result[0]["label"] == keyword.name
    assert result[0]["slug"] == keyword.slug
    assert result[0]["active"] is False
