from model_bakery.recipe import Recipe, foreign_key, related, seq


from killay.archives.lib.constants import PieceConstants
from killay.archives.models import (
    Archive,
    Category,
    Collection,
    Keyword,
    Person,
    Piece,
    PieceMeta,
    Provider,
    Sequence,
)

archive_recipe = Recipe(
    Archive,
    name=seq("Local Archive "),
    slug=seq("local-archive-"),
)

collection_recipe = Recipe(
    Collection,
    name=seq("Local Collection "),
    slug=seq("local-collection-"),
    is_visible=True,
    archive=foreign_key(archive_recipe),
)

category_recipe = Recipe(
    Category,
    name=seq("Local Category "),
    slug=seq("local-category-"),
)

person_recipe = Recipe(
    Person,
    name=seq("Local Person "),
    slug=seq("local-person-"),
)

keyword_recipe = Recipe(
    Keyword,
    name=seq("Local Keyword "),
    slug=seq("local-keyword-"),
)

piece_recipe = Recipe(
    Piece,
    code=seq("local-piece-"),
    is_published=True,
    kind=PieceConstants.KIND_VIDEO,
    collection=foreign_key(collection_recipe),
    categories=related(category_recipe),
    people=related(person_recipe),
    keywords=related(keyword_recipe),
)

piece_meta_recipe = Recipe(PieceMeta, piece=foreign_key(piece_recipe, one_to_one=True))

sequence_recipe = Recipe(
    Sequence,
    piece=foreign_key(piece_recipe),
)

provider_recipe = Recipe(
    Provider,
    piece=foreign_key(piece_recipe),
)
