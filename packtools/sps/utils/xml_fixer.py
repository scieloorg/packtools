from lxml import etree


def fix_inline_graphic_in_caption(xmltree):
    """
    Corrige elementos inline-graphic incorretamente posicionados dentro de caption/label.

    Esta função busca primeiro os containers (fig, table-wrap, disp-formula) que:
    - Contêm inline-graphic dentro de label ou caption
    - NÃO possuem elemento graphic

    Para cada container encontrado, se houver exatamente um inline-graphic,
    remove-o de dentro do label/caption e cria um elemento graphic no nível do container.

    Args:
        xmltree: Árvore XML a ser processada

    Returns:
        list: Lista de dicionários com as modificações realizadas
    """
    if xmltree is None:
        raise ValueError("xmltree não pode ser None")

    modifications = []

    # XPath que busca containers válidos que precisam correção:
    # - São fig, table-wrap ou disp-formula
    # - Têm inline-graphic dentro de label ou caption
    # - NÃO têm elemento graphic filho direto
    xpath_containers = """
        (//fig | //table-wrap | //disp-formula)
        [(label//inline-graphic or caption//inline-graphic) and not(graphic)]
    """

    containers = xmltree.xpath(xpath_containers)

    for container in containers:
        # Busca todos os inline-graphics dentro de label ou caption deste container
        inline_graphics = container.xpath(
            ".//label//inline-graphic | .//caption//inline-graphic"
        )

        # Processa apenas se houver exatamente 1 inline-graphic
        if len(inline_graphics) != 1:
            continue

        inline_graphic = inline_graphics[0]

        try:
            # Guarda informações antes da modificação
            old_parent = inline_graphic.getparent()

            # Gera XPath para registro de modificação
            try:
                xpath = xmltree.getroottree().getpath(inline_graphic)
            except (AttributeError, ValueError):
                xpath = f".//{inline_graphic.tag}"

            # Remove inline-graphic da posição atual
            old_parent.remove(inline_graphic)

            # Cria novo elemento graphic preservando atributos e conteúdo
            graphic = etree.Element(
                "graphic",
                attrib=inline_graphic.attrib,
                nsmap=inline_graphic.nsmap
            )
            graphic.text = inline_graphic.text
            graphic.tail = inline_graphic.tail

            # Copia todos os subelementos
            for child in inline_graphic:
                graphic.append(child)

            # Determina posição de inserção (após label e caption)
            insert_position = 0
            for i, child in enumerate(container):
                if child.tag in ("label", "caption"):
                    insert_position = i + 1

            # Insere graphic na posição adequada
            container.insert(insert_position, graphic)

            # Registra modificação realizada
            modifications.append({
                "xpath": xpath,
                "action": "moved_and_renamed",
                "old_parent": old_parent.tag if old_parent is not None else "unknown",
                "new_parent": container.tag
            })

        except Exception as e:
            print(f"Erro ao processar inline-graphic no container {container.tag}: {e}")
            continue

    return modifications
