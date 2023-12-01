# from csv import DictReader
from datetime import datetime

# from pathlib import Path
from typing import List

# from django.core import serializers
# from django.conf import settings
# from django.db import transaction
# from django.utils.text import slugify

# from killay.videos.lib.constants import VideoConstants
from killay.admin.models import SiteConfiguration

# from killay.pages.models import Page


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


def get_site_configuration():
    return SiteConfiguration.objects.current()
