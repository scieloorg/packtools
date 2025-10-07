"""
Módulo para funções de correção de XML.

Este módulo contém funções utilitárias para corrigir problemas
comuns em documentos XML, especialmente para conformidade com SPS.
"""
import logging
from typing import List, Dict

from lxml import etree

logger = logging.getLogger(__name__)


def fix_inline_graphic_in_caption_and_label(xmltree: etree._Element) -> List[Dict[str, str]]:
    """
    Corrige elementos inline-graphic incorretamente posicionados dentro de caption ou label.
    
    Esta função identifica todos os elementos `inline-graphic` que estejam dentro de
    `label` ou `caption` e, quando não existir um elemento `graphic` no pai (fig,
    table-wrap, boxed-text, etc), move o `inline-graphic` para fora do `label`/`caption`
    e o renomeia para `graphic`.
    
    Args:
        xmltree: Objeto lxml.etree representando o documento XML a ser corrigido.
        
    Returns:
        list: Lista de dicionários documentando cada modificação realizada. Cada
              dicionário contém os campos:
              - xpath: caminho XPath do elemento modificado
              - action: tipo de ação realizada
              - old_parent: tag do elemento pai original
              - new_parent: tag do novo elemento pai
              
    Examples:
        >>> from lxml import etree
        >>> xml = '''<fig id="f1">
        ...   <label>Figura 1</label>
        ...   <caption><title>Título<inline-graphic xlink:href="img.jpg"/></title></caption>
        ... </fig>'''
        >>> tree = etree.fromstring(xml)
        >>> changes = fix_inline_graphic_in_caption_and_label(tree)
        >>> len(changes)
        1
        >>> changes[0]['action']
        'moved_and_renamed'
    """
    changes = []
    
    # Encontra todos os inline-graphic dentro de caption ou label
    # XPath para encontrar inline-graphic em qualquer descendente de caption ou label
    inline_graphics_in_caption_or_label = xmltree.xpath(
        ".//caption//inline-graphic | .//label//inline-graphic"
    )
    
    for inline_graphic in inline_graphics_in_caption_or_label:
        # Obtém o elemento pai do inline-graphic para documentação
        old_parent = inline_graphic.getparent()
        old_parent_tag = old_parent.tag if old_parent is not None else None
        
        # Navega até encontrar o elemento container (fig, table-wrap, boxed-text, etc)
        # que é o pai do caption/label
        container = old_parent
        while container is not None:
            parent = container.getparent()
            if parent is not None:
                # Verifica se o pai contém caption ou label
                has_caption_or_label = (
                    parent.find(".//caption") is not None or 
                    parent.find(".//label") is not None
                )
                if has_caption_or_label:
                    # Este é provavelmente o container (fig, table-wrap, etc)
                    container = parent
                    break
            container = parent
        
        # Se não encontrou um container adequado, tenta encontrar o pai direto de caption/label
        if container is None or container.tag in ('caption', 'label', 'title', 'p'):
            # Procura pelo ancestral que contém caption ou label
            current = inline_graphic
            while current is not None:
                parent = current.getparent()
                if parent is None:
                    break
                # Verifica se este elemento é um possível container
                if parent.tag in ('fig', 'table-wrap', 'boxed-text', 'disp-formula', 
                                  'supplementary-material', 'fig-group', 'article', 
                                  'sub-article', 'body', 'sec', 'app'):
                    container = parent
                    break
                current = parent
        
        # Se ainda não encontrou container, usa o elemento raiz
        if container is None:
            container = xmltree
            
        # Verifica se já existe um elemento graphic no container
        existing_graphic = container.find(".//graphic")
        
        if existing_graphic is None:
            # Não existe graphic, então vamos mover e renomear o inline-graphic
            
            # Captura o XPath antes de modificar (para documentação)
            try:
                xpath = xmltree.getpath(inline_graphic)
            except AttributeError:
                # Fallback se getpath não estiver disponível
                xpath = f".//{inline_graphic.tag}"
            
            # Remove o inline-graphic de sua posição atual
            old_parent.remove(inline_graphic)
            
            # Cria um novo elemento graphic com os mesmos atributos
            graphic = etree.Element("graphic", attrib=inline_graphic.attrib)
            
            # Copia o texto e tail se existirem
            graphic.text = inline_graphic.text
            graphic.tail = inline_graphic.tail
            
            # Copia todos os sub-elementos, se houver
            for child in inline_graphic:
                graphic.append(child)
            
            # Adiciona o novo elemento graphic ao container
            # Tenta adicionar após caption/label, se existirem
            caption = container.find(".//caption")
            label = container.find(".//label")
            
            inserted = False
            if caption is not None:
                # Adiciona após o caption
                caption_index = list(container).index(caption)
                container.insert(caption_index + 1, graphic)
                inserted = True
            elif label is not None:
                # Adiciona após o label
                label_index = list(container).index(label)
                container.insert(label_index + 1, graphic)
                inserted = True
            
            if not inserted:
                # Adiciona como último filho
                container.append(graphic)
            
            # Registra a mudança
            change = {
                "xpath": xpath,
                "action": "moved_and_renamed",
                "old_parent": old_parent_tag,
                "new_parent": container.tag,
            }
            changes.append(change)
            
            logger.info(
                f"Moved and renamed inline-graphic to graphic: {xpath} "
                f"from {old_parent_tag} to {container.tag}"
            )
    
    return changes
