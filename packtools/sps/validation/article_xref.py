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

        [
            {
            'title': 'xref element rid attribute validation',
            'xpath': './/xref[@rid]',
            'validation_type': 'match',
            'response': 'OK',
            'expected_value': aff1,
            'got_value': aff1,
            'message': 'Got aff1, expected aff1',
            'advice': 'For each xref[@rid="aff1"] must have one corresponding element which @id="aff1"'
            },
            {
            'title': 'xref element rid attribute validation',
            'xpath': './/xref[@rid]',
            'validation_type': 'match',
            'response': 'OK',
            'expected_value': fig1,
            'got_value': fig1,
            'message': 'Got fig1, expected fig1',
            'advice': 'For each xref[@rid="fig1"] must have one corresponding element which @id="fig1"'
            },
            {
            'title': 'xref element rid attribute validation',
            'xpath': './/xref[@rid]',
            'validation_type': 'match',
            'response': 'ERROR',
            'expected_value': table1,
            'got_value': None,
            'message': 'Got None, expected table1',
            'advice': 'For each xref[@rid="table1"] must have one corresponding element which @id="table1"'
            }
        ]

        """
        rids = sorted(self.article_xref.all_xref_rids)
        ids = sorted(self.article_xref.all_ids)
        for rid in rids:
            item = {
                'title': _('xref element rid attribute validation'),
                'xpath': _('.//xref[@rid]'),
                'validation_type': _('match'),
            }
            validated = rid in ids
            item['response'] = 'OK' if validated else 'ERROR'
            item['expected_value'] = rid
            item['got_value'] = rid if validated else None
            item['message'] = _('Got {}, expected {}').format(item['got_value'], rid)
            item['advice'] = None if validated else 'For each xref[@rid="{}"] must have one corresponding element which @id="{}"'.format(rid, rid)
            yield item

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

       [
            {
            'title': 'xref element id attribute validation',
            'xpath': './/*[@id]',
            'validation_type': 'match',
            'response': 'OK',
            'expected_value': aff1,
            'got_value': aff1,
            'message': 'Got aff1, expected aff1',
            'advice': 'For each @id="aff1" must have one corresponding element which xref[@rid="aff1"]'
            },
            {
            'title': 'xref element id attribute validation',
            'xpath': './/*[@id]',
            'validation_type': 'match',
            'response': 'OK',
            'expected_value': fig1,
            'got_value': fig1,
            'message': 'Got fig1, expected fig1',
            'advice': 'For each @id="fig1" must have one corresponding element which xref[@rid="fig1"]'
            },
            {
            'title': 'xref element id attribute validation',
            'xpath': './/*[@id]',
            'validation_type': 'match',
            'response': 'ERROR',
            'expected_value': table1,
            'got_value': None,
            'message': 'Got None, expected table1',
            'advice': 'For each @id="table1" must have one corresponding element which xref[@rid="table1"]'
            }
        ]
        """
        rids = sorted(self.article_xref.all_xref_rids)
        ids = sorted(self.article_xref.all_ids)
        for id in ids:
            item = {
                'title': _('element id attribute validation'),
                'xpath': _('.//*[@id]'),
                'validation_type': _('match')
            }
            validated = id in rids
            item['response'] = 'OK' if validated else 'ERROR'
            item['expected_value'] = id
            item['got_value'] = id if validated else None
            item['message'] = _('Got {}, expected {}').format(item['got_value'], id)
            item['advice'] = None if validated else 'For each @id="{}" must have one corresponding element which xref[@rid="{}"]'.format(id, id)
            yield item

    def validate(self, data):
        """
        Função que executa as validações da classe ArticleXrefValidation.

        Returns:
            dict: Um dicionário contendo os resultados das validações realizadas.
        
        """        
        xref_id_results = {
            'article_xref_id_validation': self.validate_id()
            }
        xref_rid_results = { 
            'article_xref_rid_validation': self.validate_rid()
            }
        
        xref_id_results.update(xref_rid_results)
        return xref_id_results
