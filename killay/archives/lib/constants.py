from django.utils.translation import gettext_lazy


class ArchiveConstants:
    VERBOSE_NAME = gettext_lazy("archive")
    VERBOSE_NAME_PLURAL = gettext_lazy("archives")
    FIELD_NAME = gettext_lazy("Name")
    FIELD_NAME_HELP_TEXT = gettext_lazy("Name of the Archive")
    FIELD_SLUG = gettext_lazy("Slug")
    FIELD_SLUG_HELP_TEXT = gettext_lazy(
        "Slug of the archive, must be unique in the site"
    )
    FIELD_DESCRIPTION = gettext_lazy("Description")
    FIELD_DESCRIPTION_HELP_TEXT = gettext_lazy("Description of the archive")
    FIELD_POSITION = gettext_lazy("Position")
    FIELD_POSITION_HELP_TEXT = gettext_lazy(
        "Determines the position in which it will be displayed, the smaller "
        "the number, the earlier it will be located"
    )
    FIELD_IMAGE = gettext_lazy("Image")
    FIELD_IMAGE_HELP_TEXT = gettext_lazy("Representative image of the archive")
    FIELD_IS_VISIBLE = gettext_lazy("Is visible")
    FIELD_IS_VISIBLE_HELP_TEXT = gettext_lazy(
        "Indicates if the archive will be visible to the public"
    )
    FIELD_IS_RESTRICTED = gettext_lazy("Is restricted")
    FIELD_IS_RESTRICTED_HELP_TEXT = gettext_lazy(
        "Indicates if the archive will be restricted to some public"
    )
    FIELD_PLACES = gettext_lazy("Restricted to this places")
    FIELD_PLACES_HELP_TEXT = gettext_lazy(
        "If the archive is restricted it will be visible only in these places"
    )


class CollectionConstants:
    VERBOSE_NAME = gettext_lazy("collection")
    VERBOSE_NAME_PLURAL = gettext_lazy("collections")
    FIELD_ARCHIVE = gettext_lazy("Archive")
    FIELD_ARCHIVE_HELP_TEXT = gettext_lazy("Archive to which the collection belongs")
    FIELD_NAME = gettext_lazy("Name")
    FIELD_NAME_HELP_TEXT = gettext_lazy("Name of the collection")
    FIELD_SLUG = gettext_lazy("Slug")
    FIELD_SLUG_HELP_TEXT = gettext_lazy(
        "Slug of the collection, must be unique in the site"
    )
    FIELD_DESCRIPTION = gettext_lazy("Description")
    FIELD_DESCRIPTION_HELP_TEXT = gettext_lazy("Description of the collection")
    FIELD_POSITION = gettext_lazy("Position")
    FIELD_POSITION_HELP_TEXT = gettext_lazy(
        "Determines the position in which it will be displayed, the smaller "
        "the number, the earlier it will be located"
    )
    FIELD_IS_VISIBLE = gettext_lazy("Is visible")
    FIELD_IS_VISIBLE_HELP_TEXT = gettext_lazy(
        "Indicates if the collection will be visible to the public"
    )
    FIELD_IS_RESTRICTED = gettext_lazy("Is restricted")
    FIELD_IS_RESTRICTED_HELP_TEXT = gettext_lazy(
        "Indicates if the collection will be restricted to some public"
    )
    FIELD_IMAGE = gettext_lazy("Image")
    FIELD_IMAGE_HELP_TEXT = gettext_lazy("Representative image of the collection")
    FIELD_PLACES = gettext_lazy("Restricted to this places")
    FIELD_PLACES_HELP_TEXT = gettext_lazy(
        "If the collection is restricted it will be visible only in these places"
    )


class CategoryConstants:
    VERBOSE_NAME = gettext_lazy("category")
    VERBOSE_NAME_PLURAL = gettext_lazy("categories")
    FIELD_COLLECTION = gettext_lazy("Collection")
    FIELD_COLLECTION_HELP_TEXT = gettext_lazy(
        "Collection to which the category belongs"
    )
    FIELD_NAME = gettext_lazy("Name")
    FIELD_NAME_HELP_TEXT = gettext_lazy("Name of the category")
    FIELD_SLUG = gettext_lazy("Slug")
    FIELD_SLUG_HELP_TEXT = gettext_lazy(
        "Slug of the category, must be unique in the site"
    )
    FIELD_DESCRIPTION = gettext_lazy("Description")
    FIELD_DESCRIPTION_HELP_TEXT = gettext_lazy("Description of the category")
    FIELD_POSITION = gettext_lazy("Position")
    FIELD_POSITION_HELP_TEXT = gettext_lazy(
        "Determines the position in which it will be displayed, the smaller "
        "the number, the earlier it will be located"
    )


