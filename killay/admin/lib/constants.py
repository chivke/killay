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
