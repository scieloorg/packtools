import logging
from unittest import TestCase
from unittest.mock import patch

from lxml import etree

from packtools.sps.pid_provider.xml_sps_adapter import (PidProviderXMLAdapter,
                                                        _str_with_64_char)
from packtools.sps.pid_provider.xml_sps_lib import XMLWithPre


def _get_xml_adapter(xml=None):
    xml = xml or (
        """
        <article>
            <front>
                <article-meta/>
            </front>
        </article>
    """
    )
    xmltree = etree.fromstring(xml)
    xml_with_pre = XMLWithPre("", xmltree)
    return PidProviderXMLAdapter(xml_with_pre)


class PidProviderXMLAdapterAbsentDataTest(TestCase):
    def setUp(self):
        self.xml_adapter = _get_xml_adapter()

    def test_is_aop(self):
        self.assertTrue(self.xml_adapter.is_aop)

    def test_absent_links(self):
        self.assertIsNone(self.xml_adapter.z_links)

    def test_absent_collab(self):
        self.assertIsNone(self.xml_adapter.z_collab)

    def test_absent_surnames(self):
        self.assertIsNone(self.xml_adapter.z_surnames)

    def test_absent_article_titles_texts(self):
        self.assertIsNone(self.xml_adapter.z_article_titles_texts)


class PidProviderXMLAdapterIssnsTest(TestCase):
    def _get_xml_adapter(self, eissn=None, pissn=None):
        if eissn:
            eissn = f'<issn pub-type="epub">{eissn}</issn>'
        if pissn:
            pissn = f'<issn pub-type="ppub">{pissn}</issn>'
        xml = f"""
            <article>
                <front>
                    <journal-meta>
                      {eissn}{pissn}
                    </journal-meta>
                    <article-meta>
                        <pub-date publication-format="electronic" date-type="pub">
                        <day>29</day>
                        <month>10</month>
                        <year>2020</year>
                      </pub-date>
                      <pub-date date-type="collection" publication-format="electronic">
                        <year>2021</year>
                      </pub-date>
                      <volume>29</volume>
                    </article-meta>
                </front>
            </article>
        """
        return _get_xml_adapter(xml)

    def test_v2_prefix_with_print_issn(self):
        xml_adapter = self._get_xml_adapter(pissn="0104-1169")
        self.assertEqual("S0104-11692021", xml_adapter.v2_prefix)

    def test_v2_prefix_with_e_issn(self):
        xml_adapter = self._get_xml_adapter(eissn="1518-8345")
        self.assertEqual("S1518-83452021", xml_adapter.v2_prefix)

    def test_v2_prefix_with_e_issn_both_issns_given(self):
        xml_adapter = self._get_xml_adapter(pissn="0104-1169", eissn="1518-8345")
        self.assertEqual("S1518-83452021", xml_adapter.v2_prefix)


class PidProviderXMLAdapterLinksTest(TestCase):
    def setUp(self):
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink">
                <front>
                    <related-article xlink:href="10.1590/xxxx"/>
                    <related-article xlink:href="10.1590/bbbb"/>
                </front>
            </article>
        """
        self.xml_adapter = _get_xml_adapter(xml)

    def test_links(self):
        self.assertEqual(
            "6b72bd4b527ccb19f6ccf9152c4e81abde3682d2d18e3cc15be939d16698f753",
            self.xml_adapter.z_links,
        )


class PidProviderXMLAdapterCollabTest(TestCase):
    def setUp(self):
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink">
                <front>
                    <article-meta>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <collab>XXXX Institute</collab>
                            </contrib>
                          </contrib-group>
                    </article-meta>
                </front>
            </article>
        """
        self.xml_adapter = _get_xml_adapter(xml)

    def test_collab(self):
        self.assertEqual(
            "1a6702665c1f2788424bf3859403b5faab1c5639497b231d5a04f24263dc1619",
            self.xml_adapter.z_collab,
        )


