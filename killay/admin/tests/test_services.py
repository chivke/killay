import pytest

# from csv import DictWriter
from datetime import datetime

# from factory import Faker
# from django.core import serializers

from killay.admin import services as admin_services

# from killay.videos.lib.constants import VideoConstants
# from killay.videos.models import Video
# from killay.pages.models import Page


pytestmark = pytest.mark.django_db


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
