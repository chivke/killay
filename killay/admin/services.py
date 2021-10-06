from csv import DictReader
from datetime import datetime
from pathlib import Path
from typing import List

from django.core import serializers
from django.conf import settings
from django.db import transaction
from django.utils.text import slugify

from killay.videos.lib.constants import VideoConstants
from killay.admin.models import Logo
from killay.pages.models import Page
from killay.videos.models import (
    Video,
    VideoMeta,
    VideoCategorization,
    VideoCategory,
    VideoCollection,
    VideoPerson,
    VideoKeyword,
)


def date_serializer_for_data_list(data: dict, fields: List[str]) -> dict:
    serialized_data = {**data}
    for field, value in data.items():
        if field in fields:
            try:
                datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                pass
            else:
                continue
            try:
                serialized_date = datetime.strptime(value, "%d-%m-%Y").strftime(
                    "%Y-%m-%d"
                )
            except ValueError:
                pass
            else:
                serialized_data[field] = serialized_date
                continue
            try:
                serialized_data[field] = datetime.strptime(value, "%m-%y").strftime(
                    "%Y-%m-%d"
                )
            except ValueError:
                serialized_data[field] = None
    return serialized_data


def video_bulk_create_from_csv_file(path: str, collection: str):
    with open(path, "r") as file:
        videos_data_list = list(DictReader(file))
    assert all(
        [field in videos_data_list[0] for field in VideoConstants.FIELDS_FOR_CSV_BULK]
    )

    videos_data_list = [
        date_serializer_for_data_list(
            video_data, fields=["description_date", "register_date"]
        )
        for video_data in videos_data_list
    ]
    videos_data_list = [
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
                field: value.split("/") if field == "categories" else value.split(",")
                for field, value in video_data.items()
                if field in VideoConstants.FIELDS_OF_VIDEOCATEGORIZATION_FOR_CSV_BULK
            },
        }
        for video_data in videos_data_list
    ]

    created_videos = []
    with transaction.atomic():
        collection, _ = VideoCollection.objects.get_or_create(
            slug=slugify(collection), defaults={"name": collection}
        )
        for video_data in videos_data_list:
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
                            slug=slugify(value[:254]),
                            collection_id=collection.id,
                            defaults={"name": value[:254]},
                        )
                    )[0]
                    for value in video_data["videocategorization_data"][field]
                ]
            video_categorization = VideoCategorization(
                video=video, collection_id=collection.id
            )
            video_categorization.save()
            video_categorization.categories.add(*categorization["categories"])
            video_categorization.people.add(*categorization["people"])
            video_categorization.keywords.add(*categorization["keywords"])
            created_videos.append(video)
    return created_videos


def bulk_update_data_for_deploy(
    path: str = ".data_for_deploy",
    videos_csv_filename: str = "videos.csv",
    collection_name: str = "First Collection",
    thumbs_foldername: str = "thumbs",
    sequences_vtt_foldername: str = "VTT",
    home_header_image_filename: str = "home_header_image.jpg",
    logos_foldername: str = "logos",
    fixtures_foldername: str = "fixtures",
):
    def __update_home_header_image(image):
        home = Page.objects.get(slug="home")
        with open(str(image), "rb") as file:
            home.header_image.save(home_header_image_filename, file)
        home.save()

    def __upload_logos(logos):
        with transaction.atomic():
            for logo in logos:
                logo_obj = Logo(name=logo.name, configuration_id=settings.SITE_ID)
                with open(str(logo), "rb") as file:
                    logo_obj.image.save(f"{logo.name}.jpg", file)
                logo_obj.save()

    def __upload_fixtures(fixtures):
        with transaction.atomic():
            for fixture in fixtures:
                with open(str(fixture), "r") as file:
                    for obj in serializers.deserialize("json", file.read()):
                        obj.save()

    path = Path(path)
    assert path.is_dir()
    videos_csv_path = path / videos_csv_filename
    thumbs_path = path / thumbs_foldername
    vtts_path = path / sequences_vtt_foldername
    home_header_image = path / home_header_image_filename
    logos_path = path / logos_foldername
    fixtures_path = path / fixtures_foldername

    if videos_csv_path.is_file():
        video_bulk_create_from_csv_file(
            str(videos_csv_path), collection=collection_name
        )
    if thumbs_path.is_dir():
        thumbs = [thumb for thumb in thumbs_path.iterdir() if thumb.suffix == ".jpg"]
        thumbs_codes = [thumb.name[: -len(thumb.suffix)] for thumb in thumbs]
        videos_code_map = {
            video.code: video for video in Video.objects.filter(code__in=thumbs_codes)
        }
        for code, video in videos_code_map.items():
            with open(str(thumbs_path / f"{code}.jpg"), "rb") as file:
                video.thumb.save(f"{code}.jpg", file)
            video.save()
    if vtts_path.is_dir():
        vtt_files = [vtt for vtt in vtts_path.iterdir() if vtt.suffix == ".vtt"]
        vtt_codes = [vtt.name[: -len(vtt.suffix)] for vtt in vtt_files]
        videos_code_map = {
            video.code: video for video in Video.objects.filter(code__in=vtt_codes)
        }
        for code, video in videos_code_map.items():
            video.import_from_vtt_file(str(vtts_path / f"{code}.vtt"))

    if logos_path.is_dir():
        logos = [logo for logo in logos_path.iterdir() if logo.suffix == ".png"]
        if logos:
            __upload_logos(logos)

    if fixtures_path.is_dir():
        fixtures = [
            fixture for fixture in fixtures_path.iterdir() if fixture.suffix == ".json"
        ]
        __upload_fixtures(fixtures)

    if home_header_image.is_file():
        __update_home_header_image(home_header_image)
