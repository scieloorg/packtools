from packtools.sps.models.v2.article_xref import ArticleXref
from packtools.sps.validation.utils import format_response


class ArticleXrefValidation:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree
        self.article_xref = ArticleXref(xml_tree)

    def validate_rid(self, element_name=None, error_level="ERROR"):
        """
        Checks if all `rid` attributes (source) in `<xref>` elements have corresponding `id` attributes (destination)
        in the XML document.

    Parameters
    ----------
    element_name : str
        The name of the element to be validated.
    error_level : str, optional
        The level of error reporting (default is "ERROR").

    Yields
    ------
    dict
        A dictionary containing the following keys:
        - title (str): The title of the validation.
        - xpath (str): The XPath query used to locate the elements being validated.
        - validation_type (str): The type of validation being performed (e.g., "match").
        - response (str): The result of the validation ("OK" or "ERROR").
        - expected_value (str): The expected `rid` value.
        - got_value (str or None): The actual value found or `None` if not found.
        - message (str): A message explaining the result of the validation.
        - advice (str): A recommendation or advice based on the validation result.
        - error_level (str): The level of error reporting.
        - data (dict): Additional data related to the validation context, which includes:
            - parent (str): The parent element's tag.
            - parent_id (str or None): The `id` of the parent element, if available.
            - parent_article_type (str): The type of the article (e.g., "research-article").
            - parent_lang (str): The language of the parent element.
            - tag (str): The tag of the element being validated.
            - attributes (dict): A dictionary of the element's attributes.
        """

        ids = self.article_xref.all_ids(element_name)
        for rid, rid_list in self.article_xref.all_xref_rids().items():
            for rid_data in rid_list:
                is_valid = rid in ids
                yield format_response(
                    title="xref element rid attribute validation",
                    parent="article",
                    parent_id=None,
                    parent_article_type=self.xml_tree.get("article-type"),
                    parent_lang=self.xml_tree.get("{http://www.w3.org/XML/1998/namespace}lang"),
                    item="xref",
                    sub_item="@rid",
                    validation_type="match",
                    is_valid=is_valid,
                    expected=rid,
                    obtained=rid if is_valid else None,
                    advice='For each xref[@rid="{}"] must have at least one corresponding element which @id="{}"'.format(rid, rid),
                    data=rid_data,
                    error_level=error_level,
                )

    def validate_id(self, element_name=None, error_level="ERROR"):
        """
        Checks if all `id` attributes (destination) in the XML document have corresponding `rid` attributes (source)
        in `<xref>` elements.

    Parameters
    ----------
    element_name : str
        The name of the element to be validated.
    error_level : str, optional
        The level of error reporting (default is "ERROR").

    Yields
    ------
    dict
        A dictionary containing the following keys:
        - title (str): The title of the validation.
        - xpath (str): The XPath query used to locate the elements being validated.
        - validation_type (str): The type of validation being performed (e.g., "match").
        - response (str): The result of the validation ("OK" or "ERROR").
        - expected_value (str): The expected `id` value.
        - got_value (str or None): The actual value found or `None` if not found.
        - message (str): A message explaining the result of the validation.
        - advice (str): A recommendation or advice based on the validation result.
        - error_level (str): The level of error reporting.
        - data (dict): Additional data related to the validation context, which includes:
            - parent (str): The parent element's tag.
            - parent_id (str or None): The `id` of the parent element, if available.
            - parent_article_type (str): The type of the article (e.g., "research-article").
            - parent_lang (str): The language of the parent element.
            - tag (str): The tag of the element being validated.
            - attributes (dict): A dictionary of the element's attributes.
        """
        rids = self.article_xref.all_xref_rids()
        for id, id_list in self.article_xref.all_ids(element_name).items():
            for id_data in id_list:
                is_valid = id in rids
                yield format_response(
                    title="element id attribute validation",
                    parent=id_data.get("parent"),
                    parent_id=id_data.get("parent_id"),
                    parent_article_type=id_data.get("parent_article_type"),
                    parent_lang=id_data.get("parent_lang"),
                    item=id_data.get("tag"),
                    sub_item="@id",
                    validation_type="match",
                    is_valid=is_valid,
                    expected=id,
                    obtained=id if is_valid else None,
                    advice='For each @id="{}" must have at least one corresponding element which xref[@rid="{}"]'.format(id, id),
                    data=id_data,
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
