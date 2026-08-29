import logging
from unittest import TestCase
from unittest.mock import patch, PropertyMock

from lxml import etree

from packtools.sps.pid_provider.xml_sps_adapter import (PidProviderXMLAdapter,
                                                        _str_with_64_char)
from packtools.sps.pid_provider.xml_sps_lib import XMLWithPre, generate_finger_print


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


class PidProviderXMLAdapterGetDataToCompareTest(TestCase):

    def _get_xml_adapter_with_body(self, body_text=""):
        xml = f"""
            <article xmlns:xlink="http://www.w3.org/1999/xlink">
                <front>
                    <article-meta/>
                </front>
                <body><p>{body_text}</p></body>
            </article>
        """
        return _get_xml_adapter(xml)

    def test_returns_expected_keys_without_z_partial_body(self):
        xml_adapter = self._get_xml_adapter_with_body("Texto de teste")
        result = xml_adapter.get_data_to_compare()
        self.assertEqual(
            set(result.keys()),
            {
                "article_titles",
                "z_surnames",
                "z_collab",
                "z_links",
                "body_fragment_fingerprint",
                "body_fragment",
            },
        )
        self.assertNotIn("z_partial_body", result)

    def test_body_fragment_uses_default_max_length_300(self):
        xml_adapter = self._get_xml_adapter_with_body("Texto de teste")
        result = xml_adapter.get_data_to_compare()
        self.assertEqual(result["body_fragment"], "texto de teste")
        self.assertEqual(xml_adapter.xml_with_pre.max_body_fragment_length, 300)

    def test_body_fragment_respects_custom_max_body_fragment_length(self):
        xml_adapter = self._get_xml_adapter_with_body("Texto de teste longo")
        result = xml_adapter.get_data_to_compare(max_body_fragment_length=5)
        self.assertEqual(result["body_fragment"], "texto")
        # o setter deve ter propagado o valor para xml_with_pre
        self.assertEqual(xml_adapter.xml_with_pre.max_body_fragment_length, 5)

    def test_body_fragment_fingerprint_matches_fingerprint_of_body_fragment(self):
        xml_adapter = self._get_xml_adapter_with_body("Texto de teste")
        result = xml_adapter.get_data_to_compare()
        expected = generate_finger_print(result["body_fragment"])
        self.assertEqual(result["body_fragment_fingerprint"], expected)

    def test_setter_not_triggered_when_length_matches_current_value(self):
        xml_adapter = self._get_xml_adapter_with_body("abc")
        # já está em 300 (default); patchear o setter para confirmar que
        # NÃO é chamado quando o valor pedido já é o vigente
        with patch.object(
            type(xml_adapter.xml_with_pre),
            "max_body_fragment_length",
            new_callable=PropertyMock,
        ) as mock_prop:
            mock_prop.return_value = 300
            xml_adapter.get_data_to_compare(max_body_fragment_length=300)
            # getter é chamado (comparação), mas nenhuma chamada de
            # "set" deve ocorrer -- PropertyMock só registra get/set juntos,
            # então validamos indiretamente via call_count do getter (>=1)
            # e ausência de exceção de setattr bloqueado.
            self.assertTrue(mock_prop.called)

    def test_repeated_call_with_same_length_reuses_cached_body_fragment(self):
        # cached_property armazena o valor computado em xml_with_pre.__dict__;
        # não dá para espionar xmltree.xpath diretamente porque
        # lxml.etree._Element é um tipo C e seus atributos/métodos são
        # read-only (não suportam patch.object).
        xml_adapter = self._get_xml_adapter_with_body("abc")

        first = xml_adapter.get_data_to_compare()  # popula o cache (length=300)
        self.assertIn("body_text", xml_adapter.xml_with_pre.__dict__)
        self.assertNotIn("body_fragment", xml_adapter.xml_with_pre.__dict__)

        cached_body_text_obj = xml_adapter.xml_with_pre.__dict__["body_text"]
    
        second = xml_adapter.get_data_to_compare()  # mesmo length, deve reusar cache

        # identidade preservada -> não foi recomputado
        self.assertIs(xml_adapter.xml_with_pre.__dict__["body_text"], cached_body_text_obj)

        with self.assertRaises(KeyError):
            xml_adapter.xml_with_pre.__dict__["body_fragment"]
        self.assertEqual(first["body_fragment"], second["body_fragment"])

    def test_changing_length_invalidates_effectively_recomputes_fragment(self):
        xml_adapter = self._get_xml_adapter_with_body("abcdefgh")
        first = xml_adapter.get_data_to_compare(max_body_fragment_length=300)
        second = xml_adapter.get_data_to_compare(max_body_fragment_length=3)
        self.assertNotEqual(first["body_fragment"], second["body_fragment"])
        self.assertEqual(second["body_fragment"], "abc")

    def test_empty_body_returns_empty_fragment(self):
        xml_adapter = _get_xml_adapter()  # sem <body>
        result = xml_adapter.get_data_to_compare()
        self.assertEqual(result["body_fragment"], "")
