import re

from typing import List


def parse_sequences_from_vtt_file(path: str) -> List[dict]:
    with open(path, "r", encoding="utf-8") as file:
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
        if last_line and re.match(r"[\d:.]* --> [\d:.]*", last_line):
            data_to_import.append({"content": line, "ini": ini, "end": end})
        last_line = line
    return data_to_import
