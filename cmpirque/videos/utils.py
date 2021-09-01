import re
import time

from typing import List

from django.forms import ClearableFileInput


def parse_sequences_from_vtt_file(path: str) -> List[dict]:
    def _get_seconds_from_time(str_time):
        obj_time = time.strptime(str_time, "%H:%M:%S")
        return str(obj_time)  # .tm_hour * 3600 + obj_time.tm_min * 60 + obj_time.tm_sec

    with open(path, "r") as file:
        lines = list(file.readlines())
    data_to_import = []
    last_line = None
    for index, line in enumerate(lines):
        if last_line is None:
            assert not data_to_import
            assert re.match(
                "WEBVTT", line
            ), f"Error in line {index} of vtt file: {path}"
        if re.match(r"\d+\n", line):
            assert re.match(
                "\n", last_line
            ), f"Error in line {index} of vtt file: {path}"
        if re.match(r"[\d:.]* --> [\d:.]*", line):
            assert re.match(
                r"\d+\n", last_line
            ), f"Error in line {index} of vtt file: {path}"
            ini, end = re.findall(r"[\d:]{8}", line)
            # ini = _get_seconds_from_time(ini)
            # end = _get_seconds_from_time(end)
        if last_line and re.match(r"[\d:.]* --> [\d:.]*", last_line):
            data_to_import.append({"content": line, "ini": ini, "end": end})
        last_line = line
    return data_to_import


class ImageFileInput(ClearableFileInput):
    template_name = "admin/field_image_input.html"
