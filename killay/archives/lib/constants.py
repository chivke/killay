class PieceConstants:
    KIND_VIDEO = "VIDEO"
    KIND_IMAGE = "IMAGE"
    KIND_SOUND = "SOUND"
    KIND_DOCUMENT = "DOCUMENT"
    KIND_CHOICES = [
        (KIND_VIDEO, "Video"),
        (KIND_IMAGE, "Image"),
        (KIND_SOUND, "Sound"),
        (KIND_DOCUMENT, "Document"),
    ]


class ProviderConstants:
    YOUTUBE = "youtube"
    VIMEO = "vimeo"
    PLYR_PROVIDER_CHOICES = [(YOUTUBE, "Youtube"), (VIMEO, "Vimeo")]
