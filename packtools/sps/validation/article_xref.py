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
                    'expected_value': True,
                    'got_value': True,
                    'message': 'Got True, expected True',
                    'advice': 'For each xref[@rid="aff1"] must have one corresponding element which @id="aff1"'
                    },
                    {
                    'title': 'xref element rid attribute validation',
                    'xpath': './/xref[@rid]',
                    'validation_type': 'match',
                    'response': 'OK',
                    'expected_value': True,
                    'got_value': True,
                    'message': 'Got True, expected True',
                    'advice': 'For each xref[@rid="fig1"] must have one corresponding element which @id="fig1"'
                    },
                    {
                    'title': 'xref element rid attribute validation',
                    'xpath': './/xref[@rid]',
                    'validation_type': 'match',
                    'response': 'ERROR',
                    'expected_value': True,
                    'got_value': False,
                    'message': 'Got False, expected True',
                    'advice': 'For each xref[@rid="table1"] must have one corresponding element which @id="table1"'
                    }
                ]
        }
        """
        rids = sorted(self.article_xref.all_xref_rids)
        ids = sorted(self.article_xref.all_ids)
        resp = {'validation': []}
        for rid in rids:
            item = {
                'title': _('xref element rid attribute validation'),
                'xpath': _('.//xref[@rid]'),
                'validation_type': _('match'),
            }
            validated = rid in ids
            item['response'] = 'OK' if validated else 'ERROR'
            item['expected_value'] = True
            item['got_value'] = validated
            item['message'] = _('Got {}, expected True').format(validated)
            item['advice'] = 'For each xref[@rid="{}"] must have one corresponding element which @id="{}"'.format(rid, rid)
            resp['validation'].append(item)
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
                    'expected_value': True,
                    'got_value': True,
                    'message': 'Got True, expected True',
                    'advice': 'For each @id="aff1" must have one corresponding element which xref[@rid="aff1"]'
                    },
                    {
                    'title': 'xref element id attribute validation',
                    'xpath': './/*[@id]',
                    'validation_type': 'match',
                    'response': 'OK',
                    'expected_value': True,
                    'got_value': True,
                    'message': 'Got True, expected True',
                    'advice': 'For each @id="fig1" must have one corresponding element which xref[@rid="fig1"]'
                    },
                    {
                    'title': 'xref element id attribute validation',
                    'xpath': './/*[@id]',
                    'validation_type': 'match',
                    'response': 'ERROR',
                    'expected_value': True,
                    'got_value': False,
                    'message': 'Got False, expected True',
                    'advice': 'For each @id="table1" must have one corresponding element which xref[@rid="table1"]'
                    }
                ]
        }
        """
        rids = sorted(self.article_xref.all_xref_rids)
        ids = sorted(self.article_xref.all_ids)
        resp = {'validation': []}
        for id in ids:
            item = {
                'title': _('xref element id attribute validation'),
                'xpath': _('.//*[@id]'),
                'validation_type': _('match')
            }
            validated = id in rids
            item['response'] = 'OK' if validated else 'ERROR'
            item['expected_value'] = True
            item['got_value'] = validated
            item['message'] = _('Got {}, expected True').format(validated)
            item['advice'] = 'For each @id="{}" must have one corresponding element which xref[@rid="{}"]'.format(id, id)
            resp['validation'].append(item)
        return resp

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
