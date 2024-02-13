import logging

from packtools.sps.utils import xml_utils

logger = logging.getLogger(__name__)


def _is_funding_source(text):
    return all(char.isalpha() or char.isspace() for char in text)


def _strip_and_remove_final_dot(text):
    text = text.strip()
    if text.endswith('.'):
        text = text[:-1]
    return text


def _is_award_id(text):
    # TODO outros casos podem ser considerados, além do DOI
    invalid_patterns = ['doi.org', ]
    return not any(pattern in text for pattern in invalid_patterns)


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

    @property
    def financial_disclosure(self):
        # TODO separar os valores entre 'funding-source' e 'award-id'
        for node in self._xmltree.xpath(".//fn-group/fn[@fn-type='financial-disclosure']"):
            yield " ".join([item.strip() for item in node.xpath(".//text()") if item.strip()])

    @property
    def award_groups(self):
        items = []
        for node in self._xmltree.xpath(".//funding-group/award-group"):
            d = {
                "funding-source": [source.text for source in node.xpath("funding-source")],
                "award-id": [id.text for id in node.xpath("award-id")]
            }
            items.append(d)
        return items

    @property
    def funding_sources(self):
        items = []
        for node in self._xmltree.xpath(".//funding-group/award-group/funding-source"):
            items.append(node.text)
        return items

    @property
    def funding_statement(self):
        funding_statements = self._xmltree.xpath(".//funding-group/funding-statement")
        if funding_statements:
            return funding_statements[0].text

    @property
    def principal_award_recipients(self):
        items = []
        for node in self._xmltree.xpath(".//funding-group/award-group/principal-award-recipient"):
            items.append(node.text)
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
                "text": " ".join([paragraph.text for paragraph in node.xpath("p")])
                }
            )
        return items
