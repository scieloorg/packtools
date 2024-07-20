from unittest import TestCase, skip

from lxml import etree
from packtools.sps.models.article_doi_with_lang import (
    DoiWithLang,
)


def _get_xmltree(doi=None, doi1=None, doi2=None):
    doi = doi or ''
    doi1 = doi1 or ''
    doi2 = doi2 or ''
    if doi:
        doi = (
            f'<article-id pub-id-type="doi">{doi}</article-id>'
        )
    if doi1:
        doi1 = (
            """<sub-article xml:lang='es' id="01" article-type='translation'><front-stub>"""
            f"""<article-id pub-id-type="doi">{doi1}</article-id>"""
            """</front-stub></sub-article>"""
        )
    if doi2:
        doi2 = (
            """<sub-article xml:lang='en' id="02" article-type='translation'><front-stub>"""
            f"""<article-id pub-id-type="doi">{doi2}</article-id>"""
            """</front-stub></sub-article>"""
        )
    s = (
        "<article xml:lang='pt' article-type='research-article'>"
        "<front>"
        "    <article-meta>"
        f"{doi}"
        "    </article-meta>"
        "</front>"
        f"{doi1}{doi2}"
        "</article>"
    )
    return etree.fromstring(s)


class TestDoiWithLang(TestCase):
    """
    """
    def setUp(self):
        doi = '10.1590/1678-69712003/administracao.v4n1p108-123'
        doi1 = '10.1590/1678-69712003/administracao.v4n1p108-123.es'
        doi2 = '10.1590/1678-69712003/administracao.v4n1p108-123.en'
        self.article_doi_with_lang = DoiWithLang(_get_xmltree(doi, doi1, doi2))

    def test_main_doi(self):
        self.assertEqual("10.1590/1678-69712003/administracao.v4n1p108-123", self.article_doi_with_lang.main_doi)

    def test_absent_main_doi(self):
        article_doi_with_lang = DoiWithLang(_get_xmltree())
        self.assertIsNone(article_doi_with_lang.main_doi)

    def test_data(self):
        self.maxDiff = None
        expected = [
            {
                "lang": "pt",
                "value": "10.1590/1678-69712003/administracao.v4n1p108-123",
                "parent": "article",
                "parent_article_type": "research-article",
            },
            {
                "lang": "es",
                "value": "10.1590/1678-69712003/administracao.v4n1p108-123.es",
                "parent": "sub-article",
                "parent_article_type": "translation",
                "parent_id": "01",
            },
            {
                "lang": "en",
                "value": "10.1590/1678-69712003/administracao.v4n1p108-123.en",
                "parent": "sub-article",
                "parent_article_type": "translation",
                "parent_id": "02",
            },
        ]
        self.assertEqual(expected, self.article_doi_with_lang.data)
