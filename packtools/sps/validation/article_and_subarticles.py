from lxml import etree

from packtools.sps.models.article_and_subarticles import ArticleAndSubArticles
from packtools.sps.models.v2.article_toc_sections import ArticleTocSections
from packtools.sps.models.article_ids import ArticleIds
from packtools.sps.validation.exceptions import (
    ValidationArticleAndSubArticlesLanguageCodeException,
    ValidationArticleAndSubArticlesSpecificUseException,
    ValidationArticleAndSubArticlesDtdVersionException,
    ValidationArticleAndSubArticlesArticleTypeException,
    ValidationArticleAndSubArticlesSubjectsException,
)
from packtools.sps.validation.similarity_utils import most_similar, similarity
from packtools.sps.validation.utils import build_response, format_response


class ArticleLangValidation:
    def __init__(self, xmltree, params):
        self.xmltree = xmltree
        self.articles = ArticleAndSubArticles(self.xmltree)
        self.params = self._get_default_params()
        self.params.update(params or {})

    def _get_default_params(self):
        return {
            "language_codes_list": ["pt", "en", "es"],  # Common languages in scientific publications
            "language_error_level": "CRITICAL"
        }

    def validate_language(self):
        """
        Check whether the article language matches the options provided in a standard list.

        XML input
        ---------
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v3">zTn4sYXBrfSTMNVPF5Dm7jr</article-id>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0103-50532014001202258</article-id>
                    <article-id pub-id-type="doi">10.5935/0103-5053.20140192</article-id>
                </article-meta>
            </front>
        </article>

        Params
        ------
        language_codes_list : list
            A list of language codes to validate against.

        error_level : str, optional
            The level of error to report if the validation fails. Default is "CRITICAL".

        Returns
        -------
        generator of dict
            A generator that yields dictionaries with validation results, such as:
            [
                {
                    'title': 'Article element lang attribute validation',
                    'parent': 'article',
                    'parent_id': None,
                    'parent_article_type': 'research-article',
                    'parent_lang': 'en',
                    'item': 'article',
                    'sub_item': '@xml:lang',
                    'validation_type': 'value in list',
                    'response': 'CRITICAL',
                    'expected_value': ['pt', 'en', 'es'],
                    'got_value': 'en',
                    'message': 'Got en, expected one item of this list: pt | en | es',
                    'advice': 'XML article has en as language, expected one item of this list: pt | en | es',
                    'data': {
                        'specific_use': 'sps-1.9',
                        'dtd_version': '1.1'
                    },
                },...
            ]
        """
        try:
            language_codes_list = self.params["language_codes_list"] or []
        except KeyError:
            raise ValidationArticleAndSubArticlesLanguageCodeException(
                "Function requires list of language codes"
            )

        for article in self.articles.data:
            article_lang = article.get("lang")
            article_type = article.get("article_type")
            article_id = article.get("article_id")
            parent = article.get("parent_name")

            valid = article_lang in language_codes_list

            name = article_id or parent
            parent_id = f' id="{article_id}"' if article_id else ''
            if article_lang:
                xml = f'<{parent}{parent_id} xml:lang="{article_lang}">'
                advice = f'Replace {article_lang} in {xml} with one of {language_codes_list}'
            else:
                xml = f'<{parent}{parent_id}>'
                xml2 = f'<{parent}{parent_id} xml:lang="VALUE">'

                advice = f'Add xml:lang="VALUE" in {xml}: {xml2} and replace VALUE with one of {language_codes_list}'
            yield format_response(
                    title=f"{name} language",
                    parent=parent,
                    parent_id=article_id,
                    parent_article_type=article_type,
                    parent_lang=article_lang,
                    item=parent,
                    sub_item="@xml:lang",
                    validation_type="value in list",
                    is_valid=valid,
                    expected=language_codes_list,
                    obtained=article_lang,
                    advice=advice,
                    data=article,
                    error_level=self.params["language_error_level"],
            )