class PersonConstants:
    VERBOSE_NAME = gettext_lazy("person")
    VERBOSE_NAME_PLURAL = gettext_lazy("people")
    FIELD_NAME = gettext_lazy("Name")
    FIELD_NAME_HELP_TEXT = gettext_lazy("Name of the person")
    FIELD_SLUG = gettext_lazy("Slug")
    FIELD_SLUG_HELP_TEXT = gettext_lazy(
        "Slug of the person, must be unique in the site"
    )
    FIELD_DESCRIPTION = gettext_lazy("Description")
    FIELD_DESCRIPTION_HELP_TEXT = gettext_lazy("Description of the person")
    FIELD_POSITION = gettext_lazy("Position")
    FIELD_POSITION_HELP_TEXT = gettext_lazy(
        "Determines the position in which it will be displayed, the smaller "
        "the number, the earlier it will be located"
    )


class KeywordConstants:
    VERBOSE_NAME = gettext_lazy("keyword")
    VERBOSE_NAME_PLURAL = gettext_lazy("keywords")
    FIELD_NAME = gettext_lazy("Name")
    FIELD_NAME_HELP_TEXT = gettext_lazy("Name of the keyword")
    FIELD_SLUG = gettext_lazy("Slug")
    FIELD_SLUG_HELP_TEXT = gettext_lazy(
        "Slug of the keyword, must be unique in the site"
    )
    FIELD_DESCRIPTION = gettext_lazy("Description")
    FIELD_DESCRIPTION_HELP_TEXT = gettext_lazy("Description of the keyword")
    FIELD_POSITION = gettext_lazy("Position")
    FIELD_POSITION_HELP_TEXT = gettext_lazy(
        "Determines the position in which it will be displayed, the smaller "
        "the number, the earlier it will be located"
    )


class PieceConstants:
    KIND_VIDEO = "VIDEO"
    KIND_IMAGE = "IMAGE"
    KIND_SOUND = "SOUND"
    KIND_DOCUMENT = "DOCUMENT"
    KIND_CHOICES = [
        (KIND_VIDEO, gettext_lazy("Video")),
        (KIND_IMAGE, gettext_lazy("Image")),
        (KIND_SOUND, gettext_lazy("Sound")),
        (KIND_DOCUMENT, gettext_lazy("Document")),
    ]
    KIND_LIST = [KIND_VIDEO, KIND_IMAGE, KIND_SOUND, KIND_DOCUMENT]
    VERBOSE_NAME = gettext_lazy("piece")
    VERBOSE_NAME_PLURAL = gettext_lazy("pieces")
    FIELD_CODE = gettext_lazy("Code")
    FIELD_CODE_HELP_TEXT = gettext_lazy("Code of the piece, must be unique in the site")
    FIELD_TITLE = gettext_lazy("Title")
    FIELD_TITLE_HELP_TEXT = gettext_lazy("Title of the piece")
    FIELD_THUMB = gettext_lazy("Thumb")
    FIELD_THUMB_HELP_TEXT = gettext_lazy(
        "thumbnail of representative image of the piece"
    )
    FIELD_IS_PUBLISHED = gettext_lazy("Is published")
    FIELD_IS_PUBLISHED_HELP_TEXT = gettext_lazy(
        "If the piece is not published, you will need to " "log in as admin to visit it"
    )
    FIELD_KIND = gettext_lazy("Kind")
    FIELD_KIND_HELP_TEXT = gettext_lazy(
        "Kind of the piece (video, sound, image or document)"
    )
    FIELD_COLLECTION = gettext_lazy("Collection")
    FIELD_COLLECTION_HELP_TEXT = gettext_lazy("Collection to which the piece belongs")
    FIELD_CATEGORIES = gettext_lazy("Categories")
    FIELD_CATEGORIES_HELP_TEXT = gettext_lazy("Categories to which the piece belongs")
    FIELD_PEOPLE = gettext_lazy("People")
    FIELD_PEOPLE_HELP_TEXT = gettext_lazy("People who relate to the piece")
    FIELD_KEYWORDS = gettext_lazy("Keywords")
    FIELD_KEYWORDS_HELP_TEXT = gettext_lazy("Keywords related to the piece")
    FIELD_IS_RESTRICTED = gettext_lazy("Is restricted")
    FIELD_IS_RESTRICTED_HELP_TEXT = gettext_lazy(
        "Indicates if the piece will be restricted to some public"
    )
    FIELD_PLACES = gettext_lazy("Restricted to this places")
    FIELD_PLACES_HELP_TEXT = gettext_lazy(
        "If the piece is restricted it will be visible only in these places"
    )


