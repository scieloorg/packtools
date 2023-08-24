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
        items = []
        for node in self._xmltree.xpath(".//fn-group/fn[@fn-type='financial-disclosure']/p"):
            link = node.xpath(".//ext-link[@ext-link-type='uri']")
            if link:
                items.append(link[0].get("{http://www.w3.org/1999/xlink}href"))
            else:
                items.append(node.text)
        return items

    @property
    def award_groups(self):
        items = []
        for node in self._xmltree.xpath(".//funding-group/award-group"):
            funding_sources = node.xpath("funding-source")
            award_ids = node.xpath("award-id")
            d = {}
            d["funding-source"] = [item.text for item in funding_sources]
            d["award-id"] = [item.text for item in award_ids]
            items.append(d)
        return items

    @property
    def funding_sources(self):
        items = []
        for node in self._xmltree.xpath(".//funding-group/award-group/funding-source"):
            items.append(node.text)
        return items