class ArticleTypeValidation:
    def __init__(self, xmltree, params):
        self.xmltree = xmltree
        self.articles = ArticleAndSubArticles(self.xmltree)
        self.subject_english_version = ArticleTocSections(self.xmltree).sections_dict.get("en")

        self.params = self._get_default_params()
        self.params.update(params or {})

    def _get_default_params(self):
        return {
            "article_type_list": [
                "research-article",
                "review-article",
                "editorial",
                "letter",
                "case-report",
                "brief-report",
                "rapid-communication"
            ],
            "article_type_error_level": "CRITICAL",
            "article_type_and_subject_expected_similarity": 0.6,
            "article_type_and_subject_expected_similarity_error_level": "ERROR"
        }

    def validate_article_type(self):
        article_type = self.articles.main_article_type
        try:
            article_type_list = self.params["article_type_list"] or []
        except KeyError:
            raise ValidationArticleAndSubArticlesArticleTypeException(
                "ArticleTypeValidation.validate_article_type requires article_type_list"
            )

        validated = article_type in article_type_list

        for article in self.articles.data:
            article_lang = article.get("lang")
            article_type = article.get("article_type")
            article_id = article.get("article_id")
            parent = article.get("parent_name")

            valid = article_type in article_type_list

            name = article_id or parent
            xml = f'<{parent} article-type=""/>'
            advice = None if valid else f'Complete {name} article-type {xml} with valid value {article_type_list}'
            yield format_response(
                    title=f"{name} article-type",
                    parent=parent,
                    parent_id=article_id,
                    parent_article_type=article_type,
                    parent_lang=article_type,
                    item=parent,
                    sub_item="article-type",
                    validation_type="value in list",
                    is_valid=valid,
                    expected=article_type_list,
                    obtained=article_type,
                    advice=advice,
                    data=article,
                    error_level=self.params["article_type_error_level"],
            )

    def validate_article_type_vs_subject_similarity(self):
        if not self.subject_english_version:
            # nao ha section em ingles
            return
        try:
            article_type_list = self.params["article_type_list"]
        except KeyError:
            raise ValidationArticleAndSubArticlesSubjectsException(
                "Function requires list of article types to check the similarity with subjects"
            )

        subject = self.subject_english_version and self.subject_english_version[0]
        article_type = self.articles.main_article_type
        
        article_subject = subject["section"]

        # compara subject com todos os valores possíveis de article_type
        similarity_by_rate = similarity(article_type_list, article_subject)

        expected_similarity = float(self.params.get("article_type_and_subject_expected_similarity")) or 0.6
        most_similar_article_type = []
        for k, items in similarity_by_rate.items():
            if k > expected_similarity:
                most_similar_article_type.extend(items)

        # a similaridade pode ser baixa mas o tipo pode estar correto
        if most_similar_article_type:
            # continua a verificar a validade
            # article-type deve ser similar ao título da seção do sumário (inglês)
            valid = article_type in most_similar_article_type
        
            xml_article_type = f'<article article-type="{article_type}"/>'
            xml_subject = f'<subject-group subj-group-type="heading"><subject>{article_subject}</subject></subject-group>'
            
            data = {
                "subject": article_subject,
                "article_type": article_type,
                "article_type_list": article_type_list,
                "most_similar_article_type": most_similar_article_type,
                "similarity_by_rate": similarity_by_rate,
                "expected similarity": expected_similarity
            }
            data.update({
                "specific_use": self.articles.specific_use,
                "dtd_version": self.articles.dtd_version
            })

            title = f"article type and table of contents section"
            choices = " | ".join(most_similar_article_type)
            advice = None
            if not valid:
                advice = (
                    f"Check {xml_article_type} and {xml_subject}. Other values for article-type seems to be more suitable: {choices}. "
                )
            yield format_response(
                title=title,
                parent="article",
                parent_article_type=self.articles.main_article_type,
                parent_lang=self.articles.main_lang,
                parent_id=None,
                item="article",
                sub_item="@article-type",
                validation_type="similarity",
                is_valid=valid,
                expected=article_type_list,
                obtained=article_type,
                advice=advice,
                data=data,
                error_level=self.params["article_type_and_subject_expected_similarity_error_level"],
            )


