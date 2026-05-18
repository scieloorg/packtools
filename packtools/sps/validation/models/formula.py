from packtools.sps.models.formula import Formula
from packtools.sps.utils.xml_utils import get_parent_context, put_parent_context


class ArticleFormulas:
    """
    Represents an article with its associated formulas, grouped by language.

    Parameters:
        xml_tree (xml.etree.ElementTree.ElementTree): The parsed XML document representing the article.
    """

    def __init__(self, xml_tree):
        self.xml_tree = xml_tree

    @property
    def disp_formula_items(self):
        """
        Generator that yields formulas with their respective parent context.

        Yields:
            dict: A dictionary containing the formula data along with its parent context,
                  including language and article type details.
        """
        for node, lang, article_type, parent, parent_id in get_parent_context(self.xml_tree):
            for item in node.xpath(".//disp-formula"):
                formula = Formula(item)
                data = formula.data
                parent_data = put_parent_context(data, lang, article_type, parent, parent_id)
                yield parent_data

    @property
    def inline_formula_items(self):
        """
        Generator that yields inline formulas with their respective parent context.

        Yields:
            dict: A dictionary containing the formula data along with its parent context,
                  including language and article type details.
        """
        for node, lang, article_type, parent, parent_id in get_parent_context(self.xml_tree):
            for item in node.xpath(".//inline-formula"):
                formula = Formula(item)
                data = formula.data
                parent_data = put_parent_context(data, lang, article_type, parent, parent_id)
                yield parent_data

    @property
    def disp_formula_items_by_lang(self):
        """
        Returns a dictionary of formulas grouped by language.
        """
        langs = {}
        for item in self.disp_formula_items:
            lang = item.get("parent_lang")
            langs[lang] = item
        return langs

    @property
    def inline_formula_items_by_lang(self):
        """
        Returns a dictionary of inline formulas grouped by language.
        """
        langs = {}
        for item in self.inline_formula_items:
            lang = item.get("parent_lang")
            langs[lang] = item
        return langs
