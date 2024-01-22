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


def get_abstract_langs(abstracts):
    main_abstract = abstracts.get_main_abstract(style='inline')
    if main_abstract:
        main_abstract_lang = [main_abstract.get('lang')] if main_abstract.get('abstract') else []
    else:
        main_abstract_lang = []

    trans_abstract_langs = [item.get('lang') for item in abstracts._get_trans_abstracts(style='inline') if item.get('abstract')]

    sub_article_abstract_langs = [item.get('lang') for item in abstracts._get_sub_article_abstracts(style='inline') if item.get('abstract')]

    return {
        'article': main_abstract_lang + trans_abstract_langs,
        'sub-article': sub_article_abstract_langs
    }


def get_keyword_langs(kwd):
    resp = {
        'article': [],
        'sub-article': []
    }
    for item in kwd:
        resp[item['type']].append(item.get('lang'))

    return resp


class ArticleLangValidation:
    def __init__(self, xml_tree):
        self.article_title = article_titles.ArticleTitles(xml_tree)
        self.article_abstract = article_abstract.Abstract(xml_tree)
        self.article_kwd = kwd_group.KwdGroup(xml_tree).extract_kwd_data_with_lang_text_by_article_type(None)

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
        # obtem um dicionário com códigos de idiomas para títulos: {'article': ['pt', 'en'], 'sub-article': ['es']}
        title_langs_dict = get_title_langs(self.article_title)

        # obtem um dicionário com códigos de idiomas para resumos: {'article': ['pt', 'en'], 'sub-article': ['es']}
        abstract_langs_dict = get_abstract_langs(self.article_abstract)

        # obtem um dicionário com códigos de idiomas para palavras-chave: {'article': ['pt', 'en'], 'sub-article': ['es']}
        keyword_langs_dict = get_keyword_langs(self.article_kwd)

        # verifica a existência dos elementos no XML
        for article_type, title_langs in title_langs_dict.items():
            if not title_langs:
                yield {
                    'title': f'{article_type} title element lang attribute validation',
                    'xpath': f'.//article-title/@xml:lang',
                    'validation_type': 'exist',
                    'response': 'ERROR',
                    'expected_value': f'title for the {article_type}',
                    'got_value': None,
                    'message': f'Got None expected title for the {article_type}',
                    'advice': f'Provide title for the {article_type}'
                }

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
