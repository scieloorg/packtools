import argparse
import json
import logging

from datetime import date

from packtools.sps.utils import xml_utils


from packtools.sps.validation import (
    aff,
    article_authors,
    article_license,
    article_toc_sections,
    article_xref,
    dates,
    front_articlemeta_issue
)        

LOGGER = logging.getLogger(__name__)


def all_validation_classes():
    """
    Retorna uma lista de todas as classes de validação disponíveis.
    """
    classes = [
        aff.AffiliationValidation,
        article_authors.ArticleAuthorsValidation, 
        article_license.ArticleLicenseValidation, 
        article_toc_sections.ArticleTocSectionsValidation, 
        article_xref.ArticleXrefValidation,
        dates.ArticleDatesValidation, 
        front_articlemeta_issue.IssueValidation, 
    ]
    return classes


class DateTimeEncoder(json.JSONEncoder):
    """
    Classe que serializa objetos `date` em formato ISO para JSON.
    """
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)


class ValidationReportXML:
    def __init__(self, file_path, data_file_path=None):
        self.file_path = file_path
        self.data_validation = self.get_data_validation(data_file_path)

    def validation_report(self):
        """
        Executa todas as classes de validação com as opções fornecidas.
        Retorna um gerador que produz uma sequência de dicionários que contêm os resultados de cada classe de validação.
        """

        xmltree = self.get_xml_tree()
        for validation_class in all_validation_classes():
            validation = validation_class(xmltree)
            result = validation.validate(self.data_validation)
            yield result

    def save_json(self, output_file_path=None):
        """
        Salva um relatório de validação como uma lista de objetos JSON em um arquivo.
        """

        validation_output = self.validation_report()
        data = {}
        for result in validation_output:
            data.update(result)

        if output_file_path:                    
            try:
                with open(f"{output_file_path}", "w", encoding="utf-8") as f:
                    json.dump(data, f, cls=DateTimeEncoder)
            except IOError as e:
                LOGGER.error(f"Unable to create file on disk: {e}")
            except json.decoder.JSONDecodeError as e:
                LOGGER.error(f"JSON decoding error when saving in output file {output_file_path}: {e}")

    def get_data_validation(self, data_file_path):
        """
        Carrega dados de um arquivo JSON no caminho especificado ou em um arquivo de exemplo.
        """

        data_file_path = data_file_path or 'validation_criteria_example.json'

        try:
            with open(f"{data_file_path}", 'r') as f:
                data = json.load(f)
            return data
        except json.decoder.JSONDecodeError as e:
            LOGGER.error(f"Decoding JSON has failed: {e}")
        except FileNotFoundError as e:
            LOGGER.error(f"File not found: {e}") 
        
    def get_xml_tree(self):
        return xml_utils.get_xml_tree(self.file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Running a ReportXML instance.")
    parser.add_argument("--xml_file_path", type=str, help="The path to the XML file.")
    parser.add_argument("--validation_report_file_path", type=str, help="File that serves as validation for articles in xml.")

    xml_file_args = parser.parse_args()
    validation = ValidationReportXML(file_path=xml_file_args.xml_file_path)
    validation.validation_report()
    validation.save_json(output_file_path=xml_file_args.validation_report_file_path)