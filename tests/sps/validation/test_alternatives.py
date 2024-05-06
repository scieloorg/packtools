from lxml import etree
import unittest

from packtools.sps.validation.alternatives import AlternativesValidation


class AlternativesValidationTest(unittest.TestCase):
    def test_validation_success(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
            <body>
            <table-wrap id="t5">
            <label>Tabela 5</label>
            <caption>
            <title>Alíquota menor para prestadores</title>
            </caption>
            <alternatives>
            <graphic xlink:href="nomedaimagemdatabela.svg"/>
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
            <tr><td>De R$ 225.000,01 a RS 450.000,00</td>
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
            </alternatives>
            <table-wrap-foot>
            <fn id="TFN1">
            <p>A informação de alíquota do anexo II é significativa</p>
            </fn>
            </table-wrap-foot>
            </table-wrap>
            </body>
            <sub-article article-type="translation" xml:lang="en" id="TRen">
            <body>
            <table-wrap id="t5">
            <label>Tabela 5</label>
            <caption>
            <title>Alíquota menor para prestadores</title>
            </caption>
            <alternatives>
            <graphic xlink:href="nomedaimagemdatabela.svg"/>
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
            <tr><td>De R$ 225.000,01 a RS 450.000,00</td>
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
            </alternatives>
            <table-wrap-foot>
            <fn id="TFN1">
            <p>A informação de alíquota do anexo II é significativa</p>
            </fn>
            </table-wrap-foot>
            </table-wrap>
            </body>
            </sub-article>
            </article>
            """
        )
        obtained = list(AlternativesValidation(self.xmltree).validation())
        expected = []
        self.assertListEqual(obtained, expected)

    def test_validation_fail(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
            <body>
            <table-wrap id="t5">
            <label>Tabela 5</label>
            <caption>
            <title>Alíquota menor para prestadores</title>
            </caption>
            <alternatives>
            <p>
            altenativa
            </p>
            </alternatives>
            <table-wrap-foot>
            <fn id="TFN1">
            <p>A informação de alíquota do anexo II é significativa</p>
            </fn>
            </table-wrap-foot>
            </table-wrap>
            </body>
            <sub-article article-type="translation" xml:lang="en" id="TRen">
            <body>
            <table-wrap id="t5">
            <label>Tabela 5</label>
            <caption>
            <title>Alíquota menor para prestadores</title>
            </caption>
            <alternatives>
            <title />
            <abstract />
            </alternatives>
            <table-wrap-foot>
            <fn id="TFN1">
            <p>A informação de alíquota do anexo II é significativa</p>
            </fn>
            </table-wrap-foot>
            </table-wrap>
            </body>
            </sub-article>
            </article>
            """
        )
        obtained = list(AlternativesValidation(self.xmltree).validation())
        expected = [
            {
                'title': 'Alternatives validation',
                'parent': 'article',
                'parent_id': None,
                'item': 'table-wrap',
                'sub_item': 'alternative',
                'validation_type': 'match',
                'expected_value': ['graphic', 'table', 'inline-graphic', 'media', 'supplementary-material'],
                'got_value': ['p'],
                'response': 'ERROR',
                'message': "Got ['p'], expected ['graphic', 'table', 'inline-graphic', 'media', 'supplementary-material']",
                'advice': "Provide child tags according to the list: ['graphic', 'table', 'inline-graphic', 'media', 'supplementary-material']",
                'data': {
                    'alternative_children': ['p'],
                    'alternative_parent': 'table-wrap',
                    'parent': 'article',
                    'parent_id': None
                }
            },
            {
                'title': 'Alternatives validation',
                'parent': 'sub-article',
                'parent_id': 'TRen',
                'item': 'table-wrap',
                'sub_item': 'alternative',
                'validation_type': 'match',
                'expected_value': ['graphic', 'table', 'inline-graphic', 'media', 'supplementary-material'],
                'got_value': ['title', 'abstract'],
                'response': 'ERROR',
                'message': "Got ['title', 'abstract'], expected ['graphic', 'table', 'inline-graphic', 'media', 'supplementary-material']",
                'advice': "Provide child tags according to the list: ['graphic', 'table', 'inline-graphic', 'media', 'supplementary-material']",
                'data': {
                    'alternative_children': ['title', 'abstract'],
                    'alternative_parent': 'table-wrap',
                    'parent': 'sub-article',
                    'parent_id': 'TRen'
                }
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])


if __name__ == '__main__':
    unittest.main()
