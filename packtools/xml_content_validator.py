import csv
import os
import sys
import argparse
import json
import logging
from datetime import date, datetime

from importlib.resources import files
from packtools.sps.pid_provider.xml_sps_lib import XMLWithPre

from packtools.sps.validation.xml_validator import validate_xml_content
from packtools.sps.validation.xml_validator_rules import XMLContentValidatorRules


class XMLContentValidator:
    def __init__(self, xml_content_validator_rules):
        self.xml_content_validator_rules = xml_content_validator_rules

    def write_report(self, report_file_path, rows):
        headers = (
            "response",
            "message",
            "advice",
            "data",
            "group",
            "item",
            "sub_item",
            "validation_type",
            "title",
            "parent",
            "parent_id",
            "parent_article_type",
            "parent_lang",
            "expected_value",
            "got_value",
        )
        with open(report_file_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)

    def validate(self, xmltree):
        sps_version = xmltree.find(".").get("specific-use")
        self.xml_content_validator_rules.sps_version = sps_version

        for result in validate_xml_content(xmltree, self.xml_content_validator_rules):
            group = result["group"]
            items = result["items"] or {}
            try:
                for item in items:
                    item["group"] = group
                    yield item
            except Exception as e:
                logging.exception(e)
                print(e)
                print(result)
                print("")

    def get_xml_tree(self, xml_file_path):
        for xml_with_pre in XMLWithPre.create(path=xml_file_path):
            return xml_with_pre.xmltree


def check_paths(xml_path, report_path):
    if report_path:
        if not os.path.isdir(report_path):
            try:
                os.makedirs(report_path)
            except Exception as error:
                report_path = None

    if os.path.isdir(xml_path):
        if not report_path:
            report_path = xml_path
        for f in os.listdir(xml_path):
            if f.endswith(".xml"):
                file_path = os.path.join(xml_path, f)
                yield {
                    "xml_path": file_path,
                    "report_path": os.path.join(report_path, f + ".csv"),
                }

    elif os.path.isfile(xml_path):
        if not report_path:
            report_path = os.path.dirname(xml_path)
        yield {
            "xml_path": xml_path,
            "report_path": os.path.join(report_path, f + ".csv"),
        }

    else:
        return []


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate XML content")
    parser.add_argument("xml_path", type=str, help="XML path")
    parser.add_argument("--report_path", type=str, help="CSV output file path.")

    args = parser.parse_args()

    xml_content_validator_rules = XMLContentValidatorRules()
    validator = XMLContentValidator(xml_content_validator_rules)

    paths = list(check_paths(args.xml_path, args.report_path))
    if not paths:
        sys.exit(f"{args.xml_path} is not XML file or has no XML files")
    for item in paths:
        xmltree = validator.get_xml_tree(item["xml_path"])
        rows = validator.validate(xmltree)
        validator.write_report(item["report_path"], rows)
        print(f'{item["xml_path"]} - report created: {item["report_path"]}')
