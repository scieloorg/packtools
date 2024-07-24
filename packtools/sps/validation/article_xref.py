from ..models.article_xref import ArticleXref
from packtools.sps.validation.utils import format_response


class ArticleXrefValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.article_xref = ArticleXref(xmltree)
        self.data = list(self.article_xref.data())

    def validate_rid(self, error_level="ERROR"):
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
            'advice': 'For each xref[@rid="aff1"] must have at least one corresponding element which @id="aff1"'
            },
            {
            'title': 'xref element rid attribute validation',
            'xpath': './/xref[@rid]',
            'validation_type': 'match',
            'response': 'OK',
            'expected_value': fig1,
            'got_value': fig1,
            'message': 'Got fig1, expected fig1',
            'advice': 'For each xref[@rid="fig1"] must have at least one corresponding element which @id="fig1"'
            },
            {
            'title': 'xref element rid attribute validation',
            'xpath': './/xref[@rid]',
            'validation_type': 'match',
            'response': 'ERROR',
            'expected_value': table1,
            'got_value': None,
            'message': 'Got None, expected table1',
            'advice': 'For each xref[@rid="table1"] must have at least one corresponding element which @id="table1"'
            }
        ]

        """
        for item in self.data:
            rids = item.get("rids")
            ids = [id_tuple[1] for id_tuple in item.get("ids")]
            for rid in rids:
                is_valid = rid in ids
                yield format_response(
                    title="xref element rid attribute validation",
                    parent=item.get("parent"),
                    parent_id=item.get("parent_id"),
                    parent_article_type=item.get("parent_article_type"),
                    parent_lang=item.get("parent_lang"),
                    item="xref",
                    sub_item="@rid",
                    validation_type="match",
                    is_valid=is_valid,
                    expected=rid,
                    obtained=rid if is_valid else None,
                    advice='For each xref[@rid="{}"] must have at least one corresponding element which @id="{}"'.format(rid, rid),
                    data=item,
                    error_level=error_level,
                )

    def validate_id(self, error_level="ERROR"):
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
            'advice': 'For each @id="aff1" must have at least one corresponding element which xref[@rid="aff1"]'
            },
            {
            'title': 'xref element id attribute validation',
            'xpath': './/*[@id]',
            'validation_type': 'match',
            'response': 'OK',
            'expected_value': fig1,
            'got_value': fig1,
            'message': 'Got fig1, expected fig1',
            'advice': 'For each @id="fig1" must have at least one corresponding element which xref[@rid="fig1"]'
            },
            {
            'title': 'xref element id attribute validation',
            'xpath': './/*[@id]',
            'validation_type': 'match',
            'response': 'ERROR',
            'expected_value': table1,
            'got_value': None,
            'message': 'Got None, expected table1',
            'advice': 'For each @id="table1" must have at least one corresponding element which xref[@rid="table1"]'
            }
        ]
        """
        for item in self.data:
            rids = item.get("rids")
            ids = item.get("ids")
            for id_tuple in ids:
                tag, id = id_tuple
                is_valid = id in rids
                yield format_response(
                    title="element id attribute validation",
                    parent=item.get("parent"),
                    parent_id=item.get("parent_id"),
                    parent_article_type=item.get("parent_article_type"),
                    parent_lang=item.get("parent_lang"),
                    item=tag,
                    sub_item="@id",
                    validation_type="match",
                    is_valid=is_valid,
                    expected=id,
                    obtained=id if is_valid else None,
                    advice='For each @id="{}" must have at least one corresponding element which xref[@rid="{}"]'.format(id, id),
                    data=item,
                    error_level=error_level,
                )

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
