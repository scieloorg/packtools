from packtools.sps.models.article_and_subarticles import ArticleAndSubArticles
from packtools.sps.validation.exceptions import (
    ValidationArticleAndSubArticlesLanguageCodeException,
    ValidationArticleAndSubArticlesSpecificUseException,
    ValidationArticleAndSubArticlesDtdVersionException,
    ValidationArticleAndSubArticlesArticleTypeException,
    ValidationArticleAndSubArticlesSubjectsException

)
from packtools.sps.validation.similarity_utils import most_similar, similarity


class ArticleLangValidation:
    def __init__(self, xmltree, language_codes_list=None):
        self.xmltree = xmltree
        self.articles = ArticleAndSubArticles(self.xmltree)
        self.language_codes_list = language_codes_list

    def validate_language(self, language_codes_list=None):
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

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'Article element lang attribute validation',
                    'xpath': './article/@xml:lang',
                    'validation_type': 'value in list',
                    'response': 'OK',
                    'expected_value': ['pt', 'en', 'es'],
                    'got_value': 'en',
                    'message': 'Got en, to research-article whose id is main, expected one item of this list: pt | en | es',
                    'advice': 'XML research-article has en as language, to research-article whose id is main, expected one item
                    of this list: pt | en | es'
                },...
            ]
        """
        language_codes_list = language_codes_list or self.language_codes_list
        if not language_codes_list:
            raise ValidationArticleAndSubArticlesLanguageCodeException("Function requires list of language codes")
        for article in self.articles.data:
            article_lang = article.get('lang')
            article_type = article.get('article_type')
            article_id = article.get('article_id')
            validated = article_lang in language_codes_list

            if article_id == 'main':
                msg = '<article article-type={} xml:lang={}>'.format(article_type, article_lang)
            else:
                msg = '<sub-article article-type={} id={} xml:lang={}>'.format(article_type, article_id, article_lang)

            item = {
                'title': 'Article element lang attribute validation',
                'xpath': './article/@xml:lang' if article_id == 'main' else './/sub-article/@xml:lang',
                'validation_type': 'value in list',
                'response': 'OK' if validated else 'ERROR',
                'expected_value': language_codes_list,
                'got_value': article_lang,
                'message': 'Got {} expected one item of this list: {}'.format(msg, " | ".join(language_codes_list)),
                'advice': None if validated else '{} has {} as language, expected one item of this list: {}'.format(msg,
                                                                                                                    article_lang,
                                                                                                                    " | ".join(
                                                                                                                        language_codes_list))
            }
            yield item


class ArticleAttribsValidation:
    def __init__(self, xmltree, specific_use_list=None, dtd_version_list=None):
        self.xmltree = xmltree
        self.articles = ArticleAndSubArticles(self.xmltree)
        self.specific_use_list = specific_use_list
        self.dtd_version_list = dtd_version_list

    def validate_specific_use(self, specific_use_list=None):
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

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'Article element specific-use attribute validation',
                    'xpath': './article/@specific-use',
                    'validation_type': 'value in list',
                    'response': 'OK',
                    'expected_value': ['sps-1.9', 'preprint', 'special-issue'],
                    'got_value': 'sps-1.9',
                    'message': 'Got sps-1.9 expected one item of this list: sps-1.9 | preprint | special-issue',
                    'advice': 'XML research-article has None as specific-use expected one item of this list: sps-1.9 | preprint | special-issue'
                },...
            ]
        """
        specific_use_list = specific_use_list or self.specific_use_list
        if not specific_use_list:
            raise ValidationArticleAndSubArticlesSpecificUseException("Function requires list of specific uses")

        article_specific_use = self.articles.main_specific_use
        validated = article_specific_use in specific_use_list

        return {
            'title': 'Article element specific-use attribute validation',
            'xpath': './article/@specific-use',
            'validation_type': 'value in list',
            'response': 'OK' if validated else 'ERROR',
            'expected_value': specific_use_list,
            'got_value': article_specific_use,
            'message': 'Got {} expected one item of this list: {}'.format(article_specific_use, " | "
                                                                          .join(specific_use_list)),
            'advice': None if validated else 'XML {} has {} as specific-use, expected one item of this list: {}'
            .format(self.articles.main_article_type, article_specific_use, " | ".join(specific_use_list))
        }

    def validate_dtd_version(self, dtd_version_list=None):
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
                    'title': 'Article element dtd-version attribute validation',
                    'xpath': './article/@dtd-version',
                    'validation_type': 'value in list',
                    'response': 'OK',
                    'expected_value': ['1.1', '1.2', '1.3'],
                    'got_value': '1.1',
                    'message': 'Got 1.1 expected one item of this list: 1.1 | 1.2 | 1.3',
                    'advice': 'XML research-article has 1.1 as dtd-version expected one item of this list: 1.1 | 1.2 | 1.3'
                },...
            ]
        """
        dtd_version_list = dtd_version_list or self.dtd_version_list
        if not dtd_version_list:
            raise ValidationArticleAndSubArticlesDtdVersionException("Function requires list of dtd versions")

        article_dtd_version = self.articles.main_dtd_version
        validated = article_dtd_version in dtd_version_list

        return {
            'title': 'Article element dtd-version attribute validation',
            'xpath': './article/@dtd-version',
            'validation_type': 'value in list',
            'response': 'OK' if validated else 'ERROR',
            'expected_value': dtd_version_list,
            'got_value': article_dtd_version,
            'message': 'Got {} expected one item of this list: {}'.format(article_dtd_version, " | "
                                                                          .join(dtd_version_list)),
            'advice': None if validated else 'XML {} has {} as dtd-version, expected one item of this list: {}'
            .format(self.articles.main_article_type, article_dtd_version, " | ".join(dtd_version_list))
        }


class ArticleTypeValidation:
    def __init__(self, xmltree, article_type_list=None):
        self.xmltree = xmltree
        self.articles = ArticleAndSubArticles(self.xmltree)
        self.article_type_list = article_type_list

    def validate_article_type(self, article_type_list=None):
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
        article_type_list : list

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'Article type validation',
                    'xpath': './article/@article-type',
                    'validation_type': 'value in list',
                    'response': 'OK',
                    'expected_value': ['research-article', 'article-commentary', 'brief-report'],
                    'got_value': 'research-article',
                    'message': 'Got research-article expected one item of this list: research-article | article-commentary | brief-report',
                    'advice': 'XML has research-article as article-type, expected one item of this list: research-article | article-commentary | brief-report'
                },...
            ]
        """
        article_type = self.articles.main_article_type
        article_type_list = article_type_list or self.article_type_list

        if not article_type_list:
            raise ValidationArticleAndSubArticlesArticleTypeException("Function requires list of article types")

        article_type_list = [tp.lower() for tp in article_type_list]

        validated = article_type in article_type_list
        return {
            'title': 'Article type validation',
            'xpath': './article/@article-type',
            'validation_type': 'value in list',
            'response': 'OK' if validated else 'ERROR',
            'expected_value': article_type_list,
            'got_value': article_type,
            'message': 'Got {} expected one item of this list: {}'.format(article_type, " | "
                                                                          .join(article_type_list)),
            'advice': None if validated else 'XML has {} as article-type, expected one item of this list: {}'
            .format(article_type, " | ".join(article_type_list))
        }


