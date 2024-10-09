from packtools.sps.models import (
    article_titles,
    article_abstract,
    kwd_group,
    article_and_subarticles,
)


def _elements_exist(parent, titles, abstracts, keywords):
    """
    Verifica se os elementos de título, resumo e palavras-chave estão presentes no XML.

    Args:
        parent (str): Nome do elemento pai.
        titles (list): Lista de títulos no XML com 'parent' e 'lang' filtrados.
        abstracts (list): Lista de resumos no XML com 'parent' e 'lang' filtrados.
        keywords (list): Lista de palavras-chave no XML com 'parent' e 'lang' filtrados.

    Returns:
        tuple: Um tupla contendo:
            - bool: Indica se os elementos existem.
            - bool: Indica se o elemento é obrigatório.
            - str: Nome do elemento ausente, se houver.
            - str: XPath do elemento ausente, se houver.
            - str: Valor esperado para o elemento ausente.
    """
    # verifica se existe título no XML
    if not titles:
        return False, True, 'title', './/article-title/@xml:lang', f'title for the {parent}'
    # verifica se existe palavras-chave sem resumo
    if abstracts == [] and keywords != []:
        return False, True, 'abstract', './/abstract/@xml:lang', f'abstract for the {parent}'
    # verifica se existe resumo sem palavras-chave
    if abstracts != [] and keywords == []:
        return False, True, 'kwd-group', './/kwd-group/@xml:lang', f'keywords for the {parent}'
    # verifica se o teste é necessário
    if abstracts == [] and keywords == []:
        return True, False, None, None, None
    return True, True, None, None, None


def get_element_langs(elements):
    """
    Extrai informações de idioma e nome do elemento pai de uma lista de elementos.

    Args:
        elements (list): Lista de elementos contendo dados de idioma e nome do pai.

    Returns:
        list: Lista de dicionários contendo as chaves 'parent_name', 'lang' e, opcionalmente, 'id' ou 'article_id'.
    """
    return [
        {
            'parent_name': item.get('parent_name'),
            'lang': item.get('lang'),
            **({'id': item['id']} if 'id' in item else {}),
            **({'id': item['article_id']} if 'article_id' in item else {})
        }
        for item in elements if item
    ]


def get_advice(element, element_dict):
    """
    Gera uma mensagem de conselho sobre a falta de um elemento baseado no idioma e no nome do pai.

    Args:
        element (str): O tipo de elemento (por exemplo, 'title', 'abstract', 'kwd-group').
        element_dict (dict): Dicionário contendo informações sobre o idioma e o elemento pai.

    Returns:
        str: Mensagem de conselho formatada.
    """
    advice = f'Provide {element} in the \'{element_dict.get("lang")}\' language for {element_dict.get("parent_name")}'
    if element_dict.get("id") is not None:
        advice += f' ({element_dict.get("id")})'
    return advice


def filter_by_parent_and_lang(element_list, parent, lang):
    """
    Filtra uma lista de elementos pelo nome do pai e pelo idioma.

    Args:
        element_list (list): Lista de dicionários de elementos.
        parent (str): Nome do elemento pai a ser filtrado.
        lang (str): Idioma a ser filtrado.

    Returns:
        list: Lista filtrada de elementos que correspondem ao pai e idioma fornecidos.
    """
    return [element_dict for element_dict in element_list if
            element_dict['parent_name'] == parent and element_dict['lang'] == lang]


class ArticleLangValidation:
    """
    Classe que realiza validações de idiomas para os elementos de um artigo como títulos, resumos e palavras-chave.

    Args:
        xml_tree (lxml.etree._Element): A árvore XML que representa o artigo.
    """

    def __init__(self, xml_tree):
        self.article_title = article_titles.ArticleTitles(xml_tree)
        self.article_abstract = article_abstract.Abstract(xml_tree)
        self.article_kwd = kwd_group.KwdGroup(xml_tree).extract_kwd_data_with_lang_text_by_article_type(None)
        self.article_and_subarticles = article_and_subarticles.ArticleAndSubArticles(xml_tree)

    def validate_article_lang(self):
        """
        Verifica se os elementos de título, resumo e palavras-chave estão presentes no XML
        e se os respectivos idiomas correspondem.

        XML de entrada
        --------------
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
            Uma lista de dicionários, como:
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
        # obtem uma lista de dicionários com dados de artigo e sub-artigos: [{'parent_name': 'article', 'lang': 'pt'},...]
        article_and_subarticles_list = get_element_langs(self.article_and_subarticles.data)

        # obtem uma lista de dicionários com dados de títulos: [{'parent_name': 'article', 'lang': 'pt'},...]
        titles_list = get_element_langs(self.article_title.data)

        # obtem uma lista de dicionários com dados de resumos: [{'parent_name': 'article', 'lang': 'pt'},...]
        abstracts_list = get_element_langs(self.article_abstract.get_abstracts(style='inline'))

        # obtem uma lista de dicionários com dados de palavras-chave: [{'parent_name': 'article', 'lang': 'pt'},...]
        keywords_list = get_element_langs(self.article_kwd)

        # verifica a existência dos elementos no XML
        for article_and_subarticles_dict in article_and_subarticles_list:
            parent = article_and_subarticles_dict['parent_name']
            lang = article_and_subarticles_dict['lang']
            titles_filtered = filter_by_parent_and_lang(titles_list, parent, lang)
            abstracts_filtered = filter_by_parent_and_lang(abstracts_list, parent, lang)
            keywords_filtered = filter_by_parent_and_lang(keywords_list, parent, lang)

            exist, is_required, element, xpath, expected = _elements_exist(
                parent,
                titles_filtered,
                abstracts_filtered,
                keywords_filtered
            )

            if exist and is_required:
                # validação de correspondência entre os idiomas, usando como base o título
                for element, langs in zip(['title', 'abstract', 'kwd-group'],
                                          [titles_filtered, abstracts_filtered, keywords_filtered]):
                    advice = get_advice(element, article_and_subarticles_dict)
                    is_valid = article_and_subarticles_dict in langs
                    expected = article_and_subarticles_dict.get('lang')
                    obtained = article_and_subarticles_dict.get('lang') if is_valid else None
                    yield {
                        'title': f'{article_and_subarticles_dict.get("parent_name")} {element} element lang attribute validation',
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
                advice = get_advice(element, article_and_subarticles_dict)
                yield {
                    'title': f'{article_and_subarticles_dict.get("parent_name")} {element} element lang attribute validation',
                    'xpath': xpath,
                    'validation_type': 'exist',
                    'response': 'ERROR',
                    'expected_value': expected,
                    'got_value': None,
                    'message': f'Got None expected {expected}',
                    'advice': advice
                }
