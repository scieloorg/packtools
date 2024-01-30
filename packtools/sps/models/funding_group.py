import logging
from lxml import etree

logger = logging.getLogger(__name__)


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
        return self._xmltree.xpath(".//funding-group/funding-statement")[0].text

    @property
    def principal_award_recipients(self):
        items = []
        for node in self._xmltree.xpath(".//funding-group/award-group/principal-award-recipient"):
            items.append(node.text)
        return items

