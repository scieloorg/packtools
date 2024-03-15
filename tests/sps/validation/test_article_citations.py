from unittest import TestCase

from lxml import etree

from packtools.sps.models.article_citations import ArticleCitations
from packtools.sps.validation.article_citations import ArticleCitationValidation, ArticleCitationsValidation


class ArticleCitationValidationTest(TestCase):
    def test_validate_article_citation_year_fail(self):
        self.maxDiff = None
        xml = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <pub-date publication-format="electronic" date-type="pub">
            <day>20</day>
            <month>04</month>
            <year>2014</year>
            </pub-date>
            <pub-date publication-format="electronic" date-type="collection">
            <year>2003</year>
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
            <comment>
            DOI:
            <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
            </comment>
            </element-citation>
            </ref>
            </ref-list>
            </back>
            </article>
        """

        xmltree = etree.fromstring(xml)
        citation = list(ArticleCitations(xmltree).article_citations)[0]
        obtained = list(ArticleCitationValidation(xmltree, citation).validate_article_citation_year())

        expected = [
            {
                'title': 'element citation validation',
                'item': 'element-citation',
                'sub-item': 'year',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'a value for year between 0 and 2014',
                'got_value': '2015',
                'message': f'Got 2015 expected a value for year between 0 and 2014',
                'advice': 'The year in reference (ref-id: B1) is missing or is invalid, provide a valid value for year'
            },
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_article_citation_year_success(self):
        self.maxDiff = None
        xml = """
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
                   <comment>
                   DOI:
                   <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
                   </comment>
                   </element-citation>
                   </ref>
                   </ref-list>
                   </back>
                   </article>
               """

        xmltree = etree.fromstring(xml)
        citation = list(ArticleCitations(xmltree).article_citations)[0]
        obtained = list(ArticleCitationValidation(xmltree, citation).validate_article_citation_year(start_year=2000, end_year=2020))

        expected = [
            {
                'title': 'element citation validation',
                'item': 'element-citation',
                'sub-item': 'year',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'a value for year between 2000 and 2020',
                'got_value': '2015',
                'message': 'Got 2015 expected a value for year between 2000 and 2020',
                'advice': None
            },
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_article_citation_year_fail_invalid(self):
        self.maxDiff = None
        xml = """
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
            <year>201a</year>
            <volume>150</volume>
            <fpage>85</fpage>
            <lpage>91</lpage>
            <pub-id pub-id-type="doi">10.1016/B1</pub-id>
            <elocation-id>elocation_B1</elocation-id>
            <pub-id pub-id-type="pmid">00000000</pub-id>
            <pub-id pub-id-type="pmcid">11111111</pub-id>
            <comment>
            DOI:
            <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
            </comment>
            </element-citation>
            </ref>
            </ref-list>
            </back>
            </article>
        """

        xmltree = etree.fromstring(xml)
        citation = list(ArticleCitations(xmltree).article_citations)[0]
        obtained = list(ArticleCitationValidation(xmltree, citation).validate_article_citation_year(start_year=2000, end_year=2020))

        expected = [
            {
                'title': 'element citation validation',
                'item': 'element-citation',
                'sub-item': 'year',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'a value for year between 2000 and 2020',
                'got_value': '201a',
                'message': f'Got 201a expected a value for year between 2000 and 2020',
                'advice': 'The year in reference (ref-id: B1) is missing or is invalid, provide a valid value for year'
            },
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_article_citation_year_fail_missing(self):
        self.maxDiff = None
        xml = """
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
            <volume>150</volume>
            <fpage>85</fpage>
            <lpage>91</lpage>
            <pub-id pub-id-type="doi">10.1016/B1</pub-id>
            <elocation-id>elocation_B1</elocation-id>
            <pub-id pub-id-type="pmid">00000000</pub-id>
            <pub-id pub-id-type="pmcid">11111111</pub-id>
            <comment>
            DOI:
            <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
            </comment>
            </element-citation>
            </ref>
            </ref-list>
            </back>
            </article>
        """

        xmltree = etree.fromstring(xml)
        citation = list(ArticleCitations(xmltree).article_citations)[0]
        obtained = list(ArticleCitationValidation(xmltree, citation).validate_article_citation_year(start_year=2000, end_year=2020))

        expected = [
            {
                'title': 'element citation validation',
                'item': 'element-citation',
                'sub-item': 'year',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'a value for year between 2000 and 2020',
                'got_value': None,
                'message': f'Got None expected a value for year between 2000 and 2020',
                'advice': 'The year in reference (ref-id: B1) is missing or is invalid, provide a valid value for year'
            },
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_article_citation_source_success(self):
        self.maxDiff = None
        xml = """
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
            <comment>
            DOI:
            <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
            </comment>
            </element-citation>
            </ref>
            </ref-list>
            </back>
            </article>
        """

        xmltree = etree.fromstring(xml)
        citation = list(ArticleCitations(xmltree).article_citations)[0]
        obtained = list(ArticleCitationValidation(xmltree, citation).validate_article_citation_source())

        expected = [
            {
                'title': 'element citation validation',
                'item': 'element-citation',
                'sub-item': 'source',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'Drug Alcohol Depend.',
                'got_value': 'Drug Alcohol Depend.',
                'message': 'Got Drug Alcohol Depend. expected Drug Alcohol Depend.',
                'advice': None
            },
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_article_citation_source_fail(self):
        self.maxDiff = None
        xml = """
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
            <year>2015</year>
            <volume>150</volume>
            <fpage>85</fpage>
            <lpage>91</lpage>
            <pub-id pub-id-type="doi">10.1016/B1</pub-id>
            <elocation-id>elocation_B1</elocation-id>
            <pub-id pub-id-type="pmid">00000000</pub-id>
            <pub-id pub-id-type="pmcid">11111111</pub-id>
            <comment>
            DOI:
            <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
            </comment>
            </element-citation>
            </ref>
            </ref-list>
            </back>
            </article>
        """

        xmltree = etree.fromstring(xml)
        citation = list(ArticleCitations(xmltree).article_citations)[0]
        obtained = list(ArticleCitationValidation(xmltree, citation).validate_article_citation_source())

        expected = [
            {
                'title': 'element citation validation',
                'item': 'element-citation',
                'sub-item': 'source',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'a valid value to source',
                'got_value': None,
                'message': 'Got None expected a valid value to source',
                'advice': 'The source in reference (ref-id: B1) is missing provide a valid value to source'
            },
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_article_citation_article_title_success(self):
        self.maxDiff = None
        xml = """
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
            <comment>
            DOI:
            <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
            </comment>
            </element-citation>
            </ref>
            </ref-list>
            </back>
            </article>
        """

        xmltree = etree.fromstring(xml)
        citation = list(ArticleCitations(xmltree).article_citations)[0]
        obtained = list(ArticleCitationValidation(xmltree, citation).validate_article_citation_article_title())

        expected = [
            {
                'title': 'element citation validation',
                'item': 'element-citation',
                'sub-item': 'article-title',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'Smoking and potentially preventable hospitalisation: the benefit of smoking '
                                  'cessation in older ages',
                'got_value': 'Smoking and potentially preventable hospitalisation: the benefit of smoking cessation '
                             'in older ages',
                'message': 'Got Smoking and potentially preventable hospitalisation: the benefit of smoking cessation '
                           'in older ages expected Smoking and potentially preventable hospitalisation: the benefit '
                           'of smoking cessation in older ages',
                'advice': None
            },
        ]

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_citation_article_title_fail(self):
        self.maxDiff = None
        xml = """
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
            <source>Drug Alcohol Depend.</source>
            <year>2015</year>
            <volume>150</volume>
            <fpage>85</fpage>
            <lpage>91</lpage>
            <pub-id pub-id-type="doi">10.1016/B1</pub-id>
            <elocation-id>elocation_B1</elocation-id>
            <pub-id pub-id-type="pmid">00000000</pub-id>
            <pub-id pub-id-type="pmcid">11111111</pub-id>
            <comment>
            DOI:
            <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
            </comment>
            </element-citation>
            </ref>
            </ref-list>
            </back>
            </article>
        """

        xmltree = etree.fromstring(xml)
        citation = list(ArticleCitations(xmltree).article_citations)[0]
        obtained = list(ArticleCitationValidation(xmltree, citation).validate_article_citation_article_title())

        expected = [
            {
                'title': 'element citation validation',
                'item': 'element-citation',
                'sub-item': 'article-title',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'a valid value for article-title',
                'got_value': None,
                'message': 'Got None expected a valid value for article-title',
                'advice': 'The article-title in reference (ref-id: B1) is missing provide a valid value for article-title'
            },
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_article_citation_authors_success(self):
        self.maxDiff = None
        xml = """
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
            <comment>
            DOI:
            <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
            </comment>
            </element-citation>
            </ref>
            </ref-list>
            </back>
            </article>
        """

        xmltree = etree.fromstring(xml)
        citation = list(ArticleCitations(xmltree).article_citations)[0]
        obtained = list(ArticleCitationValidation(xmltree, citation).validate_article_citation_authors())

        expected = [
            {
                'title': 'element citation validation',
                'item': 'element-citation',
                'sub-item': 'person-group//name or person-group//colab',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'at least 1 author in each element-citation',
                'got_value': '5 authors',
                'message': f'Got 5 authors expected at least 1 author in each element-citation',
                'advice': None
            },
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_article_citation_collab_success(self):
        self.maxDiff = None
        xml = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
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
        citation = list(ArticleCitations(xmltree).article_citations)[0]
        obtained = list(ArticleCitationValidation(xmltree, citation).validate_article_citation_authors())

        expected = [
            {
                'title': 'element citation validation',
                'item': 'element-citation',
                'sub-item': 'person-group//name or person-group//colab',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'at least 1 author in each element-citation',
                'got_value': '1 authors',
                'message': f'Got 1 authors expected at least 1 author in each element-citation',
                'advice': None
            },
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_article_citation_authors_fail(self):
        self.maxDiff = None
        xml = """
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
            <comment>
            DOI:
            <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
            </comment>
            </element-citation>
            </ref>
            </ref-list>
            </back>
            </article>
        """

        xmltree = etree.fromstring(xml)
        citation = list(ArticleCitations(xmltree).article_citations)[0]
        obtained = list(ArticleCitationValidation(xmltree, citation).validate_article_citation_authors())

        expected = [
            {
                'title': 'element citation validation',
                'item': 'element-citation',
                'sub-item': 'person-group//name or person-group//colab',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'at least 1 author in each element-citation',
                'got_value': '0 authors',
                'message': f'Got 0 authors expected at least 1 author in each element-citation',
                'advice': 'There are no authors for the reference (ref-id: B1) provide at least 1 author'
            },
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_article_citation_publication_type_success(self):
        self.maxDiff = None
        xml = """
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
            <comment>
            DOI:
            <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
            </comment>
            </element-citation>
            </ref>
            </ref-list>
            </back>
            </article>
        """

        xmltree = etree.fromstring(xml)
        citation = list(ArticleCitations(xmltree).article_citations)[0]
        obtained = ArticleCitationValidation(xmltree, citation).validate_article_citation_publication_type(
            publication_type_list=['journal', 'book'])

        expected = [
            {
                'title': 'element citation validation',
                'item': 'element-citation',
                'sub-item': 'publication-type',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': ['journal', 'book'],
                'got_value': 'journal',
                'message': 'Got journal expected one item of this list: journal | book',
                'advice': None
            },
        ]

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_citation_publication_type_fail(self):
        self.maxDiff = None
        xml = """
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
            <comment>
            DOI:
            <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
            </comment>
            </element-citation>
            </ref>
            </ref-list>
            </back>
            </article>
        """

        xmltree = etree.fromstring(xml)
        citation = list(ArticleCitations(xmltree).article_citations)[0]
        obtained = ArticleCitationValidation(xmltree, citation).validate_article_citation_publication_type(
            publication_type_list=['other', 'book'])

        expected = [
            {
                'title': 'element citation validation',
                'item': 'element-citation',
                'sub-item': 'publication-type',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': ['other', 'book'],
                'got_value': 'journal',
                'message': 'Got journal expected one item of this list: other | book',
                'advice': 'publication-type for the reference (ref-id: B1) is missing or is invalid, '
                          'provide one value from the list: other | book',
            },
        ]

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_citation_success(self):
        self.maxDiff = None
        xml = """
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
            <comment>
            DOI:
            <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
            </comment>
            </element-citation>
            </ref>
            </ref-list>
            </back>
            </article>
        """

        xmltree = etree.fromstring(xml)
        obtained = list(ArticleCitationsValidation(xmltree).validate_article_citations(
            xmltree,
            publication_type_list=['journal', 'book'],
            start_year=2000,
            end_year=2020
        ))

        expected = [
            {
                'title': 'element citation validation',
                'item': 'element-citation',
                'sub-item': 'year',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'a value for year between 2000 and 2020',
                'got_value': '2015',
                'message': 'Got 2015 expected a value for year between 2000 and 2020',
                'advice': None
            },
            {
                'title': 'element citation validation',
                'item': 'element-citation',
                'sub-item': 'source',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'Drug Alcohol Depend.',
                'got_value': 'Drug Alcohol Depend.',
                'message': 'Got Drug Alcohol Depend. expected Drug Alcohol Depend.',
                'advice': None
            },
            {
                'title': 'element citation validation',
                'item': 'element-citation',
                'sub-item': 'article-title',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'Smoking and potentially preventable hospitalisation: the benefit of smoking '
                                  'cessation in older ages',
                'got_value': 'Smoking and potentially preventable hospitalisation: the benefit of smoking cessation '
                             'in older ages',
                'message': 'Got Smoking and potentially preventable hospitalisation: the benefit of smoking cessation '
                           'in older ages expected Smoking and potentially preventable hospitalisation: the benefit '
                           'of smoking cessation in older ages',
                'advice': None
            },
            {
                'title': 'element citation validation',
                'item': 'element-citation',
                'sub-item': 'person-group//name or person-group//colab',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'at least 1 author in each element-citation',
                'got_value': '5 authors',
                'message': f'Got 5 authors expected at least 1 author in each element-citation',
                'advice': None
            },
            {
                'title': 'element citation validation',
                'item': 'element-citation',
                'sub-item': 'publication-type',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': ['journal', 'book'],
                'got_value': 'journal',
                'message': 'Got journal expected one item of this list: journal | book',
                'advice': None
            },
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)