class PidProviderXMLAdapterContribGroupTest(TestCase):
    def setUp(self):
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink">
                <front>
                    <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                          <contrib-id contrib-id-type="orcid">0000-0002-6374-2189</contrib-id>
                          <name>
                            <surname>Torquato</surname>
                            <given-names>Maria Teresa da Costa Gonçalves</given-names>
                          </name>
                          <xref ref-type="aff" rid="aff1">1</xref>
                        </contrib>
                        <contrib contrib-type="author">
                          <contrib-id contrib-id-type="orcid">0000-0001-9915-447X</contrib-id>
                          <name>
                            <surname>Santis</surname>
                            <given-names>Gil Cunha De</given-names>
                          </name>
                          <xref ref-type="aff" rid="aff2">2</xref>
                        </contrib>
                        <contrib contrib-type="author">
                          <contrib-id contrib-id-type="orcid">0000-0003-1656-6626</contrib-id>
                          <name>
                            <surname>Zanetti</surname>
                            <given-names>Maria Lucia</given-names>
                          </name>
                          <xref ref-type="corresp" rid="c1"/>
                          <xref ref-type="aff" rid="aff3">3</xref>
                          <xref ref-type="aff" rid="aff4">4</xref>
                        </contrib>
                      </contrib-group>
                    </article-meta>
                </front>
            </article>
        """
        self.xml_adapter = _get_xml_adapter(xml)

    def test_surnames(self):
        self.assertEqual(
            _str_with_64_char("Torquato|Santis|Zanetti"), self.xml_adapter.z_surnames
        )


class PidProviderXMLAdapterArticleTitlesTest(TestCase):
    def _get_xml_adapter(
        self, main_title=None, trans_titles=None, sub_article_titles=None
    ):
        main_title = main_title or ""
        trans_titles = trans_titles or ""
        sub_article_titles = sub_article_titles or ""
        if main_title:
            main_title = """<article-title>Article title in English</article-title>"""
        if trans_titles:
            trans_titles = """<trans-title-group xml:lang="pt"><trans-title>Título em português</trans-title></trans-title-group>"""
        if sub_article_titles:
            sub_article_titles = """<sub-article article-type="translation" id="s2" xml:lang="es">
                    <front-stub>
                      <title-group>
                        <article-title>título en español</article-title>
                      </title-group>
                    </front-stub>
                </sub-article>"""

        xml = f"""
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="en">
                <front>
                    <article-meta>
                    <title-group>
                        {main_title}{trans_titles}
                    </title-group>
                    </article-meta>
                </front>
                {sub_article_titles}
            </article>
        """
        return _get_xml_adapter(xml)

    def test_one_title(self):
        xml_adapter = self._get_xml_adapter(main_title=True)
        self.assertEqual(
            _str_with_64_char("Article title in English"),
            xml_adapter.z_article_titles_texts,
        )

    def test_article_titles_texts_en_pt(self):
        xml_adapter = self._get_xml_adapter(main_title=True, trans_titles=True)
        self.assertEqual(
            _str_with_64_char("Article title in English|Título em português"),
            xml_adapter.z_article_titles_texts,
        )

    def test_article_titles_texts_en_pt_es(self):
        xml_adapter = self._get_xml_adapter(
            main_title=True, trans_titles=True, sub_article_titles=True
        )
        self.assertEqual(
            _str_with_64_char(
                "Article title in English|Título em português|título en español"
            ),
            xml_adapter.z_article_titles_texts,
        )

    def test_article_titles_texts_en_es(self):
        xml_adapter = self._get_xml_adapter(main_title=True, sub_article_titles=True)
        self.assertEqual(
            _str_with_64_char("Article title in English|título en español"),
            xml_adapter.z_article_titles_texts,
        )


class PidProviderXMLAdapterTest(TestCase):
    def _get_xml_adapter(self, eissn=None, pissn=None):
        if eissn:
            eissn = f'<issn pub-type="epub">{eissn}</issn>'
        if pissn:
            pissn = f'<issn pub-type="ppub">{pissn}</issn>'
        xml = f"""
            <article>
                <front>
                    <journal-meta>
                      {eissn}{pissn}
                    </journal-meta>
                    <article-meta>
                    <title-group>
                        <article-title>Article title in English</article-title>
                    </title-group>
                    <contrib-group>
                        <contrib contrib-type="author">
                          <contrib-id contrib-id-type="orcid">0000-0002-6374-2189</contrib-id>
                          <name>
                            <surname>Torquato</surname>
                            <given-names>Maria Teresa da Costa Gonçalves</given-names>
                          </name>
                          <xref ref-type="aff" rid="aff1">1</xref>
                        </contrib>
                        <contrib contrib-type="author">
                          <contrib-id contrib-id-type="orcid">0000-0001-9915-447X</contrib-id>
                          <name>
                            <surname>Santis</surname>
                            <given-names>Gil Cunha De</given-names>
                          </name>
                          <xref ref-type="aff" rid="aff2">2</xref>
                        </contrib>
                        <contrib contrib-type="author">
                          <contrib-id contrib-id-type="orcid">0000-0003-1656-6626</contrib-id>
                          <name>
                            <surname>Zanetti</surname>
                            <given-names>Maria Lucia</given-names>
                          </name>
                          <xref ref-type="corresp" rid="c1"/>
                          <xref ref-type="aff" rid="aff3">3</xref>
                          <xref ref-type="aff" rid="aff4">4</xref>
                        </contrib>

                            <contrib contrib-type="author">
                                <collab>XXXX Institute</collab>
                            </contrib>
                      </contrib-group>
                      <pub-date publication-format="electronic" date-type="pub">
                        <day>29</day>
                        <month>10</month>
                        <year>2020</year>
                      </pub-date>
                      <pub-date date-type="collection" publication-format="electronic">
                        <year>2021</year>
                      </pub-date>
                      <volume>29</volume>
                    <related-article xlink:href="10.1590/xxxx"/>
                    <related-article xlink:href="10.1590/bbbb"/>
                    </article-meta>
                </front>

                <sub-article article-type="translation" id="s2" xml:lang="es">
                    <front-stub>
                      <title-group>
                        <article-title>título en español</article-title>
                      </title-group>
                    </front-stub>
                </sub-article>
            </article>
        """
        return _get_xml_adapter(xml)
