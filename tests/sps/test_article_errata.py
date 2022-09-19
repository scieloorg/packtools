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
    def test_article_erratum_presence(self):
        data = """
        <fn-group>
            <fn fn-type="other">
                <label>Additions and Corrections</label>
                <p>On page 100, where it was read:</p>
                <p>“Joao S. Costa”</p>
                <p>Now reads:</p>
                <p>“João Silva Costa”</p>
            </fn>
        </fn-group>
        """
        xmltree = generate_xmltree(data)

        obtained = ArticleErrata(xmltree).article_errata.pop()

        self.assertIsInstance(obtained, Erratum)


    def test_article_erratum_label(self):
        data = """
        <fn-group>
            <fn fn-type="other">
                <label>Additions and Corrections</label>
                <p>On page 100, where it was read:</p>
                <p>“Joao S. Costa”</p>
                <p>Now reads:</p>
                <p>“João Silva Costa”</p>
            </fn>
        </fn-group>
        """
        xmltree = generate_xmltree(data)

        expected_label = 'Additions and Corrections'
        erratum = ArticleErrata(xmltree).article_errata.pop()
        obtained_label = erratum.label

        self.assertEqual(expected_label, obtained_label)


    def test_article_erratum_text(self):
        data = """
        <fn-group>
            <fn fn-type="other">
                <label>Additions and Corrections</label>
                <p>On page 100, where it was read:</p>
                <p>“Joao S. Costa”</p>
                <p>Now reads:</p>
                <p>“João Silva Costa”</p>
            </fn>
        </fn-group>
        """
        xmltree = generate_xmltree(data)

        expected_text = 'Additions and Corrections\nOn page 100, where it was read:\n“Joao S. Costa”\nNow reads:\n“João Silva Costa”'
        erratum = ArticleErrata(xmltree).article_errata.pop()
        obtained_text = erratum.text

        self.assertEqual(expected_text, obtained_text)
    
