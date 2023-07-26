"""<article>
<front>
    <article-meta>
      <article-categories>
        <subj-group subj-group-type="heading">
          <subject>Human and Social Management</subject>
        </subj-group>
      </article-categories>
      <title-group>
        <article-title>Inmunización de Flujos Financieros con Futuros de Tasas de Interés: un Análisis de Duración y Convexidad con el Modelo de Nelson y Siegel</article-title>
        <trans-title-group xml:lang="en">
          <trans-title>&gt;HEDGING FUTURE CASH FLOWS WITH INTEREST-RATE FUTURES CONTRACTS: A DURATION AND CONVEXITY ANALYSIS UNDER THE NELSON &amp; SIEGEL MODEL</trans-title>
        </trans-title-group>
      </title-group>
      <contrib-group>
        <contrib contrib-type="author">
          <name>
            <surname>VENEGAS-MARTÍNEZ</surname>
            <given-names>FRANCISCO</given-names>
          </name>
          <xref ref-type="aff" rid="aff1"/>
        </contrib>
      </contrib-group>
      <aff id="aff1">
        <institution content-type="orgname">Centro de Investigación en Finanzas</institution>
        <institution content-type="orgdiv1">Instituto Tecnológico y de Estudios Superiores de Monterrey (ITESM)</institution>
        <addr-line>
          <city>Tlalpan</city>
          <postal-code>14380</postal-code>
        </addr-line>
        <country country="MX">México</country>
        <email>fvenegas@campus.ccm.itesm.mx</email>
        <institution content-type="original">Director del Centro de Investigación en Finanzas, Instituto Tecnológico y de Estudios Superiores de Monterrey (ITESM), Campus Ciudad de México. Calle del Puente 222, Aulas 3, Cuarto piso, Col. Ejidos de Huipulco, Del. Tlalpan, 14380 México, D. F., E-mail: fvenegas@campus.ccm.itesm.mx</institution>
      </aff>
      <pub-date publication-format="electronic" date-type="pub">
        <day>20</day>
        <month>04</month>
        <year>2022</year>
      </pub-date>
      <pub-date publication-format="electronic" date-type="collection">
        <year>2003</year>
      </pub-date>
      <volume>4</volume>
      <issue>1</issue>
      <fpage>108</fpage>
      <lpage>123</lpage>
      <history>
        <date date-type="received">
          <day>18</day>
          <month>10</month>
          <year>2002</year>
        </date>
        <date date-type="accepted">
          <day>20</day>
          <month>12</month>
          <year>2002</year>
        </date>
      </history>
      <permissions>
        <license license-type="open-access" xlink:href="https://creativecommons.org/licenses/by/4.0/" xml:lang="es">
          <license-p>Este é um artigo publicado em acesso aberto (Open Access) sob a licença Creative Commons Attribution, que permite uso, distribuição e reprodução em qualquer meio, sem restrições desde que o trabalho original seja corretamente citado.</license-p>
        </license>
      </permissions>
      <abstract>
        <title>RESUMEN</title>
        <p>En este trabajo se presenta un modelo de inmunización de flujos financieros, pasivos y activos, contra el riesgo de tasa de interés mediante el uso de contratos a futuros sobre CETES (títulos de deuda pública del gobierno Mexicano). Las estrategias de cobertura que se derivan del modelo propuesto conducen a una reducción significativa del riesgo de mercado. Los conceptos de duración y convexidad monetaria desempeñan un papel importante en el desarrollo del modelo en cuanto a la medición y el control del riesgo. Específicamente, se controla el riesgo de desplazamientos paralelos y moderados en la estructura intertemporal de la tasa de interés y no existe control sobre otros riesgos. La robustez de las estrategias obtenidas se evalúa con la metodología de valor en riesgo. A manera de ilustración, el modelo desarrollado es aplicado en la cobertura de un conjunto de flujos financieros.</p>
      </abstract>
      <trans-abstract xml:lang="en">
        <title>ABSTRACT</title>
        <p>In this paper we present a model to immunize a future stream of assets and liabilities against interest-rate risk by means of futures contracts on government bonds. The hedging strategies derived from the model reduce significantly the market risk. The concepts of dollar duration and dollar convexity play an important role in measuring and controlling interest-rate risk. Specifically, the risk of small or moderate parallel shifts in the term structure of interest rate is controlled, there is no control on other risks. The robustness of the derived strategies is assessed in terms of the methodology of value at risk. An application is addressed by the way of illustration.</p>
      </trans-abstract>
      <kwd-group xml:lang="es">
        <title>PALABRAS CLAVE</title>
        <kwd>Inmunización de portafolios</kwd>
        <kwd>Riesgo de tasa de interés</kwd>
        <kwd>Futuros</kwd>
        <kwd>Valor en riesgo</kwd>
      </kwd-group>
      <kwd-group xml:lang="en">
        <title>KEYWORDS</title>
        <kwd>Portfolio immunization</kwd>
        <kwd>Interest-rate risk</kwd>
        <kwd>Futures contracts</kwd>
        <kwd>Value at risk</kwd>
      </kwd-group>
    </article-meta>
  </front>
</article>
"""

