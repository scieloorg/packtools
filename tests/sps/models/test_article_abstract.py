from unittest import TestCase

from lxml import etree as ET

from packtools.sps.models.article_abstract import Abstract, ArticleAbstract, Highlight, ArticleHighlights, VisualAbstract, \
    ArticleVisualAbstracts


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
                <title>Résumé</title>
                <sec>
                  <title>Objectif: </title>
                  <p>évaluer l'effet d'une intervention éducative en maison de retraite sur la qualité de vie des aidants familiaux de personnes âgées ayant survécu à un AVC.</p>
                </sec>
                <sec>
                  <title>Méthode: </title>
                  <p>Essai clinique randomisé... Module <italic>Old</italic> (WHOQOL-OLD) à 1 semaine, 2 mois et 1 an après la sortie.</p>
                </sec>
            </trans-abstract>
            </article-meta>
            </front>
            <sub-article article-type="translation" id="01" xml:lang="es">
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
            <sub-article article-type="translation" id="02" xml:lang="de">
                <front-stub>
                    <abstract>
                        <title>Zusammenfassung</title>
                        <sec>
                          <title>Ziel: </title>
                          <p>Randomisierte klinische Studie... Modul <italic>Alt</italic> (WHOQOL-OLD) 1 Woche, 2 Monate und 1 Jahr nach der Entlassung.</p>
                        </sec>
                        <sec>
                          <title>Methode: </title>
                          <p>Bewertung der Auswirkungen von Pflegeeinsätzen in Pflegeheimen auf die Lebensqualität von Familienbetreuern älterer Erwachsener, die zerebrovaskuläre Unfälle überlebt haben.</p>
                        </sec>
                      </abstract>
                </front-stub>
            </sub-article>
            </article>
            """)
        self.abstract = Abstract(xmltree)

    def test__main_abstract_without_tags(self):
        self.maxDiff = None
        expected = {
            "lang": "en",
            'parent_name': 'article',
            "abstract": "To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people. Systematic review of 12 controlled clinical trials (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials)."
        }
        result = self.abstract.get_main_abstract(style="only_p")
        self.assertDictEqual(expected, result)

    def test_get_main_abstract_default_style(self):
        """
        <title>Abstract</title>
        <sec>
            <title>Objective</title>
            <p>To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people.</p>
        </sec>
        <sec>
            <title>Design</title>
            <p>Systematic review of 12 controlled <italic>clinical trials</italic> (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials).</p>
        </sec>
        """
        expected = {
            "lang": "en",
            'parent_name': 'article',
            "abstract": {
                "lang": "en",
                "title": "Abstract",
                "sections": [
                    {
                        "title": "Objective",
                        "p": "To examine the effectiveness of day hospital attendance in prolonging independent living for "
                             "elderly people.",
                    },
                    {
                        "title": "Design",
                        "p": "Systematic review of 12 controlled clinical trials (available by January 1997) comparing day "
                             "hospital care with comprehensive care (five trials), domiciliary care (four trials), "
                             "or no comprehensive care (three trials).",

                    }],
            }
        }
        result = self.abstract.get_main_abstract()
        self.assertDictEqual(expected, result)

    def test_get_main_abstract_default_style_html(self):
        self.maxDiff = None
        """
        <title>Abstract</title>
        <sec>
            <title>Objective</title>
            <p>To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people.</p>
        </sec>
        <sec>
            <title>Design</title>
            <p>Systematic review of 12 controlled <italic>clinical trials</italic> (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials).</p>
        </sec>
        """
        expected = {
            "lang": "en",
            'parent_name': 'article',
            "abstract": {
                "lang": "en",
                "title": "<t>Abstract</t>",
                "sections": [
                    {
                        "title": "<t>Objective</t>",
                        "p": "To examine the effectiveness of day hospital attendance in prolonging independent living for "
                             "elderly people.",
                    },
                    {
                        "title": "<t>Design</t>",
                        "p": "Systematic review of 12 controlled <i>clinical trials</i> (available by January 1997) comparing day "
                             "hospital care with comprehensive care (five trials), domiciliary care (four trials), "
                             "or no comprehensive care (three trials).",

                    }],
            }
        }
        result = self.abstract.get_main_abstract(
            html=True,
            tags_to_convert_to_html={'title': 't', 'italic': 'i'}
        )
        self.assertDictEqual(expected, result)

    def test_get_main_abstract_inline(self):
        """
        <title>Abstract</title>
        <sec>
            <title>Objective</title>
            <p>To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people.</p>
        </sec>
        <sec>
            <title>Design</title>
            <p>Systematic review of 12 controlled <italic>clinical trials</italic> (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials).</p>
        </sec>
        """
        expected = {
            "lang": "en",
            'parent_name': 'article',
            "abstract": "Abstract Objective To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people. Design Systematic review of 12 controlled clinical trials (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials)."
        }
        result = self.abstract.get_main_abstract(style="inline")
        self.assertDictEqual(expected, result)

    def test_get_main_abstract_inline_html(self):
        self.maxDiff = None
        """
        <title>Abstract</title>
        <sec>
            <title>Objective</title>
            <p>To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people.</p>
        </sec>
        <sec>
            <title>Design</title>
            <p>Systematic review of 12 controlled <italic>clinical trials</italic> (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials).</p>
        </sec>
        """
        expected = {
            "lang": "en",
            'parent_name': 'article',
            "abstract": "Abstract Objective To examine the effectiveness of day hospital attendance in prolonging "
                        "independent living for elderly people. Design Systematic review of 12 controlled "
                        "<i>clinical trials</i> (available by January 1997) comparing day hospital care with "
                        "comprehensive care (five trials), domiciliary care (four trials), or no comprehensive "
                        "care (three trials)."
        }
        result = self.abstract.get_main_abstract(
            style="inline",
            html=True
        )
        self.assertDictEqual(expected, result)

    def test_get_main_abstract_xml(self):
        """
        <title>Abstract</title>
        <sec>
            <title>Objective</title>
            <p>To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people.</p>
        </sec>
        <sec>
            <title>Design</title>
            <p>Systematic review of 12 controlled <italic>clinical trials</italic> (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials).</p>
        </sec>
        """
        expected = {
            "lang": "en",
            'parent_name': 'article',
            "abstract": """<title>Abstract</title>
        <sec>
            <title>Objective</title>
            <p>To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people.</p>
        </sec>
        <sec>
            <title>Design</title>
            <p>Systematic review of 12 controlled <italic>clinical trials</italic> (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials).</p>
        </sec>""",
        }
        result = self.abstract.get_main_abstract(style="xml")
        self.assertEqual(expected["lang"], result["lang"])
        self.assertIn("<title>Abstract</title>", result["abstract"])
        self.assertIn("<italic>clinical trials</italic>", result["abstract"])
        self.assertIn("<title>Objective</title>", result["abstract"])
        self.assertIn("<title>Design</title>", result["abstract"])
        self.assertIn(
            "<p>Systematic review of 12 controlled <italic>clinical trials</italic> (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials).</p>",
            result["abstract"])

    def test_get_main_abstract_only_p(self):
        """
        <title>Abstract</title>
        <sec>
            <title>Objective</title>
            <p>To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people.</p>
        </sec>
        <sec>
            <title>Design</title>
            <p>Systematic review of 12 controlled <italic>clinical trials</italic> (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials).</p>
        </sec>
        """
        expected = {
            "lang": "en",
            'parent_name': 'article',
            "abstract": "To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people. Systematic review of 12 controlled clinical trials (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials)."
        }
        result = self.abstract.get_main_abstract(style="only_p")
        self.assertDictEqual(expected, result)

    def test_get_main_abstract_only_p_html(self):
        self.maxDiff = None
        """
        <title>Abstract</title>
        <sec>
            <title>Objective</title>
            <p>To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people.</p>
        </sec>
        <sec>
            <title>Design</title>
            <p>Systematic review of 12 controlled <italic>clinical trials</italic> (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials).</p>
        </sec>
        """
        expected = {
            "lang": "en",
            'parent_name': 'article',
            "abstract": "To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people. Systematic review of 12 controlled <i>clinical trials</i> (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials)."
        }
        result = self.abstract.get_main_abstract(
            style="only_p",
            html=True,
        )
        self.assertDictEqual(expected, result)

    def test__get_sub_article_abstracts(self):
        """
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
                    <title>Zusammenfassung</title>
                    <sec>
                      <title>Ziel: </title>
                      <p>Randomisierte klinische Studie... Modul <italic>Alt</italic> (WHOQOL-OLD) 1 Woche, 2 Monate und 1 Jahr nach der Entlassung.</p>
                    </sec>
                    <sec>
                      <title>Methode: </title>
                      <p>Bewertung der Auswirkungen von Pflegeeinsätzen in Pflegeheimen auf die Lebensqualität von Familienbetreuern älterer Erwachsener, die zerebrovaskuläre Unfälle überlebt haben.</p>
                    </sec>
                  </abstract>
            </front-stub>
        </sub-article>
        """
        self.maxDiff = None
        expected = (
            {
                "lang": "es",
                'parent_name': 'sub-article',
                "abstract": {
                    "lang": "es",
                    "title": "Resumen",
                    "sections": [
                        {
                            "title": "Objetivo: ",
                            "p": "evaluar el efecto de intervenciones de atención domiciliaria de enfermería sobre la "
                                 "calidad de vida en cuidadores familiares de adultos mayores sobrevivientes de "
                                 "accidentes cerebrovasculares. "
                        },
                        {
                            "title": "Método: ",
                            "p": "Ensayo Clínico Aleatorizado ... World Health Organization Quality of Life "
                                 "Assessment (WHOQOL-BREF) y el módulo Old(WHOQOL-OLD) "
                                 "1semana, 2meses y 1año después del alta. "
                        },
                    ]
                },
                "id": "01"
            },
            {
                "lang": "de",
                'parent_name': 'sub-article',
                "abstract": {
                    "lang": "de",
                    "title": "Zusammenfassung",
                    "sections": [
                        {
                            "title": "Ziel: ",
                            "p": "Randomisierte klinische Studie... Modul Alt (WHOQOL-OLD) 1 Woche, 2 Monate und 1 "
                                 "Jahr nach der Entlassung."
                        },
                        {
                            "title": "Methode: ",
                            "p": "Bewertung der Auswirkungen von Pflegeeinsätzen in Pflegeheimen auf die "
                                 "Lebensqualität von Familienbetreuern älterer Erwachsener, die zerebrovaskuläre "
                                 "Unfälle überlebt haben."
                        },
                    ]
                },
                "id": "02"
            },
        )
        result = self.abstract._get_sub_article_abstracts()
        for res, exp in zip(result, expected):
            with self.subTest(res["lang"]):
                self.assertDictEqual(exp, res)

    def test__get_sub_article_abstracts_html(self):
        """
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
                    <title>Zusammenfassung</title>
                    <sec>
                      <title>Ziel: </title>
                      <p>Randomisierte klinische Studie... Modul <italic>Alt</italic> (WHOQOL-OLD) 1 Woche, 2 Monate und 1 Jahr nach der Entlassung.</p>
                    </sec>
                    <sec>
                      <title>Methode: </title>
                      <p>Bewertung der Auswirkungen von Pflegeeinsätzen in Pflegeheimen auf die Lebensqualität von Familienbetreuern älterer Erwachsener, die zerebrovaskuläre Unfälle überlebt haben.</p>
                    </sec>
                  </abstract>
            </front-stub>
        </sub-article>
        """
        self.maxDiff = None
        expected = (
            {
                "lang": "es",
                'parent_name': 'sub-article',
                "abstract": {
                    "lang": "es",
                    "title": "Resumen",
                    "sections": [
                        {
                            "title": "Objetivo:",
                            "p": "evaluar el efecto de intervenciones de atención domiciliaria de enfermería sobre la "
                                 "calidad de vida en cuidadores familiares de adultos mayores sobrevivientes de "
                                 "accidentes cerebrovasculares."
                        },
                        {
                            "title": "Método:",
                            "p": "Ensayo Clínico Aleatorizado ... <i>World Health Organization Quality of Life "
                                 "Assessment</i> (WHOQOL-BREF) y el módulo <i>Old</i>(WHOQOL-OLD) "
                                 "1semana, 2meses y 1año después del alta."
                        },
                    ]
                },
                "id": "01"
            },
            {
                "lang": "de",
                'parent_name': 'sub-article',
                "abstract": {
                    "lang": "de",
                    "title": "Zusammenfassung",
                    "sections": [
                        {
                            "title": "Ziel:",
                            "p": "Randomisierte klinische Studie... Modul <i>Alt</i> (WHOQOL-OLD) 1 Woche, 2 Monate und 1 "
                                 "Jahr nach der Entlassung."
                        },
                        {
                            "title": "Methode:",
                            "p": "Bewertung der Auswirkungen von Pflegeeinsätzen in Pflegeheimen auf die "
                                 "Lebensqualität von Familienbetreuern älterer Erwachsener, die zerebrovaskuläre "
                                 "Unfälle überlebt haben."
                        },
                    ]
                },
                "id": "02"
            },
        )
        result = self.abstract._get_sub_article_abstracts(
            html=True,
            tags_to_convert_to_html={'bold': 'b'}
        )
        for res, exp in zip(result, expected):
            with self.subTest(res["lang"]):
                self.assertDictEqual(exp, res)

    def test__get_trans_abstracts(self):
        """
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
            <title>Résumé</title>
            <sec>
              <title>Objectif: </title>
              <p>évaluer l'effet d'une intervention éducative en maison de retraite sur la qualité de vie des aidants familiaux de personnes âgées ayant survécu à un AVC.</p>
            </sec>
            <sec>
              <title>Méthode: </title>
              <p>Essai clinique randomisé... Module <italic>Old</italic> (WHOQOL-OLD) à 1 semaine, 2 mois et 1 an après la sortie.</p>
            </sec>
        </trans-abstract>
        """
        self.maxDiff = None
        expected = (
            {
                "lang": "pt",
                'parent_name': 'article',
                "abstract": {
                    "lang": "pt",
                    "title": "Resumo",
                    "sections": [
                        {
                            "title": "Objetivo:",
                            "p": "avaliar o efeito de intervenção educativa domiciliar de enfermagem na qualidade de "
                                 "vida de cuidadores familiares de idosos sobreviventes de acidente vascular cerebral "
                                 "(AVC)."
                        },
                        {
                            "title": "Método:",
                            "p": "Ensaio Clínico Randomizado... Módulo <i>Old</i> (WHOQOL-OLD) em 1 semana, "
                                 "2 meses e 1 ano após a alta."
                        },
                    ]
                }
            },
            {
                "lang": "fr",
                'parent_name': 'article',
                "abstract": {
                    "lang": "fr",
                    "title": "Résumé",
                    "sections": [
                        {
                            "title": "Objectif:",
                            "p": "évaluer l'effet d'une intervention éducative en maison de retraite sur la qualité de "
                                 "vie des aidants familiaux de personnes âgées ayant survécu à un AVC."
                        },
                        {
                            "title": "Méthode:",
                            "p": "Essai clinique randomisé... Module <i>Old</i> (WHOQOL-OLD) à 1 semaine, 2 "
                                 "mois et 1 an après la sortie."
                        },
                    ]
                }
            },
        )
        result = self.abstract._get_trans_abstracts(
            html=True,
        )
        for res, exp in zip(result, expected):
            with self.subTest(exp["lang"]):
                self.assertDictEqual(exp, res)


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
                <title>Résumé</title>
                <p>Examiner l'efficacité de la fréquentation d'un hôpital de jour pour prolonger la vie autonome des personnes âgées. Revue systématique de 12 <italic>essais cliniques</italic> contrôlés (disponibles en janvier 1997) comparant les soins hospitaliers de jour aux soins complets (cinq essais), aux soins à domicile (quatre essais) ou à l'absence de soins complets (trois essais).</p>
            </trans-abstract>
            </article-meta>
            </front>
            <sub-article article-type="translation" id="01" xml:lang="es">
                <front-stub>
                    <abstract>
                        <title>Resumen</title>
                        <p>
                          Examinar la efectividad de la asistencia al hospital de día para prolongar la vida independiente de las personas mayores. Revisión sistemática de 12 <italic>ensayos clínicos</italic> controlados (disponibles en enero de 1997) que compararon la atención hospitalaria de día con atención integral (cinco ensayos), atención domiciliaria (cuatro ensayos) o ninguna atención integral (tres ensayos).</p>
                      </abstract>
                </front-stub>
            </sub-article>
            <sub-article article-type="translation" id="02" xml:lang="it">
                <front-stub>
                    <abstract>
                        <title>Riepilogo</title>
                        <p>
                          Esaminare l'efficacia della frequenza del day hospital nel prolungamento della vita autonoma delle persone anziane. Revisione sistematica di 12 <italic>studi clinici</italic> controllati (disponibili entro gennaio 1997) che confrontano l'assistenza in day hospital con l'assistenza completa (cinque studi), l'assistenza domiciliare (quattro studi) o nessuna assistenza completa (tre studi).</p>
                      </abstract>
                </front-stub>
            </sub-article>
        </article>
        """)
        self.abstract = Abstract(xmltree)

    def test__main_abstract_without_tags(self):
        self.maxDiff = None
        expected = {
            "lang": "en",
            'parent_name': 'article',
            "abstract": "To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people. Systematic review of 12 controlled clinical trials (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials)."
        }
        result = self.abstract.get_main_abstract(style="only_p")
        self.assertDictEqual(expected, result)

    def test_get_main_abstract_default_style(self):
        self.maxDiff = None
        expected = {
            "lang": "en",
            'parent_name': 'article',
            "abstract": {
                "lang": "en",
                "title": "Abstract",
                "p": "To examine the effectiveness of day hospital attendance in prolonging independent living for "
                     "elderly people. Systematic review of 12 controlled clinical trials (available by January 1997) "
                     "comparing day hospital care with comprehensive care (five trials), domiciliary care "
                     "(four trials), or no comprehensive care (three trials).",
            }
        }
        result = self.abstract.get_main_abstract()
        self.assertDictEqual(expected, result)

    def test_get_main_abstract_default_style_html(self):
        '''
        <abstract>
            <title>Abstract</title>
            <p>To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people. Systematic review of 12 controlled <italic>clinical trials</italic> (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials).</p>
        </abstract>
        '''
        self.maxDiff = None
        expected = {
            "lang": "en",
            'parent_name': 'article',
            "abstract": {
                "lang": "en",
                "title": "<title>Abstract</title>",
                "p": "To examine the effectiveness of day hospital attendance in prolonging independent living for "
                     "elderly people. Systematic review of 12 controlled <i>clinical trials</i> (available by January 1997) "
                     "comparing day hospital care with comprehensive care (five trials), domiciliary care "
                     "(four trials), or no comprehensive care (three trials).",
            }
        }
        result = self.abstract.get_main_abstract(
            html=True,
            tags_to_keep=['title'],
        )
        self.assertDictEqual(expected, result)

    def test_get_main_abstract_inline(self):
        self.maxDiff = None
        expected = {
            "lang": "en",
            'parent_name': 'article',
            "abstract": "Abstract To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people. Systematic review of 12 controlled clinical trials (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials)."
        }
        result = self.abstract.get_main_abstract(style="inline")
        self.assertDictEqual(expected, result)

    def test_get_main_abstract_inline_html(self):
        self.maxDiff = None
        expected = {
            "lang": "en",
            'parent_name': 'article',
            "abstract": "Abstract To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people. Systematic review of 12 controlled <i>clinical trials</i> (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials)."
        }
        result = self.abstract.get_main_abstract(
            style="inline",
            html=True,
        )
        self.assertDictEqual(expected, result)

    def test_get_main_abstract_xml(self):
        expected = {
            "lang": "en",
            'parent_name': 'article',
            "abstract": """<title>Abstract</title>
                <p>To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people. Systematic review of 12 controlled <italic>clinical trials</italic> (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials).</p>""",
        }
        result = self.abstract.get_main_abstract(style="xml")
        self.assertEqual(expected["lang"], result["lang"])
        self.assertIn("<title>Abstract</title>", result["abstract"])
        self.assertIn("<italic>clinical trials</italic>", result["abstract"])
        self.assertIn(
            "<p>To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people. Systematic review of 12 controlled <italic>clinical trials</italic> (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials).</p>",
            result["abstract"])

    def test_get_main_abstract_only_p(self):
        self.maxDiff = None
        expected = {
            "lang": "en",
            'parent_name': 'article',
            "abstract": "To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people. Systematic review of 12 controlled clinical trials (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials)."
        }
        result = self.abstract.get_main_abstract(style="only_p")
        self.assertDictEqual(expected, result)

    def test_get_main_abstract_only_p_html(self):
        self.maxDiff = None
        expected = {
            "lang": "en",
            'parent_name': 'article',
            "abstract": "To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people. Systematic review of 12 controlled <i>clinical trials</i> (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials)."
        }
        result = self.abstract.get_main_abstract(
            style="only_p",
            html=True,
        )
        self.assertDictEqual(expected, result)

    def test__get_sub_article_abstracts(self):
        """
        <article>
        <sub-article article-type="translation" id="01" xml:lang="es">
        <front-stub>
        <abstract>
        <title>Resumen</title>
        <p>
        Examinar la efectividad de la asistencia al hospital de día para prolongar la vida independiente de las personas mayores. Revisión sistemática de 12 <italic>ensayos clínicos</italic> controlados (disponibles en enero de 1997) que compararon la atención hospitalaria de día con atención integral (cinco ensayos), atención domiciliaria (cuatro ensayos) o ninguna atención integral (tres ensayos).</p>
        </abstract>
        </front-stub>
        </sub-article>
        <sub-article article-type="translation" id="02" xml:lang="it">
        <front-stub>
        <abstract>
        <title>Riepilogo</title>
        <p>
        Esaminare l'efficacia della frequenza del day hospital nel prolungamento della vita autonoma delle persone anziane. Revisione sistematica di 12 <italic>studi clinici</italic> controllati (disponibili entro gennaio 1997) che confrontano l'assistenza in day hospital con l'assistenza completa (cinque studi), l'assistenza domiciliare (quattro studi) o nessuna assistenza completa (tre studi).</p>
        </abstract>
        </front-stub>
        </sub-article>
        </article>
        """
        self.maxDiff = None
        expected = (
            {
                "lang": "es",
                'parent_name': 'sub-article',
                "abstract": {
                    "lang": "es",
                    "title": "Resumen",
                    "p": "Examinar la efectividad de la asistencia al hospital de día para prolongar la vida "
                         "independiente de las personas mayores. Revisión sistemática de 12 ensayos clínicos "
                         "controlados (disponibles en enero de 1997) que compararon la atención hospitalaria "
                         "de día con atención integral (cinco ensayos), atención domiciliaria (cuatro ensayos) "
                         "o ninguna atención integral (tres ensayos).",
                },
                "id": "01"
            },
            {
                "lang": "it",
                'parent_name': 'sub-article',
                "abstract": {
                    "lang": "it",
                    "title": "Riepilogo",
                    "p": "Esaminare l'efficacia della frequenza del day hospital nel prolungamento della vita "
                         "autonoma delle persone anziane. Revisione sistematica di 12 studi clinici controllati "
                         "(disponibili entro gennaio 1997) che confrontano l'assistenza in day hospital con "
                         "l'assistenza completa (cinque studi), l'assistenza domiciliare (quattro studi) o nessuna "
                         "assistenza completa (tre studi).",
                },
                "id": "02"
            },
        )
        result = self.abstract._get_sub_article_abstracts()
        for res, exp in zip(result, expected):
            with self.subTest(res["lang"]):
                self.assertDictEqual(exp, res)

    def test__get_sub_article_abstracts_html(self):
        """
        <article>
        <sub-article article-type="translation" id="01" xml:lang="es">
        <front-stub>
        <abstract>
        <title>Resumen</title>
        <p>
        Examinar la efectividad de la asistencia al hospital de día para prolongar la vida independiente de las personas mayores. Revisión sistemática de 12 <italic>ensayos clínicos</italic> controlados (disponibles en enero de 1997) que compararon la atención hospitalaria de día con atención integral (cinco ensayos), atención domiciliaria (cuatro ensayos) o ninguna atención integral (tres ensayos).</p>
        </abstract>
        </front-stub>
        </sub-article>
        <sub-article article-type="translation" id="02" xml:lang="it">
        <front-stub>
        <abstract>
        <title>Riepilogo</title>
        <p>
        Esaminare l'efficacia della frequenza del day hospital nel prolungamento della vita autonoma delle persone anziane. Revisione sistematica di 12 <italic>studi clinici</italic> controllati (disponibili entro gennaio 1997) che confrontano l'assistenza in day hospital con l'assistenza completa (cinque studi), l'assistenza domiciliare (quattro studi) o nessuna assistenza completa (tre studi).</p>
        </abstract>
        </front-stub>
        </sub-article>
        </article>
        """
        self.maxDiff = None
        expected = (
            {
                "lang": "es",
                'parent_name': 'sub-article',
                "abstract": {
                    "lang": "es",
                    "title": "Resumen",
                    "p": "Examinar la efectividad de la asistencia al hospital de día para prolongar la vida "
                         "independiente de las personas mayores. Revisión sistemática de 12 <i>ensayos clínicos</i> "
                         "controlados (disponibles en enero de 1997) que compararon la atención hospitalaria "
                         "de día con atención integral (cinco ensayos), atención domiciliaria (cuatro ensayos) "
                         "o ninguna atención integral (tres ensayos).",
                },
                "id": "01"
            },
            {
                "lang": "it",
                'parent_name': 'sub-article',
                "abstract": {
                    "lang": "it",
                    "title": "Riepilogo",
                    "p": "Esaminare l'efficacia della frequenza del day hospital nel prolungamento della vita "
                         "autonoma delle persone anziane. Revisione sistematica di 12 <i>studi clinici</i> controllati "
                         "(disponibili entro gennaio 1997) che confrontano l'assistenza in day hospital con "
                         "l'assistenza completa (cinque studi), l'assistenza domiciliare (quattro studi) o nessuna "
                         "assistenza completa (tre studi).",
                },
                "id": "02"
            },
        )
        result = self.abstract._get_sub_article_abstracts(
            html=True,
        )
        for res, exp in zip(result, expected):
            with self.subTest(res["lang"]):
                self.assertDictEqual(exp, res)

    def test__get_trans_abstracts(self):
        self.maxDiff = None
        """
        <trans-abstract xml:lang="pt">
            <title>Resumo</title>
            <p>Examinar a eficácia do atendimento em hospital-dia no prolongamento da vida independente de idosos. Revisão sistemática de 12 <italic>estudos clínicos</italic> controlados (disponível em janeiro de 1997) comparando o atendimento em hospital-dia com atendimento abrangente (cinco ensaios), atendimento domiciliar (quatro ensaios) ou nenhum atendimento abrangente (três ensaios).</p>
        </trans-abstract>
        <trans-abstract xml:lang="fr">
            <title>Résumé</title>
            <p>Examiner l'efficacité de la fréquentation d'un hôpital de jour pour prolonger la vie autonome des personnes âgées. Revue systématique de 12 <italic>essais cliniques</italic> contrôlés (disponibles en janvier 1997) comparant les soins hospitaliers de jour aux soins complets (cinq essais), aux soins à domicile (quatre essais) ou à l'absence de soins complets (trois essais).</p>
        </trans-abstract>
        """
        expected = (
            {
                "lang": "pt",
                'parent_name': 'article',
                "abstract": {
                    "lang": "pt",
                    "title": "Resumo",
                    "p": "Examinar a eficácia do atendimento em hospital-dia no prolongamento da vida independente de "
                         "idosos. Revisão sistemática de 12 <i>estudos clínicos</i> controlados (disponível "
                         "em janeiro de 1997) comparando o atendimento em hospital-dia com atendimento abrangente "
                         "(cinco ensaios), atendimento domiciliar (quatro ensaios) ou nenhum atendimento abrangente "
                         "(três ensaios).",
                }
            },
            {
                "lang": "fr",
                'parent_name': 'article',
                "abstract": {
                    "lang": "fr",
                    "title": "Résumé",
                    "p": "Examiner l'efficacité de la fréquentation d'un hôpital de jour pour prolonger la vie "
                         "autonome des personnes âgées. Revue systématique de 12 <i>essais cliniques</i> "
                         "contrôlés (disponibles en janvier 1997) comparant les soins hospitaliers de jour aux soins "
                         "complets (cinq essais), aux soins à domicile (quatre essais) ou à l'absence de soins "
                         "complets (trois essais).",
                }
            },
        )
        result = self.abstract._get_trans_abstracts(
            html=True,
        )
        for res, exp in zip(result, expected):
            with self.subTest(exp["lang"]):
                self.assertDictEqual(exp, res)


