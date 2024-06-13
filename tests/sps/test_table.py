from unittest import TestCase
from packtools.sps.utils import xml_utils

from lxml import etree

from packtools.sps.models.tables import Table


class TablesTest(TestCase):
    def test_extract_tables_with_group(self):
        xml = ("""
            <article>
                <front>
                    <article-meta>
                        <table-wrap-group id="t01">
                            <table-wrap id="t01">
                                <label>Table. </label>
                                <caption>
                                    <title>Proportion of correct HIV/AIDS knowledge responses as reported by the men who have sex with men, the difficulty and discrimination parameters for each item, estimated by Item Response Theory. Brazil, 2008-2009. (N = 3,746)</title>
                                </caption>
                                <table frame="hsides" rules="groups">
                                    <colgroup width="25%">
                                        <col width="60%"/>
                                        <col width="10%"/>
                                        <col width="10%"/>
                                        <col width="10%"/>
                                    </colgroup>
                                    <thead>
                                        <tr>
                                            <th style="font-weight:normal" align="left">Item</th>
                                            <th style="font-weight:normal">% Correct response</th>
                                            <th style="font-weight:normal">Difficulty (<italic>b</italic>
                                                <sub>
                                                    <italic>i</italic>
                                                </sub>)</th>
                                            <th style="font-weight:normal">Discrimination (<italic>a</italic>
                                                <sub>
                                                    <italic>i</italic>
                                                </sub>)</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>1. The risk of transmitting HIV is small if one follows the treatment correctly.</td>
                                            <td align="center">35.5</td>
                                            <td align="center">14.45</td>
                                            <td align="center">0.04</td>
                                        </tr>
                                        <tr>
                                            <td>2. People are using less condoms because of AIDS treatment.</td>
                                            <td align="center">34.5</td>
                                            <td align="center">14.23</td>
                                            <td align="center">0.04</td>
                                        </tr>
                                        <tr>
                                            <td>3. A person can get the AIDS virus by using public toilets.</td>
                                            <td align="center">78.1</td>
                                            <td align="center">3.72</td>
                                            <td align="center">0.95</td>
                                        </tr>
                                        <tr>
                                            <td>4. A person can get the AIDS virus through insect bites.</td>
                                            <td align="center">75.5</td>
                                            <td align="center">3.70</td>
                                            <td align="center">0.72</td>
                                        </tr>
                                        <tr>
                                            <td>5. A person can become infected by sharing eating utensils, cups or food.</td>
                                            <td align="center">85.7</td>
                                            <td align="center">3.28</td>
                                            <td align="center">1.01</td>
                                        </tr>
                                        <tr>
                                            <td>6. The risk of HIV + mothers infecting their babies is small if she receives treatment in pregnancy and childbirth.</td>
                                            <td align="center">75.8</td>
                                            <td align="center">2.70</td>
                                            <td align="center">0.32</td>
                                        </tr>
                                        <tr>
                                            <td>7. The risk of HIV infection can be reduced if you have relations only with an uninfected partner.</td>
                                            <td align="center">72.6</td>
                                            <td align="center">2.03</td>
                                            <td align="center">0.20</td>
                                        </tr>
                                        <tr>
                                            <td>8. A healthy person can be infected with the AIDS virus.</td>
                                            <td align="center">94.1</td>
                                            <td align="center">1.61</td>
                                            <td align="center">0.59</td>
                                        </tr>
                                        <tr>
                                            <td>9. A person can get the virus from sharing a syringe or needle.</td>
                                            <td align="center">96.9</td>
                                            <td align="center">1.51</td>
                                            <td align="center">0.78</td>
                                        </tr>
                                        <tr>
                                            <td>10. Anyone can get the AIDS virus if condoms are not used.</td>
                                            <td align="center">98.5</td>
                                            <td align="center">1.27</td>
                                            <td align="center">0.95</td>
                                        </tr>
                                    </tbody>
                                </table>
                                <table-wrap-foot>
                                    <p>
                                        <italic>b</italic>
                                        <sub>
                                            <italic>i</italic>
                                        </sub>: Difficulty parameter of each item; <italic>a</italic>
                                        <sub>
                                            <italic>i</italic>
                                        </sub>: Discrimination parameter of each item</p>
                                </table-wrap-foot>
                            </table-wrap>
                        </table-wrap-group>
                    </article-meta>
                </front>
            </article>
        """)

        xml = xml_utils.get_xml_tree(xml)
        extract = Table(xml).extract_table(subtag=False)
        expected_output = [
            {
            'table_group_id': 't01', 
            'tables': [
                {
                'id': 't01', 
                'label': 'Table. ', 
                'title': 'Proportion of correct HIV/AIDS knowledge responses as reported by the men who have sex with men, the difficulty and discrimination parameters for each item, estimated by Item Response Theory. Brazil, 2008-2009. (N = 3,746)', 
                'table': '<colgroup width="25%"><col width="60%"/><col width="10%"/><col width="10%"/><col width="10%"/></colgroup><thead><tr><th style="font-weight:normal" align="left">Item</th><th style="font-weight:normal">% Correct response</th><th style="font-weight:normal">Difficulty (<italic>b</italic>\n                                                <sub><italic>i</italic></sub>)</th><th style="font-weight:normal">Discrimination (<italic>a</italic>\n                                                <sub><italic>i</italic></sub>)</th></tr></thead><tbody><tr><td>1. The risk of transmitting HIV is small if one follows the treatment correctly.</td><td align="center">35.5</td><td align="center">14.45</td><td align="center">0.04</td></tr><tr><td>2. People are using less condoms because of AIDS treatment.</td><td align="center">34.5</td><td align="center">14.23</td><td align="center">0.04</td></tr><tr><td>3. A person can get the AIDS virus by using public toilets.</td><td align="center">78.1</td><td align="center">3.72</td><td align="center">0.95</td></tr><tr><td>4. A person can get the AIDS virus through insect bites.</td><td align="center">75.5</td><td align="center">3.70</td><td align="center">0.72</td></tr><tr><td>5. A person can become infected by sharing eating utensils, cups or food.</td><td align="center">85.7</td><td align="center">3.28</td><td align="center">1.01</td></tr><tr><td>6. The risk of HIV + mothers infecting their babies is small if she receives treatment in pregnancy and childbirth.</td><td align="center">75.8</td><td align="center">2.70</td><td align="center">0.32</td></tr><tr><td>7. The risk of HIV infection can be reduced if you have relations only with an uninfected partner.</td><td align="center">72.6</td><td align="center">2.03</td><td align="center">0.20</td></tr><tr><td>8. A healthy person can be infected with the AIDS virus.</td><td align="center">94.1</td><td align="center">1.61</td><td align="center">0.59</td></tr><tr><td>9. A person can get the virus from sharing a syringe or needle.</td><td align="center">96.9</td><td align="center">1.51</td><td align="center">0.78</td></tr><tr><td>10. Anyone can get the AIDS virus if condoms are not used.</td><td align="center">98.5</td><td align="center">1.27</td><td align="center">0.95</td></tr></tbody>', 'wrap-foot': 'bi: Difficulty parameter of each item; ai: Discrimination parameter of each item'
                }
                ]
            }
        ]

        self.assertEqual(extract, expected_output)

    def test_extract_tables_without_group(self):
        xml =("""
            <article>
                <front>
                    <article-meta>
                        <table-wrap id="t5">
                            <label>Tabela 5</label>
                            <caption>
                                <title>Alíquota menor para prestadores</title>
                            </caption>
                            <table>
                                <thead>
                                <tr>
                                    <th rowspan="3">Proposta de Novas Tabelas - 2016</th>
                                </tr>
                                <tr>
                                    <th>Receita Bruta em 12 Meses - em R$</th>
                                    <th>Anexo I - Comércio</th>
                                    <th>Anexo II Indústria</th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr>
                                    <td>De R$ 225.000,01 a RS 450.000,00</td>
                                    <td>4,00%</td>
                                    <td>4,50%</td>
                                </tr>
                                <tr>
                                    <td>De R$ 450.000,01 a R$ 900.000,00</td>
                                    <td>8,25%</td>
                                    <td>8,00%</td>
                                </tr>
                                <tr>
                                    <td>De R$ 900.000,01 a R$ 1.800.000,00</td>
                                    <td>11,25%</td>
                                    <td>12,25%</td>
                                </tr>
                                </tbody>
                            </table>
                            <table-wrap-foot>
                                <fn id="TFN1">
                                <p>A informação de alíquota do anexo II é significativa</p>
                                </fn>
                            </table-wrap-foot>
                        </table-wrap>
                    </article-meta>
                </front>
            </article>
        """)
        xml = xml_utils.get_xml_tree(xml)
        extract = Table(xml).extract_table(subtag=False)

        expected_output = {
            'tables': [
                {
                'id': 't5', 
                'label': 'Tabela 5', 
                'title': 'Alíquota menor para prestadores', 
                'table': '<thead><tr><th rowspan="3">Proposta de Novas Tabelas - 2016</th></tr><tr><th>Receita Bruta em 12 Meses - em R$</th><th>Anexo I - Comércio</th><th>Anexo II Indústria</th></tr></thead><tbody><tr><td>De R$ 225.000,01 a RS 450.000,00</td><td>4,00%</td><td>4,50%</td></tr><tr><td>De R$ 450.000,01 a R$ 900.000,00</td><td>8,25%</td><td>8,00%</td></tr><tr><td>De R$ 900.000,01 a R$ 1.800.000,00</td><td>11,25%</td><td>12,25%</td></tr></tbody>', 'wrap-foot': 'A informação de alíquota do anexo II é significativa'
                }
                ]
            }

        self.assertEqual(extract, expected_output)