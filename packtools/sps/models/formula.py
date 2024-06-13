from packtools.sps.utils import xml_utils

class Formula:
    def __init__(self, xmltree):
        self.xmltree = xmltree


    @property
    def disp_formula_nodes(self):
        return self.xmltree.xpath('.//disp-formula')


    def get_equation(self, node):
        mnl_namespace = {'mnl': "http://www.w3.org/1998/Math/MathML"}
        math_node_xpath = 'mnl:math'
        tex_math_xpath = 'tex-math'
        graphic_xpath = 'graphic'

        if node.xpath(math_node_xpath, namespaces=mnl_namespace) or node.xpath(tex_math_xpath):
            eq_node = node.xpath(math_node_xpath, namespaces=mnl_namespace) or node.xpath(tex_math_xpath)
            eq_node_id = eq_node[0].get('id', '')          
            eq = xml_utils.node_text_without_xref(eq_node[0])
            eq_dict = {'id': eq_node_id, 'equation': eq}
            return eq_dict
        elif node.xpath(graphic_xpath):
            eq_node = node.xpath(graphic_xpath)[0]
            eq_node_id = eq_node.get('id', '')
            eq_graphic = eq_node.get('{http://www.w3.org/1999/xlink}href')
            eq_dict = {'id': eq_node_id, 'graphic': eq_graphic}
            return eq_dict
        return 'Not found formulas'


    @property
    def extract_disp_formula(self):
        node = self.disp_formula_nodes
        formulas = {'formulas': []}
        for disp_node in node:
            disp_node_id = disp_node.get('id', '')
            
            try:
                disp_node_label = disp_node.xpath('label')[0].text  
            except IndexError:
                disp_node_label = ''
            equation = self.get_equation(node=disp_node)
            
            formula = {
                'disp_formula_id': disp_node_id,
                'disp_formula_label': disp_node_label,
                'equations': equation
            }
            formulas['formulas'].append(formula)
        return formulas