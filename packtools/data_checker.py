import csv
import os
import sys
import argparse
import json
import logging
from datetime import date, datetime

from importlib.resources import files
from packtools.sps.pid_provider.xml_sps_lib import XMLWithPre
from packtools.sps.validation.xml_validator import get_validation_results
from packtools.sps.validation.xml_validator_rules import read_json


class Report:
    def __init__(self, csv_file_path=None, exception_json_file_path=None):
        self.csv_file_path = csv_file_path
        self.exception_json_file_path = exception_json_file_path

        self.cols = (
            "xml",
            "response",
            "context",
            "advice",
            "detail",
        )
        self.write_header()
        self.create_empty_file(self.exception_json_file_path)

    def create_empty_file(self, file_path):
        with open(file_path, "w", newline="") as fp:
            fp.write("")

    def create_xml_report(self, csv_file_path, fieldnames, rows):
        with open(csv_file_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        # print(f"Created: {csv_file_path}")

    def write_header(self):
        with open(self.csv_file_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.cols)
            writer.writeheader()

    def write_rows(self, rows):
        with open(self.csv_file_path, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.cols)
            writer.writerows(rows)

    def register_exceptions(self, exceptions):
        if exceptions:
            with open(self.exception_json_file_path, "a") as fp:
                fp.write("\n".join([json.dumps(error) for error in exceptions])+"\n")
            print(self.exception_json_file_path)


class XMLFile:
    def __init__(self, xml_file_path, xml_csv_path):
        self.cols = (
            "response",
            "context",
            "advice",
            "detail",
        )
        self.xml_file_path = xml_file_path
        self.xml_csv_path = xml_csv_path
        self.exceptions = None
        self.results = None

    def validate(self, params):
        self.exceptions = []
        self.results = []
        try:
            xmltree = self.get_xml_tree()
        except Exception as e:
            logging.error(f"Unable to read {self.xml_file_path}")
            return

        for item in get_validation_results(xmltree, params):
            if item["response"] == "exception":
                self.exceptions.append(item)
            else:
                item["context"] = item["group"]
                item = self.get_error(item)
                if item:
                    self.results.append(item)

    def get_xml_tree(self):
        for xml_with_pre in XMLWithPre.create(path=self.xml_file_path):
            return xml_with_pre.xmltree

    # def fix_row(self, row):
    #     parent_id = row["parent_id"] or ''
    #     parent = row["parent"]
    #     suffix = ""
    #     if parent_id:
    #         suffix = f"({parent} {parent_id})"
        
    #     parent = f"{parent} {parent_id}"
    #     title = []
    #     for k in ("item", "sub_item"):
    #         if row[k] not in title:
    #             if row[k]:
    #                 title.append(row[k])
    #     return {"item": " / ".join(title) + suffix, "detail": row["data"]}

    def get_error(self, row):
        if not row:
            return
        if row["response"] == "OK":
            return
        if self.cols:
            row_ = {}
            for k in self.cols:
                try:
                    row_[k] = row[k]
                except KeyError:
                    pass
            row_["detail"] = row["data"]
            return row_
        else:
            return row

    def add_xml(self):
        for row in self.results:
            row["xml"] = self.xml_file_path
            yield row


class XMLDataChecker:
    def __init__(self, csv_file_path, exception_json_file_path, xml_path, xml_csv_path=None):
        self.xml_csv_path = xml_csv_path
        self.csv_file_path = csv_file_path
        self.exception_json_file_path = exception_json_file_path
        if self.xml_csv_path:
            if not os.path.isdir(self.xml_csv_path):
                try:
                    os.makedirs(self.xml_csv_path)
                except Exception as error:
                    pass

        self.xmls = []
        if os.path.isdir(xml_path):
            if not self.xml_csv_path:
                self.xml_csv_path = xml_path
            self.xmls = self._get_xml_file_paths(xml_path)
        elif os.path.isfile(xml_path):
            if not self.xml_csv_path:
                self.xml_csv_path = os.path.dirname(xml_path)
            self.xmls = [xml_path]

        if not self.xmls:
            raise FileNotFoundError(f"Not found xmls in {xml_path}")

    def _get_xml_file_paths(self, path):
        """
        Busca recursivamente todos os arquivos XML em um diretório e seus subdiretorios.
        
        Args:
            path (str): Caminho do diretório raiz para iniciar a busca
            
        Returns:
            list: Lista com os caminhos completos de todos os arquivos XML encontrados
        """
        xml_files = []
        
        # Percorre o diretório e subdiretorios
        for root, dirs, files in os.walk(path):
            # Filtra apenas arquivos com extensão .xml (case insensitive)
            for file in files:
                name, ext = os.path.splitext(file)
                if ext == ".xml":
                    # Constrói e adiciona o caminho completo do arquivo
                    yield os.path.join(root, file)

    def get_xml_files(self):
        for file_path in self.xmls:
            f = os.path.basename(file_path)
            try:
                yield XMLFile(
                    file_path,
                    os.path.join(self.xml_csv_path, f + ".csv"),
                )
            except Exception as e:
                print(f"Unable to read {file_path} {e}")

    def validate(self, params, csv_per_xml):
        report = Report(self.csv_file_path, self.exception_json_file_path)
        for xml_file in self.get_xml_files():
            if not xml_file:
                continue
            try:
                xml_file.validate(params)
                if csv_per_xml:
                    report.create_xml_report(xml_file.xml_csv_path, xml_file.cols, xml_file.results)
                else:
                    report.write_rows(xml_file.add_xml())
                report.register_exceptions(xml_file.exceptions)
            except Exception as e:
                print(f"Unable to process {xml_file.xml_file_path} {e}")
        if csv_per_xml:
            print("CSV file created and placed next to each XML")
        else:
            print(f"Created {self.csv_file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="XML data checker")
    parser.add_argument("xml_path", type=str, help="XML folder or file path")
    parser.add_argument("output_path", type=str, help="Ouput folder path")
    parser.add_argument("--csv_per_xml", dest='csv_per_xml', action='store_true', help="Create one csv per xml", default=False)

    args = parser.parse_args()

    if args.output_path and not os.path.isdir(args.output_path):
        os.makedirs(args.output_path)

    csv_per_xml = args.csv_per_xml
    prefix = datetime.now().isoformat().replace(" ", "").replace(":", "").replace(".", "")
    csv_file_path = os.path.join(args.output_path, f"{prefix}-errors.csv")
    exception_json_file_path = os.path.join(args.output_path, f"{prefix}-exceptions.jsonl")
    xml_path = args.xml_path
    try:
        validator = XMLDataChecker(csv_file_path, exception_json_file_path, xml_path)
        validator.validate({}, csv_per_xml)

    except FileNotFoundError as e:
        sys.exit(e)
