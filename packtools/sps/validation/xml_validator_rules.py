import os
import json
import logging
from importlib.resources import files


def json_loads(content):
    try:
        return json.loads(content)
    except Exception as e:        
        return json.loads(fix_json(content))

def read_json(path):
    if path and os.path.isfile(path):
        with open(path, "r") as fp:
            data = json_loads(fp.read())
        return data
    return {}


def fix_json(content):
    content = content.strip()
    temp = " ".join(content.split())
    return temp.replace(", ]", "]").replace(", }", "}")


def get_default_rules():
    params_path = "packtools.sps.validation_rules"
    rules = {}
    for entry in files(params_path).iterdir():
        filename = entry.name
        if filename.endswith(".json"):
            content = (
                files(params_path)
                .joinpath(filename)
                .read_text()
            )
            rules.update(json_loads(content) or {})
    rules["journal_data"] = None
    return rules


def get_group_rules(group):
    params_path = "packtools.sps.validation_rules"
    content = files(params_path).joinpath(f"{group}_rules.json").read_text()
    return json_loads(content)
