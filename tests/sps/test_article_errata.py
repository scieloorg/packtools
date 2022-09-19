from unittest import TestCase

from packtools.sps.utils import xml_utils

from packtools.sps.models.article_errata import ArticleErrata, Erratum


def generate_xmltree(erratum1, erratum2=None):
    xml = """
    <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
        <front>
            <article-meta></article-meta>
        </front>
        <body>
        </body>
        <back>
        {0}
        {1}
        </back>
    </article>
    """
    return xml_utils.get_xml_tree(xml.format(erratum1, erratum2))


class ArticleErrataTest(TestCase):
