import json
from typing import Any

cpdef object load_config(str path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
