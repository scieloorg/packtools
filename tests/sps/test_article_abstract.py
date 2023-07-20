from unittest import TestCase

from lxml import etree as ET

from packtools.sps.models.article_abstract import Abstract


class AbstractTest(TestCase):
    maxDiff = None

    def test_main_abstract_with_tags(self):
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
        obtained = Abstract(data).main_abstract_with_tags

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

    def test_main_abstract_without_tags(self):
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
        obtained = Abstract(data).main_abstract_without_tags

        expected = {"en": "objective method results conclusion"}

        self.assertEqual(obtained, expected)

    def test_sub_article_abstract_with_tags(self):
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
        obtained = Abstract(data).sub_article_abstract_with_tags

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

    def test_sub_article_abstract_without_tags(self):
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
        obtained = Abstract(data).sub_article_abstract_without_tags

        expected = {"pt": "objetivo metodo resultados conclusão"}

        self.assertEqual(obtained, expected)

    def test_trans_abstract_with_tags(self):
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
        obtained = Abstract(data).trans_abstract_with_tags

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

    def test_trans_abstract_without_tags(self):
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
        obtained = Abstract(data).trans_abstract_without_tags

        expected = {"es": "objetivo metodo resultados conclusion"}

        self.assertEqual(obtained, expected)

    def test_abstracts_with_tags(self):
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
        obtained = Abstract(data).abstracts_with_tags

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

    def test_abstracts_without_tags(self):
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
        obtained = Abstract(data).abstracts_without_tags

        expected = {
            "en": "objective method results conclusion",
            "pt": "objetivo metodo resultados conclusão",
            "es": "objetivo metodo resultados conclusion",
        }

        self.assertEqual(obtained, expected)

    def test_without_trans_abstract_with_tags(self):
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
        obtained = Abstract(data).trans_abstract_with_tags

        expected = None

        self.assertEqual(obtained, expected)


