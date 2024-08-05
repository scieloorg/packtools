from lxml import etree

from packtools.sps.models.fig import ArticleFigs
from packtools.sps.validation.utils import format_response


class FigValidation:
    """
    A class used to validate the existence of <fig> elements within an XML document.

    Attributes
    ----------
    xmltree : lxml.etree._ElementTree
        The parsed XML document representing the article.
    figures_by_language : dict
        A dictionary containing information about figures grouped by language.

    Methods
    -------
    validate_fig_existence(error_level="WARNING")
        Validates the existence of <fig> elements within the XML document and yields formatted responses.
    """

    def __init__(self, xmltree):
        """
        Initializes a FigValidation object.

        Parameters
        ----------
        xmltree : lxml.etree._ElementTree
            The parsed XML document representing the article.
        """
        self.xmltree = xmltree
        self.figures_by_language = ArticleFigs(xmltree).items_by_lang

    def validate_fig_existence(self, error_level="WARNING"):
        """
        Validates the existence of <fig> elements within the XML document.

        If <fig> elements are found, yields a formatted response for each figure.
        If no <fig> elements are found, yields a single formatted response indicating their absence.

        Parameters
        ----------
        error_level : str, optional
            The level of the error to be reported (default is "WARNING").

        Yields
        ------
        dict
            A dictionary containing the validation response.
        """
        if self.figures_by_language:
            for lang, figure_data_list in self.figures_by_language.items():
                for figure_data in figure_data_list:
                    figure_node = figure_data.get("node").element
                    yield format_response(
                        title="fig presence",
                        parent=figure_data.get("parent"),
                        parent_id=figure_data.get("parent_id"),
                        parent_article_type=figure_data.get("parent_article_type"),
                        parent_lang=figure_data.get("parent_lang"),
                        item="fig",
                        sub_item=None,
                        validation_type="exist",
                        is_valid=True,
                        expected="<fig> element",
                        obtained=etree.tostring(figure_node, encoding='unicode'),
                        advice=None,
                        data=figure_data,
                        error_level="OK",
                    )
        else:
            yield format_response(
                title="fig presence",
                parent="article",
                parent_id=None,
                parent_article_type=self.xmltree.get("article-type"),
                parent_lang=self.xmltree.get(
                    "{http://www.w3.org/XML/1998/namespace}lang"
                ),
                item="fig",
                sub_item=None,
                validation_type="exist",
                is_valid=False,
                expected="<fig> element",
                obtained=None,
                advice="Add <fig> element to illustrate the content.",
                data=None,
                error_level=error_level,
            )
