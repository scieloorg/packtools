from unittest import TestCase

from lxml import etree

from packtools.sps.models import funding_group


class FundingTest(TestCase):
    def setUp(self):
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.1" specific-use="sps-1.9" article-type="research-article" xml:lang="en">
        <front>
        <article-meta>
        <article-id specific-use="scielo-v3" pub-id-type="publisher-id">jmDFVrCpQhRKx9bsw68xLPw</article-id>
        <article-id specific-use="scielo-v2" pub-id-type="publisher-id">S0102-86502022000100202</article-id>
        <article-id pub-id-type="other">00202</article-id>
        <article-id pub-id-type="doi">10.1590/acb370101</article-id>
        <funding-group>
        <award-group>
        <funding-source>Natural Science Foundation of Hunan Province</funding-source>
        <award-id>2019JJ40269</award-id>
        </award-group>
        <award-group>
        <funding-source>Hubei Provincial Natural Science Foundation of China</funding-source>
        <award-id>2020CFB547</award-id>
        </award-group>
        <funding-statement>Natural Science Foundation of Hunan Province Grant No. 2019JJ40269 Hubei Provincial Natural Science Foundation of China Grant No. 2020CFB547</funding-statement>
        </funding-group>
        </article-meta>
        </front>
        <back>
        <fn-group>
        <fn fn-type="financial-disclosure">
        <label>Funding</label>
        <p>Conselho Nacional de Desenvolvimento Científico e Tecnológico</p>
        <p>
        [
        <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.13039/501100003593">https://doi.org/10.13039/501100003593</ext-link>
        ]
        </p>
        <p>Grant No: 303625/2019-8</p>
        <p>Fundação de Amparo à Pesquisa do Estado de São Paulo</p>
        <p>
        [
        <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.13039/501100001807">https://doi.org/10.13039/501100001807</ext-link>
        ]
        </p>
        <p>Grant No: 2016/17640-0</p>
        <p>Coordenação de Aperfeiçoamento de Pessoal de Nível Superior.</p>
        <p>
        [
        <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.13039/501100002322">https://doi.org/10.13039/501100002322</ext-link>
        ]
        </p>
        <p>Finance code 0001.</p>
        </fn>
        <fn fn-type="other">
        <label>Data availability statement</label>
        <p>All dataset were generated or analyzed in the current study.</p>
        </fn>
        <fn fn-type="other">
        <p>Research performed at the Immunopharmacology Laboratory, Universidade São Francisco (USF), Bragança Paulista (SP), Brazil. Part of a master degree thesis of the Postgraduate Program in Health Science. Tutor: Alessandra Gambero.</p>
        </fn>
        </fn-group>
        </back>
        </article>
        """
        xml_tree = etree.fromstring(xml)
        self.funding = funding_group.FundingGroup(xml_tree)

    def test_financial_disclosure(self):
        expected = [
            'Conselho Nacional de Desenvolvimento Científico e Tecnológico',
            'https://doi.org/10.13039/501100003593',
            'Grant No: 303625/2019-8',
            'Fundação de Amparo à Pesquisa do Estado de São Paulo',
            'https://doi.org/10.13039/501100001807',
            'Grant No: 2016/17640-0',
            'Coordenação de Aperfeiçoamento de Pessoal de Nível Superior.',
            'https://doi.org/10.13039/501100002322',
            'Finance code 0001.'
        ]
        obtained = self.funding.financial_disclosure
        self.assertEqual(expected, obtained)