class AbstractWithSectionsTest(TestCase):

    def setUp(self):
        self.xmltree = ET.fromstring(
            """
            <article 
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <abstract>
                <title>Abstract</title>
                <sec>
                    <title>Objective</title>
                    <p>To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people.</p>
                </sec>
                <sec>
                    <title>Design</title>
                    <p>Systematic review of 12 controlled <italic>clinical trials</italic> (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials).</p>
                </sec>
            </abstract>
            <trans-abstract xml:lang="pt">
                <title>Resumo</title>
                <sec>
                  <title>Objetivo: </title>
                  <p>avaliar o efeito de intervenção educativa domiciliar de enfermagem na qualidade de vida de cuidadores familiares de idosos sobreviventes de acidente vascular cerebral (AVC). </p>
                </sec>
                <sec>
                  <title>Método: </title>
                  <p>Ensaio Clínico Randomizado... Módulo <italic>Old</italic> (WHOQOL-OLD) em 1 semana, 2 meses e 1 ano após a alta. </p>
                </sec>
            </trans-abstract>
            </article-meta>
            </front>
            <sub-article article-type="translation" xml:lang="es">
                <front-stub>
                    <abstract>
                        <title>Resumen</title>
                        <sec>
                          <title>Objetivo: </title>
                          <p>evaluar el efecto de intervenciones de atención domiciliaria de enfermería sobre la calidad de vida en cuidadores familiares de adultos mayores sobrevivientes de accidentes cerebrovasculares. </p>
                        </sec>
                        <sec>
                          <title>Método: </title>
                          <p>Ensayo Clínico Aleatorizado ... <italic>World Health Organization Quality of Life Assessment</italic> (WHOQOL-BREF) y el módulo <italic>Old</italic>(WHOQOL-OLD) 1semana, 2meses y 1año después del alta. </p>
                        </sec>
                      </abstract>
                </front-stub>
            </sub-article>
            </article>
            """)

    def test_trans_abstract_with_tags(self):
        expected = {
            'lang': 'pt',
            'title': 'Resumo',
            'sections': {
                'Objetivo: ': 'avaliar o efeito de intervenção educativa domiciliar de enfermagem na qualidade de vida de cuidadores familiares de idosos sobreviventes de acidente vascular cerebral (AVC). ',
                'Método: ': 'Ensaio Clínico Randomizado... Módulo <italic>Old</italic> (WHOQOL-OLD) em 1 semana, 2 meses e 1 ano após a alta. ',
        }}
        obtained = Abstract(self.xmltree).trans_abstract_with_tags
        self.assertEqual(obtained, expected)

    def test_trans_abstract_without_tags(self):
        expected = {
            'pt': 'avaliar o efeito de intervenção educativa domiciliar de enfermagem na qualidade de vida de cuidadores familiares de idosos sobreviventes de acidente vascular cerebral (AVC).  Ensaio Clínico Randomizado... Módulo Old (WHOQOL-OLD) em 1 semana, 2 meses e 1 ano após a alta. ',
        }
        obtained = Abstract(self.xmltree).trans_abstract_without_tags
        self.assertEqual(obtained, expected)

    def test__get_abstract_by_lang_returns_all(self):
        expected = {
            'en': {
                'title': 'Abstract',
                'sections': [{
                    'title': 'Objective',
                    'p': 'To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people.',
                },
                {
                    'title': 'Design',
                    'p': 'Systematic review of 12 controlled <italic>clinical trials</italic> (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials).',
                }],
            }
        }
        obtained = Abstract(self.xmltree)._get_abstract_by_lang(
            abstract_xpath=".//front//abstract",
            lang="en",
            return_title=True,
            return_sec_title=True,
            return_tags=True,
        )
        self.assertIsInstance(obtained, dict)
        for k, v in obtained.items():
            self.assertEqual("en", k)
            self.assertDictEqual(v, expected["en"])

    def test__get_abstract_by_lang_returns_tags_false(self):
        """
        Remove `<italic>` and `</italic>` from: `Systematic review of 12 controlled <italic>clinical trials</italic> (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials).`

        """
        obtained = Abstract(self.xmltree)._get_abstract_by_lang(
            abstract_xpath=".//front//abstract",
            lang="en",
            return_title=True,
            return_sec_title=True,
            return_tags=False,
        )
        self.assertNotIn("<italic>", obtained["en"]["sections"][1]["p"])

    def test__get_abstract_by_lang_does_not_returns_abstract_title(self):
        obtained = Abstract(self.xmltree)._get_abstract_by_lang(
            abstract_xpath=".//front//abstract",
            lang="en",
            return_title=False,
            return_sec_title=True,
            return_tags=True,
        )
        self.assertIsNone(obtained["en"].get("title"))

    def test__get_abstract_by_lang_does_not_returns_abstract_sec_title(self):
        obtained = Abstract(self.xmltree)._get_abstract_by_lang(
            abstract_xpath=".//front//abstract",
            lang="en",
            return_title=True,
            return_sec_title=False,
            return_tags=True,
        )
        self.assertIsNone(obtained["en"]["sections"][0].get("title"))
        self.assertIsNone(obtained["en"]["sections"][1].get("title"))

    def test__get_main_abstract(self):
        expected = {
            'lang': 'en',
            'abstract': {
                'title': 'Abstract',
                'sections': [{
                    'title': 'Objective',
                    'p': 'To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people.',
                },
                {
                    'title': 'Design',
                    'p': 'Systematic review of 12 controlled <italic>clinical trials</italic> (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials).',
                }],
            }
        }
        obtained = Abstract(self.xmltree).get_main_abstract(
            return_title=True,
            return_sec_title=True,
            return_tags=True,
        )
        self.assertDictEqual(expected, obtained)


