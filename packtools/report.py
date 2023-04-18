import argparse

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


class ReportXML:
    def __init__(self, file_path):
        self.file_path = file_path

    def report(self, **kwargs):
        """
        Executa todas as classes de validação com as opções fornecidas.
        Retorna uma lista de dicionários que contêm os resultados de cada classe de validação.
        """

        xmltree = self.get_xml_tree()
        report = []
        for validation_class in all_validation_classes():
            validation = validation_class(xmltree)
            result = validation.call_methods(**kwargs)
            report.append(result)
        return report
        
    def get_xml_tree(self):
        return xml_utils.get_xml_tree(self.file_path)


if __name__ == '__main__':
    #TO_DO: Adicionar o dicionário kwargs ao arquivo .json
    kwargs = {
        'credit_terms_and_urls': credit_terms_and_urls,
        'expected_value_license': {
            'lang': 'pt',
            'link': 'http://creativecommons.org/licenses/by/4.0/',
            'licence_p': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.'
        },
        'expected_code': '4.0',
        'expected_version': 'by',
        'expected_toc_sections': {
            "es": ["Nome da seção do artigo em espanhol"],
            "en": ["Nome da seção do sub-artigo em inglês"]
        },
        'order': [
            "received", 
            "rev-request", 
            "rev-recd", 
            "accepted", 
            "approved"
        ],
        'required_events': [
            "received", 
            "approved"
        ],
        'expected_value_volume': '10',
        'expected_value_supplment': '10',
        'expected_value_issue': '10',
    }

    parser = argparse.ArgumentParser(description='Running a ReportXML instance.')
    parser.add_argument('--arg1', type=str, help='The path to the XML file.')

    file_xml = parser.parse_args()
    ReportXML(file_path=file_xml.arg1).report(**kwargs)