class AbstractWithStylesTest(TestCase):

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
                    <title>inicio</title>
                    <p><bold>conteúdo de bold</bold> text </p>
                </sec>
                <sec>
                    <title>meio</title>
                    <p>text <bold>conteúdo de bold</bold> text </p>
                </sec>
                <sec>
                    <title>fim</title>
                    <p>text <bold>conteúdo de bold</bold></p>
                </sec>
                <sec>
                    <title>aninhado</title>
                    <p>text <bold>conteúdo <italic>de</italic> bold</bold></p>
                </sec>
            </abstract>
            <trans-abstract xml:lang="pt">
                <title>Abstract</title>
                <sec>
                    <title>inicio</title>
                    <p><bold>conteúdo de bold</bold> text </p>
                </sec>
                <sec>
                    <title>meio</title>
                    <p>text <bold>conteúdo de bold</bold> text </p>
                </sec>
                <sec>
                    <title>fim</title>
                    <p>text <bold>conteúdo de bold</bold></p>
                </sec>
                <sec>
                    <title>aninhado</title>
                    <p>text <bold>conteúdo <italic>de</italic> bold</bold></p>
                </sec>
            </trans-abstract>
            </article-meta>
            </front>
            <sub-article article-type="translation" id="01" xml:lang="es">
                <front-stub>
                    <abstract>
                        <title>Abstract</title>
                        <sec>
                            <title>inicio</title>
                            <p><bold>conteúdo de bold</bold> text </p>
                        </sec>
                        <sec>
                            <title>meio</title>
                            <p>text <bold>conteúdo de bold</bold> text </p>
                        </sec>
                        <sec>
                            <title>fim</title>
                            <p>text <bold>conteúdo de bold</bold></p>
                        </sec>
                        <sec>
                            <title>aninhado</title>
                            <p>text <bold>conteúdo <italic>de</italic> bold</bold></p>
                        </sec>
                    </abstract>
                </front-stub>
            </sub-article>
            </article>
            """)
        self.abstract = Abstract(xmltree)

    def test__main_abstract_without_tags(self):
        self.maxDiff = None
        expected = {
            "lang": "en",
            'parent_name': 'article',
            "abstract": 'conteúdo de bold text text conteúdo de bold text text conteúdo de bold text conteúdo de bold',
        }
        result = self.abstract.get_main_abstract(style="only_p")
        self.assertDictEqual(expected, result)

    def test_get_main_abstract_default_style(self):
        self.maxDiff = None
        """
        <sec>
            <title>inicio</title>
            <p><bold>conteúdo de bold</bold> text </p>
        </sec>
        <sec>
            <title>meio</title>
            <p>text <bold>conteúdo de bold</bold> text </p>
        </sec>
        <sec>
            <title>fim</title>
            <p>text <bold>conteúdo de bold</bold></p>
        </sec>
        <sec>
            <title>aninhado</title>
            <p>text <bold>conteúdo <italic>de</italic> bold</bold></p>
        </sec>
        """
        expected = {
            "lang": "en",
            'parent_name': 'article',
            "abstract": {
                "lang": "en",
                "title": "Abstract",
                "sections": [{
                    "title": "inicio",
                    "p": "conteúdo de bold text ",
                },
                    {
                        "title": "meio",
                        "p": "text conteúdo de bold text ",
                    },
                    {
                        "title": "fim",
                        "p": "text conteúdo de bold",
                    },
                    {
                        "title": "aninhado",
                        "p": "text conteúdo de bold",

                    }],
            }
        }
        result = self.abstract.get_main_abstract()
        self.assertDictEqual(expected, result)

    def test_get_main_abstract_default_style_html(self):
        self.maxDiff = None
        """
        <sec>
            <title>inicio</title>
            <p><bold>conteúdo de bold</bold> text </p>
        </sec>
        <sec>
            <title>meio</title>
            <p>text <bold>conteúdo de bold</bold> text </p>
        </sec>
        <sec>
            <title>fim</title>
            <p>text <bold>conteúdo de bold</bold></p>
        </sec>
        <sec>
            <title>aninhado</title>
            <p>text <bold>conteúdo <italic>de</italic> bold</bold></p>
        </sec>
        """
        expected = {
            "lang": "en",
            'parent_name': 'article',
            "abstract": {
                "lang": "en",
                "title": "<title>Abstract</title>",
                "sections": [{
                    "title": "<title>inicio</title>",
                    "p": "<b>conteúdo de bold</b> text",
                },
                    {
                        "title": "<title>meio</title>",
                        "p": "text <b>conteúdo de bold</b> text",
                    },
                    {
                        "title": "<title>fim</title>",
                        "p": "text <b>conteúdo de bold</b>",
                    },
                    {
                        "title": "<title>aninhado</title>",
                        "p": "text <b>conteúdo <i>de</i> bold</b>",

                    }],
            }
        }
        result = self.abstract.get_main_abstract(
            html=True,
            tags_to_keep=['title'],
            tags_to_convert_to_html={'bold': 'b'}
        )
        self.assertDictEqual(expected, result)

    def test_get_main_abstract_inline(self):
        self.maxDiff = None
        """
        <abstract>
                <title>Abstract</title>
                <sec>
                    <title>inicio</title>
                    <p><bold>conteúdo de bold</bold> text </p>
                </sec>
                <sec>
                    <title>meio</title>
                    <p>text <bold>conteúdo de bold</bold> text </p>
                </sec>
                <sec>
                    <title>fim</title>
                    <p>text <bold>conteúdo de bold</bold></p>
                </sec>
                <sec>
                    <title>aninhado</title>
                    <p>text <bold>conteúdo <italic>de</italic> bold</bold></p>
                </sec>
            </abstract>
        """
        expected = {
            "lang": "en",
            'parent_name': 'article',
            "abstract": 'Abstract inicio conteúdo de bold text meio text conteúdo de bold '
                        'text fim text conteúdo de bold aninhado text conteúdo de bold',
        }
        result = self.abstract.get_main_abstract(style="inline")
        self.assertDictEqual(expected, result)

    def test_get_main_abstract_inline_html(self):
        self.maxDiff = None
        """
        <abstract>
                <title>Abstract</title>
                <sec>
                    <title>inicio</title>
                    <p><bold>conteúdo de bold</bold> text </p>
                </sec>
                <sec>
                    <title>meio</title>
                    <p>text <bold>conteúdo de bold</bold> text </p>
                </sec>
                <sec>
                    <title>fim</title>
                    <p>text <bold>conteúdo de bold</bold></p>
                </sec>
                <sec>
                    <title>aninhado</title>
                    <p>text <bold>conteúdo <italic>de</italic> bold</bold></p>
                </sec>
            </abstract>
        """
        expected = {
            "lang": "en",
            'parent_name': 'article',
            "abstract": 'Abstract inicio <b>conteúdo de bold</b> text meio text <b>conteúdo de bold</b> '
                        'text fim text <b>conteúdo de bold</b> aninhado text <b>conteúdo <i>de</i> bold</b>',
        }
        result = self.abstract.get_main_abstract(
            style="inline",
            html=True,
            tags_to_convert_to_html={'bold': 'b'}
        )
        self.assertDictEqual(expected, result)

    def test_get_main_abstract_xml(self):
        """
        <title>Abstract</title>
        <sec>
            <title>Objective</title>
            <p>To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people.</p>
        </sec>
        <sec>
            <title>Design</title>
            <p>Systematic review of 12 controlled <italic>clinical trials</italic> (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials).</p>
        </sec>
        """
        self.maxDiff = None
        expected = {
            "lang": "en",
            'parent_name': 'article',
            "abstract": "<title>Abstract</title><sec><title>inicio</title><p><bold>conteúdo de bold</bold> text </p>"
                        "</sec><sec><title>meio</title><p>text <bold>conteúdo de bold</bold> text </p></sec><sec>"
                        "<title>fim</title><p>text <bold>conteúdo de bold</bold></p></sec><sec><title>aninhado</title>"
                        "<p>text <bold>conteúdo <italic>de</italic> bold</bold></p></sec>",
        }
        result = self.abstract.get_main_abstract(style="xml")
        self.assertEqual(expected["lang"], result["lang"])
        self.assertIn("<title>Abstract</title>", result["abstract"])
        self.assertIn("<p><bold>conteúdo de bold</bold> text </p>", result["abstract"])
        self.assertIn("<p>text <bold>conteúdo de bold</bold> text </p>", result["abstract"])
        self.assertIn("<p>text <bold>conteúdo de bold</bold></p>", result["abstract"])
        self.assertIn("<p>text <bold>conteúdo <italic>de</italic> bold</bold></p>", result["abstract"])

    def test_get_main_abstract_only_p(self):
        """
        <abstract>
                <title>Abstract</title>
                <sec>
                    <title>inicio</title>
                    <p><bold>conteúdo de bold</bold> text </p>
                </sec>
                <sec>
                    <title>meio</title>
                    <p>text <bold>conteúdo de bold</bold> text </p>
                </sec>
                <sec>
                    <title>fim</title>
                    <p>text <bold>conteúdo de bold</bold></p>
                </sec>
                <sec>
                    <title>aninhado</title>
                    <p>text <bold>conteúdo <italic>de</italic> bold</bold></p>
                </sec>
            </abstract>
        """
        expected = {
            "lang": "en",
            'parent_name': 'article',
            "abstract": 'conteúdo de bold text text conteúdo de bold text text conteúdo de bold text conteúdo de bold',
        }
        result = self.abstract.get_main_abstract(style="only_p")
        self.assertDictEqual(expected, result)

    def test_get_main_abstract_only_p_html(self):
        """
        <abstract>
                <title>Abstract</title>
                <sec>
                    <title>inicio</title>
                    <p><bold>conteúdo de bold</bold> text </p>
                </sec>
                <sec>
                    <title>meio</title>
                    <p>text <bold>conteúdo de bold</bold> text </p>
                </sec>
                <sec>
                    <title>fim</title>
                    <p>text <bold>conteúdo de bold</bold></p>
                </sec>
                <sec>
                    <title>aninhado</title>
                    <p>text <bold>conteúdo <italic>de</italic> bold</bold></p>
                </sec>
            </abstract>
        """
        expected = {
            "lang": "en",
            'parent_name': 'article',
            "abstract": '<b>conteúdo de bold</b> text text <b>conteúdo de bold</b> text text <b>conteúdo de bold</b> '
                        'text <b>conteúdo <i>de</i> bold</b>',
        }
        result = self.abstract.get_main_abstract(
            style="only_p",
            html=True,
            tags_to_convert_to_html={'italic': 'i', 'bold': 'b'}
        )
        self.assertDictEqual(expected, result)

    def test__get_sub_article_abstracts(self):
        self.maxDiff = None
        """
        <sub-article article-type="translation" id="01" xml:lang="es">
            <front-stub>
                <abstract>
                    <title>Abstract</title>
                    <sec>
                        <title>inicio</title>
                        <p><bold>conteúdo de bold</bold> text </p>
                    </sec>
                    <sec>
                        <title>meio</title>
                        <p>text <bold>conteúdo de bold</bold> text </p>
                    </sec>
                    <sec>
                        <title>fim</title>
                        <p>text <bold>conteúdo de bold</bold></p>
                    </sec>
                    <sec>
                        <title>aninhado</title>
                        <p>text <bold>conteúdo <italic>de</italic> bold</bold></p>
                    </sec>
                </abstract>
            </front-stub>
        </sub-article>
        """
        self.maxDiff = None
        expected = (
            {
                "lang": "es",
                'parent_name': 'sub-article',
                "abstract": {
                    "lang": "es",
                    "title": "Abstract",
                    "sections": [
                        {
                            "title": "inicio",
                            "p": "conteúdo de bold text "
                        },
                        {
                            "title": "meio",
                            "p": "text conteúdo de bold text "
                        },
                        {
                            "title": "fim",
                            "p": "text conteúdo de bold"
                        },
                        {
                            "title": "aninhado",
                            "p": "text conteúdo de bold"
                        },
                    ]
                },
                "id": "01"
            },
        )
        result = self.abstract._get_sub_article_abstracts()
        for res, exp in zip(result, expected):
            with self.subTest(res["lang"]):
                self.assertDictEqual(exp, res)

    def test__get_sub_article_abstracts_html(self):
        self.maxDiff = None
        """
        <sub-article article-type="translation" id="01" xml:lang="es">
            <front-stub>
                <abstract>
                    <title>Abstract</title>
                    <sec>
                        <title>inicio</title>
                        <p><bold>conteúdo de bold</bold> text </p>
                    </sec>
                    <sec>
                        <title>meio</title>
                        <p>text <bold>conteúdo de bold</bold> text </p>
                    </sec>
                    <sec>
                        <title>fim</title>
                        <p>text <bold>conteúdo de bold</bold></p>
                    </sec>
                    <sec>
                        <title>aninhado</title>
                        <p>text <bold>conteúdo <italic>de</italic> bold</bold></p>
                    </sec>
                </abstract>
            </front-stub>
        </sub-article>
        """
        self.maxDiff = None
        expected = (
            {
                "lang": "es",
                'parent_name': 'sub-article',
                "abstract": {
                    "lang": "es",
                    "title": "Abstract",
                    "sections": [
                        {
                            "title": "inicio",
                            "p": "<b>conteúdo de bold</b> text"
                        },
                        {
                            "title": "meio",
                            "p": "text <b>conteúdo de bold</b> text"
                        },
                        {
                            "title": "fim",
                            "p": "text <b>conteúdo de bold</b>"
                        },
                        {
                            "title": "aninhado",
                            "p": "text <b>conteúdo <i>de</i> bold</b>"
                        },
                    ]
                },
                "id": "01"
            },
        )
        result = self.abstract._get_sub_article_abstracts(
            html=True,
            tags_to_convert_to_html={'italic': 'i', 'bold': 'b'}
        )
        for res, exp in zip(result, expected):
            with self.subTest(res["lang"]):
                self.assertDictEqual(exp, res)

    def test__get_trans_abstracts(self):
        """
        <trans-abstract xml:lang="pt">
            <title>Abstract</title>
            <sec>
                <title>inicio</title>
                <p><bold>conteúdo de bold</bold> text </p>
            </sec>
            <sec>
                <title>meio</title>
                <p>text <bold>conteúdo de bold</bold> text </p>
            </sec>
            <sec>
                <title>fim</title>
                <p>text <bold>conteúdo de bold</bold></p>
            </sec>
            <sec>
                <title>aninhado</title>
                <p>text <bold>conteúdo <italic>de</italic> bold</bold></p>
            </sec>
        </trans-abstract>
        """
        self.maxDiff = None
        expected = (
            {
                "lang": "pt",
                'parent_name': 'article',
                "abstract": {
                    "lang": "pt",
                    "title": "Abstract",
                    "sections": [
                        {
                            "title": "inicio",
                            "p": "<b>conteúdo de bold</b> text"
                        },
                        {
                            "title": "meio",
                            "p": "text <b>conteúdo de bold</b> text"
                        },
                        {
                            "title": "fim",
                            "p": "text <b>conteúdo de bold</b>"
                        },
                        {
                            "title": "aninhado",
                            "p": "text <b>conteúdo <i>de</i> bold</b>"
                        },
                    ]
                }
            },
        )
        result = self.abstract._get_trans_abstracts(
            html=True,
            tags_to_convert_to_html={'italic': 'i', 'bold': 'b'}
        )
        for res, exp in zip(result, expected):
            with self.subTest(exp["lang"]):
                self.assertDictEqual(exp, res)


class ArticleAbstractTest(TestCase):

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
                    <title>inicio</title>
                    <p><bold>conteúdo de bold</bold> text </p>
                </sec>
                <sec>
                    <title>meio</title>
                    <p>text <bold>conteúdo de bold</bold> text </p>
                </sec>
                <sec>
                    <title>fim</title>
                    <p>text <bold>conteúdo de bold</bold></p>
                </sec>
                <sec>
                    <title>aninhado</title>
                    <p>text <bold>conteúdo <italic>de</italic> bold</bold></p>
                </sec>
            </abstract>
            <trans-abstract xml:lang="pt">
                <title>Abstract</title>
                <sec>
                    <title>inicio</title>
                    <p><bold>conteúdo de bold</bold> text</p>
                </sec>
                <sec>
                    <title>meio</title>
                    <p>text <bold>conteúdo de bold</bold> text</p>
                </sec>
                <sec>
                    <title>fim</title>
                    <p>text <bold>conteúdo de bold</bold></p>
                </sec>
                <sec>
                    <title>aninhado</title>
                    <p>text <bold>conteúdo <italic>de</italic> bold</bold></p>
                </sec>
            </trans-abstract>
            </article-meta>
            </front>
            <sub-article article-type="translation" id="01" xml:lang="es">
                <front-stub>
                    <abstract>
                        <title>Abstract</title>
                        <sec>
                            <title>inicio</title>
                            <p><bold>conteúdo de bold</bold> text</p>
                        </sec>
                        <sec>
                            <title>meio</title>
                            <p>text <bold>conteúdo de bold</bold> text</p>
                        </sec>
                        <sec>
                            <title>fim</title>
                            <p>text <bold>conteúdo de bold</bold></p>
                        </sec>
                        <sec>
                            <title>aninhado</title>
                            <p>text <bold>conteúdo <italic>de</italic> bold</bold></p>
                        </sec>
                    </abstract>
                </front-stub>
            </sub-article>
            </article>
            """)
        self.abstract = ArticleAbstract(xmltree)

    def test_get_main_abstract(self):
        self.maxDiff = None
        expected = [
            {
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'lang': 'en',
                'abstract_type': None,
                'html_text': 'Abstract inicio <b>conteúdo de bold</b> text meio text <b>conteúdo de bold</b> text fim text '
                             '<b>conteúdo de bold</b> aninhado text <b>conteúdo <i>de</i> bold</b>',
                'plain_text': 'Abstract inicio conteúdo de bold text meio text conteúdo de bold text fim text conteúdo de '
                              'bold aninhado text conteúdo de bold'
            }
        ]
        self.abstract.configure(tags_to_convert_to_html={'bold': 'b'})
        self.assertEqual(expected, list(self.abstract.get_main_abstract()))

    def test_get_main_abstract_structured(self):
        self.maxDiff = None
        expected = [
            {
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'lang': 'en',
                'abstract_type': None,
                'title': {'html_text': 'Abstract', 'lang': 'en', 'plain_text': 'Abstract'},
                'sections': [
                    {
                        'p': {'html_text': '<b>conteúdo de bold</b> text', 'lang': 'en', 'plain_text': 'conteúdo de bold text'},
                        'title': {'html_text': 'inicio', 'lang': 'en', 'plain_text': 'inicio'}
                    },
                    {
                        'p': {'html_text': 'text <b>conteúdo de bold</b> text', 'lang': 'en',
                              'plain_text': 'text conteúdo de bold text'},
                        'title': {'html_text': 'meio', 'lang': 'en', 'plain_text': 'meio'}
                    },
                    {
                        'p': {'html_text': 'text <b>conteúdo de bold</b>', 'lang': 'en',
                              'plain_text': 'text conteúdo de bold'},
                        'title': {'html_text': 'fim', 'lang': 'en', 'plain_text': 'fim'}
                    },
                    {
                        'p': {'html_text': 'text <b>conteúdo <i>de</i> bold</b>', 'lang': 'en',
                              'plain_text': 'text conteúdo de bold'},
                        'title': {'html_text': 'aninhado', 'lang': 'en', 'plain_text': 'aninhado'}
                    }
                ]
            }
        ]
        self.abstract.configure(tags_to_convert_to_html={'bold': 'b'})
        self.assertEqual(expected, list(self.abstract.get_main_abstract(structured=True)))

    def test_get_sub_article_abstract(self):
        self.maxDiff = None
        expected = [
            {
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': '01',
                'parent_lang': 'es',
                'lang': 'es',
                'id': '01',
                'abstract_type': None,
                'html_text': 'Abstract inicio <b>conteúdo de bold</b> text meio text <b>conteúdo de bold</b> text fim text '
                             '<b>conteúdo de bold</b> aninhado text <b>conteúdo <i>de</i> bold</b>',
                'plain_text': 'Abstract inicio conteúdo de bold text meio text conteúdo de bold text fim text conteúdo de '
                              'bold aninhado text conteúdo de bold'
            }
        ]
        self.abstract.configure(tags_to_convert_to_html={'bold': 'b'})
        obtained = list(self.abstract.get_sub_article_abstract())
        for i, abstract in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(abstract, obtained[i])

    def test_get_sub_article_abstract_structured(self):
        self.maxDiff = None
        expected = [
            {
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': '01',
                'parent_lang': 'es',
                'lang': 'es',
                'id': '01',
                'abstract_type': None,
                'title': {'html_text': 'Abstract', 'lang': 'es', 'plain_text': 'Abstract'},
                'sections': [
                    {
                        'p': {'html_text': '<b>conteúdo de bold</b> text', 'lang': 'es', 'plain_text': 'conteúdo de bold text'},
                        'title': {'html_text': 'inicio', 'lang': 'es', 'plain_text': 'inicio'}
                    },
                    {
                        'p': {'html_text': 'text <b>conteúdo de bold</b> text', 'lang': 'es', 'plain_text': 'text conteúdo de bold text'},
                        'title': {'html_text': 'meio', 'lang': 'es', 'plain_text': 'meio'}
                    },
                    {
                        'p': {'html_text': 'text <b>conteúdo de bold</b>', 'lang': 'es', 'plain_text': 'text conteúdo de bold'},
                        'title': {'html_text': 'fim', 'lang': 'es', 'plain_text': 'fim'}
                    },
                    {
                        'p': {'html_text': 'text <b>conteúdo <i>de</i> bold</b>', 'lang': 'es', 'plain_text': 'text conteúdo de bold'},
                        'title': {'html_text': 'aninhado', 'lang': 'es', 'plain_text': 'aninhado'}
                    }
                ]
            }
        ]
        self.abstract.configure(tags_to_convert_to_html={'bold': 'b'})
        obtained = list(self.abstract.get_sub_article_abstract(structured=True))
        for i, abstract in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(abstract, obtained[i])

    def test_get_trans_abstract(self):
        self.maxDiff = None
        expected = [
            {
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'lang': 'pt',
                'abstract_type': None,
                'html_text': 'Abstract inicio <b>conteúdo de bold</b> text meio text <b>conteúdo de bold</b> text fim text '
                             '<b>conteúdo de bold</b> aninhado text <b>conteúdo <i>de</i> bold</b>',
                'plain_text': 'Abstract inicio conteúdo de bold text meio text conteúdo de bold text fim text conteúdo de '
                              'bold aninhado text conteúdo de bold'
            }
        ]
        self.abstract.configure(tags_to_convert_to_html={'bold': 'b'})
        obtained = list(self.abstract.get_trans_abstract())
        for i, abstract in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(abstract, obtained[i])

    def test_get_trans_abstract_structured(self):
        self.maxDiff = None
        expected = [
            {
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'lang': 'pt',
                'abstract_type': None,
                'title': {'html_text': 'Abstract', 'lang': 'pt', 'plain_text': 'Abstract'},
                'sections': [
                        {
                            'p': {'html_text': '<b>conteúdo de bold</b> text', 'lang': 'pt', 'plain_text': 'conteúdo de bold text'},
                            'title': {'html_text': 'inicio', 'lang': 'pt', 'plain_text': 'inicio'}
                        },
                        {
                            'p': {'html_text': 'text <b>conteúdo de bold</b> text', 'lang': 'pt', 'plain_text': 'text conteúdo de bold text'},
                            'title': {'html_text': 'meio', 'lang': 'pt', 'plain_text': 'meio'}
                        },
                        {
                            'p': {'html_text': 'text <b>conteúdo de bold</b>', 'lang': 'pt', 'plain_text': 'text conteúdo de bold'},
                            'title': {'html_text': 'fim', 'lang': 'pt', 'plain_text': 'fim'}
                        },
                        {
                            'p': {'html_text': 'text <b>conteúdo <i>de</i> bold</b>', 'lang': 'pt', 'plain_text': 'text conteúdo de bold'},
                            'title': {'html_text': 'aninhado', 'lang': 'pt', 'plain_text': 'aninhado'}
                        }
                    ]
            }
        ]
        self.abstract.configure(tags_to_convert_to_html={'bold': 'b'})
        obtained = list(self.abstract.get_trans_abstract(structured=True))
        for i, abstract in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(abstract, obtained[i])

    def test_get_abstracts(self):
        self.maxDiff = None
        expected = [
            {
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'lang': 'en',
                'abstract_type': None,
                'title': {'html_text': 'Abstract', 'lang': 'en', 'plain_text': 'Abstract'},
                'sections': [
                    {
                        'p': {'html_text': '<b>conteúdo de bold</b> text', 'lang': 'en',
                              'plain_text': 'conteúdo de bold text'},
                        'title': {'html_text': 'inicio', 'lang': 'en', 'plain_text': 'inicio'}
                    },
                    {
                        'p': {'html_text': 'text <b>conteúdo de bold</b> text', 'lang': 'en',
                              'plain_text': 'text conteúdo de bold text'},
                        'title': {'html_text': 'meio', 'lang': 'en', 'plain_text': 'meio'}
                    },
                    {
                        'p': {'html_text': 'text <b>conteúdo de bold</b>', 'lang': 'en',
                              'plain_text': 'text conteúdo de bold'},
                        'title': {'html_text': 'fim', 'lang': 'en', 'plain_text': 'fim'}
                    },
                    {
                        'p': {'html_text': 'text <b>conteúdo <i>de</i> bold</b>', 'lang': 'en',
                              'plain_text': 'text conteúdo de bold'},
                        'title': {'html_text': 'aninhado', 'lang': 'en', 'plain_text': 'aninhado'}
                    }
                ]
            },
            {
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': '01',
                'parent_lang': 'es',
                'lang': 'es',
                'id': '01',
                'abstract_type': None,
                'title': {'html_text': 'Abstract', 'lang': 'es', 'plain_text': 'Abstract'},
                'sections': [
                    {
                        'p': {'html_text': '<b>conteúdo de bold</b> text', 'lang': 'es',
                              'plain_text': 'conteúdo de bold text'},
                        'title': {'html_text': 'inicio', 'lang': 'es', 'plain_text': 'inicio'}
                    },
                    {
                        'p': {'html_text': 'text <b>conteúdo de bold</b> text', 'lang': 'es',
                              'plain_text': 'text conteúdo de bold text'},
                        'title': {'html_text': 'meio', 'lang': 'es', 'plain_text': 'meio'}
                    },
                    {
                        'p': {'html_text': 'text <b>conteúdo de bold</b>', 'lang': 'es',
                              'plain_text': 'text conteúdo de bold'},
                        'title': {'html_text': 'fim', 'lang': 'es', 'plain_text': 'fim'}
                    },
                    {
                        'p': {'html_text': 'text <b>conteúdo <i>de</i> bold</b>', 'lang': 'es',
                              'plain_text': 'text conteúdo de bold'},
                        'title': {'html_text': 'aninhado', 'lang': 'es', 'plain_text': 'aninhado'}
                    }
                ]
            },
            {
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'lang': 'pt',
                'abstract_type': None,
                'title': {'html_text': 'Abstract', 'lang': 'pt', 'plain_text': 'Abstract'},
                'sections': [
                    {
                        'p': {'html_text': '<b>conteúdo de bold</b> text', 'lang': 'pt',
                              'plain_text': 'conteúdo de bold text'},
                        'title': {'html_text': 'inicio', 'lang': 'pt', 'plain_text': 'inicio'}
                    },
                    {
                        'p': {'html_text': 'text <b>conteúdo de bold</b> text', 'lang': 'pt',
                              'plain_text': 'text conteúdo de bold text'},
                        'title': {'html_text': 'meio', 'lang': 'pt', 'plain_text': 'meio'}
                    },
                    {
                        'p': {'html_text': 'text <b>conteúdo de bold</b>', 'lang': 'pt',
                              'plain_text': 'text conteúdo de bold'},
                        'title': {'html_text': 'fim', 'lang': 'pt', 'plain_text': 'fim'}
                    },
                    {
                        'p': {'html_text': 'text <b>conteúdo <i>de</i> bold</b>', 'lang': 'pt',
                              'plain_text': 'text conteúdo de bold'},
                        'title': {'html_text': 'aninhado', 'lang': 'pt', 'plain_text': 'aninhado'}
                    }
                ]
            }
        ]
        self.abstract.configure(tags_to_convert_to_html={'bold': 'b'})
        obtained = list(self.abstract.get_abstracts(structured=True))
        for i, abstract in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(abstract, obtained[i])

    def test_get_abstracts_by_lang(self):
        self.maxDiff = None
        expected = {
            'en': {
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'lang': 'en',
                'abstract_type': None,
                'html_text': 'Abstract inicio <b>conteúdo de bold</b> text meio text <b>conteúdo de bold</b> text fim text '
                             '<b>conteúdo de bold</b> aninhado text <b>conteúdo <i>de</i> bold</b>',
                'plain_text': 'Abstract inicio conteúdo de bold text meio text conteúdo de bold text fim text conteúdo de '
                              'bold aninhado text conteúdo de bold'
            },
            'es': {
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': '01',
                'parent_lang': 'es',
                'lang': 'es',
                'id': '01',
                'abstract_type': None,
                'html_text': 'Abstract inicio <b>conteúdo de bold</b> text meio text <b>conteúdo de bold</b> text fim text '
                             '<b>conteúdo de bold</b> aninhado text <b>conteúdo <i>de</i> bold</b>',
                'plain_text': 'Abstract inicio conteúdo de bold text meio text conteúdo de bold text fim text conteúdo de '
                              'bold aninhado text conteúdo de bold'
            },
            'pt': {
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'lang': 'pt',
                'abstract_type': None,
                'html_text': 'Abstract inicio <b>conteúdo de bold</b> text meio text <b>conteúdo de bold</b> text fim text '
                             '<b>conteúdo de bold</b> aninhado text <b>conteúdo <i>de</i> bold</b>',
                'plain_text': 'Abstract inicio conteúdo de bold text meio text conteúdo de bold text fim text conteúdo de '
                              'bold aninhado text conteúdo de bold'
            }
        }
        self.abstract.configure(tags_to_convert_to_html={'bold': 'b'})
        obtained = self.abstract.get_abstracts_by_lang()
        self.assertDictEqual(expected, obtained)