class ArticleSubjectsValidation:
    def __init__(self, xmltree, subjects_list=None):
        self.xmltree = xmltree
        self.articles = ArticleAndSubArticles(self.xmltree)
        self.subjects_list = subjects_list

    def validate_without_subjects(self):
        """
        Check whether an article that shouldn't have a subject actually doesn't.

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

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'Article type vs subjects validation',
                    'xpath': './article/@article-type .//subject',
                    'validation_type': 'value in list',
                    'response': 'ERROR',
                    'expected_value': None,
                    'got_value': ['scientific article', 'artigo científico', 'artículo científico'],
                    'message': 'Got scientific article, artigo científico, artículo científico expected no subject',
                    'advice': 'XML has scientific article, artigo científico, artículo científico as subjects expected no subjects'
                },...
            ]
        """
        declared_subjects = [subject['subject'].lower() for subject in self.articles.data if subject['subject']]

        validated = len(declared_subjects) == 0
        got_value = None if validated else ", ".join(declared_subjects)
        return {
            'title': 'Article type vs subjects validation',
            'xpath': './article/@article-type .//subject',
            'validation_type': 'value in list',
            'response': 'OK' if validated else 'ERROR',
            'expected_value': None,
            'got_value': None if validated else declared_subjects,
            'message': 'Got {} expected no subject'.format(got_value),
            'advice': 'XML has {} as subjects, expected no subjects'.format(got_value)
        }

    def validate_article_type_vs_subject_similarity(self, subjects_list=None, expected_similarity=0):
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
        subjects_list : list of dict, such as:
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

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'Article type vs subjects validation',
                    'xpath': './article/@article-type .//subject',
                    'validation_type': 'similarity',
                    'response': 'ERROR',
                    'expected_value': 0.7,
                    'got_value': 0.6818181818181818,
                    'message': 'The article id: main must match the Original Article (en) with a rate greater than or equal to 0.7',
                    'advice': 'The subject Scientific Article (en) does not match the items provided in the list: '
                              'Original Article (en) | Artigo Original (pt) | Artículo Original (es)'
                },...
            ]
        """

        subjects_list = subjects_list or self.subjects_list

        if not subjects_list:
            raise ValidationArticleAndSubArticlesSubjectsException("Function requires list of subjects")

        subjects_list = [f"{item['subject']} ({item['lang']})" for item in subjects_list]
        result = []

        for article in self.articles.data:
            article_subject = f"{article['subject']} ({article['lang']})"
            article_id = article['article_id']
            calculated_similarity, subject = most_similar(similarity(subjects_list, article_subject))
            validated = calculated_similarity >= expected_similarity
            result.append(
                {
                    'title': 'Article type vs subjects validation',
                    'xpath': './article/@article-type .//subject',
                    'validation_type': 'similarity',
                    'response': "OK" if validated else "ERROR",
                    'expected_value': expected_similarity,
                    'got_value': calculated_similarity,
                    'message': f'The article id: {article_id} must match the {subject[0]} with a rate greater than or equal to {expected_similarity}',
                    'advice': None if validated else 'The subject {} does not match the items provided in the list: {}'
                    .format(article_subject, " | ".join(subjects_list))
                }
            )

        return result

    def validate(self, data):
        """
        Função que executa as validações da classe ArticleValidation.

        Returns:
            dict: Um dicionário contendo os resultados das validações realizadas.

        """
        return {
            'article_lang_validation': self.validate_language(data['language_codes_list']),
            'article_specific_use_validation': self.validate_specific_use(data['specific_use_list'])
        }



