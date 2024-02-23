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
    return all(char.isalpha() or char.isspace() or char in special_chars for char in text)


def _looks_like_award_id(text):
    # TODO outros casos podem ser considerados, além do DOI
    invalid_patterns = ['doi.org', ]
    return not any(pattern in text for pattern in invalid_patterns)


def _get_first_number_sequence(text, special_chars):
    number = ""
    i = 0
    while i < len(text) and not text[i].isdigit():
        i += 1
    while i < len(text) and (text[i].isdigit() or text[i] in special_chars):
        number += text[i]
        i += 1
    return number or None


class FundingGroup:
    """
    Class that performs the extraction of values for funding-source and award-id.
    To return both attributes, award_groups is used.
    To return only institutions, use funding_sources.

    Parameters
    ----------
    xml
        XML file that contains the attributes of interest.

    Returns
    -------
    list
        Arrangement containing a dictionary that correlates funding-source and award-id or values of one of the attributes.
    """

    def __init__(self, xmltree):
        self._xmltree = xmltree

    def fn_financial_information(self, special_chars_funding=[], special_chars_award_id=[]):
        items = []
        for fn_type in ('financial-disclosure', 'supported-by'):
            funding_sources = []
            award_ids = []
            for nodes in self._xmltree.xpath(f".//fn-group/fn[@fn-type='{fn_type}']"):
                for node in nodes.xpath('p'):
                    text = xml_utils.node_plain_text(node)
                    if _is_funding_source(text, special_chars_funding):
                        funding_sources.append(text)
                    if _is_award_id(text):
                        if number := _get_first_number_sequence(text, special_chars_award_id):
                            award_ids.append(number)

                items.append(
                    {
                        "fn-type": fn_type,
                        "look-like-funding-source": funding_sources,
                        "look-like-award-id": award_ids
                    }
                )
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
        for node in self._xmltree.xpath(".//back//ack"):
            items.append(
                {
                    "title": node.findtext("title"),
                    "text": " ".join([xml_utils.get_node_without_subtag(paragraph) for paragraph in node.xpath("p")])
                }
            )
        return items
