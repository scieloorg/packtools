from packtools.sps.utils.file_utils import (
    get_files_list_filtered, 
    get_file_content_from_zip,
)
from packtools.sps.utils.xml_utils import get_xml_tree
from packtools.sps.validation import erratum
from packtools.sps.models.article_and_subarticles import ArticleAndSubArticles
from packtools.sps.models.article_doi_with_lang import DoiWithLang
from packtools.sps.models.front_articlemeta_issue import ArticleMetaIssue
from packtools.sps.models.front_journal_meta import ISSN, Acronym


class PackageErratumHasUnexpectedQuantityOfXMLFilesError(Exception):
    ...


class PackageErratumHasNoErrataXMLFileError(Exception):
    ...


class PackageErratumHasNoArticleXMLFileError(Exception):
    ...


class Package:
    def __init__(self, zip_path):
        self.zip_path = zip_path
        self.xmltree_article = None


class PackageWithErrata(Package):
    def __init__(self, zip_path, errata_types=['correction']):
        super().__init__(zip_path)

        self.xmltree_errata = None
        self.errata_types = errata_types
        self.discover_errata_and_article_xmls()

    def discover_errata_and_article_xmls(self):
        xmls = get_files_list_filtered(self.zip_path, ['.xml'])
        if len(xmls) != 2:
            raise PackageErratumHasUnexpectedQuantityOfXMLFilesError()

        for file_name in xmls:
            x_file_content = get_file_content_from_zip(file_name, self.zip_path)
            x_tree = get_xml_tree(x_file_content)
            x_article_and_subarticles = ArticleAndSubArticles(x_tree)

            if x_article_and_subarticles.main_article_type in self.errata_types:
                self.xmltree_errata = x_tree
            else:
                self.xmltree_article = x_tree

        if self.xmltree_article is None:
            raise PackageErratumHasNoArticleXMLFileError()

        if self.xmltree_errata is None:
            raise PackageErratumHasNoErrataXMLFileError()

    def is_valid(self):
        return erratum.has_compatible_errata_and_document(self.xmltree_errata, self.xmltree_article)


class PackageArticle(Package):
    def __init__(self, zip_path):
        super().__init__(zip_path)
        self.discover_article_xml()

    def discover_article_xml(self):
        xmls = get_files_list_filtered(self.zip_path, ['.xml'])
        if len(xmls) != 1:
            raise PackageErratumHasUnexpectedQuantityOfXMLFilesError()

        x_file_content = get_file_content_from_zip(xmls.pop(), self.zip_path)
        self.xmltree_article = get_xml_tree(x_file_content)


class PackageName:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def name(self):
        dwl = DoiWithLang(self.xmltree)
        _doi = dwl.main_doi and dwl.main_doi.split("/")[-1]

        ami = ArticleMetaIssue(self.xmltree)
        _fpage = ami.fpage
        if ami.fpage_seq:
            _fpage += ami.fpage_seq
        last_item = str(_fpage or ami.elocation_id or ami.order or _doi).zfill(5)

        issn = ISSN(self.xmltree)
        acron = Acronym(self.xmltree)
        data = (
            issn.epub or issn.ppub,
            acron.text,
            ami.volume,
            ami.number,
            ami.suppl and f"s{ami.suppl}",
            last_item,
        )
        return "-".join([str(item).zfill(2) for item in data if item])