class ArticleIdValidation:
    def __init__(self, xmltree, params):
        self.xmltree = xmltree
        self.articles = ArticleAndSubArticles(self.xmltree)
        self.article_ids = ArticleIds(self.xmltree)
        self.params = self._get_default_params()
        self.params.update(params or {})

    def _get_default_params(self):
        return {
            "id_other_error_level": "ERROR"
        }

    def validate_article_id_other(self):
        order = self.article_ids.other
        if not order:
            return

        expected = []
        valid = False
        try:
            valid = 0 < int(order) <= 99999
            if not valid:
                expected.append("a numerical value from 1 to 99999")
        except (TypeError, ValueError):
            expected.append("a numerical value from 1 to 99999")

        try:
            n = len(order)
            valid = 0 < n <= 5
            if not valid:
                expected.append(f"must have maximum 5 characters. Found {n}")
        except (TypeError, ValueError):
            expected.append(f"must have maximum 5 characters. Found {n}")

        expected_value = " and ".join(expected)
        yield build_response(
            title='table of contents article order',
            parent=self.article_ids.data,
            item="article-id",
            sub_item='@pub-id-type="other"',
            validation_type="format",
            is_valid=not expected,
            expected=expected_value,
            obtained=order,
            advice=f'Fix the table of contents article order {order} in <article-id pub-id-type="other">{order}</article-id>. It must be {expected_value}',
            data=self.article_ids.data,
            error_level=self.params["id_other_error_level"],
        )


class JATSAndDTDVersionValidation:

    def __init__(self, xml_tree, params):
        self.xml_tree = xml_tree
        self.article_and_sub_articles = ArticleAndSubArticles(self.xml_tree)
        self.dtd_version = self.article_and_sub_articles.dtd_version
        self.specific_use = self.article_and_sub_articles.specific_use
        self.params = self._get_default_params()
        self.params.update(params or {})

    def _get_default_params(self):
        return {
            "specific_use_list": {
                "sps-1.1": ["1.0"],
                "sps-1.2": ["1.0"],
                "sps-1.3": ["1.0"],
                "sps-1.4": ["1.0"],
                "sps-1.5": ["1.0"],
                "sps-1.6": ["1.0"],
                "sps-1.7": ["1.0", "1.1"],
                "sps-1.8": ["1.0", "1.1"],
                "sps-1.9": ["1.1"],
                "sps-1.10": ["1.1", "1.2", "1.3"]
            },
            "jats_and_dtd_version_error_level": "CRITICAL"
        }

    def validate(self):
        sps_version = self.specific_use
        jats_version = self.dtd_version

        versions = self.params["specific_use_list"]

        expected_jats_versions = versions.get(sps_version) or []

        advice = None
        if not versions:
            advice = f'Complete SPS version <article specific-use=""/> with valid value: {list(versions.keys())}',

        elif jats_version not in expected_jats_versions:
            xml = f'<article specific-use="" dtd-version=""/>'
            advice = f'Complete SPS (specific-use="") and JATS (dtd-version="") versions in {xml} with compatible values: {versions}'

        expected = expected_jats_versions or versions
        got = {
            "specific-use": sps_version,
            "dtd-version": jats_version,
        }
        data = {
            "specific-use": sps_version,
            "dtd-version": jats_version,
            "expected values": expected,
        }
        yield format_response(
            title='SPS and JATS versions',
            parent="article",
            parent_id=None,
            parent_article_type=self.article_and_sub_articles.main_article_type,
            parent_lang=self.article_and_sub_articles.main_lang,
            item="specific-use and dtd-version",
            sub_item=None,
            validation_type="match",
            is_valid=not advice,
            expected=expected,
            obtained=got,
            advice=advice,
            data=data,
            error_level=self.params["jats_and_dtd_version_error_level"],
        )
