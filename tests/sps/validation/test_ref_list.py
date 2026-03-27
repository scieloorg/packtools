from unittest import TestCase
from lxml import etree

from packtools.sps.validation.references import ReferenceValidation, ReferencesValidation


class RefListPresenceValidationTest(TestCase):
    """Tests for Rule 1: ref-list presence in indexable documents."""

    def setUp(self):
        self.params = {
            "publication_type_requires": {
                "journal": ["source", "year", "article-title", "person-group"],
                "book": ["source", "year", "person-group"],
            },
        }

    def test_ref_list_present(self):
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" xml:lang="en">
            <front>
            <article-meta>
                <pub-date publication-format="electronic" date-type="pub">
                <year>2024</year>
                </pub-date>
            </article-meta>
            </front>
            <back>
            <ref-list>
                <ref id="B1">
                <mixed-citation>Author A. Title. 2020.</mixed-citation>
                <element-citation publication-type="journal">
                <source>Journal</source>
                <year>2020</year>
                </element-citation>
                </ref>
            </ref-list>
            </back>
            </article>
        """
        xmltree = etree.fromstring(xml)
        validation = ReferencesValidation(xmltree, self.params)
        results = [r for r in validation.validate_ref_list_presence()]
        self.assertEqual(1, len(results))
        self.assertEqual("OK", results[0]["response"])

    def test_ref_list_absent_in_research_article(self):
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" xml:lang="en">
            <front>
            <article-meta>
                <pub-date publication-format="electronic" date-type="pub">
                <year>2024</year>
                </pub-date>
            </article-meta>
            </front>
            <back/>
            </article>
        """
        xmltree = etree.fromstring(xml)
        validation = ReferencesValidation(xmltree, self.params)
        results = [r for r in validation.validate_ref_list_presence()]
        self.assertEqual(1, len(results))
        self.assertEqual("CRITICAL", results[0]["response"])
        self.assertEqual("<ref-list> in <back>", results[0]["expected_value"])

    def test_ref_list_exempt_correction(self):
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="correction" xml:lang="en">
            <front><article-meta></article-meta></front>
            <back/>
            </article>
        """
        xmltree = etree.fromstring(xml)
        validation = ReferencesValidation(xmltree, self.params)
        results = list(validation.validate_ref_list_presence())
        self.assertEqual(0, len(results))

    def test_ref_list_exempt_retraction(self):
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="retraction" xml:lang="en">
            <front><article-meta></article-meta></front>
            <back/>
            </article>
        """
        xmltree = etree.fromstring(xml)
        validation = ReferencesValidation(xmltree, self.params)
        results = list(validation.validate_ref_list_presence())
        self.assertEqual(0, len(results))

    def test_ref_list_exempt_addendum(self):
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="addendum" xml:lang="en">
            <front><article-meta></article-meta></front>
            <back/>
            </article>
        """
        xmltree = etree.fromstring(xml)
        validation = ReferencesValidation(xmltree, self.params)
        results = list(validation.validate_ref_list_presence())
        self.assertEqual(0, len(results))

    def test_ref_list_exempt_expression_of_concern(self):
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="expression-of-concern" xml:lang="en">
            <front><article-meta></article-meta></front>
            <back/>
            </article>
        """
        xmltree = etree.fromstring(xml)
        validation = ReferencesValidation(xmltree, self.params)
        results = list(validation.validate_ref_list_presence())
        self.assertEqual(0, len(results))

    def test_ref_list_exempt_reviewer_report(self):
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="reviewer-report" xml:lang="en">
            <front><article-meta></article-meta></front>
            <back/>
            </article>
        """
        xmltree = etree.fromstring(xml)
        validation = ReferencesValidation(xmltree, self.params)
        results = list(validation.validate_ref_list_presence())
        self.assertEqual(0, len(results))


class RefPresenceValidationTest(TestCase):
    """Tests for Rule 2: ref presence in ref-list."""

    def setUp(self):
        self.params = {
            "publication_type_requires": {
                "journal": ["source", "year"],
            },
        }

    def test_ref_list_with_refs(self):
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" xml:lang="en">
            <front>
            <article-meta>
                <pub-date publication-format="electronic" date-type="pub">
                <year>2024</year>
                </pub-date>
            </article-meta>
            </front>
            <back>
            <ref-list>
                <ref id="B1">
                <mixed-citation>Ref 1</mixed-citation>
                <element-citation publication-type="journal">
                <source>Journal</source>
                <year>2020</year>
                </element-citation>
                </ref>
            </ref-list>
            </back>
            </article>
        """
        xmltree = etree.fromstring(xml)
        validation = ReferencesValidation(xmltree, self.params)
        results = list(validation.validate_ref_presence())
        self.assertEqual(1, len(results))
        self.assertEqual("OK", results[0]["response"])

    def test_ref_list_empty(self):
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" xml:lang="en">
            <front>
            <article-meta>
                <pub-date publication-format="electronic" date-type="pub">
                <year>2024</year>
                </pub-date>
            </article-meta>
            </front>
            <back>
            <ref-list>
                <title>References</title>
            </ref-list>
            </back>
            </article>
        """
        xmltree = etree.fromstring(xml)
        validation = ReferencesValidation(xmltree, self.params)
        results = list(validation.validate_ref_presence())
        self.assertEqual(1, len(results))
        self.assertEqual("CRITICAL", results[0]["response"])
        self.assertEqual("at least one <ref> in <ref-list>", results[0]["expected_value"])


class ElementCitationPresenceValidationTest(TestCase):
    """Tests for Rule 4: element-citation presence in each ref."""

    def setUp(self):
        self.params = {
            "publication_type_requires": {
                "journal": ["source", "year"],
            },
        }
        self.reference_data = {
            "ref_id": "B1",
            "publication_type": "journal",
            "mixed_citation": "Test ref",
            "mixed_citation_sub_tags": [],
            "source": "Source",
            "year": "2020",
            "all_authors": [{"surname": "Author", "given-names": "A"}],
            "parent": "article",
            "parent_article_type": "research-article",
            "parent_id": None,
            "parent_lang": "en",
            "citing_pub_year": "2024",
            "filtered_not_marked": [],
            "not_marked": [],
            "marked": [],
            "unmatched": [],
            "has_element_citation": True,
            "ext_link_count_element_citation": 0,
            "ext_link_count_mixed_citation": 0,
            "date_in_citation_content_type": None,
            "names_without_surname": [],
        }

    def test_element_citation_present(self):
        data = self.reference_data.copy()
        data["has_element_citation"] = True
        validation = ReferenceValidation(data, self.params)
        results = list(validation.validate_element_citation())
        self.assertEqual(1, len(results))
        self.assertEqual("OK", results[0]["response"])

    def test_element_citation_absent(self):
        data = self.reference_data.copy()
        data["has_element_citation"] = False
        validation = ReferenceValidation(data, self.params)
        results = list(validation.validate_element_citation())
        self.assertEqual(1, len(results))
        self.assertEqual("CRITICAL", results[0]["response"])
        self.assertEqual("element-citation", results[0]["expected_value"])
        self.assertIsNone(results[0]["got_value"])


class ExtLinkCountElementCitationValidationTest(TestCase):
    """Tests for Rule 7: no multiple ext-links in element-citation."""

    def setUp(self):
        self.params = {
            "publication_type_requires": {
                "journal": ["source", "year"],
            },
        }
        self.reference_data = {
            "ref_id": "B1",
            "publication_type": "journal",
            "mixed_citation": "Test ref",
            "mixed_citation_sub_tags": [],
            "source": "Source",
            "year": "2020",
            "all_authors": [],
            "parent": "article",
            "parent_article_type": "research-article",
            "parent_id": None,
            "parent_lang": "en",
            "citing_pub_year": "2024",
            "filtered_not_marked": [],
            "not_marked": [],
            "marked": [],
            "unmatched": [],
            "has_element_citation": True,
            "ext_link_count_element_citation": 0,
            "ext_link_count_mixed_citation": 0,
            "date_in_citation_content_type": None,
            "names_without_surname": [],
        }

    def test_no_ext_links(self):
        data = self.reference_data.copy()
        data["ext_link_count_element_citation"] = 0
        validation = ReferenceValidation(data, self.params)
        results = list(validation.validate_ext_link_count_element_citation())
        self.assertEqual(0, len(results))

    def test_one_ext_link(self):
        data = self.reference_data.copy()
        data["ext_link_count_element_citation"] = 1
        validation = ReferenceValidation(data, self.params)
        results = list(validation.validate_ext_link_count_element_citation())
        self.assertEqual(0, len(results))

    def test_multiple_ext_links(self):
        data = self.reference_data.copy()
        data["ext_link_count_element_citation"] = 3
        validation = ReferenceValidation(data, self.params)
        results = list(validation.validate_ext_link_count_element_citation())
        self.assertEqual(1, len(results))
        self.assertEqual("ERROR", results[0]["response"])
        self.assertEqual("at most 1 <ext-link> in <element-citation>", results[0]["expected_value"])
        self.assertEqual("3 <ext-link> elements", results[0]["got_value"])


class ExtLinkCountMixedCitationValidationTest(TestCase):
    """Tests for Rule 8: no multiple ext-links in mixed-citation."""

    def setUp(self):
        self.params = {
            "publication_type_requires": {
                "journal": ["source", "year"],
            },
        }
        self.reference_data = {
            "ref_id": "B1",
            "publication_type": "journal",
            "mixed_citation": "Test ref",
            "mixed_citation_sub_tags": [],
            "source": "Source",
            "year": "2020",
            "all_authors": [],
            "parent": "article",
            "parent_article_type": "research-article",
            "parent_id": None,
            "parent_lang": "en",
            "citing_pub_year": "2024",
            "filtered_not_marked": [],
            "not_marked": [],
            "marked": [],
            "unmatched": [],
            "has_element_citation": True,
            "ext_link_count_element_citation": 0,
            "ext_link_count_mixed_citation": 0,
            "date_in_citation_content_type": None,
            "names_without_surname": [],
        }

    def test_no_ext_links(self):
        data = self.reference_data.copy()
        data["ext_link_count_mixed_citation"] = 0
        validation = ReferenceValidation(data, self.params)
        results = list(validation.validate_ext_link_count_mixed_citation())
        self.assertEqual(0, len(results))

    def test_one_ext_link(self):
        data = self.reference_data.copy()
        data["ext_link_count_mixed_citation"] = 1
        validation = ReferenceValidation(data, self.params)
        results = list(validation.validate_ext_link_count_mixed_citation())
        self.assertEqual(0, len(results))

    def test_multiple_ext_links(self):
        data = self.reference_data.copy()
        data["ext_link_count_mixed_citation"] = 2
        validation = ReferenceValidation(data, self.params)
        results = list(validation.validate_ext_link_count_mixed_citation())
        self.assertEqual(1, len(results))
        self.assertEqual("ERROR", results[0]["response"])
        self.assertEqual("at most 1 <ext-link> in <mixed-citation>", results[0]["expected_value"])
        self.assertEqual("2 <ext-link> elements", results[0]["got_value"])


class LpageWhenFpageValidationTest(TestCase):
    """Tests for Rule 11: lpage required when fpage exists."""

    def setUp(self):
        self.params = {
            "publication_type_requires": {
                "journal": ["source", "year"],
            },
        }
        self.reference_data = {
            "ref_id": "B1",
            "publication_type": "journal",
            "mixed_citation": "Test ref",
            "mixed_citation_sub_tags": [],
            "source": "Source",
            "year": "2020",
            "all_authors": [],
            "parent": "article",
            "parent_article_type": "research-article",
            "parent_id": None,
            "parent_lang": "en",
            "citing_pub_year": "2024",
            "filtered_not_marked": [],
            "not_marked": [],
            "marked": [],
            "unmatched": [],
            "has_element_citation": True,
            "ext_link_count_element_citation": 0,
            "ext_link_count_mixed_citation": 0,
            "date_in_citation_content_type": None,
            "names_without_surname": [],
        }

    def test_fpage_and_lpage_present(self):
        data = self.reference_data.copy()
        data["fpage"] = "31"
        data["lpage"] = "68"
        validation = ReferenceValidation(data, self.params)
        results = list(validation.validate_lpage_when_fpage())
        self.assertEqual(0, len(results))

    def test_fpage_without_lpage(self):
        data = self.reference_data.copy()
        data["fpage"] = "31"
        validation = ReferenceValidation(data, self.params)
        results = list(validation.validate_lpage_when_fpage())
        self.assertEqual(1, len(results))
        self.assertEqual("ERROR", results[0]["response"])
        self.assertEqual("<lpage> when <fpage> is present", results[0]["expected_value"])
        self.assertIn("31", results[0]["got_value"])

    def test_no_fpage_no_lpage(self):
        data = self.reference_data.copy()
        validation = ReferenceValidation(data, self.params)
        results = list(validation.validate_lpage_when_fpage())
        self.assertEqual(0, len(results))


class SizeUnitsValidationTest(TestCase):
    """Tests for Rule 12: size must have @units='pages'."""

    def setUp(self):
        self.params = {
            "publication_type_requires": {
                "book": ["source", "year"],
            },
        }
        self.reference_data = {
            "ref_id": "B1",
            "publication_type": "book",
            "mixed_citation": "Test ref",
            "mixed_citation_sub_tags": [],
            "source": "Source",
            "year": "2020",
            "all_authors": [],
            "parent": "article",
            "parent_article_type": "research-article",
            "parent_id": None,
            "parent_lang": "en",
            "citing_pub_year": "2024",
            "filtered_not_marked": [],
            "not_marked": [],
            "marked": [],
            "unmatched": [],
            "has_element_citation": True,
            "ext_link_count_element_citation": 0,
            "ext_link_count_mixed_citation": 0,
            "date_in_citation_content_type": None,
            "names_without_surname": [],
        }

    def test_size_units_pages(self):
        data = self.reference_data.copy()
        data["size_info"] = {"units": "pages", "text": "258 p"}
        validation = ReferenceValidation(data, self.params)
        results = list(validation.validate_size_units())
        self.assertEqual(0, len(results))

    def test_size_units_wrong(self):
        data = self.reference_data.copy()
        data["size_info"] = {"units": "volumes", "text": "3"}
        validation = ReferenceValidation(data, self.params)
        results = list(validation.validate_size_units())
        self.assertEqual(1, len(results))
        self.assertEqual("ERROR", results[0]["response"])
        self.assertEqual('<size units="pages">', results[0]["expected_value"])
        self.assertEqual('<size units="volumes">', results[0]["got_value"])

    def test_size_units_missing(self):
        data = self.reference_data.copy()
        data["size_info"] = {"units": None, "text": "258 p"}
        validation = ReferenceValidation(data, self.params)
        results = list(validation.validate_size_units())
        self.assertEqual(1, len(results))
        self.assertEqual("ERROR", results[0]["response"])

    def test_no_size(self):
        data = self.reference_data.copy()
        validation = ReferenceValidation(data, self.params)
        results = list(validation.validate_size_units())
        self.assertEqual(0, len(results))


class DateInCitationContentTypeValidationTest(TestCase):
    """Tests for Rule 13: date-in-citation must have @content-type='access-date'."""

    def setUp(self):
        self.params = {
            "publication_type_requires": {
                "webpage": ["source"],
            },
        }
        self.reference_data = {
            "ref_id": "B1",
            "publication_type": "webpage",
            "mixed_citation": "Test ref",
            "mixed_citation_sub_tags": [],
            "source": "Source",
            "all_authors": [],
            "parent": "article",
            "parent_article_type": "research-article",
            "parent_id": None,
            "parent_lang": "en",
            "citing_pub_year": "2024",
            "filtered_not_marked": [],
            "not_marked": [],
            "marked": [],
            "unmatched": [],
            "has_element_citation": True,
            "ext_link_count_element_citation": 0,
            "ext_link_count_mixed_citation": 0,
            "date_in_citation_content_type": None,
            "names_without_surname": [],
        }

    def test_correct_content_type(self):
        data = self.reference_data.copy()
        data["date_in_citation"] = "10 abr 2010"
        data["date_in_citation_content_type"] = "access-date"
        validation = ReferenceValidation(data, self.params)
        results = list(validation.validate_date_in_citation_content_type())
        self.assertEqual(0, len(results))

    def test_wrong_content_type(self):
        data = self.reference_data.copy()
        data["date_in_citation"] = "10 abr 2010"
        data["date_in_citation_content_type"] = "update"
        validation = ReferenceValidation(data, self.params)
        results = list(validation.validate_date_in_citation_content_type())
        self.assertEqual(1, len(results))
        self.assertEqual("ERROR", results[0]["response"])
        self.assertEqual('<date-in-citation content-type="access-date">', results[0]["expected_value"])
        self.assertEqual('<date-in-citation content-type="update">', results[0]["got_value"])

    def test_missing_content_type(self):
        data = self.reference_data.copy()
        data["date_in_citation"] = "10 abr 2010"
        data["date_in_citation_content_type"] = None
        validation = ReferenceValidation(data, self.params)
        results = list(validation.validate_date_in_citation_content_type())
        self.assertEqual(1, len(results))
        self.assertEqual("ERROR", results[0]["response"])

    def test_no_date_in_citation(self):
        data = self.reference_data.copy()
        validation = ReferenceValidation(data, self.params)
        results = list(validation.validate_date_in_citation_content_type())
        self.assertEqual(0, len(results))


class SurnameInNameValidationTest(TestCase):
    """Tests for Rule 14: name in person-group must have surname."""

    def setUp(self):
        self.params = {
            "publication_type_requires": {
                "journal": ["source", "year"],
            },
        }
        self.reference_data = {
            "ref_id": "B1",
            "publication_type": "journal",
            "mixed_citation": "Test ref",
            "mixed_citation_sub_tags": [],
            "source": "Source",
            "year": "2020",
            "all_authors": [],
            "parent": "article",
            "parent_article_type": "research-article",
            "parent_id": None,
            "parent_lang": "en",
            "citing_pub_year": "2024",
            "filtered_not_marked": [],
            "not_marked": [],
            "marked": [],
            "unmatched": [],
            "has_element_citation": True,
            "ext_link_count_element_citation": 0,
            "ext_link_count_mixed_citation": 0,
            "date_in_citation_content_type": None,
            "names_without_surname": [],
        }

    def test_all_names_have_surname(self):
        data = self.reference_data.copy()
        data["names_without_surname"] = []
        validation = ReferenceValidation(data, self.params)
        results = list(validation.validate_surname_in_name())
        self.assertEqual(0, len(results))

    def test_name_without_surname(self):
        data = self.reference_data.copy()
        data["names_without_surname"] = ["John"]
        validation = ReferenceValidation(data, self.params)
        results = list(validation.validate_surname_in_name())
        self.assertEqual(1, len(results))
        self.assertEqual("ERROR", results[0]["response"])
        self.assertEqual("<surname> in <name>", results[0]["expected_value"])
        self.assertEqual("John", results[0]["got_value"])

    def test_multiple_names_without_surname(self):
        data = self.reference_data.copy()
        data["names_without_surname"] = ["John", "Jane"]
        validation = ReferenceValidation(data, self.params)
        results = list(validation.validate_surname_in_name())
        self.assertEqual(2, len(results))
        self.assertEqual("ERROR", results[0]["response"])
        self.assertEqual("ERROR", results[1]["response"])


class ModelExtractRefListTest(TestCase):
    """Tests for model extraction of new ref-list data fields."""

    def test_ext_link_count_in_element_citation(self):
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" xml:lang="en">
            <front>
            <article-meta>
                <pub-date publication-format="electronic" date-type="pub">
                <year>2024</year>
                </pub-date>
            </article-meta>
            </front>
            <back>
            <ref-list>
                <ref id="B1">
                <mixed-citation>Ref text</mixed-citation>
                <element-citation publication-type="journal">
                <source>J</source>
                <year>2020</year>
                <ext-link ext-link-type="uri" xlink:href="http://example1.com">link1</ext-link>
                <ext-link ext-link-type="uri" xlink:href="http://example2.com">link2</ext-link>
                </element-citation>
                </ref>
            </ref-list>
            </back>
            </article>
        """
        from packtools.sps.models.references import XMLReferences
        xmltree = etree.fromstring(xml)
        refs = list(XMLReferences(xmltree).items)
        self.assertEqual(1, len(refs))
        self.assertEqual(2, refs[0]["ext_link_count_element_citation"])

    def test_ext_link_count_in_mixed_citation(self):
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" xml:lang="en">
            <front>
            <article-meta>
                <pub-date publication-format="electronic" date-type="pub">
                <year>2024</year>
                </pub-date>
            </article-meta>
            </front>
            <back>
            <ref-list>
                <ref id="B1">
                <mixed-citation>Text <ext-link ext-link-type="uri" xlink:href="http://a.com">a</ext-link> and <ext-link ext-link-type="uri" xlink:href="http://b.com">b</ext-link></mixed-citation>
                <element-citation publication-type="journal">
                <source>J</source>
                <year>2020</year>
                </element-citation>
                </ref>
            </ref-list>
            </back>
            </article>
        """
        from packtools.sps.models.references import XMLReferences
        xmltree = etree.fromstring(xml)
        refs = list(XMLReferences(xmltree).items)
        self.assertEqual(1, len(refs))
        self.assertEqual(2, refs[0]["ext_link_count_mixed_citation"])

    def test_date_in_citation_content_type(self):
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" xml:lang="en">
            <front>
            <article-meta>
                <pub-date publication-format="electronic" date-type="pub">
                <year>2024</year>
                </pub-date>
            </article-meta>
            </front>
            <back>
            <ref-list>
                <ref id="B1">
                <mixed-citation>Ref text</mixed-citation>
                <element-citation publication-type="webpage">
                <source>Site</source>
                <date-in-citation content-type="access-date">10 abr 2010</date-in-citation>
                </element-citation>
                </ref>
            </ref-list>
            </back>
            </article>
        """
        from packtools.sps.models.references import XMLReferences
        xmltree = etree.fromstring(xml)
        refs = list(XMLReferences(xmltree).items)
        self.assertEqual(1, len(refs))
        self.assertEqual("access-date", refs[0]["date_in_citation_content_type"])

    def test_names_without_surname(self):
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" xml:lang="en">
            <front>
            <article-meta>
                <pub-date publication-format="electronic" date-type="pub">
                <year>2024</year>
                </pub-date>
            </article-meta>
            </front>
            <back>
            <ref-list>
                <ref id="B1">
                <mixed-citation>Ref text</mixed-citation>
                <element-citation publication-type="journal">
                <person-group person-group-type="author">
                <name>
                <surname>Silva</surname>
                <given-names>J</given-names>
                </name>
                <name>
                <given-names>NoSurname</given-names>
                </name>
                </person-group>
                <source>J</source>
                <year>2020</year>
                </element-citation>
                </ref>
            </ref-list>
            </back>
            </article>
        """
        from packtools.sps.models.references import XMLReferences
        xmltree = etree.fromstring(xml)
        refs = list(XMLReferences(xmltree).items)
        self.assertEqual(1, len(refs))
        self.assertEqual(["NoSurname"], refs[0]["names_without_surname"])

    def test_has_element_citation_true(self):
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" xml:lang="en">
            <front>
            <article-meta>
                <pub-date publication-format="electronic" date-type="pub">
                <year>2024</year>
                </pub-date>
            </article-meta>
            </front>
            <back>
            <ref-list>
                <ref id="B1">
                <mixed-citation>Ref text</mixed-citation>
                <element-citation publication-type="journal">
                <source>J</source>
                <year>2020</year>
                </element-citation>
                </ref>
            </ref-list>
            </back>
            </article>
        """
        from packtools.sps.models.references import XMLReferences
        xmltree = etree.fromstring(xml)
        refs = list(XMLReferences(xmltree).items)
        self.assertEqual(1, len(refs))
        self.assertTrue(refs[0]["has_element_citation"])


