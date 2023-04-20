import argparse
import json
import logging

from datetime import datetime, date

from packtools.sps.utils import xml_utils
from tests.sps.validation.test_article_authors import credit_terms_and_urls


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
        validation_output = self.validation_report()
        data = []

        if output_file_path:
            for result in list(validation_output):
                data.append(json.dumps(result, cls=DateTimeEncoder))
                    
            with open(f"{output_file_path}" , "w") as f:
                f.write(",\n".join(data))

    def get_data_validation(self, data_file_path):
        if not data_file_path:
            data_file_path = 'data_validation.json'
        try:
            with open(f"{data_file_path}", 'r') as f:
                data = json.load(f)
            return data
        except json.decoder.JSONDecodeError:  # inclui json.decoder.JSONDecodeError
            LOGGER.info('Decoding JSON has failed')
        
    
    def get_xml_tree(self):
        return xml_utils.get_xml_tree(self.file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Running a ReportXML instance.")
    parser.add_argument("--arg1", type=str, help="The path to the XML file.")
    parser.add_argument("--arg2", type=str, help="File that serves as validation for articles in xml.")

    file_xml = parser.parse_args()
    validation = ValidationReportXML(file_path=file_xml.arg1)
    validation.validation_report()
    validation.save_json(output_file_path=file_xml.arg2)