import re
from packtools.sps.utils import xml_utils


def get_node_without_subtag(node):
    """
        Função que retorna nó sem subtags. 
    """
    return "".join(node.xpath(".//text()"))


class AffiliationExtractor:
    def __init__(self, xmltree):
        self._xmltree = xmltree

    @property
    def extract_article_meta(self):
        return self._xmltree.xpath(".//article-meta")

    @property
    def extract_front_stub(self):
        return self._xmltree.xpath(".//front-stub")

    @property
    def extract_contrib_group(self):
        return self._xmltree.xpath(".//contrib-group")

    def extract_affiliation_data(self, nodes, subtag):
        data = []
        address_aff = ['state', 'city']
        institution_aff = ["orgname", "orgdiv1", "orgdiv2", "original"]

        # Define se a extração vai ocorrer com subtags ou sem.
        aff_text = xml_utils.node_text_without_xref if subtag else get_node_without_subtag

        for node in nodes:
            for aff_node in node.xpath('aff'):

                affiliation_id = aff_node.get('id')

                try:
                    label = aff_node.xpath('label')[0].text
                except IndexError:
                    label = None

                institution = {}
                for inst in institution_aff:
                    try:
                        institution[inst] = aff_text(aff_node.xpath(f'institution[@content-type="{inst}"]')[0])
                    except IndexError:
                        institution[inst] = ''

                address = {}
                for field in address_aff:
                    try:
                        address[field] = aff_text(
                            aff_node.xpath(f'addr-line/named-content[@content-type="{field}"]')[0])
                    except IndexError:
                        pass

                city = address['city']
                state = address['state']

                try:
                    country_node = aff_node.xpath('country')[0]
                    country = aff_text(country_node)
                    country_code = country_node.get('country', '')
                except IndexError:
                    country = ''
                    country_code = ''

                try:
                    email = aff_node.xpath('email')[0].text
                except IndexError:
                    email = ''

                data.append({
                    'id': affiliation_id,
                    'label': label,
                    'institution': [institution],
                    'city': city,
                    'state': state,
                    'country': [
                        {
                            'code': country_code,
                            'name': country,
                        }
                    ],
                    'email': email,
                })

        return data

    def get_affiliation_dict(self, subtag):
        data = {}
        for item in self.get_affiliation_data_from_multiple_tags(subtag):
            data[item['id']] = item
        return data

    def get_affiliation_data_from_multiple_tags(self, subtag):
        list_nodes = []

        article_meta_node = self.extract_article_meta
        front_stub_node = self.extract_front_stub
        contrib_group_node = self.extract_contrib_group

        try:
            if article_meta_node[0].xpath('aff'):
                list_nodes.append(article_meta_node[0])
        except IndexError:
            pass

        try:
            if front_stub_node[0].xpath('aff'):
                list_nodes.append(front_stub_node[0])
        except IndexError:
            pass

        try:
            if contrib_group_node[0].xpath('aff'):
                list_nodes.append(contrib_group_node[0])
        except IndexError:
            pass

        data = self.extract_affiliation_data(nodes=list_nodes, subtag=subtag)

        return data
