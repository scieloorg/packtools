from packtools.sps.models import (
    article_titles,
    article_abstract,
    kwd_group
)


def _elements_exist(title_dict, title_object, abstracts, keywords):
    # verifica se existe título no XML
    if not title_object.article_title_dict.get(title_dict.get('lang')):
        return False, True, 'title', './/article-title/@xml:lang', f'title for the {title_dict.get("parent_name")}'
    # verifica se existe palavras-chave sem resumo
    if abstracts == [] and keywords != []:
        return False, True, 'abstract', './/abstract/@xml:lang', f'abstract for the {title_dict.get("parent_name")}'
    # verifica se existe resumo sem palavras-chave
    if abstracts != [] and keywords == []:
        return False, True, 'kwd-group', './/kwd-group/@xml:lang', f'keywords for the {title_dict.get("parent_name")}'
    # verifica se o teste é necessário
    if abstracts == [] and keywords == []:
        return True, False, None, None, None
    return True, True, None, None, None


def get_element_langs(elements):
    return [
        {
            'parent_name': item.get('parent_name'),
            'lang': item.get('lang'),
            **({'id': item['id']} if 'id' in item else {})
        }
        for item in elements if item
    ]


def get_advice(element, title_dict):
    advice = f'Provide {element} in the \'{title_dict.get("lang")}\' language for {title_dict.get("parent_name")}'
    if title_dict.get("id") is not None:
        advice += f' ({title_dict.get("id")})'
    return advice



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
        # obtem uma lista de dicionários com dados de títulos: [{'parent_name': 'article', 'lang': 'pt'},...]
        titles_list = get_element_langs(self.article_title.data)

        # obtem uma lista de dicionários com dados de resumos: [{'parent_name': 'article', 'lang': 'pt'},...]
        abstracts_list = get_element_langs(self.article_abstract.get_abstracts(style='inline'))

        # obtem uma lista de dicionários com dados de palavras-chave: [{'parent_name': 'article', 'lang': 'pt'},...]
        keywords_list = get_element_langs(self.article_kwd)

        # verifica a existência de title no XML
        if not titles_list:
            yield {
                'title': f'XML title element lang attribute validation',
                'xpath': f'.//article-title/@xml:lang',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': f'title for the XML',
                'got_value': None,
                'message': f'Got None expected title for the XML',
                'advice': f'Provide title for the XML'
            }

        # verifica a existência dos elementos no XML
        for title_dict in titles_list:
            exist, is_required, element, xpath, expected = _elements_exist(
                title_dict,
                self.article_title,
                [abstract_dict for abstract_dict in abstracts_list if
                 abstract_dict.get('parent_name') == title_dict.get('parent_name')],
                [keyword_dict for keyword_dict in keywords_list if
                 keyword_dict.get('parent_name') == title_dict.get('parent_name')]
            )

            if exist and is_required:
                # validação de correspondência entre os idiomas, usando como base o título
                for element, langs in zip(['abstract', 'kwd-group'], [abstracts_list, keywords_list]):
                    advice = get_advice(element, title_dict)
                    is_valid = title_dict in langs
                    expected = title_dict.get('lang')
                    obtained = title_dict.get('lang') if is_valid else None
                    yield {
                        'title': f'{title_dict.get("parent_name")} {element} element lang attribute validation',
                        'xpath': f'.//article-title/@xml:lang .//{element}/@xml:lang',
                        'validation_type': 'match',
                        'response': 'OK' if is_valid else 'ERROR',
                        'expected_value': expected,
                        'got_value': obtained,
                        'message': f'Got {obtained} expected {expected}',
                        'advice': None if is_valid else advice
                    }
            elif is_required:
                # resposta para a verificação de ausência de elementos
                advice = get_advice(element, title_dict)
                yield {
                    'title': f'{title_dict.get("parent_name")} {element} element lang attribute validation',
                    'xpath': xpath,
                    'validation_type': 'exist',
                    'response': 'ERROR',
                    'expected_value': expected,
                    'got_value': None,
                    'message': f'Got None expected {expected}',
                    'advice': advice
                }
