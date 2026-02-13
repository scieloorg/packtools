"""
XML Fixer utilities for completing and fixing XML structures.

This module provides utilities to fix and complete XML structures,
particularly for SciELO Publishing Schema (SPS) compliance.
"""

from lxml import etree


def complete_pub_date(xmltree, default_day=15, default_month=6):
    """
    Completa elementos pub-date incompletos com valores padrão para day e month.
    
    Esta função processa elementos <pub-date> no XML e adiciona elementos <day> e <month>
    quando estes estão ausentes, mantendo a ordem correta dos elementos (year, month, day).
    
    Args:
        xmltree: Árvore XML (lxml.etree.Element) a ser processada
        default_day (int, optional): Dia padrão para completar (1-31). Padrão: 15
        default_month (int, optional): Mês padrão para completar (1-12). Padrão: 6
    
    Returns:
        list: Lista de dicionários contendo as mudanças realizadas. Cada dicionário tem:
            - xpath (str): XPath do elemento pub-date modificado
            - element_added (str): Nome do elemento adicionado ('day' ou 'month')
            - value (str): Valor adicionado
    
    Raises:
        ValueError: Se default_day não está entre 1-31 ou default_month não está entre 1-12
    
    Examples:
        >>> from lxml import etree
        >>> xml = '''<article>
        ...   <front>
        ...     <article-meta>
        ...       <pub-date pub-type="pub">
        ...         <year>2024</year>
        ...       </pub-date>
        ...     </article-meta>
        ...   </front>
        ... </article>'''
        >>> tree = etree.fromstring(xml)
        >>> changes = complete_pub_date(tree)
        >>> len(changes)
        2
        >>> changes[0]['element_added']
        'month'
        >>> changes[1]['element_added']
        'day'
        
        >>> # Após a execução, o XML terá:
        >>> pub_date = tree.find('.//pub-date')
        >>> pub_date.findtext('month')
        '6'
        >>> pub_date.findtext('day')
        '15'
        
        >>> # Com valores personalizados:
        >>> tree = etree.fromstring(xml)
        >>> changes = complete_pub_date(tree, default_day=1, default_month=1)
        >>> pub_date = tree.find('.//pub-date')
        >>> pub_date.findtext('month')
        '1'
        >>> pub_date.findtext('day')
        '1'
        
        >>> # Não modifica elementos já existentes:
        >>> xml_complete = '''<article>
        ...   <front>
        ...     <article-meta>
        ...       <pub-date pub-type="pub">
        ...         <year>2024</year>
        ...         <month>3</month>
        ...         <day>20</day>
        ...       </pub-date>
        ...     </article-meta>
        ...   </front>
        ... </article>'''
        >>> tree = etree.fromstring(xml_complete)
        >>> changes = complete_pub_date(tree)
        >>> len(changes)
        0
    """
    # Validar parâmetros
    if not isinstance(default_day, int) or default_day < 1 or default_day > 31:
        raise ValueError("default_day must be between 1 and 31")
    
    if not isinstance(default_month, int) or default_month < 1 or default_month > 12:
        raise ValueError("default_month must be between 1 and 12")
    
    changes = []
    
    # Buscar elementos pub-date com pub-type='pub' ou publication-format='electronic'
    xpath_query = (
        ".//pub-date[@pub-type='pub'] | "
        ".//pub-date[@publication-format='electronic']"
    )
    
    pub_date_nodes = xmltree.xpath(xpath_query)
    
    for pub_date_node in pub_date_nodes:
        # Obter xpath do elemento para reportar
        tree = pub_date_node.getroottree()
        xpath = tree.getpath(pub_date_node)
        
        # Verificar se year existe (necessário para processar)
        year_elem = pub_date_node.find('year')
        if year_elem is None:
            continue
        
        # Verificar e adicionar month se ausente
        month_elem = pub_date_node.find('month')
        if month_elem is None:
            month_elem = etree.Element('month')
            month_elem.text = str(default_month)
            
            # Inserir após year
            year_index = list(pub_date_node).index(year_elem)
            pub_date_node.insert(year_index + 1, month_elem)
            
            changes.append({
                'xpath': xpath,
                'element_added': 'month',
                'value': str(default_month)
            })
        
        # Verificar e adicionar day se ausente
        day_elem = pub_date_node.find('day')
        if day_elem is None:
            day_elem = etree.Element('day')
            day_elem.text = str(default_day)
            
            # Inserir após month
            month_elem = pub_date_node.find('month')  # Atualizar referência
            month_index = list(pub_date_node).index(month_elem)
            pub_date_node.insert(month_index + 1, day_elem)
            
            changes.append({
                'xpath': xpath,
                'element_added': 'day',
                'value': str(default_day)
            })
    
    return changes
