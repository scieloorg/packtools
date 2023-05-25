from unittest import TestCase

from lxml import etree as ET

from packtools.sps.models.article_abstract import Abstract
from packtools.sps.utils import xml_utils


class AbstractTest(TestCase):
    maxDiff = None

    def test_main_abstract_with_title(self):
        xml = """
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
        data = ET.fromstring(xml)
        obtained = Abstract(data).main_abstract_with_title(subtag=False)
        # import ipdb; ipdb.set_trace()
        expected = {
            "lang": "en",
            "title": "Abstract",
            "sections": {
                "Objective:": "objective",
                "Method:": "method",
                "Results:": "results",
                "Conclusion:": "conclusion",
            },
        }

        self.assertEqual(obtained, expected)

    def test_main_abstract_without_title(self):
        xml = """
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
        data = ET.fromstring(xml)
        obtained = Abstract(data).main_abstract_without_title(subtag=False)

        expected = {"en": "objective method results conclusion"}

        self.assertEqual(obtained, expected)

    def test_sub_article_abstract_with_title(self):
        xml = """
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
        data = ET.fromstring(xml)
        obtained = Abstract(data).sub_article_abstract_with_title(subtag=False)

        expected = {
            "lang": "pt",
            "title": "RESUMO",
            "sections": {
                "Objetivo:": "objetivo",
                "Método:": "metodo",
                "Resultados:": "resultados",
                "Conclusão:": "conclusão",
            },
        }

        self.assertEqual(obtained, expected)

    def test_sub_article_abstract_without_title(self):
        xml = """
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
        data = ET.fromstring(xml)
        obtained = Abstract(data).sub_article_abstract_without_title(subtag=False)

        expected = {"pt": "objetivo metodo resultados conclusão"}

        self.assertEqual(obtained, expected)

    def test_trans_abstract_with_title(self):
        xml = """
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
        data = ET.fromstring(xml)
        obtained = Abstract(data).trans_abstract_with_title(subtag=False)

        expected = {
            "lang": "es",
            "title": "RESUMEN",
            "sections": {
                "Objetivo:": "objetivo",
                "Método:": "metodo",
                "Resultados:": "resultados",
                "Conclusión:": "conclusion",
            },
        }

        self.assertEqual(obtained, expected)

    def test_trans_abstract_without_title(self):
        xml = """
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
        data = ET.fromstring(xml)
        obtained = Abstract(data).trans_abstract_without_title(subtag=False)

        expected = {"es": "objetivo metodo resultados conclusion"}

        self.assertEqual(obtained, expected)

    def test_abstracts_with_title(self):
        xml = """
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
        data = ET.fromstring(xml)
        obtained = Abstract(data).abstracts_with_title(subtag=True)

        expected = [
            {
                "lang": "en",
                "title": "Abstract",
                "sections": {
                    "Objective:": "objective",
                    "Method:": "method",
                    "Results:": "results",
                    "Conclusion:": "conclusion",
                },
            },
            {
                "lang": "es",
                "title": "RESUMEN",
                "sections": {
                    "Objetivo:": "objetivo",
                    "Método:": "metodo",
                    "Resultados:": "resultados",
                    "Conclusión:": "conclusion",
                },
            },
            {
                "lang": "pt",
                "title": "RESUMO",
                "sections": {
                    "Objetivo:": "objetivo",
                    "Método:": "metodo",
                    "Resultados:": "resultados",
                    "Conclusão:": "conclusão",
                },
            },
        ]

        self.assertEqual(obtained, expected)

    def test_abstracts_without_title(self):
        xml = """
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
        data = ET.fromstring(xml)
        obtained = Abstract(data).abstracts_without_title(subtag=False)

        expected = {
            "en": "objective method results conclusion",
            "pt": "objetivo metodo resultados conclusão",
            "es": "objetivo metodo resultados conclusion",
        }

        self.assertEqual(obtained, expected)

    def test_without_trans_abstract_with_title(self):
        xml = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            </article-meta>
            </front>
            </article>
            """
        data = ET.fromstring(xml)
        obtained = Abstract(data).trans_abstract_with_title(subtag=False)

        expected = None

        self.assertEqual(obtained, expected)

    def test_main_abstract_with_title_and_without_subtags(self):
        xml = """
        <article>
            <front>
                <article-meta>
                    <abstract>
                <title>Abstract</title>
                <sec>
                    <title>Background and objectives:</title>
                    <p>Pain is one of the most common reason for seeking medical care. This study
                        aimed to analyze patients with chronic pain in Maricá, Rio de Janeiro State,
                        Brazil.</p>
                </sec>
                <sec>
                    <title>Methods:</title>
                    <p>A transversal retrospective study with 200 patients, who were treated in
                        ambulatory care in a public hospital from June 2014 to December 2015. The
                        variables considered were: pain intensity, type of pain, anatomical
                        location, diagnosis and treatment. The data were statistically analyzed, the
                        Fisher's exact test was applied, and the probability <italic>p</italic> was
                        significant when &#x2264;0.05.</p>
                </sec>
            </abstract>
                </article-meta>
            </front>
        </article>
        """
        xml = ET.fromstring(xml)
        obtained = Abstract(xmltree=xml).main_abstract_with_title(subtag=False)

        expected = {
            "lang": None,
            "title": "Abstract",
            "sections": {
                "Background and objectives:": "Pain is one of the most common reason for seeking medical care. This study\n                        aimed to analyze patients with chronic pain in Maricá, Rio de Janeiro State,\n                        Brazil.",
                "Methods:": "A transversal retrospective study with 200 patients, who were treated in\n                        ambulatory care in a public hospital from June 2014 to December 2015. The\n                        variables considered were: pain intensity, type of pain, anatomical\n                        location, diagnosis and treatment. The data were statistically analyzed, the\n                        Fisher's exact test was applied, and the probability p was\n                        significant when ≤0.05.",
            },
        }

        self.assertEqual(obtained, expected)

    def test_main_abstract_with_title_and_subtags(self):
        xml = """
        <article>
            <front>
                <article-meta>
                    <abstract>
                <title>Abstract</title>
                <sec>
                    <title>Background and objectives:</title>
                    <p>Pain is one of the most common reason for seeking medical care. This study
                        aimed to analyze patients with chronic pain <italic>in</italic> Maricá, Rio de Janeiro State,
                        Brazil.</p>
                </sec>
                <sec>
                    <title>Methods:</title>
                    <p>A transversal retrospective study with 200 patients, who were treated in
                        ambulatory care in a public hospital from June 2014 to December 2015. The
                        variables considered were: pain intensity, type of pain, anatomical
                        location, diagnosis and treatment. The data were statistically analyzed, the
                        Fisher's exact test was applied, and the probability <italic>p</italic> was
                        significant when &#x2264;0.05.</p>
                </sec>
            </abstract>
                </article-meta>
            </front>
        </article>
        """
        xml = ET.fromstring(xml)
        obtained = Abstract(xmltree=xml).main_abstract_with_title(subtag=True)

        expected = {
            "lang": None,
            "title": "Abstract",
            "sections": {
                "Background and objectives:": "Pain is one of the most common reason for seeking medical care. This study\n                        aimed to analyze patients with chronic pain <italic>in</italic> Maricá, Rio de Janeiro State,\n                        Brazil.",
                "Methods:": "A transversal retrospective study with 200 patients, who were treated in\n                        ambulatory care in a public hospital from June 2014 to December 2015. The\n                        variables considered were: pain intensity, type of pain, anatomical\n                        location, diagnosis and treatment. The data were statistically analyzed, the\n                        Fisher's exact test was applied, and the probability <italic>p</italic> was\n                        significant when ≤0.05.",
            },
        }

        self.assertEqual(obtained, expected)