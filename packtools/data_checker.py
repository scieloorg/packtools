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
from packtools.sps.validation.xml_validator_rules import get_default_rules


class XMLContentValidator:
    def __init__(self, params):
        self.params = params
        self.STANDARD_HEADER = (
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
        self.less_cols = (
            "response",
            "item",
            "title",
            "context",
            "advice",
            "got_value",
            "expected_value",
            "data",
        )

    def format_context(self, row):
        parent_id = row["parent_id"] or ''
        parent = row["parent"]
        
        parent = f"{parent} {parent_id}"
        title = []
        for k in ("item", "sub_item"):
            if row[k] not in title:
                if row[k]:
                    title.append(row[k])
        return {"context": parent, "item": " / ".join(title)}

    def filter_rows(self, rows, headers=None):
        for row in rows:
            if not row:
                continue
            if row["response"] == "OK":
                continue
            row_ = {}
            for k in self.less_cols:
                try:
                    row_[k] = row[k]
                except KeyError:
                    pass
            row_.update(self.format_context(row))
            yield row_

    def write_report(self, fieldnames, rows, report_file_path):
        with open(report_file_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"Report created: {report_file_path}")

    def validate(self, xmltree, errors):
        for result in validate_xml_content(xmltree, self.params):
            for item in result["items"]:
                try:
                    if item:
                        yield item
                except Exception as e:
                    errors.append(str(e))

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

    files = []
    if os.path.isdir(xml_path):
        if not report_path:
            report_path = xml_path
        files = [os.path(xml_path, f) for f in os.listdir(xml_path)]
    elif os.path.isfile(xml_path):
        if not report_path:
            report_path = os.path.dirname(xml_path)
        files = [xml_path]

    found = False
    for file_path in files:
        f = os.path.basename(file_path)
        yield {
            "xml_path": file_path,
            "report_path": os.path.join(report_path, f + ".csv"),
            "err_path": os.path.join(report_path, f + ".err"),
        }
        found = True
    if not found:
        raise FileNotFoundError(xml_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate XML content")
    parser.add_argument("xml_path", type=str, help="XML path")
    parser.add_argument("--report_path", type=str, help="CSV output file path.")

    args = parser.parse_args()

    validator = XMLContentValidator(get_default_rules())

    try:
        for item in check_paths(args.xml_path, args.report_path):
            print()
            print(item["xml_path"])

            xmltree = validator.get_xml_tree(item["xml_path"])

            errors = []
            rows = validator.validate(xmltree, errors)
            filtered_rows = validator.filter_rows(rows)
            validator.write_report(validator.less_cols, filtered_rows, item["report_path"])

            if errors:
                with open(item["err_path"], "w") as err_file:
                    err_file.write("\n".join(errors))
                print(item["err_path"])

    except FileNotFoundError as e:
        sys.exit(f"Unable to find XML files: {e}")

