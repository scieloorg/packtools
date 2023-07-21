from unittest import TestCase

from lxml import etree as ET

from packtools.sps.models.article_abstract import Abstract


class AbstractTest(TestCase):
    maxDiff = None

    def setUp(self):
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
        xmltree = ET.fromstring(xml)
        self.abstract = Abstract(xmltree)

    def test_main_abstract_with_tags(self):
        obtained = self.abstract.main_abstract_with_tags
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
        obtained = self.abstract.main_abstract_without_tags
        expected = {'en': 'objective method results conclusion'}
        self.assertEqual(obtained, expected)


class SubArticleAbstractTest(TestCase):
    maxDiff = None

    def setUp(self):
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
        xmltree = ET.fromstring(xml)
        self.abstract = Abstract(xmltree)

    def test_sub_article_abstract_with_tags(self):
        obtained = self.abstract.sub_article_abstract_with_tags

        expected = {
            "lang": "pt",
            "title": "RESUMO",
            "sections": {
                "Objetivo:": "objetivo",
                "Método:": "metodo",
                "Resultados:": "resultados",
                "Conclusão:": "conclusão"
            }
        }

        self.assertEqual(obtained, expected)

    def test_sub_article_abstract_without_tags(self):
        obtained = self.abstract.sub_article_abstract_without_tags
        expected = {'pt': 'objetivo metodo resultados conclusão'}
        self.assertEqual(obtained, expected)


class ArticleTransAbstractTest(TestCase):
    maxDiff = None

    def setUp(self):
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
        xmltree = ET.fromstring(xml)
        self.abstract = Abstract(xmltree)

    def test_trans_abstract_with_tags(self):
        obtained = self.abstract.trans_abstract_with_tags

        expected = {
            "lang": "es",
            "title": "RESUMEN",
            "sections": {
                "Objetivo:": "objetivo",
                "Método:": "metodo",
                "Resultados:": "resultados",
                "Conclusión:": "conclusion"
            }
        }

        self.assertEqual(obtained, expected)

    def test_trans_abstract_without_tags(self):
        obtained = self.abstract.trans_abstract_without_tags

        expected = {'es': 'objetivo metodo resultados conclusion'}

        self.assertEqual(obtained, expected)


class ArticleAbstractsTest(TestCase):
    maxDiff = None

    def setUp(self):
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
        xmltree = ET.fromstring(xml)
        self.abstract = Abstract(xmltree)

    def test_abstracts_with_tags(self):
        obtained = self.abstract.abstracts_with_tags

        expected = [
            {
                "lang": "en",
                "title": "Abstract",
                "sections": {
                    "Objective:": "objective",
                    "Method:": "method",
                    "Results:": "results",
                    "Conclusion:": "conclusion"
                }
            },
            {
                "lang": "es",
                "title": "RESUMEN",
                "sections": {
                    "Objetivo:": "objetivo",
                    "Método:": "metodo",
                    "Resultados:": "resultados",
                    "Conclusión:": "conclusion"
                }
            },
            {
                "lang": "pt",
                "title": "RESUMO",
                "sections": {
                    "Objetivo:": "objetivo",
                    "Método:": "metodo",
                    "Resultados:": "resultados",
                    "Conclusão:": "conclusão"
                }
            }

        ]

        self.assertEqual(obtained, expected)

    def test_abstracts_without_tags(self):

        obtained = self.abstract.abstracts_without_tags

        expected = {
            'en': 'objective method results conclusion',
            'pt': 'objetivo metodo resultados conclusão',
            'es': 'objetivo metodo resultados conclusion'
        }

        self.assertEqual(obtained, expected)

    def test_without_trans_abstract_with_tags(self):
        xml = (
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            </article-meta>
            </front>
            </article>
            """
        )
        data = ET.fromstring(xml)
        obtained = Abstract(data).trans_abstract_with_tags

        expected = None

        self.assertEqual(obtained, expected)


class AbstractWithSectionsTest(TestCase):

    def setUp(self):
        xmltree = ET.fromstring(
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

            <trans-abstract xml:lang="fr">
                <title>Resumo</title>
                <sec>
                  <title>Objetivo: </title>
                  <p>évaluer l'effet d'une intervention éducative en maison de retraite sur la qualité de vie des aidants familiaux de personnes âgées ayant survécu à un AVC.</p>
                </sec>
                <sec>
                  <title>Método: </title>
                  <p>Essai clinique randomisé... Module <italic>Old</italic> (WHOQOL-OLD) à 1 semaine, 2 mois et 1 an après la sortie.</p>
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
            <sub-article article-type="translation" xml:lang="de">
                <front-stub>
                    <abstract>
                        <title>Resumen</title>
                        <sec>
                          <title>Objetivo: </title>
                          <p>Randomisierte klinische Studie... Modul <italic>Alt</italic> (WHOQOL-OLD) 1 Woche, 2 Monate und 1 Jahr nach der Entlassung.</p>
                        </sec>
                        <sec>
                          <title>Método: </title>
                          <p>Bewertung der Auswirkungen von Pflegeeinsätzen in Pflegeheimen auf die Lebensqualität von Familienbetreuern älterer Erwachsener, die zerebrovaskuläre Unfälle überlebt haben.</p>
                        </sec>
                      </abstract>
                </front-stub>
            </sub-article>
            </article>
            """)
        self.abstract = Abstract(xmltree)

    def test__get_section_titles_and_paragraphs(self):
        expected = {
            "Objective": "To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people.",
            "Design": "Systematic review of 12 controlled <italic>clinical trials</italic> (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials).",
        }
        result = self.abstract._get_section_titles_and_paragraphs(
            ".//front//abstract",
        )
        self.assertDictEqual(expected, result)

    def test__main_abstract_without_tags(self):
        expected = {
            "en": "To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people. Systematic review of 12 controlled clinical trials (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials)."}
        result = self.abstract.main_abstract_without_tags
        self.assertDictEqual(expected, result)

    def test__sub_article_abstract_without_tags(self):
        expected = {
            "es": "evaluar el efecto de intervenciones de atención domiciliaria de enfermería sobre la calidad de vida en cuidadores familiares de adultos mayores sobrevivientes de accidentes cerebrovasculares. Ensayo Clínico Aleatorizado ... World Health Organization Quality of Life Assessment (WHOQOL-BREF) y el módulo Old(WHOQOL-OLD) 1semana, 2meses y 1año después del alta.",
            "de": "Randomisierte klinische Studie... Modul Alt (WHOQOL-OLD) 1 Woche, 2 Monate und 1 Jahr nach der Entlassung. Bewertung der Auswirkungen von Pflegeeinsätzen in Pflegeheimen auf die Lebensqualität von Familienbetreuern älterer Erwachsener, die zerebrovaskuläre Unfälle überlebt haben.",
        }
        result = self.abstract.sub_article_abstract_without_tags
        self.assertDictEqual(expected, result)

    def test__trans_abstract_without_tags(self):
        expected = {
            "pt": "avaliar o efeito de intervenção educativa domiciliar de enfermagem na qualidade de vida de cuidadores familiares de idosos sobreviventes de acidente vascular cerebral (AVC). Ensaio Clínico Randomizado... Módulo Old (WHOQOL-OLD) em 1 semana, 2 meses e 1 ano após a alta.",
            "fr": "évaluer l'effet d'une intervention éducative en maison de retraite sur la qualité de vie des aidants familiaux de personnes âgées ayant survécu à un AVC. Essai clinique randomisé... Module Old (WHOQOL-OLD) à 1 semaine, 2 mois et 1 an après la sortie.",
        }
        result = self.abstract.trans_abstract_without_tags
        print("")
        print(result["fr"])
        print(expected["fr"])

        self.assertDictEqual(expected, result)