class HighlightTest(TestCase):
    def setUp(self):
        xmltree = ET.fromstring(
            """
            <article article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
                <front>
                    <article-meta>
                        <abstract abstract-type="key-points">
                            <title>HIGHLIGHTS</title>
                            <p>Nam vitae leo aliquet, pretium ante at, faucibus felis</p>
                            <p>Aliquam ac mauris et libero pulvinar facilisis</p>
                            <p>Fusce aliquam ipsum ut diam luctus porta</p>
                            <p>Ut a erat ac odio placerat convallis</p>
                        </abstract>
                    </article-meta>
                </front>
            </article>
            """)
        self.highlight = Highlight(xmltree.xpath('.//abstract')[0])

    def test_highlight_title(self):
        self.assertEqual(self.highlight.title, "HIGHLIGHTS")

    def test_highlights(self):
        expected = [
            'Nam vitae leo aliquet, pretium ante at, faucibus felis',
            'Aliquam ac mauris et libero pulvinar facilisis',
            'Fusce aliquam ipsum ut diam luctus porta',
            'Ut a erat ac odio placerat convallis'
        ]

        obtained = list(self.highlight.p)

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertEqual(item, obtained[i])

    def test_data(self):
        expected = {
            "title": "HIGHLIGHTS",
            'list': [],
            "highlights": [
                'Nam vitae leo aliquet, pretium ante at, faucibus felis',
                'Aliquam ac mauris et libero pulvinar facilisis',
                'Fusce aliquam ipsum ut diam luctus porta',
                'Ut a erat ac odio placerat convallis'
            ]
        }

        obtained = self.highlight.data
        self.assertEqual(expected, obtained)