class SequenceConstants:
    VERBOSE_NAME = gettext_lazy("sequence")
    VERBOSE_NAME_PLURAL = gettext_lazy("sequences")
    FIELD_TITLE = gettext_lazy("Title")
    FIELD_TITLE_HELP_TEXT = gettext_lazy("Title of piece sequence")
    FIELD_CONTENT = gettext_lazy("Content")
    FIELD_CONTENT_HELP_TEXT = gettext_lazy("Tex content of piece sequence")
    FIELD_INI = gettext_lazy("Initiation")
    FIELD_INI_HELP_TEXT = gettext_lazy("Initiation time of piece sequence")
    FIELD_END = gettext_lazy("End")
    FIELD_END_HELP_TEXT = gettext_lazy("End time of piece sequence")


class ProviderConstants:
    VERBOSE_NAME = gettext_lazy("provider")
    VERBOSE_NAME_PLURAL = gettext_lazy("providers")
    FIELD_ACTIVE = gettext_lazy("Active")
    FIELD_ACTIVE_HELP_TEXT = gettext_lazy(
        "Determines if the provider is active, "
        "only one provider can be active at a time"
    )
    FIELD_PLY_EMBED_ID = gettext_lazy("Video Embed ID")
    FIELD_PLY_EMBED_ID_HELP_TEXT = gettext_lazy(
        "Video ID to be embedded in the player, " "field used by pieces of kind video"
    )
    FIELD_PLYR_PROVIDER = gettext_lazy("Video Provider")
    FIELD_PLYR_PROVIDER_HELP_TEXT = gettext_lazy(
        "Video provider associated with the embed ID, "
        "field used by pieces of kind video"
    )
    FIELD_IMAGE = gettext_lazy("Image")
    FIELD_IMAGE_HELP_TEXT = gettext_lazy(
        "Image hosted on the server, field used by pieces of kind image"
    )
    FIELD_FILE = gettext_lazy("File")
    FIELD_FILE_HELP_TEXT = gettext_lazy(
        "File hosted on the server, " "field used by pieces of kind document and sound"
    )
    FIELD_ONLINE = gettext_lazy("Online")
    FIELD_CHECKED_AT = gettext_lazy("Online Checked At")

    YOUTUBE = "youtube"
    VIMEO = "vimeo"
    PLYR_PROVIDER_LIST = [YOUTUBE, VIMEO]
    PLYR_PROVIDER_CHOICES = [(YOUTUBE, "Youtube"), (VIMEO, "Vimeo")]
    URL_TEMPLATE = {
        YOUTUBE: ("https://{plyr_provider}.com/embed/{ply_embed_id}"),
        VIMEO: ("https://player.{plyr_provider}.com/video/{ply_embed_id}"),
    }
    URL_PLYR_TEMPLATE = {
        YOUTUBE: (
            URL_TEMPLATE[YOUTUBE] + "?origin=https://plyr.io&amp;iv_load_policy=3&amp;"
            "modestbranding=1&amp;responsive=true&amp;playsinline=1&amp;"
            "showinfo=0&amp;rel=0&amp;enablejsapi=1"
        ),
        VIMEO: (
            URL_TEMPLATE[VIMEO] + "?loop=false&amp;byline=false&amp;portrait=false&amp;"
            "title=false&amp;speed=true&amp;transparent=0&amp;gesture=media"
        ),
    }
    YOUTUBE_ID_REGEX = r"https:\/\/[w.]*youtube.com/watch\?v=([A-Za-z0-9]*)"
    VIMEO_ID_REGEX = r"https:\/\/[w.]*vimeo.com/([0-9]*)"
    THUMB_YOUTUBE_TEMPLATE = "https://i.ytimg.com/vi/{code}/sddefault.jpg"


