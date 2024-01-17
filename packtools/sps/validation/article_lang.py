from packtools.sps.models import (
    article_titles,
    article_abstract,
    kwd_group
)


def _elements_exist(title, abstract, keyword):
    # verifica se existe título no XML
    if not title.article_title.get('text'):
        return False, 'title', './/article-title/@xml:lang', 'title for the article', title.article_title.get('lang')
    # verifica se existe palavras-chave sem resumo
    if abstract == [] and keyword != []:
        return False, 'abstract', './/abstract/@xml:lang', 'abstract for the article', " | ".join(keyword)
    # verifica se existe resumo sem palavras-chave
    if abstract != [] and keyword == []:
        return False, 'kwd-group', './/kwd-group/@xml:lang', 'keywords for the article', " | ".join(abstract)
    return True, None, None, None, None