class HighlightsTest(TestCase):
    def setUp(self):
        xmltree = ET.fromstring(
            """
            <article article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
                <front>
                    <article-meta>
                        <abstract abstract-type="key-points">
                            <title>HIGHLIGHTS</title>
                            <p>Nam vitae leo aliquet, pretium ante at, faucibus felis</p>
                            <p>Aliquam ac mauris et libero pulvinar facilisis</p>
                            <p>Fusce aliquam ipsum ut diam luctus porta</p>
                            <p>Ut a erat ac odio placerat convallis</p>
                        </abstract>
                    </article-meta>
                </front>
                <sub-article article-type="translation" id="01" xml:lang="es">
                    <front-stub>
                        <abstract abstract-type="key-points">
                            <title>HIGHLIGHTS</title>
                            <p>Nam vitae leo aliquet, pretium ante at, faucibus felis</p>
                            <p>Aliquam ac mauris et libero pulvinar facilisis</p>
                            <p>Fusce aliquam ipsum ut diam luctus porta</p>
                            <p>Ut a erat ac odio placerat convallis</p>
                        </abstract>
                    </front-stub>
                </sub-article>
            </article>
            """)
        self.highlights = ArticleHighlights(xmltree)

    def test_highlights(self):
        expected = [
            {
                "title": "HIGHLIGHTS",
                "highlights": [
                    'Nam vitae leo aliquet, pretium ante at, faucibus felis',
                    'Aliquam ac mauris et libero pulvinar facilisis',
                    'Fusce aliquam ipsum ut diam luctus porta',
                    'Ut a erat ac odio placerat convallis'
                ],
                'list': [],
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
            },
            {
                "title": "HIGHLIGHTS",
                "highlights": [
                    'Nam vitae leo aliquet, pretium ante at, faucibus felis',
                    'Aliquam ac mauris et libero pulvinar facilisis',
                    'Fusce aliquam ipsum ut diam luctus porta',
                    'Ut a erat ac odio placerat convallis'
                ],
                'list': [],
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': '01',
                'parent_lang': 'es',
            }
        ]

        obtained = list(self.highlights.article_highlights())

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])


