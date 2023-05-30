from django.utils.translation import gettext_lazy


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


class ProviderConstants:
    YOUTUBE = "youtube"
    VIMEO = "vimeo"
    PLYR_PROVIDER_CHOICES = [(YOUTUBE, "Youtube"), (VIMEO, "Vimeo")]
    URL_TEMPLATE = {
        YOUTUBE: ("https://player.{plyr_provider}.com/embed/{ply_embed_id}"),
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
