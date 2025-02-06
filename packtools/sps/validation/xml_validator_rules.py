import os
import json
import logging


def fix_json(content):
    temp = " ".join(content.split())
    return temp.replace(", ]", "]").replace(", }", "}")


def get_default_rules():
    rules = {}
    dirname = "packtools/sps/validation_rules"
    for filename in os.listdir(dirname):
        if filename.endswith(".json"):
            path = os.path.join(dirname, filename)
            try:
                with open(path, "r") as fp:
                    content_file = fix_json(fp.read())
                rules.update(json.loads(content_file))
            except Exception as e:
                logging.exception(f"{filename}: {e}")
    rules["journal_data"] = None
    return rules
