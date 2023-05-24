from django.utils.translation import gettext_lazy


class SiteConfigurationConstants:
    FACEBOOK = "facebook"
    TWITTER = "twitter"
    INSTAGRAM = "instagram"
    YOUTUBE = "youtube"
    VIMEO = "vimeo"
    PROVIDER_CHOICES = [
        (FACEBOOK, "Facebook"),
        (TWITTER, "Twitter"),
        (INSTAGRAM, "Instagram"),
        (YOUTUBE, "Youtube"),
        (VIMEO, "Vimeo"),
    ]


class ArchivesViewConstants:
    MAIN_TITLE = gettext_lazy("Archives Content Manager")


def _get_pattern_names(slugs: list, action: str) -> dict:
    return {slug: f"admin:{slug}_{action}" for slug in slugs}


class ContentManagerConstants:
    MAIN_TITLE = gettext_lazy("Content Manager")
    SLUG_ARCHIVE = "archive"
    SLUG_COLLECTION = "collection"
    SLUG_PIECE = "piece"
    SLUG_CATEGORY = "category"
    SLUG_PERSON = "person"
    SLUG_KEYWORD = "keyword"
    VIEW_SLUGS = [
        SLUG_ARCHIVE,
        SLUG_COLLECTION,
        SLUG_PIECE,
        SLUG_CATEGORY,
        SLUG_PERSON,
        SLUG_KEYWORD,
    ]

    NAME_ARCHIVE = gettext_lazy("Archives")
    NAME_COLLECTION = gettext_lazy("Collections")
    NAME_PIECE = gettext_lazy("Pieces")
    NAME_CATEGORY = gettext_lazy("Categories")
    NAME_PERSON = gettext_lazy("People")
    NAME_KEYWORD = gettext_lazy("Keywords")

    VIEWS_SECOND_TITLE = {
        SLUG_ARCHIVE: NAME_ARCHIVE,
        SLUG_COLLECTION: NAME_COLLECTION,
        SLUG_PIECE: NAME_PIECE,
        SLUG_CATEGORY: NAME_CATEGORY,
        SLUG_PERSON: NAME_PERSON,
        SLUG_KEYWORD: NAME_KEYWORD,
    }
    VIEWS_LIST = _get_pattern_names(slugs=VIEW_SLUGS, action="list")
    VIEWS_CREATE = _get_pattern_names(slugs=VIEW_SLUGS, action="create")
    VIEWS_UPDATE = _get_pattern_names(slugs=VIEW_SLUGS, action="update")
    VIEWS_DELETE = _get_pattern_names(slugs=VIEW_SLUGS, action="delete")
    DICT_LINK = {
        SLUG_ARCHIVE: {
            "list": {"view": f"admin:{SLUG_ARCHIVE}_list", "name": NAME_ARCHIVE}
        },
        SLUG_COLLECTION: {
            "list": {"view": f"admin:{SLUG_COLLECTION}_list", "name": NAME_COLLECTION}
        },
        SLUG_PIECE: {"list": {"view": f"admin:{SLUG_PIECE}_list", "name": NAME_PIECE}},
        SLUG_CATEGORY: {
            "list": {"view": f"admin:{SLUG_CATEGORY}_list", "name": NAME_CATEGORY}
        },
        SLUG_PERSON: {
            "list": {"view": f"admin:{SLUG_PERSON}_list", "name": NAME_PERSON}
        },
        SLUG_KEYWORD: {
            "list": {"view": f"admin:{SLUG_KEYWORD}_list", "name": NAME_KEYWORD}
        },
    }
