from unittest import TestCase

from lxml import etree

from packtools.sps.models.references import ArticleReferences
from packtools.sps.validation.references import (
    ReferenceValidation,
    ReferencesValidation,
)

params = {
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
    "publication_type_list": [
        "book",
        "confproc",
        "data",
        "database",
        "journal",
        "legal-doc",
        "letter",
        "newspaper",
        "patent",
        "preprint",
        "report",
        "software",
        "thesis",
        "webpage",
        "other"
    ]
}

class ReferenceValidationTest(TestCase):

    def setUp(self):
        params["end_year"] = None

    def test_validate_year_fail(self):
        self.maxDiff = None
        xml = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <pub-date publication-format="electronic" date-type="pub">
            <day>20</day>
            <month>04</month>
            <year>2014</year>
            </pub-date>
            <pub-date publication-format="electronic" date-type="collection">
            <year>2014</year>
            </pub-date>
            <volume>4</volume>
            <issue>1</issue>
            <fpage>108</fpage>
            <lpage>123</lpage>
            </article-meta>
            </front>
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
            <comment>DOI: <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
            </comment>
            </element-citation>
            </ref>
            </ref-list>
            </back>
            </article>
        """

        xmltree = etree.fromstring(xml)
        params["end_year"] = "2014"
        reference = list(ArticleReferences(xmltree).article_references)[0]
        obtained = list(ReferenceValidation(reference, params).validate_year())

        expected = [
            {
                "title": "reference year",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "en",
                "item": "element-citation",
                "sub_item": "year",
                "validation_type": "exist",
                "response": "ERROR",
                "expected_value": "reference year, previous or equal to 2014",
                "got_value": "2015",
                "message": f"Got 2015, expected reference year, previous or equal to 2014",
                "advice": "Identify the reference year, previous or equal to 2014",
                "data": {
                    "all_authors": [
                        {
                            "given-names": "B",
                            "prefix": "The Honorable",
                            "suffix": "III",
                            "surname": "Tran",
                        },
                        {"given-names": "MO", "surname": "Falster"},
                        {"given-names": "K", "surname": "Douglas"},
                        {"given-names": "F", "surname": "Blyth"},
                        {"given-names": "LR", "surname": "Jorm"},
                    ],
                    "article_title": "Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in older ages",
                    "author_type": "person",
                    "citation_ids": {
                        "doi": "10.1016/B1",
                        "pmcid": "11111111",
                        "pmid": "00000000",
                    },
                    "comment_text": {
                        "ext_link_text": "https://doi.org/10.1016/j.drugalcdep.2015.02.028",
                        "full_comment": "DOI: https://doi.org/10.1016/j.drugalcdep.2015.02.028",
                        "text_between": "DOI: ",
                        "text_before": None,
                        "has_comment": True,
                    },
                    "elocation_id": "elocation_B1",
                    "fpage": "85",
                    "label": "1.",
                    "lpage": "91",
                    "main_author": {
                        "given-names": "B",
                        "prefix": "The Honorable",
                        "suffix": "III",
                        "surname": "Tran",
                    },
                    "mixed_citation": "1. Tran B, Falster MO, Douglas K, Blyth F, Jorm "
                    "LR. Smoking and potentially preventable "
                    "hospitalisation: the benefit of smoking cessation "
                    "in older ages. Drug Alcohol Depend. "
                    "2015;150:85-91. DOI: "
                    "https://doi.org/10.1016/j.drugalcdep.2015.02.028",
                    "mixed_citation_sub_tags": ["ext-link"],
                    "publication_type": "journal",
                    "ref_id": "B1",
                    "source": "Drug Alcohol Depend.",
                    "volume": "150",
                    "year": "2015",
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "en",
                },
            },
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_year_success(self):
        self.maxDiff = None
        xml = """
                   <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
                   article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
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
                   <comment>DOI: <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
                   </comment>
                   </element-citation>
                   </ref>
                   </ref-list>
                   </back>
                   </article>
               """

        xmltree = etree.fromstring(xml)
        reference = list(ArticleReferences(xmltree).article_references)[0]
        params["end_year"] = 2020
        obtained = list(
            ReferenceValidation(reference, params).validate_year()
        )
        self.assertEqual(0, len(obtained))

    def test_validate_year_fail_invalid(self):
        self.maxDiff = None
        xml = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
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
            <year>201a</year>
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

        xmltree = etree.fromstring(xml)
        reference = list(ArticleReferences(xmltree).article_references)[0]
        params["end_year"] = 2020
        obtained = list(
            ReferenceValidation(reference, params).validate_year()
        )

        expected = [
            {
                "title": "reference year",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "en",
                "item": "element-citation",
                "sub_item": "year",
                "validation_type": "exist",
                "response": "ERROR",
                "expected_value": "reference year, previous or equal to 2020",
                "got_value": "201a",
                "message": f"Got 201a, expected reference year, previous or equal to 2020",
                "advice": "Identify the reference year, previous or equal to 2020",
                "data": {
                    "all_authors": [
                        {
                            "given-names": "B",
                            "prefix": "The Honorable",
                            "suffix": "III",
                            "surname": "Tran",
                        },
                        {"given-names": "MO", "surname": "Falster"},
                        {"given-names": "K", "surname": "Douglas"},
                        {"given-names": "F", "surname": "Blyth"},
                        {"given-names": "LR", "surname": "Jorm"},
                    ],
                    "article_title": "Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in older ages",
                    "author_type": "person",
                    "citation_ids": {
                        "doi": "10.1016/B1",
                        "pmcid": "11111111",
                        "pmid": "00000000",
                    },
                    "comment_text": {
                        "ext_link_text": "https://doi.org/10.1016/j.drugalcdep.2015.02.028",
                        "full_comment": "DOI: https://doi.org/10.1016/j.drugalcdep.2015.02.028",
                        "text_between": "DOI: ",
                        "text_before": None,
                        "has_comment": True,
                    },
                    "elocation_id": "elocation_B1",
                    "fpage": "85",
                    "label": "1.",
                    "lpage": "91",
                    "main_author": {
                        "given-names": "B",
                        "prefix": "The Honorable",
                        "suffix": "III",
                        "surname": "Tran",
                    },
                    "mixed_citation": "1. Tran B, Falster MO, Douglas K, Blyth F, Jorm "
                    "LR. Smoking and potentially preventable "
                    "hospitalisation: the benefit of smoking cessation "
                    "in older ages. Drug Alcohol Depend. "
                    "2015;150:85-91. DOI: "
                    "https://doi.org/10.1016/j.drugalcdep.2015.02.028",
                    "mixed_citation_sub_tags": ["ext-link"],
                    "publication_type": "journal",
                    "ref_id": "B1",
                    "source": "Drug Alcohol Depend.",
                    "volume": "150",
                    "year": "201a",
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "en",
                },
            },
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_year_fail_missing(self):
        self.maxDiff = None
        xml = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
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

        xmltree = etree.fromstring(xml)
        reference = list(ArticleReferences(xmltree).article_references)[0]
        params["end_year"] = 2020
        obtained = list(
            ReferenceValidation(reference, params).validate_year()
        )

        expected = [
            {
                "title": "reference year",
                "item": "element-citation",
                "sub_item": "year",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "en",
                "validation_type": "exist",
                "response": "ERROR",
                "expected_value": "reference year, previous or equal to 2020",
                "got_value": None,
                "message": f"Got None, expected reference year, previous or equal to 2020",
                "advice": "Identify the reference year, previous or equal to 2020",
                "data": {
                    "all_authors": [
                        {
                            "given-names": "B",
                            "prefix": "The Honorable",
                            "suffix": "III",
                            "surname": "Tran",
                        },
                        {"given-names": "MO", "surname": "Falster"},
                        {"given-names": "K", "surname": "Douglas"},
                        {"given-names": "F", "surname": "Blyth"},
                        {"given-names": "LR", "surname": "Jorm"},
                    ],
                    "article_title": "Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in older ages",
                    "author_type": "person",
                    "citation_ids": {
                        "doi": "10.1016/B1",
                        "pmcid": "11111111",
                        "pmid": "00000000",
                    },
                    "comment_text": {
                        "ext_link_text": "https://doi.org/10.1016/j.drugalcdep.2015.02.028",
                        "full_comment": "DOI: https://doi.org/10.1016/j.drugalcdep.2015.02.028",
                        "text_between": "DOI: ",
                        "text_before": None,
                        "has_comment": True,
                    },
                    "elocation_id": "elocation_B1",
                    "fpage": "85",
                    "label": "1.",
                    "lpage": "91",
                    "main_author": {
                        "given-names": "B",
                        "prefix": "The Honorable",
                        "suffix": "III",
                        "surname": "Tran",
                    },
                    "mixed_citation": "1. Tran B, Falster MO, Douglas K, Blyth F, Jorm "
                    "LR. Smoking and potentially preventable "
                    "hospitalisation: the benefit of smoking cessation "
                    "in older ages. Drug Alcohol Depend. "
                    "2015;150:85-91. DOI: "
                    "https://doi.org/10.1016/j.drugalcdep.2015.02.028",
                    "mixed_citation_sub_tags": ["ext-link"],
                    "publication_type": "journal",
                    "ref_id": "B1",
                    "source": "Drug Alcohol Depend.",
                    "volume": "150",
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "en",
                },
            },
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_source_success(self):
        self.maxDiff = None
        xml = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
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
            <comment>DOI: <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
            </comment>
            </element-citation>
            </ref>
            </ref-list>
            </back>
            </article>
        """

        xmltree = etree.fromstring(xml)
        reference = list(ArticleReferences(xmltree).article_references)[0]
        obtained = list(ReferenceValidation(reference, params).validate_source())
        self.assertEqual(0, len(obtained))

    def test_validate_source_fail(self):
        self.maxDiff = None
        xml = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
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

        xmltree = etree.fromstring(xml)
        reference = list(ArticleReferences(xmltree).article_references)[0]
        obtained = list(ReferenceValidation(reference, params).validate_source())

        expected = [
            {
                "title": "reference source",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "en",
                "item": "element-citation",
                "sub_item": "source",
                "validation_type": "exist",
                "response": "ERROR",
                "expected_value": "reference source",
                "got_value": None,
                "message": "Got None, expected reference source",
                "advice": "Identify the reference source",
                "data": {
                    "all_authors": [
                        {
                            "given-names": "B",
                            "prefix": "The Honorable",
                            "suffix": "III",
                            "surname": "Tran",
                        },
                        {"given-names": "MO", "surname": "Falster"},
                        {"given-names": "K", "surname": "Douglas"},
                        {"given-names": "F", "surname": "Blyth"},
                        {"given-names": "LR", "surname": "Jorm"},
                    ],
                    "article_title": "Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in older ages",
                    "author_type": "person",
                    "citation_ids": {
                        "doi": "10.1016/B1",
                        "pmcid": "11111111",
                        "pmid": "00000000",
                    },
                    "comment_text": {
                        "ext_link_text": "https://doi.org/10.1016/j.drugalcdep.2015.02.028",
                        "full_comment": "DOI: https://doi.org/10.1016/j.drugalcdep.2015.02.028",
                        "text_between": "DOI: ",
                        "text_before": None,
                        "has_comment": True,
                    },
                    "elocation_id": "elocation_B1",
                    "fpage": "85",
                    "label": "1.",
                    "lpage": "91",
                    "main_author": {
                        "given-names": "B",
                        "prefix": "The Honorable",
                        "suffix": "III",
                        "surname": "Tran",
                    },
                    "mixed_citation": "1. Tran B, Falster MO, Douglas K, Blyth F, Jorm "
                    "LR. Smoking and potentially preventable "
                    "hospitalisation: the benefit of smoking cessation "
                    "in older ages. Drug Alcohol Depend. "
                    "2015;150:85-91. DOI: "
                    "https://doi.org/10.1016/j.drugalcdep.2015.02.028",
                    "mixed_citation_sub_tags": ["ext-link"],
                    "publication_type": "journal",
                    "ref_id": "B1",
                    "volume": "150",
                    "year": "2015",
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "en",
                },
            },
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_article_title_success(self):
        self.maxDiff = None
        xml = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
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
            <comment>DOI: <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
            </comment>
            </element-citation>
            </ref>
            </ref-list>
            </back>
            </article>
        """

        xmltree = etree.fromstring(xml)
        reference = list(ArticleReferences(xmltree).article_references)[0]
        obtained = list(ReferenceValidation(reference, params).validate_article_title())
        self.assertEqual(0, len(obtained))

    def test_validate_article_title_fail(self):
        self.maxDiff = None
        xml = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
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

        xmltree = etree.fromstring(xml)
        reference = list(ArticleReferences(xmltree).article_references)[0]
        obtained = list(ReferenceValidation(reference, params).validate_article_title())

        expected = [
            {
                "title": "reference article-title",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "en",
                "item": "element-citation",
                "sub_item": "article-title",
                "validation_type": "exist",
                "response": "ERROR",
                "expected_value": "reference article-title",
                "got_value": None,
                "message": "Got None, expected reference article-title",
                "advice": "Identify the reference article-title",
                "data": {
                    "all_authors": [
                        {
                            "given-names": "B",
                            "prefix": "The Honorable",
                            "suffix": "III",
                            "surname": "Tran",
                        },
                        {"given-names": "MO", "surname": "Falster"},
                        {"given-names": "K", "surname": "Douglas"},
                        {"given-names": "F", "surname": "Blyth"},
                        {"given-names": "LR", "surname": "Jorm"},
                    ],
                    "author_type": "person",
                    "citation_ids": {
                        "doi": "10.1016/B1",
                        "pmcid": "11111111",
                        "pmid": "00000000",
                    },
                    "comment_text": {
                        "ext_link_text": "https://doi.org/10.1016/j.drugalcdep.2015.02.028",
                        "full_comment": "DOI: https://doi.org/10.1016/j.drugalcdep.2015.02.028",
                        "text_between": "DOI: ",
                        "text_before": None,
                        "has_comment": True,
                    },
                    "elocation_id": "elocation_B1",
                    "fpage": "85",
                    "label": "1.",
                    "lpage": "91",
                    "main_author": {
                        "given-names": "B",
                        "prefix": "The Honorable",
                        "suffix": "III",
                        "surname": "Tran",
                    },
                    "mixed_citation": "1. Tran B, Falster MO, Douglas K, Blyth F, Jorm "
                    "LR. Smoking and potentially preventable "
                    "hospitalisation: the benefit of smoking cessation "
                    "in older ages. Drug Alcohol Depend. "
                    "2015;150:85-91. DOI: "
                    "https://doi.org/10.1016/j.drugalcdep.2015.02.028",
                    "mixed_citation_sub_tags": ["ext-link"],
                    "publication_type": "journal",
                    "ref_id": "B1",
                    "source": "Drug Alcohol Depend.",
                    "volume": "150",
                    "year": "2015",
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "en",
                },
            },
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_authors_success(self):
        self.maxDiff = None
        xml = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
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
            <comment>DOI: <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
            </comment>
            </element-citation>
            </ref>
            </ref-list>
            </back>
            </article>
        """

        xmltree = etree.fromstring(xml)
        reference = list(ArticleReferences(xmltree).article_references)[0]
        obtained = list(ReferenceValidation(reference, params).validate_authors())

        self.assertEqual(0, len(obtained))

    def test_validate_collab_success(self):
        self.maxDiff = None
        xml = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <back>
            <ref-list>
                 <ref id="B2">
                    <mixed-citation>
                       2. Brasil. Lei n.
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

        xmltree = etree.fromstring(xml)
        reference = list(ArticleReferences(xmltree).article_references)[0]
        obtained = list(ReferenceValidation(reference, params).validate_authors())
        self.assertEqual(0, len(obtained))

    def test_validate_authors_fail(self):
        self.maxDiff = None
        xml = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <back>
            <ref-list>
            <title>REFERENCES</title>
            <ref id="B1">
            <label>1.</label>
            <mixed-citation>
            1. Tran B, Falster MO, Douglas K, Blyth F, Jorm LR. Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in older ages. Drug Alcohol Depend. 2015;150:85-91. DOI: <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
            </mixed-citation>
            <element-citation publication-type="journal">
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

        xmltree = etree.fromstring(xml)
        reference = list(ArticleReferences(xmltree).article_references)[0]
        obtained = list(ReferenceValidation(reference, params).validate_authors())

        expected = [
            {
                "title": "reference person-group//name or person-group//collab",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "en",
                "item": "element-citation",
                "sub_item": "person-group//name or person-group//collab",
                "validation_type": "exist",
                "response": "ERROR",
                "expected_value": "reference person-group//name or person-group//collab",
                "got_value": None,
                "message": f"Got None, expected reference person-group//name or person-group//collab",
                "advice": "Identify the reference authors",
                "data": {
                    "article_title": "Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in older ages",
                    "author_type": "person",
                    "citation_ids": {
                        "doi": "10.1016/B1",
                        "pmcid": "11111111",
                        "pmid": "00000000",
                    },
                    "comment_text": {
                        "ext_link_text": "https://doi.org/10.1016/j.drugalcdep.2015.02.028",
                        "full_comment": "DOI: https://doi.org/10.1016/j.drugalcdep.2015.02.028",
                        "text_between": "DOI: ",
                        "text_before": None,
                        "has_comment": True,
                    },
                    "elocation_id": "elocation_B1",
                    "fpage": "85",
                    "label": "1.",
                    "lpage": "91",
                    "mixed_citation": "1. Tran B, Falster MO, Douglas K, Blyth F, Jorm "
                    "LR. Smoking and potentially preventable "
                    "hospitalisation: the benefit of smoking cessation "
                    "in older ages. Drug Alcohol Depend. "
                    "2015;150:85-91. DOI: "
                    "https://doi.org/10.1016/j.drugalcdep.2015.02.028",
                    "mixed_citation_sub_tags": ["ext-link"],
                    "publication_type": "journal",
                    "ref_id": "B1",
                    "source": "Drug Alcohol Depend.",
                    "volume": "150",
                    "year": "2015",
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "en",
                },
            },
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_validate_publication_type_success(self):
        self.maxDiff = None
        xml = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
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
            <comment>DOI: <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
            </comment>
            </element-citation>
            </ref>
            </ref-list>
            </back>
            </article>
        """

        xmltree = etree.fromstring(xml)
        reference = list(ArticleReferences(xmltree).article_references)[0]
        obtained = ReferenceValidation(reference, params).validate_publication_type()
        self.assertEqual(0, len(list(obtained)))

    def test_validate_publication_type_fail(self):
        self.maxDiff = None
        xml = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
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
            <comment>DOI: <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
            </comment>
            </element-citation>
            </ref>
            </ref-list>
            </back>
            </article>
        """

        xmltree = etree.fromstring(xml)
        reference = list(ArticleReferences(xmltree).article_references)[0]
        obtained = ReferenceValidation(reference, params).validate_publication_type()

        expected = [
            {
                "title": "reference @publication-type",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "en",
                "item": "element-citation",
                "sub_item": "@publication-type",
                "validation_type": "value in list",
                "response": "ERROR",
                "expected_value": "one of ['other', 'book']",
                "got_value": "journal",
                "message": "Got journal, expected one of ['other', 'book']",
                "advice": "Provide a value for @publication-type, one of ['other', 'book']",
                "data": {
                    "all_authors": [
                        {
                            "given-names": "B",
                            "prefix": "The Honorable",
                            "suffix": "III",
                            "surname": "Tran",
                        },
                        {"given-names": "MO", "surname": "Falster"},
                        {"given-names": "K", "surname": "Douglas"},
                        {"given-names": "F", "surname": "Blyth"},
                        {"given-names": "LR", "surname": "Jorm"},
                    ],
                    "article_title": "Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in older ages",
                    "author_type": "person",
                    "citation_ids": {
                        "doi": "10.1016/B1",
                        "pmcid": "11111111",
                        "pmid": "00000000",
                    },
                    "comment_text": {
                        "ext_link_text": "https://doi.org/10.1016/j.drugalcdep.2015.02.028",
                        "full_comment": "DOI: https://doi.org/10.1016/j.drugalcdep.2015.02.028",
                        "text_between": "DOI: ",
                        "text_before": None,
                        "has_comment": True,
                    },
                    "elocation_id": "elocation_B1",
                    "fpage": "85",
                    "label": "1.",
                    "lpage": "91",
                    "main_author": {
                        "given-names": "B",
                        "prefix": "The Honorable",
                        "suffix": "III",
                        "surname": "Tran",
                    },
                    "mixed_citation": "1. Tran B, Falster MO, Douglas K, Blyth F, Jorm "
                    "LR. Smoking and potentially preventable "
                    "hospitalisation: the benefit of smoking cessation "
                    "in older ages. Drug Alcohol Depend. "
                    "2015;150:85-91. DOI: "
                    "https://doi.org/10.1016/j.drugalcdep.2015.02.028",
                    "mixed_citation_sub_tags": ["ext-link"],
                    "publication_type": "journal",
                    "ref_id": "B1",
                    "source": "Drug Alcohol Depend.",
                    "volume": "150",
                    "year": "2015",
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "en",
                },
            },
        ]

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_success(self):
        self.maxDiff = None
        xml = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front><article-meta><pub-date><year>2021</year></pub-date></article-meta></front>
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
            <comment>DOI: <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
            </comment>
            </element-citation>
            </ref>
            </ref-list>
            </back>
            </article>
        """

        xmltree = etree.fromstring(xml)
        params["end_year"] = 2020
        params["dtd_version"] = 1.3
        obtained = list(
            ReferencesValidation(
                xmltree,
                params,
            ).validate()
        )
        self.assertEqual(1, len(obtained))

    def test_validate_comment_is_required_or_not_B1(self):
        self.maxDiff = None
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
        reference = list(ArticleReferences(xml_tree).article_references)[0]
        obtained = list(
            ReferenceValidation(reference, params).validate_comment_is_required_or_not()
        )

        expected = [
            {
                "title": "comment is required or not",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
                "item": "element-citation",
                "sub_item": "comment",
                "validation_type": "exist",
                "response": "ERROR",
                "got_value": "<comment></comment>text<ext-link>https://...</ext-link>",
                "expected_value": "<comment>text<ext-link>https://...</ext-link></comment>",
                "message": "Got <comment></comment>text<ext-link>https://...</ext-link>, expected "
                "<comment>text<ext-link>https://...</ext-link></comment>",
                "advice": "Wrap the <ext-link> tag and its content within the <comment> tag",
                "data": {
                    "author_type": "person",
                    "comment_text": {
                        "ext_link_text": "https://...",
                        "full_comment": None,
                        "text_between": None,
                        "text_before": "text",
                        "has_comment": True,
                    },
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "publication_type": "other",
                    "ref_id": "B1",
                    "text_before_extlink": "text",
                },
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_comment_is_required_or_not_B2(self):
        self.maxDiff = None
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
        reference = list(ArticleReferences(xml_tree).article_references)[0]
        obtained = list(
            ReferenceValidation(reference, params).validate_comment_is_required_or_not()
        )

        self.assertListEqual(obtained, [])

    def test_validate_comment_is_required_or_not_B3(self):
        self.maxDiff = None
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
        reference = list(ArticleReferences(xml_tree).article_references)[0]
        obtained = list(
            ReferenceValidation(reference, params).validate_comment_is_required_or_not()
        )

        expected = [
            {
                "title": "comment is required or not",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
                "item": "element-citation",
                "sub_item": "comment",
                "validation_type": "exist",
                "response": "ERROR",
                "got_value": "<comment></comment><ext-link>https://...</ext-link>",
                "expected_value": "<ext-link>https://...</ext-link>",
                "message": "Got <comment></comment><ext-link>https://...</ext-link>, expected "
                "<ext-link>https://...</ext-link>",
                "advice": "Remove the <comment> tag that has no content",
                "data": {
                    "author_type": "person",
                    "comment_text": {
                        "ext_link_text": "https://...",
                        "full_comment": None,
                        "text_between": None,
                        "text_before": None,
                        "has_comment": True,
                    },
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "publication_type": "other",
                    "ref_id": "B3",
                },
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_comment_is_required_or_not_B4(self):
        self.maxDiff = None
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
        reference = list(ArticleReferences(xml_tree).article_references)[0]
        obtained = list(
            ReferenceValidation(reference, params).validate_comment_is_required_or_not()
        )

        self.assertListEqual(obtained, [])

    def test_validate_comment_is_required_or_not_B5(self):
        self.maxDiff = None
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
        reference = list(ArticleReferences(xml_tree).article_references)[0]
        obtained = list(
            ReferenceValidation(reference, params).validate_comment_is_required_or_not()
        )

        expected = [
            {
                "title": "comment is required or not",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
                "item": "element-citation",
                "sub_item": "comment",
                "validation_type": "exist",
                "response": "ERROR",
                "got_value": "<comment><ext-link>https://...</ext-link></comment>",
                "expected_value": "<ext-link>https://...</ext-link>",
                "message": "Got <comment><ext-link>https://...</ext-link></comment>, expected "
                "<ext-link>https://...</ext-link>",
                "advice": "Remove the <comment> tag that has no content",
                "data": {
                    "author_type": "person",
                    "comment_text": {
                        "ext_link_text": "https://...",
                        "full_comment": "https://...",
                        "text_between": None,
                        "text_before": None,
                        "has_comment": True,
                    },
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "publication_type": "other",
                    "ref_id": "B5",
                },
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_mixed_citation_sub_tags(self):
        self.maxDiff = None
        xml = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <back>
            <ref-list>
            <title>REFERENCES</title>
            <ref id="B1">
            <label>1.</label>
            <mixed-citation>
            1. Tran B, Falster MO, Douglas K, Blyth F, Jorm LR. Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in older ages. Drug Alcohol Depend. 2015;150:85-91. DOI: <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
            </mixed-citation>
            <element-citation publication-type="journal" />
            </ref>
            </ref-list>
            </back>
            </article>
        """

        xmltree = etree.fromstring(xml)
        reference = list(ArticleReferences(xmltree).article_references)[0]
        obtained = list(
            ReferenceValidation(reference, params).validate_mixed_citation_sub_tags()
        )

        expected = [
            {
                "advice": "remove ['ext-link'] from mixed-citation",
                "data": {
                    "author_type": "person",
                    "label": "1.",
                    "mixed_citation": "1. Tran B, Falster MO, Douglas K, Blyth F, Jorm "
                    "LR. Smoking and potentially preventable "
                    "hospitalisation: the benefit of smoking cessation "
                    "in older ages. Drug Alcohol Depend. "
                    "2015;150:85-91. DOI: "
                    "https://doi.org/10.1016/j.drugalcdep.2015.02.028",
                    "mixed_citation_sub_tags": ["ext-link"],
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "en",
                    "publication_type": "journal",
                    "ref_id": "B1",
                },
                "expected_value": [],
                "got_value": ["ext-link"],
                "item": "mixed-citation",
                "message": "Got ['ext-link'], expected []",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "response": "ERROR",
                "sub_item": None,
                "title": "mixed-citation sub elements",
                "validation_type": "exist",
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_title_tag_by_dtd_version(self):
        self.maxDiff = None

        xml = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="research-article" 
            dtd-version="1.3" specific-use="sps-1.9" xml:lang="en">
                <back>
                    <ref-list>
                        <title>REFERENCES</title>
                        <ref id="B1">
                            <element-citation publication-type="book">
                                <chapter-title>Chapter Title</chapter-title>
                            </element-citation>
                        </ref>
                    </ref-list>
                </back>
            </article>
        """

        xml_tree = etree.fromstring(xml)

        # Completa os parâmetros existentes
        params["dtd_version"] = "1.3"
        params["end_year"] = 2010

        # Executa a validação completa
        all_obtained = list(ReferencesValidation(xml_tree, params).validate())

        # Filtra apenas os resultados relevantes para `validate_title_tag_by_dtd_version`
        obtained = [
            item
            for item in all_obtained
            if item["title"] == "part-title"
        ]

        # Resultado esperado
        expected = [
            {
                'advice': 'Replace <chapter-title> with <part-title> to meet the required standard.',
                'data': {
                    'author_type': 'person',
                    'chapter_title': 'Chapter Title',
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'en',
                    'publication_type': 'book',
                    'ref_id': 'B1'
                },
                'expected_value': '<part-title>',
                'got_value': '<chapter-title>',
                'item': 'element-citation',
                'message': 'Got <chapter-title>, expected <part-title>',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'response': 'CRITICAL',
                'sub_item': 'part-title',
                'title': 'part-title',
                'validation_type': 'exist'
            }
        ]

        # Verificação
        self.assertEqual(len(obtained), len(expected))
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_title_tag_by_dtd_version_invalid_dtd_version(self):
        self.maxDiff = None

        xml = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="research-article" 
            dtd-version="a" specific-use="sps-1.9" xml:lang="en">
                <back>
                    <ref-list>
                        <title>REFERENCES</title>
                        <ref id="B1">
                            <element-citation publication-type="book">
                                <chapter-title>Chapter Title</chapter-title>
                            </element-citation>
                        </ref>
                    </ref-list>
                </back>
            </article>
        """

        xml_tree = etree.fromstring(xml)

        # Completa os parâmetros existentes
        params["dtd_version"] = "a"
        params["end_year"] = 2010

        # Verifica se a exceção ValueError é levantada com a mensagem esperada
        with self.assertRaises(ValueError) as context:
            list(ReferencesValidation(xml_tree, params).validate())

        # Valida a mensagem de erro
        self.assertEqual(
            str(context.exception),
            "Invalid DTD version: expected a numeric value."
        )
