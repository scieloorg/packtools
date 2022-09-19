from unittest import TestCase

from packtools.sps.utils import xml_utils

from packtools.sps.models.article_errata import ArticleWithErrataNotes, Footnote


def generate_xmltree(erratum1, erratum2=None):
    xml = """
    <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
        <front>
            <article-meta></article-meta>
        </front>
        <body>
        </body>
        <back>
        {0}
        {1}
        </back>
    </article>
    """
    return xml_utils.get_xml_tree(xml.format(erratum1, erratum2))


class ArticleErrataTest(TestCase):
    def test_footnote_presence(self):
        data = """
        <fn-group>
            <fn fn-type="other">
                <label>Additions and Corrections</label>
                <p>On page 100, where it was read:</p>
                <p>“Joao S. Costa”</p>
                <p>Now reads:</p>
                <p>“João Silva Costa”</p>
            </fn>
        </fn-group>
        """
        xmltree = generate_xmltree(data)

        obtained = ArticleWithErrataNotes(xmltree).footnotes().pop()

        self.assertIsInstance(obtained, Footnote)


    def test_footnote_label(self):
        data = """
        <fn-group>
            <fn fn-type="other">
                <label>Additions and Corrections</label>
                <p>On page 100, where it was read:</p>
                <p>“Joao S. Costa”</p>
                <p>Now reads:</p>
                <p>“João Silva Costa”</p>
            </fn>
        </fn-group>
        """
        xmltree = generate_xmltree(data)

        expected_label = 'Additions and Corrections'
        fn = ArticleWithErrataNotes(xmltree).footnotes().pop()
        obtained_label = fn.label

        self.assertEqual(expected_label, obtained_label)


    def test_footnote_text(self):
        data = """
        <fn-group>
            <fn fn-type="other">
                <label>Additions and Corrections</label>
                <p>On page 100, where it was read:</p>
                <p>“Joao S. Costa”</p>
                <p>Now reads:</p>
                <p>“João Silva Costa”</p>
            </fn>
        </fn-group>
        """
        xmltree = generate_xmltree(data)

        expected_text = 'Additions and Corrections\nOn page 100, where it was read:\n“Joao S. Costa”\nNow reads:\n“João Silva Costa”'
        fn = ArticleWithErrataNotes(xmltree).footnotes().pop()
        obtained_text = fn.text

        self.assertEqual(expected_text, obtained_text)
    

    def test_footnote_with_table(self):
        data = """
        <fn-group>
            <fn fn-type="other">
                <label>Corrections</label>
                <p>Article “Risk factors for site complications of intravenous therapy in children and adolescents with cancer”, with number of DOI: <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1590/0034-7167-2019-0471">https://doi.org/10.1590/0034-7167-2019-0471</ext-link>, published in the journal Revista Brasileira de Enfermagem, 73(4):e20190471, on page 3:</p>
                <p>Where to read:</p>
                <p>In the multiple analysis, logistic regression was performed and modeling was achieved when all variables presented p ≤ 0.05.</p>
                <p>Read:</p>
                <p>In the multiple analysis, Poisson regression with robust variance was performed and modeling was achieved when all variables presented p ≤ 0.05.</p>
                <p>On page 6, <xref ref-type="table" rid="t11">Table 5</xref>, where it read:</p>
                <p>
                    <table-wrap id="t11">
                        <label>Tabela 5</label>
                        <caption>
                            <title>Regressão Logística das variáveis relacionadas à Terapia Intravenosa prévia associadas à ocorrência de complicação em crianças e adolescentes admitidos em unidades de clínica oncológica pediátrica, Feira de Santana, Bahia, Brasil, 2015 - 2016</title>
                        </caption>
                        <table frame="hsides" rules="groups">
                            <colgroup>
                                <col width="40%"/>
                                <col width="20%"/>
                                <col width="20%"/>
                                <col width="20%"/>
                            </colgroup>
                            <thead>
                                <tr>
                                    <th align="left" rowspan="2">Variables</th>
                                    <th align="center" colspan="2">Complicações da Terapia Intravenosa</th>
                                    <th align="center" rowspan="2"><italic>p</italic><break/>value</th>
                                </tr>
                                <tr>
                                    <th align="center">RR</th>
                                    <th align="center">IC</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td align="left">Terapia Intravenosa periférica prolongada</td>
                                    <td align="center">3.44</td>
                                    <td align="center">1.58 - 7.50</td>
                                    <td align="center">0.002</td>
                                </tr>
                                <tr>
                                    <td align="left">Antecedente de complicações</td>
                                    <td align="center">4.22</td>
                                    <td align="center">2.84 - 6.26</td>
                                    <td align="center">&lt;0.001</td>
                                </tr>
                                <tr>
                                    <td align="left">Utilização de medicamentos não irritantes/vesicantes</td>
                                    <td align="center">1.99</td>
                                    <td align="center">1.26 - 3.15</td>
                                    <td align="center">0.003</td>
                                </tr>
                                <tr>
                                    <td align="left">Utilização de solução vesicante</td>
                                    <td align="center">2.65</td>
                                    <td align="center">1.69 - 4.17</td>
                                    <td align="center">&lt;0.001</td>
                                </tr>
                            </tbody>
                        </table>
                    </table-wrap>
                </p>
                <p>Read:</p>
                <p>
                    <table-wrap id="t12">
                        <label>Table 5</label>
                        <caption>
                            <title>Poisson Regression of variables related to previous Intravenous Therapy associated with the occurrence of complications in children and adolescents admitted to pediatric oncology clinic units in the interior of Bahia, Brazil, Apr 2015 - Dec 2016</title>
                        </caption>
                        <table frame="hsides" rules="groups">
                            <colgroup>
                                <col width="40%"/>
                                <col width="20%"/>
                                <col width="20%"/>
                                <col width="20%"/>
                            </colgroup>
                            <thead>
                                <tr>
                                    <th align="left" rowspan="2">Variables</th>
                                    <th align="center" colspan="2">Intravenous Therapy Complications</th>
                                    <th align="center" rowspan="2"><italic>p</italic><break/>value</th>
                                </tr>
                                <tr>
                                    <th align="center">RR</th>
                                    <th align="center">CI</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td align="left">Prolonged peripheral IVT</td>
                                    <td align="center">3.44</td>
                                    <td align="center">1.58 - 7.50</td>
                                    <td align="center">0.002</td>
                                </tr>
                                <tr>
                                    <td align="left">Hystory of complications</td>
                                    <td align="center">4.22</td>
                                    <td align="center">2.84 - 6.26</td>
                                    <td align="center">&lt;0.001</td>
                                </tr>
                                <tr>
                                    <td align="left">Use of non-irritating/vesicant medication</td>
                                    <td align="center">1.99</td>
                                    <td align="center">1.26 - 3.15</td>
                                    <td align="center">0.003</td>
                                </tr>
                                <tr>
                                    <td align="left">Use of vesicant solution</td>
                                    <td align="center">2.65</td>
                                    <td align="center">1.69 - 4.17</td>
                                    <td align="center">&lt;00001</td>
                                </tr>
                            </tbody>
                        </table>
                    </table-wrap>
                </p>
            </fn>
        </fn-group>
        """
        xmltree = generate_xmltree(data)

        expected_label = 'Corrections'
        expected_text = 'Corrections\nArticle “Risk factors for site complications of intravenous therapy in children and adolescents with cancer”, with number of DOI: \nhttps://doi.org/10.1590/0034-7167-2019-0471\n, published in the journal Revista Brasileira de Enfermagem, 73(4):e20190471, on page 3:\nWhere to read:\nIn the multiple analysis, logistic regression was performed and modeling was achieved when all variables presented p ≤ 0.05.\nRead:\nIn the multiple analysis, Poisson regression with robust variance was performed and modeling was achieved when all variables presented p ≤ 0.05.\nOn page 6, \nTable 5\n, where it read:\nTabela 5\nRegressão Logística das variáveis relacionadas à Terapia Intravenosa prévia associadas à ocorrência de complicação em crianças e adolescentes admitidos em unidades de clínica oncológica pediátrica, Feira de Santana, Bahia, Brasil, 2015 - 2016\nVariables\nComplicações da Terapia Intravenosa\np\nvalue\nRR\nIC\nTerapia Intravenosa periférica prolongada\n3.44\n1.58 - 7.50\n0.002\nAntecedente de complicações\n4.22\n2.84 - 6.26\n<0.001\nUtilização de medicamentos não irritantes/vesicantes\n1.99\n1.26 - 3.15\n0.003\nUtilização de solução vesicante\n2.65\n1.69 - 4.17\n<0.001\nRead:\nTable 5\nPoisson Regression of variables related to previous Intravenous Therapy associated with the occurrence of complications in children and adolescents admitted to pediatric oncology clinic units in the interior of Bahia, Brazil, Apr 2015 - Dec 2016\nVariables\nIntravenous Therapy Complications\np\nvalue\nRR\nCI\nProlonged peripheral IVT\n3.44\n1.58 - 7.50\n0.002\nHystory of complications\n4.22\n2.84 - 6.26\n<0.001\nUse of non-irritating/vesicant medication\n1.99\n1.26 - 3.15\n0.003\nUse of vesicant solution\n2.65\n1.69 - 4.17\n<00001'

        obtained = ArticleWithErrataNotes(xmltree).footnotes().pop()

        self.assertEqual(expected_label, obtained.label)
        self.assertEqual(expected_text, obtained.text)


    def test_two_footnotes(self):
        data1 = """
        <fn-group>
            <fn fn-type="other">
                <label>Erratum number 1</label>
                <p>On page 10, where it was read:</p>
                <p>“Joao S. Costa”</p>
                <p>Now reads:</p>
                <p>“João Silva Costa”</p>
            </fn>
        </fn-group>
        """

        data2 = """
        <fn-group>
            <fn fn-type="other">
                <label>Erratum number 2</label>
                <p>On page 23, where it was read:</p>
                <p>“Joao S. Costa”</p>
                <p>Now reads:</p>
                <p>“SciELO Research Group”</p>
            </fn>
        </fn-group>
        """
        xmltree = generate_xmltree(data1, data2)

        expected_labels = ['Erratum number 1', 'Erratum number 2']
        obtained_labels = [ae.label for ae in ArticleWithErrataNotes(xmltree).footnotes()]

        expected_texts = ['Erratum number 1\nOn page 10, where it was read:\n“Joao S. Costa”\nNow reads:\n“João Silva Costa”', 'Erratum number 2\nOn page 23, where it was read:\n“Joao S. Costa”\nNow reads:\n“SciELO Research Group”']
        obtained_texts = [ae.text for ae in ArticleWithErrataNotes(xmltree).footnotes()]

        self.assertListEqual(expected_labels, obtained_labels)
        self.assertListEqual(expected_texts, obtained_texts)
