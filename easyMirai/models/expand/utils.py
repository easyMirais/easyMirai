import json
import os


def getApi(field: str):
    path = os.path.abspath(os.path.join(os.path.dirname(
        __file__), "../..", "data", "api", f"{field.lower()}.json"))
    if os.path.exists(path):
        with open(path, encoding="utf8") as f:
            return json.loads(f.read())
