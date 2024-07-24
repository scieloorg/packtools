from packtools.sps.utils import xml_utils


def get_node_without_subtag(node):
    """
        Função que retorna nó sem subtags. 
    """
    return "".join(node.xpath(".//text()"))


class Table:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    
    def extract_table(self, subtag):
        table_node = self.xmltree.xpath('.//table-wrap-group') or self.xmltree.xpath('.//table-wrap')
        extract_node_text = xml_utils.node_text_without_xref if subtag else get_node_without_subtag
        
        if table_node:
            if self.xmltree.xpath('.//table-wrap-group'):
                return self._extract_table_with_table_wrap_group(node=table_node, extract_node_text=extract_node_text)
            else:
                return self._extract_table_without_table_wrap_group(node=table_node, extract_node_text=extract_node_text)
        else:
            return 'No tables found.'


    def _extract_table_with_table_wrap_group(self, node, extract_node_text):
        tables = []

        for table_node in node:
            table_group_id = table_node.get('id', '')
            table_group = {'table_group_id': table_group_id}
            data = self._extract_table_without_table_wrap_group(node=table_node.xpath('.//table-wrap'), extract_node_text=extract_node_text)
            table_group.update(data)
            tables.append(table_group)
        return tables


    def _extract_table_without_table_wrap_group(self, node, extract_node_text):
        tables = {'tables': []}
        data_tables = ['label', 'title']

        for table_node in node:
            table_id = table_node.get('id', '')
            data = {'id': table_id}
            
            for field in data_tables:
                try:
                    data[field]  = extract_node_text(table_node.xpath(f'.//{field}')[0])
                except IndexError:
                    data[field] = ''
            
            try:
                data['table'] = xml_utils.node_text_without_xref(table_node.xpath('table')[0])
            except IndexError:
                data['table'] = ''
            
            foot = self.extract_table_wrap_foot(node=table_node, extract_node_text=extract_node_text)
            
            data.update(foot)
            tables['tables'].append(data)
        return tables


    def extract_table_wrap_foot(self, node, extract_node_text):
        try:
            foot = extract_node_text(node.xpath('table-wrap-foot')[0])
        except IndexError:
            foot = ''
        foot = {'wrap-foot': foot}
        return foot