class AbstractWithoutSectionsTest(TestCase):

    def setUp(self):
        xmltree = ET.fromstring(
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
        self.abstract = Abstract(xmltree)

    def test__get_section_titles_and_paragraphs(self):
        expected = {}
        result = self.abstract._get_section_titles_and_paragraphs(
            ".//front//abstract",
        )
        self.assertDictEqual(expected, result)

    def test__main_abstract_without_tags(self):
        expected = {"en": "To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people. Systematic review of 12 controlled clinical trials (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials)."}
        result = self.abstract.main_abstract_without_tags
        self.assertDictEqual(expected, result)

    def test__sub_article_abstract_without_tags(self):
        expected = {
            "es": "Examinar la efectividad de la asistencia al hospital de día para prolongar la vida independiente de las personas mayores. Revisión sistemática de 12 ensayos clínicos controlados (disponibles en enero de 1997) que compararon la atención hospitalaria de día con atención integral (cinco ensayos), atención domiciliaria (cuatro ensayos) o ninguna atención integral (tres ensayos).",
            "it": "Esaminare l'efficacia della frequenza del day hospital nel prolungamento della vita autonoma delle persone anziane. Revisione sistematica di 12 studi clinici controllati (disponibili entro gennaio 1997) che confrontano l'assistenza in day hospital con l'assistenza completa (cinque studi), l'assistenza domiciliare (quattro studi) o nessuna assistenza completa (tre studi).",
        }
        result = self.abstract.sub_article_abstract_without_tags
        self.assertDictEqual(expected, result)

    def test__trans_abstract_without_tags(self):
        expected = {
            "pt": "Examinar a eficácia do atendimento em hospital-dia no prolongamento da vida independente de idosos. Revisão sistemática de 12 estudos clínicos controlados (disponível em janeiro de 1997) comparando o atendimento em hospital-dia com atendimento abrangente (cinco ensaios), atendimento domiciliar (quatro ensaios) ou nenhum atendimento abrangente (três ensaios).",
            "fr": "Examiner l'efficacité de la fréquentation d'un hôpital de jour pour prolonger la vie autonome des personnes âgées. Revue systématique de 12 essais cliniques contrôlés (disponibles en janvier 1997) comparant les soins hospitaliers de jour aux soins complets (cinq essais), aux soins à domicile (quatre essais) ou à l'absence de soins complets (trois essais).",
        }
        result = self.abstract.trans_abstract_without_tags
        self.assertDictEqual(expected, result)
