from packtools.sps.models import (
    article_titles,
    article_abstract,
    kwd_group
)


def _elements_exist(article_type, title_lang, title, abstract, keyword):
    # verifica se existe título no XML
    if not title.article_title_dict.get(title_lang):
        return False, True, 'title', './/article-title/@xml:lang', f'title for the {article_type}'
    # verifica se existe palavras-chave sem resumo
    if abstract == [] and keyword != []:
        return False, True, 'abstract', './/abstract/@xml:lang', f'abstract for the {article_type}'
    # verifica se existe resumo sem palavras-chave
    if abstract != [] and keyword == []:
        return False, True, 'kwd-group', './/kwd-group/@xml:lang', f'keywords for the {article_type}'
    # verifica se o teste é necessário
    if abstract == [] and keyword == []:
        return True, False, None, None, None
    return True, True, None, None, None


def get_title_langs(titles):
    article_langs = (
        ([titles.article_title.get('lang')] if titles.article_title.get('text') else []) +
        [item.get('lang') for item in titles.trans_titles if item.get('text')]
    )

    sub_article_langs = [item.get('lang') for item in titles.sub_article_titles if item.get('text')]

    resp = {'article': article_langs}

    if sub_article_langs:
        resp['sub-article'] = sub_article_langs

    return resp




class ArticleLangValidation:
    def __init__(self, xml_tree):
        self.article_title = article_titles.ArticleTitles(xml_tree)
        self.article_abstract = article_abstract.Abstract(xml_tree)
        self.article_kwd = kwd_group.KwdGroup(xml_tree).extract_kwd_extract_data_by_lang(None)

    def validate_article_lang(self):
        """
        Checks whether the title, abstract and keyword elements are present in the XML and whether the respective languages match.

        XML input
        ---------
        <article  xml:lang="pt">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título em português</article-title>
                        <trans-title-group xml:lang="en">
                            <trans-title>Title in english</trans-title>
                        </trans-title-group>
                    </title-group>
                    <abstract><p>Resumo em português</p></abstract>
                    <trans-abstract xml:lang="en">Abstract in english</trans-abstract>
                    <kwd-group xml:lang="pt">
                        <kwd>Palavra chave 1</kwd>
                        <kwd>Palavra chave 2</kwd>
                    </kwd-group>
                    <kwd-group xml:lang="en">
                        <kwd>Keyword 1</kwd>
                        <kwd>Keyword 2</kwd>
                    </kwd-group>
                </article-meta>
            </front>
        </article>

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'abstract element lang attribute validation',
                    'xpath': './/article-title/@xml:lang .//abstract/@xml:lang',
                    'validation_type': 'match',
                    'response': 'OK',
                    'expected_value': 'pt',
                    'got_value': 'pt',
                    'message': 'Got pt expected pt',
                    'advice': None
                },...
            ]
        """
        # obtem uma lista com códigos de idiomas para títulos: ['pt', 'en', 'es']
        title_lang_list = [self.article_title.article_title.get('lang')] + \
                          [item.get('lang') for item in self.article_title.trans_titles]

        # obtem uma lista com códigos de idiomas para resumos: ['pt', 'en', 'es']
        try:
            abstract_lang_list = [self.article_abstract.get_main_abstract().get('lang')] + \
                                 [item.get('lang') for item in self.article_abstract._get_trans_abstracts()]
        except AttributeError:
            abstract_lang_list = []

        # obtem uma lista com códigos de idiomas para palavras-chave: ['pt', 'en', 'es']
        keyword_lang_list = list(self.article_kwd.keys())

        # verifica a exsitência dos elementos no XML
        exist, element, xpath, expected, lang = _elements_exist(self.article_title, abstract_lang_list,
                                                                keyword_lang_list)

        if exist:
            # validação de correspondência entre os idiomas, usando como base o título
            for element, langs in zip(['abstract', 'kwd-group'], [abstract_lang_list, keyword_lang_list]):
                for title_lang, element_lang in zip(title_lang_list, langs):
                    is_valid = title_lang == element_lang
                    expected = title_lang
                    obtained = element_lang
                    advice = None if is_valid else f'Provide {element} in the language \'{title_lang}\''
                    yield {
                        'title': f'{element} element lang attribute validation',
                        'xpath': f'.//article-title/@xml:lang .//{element}/@xml:lang',
                        'validation_type': 'match',
                        'response': 'OK' if is_valid else 'ERROR',
                        'expected_value': expected,
                        'got_value': obtained,
                        'message': f'Got {obtained} expected {expected}',
                        'advice': advice
                    }
        else:
            # resposta para a verificação de ausência de elementos
            yield {
                'title': f'{element} element lang attribute validation',
                'xpath': xpath,
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': expected,
                'got_value': None,
                'message': f'Got None expected {expected}',
                'advice': f'Provide a {element} in the language \'{lang}\''
            }
