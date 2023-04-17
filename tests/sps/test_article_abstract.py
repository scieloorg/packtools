from unittest import TestCase

from lxml import etree as ET

from packtools.sps.models.article_abstract import Abstract


class AbstractTest(TestCase):
    maxDiff = None

    def test_main_abstract_with_tags(self):
        xml = (
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <abstract>
                <title>Abstract</title>
                    <sec>
                    <title>Objective:</title>
                        <p>objective</p>
                    </sec>
                    <sec>
                    <title>Method:</title>
                        <p>method</p>
                    </sec>
                    <sec>
                    <title>Results:</title>
                        <p>results</p>
                    </sec>
                    <sec>
                    <title>Conclusion:</title>
                        <p>conclusion</p>
                    </sec>
            </abstract>
            </article-meta>
            </front>
            </article>
            """
        )
        data = ET.fromstring(xml)
        obtained = Abstract(data).main_abstract_with_tags

        expected = {
            "lang": "en",
            "title": "Abstract",
            "sections": {
                "Objective:": "objective",
                "Method:": "method",
                "Results:": "results",
                "Conclusion:": "conclusion"
            }
        }

        self.assertEqual(obtained, expected)

    def test_main_abstract_without_tags(self):
        xml = (
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <abstract>
                <title>Abstract</title>
                    <sec>
                    <title>Objective:</title>
                        <p>objective</p>
                    </sec>
                    <sec>
                    <title>Method:</title>
                        <p>method</p>
                    </sec>
                    <sec>
                    <title>Results:</title>
                        <p>results</p>
                    </sec>
                    <sec>
                    <title>Conclusion:</title>
                        <p>conclusion</p>
                    </sec>
            </abstract>
            </article-meta>
            </front>
            </article>
            """
        )
        data = ET.fromstring(xml)
        obtained = Abstract(data).main_abstract_without_tags

        expected = {'en': 'objective method results conclusion'}

        self.assertEqual(obtained, expected)

    def test_sub_article_abstract_with_tags(self):
        xml = (
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
                <sub-article article-type="translation" id="s1" xml:lang="pt">
                    <front-stub>
                        <article-id pub-id-type="doi">10.1590/1980-220X-REEUSP-2021-0569pt</article-id>
                        <abstract>
                            <title>RESUMO</title>
                            <sec>
                                <title>Objetivo:</title>
                                <p>objetivo</p>
                            </sec>
                            <sec>
                                <title>Método:</title>
                                <p>metodo</p>
                            </sec>
                            <sec>
                                <title>Resultados:</title>
                                <p>resultados</p>
                            </sec>
                            <sec>
                                <title>Conclusão:</title>
                                <p>conclusão</p>
                            </sec>
                        </abstract>
                    </front-stub>
                </sub-article>
            </article>
            """
        )
        data = ET.fromstring(xml)
        obtained = Abstract(data).sub_article_abstract_with_tags

        expected = {
            "title": "RESUMO",
            "lang": "pt",
            "Objetivo:": "objetivo",
            "Método:": "metodo",
            "Resultados:": "resultados",
            "Conclusão:": "conclusão"

        }

        self.assertEqual(obtained, expected)

    def test_sub_article_abstract_without_tags(self):
        xml = (
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
                <sub-article article-type="translation" id="s1" xml:lang="pt">
                    <front-stub>
                        <article-id pub-id-type="doi">10.1590/1980-220X-REEUSP-2021-0569pt</article-id>
                        <abstract>
                            <title>RESUMO</title>
                            <sec>
                                <title>Objetivo:</title>
                                <p>objetivo</p>
                            </sec>
                            <sec>
                                <title>Método:</title>
                                <p>metodo</p>
                            </sec>
                            <sec>
                                <title>Resultados:</title>
                                <p>resultados</p>
                            </sec>
                            <sec>
                                <title>Conclusão:</title>
                                <p>conclusão</p>
                            </sec>
                        </abstract>
                    </front-stub>
                </sub-article>
            </article>
            """
        )
        data = ET.fromstring(xml)
        obtained = Abstract(data).sub_article_abstract_without_tags

        expected = {'pt': 'objetivo metodo resultados conclusão'}

        self.assertEqual(obtained, expected)

    def test_trans_abstract_with_tags(self):
        xml = (
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <trans-abstract xml:lang="es">
            <title>RESUMEN</title>
            <sec>
            <title>Objetivo:</title>
            <p>objetivo</p>
            </sec>
            <sec>
            <title>Método:</title>
            <p>metodo</p>
            </sec>
            <sec>
            <title>Resultados:</title>
            <p>resultados</p>
            </sec>
            <sec>
            <title>Conclusión:</title>
            <p>conclusion</p>
            </sec>
            </trans-abstract>
            </article-meta>
            </front>
            </article>
            """
        )
        data = ET.fromstring(xml)
        obtained = Abstract(data).trans_abstract_with_tags

        expected = {
            "title": "RESUMEN",
            "lang": "es",
            "Objetivo:": "objetivo",
            "Método:": "metodo",
            "Resultados:": "resultados",
            "Conclusión:": "conclusion"

            }

        self.assertEqual(obtained, expected)

    def test_trans_abstract_without_tags(self):
        xml = (
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <trans-abstract xml:lang="es">
            <title>RESUMEN</title>
            <sec>
            <title>Objetivo:</title>
            <p>objetivo</p>
            </sec>
            <sec>
            <title>Método:</title>
            <p>metodo</p>
            </sec>
            <sec>
            <title>Resultados:</title>
            <p>resultados</p>
            </sec>
            <sec>
            <title>Conclusión:</title>
            <p>conclusion</p>
            </sec>
            </trans-abstract>
            </article-meta>
            </front>
            </article>
            """
        )
        data = ET.fromstring(xml)
        obtained = Abstract(data).trans_abstract_without_tags

        expected = {'es': 'objetivo metodo resultados conclusion'}

        self.assertEqual(obtained, expected)

    def test_abstracts_with_tags(self):
        xml = (
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
                <abstract>
                    <title>Abstract</title>
                        <sec>
                        <title>Objective:</title>
                            <p>objective</p>
                        </sec>
                        <sec>
                        <title>Method:</title>
                            <p>method</p>
                        </sec>
                        <sec>
                        <title>Results:</title>
                            <p>results</p>
                        </sec>
                        <sec>
                        <title>Conclusion:</title>
                            <p>conclusion</p>
                        </sec>
                </abstract>
                    <trans-abstract xml:lang="es">
                    <title>RESUMEN</title>
                    <sec>
                    <title>Objetivo:</title>
                        <p>objetivo</p>
                    </sec>
                    <sec>
                    <title>Método:</title>
                        <p>metodo</p>
                    </sec>
                    <sec>
                    <title>Resultados:</title>
                        <p>resultados</p>
                    </sec>
                    <sec>
                    <title>Conclusión:</title>
                        <p>conclusion</p>
                    </sec>
                </trans-abstract>
            </article-meta>
            </front>
            <sub-article article-type="translation" id="s1" xml:lang="pt">
                    <front-stub>
                        <article-id pub-id-type="doi">10.1590/1980-220X-REEUSP-2021-0569pt</article-id>
                        <abstract>
                            <title>RESUMO</title>
                            <sec>
                                <title>Objetivo:</title>
                                <p>objetivo</p>
                            </sec>
                            <sec>
                                <title>Método:</title>
                                <p>metodo</p>
                            </sec>
                            <sec>
                                <title>Resultados:</title>
                                <p>resultados</p>
                            </sec>
                            <sec>
                                <title>Conclusão:</title>
                                <p>conclusão</p>
                            </sec>
                        </abstract>
                    </front-stub>
                </sub-article>
            </article>
            """
        )
        data = ET.fromstring(xml)
        obtained = Abstract(data).abstracts_with_tags

        expected = [
            {
                "title": "Abstract",
                "lang": "en",
                "Objective:": "objective",
                "Method:": "method",
                "Results:": "results",
                "Conclusion:": "conclusion"
            },
            {
                "title": "RESUMO",
                "lang": "pt",
                "Objetivo:": "objetivo",
                "Método:": "metodo",
                "Resultados:": "resultados",
                "Conclusão:": "conclusão"
            },
            {
                "title": "RESUMEN",
                "lang": "es",
                "Objetivo:": "objetivo",
                "Método:": "metodo",
                "Resultados:": "resultados",
                "Conclusión:": "conclusion"
            }
        ]

        self.assertEqual(obtained, expected)

    def test_abstracts_without_tags(self):
        xml = (
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
                <abstract>
                    <title>Abstract</title>
                        <sec>
                        <title>Objective:</title>
                            <p>objective</p>
                        </sec>
                        <sec>
                        <title>Method:</title>
                            <p>method</p>
                        </sec>
                        <sec>
                        <title>Results:</title>
                            <p>results</p>
                        </sec>
                        <sec>
                        <title>Conclusion:</title>
                            <p>conclusion</p>
                        </sec>
                </abstract>
                    <trans-abstract xml:lang="es">
                    <title>RESUMEN</title>
                    <sec>
                    <title>Objetivo:</title>
                        <p>objetivo</p>
                    </sec>
                    <sec>
                    <title>Método:</title>
                        <p>metodo</p>
                    </sec>
                    <sec>
                    <title>Resultados:</title>
                        <p>resultados</p>
                    </sec>
                    <sec>
                    <title>Conclusión:</title>
                        <p>conclusion</p>
                    </sec>
                </trans-abstract>
            </article-meta>
            </front>
            <sub-article article-type="translation" id="s1" xml:lang="pt">
                    <front-stub>
                        <article-id pub-id-type="doi">10.1590/1980-220X-REEUSP-2021-0569pt</article-id>
                        <abstract>
                            <title>RESUMO</title>
                            <sec>
                                <title>Objetivo:</title>
                                <p>objetivo</p>
                            </sec>
                            <sec>
                                <title>Método:</title>
                                <p>metodo</p>
                            </sec>
                            <sec>
                                <title>Resultados:</title>
                                <p>resultados</p>
                            </sec>
                            <sec>
                                <title>Conclusão:</title>
                                <p>conclusão</p>
                            </sec>
                        </abstract>
                    </front-stub>
                </sub-article>
            </article>
            """
        )
        data = ET.fromstring(xml)
        obtained = Abstract(data).abstracts_without_tags

        expected = {
            'en': 'objective method results conclusion',
            'pt': 'objetivo metodo resultados conclusão',
            'es': 'objetivo metodo resultados conclusion'
        }

        self.assertEqual(obtained, expected)
