import logging

from packtools.sps.utils import xml_utils

logger = logging.getLogger(__name__)


def _looks_like_institution_name(text, special_chars):
    """
    Checks whether all characters in text are alphanumeric, spaces or belong to the list of characters considered valid
     in composing the name of the funding source.

    Example: special_chars = ['.', ',', '-']

    In other words, it checks whether a text is, potentially, the name of a funding source.
    """
    for char in text:
        if not (char.isalpha() or char.isspace() or char in special_chars):
            return False
    return True


def _looks_like_award_id(text):
    # TODO outros casos podem ser considerados, além do DOI
    invalid_patterns = ['doi.org', ]
    for pattern in invalid_patterns:
        if pattern in text:
            return False
    return True


def _get_first_number_sequence(text, special_chars):
    number = ""

    # encontra o primeiro caracter numérico em text
    for i, item in enumerate(text):
        if item.isdigit():
            text = text[i:]
            break
    # pega primeira sequência de caracteres numéricos ou permitidos na lista
    for i, item in enumerate(text):
        if item.isdigit() or item in special_chars:
            number += item
        else:
            break

    return number or None


def has_digit(text):
    for n in range(10):
        if str(n) in text:
            return True
    return False


class FundingGroup:
    """
    Class that performs the extraction of values for funding-source and award-id.
    To return both attributes, award_groups is used.
    To return only institutions, use funding_sources.

    Parameters
    ----------
    xml
        XML file that contains the attributes of interest.
    params : dict
        Dictionary containing special characters configuration:
        - special_chars_funding: List of special characters allowed in funding source names
        - special_chars_award_id: List of special characters allowed in award IDs

    Returns
    -------
    list
        Arrangement containing a dictionary that correlates funding-source and award-id or values of one of the attributes.
    """

    def __init__(self, xmltree, params=None):
        self._xmltree = xmltree
        self.params = params or {
            "special_chars_funding": ['.', ','],
            "special_chars_award_id": ['/', '.', '-']
        }

    def _process_paragraph_node(self, node):
        """
        Process a single paragraph node to extract funding sources and award IDs.
        
        Parameters
        ----------
        node : lxml.etree.Element
            The paragraph node to process
        Returns
        -------
        dict
            Dictionary containing fn-type, extracted funding sources, award IDs and original text
        """
        text = xml_utils.node_plain_text(node)
        funding_sources = []
        award_ids = []
        
        if has_digit(text):
            number = _get_first_number_sequence(
                text, 
                self.params['special_chars_award_id']
            )
            if _looks_like_award_id(text) and number is not None:
                award_ids.append(number)
        
        return {
            "look-like-award-id": award_ids,
            "text": text
        }
        
    def fn_financial_information(self):
        items = []
        for fn_type in ('financial-disclosure', 'supported-by'):
            for nodes in self._xmltree.xpath(f".//fn-group/fn[@fn-type='{fn_type}']"):
                for node in nodes.xpath('p'):
                    node_data = self._process_paragraph_node(node)
                    node_data['fn-type'] = fn_type
                    items.append(node_data)
        return items

    @property
    def award_groups(self):
        items = []
        for node in self._xmltree.xpath(".//funding-group/award-group"):
            d = {
                "funding-source": [xml_utils.get_node_without_subtag(source) for source in
                                   node.xpath("funding-source")],
                "award-id": [xml_utils.get_node_without_subtag(id) for id in node.xpath("award-id")]
            }
            items.append(d)
        return items

    @property
    def funding_sources(self):
        items = []
        for node in self._xmltree.xpath(".//funding-group/award-group/funding-source"):
            items.append(xml_utils.get_node_without_subtag(node))
        return items

    @property
    def funding_statement(self):
        """
        De acordo com https://scielo.readthedocs.io/projects/scielo-publishing-schema/pt-br/latest/tagset/elemento-funding-statement.html?highlight=funding-statement
        <funding-statement> ocorre zero ou uma vez.
        """
        return self._xmltree.findtext(".//funding-group/funding-statement")

    @property
    def principal_award_recipients(self):
        items = []
        for node in self._xmltree.xpath(".//funding-group/award-group/principal-award-recipient"):
            items.append(xml_utils.get_node_without_subtag(node))
        return items

    @property
    def principal_investigators(self):
        items = []
        for node in self._xmltree.xpath(".//funding-group/award-group/principal-investigator/string-name"):
            d = {
                "given-names": node.findtext("given-names"),
                "surname": node.findtext("surname")
            }
            items.append(d)
        return items

    @property
    def ack(self):
        items = []
        for ack in self._xmltree.xpath(".//back//ack"):
            item = {
                "title": ack.findtext("title"),
                "p": []
            }
            for node in nodes.xpath('p'):
                node_data = self._process_paragraph_node(node)
                item["p"].append(node_data)
            items.append(item)
        return items

    @property
    def article_type(self):
        return self._xmltree.xpath(".")[0].get("article-type")

    @property
    def article_lang(self):
        return self._xmltree.xpath(".")[0].get("{http://www.w3.org/XML/1998/namespace}lang")

    def extract_funding_data(self):
        """
        Extracts various financial and funding-related information from the XML for validation purposes.

        This function processes the XML to retrieve information about the article type, language,
        and financial details, which are essential for validating the completeness and correctness
        of funding information in scientific articles.

        Parameters
        ----------
        funding_special_chars : list, optional
            List of special characters considered valid in the names of funding sources.
        award_id_special_chars : list, optional
            List of special characters considered valid in award IDs.

        Returns
        -------
        dict
            A dictionary containing various pieces of extracted information for validation purposes,
            such as article type, language, financial information, award groups, funding sources,
            funding statement, principal award recipients, and acknowledgments. This data is used
            to ensure that the article's funding information meets required standards and includes
            all necessary details.
        """
        return {
            # Type of the article, obtained from the "article-type" attribute in the XML root element.
            "article_type": self.article_type,
            # Language of the article, obtained from the "lang" attribute in the XML namespace.
            "article_lang": self.article_lang,
            # Possible financial information extracted from the financial footnote group.
            "fn_financial_information": self.fn_financial_information(),
            # Award groups, containing funding sources and award IDs.
            "award_groups": self.award_groups,
            # Funding sources listed in "award-groups".
            "funding_sources": self.funding_sources,
            # Funding information obtained in "funding-statement".
            "funding_statement": self.funding_statement,
            # Principal award recipients obtained in "principal-award-recipient".
            "principal_award_recipients": self.principal_award_recipients,
            # Funding information obtained in "ack".
            "ack": self.ack
        }

    @property
    def data(self):
        if self.award_groups:
            _data = []
            for item in self.award_groups:
                award_id = item.get("award-id")
                funding_source = item.get("funding-source")
                if award_id and funding_source:
                    for aid in award_id:
                        _data.append(
                            {
                                "award-id": aid,
                                "funding-source": funding_source
                            }
                        )
            return _data