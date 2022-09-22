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

