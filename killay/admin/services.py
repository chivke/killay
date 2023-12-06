from datetime import datetime

from typing import List

from killay.admin.models import SiteConfiguration


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
