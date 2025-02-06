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
from packtools.sps.validation.utils import format_response, build_response


class ArticleLangValidation:
    def __init__(self, xmltree, params):
        self.xmltree = xmltree
        self.articles = ArticleAndSubArticles(self.xmltree)
        self.params = params

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
            language_codes_list = self.params["language_codes_list"]
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
            xml = f'<{parent} xml:lang=""/>'
            advice = None if valid else f'Complete {name} xml:lang {xml} with valid value {language_codes_list}'
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
        self.params = params
        self.xmltree = xmltree
        self.articles = ArticleAndSubArticles(self.xmltree)
        self.subject_english_version = ArticleTocSections(self.xmltree).sections_dict.get("en")

    def validate_article_type(self):
        """
        Check whether the article type attribute of the article matches the options provided in a standard list.

        XML input
        ---------
        <article article-type="research-article" dtd-version="1.1"
        specific-use="sps-1.9" xml:lang="portugol" xmlns:mml="http://www.w3.org/1998/Math/MathML"
        xmlns:xlink="http://www.w3.org/1999/xlink">
            <sub-article article-type="translation" id="s1" xml:lang="en">
            </sub-article>
        </article>

        Params
        ------
        article_type_list : list, optional
            A list of valid article types that the article's type should match. If not provided, defaults to `self.article_type_list`.

        error_level : str, optional
            The level of error to report if the validation fails. Default is "CRITICAL".

        Returns
        -------
        generator of dict
            A generator that yields dictionaries with validation results, such as:
            [
                {
                    "title": "Article type validation",
                    'parent': 'article',
                    'parent_id': None,
                    'parent_article_type': 'research-article',
                    'parent_lang': 'portugol',
                    'item': 'article',
                    'sub_item': '@article-type',
                    "validation_type": "value in list",
                    "response": "OK",
                    "expected_value": ["research-article"],
                    "got_value": "research-article",
                    'message': "Got research-article, expected ['research-article']",
                    "advice": None,
                    'data': {
                        'article_id': None,
                        'article_type': 'research-article',
                        'dtd_version': None,
                        'lang': 'portugol',
                        'line_number': 2,
                        'specific_use': 'sps-1.9',
                        'subject': None
                    }
                },...
            ]
        """
        article_type = self.articles.main_article_type
        try:
            article_type_list = self.params["article_type_list"]
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
        """
        Check how similar the type of article and its respective subjects are.

        XML input
        ---------
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
        article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <article-id pub-id-type="publisher-id" specific-use="scielo-v3">TPg77CCrGj4wcbLCh9vG8bS</article-id>
            <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0104-11692020000100303</article-id>
            <article-categories>
                <subj-group subj-group-type="heading">
                    <subject>Scientific Article</subject>
                </subj-group>
            </article-categories>
            <sub-article article-type="translation" id="s1" xml:lang="pt">
                <article-categories>
                    <subj-group subj-group-type="heading">
                        <subject>Artigo Científico</subject>
                    </subj-group>
                </article-categories>
            </sub-article>
            <sub-article article-type="translation" id="s2" xml:lang="es">
                <article-categories>
                    <subj-group subj-group-type="heading">
                        <subject>Artículo Científico</subject>
                    </subj-group>
                </article-categories>
            </sub-article>
        </article>

        Params
        ------
        expected_similarity : float
            The minimum similarity score required for the validation to pass.

        subjects_list : list of dict, optional
            A list of dictionaries where each dictionary contains a subject and its language, such as:
            [
                {
                    'subject': 'original article',
                    'lang': 'en'
                },
                {
                    'subject': 'artigo original',
                    'lang': 'pt'
                },
                {
                    'subject': 'artículo original',
                    'lang': 'es'
                }
            ]
            If not provided, defaults to `self.subjects_list`.

        error_level : str, optional
            The level of error to report if the validation fails. Default is "ERROR".

        article_type_list : list of str, optional
            A list of article types that should be checked for similarity against the subjects.
            Only articles of these types will be validated. For example: ['research-article', 'review-article'].
            If not provided, defaults to `self.apply_to_article_types`.

        Returns
        -------
        generator of dict
            A generator that yields dictionaries with validation results, such as:
            [
                {
                    "title": "Article type vs subjects validation",
                    'parent': 'article',
                    'parent_id': None,
                    'parent_article_type': 'research-article',
                    'parent_lang': 'en',
                    'item': 'article',
                    'sub_item': '@article-type',
                    "validation_type": "similarity",
                    "response": "ERROR",
                    "expected_value": 0.7,
                    "got_value": 0.6818181818181818,
                    'message': 'Got 0.6818181818181818, expected 0.7',
                    "advice": "The subject Scientific Article (en) does not match the items provided in the list: "
                    "Original Article (en) | Artigo Original (pt) | Artículo Original (es)",
                    'data': {
                        'article_id': None,
                        'article_type': 'research-article',
                        'dtd_version': '1.1',
                        'lang': 'en',
                        'line_number': 3,
                        'specific_use': 'sps-1.9',
                        'subject': 'Scientific Article'
                    },
                },...
            ]
        """

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
        calculated_similarity, most_similar_article_type = most_similar(
            similarity(article_type_list, article_subject)
        )

        expected_similarity = float(self.params.get("article_type_and_subject_expected_similarity")) or 0.6

        # a similaridade pode ser baixa mas o tipo pode estar correto
        if calculated_similarity >= expected_similarity:
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
                "similarity": calculated_similarity,
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
        self.params = params

    def validate_article_id_other(self):
        """
        Check whether an article that shouldn't have a subject actually doesn't.

        XML input
        ---------
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
        article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v3">TPg77CCrGj4wcbLCh9vG8bS</article-id>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0104-11692020000100303</article-id>
                    <article-id pub-id-type="other">123</article-id>
                </article-meta>
            </front>
        </article>

        Returns
        -------
        dict, such as:
            {
                "title": "Article id other validation",
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'en',
                'item': 'article-id',
                'sub_item': '@pub-id-type="other"',
                "validation_type": "format",
                "response": "OK",
                "expected_value": "123",
                "got_value": "123",
                'message': 'Got 123, expected 123',
                "advice": None,
                'data': {
                    'other': '123',
                    'v2': 'S0104-11692020000100303',
                    'v3': 'TPg77CCrGj4wcbLCh9vG8bS'
                },
            }
        """
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
            is_valid=valid,
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
        self.params = params

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
            advice = f"Complete respectively SPS and JATS versions {xml} with compatible values: {versions}"

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
