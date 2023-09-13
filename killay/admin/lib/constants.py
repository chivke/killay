from datetime import date, time
from django.utils.translation import gettext_lazy


class SiteConfigurationConstants:
    VERBOSE_NAME = gettext_lazy("Site Configuration")
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
    MAIN_TITLE = gettext_lazy("Configuration")
    NAME_GENERAL = gettext_lazy("General")
    NAME_VIEWER = gettext_lazy("Visualization")
    NAME_SOCIAL_MEDIA = gettext_lazy("Social Medias")
    NAME_LOGO = gettext_lazy("Logos")
    NAME_PAGES = gettext_lazy("Pages")
    NAME_USERS = gettext_lazy("Users")
    PATTERN_GENERAL = "admin:site_configuration"
    PATTERN_VIEWER = "admin:site_viewer"
    PATTERN_SOCIAL_MEDIA = "admin:site_social_media_list"
    PATTERN_LOGO = "admin:site_logo_list"
    PATTERN_PAGE_LIST = "admin:pages_list"
    PATTERN_USER_LIST = "admin:users_list"
    PATTERN_BY_NAME = {
        NAME_GENERAL: PATTERN_GENERAL,
        NAME_VIEWER: PATTERN_VIEWER,
        NAME_SOCIAL_MEDIA: PATTERN_SOCIAL_MEDIA,
        NAME_LOGO: PATTERN_LOGO,
    }
    FIELD_NAME = gettext_lazy("Name of Site")
    FIELD_NAME_HELP_TEXT = gettext_lazy(
        "Site name, can be omitted with certain display options"
    )
    FIELD_DOMAIN = gettext_lazy("Domain")
    FIELD_DOMAIN_HELP_TEXT = gettext_lazy("Domain of the site (example.com)")
    FIELD_IS_PUBLISHED = gettext_lazy("Is published")
    FIELD_IS_PUBLISHED_HELP_TEXT = gettext_lazy(
        "If the site is not published, you will need to log in to visit it"
    )
    FIELD_FOOTER_IS_VISIBLE = gettext_lazy("Footer is visible")
    FIELD_FOOTER_IS_VISIBLE_HELP_TEXT = gettext_lazy(
        "Indicates whether or not the footer will be displayed"
    )
    DESCRIPTION_GENERAL = gettext_lazy("General site configuration options")
    DESCRIPTION_VIEWER = gettext_lazy(
        "Site archival content display options and preferences"
    )
    DESCRIPTION_SOCIAL_MEDIA = gettext_lazy(
        "Allows you to manage institutional social networks to be "
        "displayed on the site"
    )
    DESCRIPTION_LOGO = gettext_lazy(
        "Allows you to manage institutional logos to be displayed on the site"
    )


class ArchivesViewConstants:
    MAIN_TITLE = gettext_lazy("Archives Content Manager")


def _get_pattern_names(slugs: list, action: str) -> dict:
    return {slug: f"admin:{slug}_{action}" for slug in slugs}


