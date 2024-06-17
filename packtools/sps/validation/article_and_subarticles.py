from packtools.sps.models.article_and_subarticles import ArticleAndSubArticles
from packtools.sps.models.article_ids import ArticleIds
from packtools.sps.validation.exceptions import (
    ValidationArticleAndSubArticlesLanguageCodeException,
    ValidationArticleAndSubArticlesSpecificUseException,
    ValidationArticleAndSubArticlesDtdVersionException,
    ValidationArticleAndSubArticlesArticleTypeException,
    ValidationArticleAndSubArticlesSubjectsException,
)
from packtools.sps.validation.similarity_utils import most_similar, similarity
from packtools.sps.validation.utils import format_response


class ArticleLangValidation:
    def __init__(self, xmltree, language_codes_list=None):
        self.xmltree = xmltree
        self.articles = ArticleAndSubArticles(self.xmltree)
        self.language_codes_list = language_codes_list

    def validate_language(self, language_codes_list=None, error_level=None):
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
        language_codes_list = language_codes_list or self.language_codes_list
        if not language_codes_list:
            raise ValidationArticleAndSubArticlesLanguageCodeException(
                "Function requires list of language codes"
            )
        error_level = error_level or 'CRITICAL'
        for article in self.articles.data:
            article_lang = article.get("lang")
            article_type = article.get("article_type")
            article_id = article.get("article_id")
            validated = article_lang in language_codes_list

            if article_id is None:
                parent = "article"
                msg = "<article article-type={} xml:lang={}>".format(
                    article_type, article_lang
                )
            else:
                parent = "sub-article"
                msg = "<sub-article article-type={} id={} xml:lang={}>".format(
                    article_type, article_id, article_lang
                )

            yield format_response(
                    title="Article element lang attribute validation",
                    parent=parent,
                    parent_id=article_id,
                    parent_article_type=article_type,
                    parent_lang=article_lang,
                    item=parent,
                    sub_item="@xml:lang",
                    validation_type="value in list",
                    is_valid=validated,
                    expected=language_codes_list,
                    obtained=article_lang,
                    advice="{} has {} as language, expected one item of this list: {}".format(
                        msg, article_lang, " | ".join(language_codes_list)
                    ),
                    data=article,
                    error_level=error_level
            )


class ArticleAttribsValidation:
    def __init__(self, xmltree, specific_use_list=None, dtd_version_list=None):
        self.xmltree = xmltree
        self.articles = ArticleAndSubArticles(self.xmltree)
        self.specific_use_list = specific_use_list
        self.dtd_version_list = dtd_version_list

    def validate_specific_use(self, specific_use_list=None, error_level=None):
        """
        Check whether the specific use attribute of the article matches the options provided in a standard list.

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
        specific_use_list : list
            A list of specific uses to validate against.

        error_level : str, optional
            The level of error to report if the validation fails. Default is "CRITICAL".

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'Article element specific-use attribute validation',
                    'parent': 'article',
                    'parent_id': None,
                    'parent_article_type': 'research-article',
                    'parent_lang': 'portugol',
                    'item': 'article',
                    'sub_item': '@specific-use',
                    'validation_type': 'value in list',
                    'response': 'OK',
                    'expected_value': ['sps-1.9', 'preprint', 'special-issue'],
                    'got_value': 'sps-1.9',
                    'message': 'Got sps-1.9, expected one item of this list: sps-1.9 | preprint | special-issue',
                    'advice': None,
                    'data': {
                        'specific_use': 'sps-1.9',
                        'dtd_version': '1.1'
                    }
                },...
            ]
        """
        error_level = error_level or "CRITICAL"
        specific_use_list = specific_use_list or self.specific_use_list
        if not specific_use_list:
            raise ValidationArticleAndSubArticlesSpecificUseException(
                "Function requires list of specific uses"
            )

        validated = self.articles.main_specific_use in specific_use_list

        data = self.articles.data[0]
        data.update({
            "specific_use": self.articles.main_specific_use,
            "dtd_version": self.articles.main_dtd_version
        })

        yield format_response(
            title="Article element specific-use attribute validation",
            parent="article",
            parent_id=None,
            parent_article_type=self.articles.main_article_type,
            parent_lang=self.articles.main_lang,
            item="article",
            sub_item="@specific-use",
            validation_type="value in list",
            is_valid=validated,
            expected=specific_use_list,
            obtained=self.articles.main_specific_use,
            advice="XML {} has {} as specific-use, expected one item of this list: {}".format(
                    self.articles.main_article_type,
                    self.articles.main_specific_use,
                    " | ".join(specific_use_list),
                ),
            data=data,
            error_level=error_level,
        )

    def validate_dtd_version(self, dtd_version_list=None, error_level=None):
        """
        Check whether the dtd version attribute of the article matches the options provided in a standard list.

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
        dtd_version_list : list

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    "title": "Article element dtd-version attribute validation",
                    'parent': 'article',
                    'parent_id': None,
                    'parent_article_type': 'research-article',
                    'parent_lang': 'portugol',
                    'item': 'article',
                    'sub_item': '@dtd-version',
                    "validation_type": "value in list",
                    "response": "CRITICAL",
                    "expected_value": ["1.1", "1.2", "1.3"],
                    "got_value": None,
                    'message': "Got None, expected ['1.1', '1.2', '1.3']",
                    'advice': 'XML research-article has None as dtd-version, expected one item of this list: 1.1 | 1.2 | 1.3',
                    'data': {
                        'article_id': None,
                        'article_type': 'research-article',
                        'dtd_version': None,
                        'lang': 'portugol',
                        'line_number': 2,
                        'specific_use': 'sps-1.9',
                        'subject': None
                    },
                }
            ]
        """
        error_level = error_level or "CRITICAL"
        dtd_version_list = dtd_version_list or self.dtd_version_list
        if not dtd_version_list:
            raise ValidationArticleAndSubArticlesDtdVersionException(
                "Function requires list of dtd versions"
            )

        validated = self.articles.main_dtd_version in dtd_version_list

        data = self.articles.data[0]
        data.update({
            "specific_use": self.articles.main_specific_use,
            "dtd_version": self.articles.main_dtd_version
        })

        yield format_response(
            title="Article element dtd-version attribute validation",
            parent="article",
            parent_id=None,
            parent_article_type=self.articles.main_article_type,
            parent_lang=self.articles.main_lang,
            item="article",
            sub_item="@dtd-version",
            validation_type="value in list",
            is_valid=validated,
            expected=dtd_version_list,
            obtained=self.articles.main_dtd_version,
            advice="XML {} has {} as dtd-version, expected one item of this list: {}".format(
                    self.articles.main_article_type,
                    self.articles.main_dtd_version,
                    " | ".join(dtd_version_list),
            ),
            data=data,
            error_level=error_level
        )


