from packtools.sps.models import article_and_subarticles, article_titles, article_abstract, kwd_group
from packtools.sps.validation.utils import format_response


def _elements_exist(title, abstract, keyword):
    """
    Verifica a existência dos elementos de título, resumo e palavras-chave no XML.

    Parâmetros
    ----------
    title : dict
        Dicionário com dados do título do artigo no XML.
    abstract : dict
        Dicionário com dados do resumo do artigo no XML.
    keyword : dict
        Dicionário com dados dss palavras-chave do artigo no XML.

    Retorna
    -------
    tuple
        Um tuple contendo três valores:
        - bool: Se todos os elementos necessários estão presentes.
        - bool: Se o elemento ausente é obrigatório.
        - str: O nome do elemento ausente, se houver.
    """
    # Verifica se existe título no XML
    if not title:
        return False, True, 'article title'
    # Verifica se existe palavras-chave sem resumo
    if not abstract and keyword:
        return False, True, 'abstract'
    # Verifica se existe resumo sem palavras-chave
    if abstract and not keyword:
        return False, True, 'kwd-group'
    return True, False, None


class MetadataLanguagesValidation:
    """
    Classe para validação de idiomas de artigos no XML. Verifica se os elementos
    de título, resumo e palavras-chave estão presentes no XML e se os respectivos
    idiomas correspondem.

    Atributos
    ---------
    article_and_subarticles : ArticleAndSubArticles
        Instância que contém dados de artigos e subartigos do XML.
    article_title : ArticleTitles
        Instância que contém títulos do artigo por idioma.
    article_abstract : ArticleAbstract
        Instância que contém resumos do artigo por idioma.
    article_kwd : ArticleKeywords
        Instância que contém palavras-chave do artigo por idioma.
    """

    def __init__(self, xml_tree):
        """
        Inicializa a classe com a árvore XML fornecida.

        Parâmetros
        ----------
        xml_tree : ElementTree
            A árvore XML do artigo a ser validado.
        """
        self.article_and_subarticles = article_and_subarticles.ArticleAndSubArticles(xml_tree)
        self.article_title = article_titles.ArticleTitles(xml_tree)
        self.article_abstract = article_abstract.ArticleAbstract(xml_tree)
        self.article_kwd = kwd_group.ArticleKeywords(xml_tree)
        self.xml_tree = xml_tree

    def validate(self, error_level="ERROR"):
        """
        Valida os idiomas dos elementos de título, resumo e palavras-chave no XML,
        e gera uma resposta de validação para cada verificação.

        Parâmetros
        ----------
        error_level : str, opcional
            O nível de erro a ser retornado na resposta (padrão é "ERROR").

        Retorna
        -------
        generator
            Gera dicionários que contêm os resultados de validação para cada
            idioma de artigo/subartigo, com as informações sobre a validação e
            eventuais erros encontrados.
        """
        # Títulos indexados por idioma
        titles_by_lang = self.article_title.article_title_dict

        # Resumos indexados por idioma
        abstracts_by_lang = self.article_abstract.get_abstracts_by_lang()

        # Palavras-chave indexadas por idioma
        self.article_kwd.configure()
        keywords_by_lang = self.article_kwd.items_by_lang

        # Idiomas do xml
        XML_NS = "{http://www.w3.org/XML/1998/namespace}lang"
        languages = {self.xml_tree.attrib.get(XML_NS)} if self.xml_tree.attrib.get(XML_NS) else set()
        languages.update(
            elem.attrib.get(XML_NS) for elem in self.xml_tree.findall(f".//*[@{XML_NS}]") if elem.attrib.get(XML_NS)
        )

        # Verifica a existência dos elementos no XML
        for lang in list(languages):
            title = titles_by_lang.get(lang)
            abstract = abstracts_by_lang.get(lang)
            keyword = keywords_by_lang.get(lang)

            exist, is_required, missing_element_name = _elements_exist(title, abstract, keyword)

            if not exist and is_required:
                # Resposta para a verificação de ausência de elementos
                yield format_response(
                    title=f'{missing_element_name} element lang attribute',
                    parent=None,
                    parent_id=None,
                    parent_article_type=None,
                    parent_lang=lang,
                    item=missing_element_name,
                    sub_item=None,
                    validation_type='match',
                    is_valid=False,
                    expected=f"{missing_element_name} in {lang}",
                    obtained=None,
                    advice=f'Mark {missing_element_name} for {lang} language',
                    data=None,
                    error_level=error_level,
                )
