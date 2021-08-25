from csv import DictReader

from django.db import transaction
from django.utils.text import slugify

from cmpirque.videos.lib.constants import VideoConstants
from cmpirque.videos.models import (
    Video,
    VideoMeta,
    VideoCategorization,
    VideoCategory,
    VideoPerson,
    VideoKeyword,
)


def video_bulk_create_from_csv_file(path: str):
    with open(path, "r") as file:
        videos_data_list = list(DictReader(file))
    assert all(
        [field in videos_data_list[0] for field in VideoConstants.FIELDS_FOR_CSV_BULK]
    )
    video_data_list = [
        {
            "video_data": {
                field: value
                for field, value in video_data.items()
                if field in VideoConstants.FIELDS_OF_VIDEO_FOR_CSV_BULK
            },
            "videometa_data": {
                field: value
                for field, value in video_data.items()
                if field in VideoConstants.FIELDS_OF_VIDEOMETA_FOR_CSV_BULK
            },
            "videocategorization_data": {
                field: value.split("/")
                for field, value in video_data.items()
                if field in VideoConstants.FIELDS_OF_VIDEOCATEGORIZATION_FOR_CSV_BULK
            },
        }
        for video_data in videos_data_list
    ]
    created_videos = []
    with transaction.atomic():
        for video_data in video_data_list:
            video_meta = VideoMeta(**video_data["videometa_data"])
            video_meta.save()
            video = Video(meta_id=video_meta.id, **video_data["video_data"])
            video.save()
            categorization = {}
            for field, model in [
                ("categories", VideoCategory),
                ("people", VideoPerson),
                ("keywords", VideoKeyword),
            ]:
                categorization[field] = [
                    (
                        model.objects.get_or_create(
                            slug=slugify(value), defaults={"name": value}
                        )
                    )[0]
                    for value in video_data["videocategorization_data"][field]
                ]
            video_categorization = VideoCategorization(video=video)
            video_categorization.save()
            video_categorization.categories.add(*categorization["categories"])
            video_categorization.people.add(*categorization["people"])
            video_categorization.keywords.add(*categorization["keywords"])
            created_videos.append(video)
    return created_videos