class AbstractWithoutSectionsTest(TestCase):

    def setUp(self):
        self.xmltree = ET.fromstring(
            """
            <article 
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <abstract>
                <title>Abstract</title>
                <p>To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people. Systematic review of 12 controlled <italic>clinical trials</italic> (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials).</p>
            </abstract>
            <trans-abstract xml:lang="pt">
                <title>Resumo</title>
                <p>Examinar a eficácia do atendimento em hospital-dia no prolongamento da vida independente de idosos. Revisão sistemática de 12 <italic>estudos clínicos</italic> controlados (disponível em janeiro de 1997) comparando o atendimento em hospital-dia com atendimento abrangente (cinco ensaios), atendimento domiciliar (quatro ensaios) ou nenhum atendimento abrangente (três ensaios).</p>
            </trans-abstract>
            <trans-abstract xml:lang="fr">
                <title>Resumo</title>
                <p>Examiner l'efficacité de la fréquentation d'un hôpital de jour pour prolonger la vie autonome des personnes âgées. Revue systématique de 12 <italic>essais cliniques</italic> contrôlés (disponibles en janvier 1997) comparant les soins hospitaliers de jour aux soins complets (cinq essais), aux soins à domicile (quatre essais) ou à l'absence de soins complets (trois essais).</p>
            </trans-abstract>
            </article-meta>
            </front>
            <sub-article article-type="translation" xml:lang="es">
                <front-stub>
                    <abstract>
                        <title>Resumen</title>
                        <p>
                          Examinar la efectividad de la asistencia al hospital de día para prolongar la vida independiente de las personas mayores. Revisión sistemática de 12 <italic>ensayos clínicos</italic> controlados (disponibles en enero de 1997) que compararon la atención hospitalaria de día con atención integral (cinco ensayos), atención domiciliaria (cuatro ensayos) o ninguna atención integral (tres ensayos).</p>
                      </abstract>
                </front-stub>
            </sub-article>
            <sub-article article-type="translation" xml:lang="it">
                <front-stub>
                    <abstract>
                        <title>Resumen</title>
                        <p>
                          Esaminare l'efficacia della frequenza del day hospital nel prolungamento della vita autonoma delle persone anziane. Revisione sistematica di 12 <italic>studi clinici</italic> controllati (disponibili entro gennaio 1997) che confrontano l'assistenza in day hospital con l'assistenza completa (cinque studi), l'assistenza domiciliare (quattro studi) o nessuna assistenza completa (tre studi).</p>
                      </abstract>
                </front-stub>
            </sub-article>
            </article>
            """)

    def test__get_abstract_by_lang_returns_all(self):
        expected = {
            'en': {
                'title': 'Abstract',
                'p': 'To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people. Systematic review of 12 controlled <italic>clinical trials</italic> (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials).',
            },
        }
        obtained = Abstract(self.xmltree)._get_abstract_by_lang(
            abstract_xpath=".//front//abstract",
            lang="en",
            return_title=True,
            return_sec_title=True,
            return_tags=True,
        )
        self.assertIsInstance(obtained, dict)
        for k, v in obtained.items():
            self.assertEqual("en", k)
            self.assertDictEqual(v, expected["en"])

    def test__get_abstract_by_lang_returns_tags_false(self):
        """
        Remove `<italic>` and `</italic>` from: `Systematic review of 12 controlled <italic>clinical trials</italic> (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials).`

        """
        obtained = Abstract(self.xmltree)._get_abstract_by_lang(
            abstract_xpath=".//front//abstract",
            lang="en",
            return_title=True,
            return_sec_title=True,
            return_tags=False,
        )
        self.assertNotIn("<italic>", obtained["en"]["p"])

    def test__get_abstract_by_lang_does_not_returns_abstract_title(self):
        obtained = Abstract(self.xmltree)._get_abstract_by_lang(
            abstract_xpath=".//front//abstract",
            lang="en",
            return_title=False,
            return_sec_title=True,
            return_tags=True,
        )
        self.assertIsNone(obtained["en"].get("title"))

    def test__get_main_abstract(self):
        expected = {
            'lang': 'en',
            'abstract': {
                'title': 'Abstract',
                'p': 'To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people. Systematic review of 12 controlled <italic>clinical trials</italic> (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials).',
            }
        }
        obtained = Abstract(self.xmltree).get_main_abstract(
            return_title=True,
            return_sec_title=True,
            return_tags=True,
        )
        self.assertDictEqual(expected, obtained)

    def test_main_abstract_with_tags(self):
        obtained = Abstract(self.xmltree).main_abstract_with_tags

        expected = {
            "lang": "en",
            "title": "Abstract",
            "p": "To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people. Systematic review of 12 controlled <italic>clinical trials</italic> (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials).",
        }
        self.assertDictEqual(obtained, expected)

    def test_main_abstract_without_tags(self):
        obtained = Abstract(self.xmltree).main_abstract_without_tags

        expected = {"en": "To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people. Systematic review of 12 controlled clinical trials (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials)."}
        self.assertDictEqual(obtained, expected)
