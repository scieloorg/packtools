from ..models.article_xref import ArticleXref
from packtools.translator import _


class ArticleXrefValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.article_xref = ArticleXref(xmltree)

    def validate_rid(self):
        """
        Checks if all rids (source) have the respective ids (destination)

        Returns
        -------
        dict
            A dictionary that registers the rids, ids, the difference between them and a message.

        Examples
        --------
        >>> validate_rid()

        {
            'validation':
                [
                    {
                    'title': 'xref element rid attribute validation',
                    'xpath': './/xref[@rid]',
                    'validation_type': 'match',
                    'response': 'OK',
                    'expected_value': 'aff1',
                    'got_value': 'aff1',
                    'message': 'rid have the respective id',
                    'advice': None
                    },
                    {
                    'title': 'xref element rid attribute validation',
                    'xpath': './/xref[@rid]',
                    'validation_type': 'match',
                    'response': 'OK',
                    'expected_value': 'fig1',
                    'got_value': 'fig1',
                    'message': 'rid have the respective id',
                    'advice': None
                    },
                    {
                    'title': 'xref element rid attribute validation',
                    'xpath': './/xref[@rid]',
                    'validation_type': 'match',
                    'response': 'ERROR',
                    'expected_value': 'table1',
                    'got_value': None,
                    'message': 'rid does not have the respective id',
                    'advice': 'add attribute id = table1 to the corresponding rid = table1'
                    }
                ]
        }
        """
        rids = sorted(self.article_xref.all_xref_rids)
        ids = sorted(self.article_xref.all_ids)
        resp = {_('validation'): []}
        for rid in rids:
            item = {
                _('title'): _('xref element rid attribute validation'),
                _('xpath'): _('.//xref[@rid]'),
                _('validation_type'): _('match'),
            }
            validated = rid in ids
            item[_('response')] = 'OK' if validated else 'ERROR'
            item[_('expected_value')] = rid
            item[_('got_value')] = rid if validated else None
            item[_('message')] = _('rid have the respective id') if validated else _('rid does not have the respective id')
            item[_('advice')] = None if validated else _(f'add attribute id = {rid} to the corresponding rid = {rid}')
            resp[_('validation')].append(item)
        return resp

    def validate_id(self):
        """
        Checks if all ids (destination) have the respective rids (source)

        Returns
        -------
        dict
            A dictionary that registers the rids, ids, the difference between them and a message.

        Examples
        --------
        >>> validate_id()

        {
            'validation':
                [
                    {
                    'title': 'xref element id attribute validation',
                    'xpath': './/*[@id]',
                    'validation_type': 'match',
                    'response': 'OK',
                    'expected_value': 'aff1',
                    'got_value': 'aff1',
                    'message': 'id have the respective rid',
                    'advice': None
                    },
                    {
                    'title': 'xref element id attribute validation',
                    'xpath': './/*[@id]',
                    'validation_type': 'match',
                    'response': 'OK',
                    'expected_value': 'fig1',
                    'got_value': 'fig1',
                    'message': 'id have the respective rid',
                    'advice': None
                    },
                    {
                    'title': 'xref element id attribute validation',
                    'xpath': './/*[@id]',
                    'validation_type': 'match',
                    'response': 'ERROR',
                    'expected_value': 'table1',
                    'got_value': None,
                    'message': 'id does not have the respective rid',
                    'advice': 'add attribute rid = table1 to the corresponding id = table1'
                    }
                ]
        }
        """
        rids = sorted(self.article_xref.all_xref_rids)
        ids = sorted(self.article_xref.all_ids)
        resp = {'validation': []}
        for id in ids:
            item = {
                _('title'): _('xref element id attribute validation'),
                _('xpath'): _('.//*[@id]'),
                _('validation_type'): _('match')
            }
            validated = id in rids
            item[_('response')] = 'OK' if validated else 'ERROR'
            item[_('expected_value')] = id
            item[_('got_value')] = id if validated else None
            item[_('message')] = _('id have the respective rid') if validated else _('id does not have the respective rid')
            item[_('advice')] = None if validated else _(f'add attribute rid = {id} to the corresponding id = {id}')
            resp[_('validation')].append(item)
        return resp

    def validate(self, data):
        """
        Função que executa as validações da classe ArticleXrefValidation.

        Returns:
            dict: Um dicionário contendo os resultados das validações realizadas.
        
        """        
        xref_id_results = {
            _('article_xref_id_validation'): self.validate_id()
            }
        xref_rid_results = { 
            _('article_xref_rid_validation'): self.validate_rid()
            }
        
        xref_id_results.update(xref_rid_results)
        return xref_id_results
