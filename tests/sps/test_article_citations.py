from packtools.sps.models.article_citations import ArticleCitations
from unittest import TestCase, skip

from lxml import etree


class AuthorsTest(TestCase):

    def setUp(self):
        xml = (
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <back>
            <ref-list>
            <title>REFERENCES</title>
            <ref id="B1">
            <label>1.</label>
            <mixed-citation>
            1. Tran B, Falster MO, Douglas K, Blyth F, Jorm LR. Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in older ages. Drug Alcohol Depend. 2015;150:85-91. DOI:
            <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
            </mixed-citation>
            <element-citation publication-type="journal">
            <person-group person-group-type="author">
            <name>
            <surname>Tran</surname>
            <given-names>B</given-names>
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
            <comment>
            DOI:
            <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
            </comment>
            </element-citation>
            </ref>
            <ref id="B2">
            <label>2.</label>
            <mixed-citation>
            2. Kwon JA, Jeon W, Park EC, Kim JH, Kim SJ, Yoo KB, et al. Effects of disease detection on changes in smoking behavior. Yonsei Med J. 2015;56(4): 1143-9. DOI:
            <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.3349/ymj.2015.56.4.1143">https://doi.org/10.3349/ymj.2015.56.4.1143</ext-link>
            </mixed-citation>
            <element-citation publication-type="journal">
            <person-group person-group-type="author">
            <name>
            <surname>Kwon</surname>
            <given-names>JA</given-names>
            </name>
            <name>
            <surname>Jeon</surname>
            <given-names>W</given-names>
            </name>
            <name>
            <surname>Park</surname>
            <given-names>EC</given-names>
            </name>
            <name>
            <surname>Kim</surname>
            <given-names>JH</given-names>
            </name>
            <name>
            <surname>Kim</surname>
            <given-names>SJ</given-names>
            </name>
            <name>
            <surname>Yoo</surname>
            <given-names>KB</given-names>
            </name>
            <etal/>
            </person-group>
            <article-title>Effects of disease detection on changes in smoking behavior</article-title>
            <source>Yonsei Med J.</source>
            <year>2015</year>
            <volume>56</volume>
            <issue>4</issue>
            <fpage>1143</fpage>
            <lpage>9</lpage>
            <comment>
            DOI:
            <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.3349/ymj.2015.56.4.1143">https://doi.org/10.3349/ymj.2015.56.4.1143</ext-link>
            </comment>
            </element-citation>
            </ref>
            </ref-list>
            </back>
            </article>
            """
        )
        xmltree = etree.fromstring(xml)
        self.citations = ArticleCitations(xmltree)

    def test_citations(self):
        expected = [
            {
                'label': '1',
                'source': 'Drug Alcohol Depend.',
                'author': 'Tran B',
                'volume': '150',
                'fpage': '85',
                'year': '2015',
                'article_title': 'Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in older ages'
            },
            {
                'label': '2',
                'source': 'Yonsei Med J.',
                'author': 'Kwon JA',
                'volume': '56',
                'issue': '4',
                'fpage': '1143',
                'year': '2015',
                'article_title': 'Effects of disease detection on changes in smoking behavior'
            }
        ]
        result = self.citations.article_citations
        self.assertEqual(expected, result)
