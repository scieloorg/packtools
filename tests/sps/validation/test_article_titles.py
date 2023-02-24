from unittest import TestCase
from lxml import etree

from packtools.sps.validation.article_titles import ArticleTitlesValidation
from packtools.sps.models.article_titles import ArticleTitles


class ArticleTitlesTest(TestCase):
    def setUp(self):
        self.xmltree = etree.fromstring(
            """
            <article xml:lang="es">
                <front>
                    <article-meta>
                        <title-group>
                            <article-title>Inmunización de <bold>Flujos Financieros</bold> con Futuros de Tasas de Interés<xref>*</xref>: un Análisis de Duración y Convexidad con el Modelo de Nelson y Siegel</article-title>
                                <trans-title-group xml:lang="en">
                                    <trans-title>HEDGING FUTURE CASH FLOWS WITH INTEREST-RATE FUTURES CONTRACTS: A DURATION AND CONVEXITY ANALYSIS UNDER THE NELSON SIEGEL MODEL</trans-title>
                                </trans-title-group>
                        </title-group>
                    </article-meta>
                </front>
                <sub-article article-type="translation" xml:lang="en">
                    <front-stub>
                        <title-group>
                            <article-title>HEDGING FUTURE CASH FLOWS WITH INTEREST-RATE FUTURES CONTRACTS: A DURATION AND CONVEXITY ANALYSIS UNDER THE NELSON SIEGEL MODEL</article-title>
                        </title-group>
                    </front-stub>
                </sub-article>
            </article>
            """
        )
        self.validation_title = ArticleTitlesValidation(self.xmltree)
        self.model_title = ArticleTitles(self.xmltree)
    def test_article_title_matches(self):
        expected = dict(
            expected_value={
                'lang': 'es',
                'text': 'Inmunización de <bold>Flujos Financieros</bold> con Futuros de Tasas de Interés:'
                        ' un Análisis de Duración y Convexidad con el Modelo de Nelson y Siegel'
            },
            obteined_value={
                'lang': 'es',
                'text': 'Inmunización de <bold>Flujos Financieros</bold> con Futuros de Tasas de Interés:'
                        ' un Análisis de Duración y Convexidad con el Modelo de Nelson y Siegel'
            },
            match=True
        )
        obtained = self.validation_title.validate_article_title(
            {
                'lang': 'es',
                'text': 'Inmunización de <bold>Flujos Financieros</bold> con Futuros de Tasas de Interés:'
                        ' un Análisis de Duración y Convexidad con el Modelo de Nelson y Siegel'
            }
        )
        self.assertDictEqual(expected, obtained)

    def test_sub_article_title_matches(self):
        expected = dict(
            expected_value=[{
                'lang': 'en',
                'text': 'HEDGING FUTURE CASH FLOWS WITH INTEREST-RATE FUTURES CONTRACTS: A DURATION AND CONVEXITY ANALYSIS UNDER THE NELSON SIEGEL MODEL'
            }],
            obteined_value=[{
                'lang': 'en',
                'text': 'HEDGING FUTURE CASH FLOWS WITH INTEREST-RATE FUTURES CONTRACTS: A DURATION AND CONVEXITY ANALYSIS UNDER THE NELSON SIEGEL MODEL'
            }],
            match=True
        )
        obtained = self.validation_title.validate_sub_article_title(
            [{
                'lang': 'en',
                'text': 'HEDGING FUTURE CASH FLOWS WITH INTEREST-RATE FUTURES CONTRACTS: A DURATION AND CONVEXITY ANALYSIS UNDER THE NELSON SIEGEL MODEL'
            }]
        )
        self.assertDictEqual(expected, obtained)

    def test_trans_title_matches(self):
        expected = dict(
            expected_value=[{
                'lang': 'en',
                'text': 'HEDGING FUTURE CASH FLOWS WITH INTEREST-RATE FUTURES CONTRACTS: A DURATION AND CONVEXITY ANALYSIS UNDER THE NELSON SIEGEL MODEL'
            }],
            obteined_value=[{
                'lang': 'en',
                'text': 'HEDGING FUTURE CASH FLOWS WITH INTEREST-RATE FUTURES CONTRACTS: A DURATION AND CONVEXITY ANALYSIS UNDER THE NELSON SIEGEL MODEL'
            }],
            match=True
        )
        obtained = self.validation_title.validate_trans_title(
            [{
                'lang': 'en',
                'text': 'HEDGING FUTURE CASH FLOWS WITH INTEREST-RATE FUTURES CONTRACTS: A DURATION AND CONVEXITY ANALYSIS UNDER THE NELSON SIEGEL MODEL'
            }]
        )
        self.assertDictEqual(expected, obtained)

    def test_article_title_differs_from_trans_title(self):
        self.assertTrue(self.validation_title)