class PieceMetaConstants:
    VERBOSE_NAME = gettext_lazy("piece metadata")
    VERBOSE_NAME_PLURAL = gettext_lazy("piece metadatas")
    FIELD_EVENT = gettext_lazy("Event")
    FIELD_EVENT_HELP_TEXT = gettext_lazy("Event related to the piece")
    FIELD_DESCRIPTION = gettext_lazy("Description")
    FIELD_DESCRIPTION_HELP_TEXT = gettext_lazy("Description of the piece")
    FIELD_DESCRIPTION_DATE = gettext_lazy("Description Date")
    FIELD_DESCRIPTION_DATE_HELP_TEXT = gettext_lazy("Date of the description")
    FIELD_LOCATION = gettext_lazy("Location")
    FIELD_LOCATION_HELP_TEXT = gettext_lazy("Location related to the piece")
    FIELD_DURATION = gettext_lazy("Duration")
    FIELD_DURATION_HELP_TEXT = gettext_lazy("Piece duration if applicable")
    FIELD_REGISTER_DATE = gettext_lazy("Register Date")
    FIELD_REGISTER_DATE_HELP_TEXT = gettext_lazy("Register date of the piece")
    FIELD_REGISTER_AUTHOR = gettext_lazy("Register Author")
    FIELD_REGISTER_AUTHOR_HELP_TEXT = gettext_lazy("Author of the piece record")
    FIELD_PRODUCTOR = gettext_lazy("Productor")
    FIELD_PRODUCTOR_HELP_TEXT = gettext_lazy("Productor of the piece")
    FIELD_NOTES = gettext_lazy("Notes")
    FIELD_NOTES_HELP_TEXT = gettext_lazy("Notes related to the piece")
    FIELD_ARCHIVIST_NOTES = gettext_lazy("Archivist Notes")
    FIELD_ARCHIVIST_NOTES_HELP_TEXT = gettext_lazy("Archivist notes of the piece")
    FIELD_DOCUMENTARY_UNIT = gettext_lazy("Documentary Unit")
    FIELD_DOCUMENTARY_UNIT_HELP_TEXT = gettext_lazy("Documentary unit of the piece")
    FIELD_LANG = gettext_lazy("Language")
    FIELD_LANG_HELP_TEXT = gettext_lazy("Language of the piece")
    FIELD_ORIGINAL_FORMAT = gettext_lazy("Original Format")
    FIELD_ORIGINAL_FORMAT_HELP_TEXT = gettext_lazy("Original format of the piece")


class PlaceConstants:
    VERBOSE_NAME = gettext_lazy("place")
    VERBOSE_NAME_PLURAL = gettext_lazy("places")
    FIELD_NAME = gettext_lazy("Name")
    FIELD_NAME_HELP_TEXT = gettext_lazy("Name of the place")
    FIELD_ALLOWED_PIECES = gettext_lazy("Allowed Pieces")
    FIELD_ALLOWED_PIECES_HELP_TEXT = gettext_lazy(
        "Restricted pieces that are allowed to see from the place"
    )
    FIELD_ALLOWED_COLLECTIONS = gettext_lazy("Allowed Collections")
    FIELD_ALLOWED_COLLECTIONS_HELP_TEXT = gettext_lazy(
        "Restricted collections that are allowed to see from the place"
    )
    FIELD_ALLOWED_ARCHIVES = gettext_lazy("Allowed Archives")
    FIELD_ALLOWED_ARCHIVES_HELP_TEXT = gettext_lazy(
        "Restricted archives that are allowed to see from the place"
    )


class PlaceAddressConstants:
    VERBOSE_NAME = gettext_lazy("place address")
    VERBOSE_NAME_PLURAL = gettext_lazy("place addresses")
    FIELD_IPV4 = gettext_lazy("IP Address")
    FIELD_IPV4_HELP_TEXT = gettext_lazy("IP Address of the place")
    FIELD_DESCRIPTION = gettext_lazy("Description")
    FIELD_DESCRIPTION_HELP_TEXT = gettext_lazy("Description of the place address")
