from django.utils.translation import gettext_lazy


class SiteContextConstants:
    NAME_ALL = gettext_lazy("All")
    NAME_LOGIN = gettext_lazy("Log In")
    NAME_LOGOUT = gettext_lazy("Log Out")
    PATTERN_USER_UPDATE = "users:update"
    PATTERN_LOGIN = "users:login"
    PATTERN_LOGOUT = "users:logout"


class ViewerConstants:
    APP_NAME = "viewer"
    NAME_SCOPE = gettext_lazy("Scope")
    NAME_HOME = gettext_lazy("Home")
    SCOPE_ALL = "ALL"
    SCOPE_ONE_ARCHIVE = "ONE_ARCHIVE"
    SCOPE_ONE_COLLECTION = "ONE_COLLECTION"
    SCOPE_CHOICES = [
        (SCOPE_ALL, gettext_lazy("All")),
        (SCOPE_ONE_ARCHIVE, gettext_lazy("One Archive")),
        (SCOPE_ONE_COLLECTION, gettext_lazy("One Collection")),
    ]
    HOME_PAGE = "PAGE"
    HOME_DEFAULT = "DEFAULT"
    HOME_CHOICES = [
        (HOME_PAGE, gettext_lazy("Page")),
        (HOME_DEFAULT, gettext_lazy("Default")),
    ]
    HELP_TEXT_SCOPE = gettext_lazy(
        "Determines the scope of the content to be viewed by the public, "
        "which can be reduced to a single archive or collection"
    )
    HELP_TEXT_SCOPE_ARCHIVE = gettext_lazy(
        "In case of selecting the scope in a single archive, "
        "the archive must be specified"
    )
    HELP_TEXT_SCOPE_COLLECTION = gettext_lazy(
        "In case of selecting the scope in a single collection, "
        "the collection must be specified"
    )
    HELP_TEXT_HOME = gettext_lazy(
        "Indicates if the home page will be used by default "
        "(depending on the scope) or a specific page will be assigned"
    )
    HELP_TEXT_HOME_PAGE = gettext_lazy(
        "In case of selecting the home by page this must be selected"
    )

    ERROR_SCOPE_ONE_ARCHIVE = gettext_lazy(
        "The one archive option requires to be specified"
    )
    ERROR_SCOPE_ONE_COLLECTION = gettext_lazy(
        "The one collection option requires to be specified"
    )

    KEY_ARCHIVE = "archive"
    KEY_COLLECTION = "collection"
    KEY_CATEGORY = "category"
    KEY_PERSON = "person"
    KEY_KEYWORD = "keyword"
    KEY_SEARCH = "search"
    KEY_KIND = "kind"
    CURSOR_KEYS = [
        KEY_ARCHIVE,
        KEY_COLLECTION,
        KEY_CATEGORY,
        KEY_PERSON,
        KEY_KEYWORD,
        KEY_SEARCH,
        KEY_KIND,
    ]


class ViewerPatternConstants:
    APP_NAME = "viewer"
    ROOT = "root"
    ARCHIVE_LIST = "archive_list"
    ARCHIVE_DETAIL = "archive_detail"
    PIECE_LIST = "piece_list"
    PIECE_DETAIL = "piece_detail"
    VIEW_NAMES = [ROOT, ARCHIVE_LIST, ARCHIVE_DETAIL, PIECE_LIST]
    HOME_BY_SCOPE = {
        ViewerConstants.SCOPE_ALL: ARCHIVE_LIST,
        ViewerConstants.SCOPE_ONE_ARCHIVE: ARCHIVE_DETAIL,
        ViewerConstants.SCOPE_ONE_COLLECTION: PIECE_LIST,
    }

    @classmethod
    def pattern_by_name(cls, name: str) -> str:
        return f"{cls.APP_NAME}:{name}"


class ViewerMessageConstants:
    VIEW_OUT_OF_SCOPE = gettext_lazy(
        "this view is not publicly visible because it is out of scope" " ({scope})"
    )
    LABEL_KIND = gettext_lazy("Kind")
    LABEL_ARCHIVES = gettext_lazy("Archives")
    LABEL_COLLECTIONS = gettext_lazy("Collections")
    LABEL_CATEGORIES = gettext_lazy("Categories")
    LABEL_PEOPLE = gettext_lazy("People")
    LABEL_KEYWORDS = gettext_lazy("Keywords")
    LABEL_ARCHIVE_LIST = gettext_lazy("Archives of {site}")
    IS_NOT_VISIBLE = gettext_lazy("Is not visible")
    IS_RESTRICTED = gettext_lazy("Is restricted to physical places")
    HELP_TEXTS = {
        "is_not_visible": IS_NOT_VISIBLE,
        "is_restricted": IS_RESTRICTED,
    }
    GENERAL_CONTEXT = {
        "collection_label": LABEL_COLLECTIONS,
        "help_texts": HELP_TEXTS,
    }
    PIECE_NOT_FOUND = gettext_lazy("Piece does not exist")
    SEARCH_TOOL_NAME = gettext_lazy("Search Options")
    SEARCH_ACTION_NAME = gettext_lazy("Search")
    SEARCH_APPLIED_FILTERS = gettext_lazy("{applied_filters} applied filters")
    TOTAL_FOUNDED_PIECES = gettext_lazy("{number} pieces were found")


class ContentConstants:
    PIECE_META_FIELDS = [
        "event",
        "register_date",
        "description",
        "description_date",
        "location",
        "duration",
        "register_author",
        "productor",
        "notes",
        "archivist_notes",
        "documentary_unit",
        "lang",
        "original_format",
    ]
    PROVIDER_MESSAGES = {"no_provider": gettext_lazy("No provider for this piece")}
    LABEL_CATEGORY = gettext_lazy("Category")
    LABEL_PERSON = gettext_lazy("Person")
    LABEL_KEYWORD = gettext_lazy("Keyword")
