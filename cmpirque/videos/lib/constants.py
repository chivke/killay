class VideoProviderConstants:
    YOUTUBE = "youtube"
    VIMEO = "vimeo"
    PLYR_PROVIDER_CHOICES = [(YOUTUBE, "Youtube"), (VIMEO, "Vimeo")]


class VideoConstants:
    FIELDS_OF_VIDEO_FOR_CSV_BULK = ["code"]
    FIELDS_OF_VIDEOCATEGORIZATION_FOR_CSV_BULK = ["categories", "people", "keywords"]
    FIELDS_OF_VIDEOMETA_FOR_CSV_BULK = [
        "title",
        "event",
        "description",
        "description_date",
        "location",
        "duration",
        "register_date",
        "register_author",
        "productor",
        "notes",
        "archivist_notes",
        "documentary_unit",
        "lang",
        "original_format",
    ]
    FIELDS_FOR_CSV_BULK = [
        *FIELDS_OF_VIDEO_FOR_CSV_BULK,
        *FIELDS_OF_VIDEOCATEGORIZATION_FOR_CSV_BULK,
        *FIELDS_OF_VIDEOMETA_FOR_CSV_BULK,
    ]
