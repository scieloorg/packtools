# coding: utf-8
import unittest
from lxml import etree
from packtools.sps.utils.prepare_request_data import prepare_request_data


class PrepareTest(unittest.TestCase):
    def setUp(self):
        xml = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" 
                     xmlns:xlink="http://www.w3.org/1999/xlink" 
                     article-type="rapid-communication" 
                     dtd-version="1.1" 
                     specific-use="sps-1.8" 
                     xml:lang="en">
                <front>
                    <journal-meta>
                        <journal-id journal-id-type="nlm-ta">Braz J Med Biol Res</journal-id>
                        <journal-id journal-id-type="publisher-id">bjmbr</journal-id>
                        <journal-title-group>
                            <journal-title>Brazilian Journal of Medical and Biological Research</journal-title>
                            <abbrev-journal-title abbrev-type="publisher">Braz. J. Med. Biol. Res.</abbrev-journal-title>
                        </journal-title-group>
                        <issn pub-type="epub">1414-431X</issn>
                        <publisher>
                            <publisher-name>Associação Brasileira de Divulgação Científica</publisher-name>
                        </publisher>
                    </journal-meta>
                    <article-meta>
                        <article-id specific-use="scielo-v3" pub-id-type="publisher-id">ywDM7t6mxHzCRWp7kGF9rXQ</article-id>
                        <article-id specific-use="scielo-v2" pub-id-type="publisher-id">S0100-879X2021001000551</article-id>
                        <article-id pub-id-type="other">00551</article-id>
                        <article-id pub-id-type="doi">10.1590/1414-431X2021e11439</article-id>
                        <article-categories>
                            <subj-group subj-group-type="heading">
                                <subject>Short Communication</subject>
                            </subj-group>
                        </article-categories>
                        <title-group>
                            <article-title>Decreased levels of cathepsin Z mRNA expressed by immune blood cells: diagnostic and prognostic implications in prostate cancer</article-title>
                        </title-group>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <contrib-id contrib-id-type="orcid">0000-0001-8528-2091</contrib-id>
                                <contrib-id contrib-id-type="scopus">24771926600</contrib-id>
                                <collab>The MARS Group</collab>
                                <name>
                                    <surname>Einstein</surname>
                                    <given-names>Albert</given-names>
                                    <prefix>Prof</prefix>
                                    <suffix>Nieto</suffix>
                                </name>
                                <xref ref-type="aff" rid="aff1">1</xref>
                            </contrib>
                            <aff id="aff1">
                                <label>1</label>
                                <institution content-type="orgname">Fundação Oswaldo Cruz</institution>
                                <institution content-type="orgdiv1">Escola Nacional de Saúde Pública Sérgio Arouca</institution>
                                <institution content-type="orgdiv2">Centro de Estudos da Saúde do Trabalhador e Ecologia Humana</institution>
                                <addr-line>
                                    <named-content content-type="city">Manguinhos</named-content>
                                    <named-content content-type="state">RJ</named-content>
                                </addr-line>
                                <country country="BR">Brasil</country>
                                <email>denise.peres@email.com</email>
                                <institution content-type="original">Fundação Oswaldo Cruz; da Escola Nacional de Saúde Pública Sérgio Arouca, do Centro de Estudos da Saúde do Trabalhador e Ecologia Humana. RJ - Manguinhos, Brasil. denise.peres@email.com</institution>
                            </aff>
                        </contrib-group>
                        <pub-date pub-type="epub">
                            <year>2021</year>
                            <month>10</month>
                            <day>15</day>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
            """
        self.xmltree = etree.fromstring(xml)

    def test_orcid_extraction(self):
        """Testa se o ORCID ID é extraído corretamente"""
        expected = "0000-0001-8528-2091"
        obtained = list(prepare_request_data(self.xmltree))
        self.assertEqual(len(obtained), 1)
        self.assertIn("orcid_id", obtained[0])
        self.assertEqual(expected, obtained[0]["orcid_id"])

    def test_author_name_extraction(self):
        """Testa se o nome completo do autor é extraído corretamente"""
        expected = "Prof Albert Einstein Nieto"
        obtained = list(prepare_request_data(self.xmltree))
        self.assertEqual(len(obtained), 1)
        self.assertIn("author_name", obtained[0])
        self.assertEqual(expected, obtained[0]["author_name"])

    def test_author_email_extraction(self):
        """Testa se o email é extraído das afiliações"""
        expected = "denise.peres@email.com"
        obtained = list(prepare_request_data(self.xmltree))
        self.assertEqual(len(obtained), 1)
        self.assertIn("author_email", obtained[0])
        self.assertEqual(expected, obtained[0]["author_email"])

    def test_work_data_structure(self):
        """Testa se work_data tem a estrutura correta"""
        obtained = list(prepare_request_data(self.xmltree))
        self.assertEqual(len(obtained), 1)

        work_data = obtained[0]["work_data"]

        # Testa estrutura básica
        self.assertIn("title", work_data)
        self.assertIn("journal-title", work_data)
        self.assertIn("type", work_data)

        # Testa título
        self.assertIn("title", work_data["title"])
        self.assertEqual(work_data["title"]["title"]["value"],
                         "Decreased levels of cathepsin Z mRNA expressed by immune blood cells: diagnostic and prognostic implications in prostate cancer")

        # Testa journal
        self.assertEqual(work_data["journal-title"]["value"], "Brazilian Journal of Medical and Biological Research")

        # Testa tipo
        self.assertEqual(work_data["type"], "rapid-communication")

    def test_work_data_external_ids(self):
        """Testa se external-ids (DOI) são extraídos corretamente"""
        obtained = list(prepare_request_data(self.xmltree))
        work_data = obtained[0]

        self.assertIn("external-id", work_data)
        external_ids = work_data["external-id"]
        self.assertEqual(len(external_ids), 1)

        doi_entry = external_ids[0]
        self.assertEqual(doi_entry["external-id-type"], "doi")
        self.assertEqual(doi_entry["external-id-value"], "10.1590/1414-431X2021e11439")
        self.assertEqual(doi_entry["external-id-url"]["value"], "https://doi.org/10.1590/1414-431X2021e11439")

    def test_work_data_publication_date(self):
        """Testa se a data de publicação é extraída corretamente"""
        obtained = list(prepare_request_data(self.xmltree))

        self.assertIn("year", obtained[0])
        self.assertEqual(obtained[0]["year"]["value"], "2021")

        self.assertIn("month", obtained[0])
        self.assertEqual(obtained[0]["month"]["value"], "10")

        self.assertIn("day", obtained[0])
        self.assertEqual(obtained[0]["day"]["value"], "15")

    def test_complete_payload_structure(self):
        """Testa se o payload completo tem todos os campos obrigatórios"""
        obtained = list(prepare_request_data(self.xmltree))
        self.assertEqual(len(obtained), 1)

        payload = obtained[0]
        required_fields = ["orcid_id", "author_email", "author_name", "work_data"]

        for field in required_fields:
            self.assertIn(field, payload, f"Campo obrigatório '{field}' ausente no payload")

    def test_missing_orcid_and_name(self):
        """Testa se contribuidor sem ORCID E nome é rejeitado"""
        xml_no_orcid_and_name = """
            <article>
                <front>
                    <journal-meta>
                        <journal-title-group>
                            <journal-title>Test Journal</journal-title>
                        </journal-title-group>
                    </journal-meta>
                    <article-meta>
                        <article-id pub-id-type="doi">10.1000/test.123</article-id>
                        <title-group>
                            <article-title>Test Article</article-title>
                        </title-group>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <xref ref-type="aff" rid="aff1">1</xref>
                            </contrib>
                            <aff id="aff1">
                                <email>test@email.com</email>
                            </aff>
                        </contrib-group>
                        <pub-date pub-type="epub">
                            <year>2024</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
            """
        xmltree = etree.fromstring(xml_no_orcid_and_name)
        obtained = list(prepare_request_data(xmltree))
        self.assertEqual(len(obtained), 0)

    def test_missing_orcid_only(self):
        """Testa se contribuidor sem ORCID (mas com nome) é rejeitado"""
        xml_no_orcid = """
            <article>
                <front>
                    <journal-meta>
                        <journal-title-group>
                            <journal-title>Test Journal</journal-title>
                        </journal-title-group>
                    </journal-meta>
                    <article-meta>
                        <article-id pub-id-type="doi">10.1000/test.123</article-id>
                        <title-group>
                            <article-title>Test Article</article-title>
                        </title-group>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <name>
                                    <surname>Test</surname>
                                    <given-names>User</given-names>
                                </name>
                                <xref ref-type="aff" rid="aff1">1</xref>
                            </contrib>
                            <aff id="aff1">
                                <email>test@email.com</email>
                            </aff>
                        </contrib-group>
                        <pub-date pub-type="epub">
                            <year>2024</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
            """
        xmltree = etree.fromstring(xml_no_orcid)
        obtained = list(prepare_request_data(xmltree))
        self.assertEqual(len(obtained), 0)

    def test_missing_name_only(self):
        """Testa se contribuidor sem nome (mas com ORCID) é rejeitado"""
        xml_no_name = """
            <article>
                <front>
                    <journal-meta>
                        <journal-title-group>
                            <journal-title>Test Journal</journal-title>
                        </journal-title-group>
                    </journal-meta>
                    <article-meta>
                        <article-id pub-id-type="doi">10.1000/test.123</article-id>
                        <title-group>
                            <article-title>Test Article</article-title>
                        </title-group>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <contrib-id contrib-id-type="orcid">0000-0001-8528-2091</contrib-id>
                                <xref ref-type="aff" rid="aff1">1</xref>
                            </contrib>
                            <aff id="aff1">
                                <email>test@email.com</email>
                            </aff>
                        </contrib-group>
                        <pub-date pub-type="epub">
                            <year>2024</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
            """
        xmltree = etree.fromstring(xml_no_name)
        obtained = list(prepare_request_data(xmltree))
        self.assertEqual(len(obtained), 0)

    def test_missing_required_work_fields(self):
        """Testa se trabalhos com campos obrigatórios ausentes são rejeitados"""

        # XML sem DOI
        xml_no_doi = """
            <article>
                <front>
                    <journal-meta>
                        <journal-title-group>
                            <journal-title>Test Journal</journal-title>
                        </journal-title-group>
                    </journal-meta>
                    <article-meta>
                        <title-group>
                            <article-title>Test Article</article-title>
                        </title-group>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <contrib-id contrib-id-type="orcid">0000-0001-8528-2091</contrib-id>
                                <name>
                                    <surname>Test</surname>
                                    <given-names>User</given-names>
                                </name>
                                <xref ref-type="aff" rid="aff1">1</xref>
                            </contrib>
                            <aff id="aff1">
                                <email>test@email.com</email>
                            </aff>
                        </contrib-group>
                        <pub-date pub-type="epub">
                            <year>2024</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
            """
        xmltree = etree.fromstring(xml_no_doi)
        obtained = list(prepare_request_data(xmltree))
        self.assertEqual(len(obtained), 0)

        # XML sem título do artigo
        xml_no_title = """
            <article>
                <front>
                    <journal-meta>
                        <journal-title-group>
                            <journal-title>Test Journal</journal-title>
                        </journal-title-group>
                    </journal-meta>
                    <article-meta>
                        <article-id pub-id-type="doi">10.1000/test.123</article-id>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <contrib-id contrib-id-type="orcid">0000-0001-8528-2091</contrib-id>
                                <name>
                                    <surname>Test</surname>
                                    <given-names>User</given-names>
                                </name>
                                <xref ref-type="aff" rid="aff1">1</xref>
                            </contrib>
                            <aff id="aff1">
                                <email>test@email.com</email>
                            </aff>
                        </contrib-group>
                        <pub-date pub-type="epub">
                            <year>2024</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
            """
        xmltree = etree.fromstring(xml_no_title)
        obtained = list(prepare_request_data(xmltree))
        self.assertEqual(len(obtained), 0)

        # XML sem journal title
        xml_no_journal = """
            <article>
                <front>
                    <article-meta>
                        <article-id pub-id-type="doi">10.1000/test.123</article-id>
                        <title-group>
                            <article-title>Test Article</article-title>
                        </title-group>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <contrib-id contrib-id-type="orcid">0000-0001-8528-2091</contrib-id>
                                <name>
                                    <surname>Test</surname>
                                    <given-names>User</given-names>
                                </name>
                                <xref ref-type="aff" rid="aff1">1</xref>
                            </contrib>
                            <aff id="aff1">
                                <email>test@email.com</email>
                            </aff>
                        </contrib-group>
                        <pub-date pub-type="epub">
                            <year>2024</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
            """
        xmltree = etree.fromstring(xml_no_journal)
        obtained = list(prepare_request_data(xmltree))
        self.assertEqual(len(obtained), 0)

        # XML sem article-type
        xml_no_type = """
            <article>
                <front>
                    <journal-meta>
                        <journal-title-group>
                            <journal-title>Test Journal</journal-title>
                        </journal-title-group>
                    </journal-meta>
                    <article-meta>
                        <article-id pub-id-type="doi">10.1000/test.123</article-id>
                        <title-group>
                            <article-title>Test Article</article-title>
                        </title-group>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <contrib-id contrib-id-type="orcid">0000-0001-8528-2091</contrib-id>
                                <name>
                                    <surname>Test</surname>
                                    <given-names>User</given-names>
                                </name>
                                <xref ref-type="aff" rid="aff1">1</xref>
                            </contrib>
                            <aff id="aff1">
                                <email>test@email.com</email>
                            </aff>
                        </contrib-group>
                        <pub-date pub-type="epub">
                            <year>2024</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
            """
        xmltree = etree.fromstring(xml_no_type)
        obtained = list(prepare_request_data(xmltree))
        self.assertEqual(len(obtained), 0)

        # XML sem ano de publicação
        xml_no_year = """
            <article>
                <front>
                    <journal-meta>
                        <journal-title-group>
                            <journal-title>Test Journal</journal-title>
                        </journal-title-group>
                    </journal-meta>
                    <article-meta>
                        <article-id pub-id-type="doi">10.1000/test.123</article-id>
                        <title-group>
                            <article-title>Test Article</article-title>
                        </title-group>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <contrib-id contrib-id-type="orcid">0000-0001-8528-2091</contrib-id>
                                <name>
                                    <surname>Test</surname>
                                    <given-names>User</given-names>
                                </name>
                                <xref ref-type="aff" rid="aff1">1</xref>
                            </contrib>
                            <aff id="aff1">
                                <email>test@email.com</email>
                            </aff>
                        </contrib-group>
                    </article-meta>
                </front>
            </article>
            """
        xmltree = etree.fromstring(xml_no_year)
        obtained = list(prepare_request_data(xmltree))
        self.assertEqual(len(obtained), 0)

    def test_multiple_contributors(self):
        """Testa processamento de múltiplos contribuidores"""
        xml_multiple = """
            <article article-type="research-article">
                <front>
                    <journal-meta>
                        <journal-title-group>
                            <journal-title>Test Journal</journal-title>
                        </journal-title-group>
                    </journal-meta>
                    <article-meta>
                        <article-id pub-id-type="doi">10.1000/test.multiple.123</article-id>
                        <title-group>
                            <article-title>Test Article</article-title>
                        </title-group>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <contrib-id contrib-id-type="orcid">0000-0001-8528-2091</contrib-id>
                                <name>
                                    <surname>First</surname>
                                    <given-names>Author</given-names>
                                </name>
                                <xref ref-type="aff" rid="aff1">1</xref>
                            </contrib>
                            <contrib contrib-type="author">
                                <contrib-id contrib-id-type="orcid">0000-0002-1825-0097</contrib-id>
                                <name>
                                    <surname>Second</surname>
                                    <given-names>Author</given-names>
                                </name>
                                <xref ref-type="aff" rid="aff2">2</xref>
                            </contrib>
                            <aff id="aff1">
                                <email>first@email.com</email>
                            </aff>
                            <aff id="aff2">
                                <email>second@email.com</email>
                            </aff>
                        </contrib-group>
                        <pub-date pub-type="epub">
                            <year>2024</year>
                            <month>03</month>
                            <day>15</day>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
            """
        xmltree = etree.fromstring(xml_multiple)
        obtained = list(prepare_request_data(xmltree))

        self.assertEqual(len(obtained), 2)

        # Verifica primeiro autor
        first_author = obtained[0]
        self.assertEqual(first_author["orcid_id"], "0000-0001-8528-2091")
        self.assertEqual(first_author["author_name"], "Author First")
        self.assertEqual(first_author["author_email"], "first@email.com")

        # Verifica segundo autor
        second_author = obtained[1]
        self.assertEqual(second_author["orcid_id"], "0000-0002-1825-0097")
        self.assertEqual(second_author["author_name"], "Author Second")
        self.assertEqual(second_author["author_email"], "second@email.com")

    def test_work_data_shared_between_authors(self):
        """Testa se work_data é compartilhado corretamente entre múltiplos autores"""
        xml_multiple = """
            <article article-type="research-article">
                <front>
                    <journal-meta>
                        <journal-title-group>
                            <journal-title>Shared Journal</journal-title>
                        </journal-title-group>
                    </journal-meta>
                    <article-meta>
                        <article-id pub-id-type="doi">10.1000/shared.123</article-id>
                        <title-group>
                            <article-title>Shared Article</article-title>
                        </title-group>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <contrib-id contrib-id-type="orcid">0000-0001-1111-1111</contrib-id>
                                <name>
                                    <surname>Author</surname>
                                    <given-names>First</given-names>
                                </name>
                                <xref ref-type="aff" rid="aff1">1</xref>
                            </contrib>
                            <contrib contrib-type="author">
                                <contrib-id contrib-id-type="orcid">0000-0002-2222-2222</contrib-id>
                                <name>
                                    <surname>Author</surname>
                                    <given-names>Second</given-names>
                                </name>
                                <xref ref-type="aff" rid="aff2">2</xref>
                            </contrib>
                            <aff id="aff1">
                                <email>first@email.com</email>
                            </aff>
                            <aff id="aff2">
                                <email>second@email.com</email>
                            </aff>
                        </contrib-group>
                        <pub-date pub-type="epub">
                            <year>2024</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
            """
        xmltree = etree.fromstring(xml_multiple)
        obtained = list(prepare_request_data(xmltree))

        self.assertEqual(len(obtained), 2)

        # Verifica se work_data é idêntico entre os autores
        work_data_1 = obtained[0]["work_data"]
        work_data_2 = obtained[1]["work_data"]

        self.assertEqual(work_data_1, work_data_2)
        self.assertEqual(work_data_1["title"]["title"]["value"], "Shared Article")
        self.assertEqual(work_data_1["journal-title"]["value"], "Shared Journal")

    def test_email_optional_field(self):
        """Testa que email pode ser None quando não encontrado"""
        xml_no_email = """
            <article article-type="research-article">
                <front>
                    <journal-meta>
                        <journal-title-group>
                            <journal-title>Test Journal</journal-title>
                        </journal-title-group>
                    </journal-meta>
                    <article-meta>
                        <article-id pub-id-type="doi">10.1000/test.123</article-id>
                        <title-group>
                            <article-title>Test Article</article-title>
                        </title-group>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <contrib-id contrib-id-type="orcid">0000-0001-8528-2091</contrib-id>
                                <name>
                                    <surname>Test</surname>
                                    <given-names>User</given-names>
                                </name>
                                <xref ref-type="aff" rid="aff1">1</xref>
                            </contrib>
                            <aff id="aff1">
                                <label>1</label>
                            </aff>
                        </contrib-group>
                        <pub-date pub-type="epub">
                            <year>2024</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
            """
        xmltree = etree.fromstring(xml_no_email)
        obtained = list(prepare_request_data(xmltree))

        self.assertEqual(len(obtained), 1)
        self.assertIn("author_email", obtained[0])
        self.assertIsNone(obtained[0]["author_email"])

    def test_date_formatting(self):
        """Testa formatação correta de datas (zfill para month/day)"""
        xml_single_digit = """
            <article article-type="research-article">
                <front>
                    <journal-meta>
                        <journal-title-group>
                            <journal-title>Test Journal</journal-title>
                        </journal-title-group>
                    </journal-meta>
                    <article-meta>
                        <article-id pub-id-type="doi">10.1000/test.123</article-id>
                        <title-group>
                            <article-title>Test Article</article-title>
                        </title-group>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <contrib-id contrib-id-type="orcid">0000-0001-8528-2091</contrib-id>
                                <name>
                                    <surname>Test</surname>
                                    <given-names>User</given-names>
                                </name>
                                <xref ref-type="aff" rid="aff1">1</xref>
                            </contrib>
                            <aff id="aff1">
                                <email>test@email.com</email>
                            </aff>
                        </contrib-group>
                        <pub-date pub-type="epub">
                            <year>2024</year>
                            <month>3</month>
                            <day>5</day>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
            """
        xmltree = etree.fromstring(xml_single_digit)
        obtained = list(prepare_request_data(xmltree))

        self.assertEqual(len(obtained), 1)
        self.assertEqual(obtained[0]["year"]["value"], "2024")
        self.assertEqual(obtained[0]["month"]["value"], "03")
        self.assertEqual(obtained[0]["day"]["value"], "05")