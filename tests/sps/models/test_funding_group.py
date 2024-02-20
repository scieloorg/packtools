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
        <principal-award-recipient>Stanford</principal-award-recipient>
        <principal-investigator>
            <string-name>
                <given-names>Sharon R.</given-names>
                <surname>Kaufman</surname>
            </string-name>
        </principal-investigator>
        </award-group>
        <award-group>
        <funding-source>Hubei Provincial Natural Science Foundation of China</funding-source>
        <award-id>2020CFB547</award-id>
        <principal-award-recipient>Berkeley</principal-award-recipient>
        <principal-investigator>
            <string-name>
                <given-names>João</given-names>
                <surname>Silva</surname>
            </string-name>
        </principal-investigator>
        </award-group>
        <funding-statement>Natural Science Foundation of Hunan Province Grant No. 2019JJ40269 Hubei Provincial Natural Science Foundation of China Grant No. 2020CFB547</funding-statement>
        </funding-group>
        </article-meta>
        </front>
        <back>
        <ack>
            <title>Acknowledgments</title>
            <p>Federal University of Rio de Janeiro (UFRJ), School of Medicine, <b>Department of Surgery and Anesthesiology</b>, RJ, Brazil, provided important support for this research.</p>
            <p>This study was funded by the Hospital Municipal Conde Modesto Leal, Center of Diagnostic and Treatment (CDT), Municipal Secretariat of Health, Maricá, RJ, Brazil.</p>
            <p>This study was presented as a poster presentation at the Brazilian Congress of Anesthesiology CBA Annual Meeting 10-14 November 2018, Belém do Pará, Brazil.</p>
        </ack>
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
        <ext-link ext-link-type="uri" 
        xlink:href="https://doi.org/10.13039/501100002322">https://doi.org/10.13039/501100002322</ext-link>
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
        <fn fn-type="supported-by">
        <p>Conselho Nacional de Desenvolvimento Científico e Tecnológico</p>
        <p>
        Número 123.456-7
        </p>
        </fn>
        </fn-group>
        </back>
        </article>
        """
        xml_tree = etree.fromstring(xml)
        self.funding = funding_group.FundingGroup(xml_tree)

    def test_fn_financial_information(self):
        self.maxDiff = None
        expected = [
            {
                'fn-type': 'financial-disclosure',
                'look-like-funding-source': [
                    'Conselho Nacional de Desenvolvimento Científico e Tecnológico',
                    'Fundação de Amparo à Pesquisa do Estado de São Paulo',
                    'Coordenação de Aperfeiçoamento de Pessoal de Nível Superior.'
                ],
                'look-like-award-id': [
                    '303625/2019-8',
                    '2016/17640-0',
                    '0001.'
                ]
            },
            {
                'fn-type': 'supported-by',
                'look-like-funding-source': ['Conselho Nacional de Desenvolvimento Científico e Tecnológico'],
                'look-like-award-id': ['123.456-7'],
            }
        ]

        obtained = self.funding.fn_financial_information(
            special_chars_funding=['.', ','],
            special_chars_award_id=['/', '.', '-']
        )
        self.assertEqual(expected, obtained)

    def test_award_groups(self):
        expected = [
            {
                "award-id": ["2019JJ40269"],
                "funding-source": ["Natural Science Foundation of Hunan Province"]
            },
            {
                "award-id": ["2020CFB547"],
                "funding-source": ["Hubei Provincial Natural Science Foundation of China"]
            }
        ]
        obtained = self.funding.award_groups
        self.assertEqual(expected, obtained)

    def test_funding_sources(self):
        expected = [
            "Natural Science Foundation of Hunan Province",
            "Hubei Provincial Natural Science Foundation of China"
        ]
        obtained = self.funding.funding_sources
        self.assertEqual(expected, obtained)

    def test_funding_statement(self):
        expected = "Natural Science Foundation of Hunan Province Grant No. 2019JJ40269 Hubei Provincial Natural Science " \
                   "Foundation of China Grant No. 2020CFB547"
        obtained = self.funding.funding_statement
        self.assertEqual(expected, obtained)

    def test_principal_award_recipients(self):
        expected = [
            "Stanford",
            "Berkeley"
        ]
        obtained = self.funding.principal_award_recipients
        self.assertEqual(expected, obtained)

    def test_principal_investigators(self):
        expected = [
            {
                "given-names": 'Sharon R.',
                "surname": 'Kaufman'
            },
            {
                "given-names": 'João',
                "surname": 'Silva'
            }
        ]
        obtained = self.funding.principal_investigators
        self.assertEqual(expected, obtained)

    def test_ack(self):
        self.maxDiff = None
        expected = [
            {
                "title": 'Acknowledgments',
                "text": 'Federal University of Rio de Janeiro (UFRJ), School of Medicine, Department of Surgery and '
                        'Anesthesiology, RJ, Brazil, provided important support for this research. This study was '
                        'funded by the Hospital Municipal Conde Modesto Leal, Center of Diagnostic and Treatment ('
                        'CDT), Municipal Secretariat of Health, Maricá, RJ, Brazil. This study was presented as a '
                        'poster presentation at the Brazilian Congress of Anesthesiology CBA Annual Meeting 10-14 '
                        'November 2018, Belém do Pará, Brazil.'
            }
        ]
        obtained = self.funding.ack
        self.assertEqual(expected, obtained)