class ArticleTypeValidation:
    def __init__(self, xmltree, article_type_list=None, subjects_list=None, apply_to_article_types=None):
        self.xmltree = xmltree
        self.articles = ArticleAndSubArticles(self.xmltree)
        self.article_type_list = article_type_list
        self.subjects_list = subjects_list
        self.apply_to_article_types = apply_to_article_types

    def validate_article_type(self, article_type_list=None, error_level=None):
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
        article_type_list = article_type_list or self.article_type_list
        error_level = error_level or "CRITICAL"

        if not article_type_list:
            raise ValidationArticleAndSubArticlesArticleTypeException(
                "Function requires list of article types"
            )

        validated = article_type in article_type_list

        data = self.articles.data[0]
        data.update({
            "specific_use": self.articles.main_specific_use,
            "dtd_version": self.articles.main_dtd_version
        })

        yield format_response(
            title="Article type validation",
            parent="article",
            parent_id=None,
            parent_article_type=self.articles.main_article_type,
            parent_lang=self.articles.main_lang,
            item="article",
            sub_item="@article-type",
            validation_type="value in list",
            is_valid=validated,
            expected=article_type_list,
            obtained=article_type,
            advice="XML has {} as article-type, expected one item of this list: {}".format(
                    article_type, " | ".join(article_type_list)
            ),
            data=data,
            error_level=error_level,
        )

    def validate_article_type_vs_subject_similarity(
        self, subjects_list=None, expected_similarity=1, error_level=None, target_article_types=None
    ):
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

        target_article_types : list of str, optional
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

        subjects_list = subjects_list or self.subjects_list

        if not subjects_list:
            raise ValidationArticleAndSubArticlesSubjectsException(
                "Function requires list of subjects"
            )

        subjects_list = [
            f"{item['subject']} ({item['lang']})" for item in subjects_list
        ]

        target_article_types = target_article_types or self.apply_to_article_types

        if not target_article_types:
            raise ValidationArticleAndSubArticlesSubjectsException(
                "Function requires list of article types to check the similarity with subjects"
            )

        error_level = error_level or "ERROR"

        articles = [article for article in self.articles.data if article.get("article_type") in target_article_types]

        for article in articles:
            article_subject = f"{article['subject']} ({article['lang']})"

            calculated_similarity, subject = most_similar(
                similarity(subjects_list, article_subject)
            )
            validated = calculated_similarity >= expected_similarity

            data = self.articles.data[0]
            data.update({
                "specific_use": self.articles.main_specific_use,
                "dtd_version": self.articles.main_dtd_version
            })

            yield format_response(
                title="Article type vs subjects validation",
                parent="article",
                parent_id=None,
                parent_article_type=article.get("article_type"),
                parent_lang=article.get("lang"),
                item="article",
                sub_item="@article-type",
                validation_type="similarity",
                is_valid=validated,
                expected=expected_similarity,
                obtained=calculated_similarity,
                advice="The subject {} does not match the items provided in the list: {}".format(
                        article_subject, " | ".join(subjects_list)
                    ),
                data=data,
                error_level=error_level
            )

    # def validate(self, data):
    #     """
    #     Função que executa as validações da classe ArticleValidation.
    #
    #     Returns:
    #         dict: Um dicionário contendo os resultados das validações realizadas.
    #
    #     """
    #     yield {
    #         "article_lang_validation": self.validate_language(
    #             data["language_codes_list"]
    #         ),
    #         "article_specific_use_validation": self.validate_specific_use(
    #             data["specific_use_list"]
    #         ),
    #     }


class ArticleIdValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.articles = ArticleAndSubArticles(self.xmltree)
        self.article_ids = ArticleIds(self.xmltree)

    def validate_article_id_other(self, error_level=None):
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
        is_valid = self.article_ids.other.isnumeric() and len(self.article_ids.other) <= 5
        error_level = error_level or "ERROR"
        expected_value = (
            self.article_ids.other if is_valid else "a numeric value with up to five digits"
        )
        yield format_response(
            title="Article id other validation",
            parent="article",
            parent_id=None,
            parent_article_type=self.articles.main_article_type,
            parent_lang=self.articles.main_lang,
            item="article-id",
            sub_item='@pub-id-type="other"',
            validation_type="format",
            is_valid=is_valid,
            expected=expected_value,
            obtained=self.article_ids.other,
            advice='Provide a numeric value for <article-id pub-id-type="other"> with up to five digits',
            data=self.article_ids.data,
            error_level=error_level,
        )
