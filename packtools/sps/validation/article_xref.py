from ..models.article_xref import ArticleXref


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
                    'context': 'xref element rid attribute validation',
                    'result': 'OK',
                    'expected_value': 'aff1',
                    'got_value': 'aff1',
                    'error_type': None,
                    'message': 'rid have the respective id'
                    },
                    {
                    'context': 'xref element rid attribute validation',
                    'result': 'OK',
                    'expected_value': 'fig1',
                    'got_value': 'fig1',
                    'error_type': None,
                    'message': 'rid have the respective id'
                    },
                    {
                    'context': 'xref element rid attribute validation',
                    'result': 'ERROR',
                    'expected_value': 'table1',
                    'got_value': None,
                    'error_type': 'no match',
                    'message': 'rid does not have the respective id'
                    }
                ]
        }
        """
        rids = sorted(self.article_xref.all_xref_rids)
        ids = sorted(self.article_xref.all_ids)
        resp = {'validation': []}
        for rid in rids:
            item = {
                'context': 'xref element rid attribute validation'
            }
            validated = rid in ids
            item['result'] = 'OK' if validated else 'ERROR'
            item['expected_value'] = rid
            item['got_value'] = rid if validated else None
            item['error_type'] = None if validated else 'no match'
            item['message'] = 'rid have the respective id' if validated else 'rid does not have the respective id'
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
                    'context': 'xref element id attribute validation',
                    'result': 'OK',
                    'expected_value': 'aff1',
                    'got_value': 'aff1',
                    'error_type': None,
                    'message': 'rid have the respective id'
                    },
                    {
                    'context': 'xref element id attribute validation',
                    'result': 'OK',
                    'expected_value': 'fig1',
                    'got_value': 'fig1',
                    'error_type': None,
                    'message': 'rid have the respective id'
                    },
                    {
                    'context': 'xref element id attribute validation',
                    'result': 'ERROR',
                    'expected_value': 'table1',
                    'got_value': None,
                    'error_type': 'no match',
                    'message': 'rid does not have the respective id'
                    }
                ]
        }
        """
        rids = sorted(self.article_xref.all_xref_rids)
        ids = sorted(self.article_xref.all_ids)
        resp = {'validation': []}
        for id in ids:
            item = {
                'context': 'xref element id attribute validation'
            }
            validated = id in rids
            item['result'] = 'OK' if validated else 'ERROR'
            item['expected_value'] = id
            item['got_value'] = id if validated else None
            item['error_type'] = None if validated else 'no match'
            item['message'] = 'id have the respective rid' if validated else 'id does not have the respective rid'
            resp['validation'].append(item)
        return resp

    @property
    def ids_without_rids(self):
        return self.article_xref.all_ids - self.article_xref.all_xref_rids

    @property
    def rids_without_ids(self):
        return self.article_xref.all_xref_rids - self.article_xref.all_ids

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
