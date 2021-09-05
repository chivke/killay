import pytest

from csv import DictWriter
from datetime import datetime
from factory import Faker
from django.core import serializers

from cmpirque.admin import services as admin_services
from cmpirque.admin.models import Logo
from cmpirque.videos.lib.constants import VideoConstants
from cmpirque.videos.models import Video
from cmpirque.pages.models import Page


pytestmark = pytest.mark.django_db


@pytest.fixture
def video_csv_data():
    faker = Faker("name")
    return [
        {
            field: (
                faker.generate()
                if field
                not in VideoConstants.FIELDS_OF_VIDEOCATEGORIZATION_FOR_CSV_BULK
                else faker.generate().replace(" ", "/")
            )
            if field not in ["duration", "description_date", "register_date"]
            else (
                Faker("time").generate()
                if field == "duration"
                else Faker("date").generate()
            )
            for field in VideoConstants.FIELDS_FOR_CSV_BULK
        }
        for index in range(5)
    ]


def test_video_bulk_create_from_csv_file(video_csv_data, tmpdir):
    csv_file = tmpdir.join("csv_file.csv")
    video_csv_data[0]["description_date"] = "04-14"
    with open(csv_file, "w") as file:
        writer = DictWriter(file, fieldnames=VideoConstants.FIELDS_FOR_CSV_BULK)
        writer.writeheader()
        for data in video_csv_data:
            writer.writerow(data)
    videos = admin_services.video_bulk_create_from_csv_file(csv_file)
    assert len(videos) == 5
    assert all([video.meta and video.categorization for video in videos])
    assert all([video.categorization.categories.exists() for video in videos])
    assert all([video.categorization.people.exists() for video in videos])
    assert all([video.categorization.keywords.exists() for video in videos])


@pytest.fixture
def sequences_vtt_file_content():
    return (
        "WEBVTT\n"
        "\n1\n00:00:01.000 --> 00:05:03.000"
        "\nContent of sequence 1\n"
        "\n2\n00:05:01.000 --> 00:10:02.000"
        "\nContent of sequence 2\n"
        "\n3\n00:10:01.000 --> 00:15:03.000"
        "\nContent of sequence 3\n"
        "\n4\n01:00:01.000 --> 01:05:03.000"
        "\nContent of sequence 4\n"
    )


@pytest.fixture
def data_for_deploy_folder(tmpdir):
    data_for_deploy = tmpdir / ".data_for_deploy"
    data_for_deploy.mkdir()
    thumbs_folder = data_for_deploy / "thumbs"
    thumbs_folder.mkdir()
    vtt_folder = data_for_deploy / "VTT"
    vtt_folder.mkdir()
    logos_folder = data_for_deploy / "logos"
    logos_folder.mkdir()
    fixtures_path = data_for_deploy / "fixtures"
    fixtures_path.mkdir()
    return data_for_deploy


@pytest.fixture
def data_for_deploy(
    page, data_for_deploy_folder, video_csv_data, sequences_vtt_file_content
):
    thumbs_folder = data_for_deploy_folder / "thumbs"
    vtt_folder = data_for_deploy_folder / "VTT"
    logos_folder = data_for_deploy_folder / "logos"
    fixtures_path = data_for_deploy_folder / "fixtures"
    video_csv_data = [
        {**data, "code": f"VIDEO-{n}"} for n, data in enumerate(video_csv_data)
    ]
    csv_file = data_for_deploy_folder.join("videos.csv")
    with open(csv_file, "w") as file:
        writer = DictWriter(file, fieldnames=VideoConstants.FIELDS_FOR_CSV_BULK)
        writer.writeheader()
        for data in video_csv_data:
            writer.writerow(data)
    thumbs_files = [thumbs_folder.join(f"VIDEO-{n}.jpg") for n in range(5)]
    for file in thumbs_files:
        file.write("X")
    vtt_files = [vtt_folder.join(f"VIDEO-{n}.vtt") for n in range(5)]
    for file in vtt_files:
        file.write(sequences_vtt_file_content)
    logos_files = [logos_folder.join(f"logo-{n}.png") for n in range(3)]
    for file in logos_files:
        file.write("X")
    fixture = fixtures_path.join("pages.json")
    fixture.write(serializers.serialize("json", Page.objects.all()))
    home_image = data_for_deploy_folder.join("home_header_image.jpg")
    home_image.write("X")
    return data_for_deploy_folder


def test_date_serializer_for_data_list():
    data = {1: "2000-01-01", 2: "01-01-2000", 3: "01-00", 4: "X", 5: "Y"}
    fields = [1, 2, 3, 4]
    serialized_data = admin_services.date_serializer_for_data_list(data, fields)
    assert all(
        [
            datetime.strptime(value, "%Y-%m-%d") if value is not None else True
            for field, value in serialized_data.items()
            if field in fields
        ]
    )


def test_bulk_update_data_for_deploy(data_for_deploy):
    admin_services.bulk_update_data_for_deploy(str(data_for_deploy))
    videos = Video.objects.all()
    assert videos.count() == 5
    assert all(
        [
            (video.thumb.url and video.sequences.count() == 4)
            for video in Video.objects.all()
        ]
    )
    page = Page.objects.filter(slug="home").first()
    assert page.header_image.url == "/media/page_images/home_header_image.jpg"
    assert Logo.objects.count() == 3
    assert Page.objects.count() == 2
