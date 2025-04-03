from unittest import TestCase
from lxml import etree

from packtools.sps.models.references import XMLReferences
from packtools.sps.validation.references import ReferenceValidation, ReferencesValidation


class ReferenceValidationTest(TestCase):
    """Testes unitários simplificados para ReferenceValidation focando nas quatro chaves principais."""

    def setUp(self):
        self.params = {
            "allowed_tags": [],
            "year_error_level": "ERROR",
            "source_error_level": "ERROR",
            "article_title_error_level": "ERROR",
            "authors_error_level": "ERROR",
            "publication_type_error_level": "CRITICAL",
            "comment_error_level": "ERROR",
            "mixed_citation_error_level": "CRITICAL",
            "mixed_citation_sub_tags_error_level": "ERROR",
            "title_tag_by_dtd_version_error_level": "CRITICAL",
            "publication_type_requires": {
                "journal": ["source", "year", "article-title", "person-group"],
                "book": ["source", "year", "person-group"],
                "other": ["source", "year"]
            }
        }
        
        # Mock reference data para testes
        self.reference_data = {
            "ref_id": "B1",
            "publication_type": "journal",
            "mixed_citation": "Artigo de teste",
            "mixed_citation_sub_tags": ["ext-link"],
            "source": "Fonte Teste",
            "year": "2015",
            "article_title": "Título do artigo",
            "all_authors": [{"surname": "Silva", "given-names": "J"}],
            "comment_text": {"ext_link_text": "https://...", "full_comment": None, "has_comment": True},
            "parent_article_type": "research-article",
            "parent_lang": "pt",
            "citing_pub_year": "2014",
            "filtered_not_marked": [],
            "not_marked": [],
            "marked": [],
            "unmatched": [],
        }

    # Testes para validate_year
    def test_validate_year_fail_future_year(self):
        reference_data = self.reference_data.copy()
        reference_data["year"] = "2015"  # ano posterior
        
        validation = ReferenceValidation(reference_data, self.params)
        results = list(validation.validate_year())
        
        self.assertEqual(1, len(results))
        result = results[0]
        
        self.assertEqual("ERROR", result["response"])
        self.assertEqual("2015", result["got_value"])
        self.assertTrue("2014" in result["expected_value"])
        self.assertTrue("reference year" in result["advice"])

    def test_validate_year_fail_invalid_year(self):
        reference_data = self.reference_data.copy()
        reference_data["year"] = "201a"  # ano inválido
        
        validation = ReferenceValidation(reference_data, self.params)
        results = list(validation.validate_year())
        
        self.assertEqual(1, len(results))
        result = results[0]
        
        self.assertEqual("ERROR", result["response"])
        self.assertEqual("201a", result["got_value"])
        self.assertTrue("reference year" in result["expected_value"])
        self.assertTrue("reference year" in result["advice"])

    # Testes para validate_source
    def test_validate_source_fail_missing(self):
        reference_data = self.reference_data.copy()
        reference_data.pop("source")  # remove a fonte
        
        validation = ReferenceValidation(reference_data, self.params)
        results = list(validation.validate_source())
        
        self.assertEqual(1, len(results))
        result = results[0]
        
        self.assertEqual("ERROR", result["response"])
        self.assertEqual(None, result["got_value"])
        self.assertEqual("reference source", result["expected_value"])
        self.assertTrue("reference source" in result["advice"])

    # Testes para validate_article_title
    def test_validate_article_title_fail_missing(self):
        reference_data = self.reference_data.copy()
        reference_data.pop("article_title")  # remove o título
        
        validation = ReferenceValidation(reference_data, self.params)
        results = list(validation.validate_article_title())
        
        self.assertEqual(1, len(results))
        result = results[0]
        
        self.assertEqual("ERROR", result["response"])
        self.assertEqual(None, result["got_value"])
        self.assertEqual("reference article-title", result["expected_value"])
        self.assertTrue("reference article-title" in result["advice"])

    # Testes para validate_authors
    def test_validate_authors_fail_missing(self):
        reference_data = self.reference_data.copy()
        reference_data.pop("all_authors")  # remove os autores
        
        validation = ReferenceValidation(reference_data, self.params)
        results = list(validation.validate_authors())
        
        self.assertEqual(1, len(results))
        result = results[0]
        
        self.assertEqual("ERROR", result["response"])
        self.assertEqual(None, result["got_value"])
        self.assertTrue("person-group" in result["expected_value"])
        self.assertTrue("<name>" in result["advice"])

    # Testes para validate_publication_type
    def test_validate_publication_type_fail_invalid(self):
        # Configure apenas livro como tipo válido
        params = self.params.copy()
        params["publication_type_requires"] = {"book": ["source", "year"]}
        
        reference_data = self.reference_data.copy()
        reference_data["publication_type"] = "journal"  # tipo não permitido
        
        validation = ReferenceValidation(reference_data, params)
        results = list(validation.validate_publication_type())
        
        self.assertEqual(1, len(results))
        result = results[0]
        
        self.assertEqual("CRITICAL", result["response"])
        self.assertEqual("journal", result["got_value"])
        self.assertEqual(["book"], result["expected_value"])
        self.assertTrue("publication-type" in result["advice"])

    # Testes para validate_comment_is_required_or_not
    def test_validate_comment_empty_with_text(self):
        reference_data = self.reference_data.copy()
        reference_data.update({
            "ext_link_text": "https://...",
            "ext_link_uri": "https://...",
            "full_comment": None,
            "text_between": None,
            "text_before_extlink": "text",
            "has_comment": True,
        })
        reference_data["text_before_extlink"] = "text"
        
        validation = ReferenceValidation(reference_data, self.params)
        results = list(validation.validate_comment_is_required_or_not())
        
        self.assertEqual(1, len(results))
        result = results[0]
        
        self.assertEqual("ERROR", result["response"])
        self.assertTrue('<comment></comment>text<ext-link xlink:href="https://...">' in result["got_value"])
        self.assertTrue('<comment>text<ext-link xlink:href="https://...">' in result["expected_value"])
        self.assertTrue("Wrap" in result["advice"])

    def test_validate_comment_empty_no_text(self):
        reference_data = self.reference_data.copy()
        reference_data.update({
            "ext_link_text": "https://...",
            "ext_link_uri": "https://...",
            "full_comment": None,
            "text_between": None,
            "text_before_extlink": None,
            "has_comment": True,
        })
        
        validation = ReferenceValidation(reference_data, self.params)
        results = list(validation.validate_comment_is_required_or_not())
        
        self.assertEqual(1, len(results))
        result = results[0]
        
        self.assertEqual("ERROR", result["response"])
        self.assertTrue('<comment></comment><ext-link xlink:href="https://...">' in result["got_value"])
        self.assertTrue('<ext-link xlink:href="https://...">' in result["expected_value"])
        self.assertTrue("Remove" in result["advice"])

    # Testes para validate_mixed_citation_sub_tags
    def test_validate_mixed_citation_sub_tags_disallowed(self):
        params = self.params.copy()
        params["allowed_tags"] = ["italic", "bold"]  # ext-link não permitido
        
        reference_data = self.reference_data.copy()
        reference_data["mixed_citation_sub_tags"] = ["ext-link", "u"]  # não permitidas
        
        validation = ReferenceValidation(reference_data, params)
        results = list(validation.validate_mixed_citation_sub_tags())
        
        self.assertEqual(1, len(results))
        result = results[0]
        
        self.assertEqual("ERROR", result["response"])
        self.assertEqual(["ext-link", "u"], result["got_value"])
        self.assertEqual(["italic", "bold"], result["expected_value"])
        self.assertTrue("remove" in result["advice"])

    # Testes para validate_mixed_citation
    def test_validate_mixed_citation_fail_missing(self):
        reference_data = self.reference_data.copy()
        reference_data.pop("mixed_citation")  # remove mixed-citation
        
        validation = ReferenceValidation(reference_data, self.params)
        results = list(validation.validate_mixed_citation())
        
        self.assertEqual(1, len(results))
        result = results[0]
        
        self.assertEqual("CRITICAL", result["response"])
        self.assertEqual(None, result["got_value"])
        self.assertEqual("mixed-citation", result["expected_value"])
        self.assertTrue("<mixed-citation>" in result["advice"])

    # Testes para validate_title_tag_by_dtd_version
    def test_validate_title_tag_for_dtd_1_3(self):
        params = self.params.copy()
        params["dtd_version"] = "1.3"
        
        reference_data = self.reference_data.copy()
        reference_data["chapter_title"] = "Título do capítulo"
        reference_data["publication_type"] = "book"
        
        validation = ReferenceValidation(reference_data, params)
        results = list(validation.validate_title_tag_by_dtd_version())
        
        self.assertEqual(1, len(results))
        result = results[0]
        
        self.assertEqual("CRITICAL", result["response"])
        self.assertEqual("<chapter-title>", result["got_value"])
        self.assertEqual("<part-title>", result["expected_value"])
        self.assertTrue("replace <chapter-title>" in result["advice"])

