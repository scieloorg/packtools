from unittest import TestCase, skip

from lxml import etree
from packtools.sps.models.article_ids import (
    ArticleIds,
)


def _get_xmltree(xml=None):
    xml = xml or ''
    s = (
        "<article>"
        "<front>"
        "    <article-meta>"
        f"{xml}"
        "    </article-meta>"
        "</front>"
        "</article>"
    )
    return etree.fromstring(s)


class TestArticleIds(TestCase):
    """
    Estes testes são para explicitar a saída de
    parse_issue usando o contéudo de <issue></issue>
    """
    def setUp(self):
        xml = (
            '<article-id specific-use="scielo-v3" pub-id-type="publisher-id">P3swRmPHQfy37r9xRbLCw8G</article-id>'
            '<article-id specific-use="scielo-v2" pub-id-type="publisher-id">S1678-69712003000100108</article-id>'
            '<article-id specific-use="previous-pid" pub-id-type="publisher-id">S1678-69712002005000108</article-id>'
            '<article-id pub-id-type="doi">10.1590/1678-69712003/administracao.v4n1p108-123</article-id>'
            '<article-id pub-id-type="other">123</article-id>'
        )
        self.article_id = ArticleIds(_get_xmltree(xml))

    def test_v3(self):
        self.assertEqual("P3swRmPHQfy37r9xRbLCw8G", self.article_id.v3)

    def test_v2(self):
        self.assertEqual("S1678-69712003000100108", self.article_id.v2)

    def test_aop_pid(self):
        self.assertEqual("S1678-69712002005000108", self.article_id.aop_pid)

    def test_other(self):
        self.assertEqual("123", self.article_id.other)

    def test_doi(self):
        self.assertEqual("10.1590/1678-69712003/administracao.v4n1p108-123", self.article_id.doi)

    def test_data(self):
        expected = {
             "v3": "P3swRmPHQfy37r9xRbLCw8G",
             "v2": "S1678-69712003000100108",
             "aop_pid": "S1678-69712002005000108",
             "other": "123",
             "doi": "10.1590/1678-69712003/administracao.v4n1p108-123",
        }
        self.assertDictEqual(expected, self.article_id.data)

    def test_absent_v3(self):
        article_id = ArticleIds(_get_xmltree())
        self.assertIsNone(article_id.v3)

    def test_absent_v2(self):
        article_id = ArticleIds(_get_xmltree())
        self.assertIsNone(article_id.v2)

    def test_absent_other(self):
        article_id = ArticleIds(_get_xmltree())
        self.assertIsNone(article_id.other)

    def test_absent_doi(self):
        article_id = ArticleIds(_get_xmltree())
        self.assertIsNone(article_id.doi)

    @skip("Teste pendente de correção e/ou ajuste")
    def test_update_v3(self):
        self.article_id.v3 = "novo_v3"
        self.assertEqual("novo_v3", self.article_id.v3)

    @skip("Teste pendente de correção e/ou ajuste")
    def test_update_aop_pid(self):
        self.article_id.aop_pid = "novo_aop_pid"
        self.assertEqual("novo_aop_pid", self.article_id.aop_pid)

    @skip("Teste pendente de correção e/ou ajuste")
    def test_update_v2_raises_AttributeError(self):
        with self.assertRaises(AttributeError):
            self.article_id.v2 = "xxxx"

    def test_update_doi_raises_AttributeError(self):
        with self.assertRaises(AttributeError):
            self.article_id.doi = "xxxx"

    def test_update_other_raises_AttributeError(self):
        with self.assertRaises(AttributeError):
            self.article_id.other = "xxxx"

    def test_update_v3_raises_ValueError(self):
        with self.assertRaises(ValueError):
            self.article_id.v3 = ""

    def test_update_aop_pid_raises_ValueError(self):
        with self.assertRaises(ValueError):
            self.article_id.aop_pid = ""


class TestArticleIdsOriginalXMLHasNoArticleId(TestCase):
    """
    Estes testes são para explicitar a saída de
    parse_issue usando o contéudo de <issue></issue>
    """
    def setUp(self):
        self.article_id = ArticleIds(_get_xmltree(''))

    @skip("Teste pendente de correção e/ou ajuste")
    def test_update_v2(self):
        self.article_id.v2 = "novo_v2"
        self.assertEqual("novo_v2", self.article_id.v2)

    @skip("Teste pendente de correção e/ou ajuste")
    def test_update_v3(self):
        self.article_id.v3 = "novo_v3"
        self.assertEqual("novo_v3", self.article_id.v3)

    @skip("Teste pendente de correção e/ou ajuste")
    def test_update_aop_pid(self):
        self.article_id.aop_pid = "novo_aop_pid"
        self.assertEqual("novo_aop_pid", self.article_id.aop_pid)

    def test_update_v2_raises_ValueError(self):
        with self.assertRaises(ValueError):
            self.article_id.v2 = ""

    def test_update_v3_raises_ValueError(self):
        with self.assertRaises(ValueError):
            self.article_id.v3 = ""

    def test_update_aop_pid_raises_ValueError(self):
        with self.assertRaises(ValueError):
            self.article_id.aop_pid = ""