class HighlightsTransAbstractTest(TestCase):
    def setUp(self):
        xmltree = ET.fromstring(
            """
            <article article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
                <front>
                    <article-meta>
                        <abstract abstract-type="key-points">
                            <title>HIGHLIGHTS</title>
                            <p>Nam vitae leo aliquet, pretium ante at, faucibus felis</p>
                            <p>Aliquam ac mauris et libero pulvinar facilisis</p>
                            <p>Fusce aliquam ipsum ut diam luctus porta</p>
                            <p>Ut a erat ac odio placerat convallis</p>
                        </abstract>
                        <trans-abstract abstract-type="key-points">
                            <title>HIGHLIGHTS</title>
                            <p>Nam vitae leo aliquet, pretium ante at, faucibus felis</p>
                            <p>Aliquam ac mauris et libero pulvinar facilisis</p>
                            <p>Fusce aliquam ipsum ut diam luctus porta</p>
                            <p>Ut a erat ac odio placerat convallis</p>
                        </trans-abstract>
                    </article-meta>
                </front>
            </article>
            """)
        self.highlights = ArticleHighlights(xmltree)

    def test_highlights(self):
        expected = [
            {
                "title": "HIGHLIGHTS",
                "highlights": [
                    'Nam vitae leo aliquet, pretium ante at, faucibus felis',
                    'Aliquam ac mauris et libero pulvinar facilisis',
                    'Fusce aliquam ipsum ut diam luctus porta',
                    'Ut a erat ac odio placerat convallis'
                ],
                'list': [],
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
            },
            {
                "title": "HIGHLIGHTS",
                "highlights": [
                    'Nam vitae leo aliquet, pretium ante at, faucibus felis',
                    'Aliquam ac mauris et libero pulvinar facilisis',
                    'Fusce aliquam ipsum ut diam luctus porta',
                    'Ut a erat ac odio placerat convallis'
                ],
                'list': [],
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
            }
        ]

        obtained = list(self.highlights.article_highlights())

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])