class ContentManagerConstants:
    MAIN_TITLE = gettext_lazy("Content Manager")
    SLUG_BULK_ACTION = "bulk_action"
    SLUG_PLACE = "place"
    SLUG_ARCHIVE = "archive"
    SLUG_COLLECTION = "collection"
    SLUG_PIECE = "piece"
    SLUG_CATEGORY = "category"
    SLUG_PERSON = "person"
    SLUG_KEYWORD = "keyword"
    VIEW_SLUGS = [
        SLUG_BULK_ACTION,
        SLUG_PLACE,
        SLUG_ARCHIVE,
        SLUG_COLLECTION,
        SLUG_PIECE,
        SLUG_CATEGORY,
        SLUG_PERSON,
        SLUG_KEYWORD,
    ]

    NAME_BULK_ACTION = gettext_lazy("Bulk Actions")
    NAME_ARCHIVE = gettext_lazy("Archives")
    NAME_COLLECTION = gettext_lazy("Collections")
    NAME_PIECE = gettext_lazy("Pieces")
    NAME_CATEGORY = gettext_lazy("Categories")
    NAME_PERSON = gettext_lazy("People")
    NAME_KEYWORD = gettext_lazy("Keywords")
    NAME_SEQUENCE = gettext_lazy("Sequences")
    NAME_PROVIDER = gettext_lazy("Providers")
    NAME_PLACE = gettext_lazy("Places")
    NAME_ADDRESS = gettext_lazy("Addresses")

    DESCRIPTION_BULK_ACTION = gettext_lazy(
        "It allows executing bulk actions to manipulate the content. "
        "These work through an excel file (xlsx) that is loaded into the system."
    )
    DESCRIPTION_PLACE = gettext_lazy(
        "It refers to the places from where the public "
        "could access restricted content"
    )
    DESCRIPTION_PLACE_ADDRESSES = gettext_lazy(
        "IP addresses associated with this place"
    )
    DESCRIPTION_ARCHIVE = gettext_lazy(
        "Archives are the broadest classification to group pieces, "
        "and can be subdivided into collections"
    )
    DESCRIPTION_COLLECTION = gettext_lazy(
        "Collections are groupings required to " "classify pieces within an archive"
    )
    DESCRIPTION_PIECE = gettext_lazy(
        "Pieces are the display units in multimedia format "
        "(videos, images, sounds and documents)."
    )
    DESCRIPTION_PIECE_GENERAL = gettext_lazy(
        "Edition of fundamental fields of the piece and its categorization"
    )
    DESCRIPTION_PIECE_META = gettext_lazy("Edition of metadata field of the piece")
    DESCRIPTION_PIECE_SEQUENCES = gettext_lazy(
        "The sequences allow you to add text content to certain moments "
        "of a piece of the video or sound kind"
    )
    DESCRIPTION_PIECE_PROVIDERS = gettext_lazy(
        "The providers allow you to manage the content of "
        "the piece to be displayed on the site"
    )
    DESCRIPTION_CATEGORY = gettext_lazy(
        "The categories are subdivisions of the pieces of the collections "
        "for their more precise classification"
    )
    DESCRIPTION_PERSON = gettext_lazy(
        "People are subjects related to pieces of the site"
    )
    DESCRIPTION_KEYWORD = gettext_lazy(
        "Keywords are concepts related to the pieces within the site"
    )

    VIEWS_SECOND_TITLE = {
        SLUG_BULK_ACTION: NAME_BULK_ACTION,
        SLUG_PLACE: NAME_PLACE,
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
        SLUG_BULK_ACTION: {
            "list": {"view": f"admin:{SLUG_BULK_ACTION}_list", "name": NAME_BULK_ACTION}
        },
        SLUG_ARCHIVE: {
            "list": {"view": f"admin:{SLUG_ARCHIVE}_list", "name": NAME_ARCHIVE}
        },
        SLUG_PLACE: {"list": {"view": f"admin:{SLUG_PLACE}_list", "name": NAME_PLACE}},
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


class SocialMediaConstants:
    VERBOSE_NAME = gettext_lazy("social media")
    VERBOSE_NAME_PLURAL = gettext_lazy("social medias")
    FIELD_PROVIDER = gettext_lazy("Provider")
    FIELD_PROVIDER_HELP_TEXT = gettext_lazy("Social network provider")
    FIELD_URL = gettext_lazy("URL")
    FIELD_URL_HELP_TEXT = gettext_lazy("Social network profile URL")
    FIELD_IS_VISIBLE = gettext_lazy("Is visible")
    FIELD_IS_VISIBLE_HELP_TEXT = gettext_lazy(
        "Indicates if the social network will be visible to the public"
    )
    FIELD_POSITION = gettext_lazy("Position")
    FIELD_POSITION_HELP_TEXT = gettext_lazy(
        "Determines the position in which it will be displayed, the smaller "
        "the number, the earlier it will be located"
    )


class LogoConstants:
    VERBOSE_NAME = gettext_lazy("logo")
    VERBOSE_NAME_PLURAL = gettext_lazy("logos")
    FIELD_NAME = gettext_lazy("Name")
    FIELD_NAME_HELP_TEXT = gettext_lazy("Name of the logo")
    FIELD_IMAGE = gettext_lazy("Image")
    FIELD_IMAGE_HELP_TEXT = gettext_lazy("Logo image")
    FIELD_IS_VISIBLE = gettext_lazy("Is visible")
    FIELD_IS_VISIBLE_HELP_TEXT = gettext_lazy(
        "Indicates if the logo will be visible to the public"
    )
    FIELD_POSITION = gettext_lazy("Position")
    FIELD_POSITION_HELP_TEXT = gettext_lazy(
        "Determines the position in which it will be displayed, the smaller "
        "the number, the earlier it will be located"
    )


class AdminNavConstants:
    ROOT_LABEL = gettext_lazy("Administrator")
    ROOT_PATTERN = "admin:site_configuration"
    LOCATION_LABEL = gettext_lazy("Location")
    LOCATION_UPDATE_PLACE_LABEL = gettext_lazy("Update place")
    LOCATION_CREATE_PLACE_LABEL = gettext_lazy("Add place")
    LOCATION_UPDATE_ADDRESS_LABEL = gettext_lazy("Update IP Address")
    LOCATION_CREATE_ADDRESS_LABEL = gettext_lazy("Add IP Address")
    LOCATION_UPDATE_PLACE_PATTERN = "admin:place_update"
    LOCATION_CREATE_PLACE_PATTERN = "admin:place_create"
    LOCATION_UPDATE_ADDRESS_PATTERN = "admin:place_address_list"
    LOCATION_CREATE_ADDRESS_PATTERN = "admin:place_address_create"
    UPDATE_PIECE_LABEL = gettext_lazy("Update Piece ({code})")
    UPDATE_ARCHIVE_LABEL = gettext_lazy("Update Archive ({slug})")
    UPDATE_COLLECTION_LABEL = gettext_lazy("Update Collection ({slug})")
    UPDATE_CATEGORY_LABEL = gettext_lazy("Update Category ({slug})")
    UPDATE_PERSON_LABEL = gettext_lazy("Update Person ({slug})")
    UPDATE_KEYWORD_LABEL = gettext_lazy("Update Keyword ({slug})")


class PageManagerConstants:
    MAIN_TITLE = gettext_lazy("Pages Manager")
    PATTERN_LIST = "admin:pages_list"
    PATTERN_CREATE = "admin:pages_create"
    PATTERN_UPDATE = "admin:pages_update"
    PATTERN_DELETE = "admin:pages_delete"
    PAGE_LIST_LABEL = gettext_lazy("Page List")


class UserManagerConstants:
    MAIN_TITLE = gettext_lazy("Users Manager")
    PATTERN_LIST = "admin:users_list"
    PATTERN_CREATE = "admin:users_create"
    PATTERN_UPDATE = "admin:users_update"
    PATTERN_DELETE = "admin:users_delete"
    LIST_LABEL = gettext_lazy("Users List")


class BulkActionConstants:
    TYPE_PIECE_CREATE = "piece_create"
    TYPES = [TYPE_PIECE_CREATE]

    TYPE_NAME_PIECE_CREATE = gettext_lazy("Bulk Create Pieces")
    TYPE_NAMES = {TYPE_PIECE_CREATE: TYPE_NAME_PIECE_CREATE}
    TYPE_DESCRIPTION_PIECE_CREATE = gettext_lazy(
        "This tool allows you to load an excel file with a series of pieces "
        "to be created. You can only add fields that do not involve uploading "
        "files (images, documents, sounds, files, etc.), "
        "the remaining fields must be updated piece by piece."
    )
    TYPE_DESCRIPTIONS = {TYPE_PIECE_CREATE: TYPE_DESCRIPTION_PIECE_CREATE}

    ACTION_TYPE_LABEL = gettext_lazy("Action Type")
    ACTION_TYPE_HELP_TEXT = gettext_lazy("Type of bulk action to execute")
    XLS_FILE_LABEL = gettext_lazy("XLS File")
    XLS_FILE_HELP_TEXT = gettext_lazy("Excel file (xls) to be processed")
    ERROR_WRONG_FILE = gettext_lazy("Wrong file extension, must be excel file")
    ERROR_WRONG_VALUE_TYPE = gettext_lazy(
        "Wrong value type for {field} field, must be {field_types}"
    )
    ERROR_FILE_IS_EMPTY = gettext_lazy("The file does not contain rows with data")
    ERROR_FIELD_IS_REQUIRED = gettext_lazy("{field} field is required")
    ERROR_FIELD_BOOL = gettext_lazy('Must be "TRUE" or "FALSE"')
    ERROR_FIELD_NOT_SLUG = gettext_lazy(
        '{field} field must be slug (only letters, numbers and "-" or "_").'
    )
    KEY_FALSE = "FALSE"
    KEY_TRUE = "TRUE"
    BOOL_KEYS = [KEY_TRUE, KEY_FALSE]
    TEMPLATE_ID = "[id={id}]"
    FILE_CONTENT_TYPE = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    FILE_NAME_TEMPLATE = "template_{action_type}.xlsx"
    SECTION_COLUMNS_TITLE = gettext_lazy("File Columns")
    SECTION_COLUMNS_DESCRIPTION = gettext_lazy(
        "Here you can review the detail of the columns of the file to be uploaded"
    )
    TITLE_REQUIRED_COLS = gettext_lazy("Required Columns")
    TITLE_NON_REQUIRED_COLS = gettext_lazy("Non Required Columns")
    TITLE_TEMPLATE = gettext_lazy("Download the template")
    DESCRIPTION_TEMPLATE = gettext_lazy(
        "You can download here a template with all the fields usable "
        "by this bulk action."
    )
    COLUMN_DATA_FIELDS = [
        gettext_lazy("Column Name"),
        gettext_lazy("Name"),
        gettext_lazy("Description"),
        gettext_lazy("Format"),
    ]
    VIDEO_URL_LABEL = gettext_lazy("Video URL")
    VIDEO_URL_DESCRIPTION = gettext_lazy(
        "Video URL from Youtube or Vimeo, " "like https://www.youtube.com/watch?v=CODE"
    )
    FILE_FORMAT_FIELD_DESCRIPTIONS = {
        str: gettext_lazy("Plain text"),
        bool: gettext_lazy("Only TRUE or FALSE"),
        int: gettext_lazy("Only numbers"),
        date: gettext_lazy("Must be in this format: YYYY:MM:DD"),
        time: gettext_lazy("Must be in this format: HH:MM:SS"),
        (str, int): gettext_lazy(
            "It can be the text suggested in the " "template or directly the ID number"
        ),
        list: gettext_lazy(
            "It allows a list of texts, they have to be "
            'separated by commas, like: "word,another-word"'
        ),
    }
    ROW_TEMPLATE = gettext_lazy("Row {row}")
    FORMAT_DATES_ALLOWED = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
    ]
    ERROR_DATE_WRONG_FORMAT = gettext_lazy(
        "date '{value}' does not match formats {formats}"
    )
    ERROR_TIME_WRONG_FORMAT = gettext_lazy(
        "time'{value}' does not match formats HH:MM:SS"
    )
    RESULT_SUCCESS_TITLE = gettext_lazy("Successful Loading Result")
    RESULT_ERROR_TITLE = gettext_lazy("Loading Errors Detected")
    RESULT_DATA_ERRORS_LABEL = gettext_lazy(
        "The file contains the following errors in its data"
    )
    RESULT_FILE_ERRORS_LABEL = gettext_lazy("The file contains errors")


class BulkActionMessageConstants:
    ERROR_WRONG_KIND = gettext_lazy("{value} is not a valid kind, must use: {kinds}")
    ERROR_WRONG_URL = gettext_lazy("{value} is not a correct URL")
    ERROR_UNKNOWN_PROVIDER = gettext_lazy(
        'url "{value}" is not from a known provider, must be: {providers}'
    )
    ERROR_DOES_NOT_EXIST = gettext_lazy("{value} for {field} field does not exist")
    ERROR_ALREADY_EXIST = gettext_lazy("{value} for {field} field already exist")
    ERROR_NOT_BELONG_TO = gettext_lazy(
        "{value} {type} not belog to {other_value} {other_type}"
    )
    ERROR_IS_REPEATED = gettext_lazy("{value} for {field} is repeated")
