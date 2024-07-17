import src

import discord, json, os
from typing import Any


gdvc_root: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
project_template_path = os.path.join(gdvc_root, "project_template.json")

def read_json(json_path : str) -> dict[str, Any]:
    with open(json_path, "r") as data:
        loaded_data = json.load(data)
        return loaded_data

def write_json(json_path : str, data) -> None:
    with open(json_path, "w") as file:
        return json.dump(data, file, indent=1)
