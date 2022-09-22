from packtools.sps.utils.file_utils import (
    get_files_list_filtered, 
    get_file_content_from_zip,
)
from packtools.sps.utils.xml_utils import get_xml_tree
from packtools.sps.validation import erratum
from packtools.sps.models.article_and_subarticles import ArticleAndSubArticles


class PackageErratumHasThreeOrMoreXMLFilesError(Exception):
    ...


class PackageErratumHasNoErrataXMLFileError(Exception):
    ...


class PackageErratumHasNoArticleXMLFileError(Exception):
    ...


class Package:
    def __init__(self, zip_path):
        self.zip_path = zip_path


class PackageWithErrata(Package):
    def __init__(self, zip_path, errata_types=['correction']):
        super().__init__(zip_path)

        self.errata_types = errata_types
        self.discover_errata_and_article_xmls()

    def discover_errata_and_article_xmls(self):
        xmls = get_files_list_filtered(self.zip_path, ['.xml'])
        if len(xmls) != 2:
            raise PackageErratumHasThreeOrMoreXMLFilesError()