class IntegrationRefListValidationTest(TestCase):
    """Integration tests with full XML for ref-list validations."""

    def setUp(self):
        self.params = {
            "publication_type_requires": {
                "journal": ["source", "year", "article-title", "person-group"],
                "book": ["source", "year", "person-group"],
                "webpage": ["source"],
                "confproc": ["source", "year", "person-group"],
                "thesis": ["source", "year", "person-group"],
                "data": ["source", "year", "person-group"],
                "other": [],
            },
        }

    def test_valid_journal_ref(self):
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" xml:lang="en">
            <front>
            <article-meta>
                <pub-date publication-format="electronic" date-type="pub">
                <year>2024</year>
                </pub-date>
            </article-meta>
            </front>
            <back>
            <ref-list>
                <ref id="B1">
                <mixed-citation>Benchimol M. Mem Inst Oswaldo Cruz. 2024;119:e240058.</mixed-citation>
                <element-citation publication-type="journal">
                <person-group person-group-type="author">
                <name>
                <surname>Benchimol</surname>
                <given-names>M</given-names>
                </name>
                </person-group>
                <article-title>Endocytosis</article-title>
                <source>Mem Inst Oswaldo Cruz</source>
                <year>2024</year>
                </element-citation>
                </ref>
            </ref-list>
            </back>
            </article>
        """
        xmltree = etree.fromstring(xml)
        validation = ReferencesValidation(xmltree, self.params)
        results = list(validation.validate())
        error_results = [r for r in results if r["response"] not in ("OK", None)]
        self.assertEqual(0, len(error_results))

    def test_multiple_ext_links_in_element_citation_via_xml(self):
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" xml:lang="en">
            <front>
            <article-meta>
                <pub-date publication-format="electronic" date-type="pub">
                <year>2024</year>
                </pub-date>
            </article-meta>
            </front>
            <back>
            <ref-list>
                <ref id="B1">
                <mixed-citation>Ref text</mixed-citation>
                <element-citation publication-type="journal">
                <person-group person-group-type="author">
                <name><surname>A</surname><given-names>B</given-names></name>
                </person-group>
                <article-title>Title</article-title>
                <source>Journal</source>
                <year>2020</year>
                <ext-link ext-link-type="uri" xlink:href="http://a.com">a</ext-link>
                <ext-link ext-link-type="uri" xlink:href="http://b.com">b</ext-link>
                </element-citation>
                </ref>
            </ref-list>
            </back>
            </article>
        """
        xmltree = etree.fromstring(xml)
        validation = ReferencesValidation(xmltree, self.params)
        results = list(validation.validate())
        ext_link_results = [r for r in results if r["title"] == "element-citation ext-link count"]
        self.assertEqual(1, len(ext_link_results))
        self.assertEqual("ERROR", ext_link_results[0]["response"])

    def test_fpage_without_lpage_via_xml(self):
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" xml:lang="en">
            <front>
            <article-meta>
                <pub-date publication-format="electronic" date-type="pub">
                <year>2024</year>
                </pub-date>
            </article-meta>
            </front>
            <back>
            <ref-list>
                <ref id="B1">
                <mixed-citation>Ref text</mixed-citation>
                <element-citation publication-type="journal">
                <person-group person-group-type="author">
                <name><surname>A</surname><given-names>B</given-names></name>
                </person-group>
                <article-title>Title</article-title>
                <source>Journal</source>
                <year>2020</year>
                <fpage>31</fpage>
                </element-citation>
                </ref>
            </ref-list>
            </back>
            </article>
        """
        xmltree = etree.fromstring(xml)
        validation = ReferencesValidation(xmltree, self.params)
        results = list(validation.validate())
        lpage_results = [r for r in results if r["title"] == "lpage when fpage"]
        self.assertEqual(1, len(lpage_results))
        self.assertEqual("ERROR", lpage_results[0]["response"])

    def test_size_without_units_pages_via_xml(self):
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" xml:lang="en">
            <front>
            <article-meta>
                <pub-date publication-format="electronic" date-type="pub">
                <year>2024</year>
                </pub-date>
            </article-meta>
            </front>
            <back>
            <ref-list>
                <ref id="B1">
                <mixed-citation>Ref text</mixed-citation>
                <element-citation publication-type="book">
                <person-group person-group-type="author">
                <name><surname>A</surname><given-names>B</given-names></name>
                </person-group>
                <source>Book</source>
                <year>2020</year>
                <size units="volumes">3</size>
                </element-citation>
                </ref>
            </ref-list>
            </back>
            </article>
        """
        xmltree = etree.fromstring(xml)
        validation = ReferencesValidation(xmltree, self.params)
        results = list(validation.validate())
        size_results = [r for r in results if r["title"] == "size units"]
        self.assertEqual(1, len(size_results))
        self.assertEqual("ERROR", size_results[0]["response"])

    def test_date_in_citation_wrong_content_type_via_xml(self):
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" xml:lang="en">
            <front>
            <article-meta>
                <pub-date publication-format="electronic" date-type="pub">
                <year>2024</year>
                </pub-date>
            </article-meta>
            </front>
            <back>
            <ref-list>
                <ref id="B1">
                <mixed-citation>Ref text</mixed-citation>
                <element-citation publication-type="webpage">
                <source>Site</source>
                <date-in-citation content-type="update">10 abr 2010</date-in-citation>
                </element-citation>
                </ref>
            </ref-list>
            </back>
            </article>
        """
        xmltree = etree.fromstring(xml)
        validation = ReferencesValidation(xmltree, self.params)
        results = list(validation.validate())
        date_results = [r for r in results if r["title"] == "date-in-citation content-type"]
        self.assertEqual(1, len(date_results))
        self.assertEqual("ERROR", date_results[0]["response"])

    def test_name_without_surname_via_xml(self):
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" xml:lang="en">
            <front>
            <article-meta>
                <pub-date publication-format="electronic" date-type="pub">
                <year>2024</year>
                </pub-date>
            </article-meta>
            </front>
            <back>
            <ref-list>
                <ref id="B1">
                <mixed-citation>Ref text</mixed-citation>
                <element-citation publication-type="journal">
                <person-group person-group-type="author">
                <name>
                <given-names>John</given-names>
                </name>
                </person-group>
                <article-title>Title</article-title>
                <source>Journal</source>
                <year>2020</year>
                </element-citation>
                </ref>
            </ref-list>
            </back>
            </article>
        """
        xmltree = etree.fromstring(xml)
        validation = ReferencesValidation(xmltree, self.params)
        results = list(validation.validate())
        surname_results = [r for r in results if r["title"] == "surname in name"]
        self.assertEqual(1, len(surname_results))
        self.assertEqual("ERROR", surname_results[0]["response"])