from unittest import TestCase
from lxml import etree

from packtools.sps.models.references import XMLReferences
from packtools.sps.validation.references import ReferenceValidation, ReferencesValidation


class ReferenceValidationTest(TestCase):
    """Testes unitários para ReferenceValidation com verificações completas."""

    def setUp(self):
        self.params = {
            "allowed_tags": [],
            "year_error_level": "ERROR",
            "source_error_level": "ERROR",
            "article_title_error_level": "ERROR",
            "authors_error_level": "ERROR",
            "publication_type_error_level": "CRITICAL",
            "comment_error_level": "ERROR",
            "mixed_citation_error_level": "CRITICAL",
            "mixed_citation_sub_tags_error_level": "ERROR",
            "title_tag_by_dtd_version_error_level": "CRITICAL",
            "publication_type_requires": {
                "journal": ["source", "year", "article-title", "person-group"],
                "book": ["source", "year", "person-group"],
                "other": ["source", "year"]
            }
        }
        
        # Mock reference data para testes
        self.reference_data = {
            "ref_id": "B1",
            "publication_type": "journal",
            "mixed_citation": "Artigo de teste",
            "mixed_citation_sub_tags": ["ext-link"],
            "source": "Fonte Teste",
            "year": "2015",
            "article_title": "Título do artigo",
            "all_authors": [{"surname": "Silva", "given-names": "J"}],
            "ext_link_uri": "https://...", 
            "ext_link_text": "https://...", "full_comment": None, "has_comment": True,
            "parent": "article",
            "parent_article_type": "research-article",
            "parent_id": None,
            "parent_lang": "pt",
            "citing_pub_year": "2014",
            "filtered_not_marked": [],
            "not_marked": [],
            "marked": [],
            "unmatched": [],
        }

    # Testes para validate_year
    def test_validate_year_fail_future_year(self):
        reference_data = self.reference_data.copy()
        reference_data["year"] = "2015"  # ano posterior
        
        validation = ReferenceValidation(reference_data, self.params)
        results = list(validation.validate_year())
        
        self.assertEqual(1, len(results))
        result = results[0]
        
        self.assertEqual("ERROR", result["response"])
        self.assertEqual("2015", result["got_value"])
        self.assertEqual("reference year (2015) previous or equal to 2014", result["expected_value"])
        self.assertEqual("B1 (journal) : Mark the reference year (2015) with <year> and it must be previous or equal to 2014", result["advice"])

    def test_validate_year_fail_invalid_year(self):
        reference_data = self.reference_data.copy()
        reference_data["year"] = "201a"  # ano inválido
        
        validation = ReferenceValidation(reference_data, self.params)
        results = list(validation.validate_year())
        
        self.assertEqual(1, len(results))
        result = results[0]
        
        self.assertEqual("ERROR", result["response"])
        self.assertEqual("201a", result["got_value"])
        self.assertEqual("reference year (201a) previous or equal to 2014", result["expected_value"])
        self.assertEqual("B1 (journal) : Mark the reference year (201a) with <year> and it must be previous or equal to 2014", result["advice"])

    # Testes para validate_source
    def test_validate_source_fail_missing(self):
        reference_data = self.reference_data.copy()
        reference_data.pop("source")  # remove a fonte
        
        validation = ReferenceValidation(reference_data, self.params)
        results = list(validation.validate_source())
        
        self.assertEqual(1, len(results))
        result = results[0]
        
        self.assertEqual("ERROR", result["response"])
        self.assertEqual(None, result["got_value"])
        self.assertEqual("reference source", result["expected_value"])
        self.assertEqual("B1 (journal) : Mark reference source with <source>", result["advice"])

    # Testes para validate_article_title
    def test_validate_article_title_fail_missing(self):
        reference_data = self.reference_data.copy()
        reference_data.pop("article_title")  # remove o título
        
        validation = ReferenceValidation(reference_data, self.params)
        results = list(validation.validate_article_title())
        
        self.assertEqual(1, len(results))
        result = results[0]
        
        self.assertEqual("ERROR", result["response"])
        self.assertEqual(None, result["got_value"])
        self.assertEqual("reference article-title", result["expected_value"])
        self.assertEqual("B1 (journal) : Mark article title with <article-title>", result["advice"])

    # Testes para validate_authors
    def test_validate_authors_fail_missing(self):
        reference_data = self.reference_data.copy()
        reference_data.pop("all_authors")  # remove os autores
        
        validation = ReferenceValidation(reference_data, self.params)
        results = list(validation.validate_authors())
        
        self.assertEqual(1, len(results))
        result = results[0]
        
        self.assertEqual("ERROR", result["response"])
        self.assertEqual(None, result["got_value"])
        self.assertEqual("reference person-group//name or person-group//collab", result["expected_value"])
        self.assertEqual("B1 (journal) : Mark reference authors with <name> (person) or <collab> (institutional)", result["advice"])

    # Testes para validate_publication_type
    def test_validate_publication_type_fail_invalid(self):
        # Configure apenas livro como tipo válido
        params = self.params.copy()
        params["publication_type_requires"] = {"book": ["source", "year"]}
        
        reference_data = self.reference_data.copy()
        reference_data["publication_type"] = "journal"  # tipo não permitido
        
        validation = ReferenceValidation(reference_data, params)
        results = list(validation.validate_publication_type())
        
        self.assertEqual(1, len(results))
        result = results[0]
        
        self.assertEqual("CRITICAL", result["response"])
        self.assertEqual("journal", result["got_value"])
        self.assertEqual(["book"], result["expected_value"])
        self.assertEqual("B1 (journal) : Complete publication-type=\"\" in <element-citation publication-type=\"\"> with valid value: ['book']", result["advice"])

    # Testes para validate_comment_is_required_or_not
    def test_validate_comment_empty_with_text(self):
        reference_data = self.reference_data.copy()
        reference_data.update({
            "ext_link_text": "https://...",
            "ext_link_uri": "https://...",
            "full_comment": None,
            "text_between": None,
            "text_before_extlink": "text",
            "has_comment": True,
        })
        reference_data["text_before_extlink"] = "text"
        
        validation = ReferenceValidation(reference_data, self.params)
        results = list(validation.validate_comment_is_required_or_not())
        
        self.assertEqual(1, len(results))
        result = results[0]
        
        self.assertEqual("ERROR", result["response"])
        self.assertEqual('<comment></comment>text<ext-link xlink:href="https://...">https://...</ext-link>', result["got_value"])
        self.assertEqual('<comment>text<ext-link xlink:href="https://...">https://...</ext-link></comment>', result["expected_value"])
        self.assertEqual('B1 (journal) : Wrap text<ext-link xlink:href="https://...">https://...</ext-link> with <comment> tag', result["advice"])

    def test_validate_comment_empty_no_text(self):
        reference_data = self.reference_data.copy()
        reference_data.update({
            "ext_link_text": "https://...",
            "ext_link_uri": "https://...",
            "full_comment": None,
            "text_between": None,
            "text_before_extlink": None,
            "has_comment": True,
        })
        
        validation = ReferenceValidation(reference_data, self.params)
        results = list(validation.validate_comment_is_required_or_not())
        
        self.assertEqual(1, len(results))
        result = results[0]
        
        self.assertEqual("ERROR", result["response"])
        self.assertEqual('<comment></comment><ext-link xlink:href="https://...">https://...</ext-link>', result["got_value"])
        self.assertEqual('<ext-link xlink:href="https://...">https://...</ext-link>', result["expected_value"])
        self.assertEqual('B1 (journal) : Analyze and decide to remove <comment> or mark the text between <comment> and <ext-link xlink:href="https://...">', result["advice"])

    # Testes para validate_mixed_citation_sub_tags
    def test_validate_mixed_citation_sub_tags_disallowed(self):
        params = self.params.copy()
        params["allowed_tags"] = ["italic", "bold"]  # ext-link não permitido
        
        reference_data = self.reference_data.copy()
        reference_data["mixed_citation_sub_tags"] = ["ext-link", "u"]  # não permitidas
        
        validation = ReferenceValidation(reference_data, params)
        results = list(validation.validate_mixed_citation_sub_tags())
        
        self.assertEqual(1, len(results))
        result = results[0]
        
        self.assertEqual("ERROR", result["response"])
        self.assertEqual(["ext-link", "u"], result["got_value"])
        self.assertEqual(["italic", "bold"], result["expected_value"])
        self.assertEqual("remove ['ext-link', 'u'] from mixed-citation", result["advice"])

    # Testes para validate_mixed_citation
    def test_validate_mixed_citation_fail_missing(self):
        reference_data = self.reference_data.copy()
        reference_data.pop("mixed_citation")  # remove mixed-citation
        
        validation = ReferenceValidation(reference_data, self.params)
        results = list(validation.validate_mixed_citation())
        
        self.assertEqual(1, len(results))
        result = results[0]
        
        self.assertEqual("CRITICAL", result["response"])
        self.assertEqual(None, result["got_value"])
        self.assertEqual("mixed-citation", result["expected_value"])
        self.assertEqual("B1 (journal): mark the full reference with <mixed-citation>", result["advice"])

    # Testes para validate_title_tag_by_dtd_version
    def test_validate_title_tag_for_dtd_1_3(self):
        params = self.params.copy()
        params["dtd_version"] = "1.3"
        
        reference_data = self.reference_data.copy()
        reference_data["chapter_title"] = "Título do capítulo"
        reference_data["publication_type"] = "book"
        
        validation = ReferenceValidation(reference_data, params)
        results = list(validation.validate_title_tag_by_dtd_version())
        
        self.assertEqual(1, len(results))
        result = results[0]
        
        self.assertEqual("CRITICAL", result["response"])
        self.assertEqual("<chapter-title>", result["got_value"])
        self.assertEqual("<part-title>", result["expected_value"])
        self.assertEqual("B1 (book) : replace <chapter-title> by <part-title>", result["advice"])


