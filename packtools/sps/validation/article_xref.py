from packtools.sps.models.v2.article_xref import ArticleXref
from packtools.sps.validation.utils import format_response


class ArticleXrefValidation:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree
        self.article_xref = ArticleXref(xml_tree)

    def validate_xref_rid_has_corresponding_element_id(self, error_level="ERROR"):
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

        ids = self.article_xref.all_ids("*")
        for rid, rid_list in self.article_xref.all_xref_rids().items():
            for xref in rid_list:
                is_valid = rid in ids
                element_name = xref.get("element_name")
                ref_type = xref.get("ref-type")
                yield format_response(
                    title="xref[@rid] -> *[@id]",
                    parent="article",
                    parent_id=None,
                    parent_article_type=self.xml_tree.get("article-type"),
                    parent_lang=self.xml_tree.get(
                        "{http://www.w3.org/XML/1998/namespace}lang"
                    ),
                    item="xref",
                    sub_item="@rid",
                    validation_type="match",
                    is_valid=is_valid,
                    expected=rid,
                    obtained=rid if is_valid else None,
                    advice=f'Found <xref rid="{rid}" ref-type="{ref_type}">...</xref>, but not found the corresponding '
                           f'<{element_name} id="{rid}">. Check if the value rid="" and ref-type="" are correct and '
                           f'check if <{element_name}> have correct id=""',
                    data=xref,
                    error_level=error_level,
                )

    def validate_element_id_has_corresponding_xref_rid(self, elements_requires_xref_rid=None, error_level="ERROR"):
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
        elements_requires_xref_rid = elements_requires_xref_rid or []
        default_error_level = error_level
        rids = self.article_xref.all_xref_rids()
        for id, id_list in self.article_xref.all_ids("*").items():
            for id_data in id_list:
                tag = id_data.get("tag")
                if tag in elements_requires_xref_rid:
                    error_level = "CRITICAL"
                    expectation = "must"
                else:
                    error_level = default_error_level
                    expectation = "can"
                is_valid = id in rids
                ref_type = rids.get(id)
                yield format_response(
                    title="*[@id] -> xref[@rid]",
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
                    advice=f'Found <{tag} id="{id}">...</{tag}>, but no corresponding <xref rid="{id}"> found. '
                           f'Check if it is missing to mark the cross-reference (<xref rid="{id}" ref-type="{ref_type}">) to <{tag} id="{id}">',
                    data=id_data,
                    error_level=error_level,
                )