class VisualAbstractTest(TestCase):
    def setUp(self):
        xmltree = ET.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" dtd-version="1.1" 
            specific-use="sps-1.9" xml:lang="en">
                <front>
                    <article-meta>
                        <abstract abstract-type="graphical">
                            <title>Visual Abstract</title>
                                <p>
                                    <fig id="vf01">
                                        <caption>
                                            <title>Título</title>
                                        </caption>
                                        <graphic xlink:href="1234-5678-zwy-12-04-0123-vs01.tif"/>
                                    </fig>
                                </p>
                        </abstract>
                    </article-meta>
                </front>
            </article>
            """)
        self.visual_abstract = VisualAbstract(xmltree.xpath('.//abstract')[0])

    def test_title(self):
        self.assertEqual(self.visual_abstract.title, "Visual Abstract")

    def test_fig_id(self):
        self.assertEqual(self.visual_abstract.fig_id, "vf01")

    def test_caption(self):
        self.assertEqual(self.visual_abstract.caption, "Título")

    def test_graphic(self):
        self.assertEqual(self.visual_abstract.graphic, "1234-5678-zwy-12-04-0123-vs01.tif")

    def test_data(self):
        expected = {
            "title": "Visual Abstract",
            "fig_id": "vf01",
            "caption": "Título",
            "graphic": "1234-5678-zwy-12-04-0123-vs01.tif"
        }

        obtained = self.visual_abstract.data

        self.assertDictEqual(expected, obtained)


class VisualAbstractsTest(TestCase):
    def setUp(self):
        xmltree = ET.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" dtd-version="1.1" 
            specific-use="sps-1.9" xml:lang="en">
                <front>
                    <article-meta>
                        <abstract abstract-type="graphical">
                            <title>Visual Abstract</title>
                                <p>
                                    <fig id="vf01">
                                        <caption>
                                            <title>Título</title>
                                        </caption>
                                        <graphic xlink:href="1234-5678-zwy-12-04-0123-vs01.tif"/>
                                    </fig>
                                </p>
                        </abstract>
                    </article-meta>
                </front>
                <sub-article article-type="translation" id="01" xml:lang="es">
                    <front-stub>
                        <abstract abstract-type="graphical">
                            <title>Visual Abstract</title>
                                <p>
                                    <fig id="vf01">
                                        <caption>
                                            <title>Título</title>
                                        </caption>
                                        <graphic xlink:href="1234-5678-zwy-12-04-0123-vs01.tif"/>
                                    </fig>
                                </p>
                        </abstract>
                    </front-stub>
                </sub-article>
            </article>
            """)
        self.visual_abstracts = ArticleVisualAbstracts(xmltree)

    def test_visual_abstracts(self):
        expected = [
            {
                "title": "Visual Abstract",
                "fig_id": "vf01",
                "caption": "Título",
                "graphic": "1234-5678-zwy-12-04-0123-vs01.tif",
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'en',
            },
            {
                "title": "Visual Abstract",
                "fig_id": "vf01",
                "caption": "Título",
                "graphic": "1234-5678-zwy-12-04-0123-vs01.tif",
                'parent': 'sub-article',
                'parent_id': '01',
                'parent_article_type': 'translation',
                'parent_lang': 'es',
            },
        ]

        obtained = list(self.visual_abstracts.article_visual_abstracts())

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])