class ReferencesValidationTest(TestCase):
    """Testes para ReferencesValidation usando XML real."""

    def setUp(self):
        self.params = {
            "allowed_tags": [],
            "year_error_level": "ERROR",
            "source_error_level": "ERROR",
            "article_title_error_level": "ERROR",
            "authors_error_level": "ERROR",
            "publication_type_error_level": "CRITICAL",
            "comment_error_level": "ERROR",
            "mixed_citation_error_level": "CRITICAL",
            "mixed_citation_sub_tags_error_level": "ERROR",
            "title_tag_by_dtd_version_error_level": "CRITICAL",
            "publication_type_requires": {
                "journal": ["source", "year", "article-title", "person-group"],
                "book": ["source", "year", "person-group"],
                "other": ["source", "year"]
            }
        }
        
        # XML de referência completa para testes
        self.xml_complete = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
                <pub-date publication-format="electronic" date-type="pub">
                <day>20</day>
                <month>04</month>
                <year>2014</year>
                </pub-date>
            </article-meta>
            </front>
            <back>
            <ref-list>
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
                <comment>DOI: <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
                </comment>
                </element-citation>
                </ref>
            </ref-list>
            </back>
            </article>
        """
        
        # XML com referência sem fonte
        self.xml_missing_source = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
                <pub-date publication-format="electronic" date-type="pub">
                <year>2014</year>
                </pub-date>
            </article-meta>
            </front>
            <back>
            <ref-list>
                <ref id="B2">
                <label>2.</label>
                <mixed-citation>Referência sem fonte</mixed-citation>
                <element-citation publication-type="journal">
                <person-group person-group-type="author">
                <name>
                <surname>Silva</surname>
                <given-names>J</given-names>
                </name>
                </person-group>
                <article-title>Título do artigo sem fonte</article-title>
                <year>2014</year>
                </element-citation>
                </ref>
            </ref-list>
            </back>
            </article>
        """
        
        # XML com publicação tipo inválido
        self.xml_invalid_publication_type = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
                <pub-date publication-format="electronic" date-type="pub">
                <year>2014</year>
                </pub-date>
            </article-meta>
            </front>
            <back>
            <ref-list>
                <ref id="B3">
                <label>3.</label>
                <mixed-citation>Referência com tipo inválido</mixed-citation>
                <element-citation publication-type="invalid-type">
                <person-group person-group-type="author">
                <name>
                <surname>Silva</surname>
                <given-names>J</given-names>
                </name>
                </person-group>
                <article-title>Título do artigo</article-title>
                <source>Fonte do artigo</source>
                <year>2014</year>
                </element-citation>
                </ref>
            </ref-list>
            </back>
            </article>
        """
        
        # XML com chapter-title usando DTD 1.3
        self.xml_chapter_title_dtd_1_3 = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="research-article" dtd-version="1.3" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
                <pub-date publication-format="electronic" date-type="pub">
                <year>2014</year>
                </pub-date>
            </article-meta>
            </front>
            <back>
            <ref-list>
                <ref id="B4">
                <label>4.</label>
                <mixed-citation>Referência com chapter-title em DTD 1.3</mixed-citation>
                <element-citation publication-type="book">
                <person-group person-group-type="author">
                <name>
                <surname>Silva</surname>
                <given-names>J</given-names>
                </name>
                </person-group>
                <chapter-title>Título do capítulo</chapter-title>
                <source>Título do livro</source>
                <year>2014</year>
                </element-citation>
                </ref>
            </ref-list>
            </back>
            </article>
        """

    def test_references_validation_year_future(self):
        """Testa validação com XML para ano futuro."""
        xmltree = etree.fromstring(self.xml_complete)
        
        # O XML tem uma referência de 2015, mas o artigo é de 2014
        validation = ReferencesValidation(xmltree, self.params)
        results = list(validation.validate())
        
        # Deve encontrar um erro de ano futuro
        year_results = [r for r in results if r["title"] == "reference year"]
        self.assertTrue(len(year_results) > 0)
        
        result = year_results[0]
        self.assertEqual("ERROR", result["response"])
        self.assertEqual("2015", result["got_value"])
        self.assertEqual("reference year (2015) previous or equal to 2014", result["expected_value"])
        # O advice vai conter informações da referência completa
        self.assertEqual("B1 (journal) : Mark the reference year (2015) with <year> and it must be previous or equal to 2014", result["advice"])

    def test_references_validation_missing_source(self):
        """Testa validação com XML para fonte ausente."""
        xmltree = etree.fromstring(self.xml_missing_source)
        
        validation = ReferencesValidation(xmltree, self.params)
        results = list(validation.validate())
        
        # Deve encontrar um erro de fonte ausente
        source_results = [r for r in results if r["title"] == "reference source"]
        self.assertTrue(len(source_results) > 0)
        
        result = source_results[0]
        self.assertEqual("ERROR", result["response"])
        self.assertEqual(None, result["got_value"])
        self.assertEqual("reference source", result["expected_value"])
        self.assertTrue("Mark reference source with <source>" in result["advice"])

    def test_references_validation_invalid_publication_type(self):
        """Testa validação com XML para tipo de publicação inválido."""
        # Configure apenas tipos específicos como válidos
        params = self.params.copy()
        params["publication_type_requires"] = {
            "journal": ["source", "year"],
            "book": ["source", "year"]
        }
        
        xmltree = etree.fromstring(self.xml_invalid_publication_type)
        
        validation = ReferencesValidation(xmltree, params)
        results = list(validation.validate())
        
        # Deve encontrar um erro de tipo de publicação inválido
        self.assertEqual(5, len(results))

        self.assertEqual(['OK', 'OK', 'CRITICAL', 'OK', None], [item['response'] for item in results])
        
        result = results[2]
        self.assertEqual("CRITICAL", result["response"])
        self.assertEqual("invalid-type", result["got_value"])
        self.assertEqual(["journal", "book"], result["expected_value"])
        self.assertTrue("Complete publication-type=\"\"" in result["advice"])

    def test_references_validation_chapter_title_dtd_1_3(self):
        """Testa validação com XML para chapter-title em DTD 1.3."""
        params = self.params.copy()
        params["dtd_version"] = "1.3"
        
        xmltree = etree.fromstring(self.xml_chapter_title_dtd_1_3)
        
        validation = ReferencesValidation(xmltree, params)
        results = list(validation.validate())
        
        # Deve encontrar um erro de chapter-title em DTD 1.3
        title_results = [r for r in results if r["title"] == "part-title"]
        self.assertTrue(len(title_results) > 0)
        
        result = title_results[0]
        self.assertEqual("CRITICAL", result["response"])
        self.assertEqual("<chapter-title>", result["got_value"])
        self.assertEqual("<part-title>", result["expected_value"])
        self.assertTrue("replace <chapter-title> by <part-title>" in result["advice"])