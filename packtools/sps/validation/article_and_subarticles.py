from packtools.sps.validation import exceptions
from packtools.sps.models.article_and_subarticles import ArticleAndSubArticles
from langcodes import tag_is_valid


def validate_language(xml):
    """
    Params
    ------
    xml: ElementTree

    Returns
    -------
        A tuple comprising the validation status and the errors list.
    """
    errors = []

    art_and_subarts = ArticleAndSubArticles(xml)

    for i in art_and_subarts.data:
        _lang = i.get('lang')
        _article_type = i.get('article_type')

        if _lang is None:
            _message = f'XML {_article_type} has no language.'
            errors.append(exceptions.ValidationArticleAndSubArticlesUnavailableLanguage(
                message=_message,
                line=i.get('line_number'),
            ))

        elif not tag_is_valid(_lang):
            _message = f'XML {_article_type} has an invalid language: {_lang}'
            errors.append(exceptions.ValidationArticleAndSubArticlesHasInvalidLanguage(
                message=_message,
                line=i.get('line_number'),
            ))
   
    return len(errors) == 0, errors
