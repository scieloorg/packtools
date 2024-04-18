from packtools.sps.models.article_citations import ArticleCitations
from unittest import TestCase, skip

from lxml import etree


class AuthorsTest(TestCase):
    def test_citations_many_authors(self):
        self.maxDiff = None
        xml = ("""
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
            """)
        xmltree = etree.fromstring(xml)
        obtained = list(ArticleCitations(xmltree).article_citations)
        expected = [
            {
                'ref_id': 'B1',
                'label': '1',
                'publication_type': 'journal',
                'author_type': 'person',
                'mixed_citation': '1. Tran B, Falster MO, Douglas K, Blyth F, Jorm LR. Smoking and potentially '
                                  'preventable hospitalisation: the benefit of smoking cessation in older ages. Drug '
                                  'Alcohol Depend. 2015;150:85-91. DOI: '
                                  'https://doi.org/10.1016/j.drugalcdep.2015.02.028',
                'source': 'Drug Alcohol Depend.',
                'main_author': {'surname': 'Tran', 'given-names': 'B', 'prefix': 'The Honorable', 'suffix': 'III'},
                'all_authors': [
                    {'surname': 'Tran', 'given-names': 'B', 'prefix': 'The Honorable', 'suffix': 'III'},
                    {'surname': 'Falster', 'given-names': 'MO'},
                    {'surname': 'Douglas', 'given-names': 'K'},
                    {'surname': 'Blyth', 'given-names': 'F'},
                    {'surname': 'Jorm', 'given-names': 'LR'}
                ],
                'volume': '150',
                'fpage': '85',
                'lpage': '91',
                'elocation_id': 'elocation_B1',
                'year': '2015',
                'article_title': 'Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in older ages',
                'citation_ids': {'pmid': '00000000', 'pmcid': '11111111', 'doi': '10.1016/B1'},
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_citations_one_author(self):
        self.maxDiff = None
        xml = ("""
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
            """)
        xmltree = etree.fromstring(xml)
        obtained = list(ArticleCitations(xmltree).article_citations)
        expected = [
            {
                'ref_id': 'B2',
                'publication_type': 'book',
                'author_type': 'person',
                'mixed_citation': 'BARTHES, Roland. Aula . São Pulo: Cultrix, 1987.',
                'source': 'Aula',
                'main_author': {'surname': 'BARTHES', 'given-names': 'Roland'},
                'all_authors': [{'surname': 'BARTHES', 'given-names': 'Roland'}],
                'elocation_id': 'elocation_B2',
                'year': '1987',
                'citation_ids': {'pmid': '22222222', 'pmcid': '33333333', 'doi': '10.1016/B2'}
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_citations_collab_element(self):
        self.maxDiff = None
        xml = ('''
        <article xmlns:xlink="http://www.w3.org/1999/xlink" specific-use="sps-1.4" dtd-version="1.0" xml:lang="pt" article-type="research-article">
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
        ''')
        xmltree = etree.fromstring(xml)
        obtained = list(ArticleCitations(xmltree).article_citations)
        expected = [
            {
                'ref_id': 'B2',
                'publication_type': 'other',
                'author_type': 'institutional',
                'mixed_citation': '2. Brasil. Lei n. o 10.332, de 19/12/2001. Instituiu '
                                  'mecanismo de financiamento para o programa de ciência e '
                                  'tecnologia para o agronegócio, para o programa de fomento '
                                  'à pesquisa em saúde, para o programa de bioteconologia e '
                                  'recursos genéticos – Genoma, para o programa de ciência e '
                                  'tecnologia para o setor aeronáutico e para o programa de '
                                  'inovação para competitividade, e dá outras providências. '
                                  'Diário Oficial da União 2001 dez 19.',
                'source': 'Diário Oficial da União',
                'article_title': 'Lei n.º 10.332, de 19/12/2001: Instituiu mecanismo de '
                                 'financiamento para o programa de ciência e tecnologia para '
                                 'o agronegócio, para o programa de fomento à pesquisa em '
                                 'saúde, para o programa de bioteconologia e recursos '
                                 'genéticos - Genoma, para o programa de ciência e tecnologia '
                                 'para o setor aeronáutico e para o programa de inovação para '
                                 'competitividade, e dá outras providências',
                'year': '2001',
                'main_author': {'collab': ['Brasil']},
                'all_authors': [{'collab': ['Brasil']}],
            },

        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])
