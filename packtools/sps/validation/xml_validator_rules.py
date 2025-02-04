import os
import json
import logging


def fix_json(content):
    temp = " ".join(content.split())
    return temp.replace(", ]", "]").replace(", }", "}")


def get_rules():
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
    return rules


def get_default_lists():
    lists = {}
    filenames = (
        "country_codes",
        "language_codes",
        "special_chars",
    )
    for filename in filenames:
        with open(f"packtools/sps/sps_versions/default/{filename}.json") as fp:
            content_file = fix_json(fp.read())
        data = json.loads(content_file)
        lists.update(data)
    return lists


class XMLContentValidatorRules:
    def __init__(
        self, journal_data=None, customized_rules=None
    ):
        self.rules = customized_rules or {}
        self.journal_data = journal_data or {}

    @property
    def rules(self):
        return self._rules or {}

    @rules.setter
    def rules(self, value):
        self._rules = {}
        self._rules.update(get_default_lists())
        self._rules.update(get_rules())
        self._rules["article_doi_rules"]["doi_api_get"] = None
        self._rules.update(value or {})

    @property
    def journal_data(self):
        return self._journal_data or {}

    @journal_data.setter
    def journal_data(self, value):
        # {
        #     "subject_list": [
        #         "Article",
        #         "Articles",
        #         "Artigo",
        #         "Artigos",
        #         "Artículos",
        #         "Artículo",
        #     ],
        #     "article_type_vs_subject_expected_similarity": 0.75,
        #     "expected_license_code": "by",
        #     "abbrev_journal_title": "",
        #     "publisher_name_list": [],
        #     "nlm_journal_title": None,
        # }
        self._journal_data = value

    @property
    def params(self):
        params = {}
        params.update(self.rules)
        params["journal_data"] = self.journal_data
        return params
