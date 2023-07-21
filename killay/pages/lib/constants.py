from django.utils.translation import gettext_lazy


class PageConstants:
    NAME_TITLE = gettext_lazy("Title")
    NAME_SLUG = gettext_lazy("Slug")
    NAME_KIND = gettext_lazy("Kind")
    NAME_CREATED_AT = gettext_lazy("Created at")
    NAME_UPDATED_AT = gettext_lazy("Updated at")
    NAME_IS_VISIBLE = gettext_lazy("Is visible")
    NAME_BODY = gettext_lazy("Body")
    NAME_HEADER_IMAGE = gettext_lazy("Header image")
    NAME_REDIRECT_TO = gettext_lazy("Redirect to (URL)")
    NAME_BODY = gettext_lazy("Body")
    NAME_POSITION = gettext_lazy("Position")
    NAME_UI_OPTIONS = gettext_lazy("UI Options")

    KIND_PAGE = "PAGE"
    KIND_LINK = "LINK"
    KIND_CHOICES = [
        (KIND_PAGE, gettext_lazy("Page")),
        (KIND_LINK, gettext_lazy("Link")),
    ]
