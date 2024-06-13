from packtools.sps.utils import xml_utils


def get_node_without_subtag(node):
    """
        Função que retorna nó sem subtags. 
    """
    return "".join(node.xpath(".//text()"))


class Figure:
    def __init__(self, xmltree):
        self.xmltree = xmltree


    def extract_figures(self, subtag):
        fig_node = self.xmltree.xpath('.//fig-group') or self.xmltree.xpath('.//fig')
        extract_node_text = xml_utils.node_text_without_xref if subtag else get_node_without_subtag

        if fig_node:
            if self.xmltree.xpath('.//fig-group'):
                return self._extract_figures_with_fig_group(node=fig_node, extract_node_text=extract_node_text)
            else:
                return self._extract_figures_without_fig_group(node=fig_node, extract_node_text=extract_node_text)
        else:
            return 'No figures found.'


    def _extract_figures_with_fig_group(self, node, extract_node_text):
        figures = []
        
        for fig_group_node in node:
            fig_group_id = fig_group_node.get('id', '')
            
            try:
                fig_group_title = extract_node_text(fig_group_node.xpath('.//title')[0])
            except IndexError:
                fig_group_title = ''
            
            fig_group = {'fig_group_id': fig_group_id, 'fig_group_title': fig_group_title}

            data = self._extract_figures_without_fig_group(node=fig_group_node.xpath('fig'), extract_node_text=extract_node_text)
            fig_group.update(data)
            
            figures.append(fig_group)
        return figures


    def _extract_figures_without_fig_group(self, node, extract_node_text):
        figures = {'figs': []}
        data_fig = ['label', 'title']

        for fig in node:
            fig_id = fig.get('id', '')
            data = {'id': fig_id}

            for field in data_fig:
                try:
                    data[field] = extract_node_text(fig.xpath(f'.//{field}')[0])
                except IndexError:
                    data[field] = ''
        
            try:
                fig_graphic = fig.xpath('graphic')[0].get('{http://www.w3.org/1999/xlink}href')
            except IndexError:
                fig_graphic = ''

            data['graphic'] = fig_graphic
            figures['figs'].append(data)
        return figures
               
        