class VisualTransAbstractsTest(TestCase):
    def setUp(self):
        xmltree = ET.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" dtd-version="1.1" 
            specific-use="sps-1.9" xml:lang="en">
                <front>
                    <article-meta>
                        <abstract abstract-type="graphical">
                            <title>Visual Abstract</title>
                                <p>
                                    <fig id="vf01">
                                        <caption>
                                            <title>Título</title>
                                        </caption>
                                        <graphic xlink:href="1234-5678-zwy-12-04-0123-vs01.tif"/>
                                    </fig>
                                </p>
                        </abstract>
                        <trans-abstract abstract-type="graphical" xml:lang="pt">
                            <title>Visual Abstract</title>
                                <p>
                                    <fig id="vf01">
                                        <caption>
                                            <title>Título</title>
                                        </caption>
                                        <graphic xlink:href="1234-5678-zwy-12-04-0123-vs01.tif"/>
                                    </fig>
                                </p>
                        </trans-abstract>
                    </article-meta>
                </front>
            </article>
            """)
        self.visual_abstracts = ArticleVisualAbstracts(xmltree)

    def test_visual_abstracts(self):
        expected = [
            {
                "title": "Visual Abstract",
                "fig_id": "vf01",
                "caption": "Título",
                "graphic": "1234-5678-zwy-12-04-0123-vs01.tif",
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'en',
            },
            {
                "title": "Visual Abstract",
                "fig_id": "vf01",
                "caption": "Título",
                "graphic": "1234-5678-zwy-12-04-0123-vs01.tif",
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'en',
            },
        ]

        obtained = list(self.visual_abstracts.article_visual_abstracts())

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])
