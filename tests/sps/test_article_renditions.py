from unittest import TestCase

from packtools.sps.utils import xml_utils

from packtools.sps.models.article_renditions import ArticleRenditions


def generate_xmltree(extralang1, extralang2=None, extralang3=None):
    xml = """
    <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
        <front>
            <article-meta>
                {0}
            </article-meta>
        </front>
        {1}
        {2}
        <body>
            <sec><p>The Eh measurements... <xref ref-type="fig" rid="f01">Figura 1</xref>:</p></sec>
        </body>
    </article>
    """
    return xml_utils.get_xml_tree(xml.format(extralang1, extralang2, extralang3))

