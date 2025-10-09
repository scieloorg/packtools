from lxml import etree


def _find_inline_graphics_in_caption_or_label(xmltree):
    """
    Encontra todos os elementos inline-graphic dentro de label ou caption.
    """
    return xmltree.xpath(".//label//inline-graphic | .//caption//inline-graphic")


def _get_parent_container(inline_graphic):
    """
    Encontra o container pai que pode conter um elemento graphic.
    """
    containers = inline_graphic.xpath(
        "ancestor::fig | ancestor::table-wrap | ancestor::boxed-text | "
        "ancestor::supplementary-material | ancestor::disp-formula"
    )
    return containers[0] if containers else None


def _group_inline_graphics_by_container(inline_graphics):
    """
    Agrupa elementos inline-graphic por seu container pai.
    """
    containers_map = {}

    for inline_graphic in inline_graphics:
        parent_container = _get_parent_container(inline_graphic)

        if parent_container is None:
            continue

        if parent_container not in containers_map:
            containers_map[parent_container] = []
        containers_map[parent_container].append(inline_graphic)

    return containers_map


def _has_existing_graphic(container):
    """
    Verifica se o container já possui um elemento graphic.
    """
    return container.find("graphic") is not None


def _create_graphic_from_inline(inline_graphic):
    """
    Cria um elemento graphic a partir de um inline-graphic, preservando atributos.
    """
    graphic = etree.Element(
        "graphic",
        attrib=inline_graphic.attrib,
        nsmap=inline_graphic.nsmap
    )

    # Preserva o texto e cauda
    graphic.text = inline_graphic.text
    graphic.tail = inline_graphic.tail

    # Copia subelementos
    for child in inline_graphic:
        graphic.append(child)

    return graphic


def _get_insert_position(container):
    """
    Determina a posição onde o graphic deve ser inserido no container.
    O graphic deve ser inserido após label e caption.
    """
    insert_position = 0
    for i, child in enumerate(container):
        if child.tag in ("label", "caption"):
            insert_position = i + 1
    return insert_position


def _get_element_xpath(xmltree, element):
    """
    Obtém o XPath de um elemento na árvore.
    """
    try:
        return xmltree.getroottree().getpath(element)
    except:
        return f".//{element.tag}"


def _create_modification_record(xmltree, inline_graphic, old_parent, new_parent):
    """
    Cria um registro de modificação.
    """
    return {
        "xpath": _get_element_xpath(xmltree, inline_graphic),
        "action": "moved_and_renamed",
        "old_parent": old_parent.tag if old_parent is not None else "unknown",
        "new_parent": new_parent.tag
    }


def _process_single_inline_graphic(xmltree, inline_graphic, container):
    """
    Processa um único inline-graphic, movendo e renomeando-o para graphic.
    """
    # Verifica se já existe graphic
    if _has_existing_graphic(container):
        return None

    # Guarda informações antes da modificação
    old_parent = inline_graphic.getparent()

    # Cria registro de modificação antes de remover
    modification = _create_modification_record(xmltree, inline_graphic, old_parent, container)

    # Remove inline-graphic da posição atual
    old_parent.remove(inline_graphic)

    # Cria novo elemento graphic
    graphic = _create_graphic_from_inline(inline_graphic)

    # Insere graphic na posição adequada
    insert_position = _get_insert_position(container)
    container.insert(insert_position, graphic)

    return modification


def fix_inline_graphic_in_caption(xmltree):
    """
    Corrige elementos inline-graphic incorretamente posicionados dentro de caption/label.

    Esta função identifica elementos <inline-graphic> que estejam dentro de <label>
    ou <caption> e, quando não existe um elemento <graphic> no elemento pai
    (fig, table-wrap, boxed-text, etc) E há apenas um inline-graphic no container,
    move o inline-graphic para fora do label/caption e o renomeia para <graphic>.

    Se houver múltiplos inline-graphics no mesmo container, nenhuma modificação
    é realizada para evitar ambiguidade.
    """
    modifications = []

    # Encontra todos os inline-graphics em label/caption
    inline_graphics = _find_inline_graphics_in_caption_or_label(xmltree)

    # Agrupa por container pai
    containers_map = _group_inline_graphics_by_container(inline_graphics)

    # Processa apenas containers com exatamente 1 inline-graphic
    for container, inline_graphics_list in containers_map.items():
        # Se houver mais de um inline-graphic, não faz nada
        if len(inline_graphics_list) > 1:
            continue

        inline_graphic = inline_graphics_list[0]

        # Processa o inline-graphic
        modification = _process_single_inline_graphic(xmltree, inline_graphic, container)

        if modification:
            modifications.append(modification)

    return modifications
