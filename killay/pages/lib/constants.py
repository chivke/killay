from django.utils.translation import gettext_lazy


class PageConstants:
    VERBOSE_NAME = gettext_lazy("page")
    VERBOSE_NAME_PLURAL = gettext_lazy("pages")
    FIELD_TITLE = gettext_lazy("Title")
    FIELD_TITLE_HELP_TEXT = gettext_lazy("Title of the page")
    FIELD_SLUG = gettext_lazy("Slug")
    FIELD_SLUG_HELP_TEXT = gettext_lazy("Slug of the page, must be unique in the site")
    FIELD_KIND = gettext_lazy("Kind")
    FIELD_KIND_HELP_TEXT = gettext_lazy("Kind of the page (page or redirect to link)")
    FIELD_CREATED_AT = gettext_lazy("Created at")
    FIELD_UPDATED_AT = gettext_lazy("Updated at")
    FIELD_IS_VISIBLE = gettext_lazy("Is visible")
    FIELD_IS_VISIBLE_HELP_TEXT = gettext_lazy(
        "Indicates if the page will be visible to the public"
    )
    FIELD_BODY = gettext_lazy("Body")
    FIELD_BODY_HELP_TEXT = gettext_lazy("Page body to render in HTML")
    FIELD_HEADER_IMAGE = gettext_lazy("Header image")
    FIELD_HEADER_IMAGE_HELP_TEXT = gettext_lazy("Header image of the page")
    FIELD_REDIRECT_TO = gettext_lazy("Redirect to")
    FIELD_REDIRECT_TO_HELP_TEXT = gettext_lazy("URL to be redirected")
    FIELD_POSITION = gettext_lazy("Position")
    FIELD_POSITION_HELP_TEXT = gettext_lazy(
        "Determines the position in which it will be displayed, the smaller "
        "the number, the earlier it will be located"
    )
    FIELD_ARCHIVE = gettext_lazy("Archive")
    FIELD_ARCHIVE_HELP_TEXT = gettext_lazy(
        "Allows you to associate the page to a specific archive"
    )
    FIELD_COLLECTION = gettext_lazy("Collection")
    FIELD_COLLECTION_HELP_TEXT = gettext_lazy(
        "Allows you to associate the page to a specific collection"
    )
    FIELD_PLACE = gettext_lazy("Place")
    FIELD_PLACE_HELP_TEXT = gettext_lazy(
        "Allows you to associate the page to a specific place"
    )
    FIELD_IS_VISIBLE_IN_NAVBAR = gettext_lazy("Is visible in navbar")
    FIELD_IS_VISIBLE_IN_NAVBAR_HELP_TEXT = gettext_lazy(
        "Indicates whether a page link appears in the navigation bar"
    )
    FIELD_IS_VISIBLE_IN_FOOTER = gettext_lazy("Is visible in footer")
    FIELD_IS_VISIBLE_IN_FOOTER_HELP_TEXT = gettext_lazy(
        "Indicates whether a page link appears in the footer"
    )
    FIELD_IS_TITLE_VISIBLE_IN_BODY = gettext_lazy("Is title visible in body")
    FIELD_IS_TITLE_VISIBLE_IN_BODY_HELP_TEXT = gettext_lazy(
        "Indicates whether a page title appears in the body"
    )

    KIND_PAGE = "PAGE"
    KIND_LINK = "LINK"
    KIND_CHOICES = [
        (KIND_PAGE, gettext_lazy("Page")),
        (KIND_LINK, gettext_lazy("Link")),
    ]
