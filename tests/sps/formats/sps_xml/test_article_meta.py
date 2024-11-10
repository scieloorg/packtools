import unittest
import xml.etree.ElementTree as ET
from packtools.sps.formats.sps_xml.article_meta import build_article_meta


class TestBuildArticleMetaPubId(unittest.TestCase):
    def test_build_article_meta_pub_id(self):
        data = {
            "pub-id-doi": "10.1016/j.bjane.2019.01.003",
            "pub-id-other": "00603"
        }
        expected_xml_str = (
            '<article-meta>'
            '<article-id pub-id-type="doi">10.1016/j.bjane.2019.01.003</article-id>'
            '<article-id pub-id-type="other">00603</article-id>'
            '</article-meta>'
        )
        article_meta_elem = build_article_meta(data)
        generated_xml_str = ET.tostring(article_meta_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_article_meta_pub_id_None(self):
        data = {
            "pub-id-doi": None,
            "pub-id-other": None
        }
        expected_xml_str = (
            '<article-meta />'
        )
        article_meta_elem = build_article_meta(data)
        generated_xml_str = ET.tostring(article_meta_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildArticleMetaCategories(unittest.TestCase):
    def test_build_article_meta_categories(self):
        data = {
            "article-subject": "Original Article"
        }
        expected_xml_str = (
            '<article-meta>'
            '<article-categories>'
            '<subj-group subj-group-type="heading">'
            '<subject>Original Article</subject>'
            '</subj-group></article-categories>'
            '</article-meta>'
        )
        article_meta_elem = build_article_meta(data)
        generated_xml_str = ET.tostring(article_meta_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_article_meta_categories_None(self):
        data = {
            "article-subject": None
        }
        expected_xml_str = (
            '<article-meta />'
        )
        article_meta_elem = build_article_meta(data)
        generated_xml_str = ET.tostring(article_meta_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildArticleMetaTitle(unittest.TestCase):
    def test_build_article_meta_title(self):
        data = {
            "article-title": "Conocimientos de los pediatras sobre la laringomalacia",
            "trans-title": {
                "en": "Pediatrician knowledge about laryngomalacia",
            }
        }
        expected_xml_str = (
            '<article-meta>'
            '<title-group>'
            '<article-title>Conocimientos de los pediatras sobre la laringomalacia</article-title>'
            '<trans-title-group xml:lang="en">'
            '<trans-title>Pediatrician knowledge about laryngomalacia</trans-title>'
            '</trans-title-group>'
            '</title-group>'
            '</article-meta>'
        )
        article_meta_elem = build_article_meta(data)
        generated_xml_str = ET.tostring(article_meta_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_article_meta_title_None(self):
        data = {
            "article_title": None,
            "trans_title": None
        }
        expected_xml_str = (
            '<article-meta />'
        )
        article_meta_elem = build_article_meta(data)
        generated_xml_str = ET.tostring(article_meta_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildArticleMetaContribs(unittest.TestCase):

    def test_build_article_meta_contribs(self):
        self.maxDiff = None
        node = {
            "contrib-group": [
                ET.fromstring(
                    '<contrib contrib-type="author">'
                    '<contrib-id contrib-id-type="orcid">0000-0003-2243-0821</contrib-id>'
                    '<name>'
                    '<surname>Castro</surname>'
                    '<given-names>Silvana de</given-names>'
                    '</name>'
                    '<xref ref-type="aff" rid="aff1">a</xref>'
                    '<xref ref-type="corresp" rid="c1">*</xref>'
                    '</contrib>'
                )
            ]
        }
        data = {}
        expected_xml_str = (
            '<article-meta>'
            '<contrib-group>'
            '<contrib contrib-type="author">'
            '<contrib-id contrib-id-type="orcid">0000-0003-2243-0821</contrib-id>'
            '<name>'
            '<surname>Castro</surname>'
            '<given-names>Silvana de</given-names>'
            '</name>'
            '<xref ref-type="aff" rid="aff1">a</xref>'
            '<xref ref-type="corresp" rid="c1">*</xref>'
            '</contrib>'
            '</contrib-group>'
            '</article-meta>'
        )
        article_meta_elem = build_article_meta(data, node)
        generated_xml_str = ET.tostring(article_meta_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildArticleMetaAffs(unittest.TestCase):

    def test_build_article_meta_affiliation(self):
        self.maxDiff = None
        node = {
            "affs": [
                ET.fromstring(
                    '<aff id="aff2">'
                    '<label>b</label>'
                    '<institution content-type="orgname">Universidade Federal Fluminense</institution>'
                    '<addr-line>'
                    '<named-content content-type="city">Niterói</named-content>'
                    '<named-content content-type="state">RJ</named-content>'
                    '</addr-line>'
                    '<country country="BR">Brazil</country>'
                    '<institution content-type="original">Universidade Federal Fluminense (UFF), Niterói, RJ, Brazil</institution>'
                    '</aff>'
                )
            ]
        }
        data = {}
        expected_xml_str = (
            '<article-meta>'
            '<aff id="aff2">'
            '<label>b</label>'
            '<institution content-type="orgname">Universidade Federal Fluminense</institution>'
            '<addr-line>'
            '<named-content content-type="city">Niterói</named-content>'
            '<named-content content-type="state">RJ</named-content>'
            '</addr-line>'
            '<country country="BR">Brazil</country>'
            '<institution content-type="original">Universidade Federal Fluminense (UFF), Niterói, RJ, Brazil</institution>'
            '</aff>'
            '</article-meta>'
        )
        article_meta_elem = build_article_meta(data, node)
        generated_xml_str = ET.tostring(article_meta_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildArticleMetaAuthorNotes(unittest.TestCase):

    def test_build_article_meta_author_notes(self):
        self.maxDiff = None
        node = {
            "author-notes": ET.fromstring(
                    '<author-notes>'
                    '<corresp id="c1">'
                    '<label>*</label>'
                    '<email>s.lellouchedecastro@gmail.com</email>'
                    '</corresp>'
                    '<fn fn-type="conflict">'
                    '<p>'
                    '<bold>Conflicts of interest</bold>'
                    '</p>'
                    '<p>The authors declare no conflicts of interest.</p>'
                    '</fn>'
                    '</author-notes>'
                )
        }
        data = {}
        expected_xml_str = (
            '<article-meta>'
            '<author-notes>'
            '<corresp id="c1">'
            '<label>*</label>'
            '<email>s.lellouchedecastro@gmail.com</email>'
            '</corresp>'
            '<fn fn-type="conflict">'
            '<p><bold>Conflicts of interest</bold></p>'
            '<p>The authors declare no conflicts of interest.</p>'
            '</fn>'
            '</author-notes>'
            '</article-meta>'
        )
        article_meta_elem = build_article_meta(data, node)
        generated_xml_str = ET.tostring(article_meta_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildArticleMetaPubDates(unittest.TestCase):

    def test_build_article_meta_pub_dates(self):
        self.maxDiff = None
        node = {
            "pub-dates": ET.fromstring(
                '<pub-date publication-format="electronic" date-type="collection">'
                '<season>Jan-Fev</season>'
                '<year>2024</year>'
                '</pub-date>'
                )
        }
        data = {}
        expected_xml_str = (
            '<article-meta>'
            '<pub-date publication-format="electronic" date-type="collection">'
            '<season>Jan-Fev</season>'
            '<year>2024</year>'
            '</pub-date>'
            '</article-meta>'
        )
        article_meta_elem = build_article_meta(data, node)
        generated_xml_str = ET.tostring(article_meta_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildArticleMetaAttribs(unittest.TestCase):
    def test_build_article_meta_attribs(self):
        data = {
            "volume": "69",
            "issue": "3",
            "fpage": "227",
            "lpage": "232"
        }
        expected_xml_str = (
            '<article-meta>'
            '<volume>69</volume>'
            '<issue>3</issue>'
            '<fpage>227</fpage>'
            '<lpage>232</lpage>'
            '</article-meta>'
        )
        article_meta_elem = build_article_meta(data)
        generated_xml_str = ET.tostring(article_meta_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_article_meta_attribs_None(self):
        data = {
            "volume": None,
            "issue": None,
            "fpage": None,
            "lpage": None
        }
        expected_xml_str = (
            '<article-meta />'
        )
        article_meta_elem = build_article_meta(data)
        generated_xml_str = ET.tostring(article_meta_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildArticleMetaAbstract(unittest.TestCase):

    def test_build_article_meta_abstract(self):
        self.maxDiff = None
        node = {
            "abstract": ET.fromstring(
                '<abstract>'
                '<title>Resumo</title>'
                '<sec>'
                '<title>Objetivo</title>'
                '<p>Verificar a sensibilidade e...</p>'
                '</sec>'
                '<sec>'
                '<title>Métodos</title>'
                '<p>Durante quatro meses foram...</p>'
                '</sec>'
                '</abstract>'
            )
        }
        data = {}
        expected_xml_str = (
            '<article-meta>'
            '<abstract>'
            '<title>Resumo</title>'
            '<sec>'
            '<title>Objetivo</title>'
            '<p>Verificar a sensibilidade e...</p>'
            '</sec>'
            '<sec>'
            '<title>Métodos</title>'
            '<p>Durante quatro meses foram...</p>'
            '</sec>'
            '</abstract>'
            '</article-meta>'
        )
        article_meta_elem = build_article_meta(data, node)
        generated_xml_str = ET.tostring(article_meta_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildArticleMetaTransAbstract(unittest.TestCase):

    def test_build_article_meta_trans_abstract(self):
        self.maxDiff = None
        node = {
            "trans-abstracts": [
                ET.fromstring(
                    '<trans-abstract xml:lang="en">'
                    '<title>Abstract</title>'
                    '<sec>'
                    '<title>Objective</title>'
                    '<p>To analyze the association between...</p>'
                    '</sec>'
                    '<sec>'
                    '<title>Method</title>'
                    '<p>Analytical study conducted with... </p>'
                    '</sec>'
                    '</trans-abstract>'
                )
            ]
        }
        data = {}
        expected_xml_str = (
            '<article-meta>'
            '<trans-abstract xml:lang="en">'
            '<title>Abstract</title>'
            '<sec>'
            '<title>Objective</title>'
            '<p>To analyze the association between...</p>'
            '</sec>'
            '<sec>'
            '<title>Method</title>'
            '<p>Analytical study conducted with... </p>'
            '</sec>'
            '</trans-abstract>'
            '</article-meta>'
        )
        article_meta_elem = build_article_meta(data, node)
        generated_xml_str = ET.tostring(article_meta_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildArticleMetaKwdGroup(unittest.TestCase):

    def test_build_article_meta_kwd_group(self):
        self.maxDiff = None
        node = {
            "kwd-group": [
                ET.fromstring(
                    '<kwd-group xml:lang="pt">'
                    '<title>Palavra-chave</title>'
                    '<kwd>Broncoscopia</kwd>'
                    '</kwd-group>'
                )
            ]
        }
        data = {}
        expected_xml_str = (
            '<article-meta>'
            '<kwd-group xml:lang="pt">'
            '<title>Palavra-chave</title>'
            '<kwd>Broncoscopia</kwd>'
            '</kwd-group>'
            '</article-meta>'
        )
        article_meta_elem = build_article_meta(data, node)
        generated_xml_str = ET.tostring(article_meta_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildArticleMetaHistory(unittest.TestCase):

    def test_build_article_meta_history(self):
        self.maxDiff = None
        node = {
            "history": ET.fromstring(
                '<history>'
                '<date date-type="received">'
                '<day>15</day>'
                '<month>03</month>'
                '<year>2013</year>'
                '</date>'
                '<date date-type="rev-recd">'
                '<day>06</day>'
                '<month>11</month>'
                '<year>2013</year>'
                '</date>'
                '</history>'
            )
        }
        data = {}
        expected_xml_str = (
            '<article-meta>'
            '<history>'
            '<date date-type="received">'
            '<day>15</day>'
            '<month>03</month>'
            '<year>2013</year>'
            '</date>'
            '<date date-type="rev-recd">'
            '<day>06</day>'
            '<month>11</month>'
            '<year>2013</year>'
            '</date>'
            '</history>'
            '</article-meta>'
        )
        article_meta_elem = build_article_meta(data, node)
        generated_xml_str = ET.tostring(article_meta_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildArticleMetaPermissions(unittest.TestCase):

    def test_build_article_meta_permissions(self):
        self.maxDiff = None
        node = {
            "permissions": ET.fromstring(
                '<permissions xmlns:xlink="http://www.w3.org/1999/xlink">'
                '<license license-type="open-access" '
                'xlink:href="http://creativecommons.org/licenses/by-nc-sa/4.0/" '
                'xml:lang="pt">This is an article published in open access under a Creative Commons license'
                '</license>'
                '</permissions>'
            )
        }
        data = {}
        expected_xml_str = (
            '<article-meta xmlns:ns0="http://www.w3.org/1999/xlink">'
            '<permissions>'
            '<license license-type="open-access" ns0:href="http://creativecommons.org/licenses/by-nc-sa/4.0/" xml:lang="pt">'
            'This is an article published in open access under a Creative Commons license'
            '</license>'
            '</permissions>'
            '</article-meta>'
        )
        article_meta_elem = build_article_meta(data, node)
        generated_xml_str = ET.tostring(article_meta_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildArticleMetaFundingGroup(unittest.TestCase):

    def test_build_article_meta_funding_group(self):
        self.maxDiff = None
        node = {
            "funding-group": ET.fromstring(
                '<funding-group>'
                '<award-group>'
                '<funding-source>CNPQ</funding-source>'
                '<award-id>12345</award-id>'
                '</award-group>'
                '</funding-group>'
            )
        }
        data = {}
        expected_xml_str = (
            '<article-meta>'
            '<funding-group>'
            '<award-group>'
            '<funding-source>CNPQ</funding-source>'
            '<award-id>12345</award-id>'
            '</award-group>'
            '</funding-group>'
            '</article-meta>'
        )
        article_meta_elem = build_article_meta(data, node)
        generated_xml_str = ET.tostring(article_meta_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildArticleMetaCounts(unittest.TestCase):

    def test_build_article_meta_counts(self):
        self.maxDiff = None
        data = {
            "fig-count": "5",
            "table-count": "3",
            "equation-count": "10",
            "ref-count": "26",
            "page-count": "6"
        }
        expected_xml_str = (
            '<article-meta>'
            '<counts>'
            '<fig-count count="5" />'
            '<table-count count="3" />'
            '<equation-count count="10" />'
            '<ref-count count="26" />'
            '<page-count count="6" />'
            '</counts>'
            '</article-meta>'
        )
        article_meta_elem = build_article_meta(data)
        generated_xml_str = ET.tostring(article_meta_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_article_meta_counts_None(self):
        self.maxDiff = None
        data = {
            "fig-count": None,
            "table-count": None
        }
        expected_xml_str = (
            '<article-meta />'
        )
        article_meta_elem = build_article_meta(data)
        generated_xml_str = ET.tostring(article_meta_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


