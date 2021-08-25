import pytest

from csv import DictWriter
from factory import Faker

from cmpirque.videos.lib.constants import VideoConstants
from cmpirque.videos import services as videos_services

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
    with open(csv_file, "w") as file:
        writer = DictWriter(file, fieldnames=VideoConstants.FIELDS_FOR_CSV_BULK)
        writer.writeheader()
        for data in video_csv_data:
            writer.writerow(data)
    videos = videos_services.video_bulk_create_from_csv_file(csv_file)
    assert len(videos) == 5
    assert all([video.meta and video.categorization for video in videos])
    assert all([video.categorization.categories.exists() for video in videos])
    assert all([video.categorization.people.exists() for video in videos])
    assert all([video.categorization.keywords.exists() for video in videos])