from unittest import TestCase

from lxml import etree

from packtools.sps.models.article_titles import ArticleTitles


class ArticleTitlesTest(TestCase):
    def setUp(self):
        xml = ("""
        <article xml:lang="es">
        <front>
            <article-meta>
              <title-group>
                <article-title>Inmunización de <bold>Flujos Financieros</bold> con Futuros de Tasas de Interés<xref>*</xref>: un Análisis de Duración y Convexidad con el Modelo de Nelson y Siegel</article-title>
                <trans-title-group xml:lang="en">
                  <trans-title>&gt;HEDGING FUTURE CASH FLOWS WITH INTEREST-RATE FUTURES CONTRACTS: A DURATION AND CONVEXITY ANALYSIS UNDER THE NELSON &amp; SIEGEL MODEL</trans-title>
                </trans-title-group>
              </title-group>
            </article-meta>
          </front>
        </article>
        """)
        xmltree = etree.fromstring(xml)
        self.article_titles = ArticleTitles(xmltree)

    def test_data(self):
        expected = [{
            "lang": "es",
            "text": (
                "Inmunización de <bold>Flujos Financieros</bold> con Futuros "
                "de Tasas de Interés: un Análisis de Duración y"
                " Convexidad con el Modelo de Nelson y Siegel"
            ),
            "plain_text": (
                "Inmunización de Flujos Financieros con Futuros "
                "de Tasas de Interés: un Análisis de Duración y"
                " Convexidad con el Modelo de Nelson y Siegel"
            ),
        },
        {
            "lang": "en",
            "text": (
                ">HEDGING FUTURE CASH FLOWS WITH INTEREST-RATE "
                "FUTURES CONTRACTS: A DURATION AND CONVEXITY ANALYSIS UNDER "
                "THE NELSON & SIEGEL MODEL"
            ),
            "plain_text": (
                ">HEDGING FUTURE CASH FLOWS WITH INTEREST-RATE "
                "FUTURES CONTRACTS: A DURATION AND CONVEXITY ANALYSIS UNDER "
                "THE NELSON & SIEGEL MODEL"
            ),
        },
        ]
        for i, item in enumerate(self.article_titles.data):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)


class SubArticleTitlesTest(TestCase):
    def setUp(self):
        xml = ("""
        <article xml:lang="es">
        <front>
            <article-meta>
              <title-group>
                <article-title>Inmunización de <bold>Flujos Financieros</bold> con Futuros de Tasas de Interés<xref>*</xref>: un Análisis de Duración y Convexidad con el Modelo de Nelson y Siegel</article-title>
              </title-group>
            </article-meta>
          </front>
            <sub-article article-type="translation" xml:lang="en">

            <front-stub>

                <title-group>
                <article-title>&gt;HEDGING FUTURE CASH FLOWS WITH INTEREST-RATE FUTURES CONTRACTS: A DURATION AND CONVEXITY ANALYSIS UNDER THE NELSON &amp; SIEGEL MODEL</article-title>
                </title-group>

            </front-stub>
            </sub-article>
        </article>
        """)
        xmltree = etree.fromstring(xml)
        self.article_titles = ArticleTitles(xmltree)

    def test_data(self):
        expected = [{
            "lang": "es",
            "text": (
                "Inmunización de <bold>Flujos Financieros</bold> con Futuros "
                "de Tasas de Interés: un Análisis de Duración y"
                " Convexidad con el Modelo de Nelson y Siegel"
            ),
            "plain_text": (
                "Inmunización de Flujos Financieros con Futuros "
                "de Tasas de Interés: un Análisis de Duración y"
                " Convexidad con el Modelo de Nelson y Siegel"
            ),
        },
        {
            "lang": "en",
            "text": (
                ">HEDGING FUTURE CASH FLOWS WITH INTEREST-RATE "
                "FUTURES CONTRACTS: A DURATION AND CONVEXITY ANALYSIS UNDER "
                "THE NELSON & SIEGEL MODEL"
            ),
            "plain_text": (
                ">HEDGING FUTURE CASH FLOWS WITH INTEREST-RATE "
                "FUTURES CONTRACTS: A DURATION AND CONVEXITY ANALYSIS UNDER "
                "THE NELSON & SIEGEL MODEL"
            ),
        },
        ]
        for i, item in enumerate(self.article_titles.data):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)
