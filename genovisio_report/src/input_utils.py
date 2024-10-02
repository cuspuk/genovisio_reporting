import gzip
import json
from typing import Any

from genovisio_report.src import core, exceptions


def load_json_from_path(path: str) -> dict[str, Any]:
    if path.endswith(core.GZIP_EXTENSION):
        with gzip.open(path, "rt", encoding="utf-8") as f:
            json_dct = json.load(f)
    elif path.endswith(core.JSON_EXTENSION):
        with open(path, "r") as f:
            json_dct = json.load(f)
    else:
        raise exceptions.InputFileInvalidError(path, [core.GZIP_EXTENSION, core.JSON_EXTENSION])
    return json_dct
