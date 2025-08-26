from packtools.sps.models.references import XMLReferences
from unittest import TestCase
from lxml import etree

from packtools.sps.utils import xml_utils


class XMLReferencesTest(TestCase):
    """Testes unitários para a classe XMLReferences com testes individuais para cada chave."""

    def setUp(self):
        # XML comum para muitos dos testes
        self.many_authors_xml = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <back>
            <ref-list>
            <title>REFERENCES</title>
            <ref id="B1">
            <label>1.</label>
            <mixed-citation>
            1. Tran B, Falster MO, Douglas K, Blyth F, Jorm LR. Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in older ages. Drug Alcohol Depend. 2015;150:85-91. DOI: <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
            </mixed-citation>
            <element-citation publication-type="journal">
            <person-group person-group-type="author">
            <name>
            <surname>Tran</surname>
            <given-names>B</given-names>
            <prefix>The Honorable</prefix>
            <suffix>III</suffix>
            </name>
            <name>
            <surname>Falster</surname>
            <given-names>MO</given-names>
            </name>
            <name>
            <surname>Douglas</surname>
            <given-names>K</given-names>
            </name>
            <name>
            <surname>Blyth</surname>
            <given-names>F</given-names>
            </name>
            <name>
            <surname>Jorm</surname>
            <given-names>LR</given-names>
            </name>
            </person-group>
            <article-title>Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in older ages</article-title>
            <source>Drug Alcohol Depend.</source>
            <year>2015</year>
            <volume>150</volume>
            <fpage>85</fpage>
            <lpage>91</lpage>
            <pub-id pub-id-type="doi">10.1016/B1</pub-id>
            <elocation-id>elocation_B1</elocation-id>
            <pub-id pub-id-type="pmid">00000000</pub-id>
            <pub-id pub-id-type="pmcid">11111111</pub-id>
            <comment>DOI:<ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link></comment>
            </element-citation>
            </ref>
            </ref-list>
            </back>
            </article>
            """
        
        self.one_author_xml = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <back>
            <ref-list>
            <title>REFERENCES</title>
            <ref id="B2">
                <mixed-citation>BARTHES, Roland. <italic>Aula</italic>. São Pulo: Cultrix, 1987.</mixed-citation>
                <element-citation publication-type="book">
                  <person-group person-group-type="author">
                    <name>
                      <surname>BARTHES</surname>
                      <given-names>Roland</given-names>
                    </name>
                  </person-group>
                  <source>Aula</source>
                  <publisher-loc>São Pulo</publisher-loc>
                  <publisher-name>Cultrix</publisher-name>
                  <year>1987</year>
                  <pub-id pub-id-type="doi">10.1016/B2</pub-id>
                  <elocation-id>elocation_B2</elocation-id>
                  <pub-id pub-id-type="pmid">22222222</pub-id>
                  <pub-id pub-id-type="pmcid">33333333</pub-id>
                </element-citation>
              </ref>
            </ref-list>
            </back>
            </article>
            """
        
        self.collab_xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" specific-use="sps-1.4" dtd-version="1.0" xml:lang="pt" article-type="research-article">
           <back>
              <ref-list>
                 <ref id="B3">
                    <mixed-citation>
                       3. Brasil. Lei n.
                       <u>
                          <sup>o</sup>
                       </u>
                       10.332, de 19/12/2001. Instituiu mecanismo de financiamento para o programa de ciência e tecnologia para o agronegócio, para o programa de fomento à pesquisa em saúde, para o programa de bioteconologia e recursos genéticos – Genoma, para o programa de ciência e tecnologia para o setor aeronáutico e para o programa de inovação para competitividade, e dá outras providências.
                       <italic>Diário Oficial da União</italic>
                       2001 dez 19.
                    </mixed-citation>
                    <element-citation publication-type="other">
                       <person-group person-group-type="authors">
                          <collab>Brasil</collab>
                       </person-group>
                       <article-title>Lei n.º 10.332, de 19/12/2001: Instituiu mecanismo de financiamento para o programa de ciência e tecnologia para o agronegócio, para o programa de fomento à pesquisa em saúde, para o programa de bioteconologia e recursos genéticos - Genoma, para o programa de ciência e tecnologia para o setor aeronáutico e para o programa de inovação para competitividade, e dá outras providências</article-title>
                       <source>Diário Oficial da União</source>
                       <date>
                          <year>2001</year>
                          <month>21</month>
                       </date>
                       <year>2001</year>
                    </element-citation>
                 </ref>
                </ref-list>
           </back>
        </article>
        """
        
        # Parse XMLs para uso nos testes
        self.many_authors_tree = etree.fromstring(self.many_authors_xml)
        self.one_author_tree = etree.fromstring(self.one_author_xml)
        self.collab_tree = etree.fromstring(self.collab_xml)
        
        # Obter referências para os testes
        self.many_authors_ref = list(XMLReferences(self.many_authors_tree).main_references)[0]
        self.one_author_ref = list(XMLReferences(self.one_author_tree).main_references)[0]
        self.collab_ref = list(XMLReferences(self.collab_tree).main_references)[0]

        # Documento para correção de problemas de obtenção de pub-id-type
        self.article1_tree = xml_utils.get_xml_tree(
            'tests/sps/fixtures/xml_test_fixtures/S1984-92302025000100304.xml'
        )
        self.article1_ref_b1 = list(XMLReferences(self.article1_tree).main_references)[0]
        self.article1_ref_b2 = list(XMLReferences(self.article1_tree).main_references)[1]

        # Documento para correção de problemas de obtenção de pub-id-type
        self.article2_tree = xml_utils.get_xml_tree(
            'tests/sps/fixtures/xml_test_fixtures/S2176-66652019000100074.xml'
        )
        self.article2_ref_b1 = list(XMLReferences(self.article2_tree).main_references)[0]

    # Testes para atributos básicos das referências
    def test_ref_id(self):
        self.assertEqual("B1", self.many_authors_ref.get("ref_id"))
        self.assertEqual("B2", self.one_author_ref.get("ref_id"))
        self.assertEqual("B3", self.collab_ref.get("ref_id"))

    def test_publication_type(self):
        self.assertEqual("journal", self.many_authors_ref.get("publication_type"))
        self.assertEqual("book", self.one_author_ref.get("publication_type"))
        self.assertEqual("other", self.collab_ref.get("publication_type"))

    def test_author_type(self):
        self.assertEqual("person", self.many_authors_ref.get("author_type"))
        self.assertEqual("person", self.one_author_ref.get("author_type"))
        self.assertEqual("institutional", self.collab_ref.get("author_type"))

    def test_ref_list_index(self):
        self.assertEqual(0, self.many_authors_ref.get("ref-list-index"))
        self.assertEqual(0, self.one_author_ref.get("ref-list-index"))
        self.assertEqual(0, self.collab_ref.get("ref-list-index"))

    # Testes para o conteúdo de mixed-citation
    def test_mixed_citation(self):
        self.assertTrue(self.many_authors_ref.get("mixed_citation").startswith("1. Tran B, Falster MO"))
        self.assertTrue(self.one_author_ref.get("mixed_citation").startswith("BARTHES, Roland"))
        self.assertTrue(self.collab_ref.get("mixed_citation").startswith("3. Brasil. Lei n."))

    def test_mixed_citation_sub_tags(self):
        self.assertEqual(['ext-link'], self.many_authors_ref.get("mixed_citation_sub_tags"))
        self.assertEqual(['italic'], self.one_author_ref.get("mixed_citation_sub_tags"))
        self.assertEqual(['u', 'italic'], self.collab_ref.get("mixed_citation_sub_tags"))

    # Testes para fonte e título
    def test_source(self):
        self.assertEqual("Drug Alcohol Depend.", self.many_authors_ref.get("source"))
        self.assertEqual("Aula", self.one_author_ref.get("source"))
        self.assertEqual("Diário Oficial da União", self.collab_ref.get("source"))

    def test_article_title(self):
        self.assertEqual(
            "Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in older ages", 
            self.many_authors_ref.get("article_title")
        )
        self.assertIsNone(self.one_author_ref.get("article_title"))
        self.assertTrue(
            self.collab_ref.get("article_title").startswith("Lei n.º 10.332")
        )

    # Testes para dados de autores
    def test_main_author(self):
        # Teste para autor principal em referência com múltiplos autores
        main_author = self.many_authors_ref.get("main_author")
        self.assertEqual("Tran", main_author.get("surname"))
        self.assertEqual("B", main_author.get("given-names"))
        self.assertEqual("The Honorable", main_author.get("prefix"))
        self.assertEqual("III", main_author.get("suffix"))

        # Teste para autor principal em referência com um autor
        main_author = self.one_author_ref.get("main_author")
        self.assertEqual("BARTHES", main_author.get("surname"))
        self.assertEqual("Roland", main_author.get("given-names"))

        # Teste para autor institucional
        main_author = self.collab_ref.get("main_author")
        self.assertEqual(["Brasil"], main_author.get("collab"))

    def test_all_authors(self):
        # Teste para todos os autores em referência com múltiplos autores
        all_authors = self.many_authors_ref.get("all_authors")
        self.assertEqual(5, len(all_authors))
        self.assertEqual("Tran", all_authors[0].get("surname"))
        self.assertEqual("Falster", all_authors[1].get("surname"))
        self.assertEqual("Douglas", all_authors[2].get("surname"))
        self.assertEqual("Blyth", all_authors[3].get("surname"))
        self.assertEqual("Jorm", all_authors[4].get("surname"))

        # Teste para todos os autores em referência com um autor
        all_authors = self.one_author_ref.get("all_authors")
        self.assertEqual(1, len(all_authors))
        self.assertEqual("BARTHES", all_authors[0].get("surname"))

        # Teste para autor institucional
        all_authors = self.collab_ref.get("all_authors")
        self.assertEqual(1, len(all_authors))
        self.assertEqual(["Brasil"], all_authors[0].get("collab"))

    # Testes para dados bibliográficos
    def test_volume(self):
        self.assertEqual("150", self.many_authors_ref.get("volume"))
        self.assertIsNone(self.one_author_ref.get("volume"))
        self.assertIsNone(self.collab_ref.get("volume"))

    def test_pages(self):
        self.assertEqual("85", self.many_authors_ref.get("fpage"))
        self.assertEqual("91", self.many_authors_ref.get("lpage"))
        self.assertIsNone(self.one_author_ref.get("fpage"))
        self.assertIsNone(self.one_author_ref.get("lpage"))

    def test_year(self):
        self.assertEqual("2015", self.many_authors_ref.get("year"))
        self.assertEqual("1987", self.one_author_ref.get("year"))
        self.assertEqual("2001", self.collab_ref.get("year"))

    def test_elocation_id(self):
        self.assertEqual("elocation_B1", self.many_authors_ref.get("elocation_id"))
        self.assertEqual("elocation_B2", self.one_author_ref.get("elocation_id"))
        self.assertIsNone(self.collab_ref.get("elocation_id"))

    # Testes para identificadores de citação
    def test_citation_ids(self):
        citation_ids = self.many_authors_ref.get("citation_ids")
        self.assertEqual("00000000", citation_ids.get("pmid"))
        self.assertEqual("11111111", citation_ids.get("pmcid"))
        self.assertEqual("10.1016/B1", citation_ids.get("doi"))

        citation_ids = self.one_author_ref.get("citation_ids")
        self.assertEqual("22222222", citation_ids.get("pmid"))
        self.assertEqual("33333333", citation_ids.get("pmcid"))
        self.assertEqual("10.1016/B2", citation_ids.get("doi"))

    def test_citation_ids_with_valid_doi(self):
        """Ref B1: <pub-id pub-id-type="doi">10.1590/1982-02672016v24n0105</pub-id>"""
        citation_ids = self.article1_ref_b1.get("citation_ids")

        expected = {"doi": "10.1590/1982-02672016v24n0105"}
        self.assertEqual(citation_ids, expected)

    def test_citation_ids_without_type_attribute(self):
        """Ref B2: <pub-id>10.3390/su13010408</pub-id> - sem pub-id-type"""
        citation_ids = self.article1_ref_b2.get("citation_ids")

        self.assertEqual(citation_ids, {})

    def test_citation_ids_absent_pub_id(self):
        """Referência sem elementos pub-id"""
        citation_ids = self.article2_ref_b1.get("citation_ids")

        self.assertEqual(citation_ids, {})

    # Testes para dados de comentário e links externos
    def test_comment_text(self):
        comment_text = self.many_authors_ref
        self.assertEqual("https://doi.org/10.1016/j.drugalcdep.2015.02.028", comment_text.get("ext_link_text"))
        self.assertEqual("DOI:https://doi.org/10.1016/j.drugalcdep.2015.02.028", comment_text.get("full_comment"))
        self.assertEqual("DOI:", comment_text.get("text_between"))
        self.assertTrue(comment_text.get("has_comment"))

    # Testes para chapter_title e part_title
    def test_chapter_title(self):
        xml = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <back>
            <ref-list>
            <title>REFERENCES</title>
            <ref id="B1">
            <element-citation publication-type="book">
            <chapter-title>Tópicos especiais em piscicultura de água doce tropical intensiva</chapter-title>
            </element-citation>
            </ref>
            </ref-list>
            </back>
            </article>
            """
        xml_tree = etree.fromstring(xml)
        ref = list(XMLReferences(xml_tree).main_references)[0]
        self.assertEqual(
            "Tópicos especiais em piscicultura de água doce tropical intensiva", 
            ref.get("chapter_title")
        )

    def test_part_title(self):
        xml = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <back>
            <ref-list>
            <title>REFERENCES</title>
            <ref id="B1">
            <element-citation publication-type="book">
            <part-title>Tópicos especiais em piscicultura de água doce tropical intensiva</part-title>
            </element-citation>
            </ref>
            </ref-list>
            </back>
            </article>
            """
        xml_tree = etree.fromstring(xml)
        ref = list(XMLReferences(xml_tree).main_references)[0]
        self.assertEqual(
            "Tópicos especiais em piscicultura de água doce tropical intensiva", 
            ref.get("part_title")
        )

    # Testes para atributos do artigo pai
    def test_parent_attributes(self):
        self.assertEqual("article", self.many_authors_ref.get("parent"))
        self.assertIsNone(self.many_authors_ref.get("parent_id"))
        self.assertEqual("research-article", self.many_authors_ref.get("parent_article_type"))
        self.assertEqual("en", self.many_authors_ref.get("parent_lang"))
        
        self.assertEqual("article", self.collab_ref.get("parent"))
        self.assertIsNone(self.collab_ref.get("parent_id"))
        self.assertEqual("research-article", self.collab_ref.get("parent_article_type"))
        self.assertEqual("pt", self.collab_ref.get("parent_lang"))

    def test_comment_before_extlink_with_text_between(self):
        """Testa extlink com comment vazio antes e texto entre eles."""
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" specific-use="sps-1.4" dtd-version="1.0" xml:lang="pt" article-type="research-article">
                <back>
                    <ref-list>
                        <ref id="B1">
                            <element-citation publication-type="other">
                                <comment></comment>text<ext-link>https://... </ext-link>
                            </element-citation>
                        </ref>
                    </ref-list>
                </back>
            </article>
        """
        
        xml_tree = etree.fromstring(xml)
        ref = list(XMLReferences(xml_tree).main_references)[0]
        
        # Verificar valores específicos
        self.assertEqual('https://... ', ref["ext_link_text"])
        self.assertEqual(None, ref["full_comment"])
        self.assertEqual('text', ref["text_before_extlink"])
        self.assertEqual(None, ref["text_between"])
        self.assertEqual(True, ref["has_comment"])

    def test_extlink_inside_comment(self):
        """Testa extlink dentro do comment com texto entre eles."""
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" specific-use="sps-1.4" dtd-version="1.0" xml:lang="pt" article-type="research-article">
                <back>
                    <ref-list>
                        <ref id="B2">
                            <element-citation publication-type="other">
                                <comment>text<ext-link>https://... </ext-link></comment>
                            </element-citation>
                        </ref>
                    </ref-list>
                </back>
            </article>
        """
        
        xml_tree = etree.fromstring(xml)
        ref = list(XMLReferences(xml_tree).main_references)[0]
        
        
        # Verificar valores específicos
        self.assertEqual('https://... ', ref["ext_link_text"])
        self.assertEqual('texthttps://... ', ref["full_comment"])
        self.assertEqual(None, ref["text_before_extlink"])
        self.assertEqual('text', ref["text_between"])
        self.assertEqual(True, ref["has_comment"])

    def test_extlink_without_text_between(self):
        """Testa extlink sem texto entre o comment vazio e ele."""
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" specific-use="sps-1.4" dtd-version="1.0" xml:lang="pt" article-type="research-article">
                <back>
                    <ref-list>
                        <ref id="B3">
                            <element-citation publication-type="other">
                                <comment></comment><ext-link>https://... </ext-link>
                            </element-citation>
                        </ref>
                    </ref-list>
                </back>
            </article>
        """
        
        xml_tree = etree.fromstring(xml)
        ref = list(XMLReferences(xml_tree).main_references)[0]
        
        
        # Verificar valores específicos
        self.assertEqual('https://... ', ref["ext_link_text"])
        self.assertEqual(None, ref["full_comment"])
        self.assertEqual(None, ref["text_before_extlink"])
        self.assertEqual(None, ref["text_between"])
        self.assertEqual(True, ref["has_comment"])

    def test_extlink_without_comment(self):
        """Testa extlink sem comment."""
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" specific-use="sps-1.4" dtd-version="1.0" xml:lang="pt" article-type="research-article">
                <back>
                    <ref-list>
                        <ref id="B4">
                            <element-citation publication-type="other">
                                <ext-link>https://... </ext-link>
                            </element-citation>
                        </ref>
                    </ref-list>
                </back>
            </article>
        """
        
        xml_tree = etree.fromstring(xml)
        ref = list(XMLReferences(xml_tree).main_references)[0]
        
        
        # Verificar valores específicos
        self.assertEqual('https://... ', ref["ext_link_text"])
        self.assertEqual(None, ref["full_comment"])
        self.assertEqual(None, ref["text_before_extlink"])
        self.assertEqual(None, ref["text_between"])
        self.assertEqual(False, ref["has_comment"])

    def test_extlink_with_empty_comment_containing_only_extlink(self):
        """Testa extlink dentro de comment sem texto adicional."""
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" specific-use="sps-1.4" dtd-version="1.0" xml:lang="pt" article-type="research-article">
                <back>
                    <ref-list>
                        <ref id="B5">
                            <element-citation publication-type="other">
                                <comment><ext-link>https://... </ext-link></comment>
                            </element-citation>
                        </ref>
                    </ref-list>
                </back>
            </article>
        """
        
        xml_tree = etree.fromstring(xml)
        ref = list(XMLReferences(xml_tree).main_references)[0]
        
        
        # Verificar valores específicos
        self.assertEqual('https://... ', ref["ext_link_text"])
        self.assertEqual('https://... ', ref["full_comment"])
        self.assertEqual(None, ref["text_before_extlink"])
        self.assertEqual(None, ref["text_between"])
        self.assertEqual(True, ref["has_comment"])

    def test_extlink_with_text_before_but_no_comment(self):
        """Testa extlink com texto antes mas sem comment."""
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" specific-use="sps-1.4" dtd-version="1.0" xml:lang="pt" article-type="research-article">
                <back>
                    <ref-list>
                        <ref id="B6">
                            <element-citation publication-type="other">
                                DOI: <ext-link>https://... </ext-link>
                            </element-citation>
                        </ref>
                    </ref-list>
                </back>
            </article>
        """
        
        xml_tree = etree.fromstring(xml)
        ref = list(XMLReferences(xml_tree).main_references)[0]
        
        
        # Verificar valores específicos
        self.assertEqual('https://... ', ref["ext_link_text"])
        self.assertEqual(None, ref["full_comment"])
        self.assertIn('DOI: ', ref["text_before_extlink"])
        self.assertEqual(None, ref["text_between"])
        self.assertEqual(False, ref["has_comment"])    
    # Teste para subarticle_references

    def test_subarticle_references(self):
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article">
                <back>
                    <ref-list>
                        <ref id="B1">
                            <element-citation publication-type="journal">
                                <source>Main Source</source>
                            </element-citation>
                        </ref>
                    </ref-list>
                </back>
                <sub-article article-type="translation" id="T1" xml:lang="es">
                    <back>
                        <ref-list>
                            <ref id="B1-es">
                                <element-citation publication-type="journal">
                                    <source>Translation Source</source>
                                </element-citation>
                            </ref>
                        </ref-list>
                    </back>
                </sub-article>
                <sub-article article-type="abstract" id="A1">
                    <back>
                        <ref-list>
                            <ref id="B1-abstract">
                                <element-citation publication-type="journal">
                                    <source>Abstract Source</source>
                                </element-citation>
                            </ref>
                        </ref-list>
                    </back>
                </sub-article>
            </article>
        """
        xml_tree = etree.fromstring(xml)
        references = XMLReferences(xml_tree)
        
        # Testar referências principais
        main_refs = list(references.main_references)
        self.assertEqual(1, len(main_refs))
        self.assertEqual("Main Source", main_refs[0].get("source"))
        
        # Testar referências de subarticles
        subarticle_refs = references.subarticle_references
        # Subarticle de abstract deve estar incluído, mas não o de translation
        self.assertEqual(1, len(subarticle_refs))
        
        # Testar property items
        all_items = list(references.items)
        # Deve incluir referências do main article e do subarticle que não é translation
        self.assertEqual(2, len(all_items))
        
        # Verificar fontes de todas as referências
        sources = [ref.get("source") for ref in all_items]
        self.assertIn("Main Source", sources)
        self.assertIn("Abstract Source", sources)

    def test_get_citation_lang(self):
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article">
                <back>
                    <ref-list>
                        <ref id="B1">
                            <element-citation publication-type="journal" xml:lang="es">
                                <source>Main Source</source>
                            </element-citation>
                        </ref>
                    </ref-list>
                </back>
            </article>
        """
        xml_tree = etree.fromstring(xml)
        references = list(XMLReferences(xml_tree).main_references)
        lang = references[0].get("lang")
        self.assertEqual(lang, "es")
