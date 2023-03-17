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
        
        #Define se a extração vai ocorrer com subtags ou sem.
        aff_text = xml_utils.node_text_without_xref if subtag else get_node_without_subtag
        
        for node in nodes:
            for aff_node in node.xpath('aff'):
                
                affiliation_id = aff_node.get('id')
                
                try:
                    label = aff_node.xpath('label')[0].text
                except IndexError:
                    label = ''
                
                try:
                    orgname = aff_text(aff_node.xpath('institution[@content-type="orgname"]')[0])
                except IndexError:
                    orgname = ''

                try:
                    orgdiv1 = aff_text(aff_node.xpath('institution[@content-type="orgdiv1"]')[0])
                except IndexError:
                    orgdiv1 = ''

                try:
                    orgdiv2 = aff_text(aff_node.xpath('institution[@content-type="orgdiv2"]')[0])
                except IndexError:
                    orgdiv2 = ''
                
                try:
                    original = aff_text(aff_node.xpath('institution[@content-type="original"]')[0])
                except IndexError:
                    original = ''
                
                country_code = aff_node.xpath('country')[0].get('country') if aff_node.xpath('country')[0].get('country') else ''

                try:
                    country = aff_text(aff_node.xpath('country')[0])
                except IndexError:
                    country = ''

                addr_state = aff_text(aff_node.xpath('addr-line/named-content[@content-type="state"]')[0])
                addr_city = aff_text(aff_node.xpath('addr-line/named-content[@content-type="city"]')[0])
                
                city = addr_city if addr_city else ''
                state = addr_state if addr_state else ''
                
                try:
                    email = aff_node.xpath('email')[0].text
                except IndexError:
                    email = ''

                data.append({
                    'id': affiliation_id, 
                    'label': label,
                    'institution': [
                        {
                            'orgname': orgname,
                            'orgdiv1': orgdiv1,
                            'orgdiv2': orgdiv2,
                            'original': original,
                        }
                    ],
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
    
            
    def extract_all_affiliation_data(self, subtag):
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