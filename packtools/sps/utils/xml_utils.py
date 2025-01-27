import logging
import re
import string

from copy import deepcopy
from lxml import etree
from packtools.sps import exceptions
from packtools.lib import file_utils

logger = logging.getLogger(__name__)


def remove_namespaces(xml_string):
    namespaces_to_remove = [
        'xmlns:xlink="http://www.w3.org/1999/xlink"',
        'xmlns:mml="http://www.w3.org/1998/Math/MathML"',
    ]
    for ns in namespaces_to_remove:
        xml_string = xml_string.replace(ns, "")
    return xml_string


def get_nodes_with_lang(xmltree, lang_xpath, node_xpath=None):
    _items = []
    for node in xmltree.xpath(lang_xpath):
        _item = {"id": node.get("id")}
        if node_xpath:
            _item["node"] = node.find(node_xpath)
        else:
            _item["node"] = node
        _item["lang"] = node.get("{http://www.w3.org/XML/1998/namespace}lang")
        _item["id"] = node.get("id")
        _items.append(_item)
    return _items


from lxml import etree
from copy import deepcopy

def node_plain_text(node):
    """
    Função que retorna texto de nó, sem subtags e com espaços padronizados.

    Para elementos <xref>, verifica o valor de @ref-type:
    - Se @ref-type é 'fn' e o conteúdo não é alfanumérico, remove o elemento.
    - Caso contrário, remove apenas a tag <xref> mantendo o conteúdo interno.

    Ajusta o comportamento de preservação do texto em caso de `tail`.
    """
    if node is None:
        return ""

    node = deepcopy(node)

    # Processa os nós <xref>
    for xref in node.findall(".//xref"):
        if xref.tail:
            _next = xref.getnext()
            if _next is None or _next.tag != "xref":
                e = etree.Element("EMPTYTAGTOKEEPXREFTAIL")
                xref.addnext(e)

    for xref in node.findall(".//xref"):
        ref_type = xref.get("ref-type")
        content = (xref.text or "").strip()

        parent = xref.getparent()

        if ref_type == "fn" and not content.isalpha():
            # Remove o <xref> completamente se @ref-type é 'fn' e o conteúdo não é alfanumérico
            if parent is not None:
                parent.remove(xref)
        else:
            # Remove apenas a tag <xref>, mantendo o conteúdo interno
            etree.strip_tags(xref, "xref")

    # Remove os elementos temporários e ajusta o texto
    etree.strip_tags(node, "EMPTYTAGTOKEEPXREFTAIL")

    # Extrai todo o texto dos nós, removendo subtags
    text_content = "".join(node.xpath(".//text()"))

    # Remove espaços extras
    text_content = ' '.join(text_content.split())

    return text_content



def node_text_without_xref(node, remove_xref=True):
    """
    Retorna text com subtags, exceto `xref`
    """
    if node is None:
        return

    node = deepcopy(node)

    if remove_xref:
        for xref in node.findall(".//xref"):
            if xref.tail:
                _next = xref.getnext()
                if _next is None or _next.tag != "xref":
                    e = etree.Element("EMPTYTAGTOKEEPXREFTAIL")
                    xref.addnext(e)
        for xref in node.findall(".//xref"):
            parent = xref.getparent()
            parent.remove(xref)
        etree.strip_tags(node, "EMPTYTAGTOKEEPXREFTAIL")
    return node_text(node)


def formatted_text(title_node):
    # FIXME substituir `formatted_text` por `node_text_without_xref`
    # por ser mais explícito
    return node_text_without_xref(title_node)


def fix_xml(xml_str):
    return fix_namespace_prefix_w(xml_str)


def fix_namespace_prefix_w(content):
    """
    Convert os textos cujo padrão é `w:st="` em `w-st="`
    """
    pattern = r"\bw:[a-z]{1,}=\""
    found_items = re.findall(pattern, content)
    logger.debug("Found %i namespace prefix w", len(found_items))
    for item in set(found_items):
        new_namespace = item.replace(":", "-")
        logger.debug("%s -> %s" % (item, new_namespace))
        content = content.replace(item, new_namespace)
    return content


def _get_xml_content(xml):
    if isinstance(xml, str):
        try:
            content = file_utils.read_file(xml)
        except (FileNotFoundError, OSError):
            content = xml
        content = fix_xml(content)
        return content.encode("utf-8")
    return xml


def get_xml_tree(content):
    parser = etree.XMLParser(remove_blank_text=True, no_network=True)
    try:
        content = _get_xml_content(content)
        xml_tree = etree.XML(content, parser)
    except etree.XMLSyntaxError as exc:
        raise exceptions.SPSLoadToXMLError(str(exc)) from None
    else:
        return xml_tree


def tostring(node, doctype=None, pretty_print=False, xml_declaration=True):
    return etree.tostring(
        node,
        doctype=doctype,
        xml_declaration=xml_declaration,
        method="xml",
        encoding="utf-8",
        pretty_print=pretty_print,
    ).decode("utf-8")


def node_text(node):
    """
    Retorna todos os node.text, incluindo a subtags
    Para <title>Text <bold>text</bold> Text</title>, retorna
    Text <bold>text</bold> Text
    """
    items = [node.text or ""]
    for child in node.getchildren():
        items.append(etree.tostring(child, encoding="utf-8").decode("utf-8"))
    return "".join(items)


def get_node_without_subtag(node, remove_extra_spaces=False):
    """
    Função que retorna nó sem subtags.
    """
    if node is None:
        return
    if remove_extra_spaces:
        return " ".join(
            [text.strip() for text in node.xpath(".//text()") if text.strip()]
        )
    return "".join(node.xpath(".//text()"))


def get_year_month_day(node):
    """
    Retorna os valores respectivos dos elementos "year", "month", "day".

    Parameters
    ----------
    node : lxml.etree.Element
        Elemento do tipo _date_, que tem os elementos "year", "month", "day".

    Returns
    -------
    tuple of strings
        ("YYYY", "MM", "DD")
    None se node is None

    """
    if node is not None:
        return tuple(
            [(node.findtext(item) or "").zfill(2) for item in ["year", "month", "day"]]
        )


def create_alternatives(node, assets_data):
    """
    ```xml
    <alternatives>
        <graphic
            xlink:href="https://minio.scielo.br/documentstore/1678-2674/
            rQRTPbt6jkrncZTsPdCyXsn/
            6d6b2cfaa2dc5bd1fb84644218506cbfbc4dfb1e.tif"/>
        <graphic
            xlink:href="https://minio.scielo.br/documentstore/1678-2674/
            rQRTPbt6jkrncZTsPdCyXsn/
            b810735a45beb5f829d4eb07e4cf68842f57313f.png"
            specific-use="scielo-web"/>
        <graphic
            xlink:href="https://minio.scielo.br/documentstore/1678-2674/
            rQRTPbt6jkrncZTsPdCyXsn/
            e9d0cd6430c85a125e7490629ce43f227d00ef5e.jpg"
            specific-use="scielo-web"
            content-type="scielo-267x140"/>
    </alternatives>
    ```
    """
    if node is None or not assets_data:
        return
    parent = node.getparent()
    if parent is None:
        return
    if len(assets_data) == 1:
        for extension, uri in assets_data.items():
            node.set("{http://www.w3.org/1999/xlink}href", uri)
            if extension in [".tif", ".tiff"]:
                pass
            elif extension in [".png"]:
                node.set("specific-use", "scielo-web")
            else:
                node.set("specific-use", "scielo-web")
                node.set("content-type", "scielo-267x140")
    else:
        alternative_node = etree.Element("alternatives")
        for extension, uri in assets_data.items():
            _node = etree.Element("graphic")
            _node.set("{http://www.w3.org/1999/xlink}href", uri)
            alternative_node.append(_node)
            if extension in [".tif", ".tiff"]:
                pass
            elif extension in [".png"]:
                _node.set("specific-use", "scielo-web")
            else:
                _node.set("specific-use", "scielo-web")
                _node.set("content-type", "scielo-267x140")
        parent.replace(node, alternative_node)


def parse_value(value):
    value = value.lower()
    if value.isdigit():
        return value.zfill(2)
    if "spe" in value:
        return "spe"
    if "sup" in value:
        return "s"
    return value


def parse_issue(issue):
    issue = " ".join([item for item in issue.split()])
    parts = issue.split()
    parts = [parse_value(item) for item in parts]
    s = "-".join(parts)
    s = s.replace("spe-", "spe")
    s = s.replace("s-", "s")
    if s.endswith("s"):
        s += "0"
    return s


def is_valid_value_for_pid_v2(value):
    if len(value or "") != 23:
        raise ValueError
    return True


VALIDATE_FUNCTIONS = dict((("scielo_pid_v2", is_valid_value_for_pid_v2),))


def is_allowed_to_update(xml_sps, attr_name, attr_new_value):
    """
    Se há uma função de validação associada com o atributo,
    verificar se é permitido atualizar o atributo, dados seus valores
    atual e/ou novo
    """
    validate_function = VALIDATE_FUNCTIONS.get(attr_name)
    if validate_function is None:
        # não há nenhuma validação, então é permitido fazer a atualização
        return True

    curr_value = getattr(xml_sps, attr_name)

    if attr_new_value == curr_value:
        # desnecessario atualizar
        return False

    try:
        # valida o valor atual do atributo
        validate_function(curr_value)

    except (ValueError, exceptions.InvalidValueForOrderError):
        # o valor atual do atributo é inválido,
        # então continuar para verificar o valor "novo"
        pass

    else:
        # o valor atual do atributo é válido,
        # então não permitir atualização
        raise exceptions.NotAllowedtoChangeAttributeValueError(
            "Not allowed to update %s (%s) with %s, "
            "because current is valid" % (attr_name, curr_value, attr_new_value)
        )

    try:
        # valida o valor novo para o atributo
        validate_function(attr_new_value)

    except (ValueError, exceptions.InvalidValueForOrderError):
        # o valor novo é inválido, então não permitir atualização
        raise exceptions.InvalidAttributeValueError(
            "Not allowed to update %s (%s) with %s, "
            "because new value is invalid" % (attr_name, curr_value, attr_new_value)
        )

    else:
        # o valor novo é válido, então não permitir atualização
        return True


def match_pubdate(node, pubdate_xpaths):
    """
    Retorna o primeiro match da lista de pubdate_xpaths
    """
    for xpath in pubdate_xpaths:
        pubdate = node.find(xpath)
        if pubdate is not None:
            return pubdate


def _generate_tag_list(tags_to_keep, tags_to_convert_to_html):
    return list(tags_to_keep or []) + list(
        tags_to_convert_to_html and tags_to_convert_to_html.keys() or []
    )


def remove_subtags(
    node,
    tags_to_keep=None,
    tags_to_keep_with_content=None,
    tags_to_remove_with_content=None,
    tags_to_convert_to_html=None,
):
    """
    Remove as subtags de node que não estiverem especificadas em allowed_tags.

    Exemplo:
        Entrada: <bold><italic>São</italic> Paulo</bold> <i>Paulo</i>, ['italic']
        Saída: <italic>São</italic> Paulo Paulo

    Outros exemplos nos testes.
    """

    # obtem a tag, seu conteúdo e seus atributos
    tag = node.tag
    text = node.text if node.text is not None else ""

    # verifica se é o caso de manutenção da tag e seu conteúdo
    if tag in (tags_to_keep_with_content or []):
        return tostring(node, xml_declaration=False)

    # verifica se é o caso de remoção do conteúdo da tag
    if tag in (tags_to_remove_with_content or []):
        return ""

    # processa as tags internas
    for child in node:
        text += remove_subtags(
            child,
            tags_to_keep,
            tags_to_keep_with_content,
            tags_to_remove_with_content,
            tags_to_convert_to_html,
        )
        if child.tail is not None:
            text += child.tail

    # gera uma lista com as tags que serão mantidas
    all_tags_to_keep = _generate_tag_list(tags_to_keep, tags_to_convert_to_html)

    text = " ".join(text.split())
    if tag in all_tags_to_keep:
        if attribs := " ".join(
            f'{key}="{value}"' for key, value in node.attrib.items()
        ):
            return f"<{tag} {attribs}>{text}</{tag}>"
        return f"<{tag}>{text}</{tag}>"
    return text


def process_subtags(
        node,
        tags_to_keep=None,
        tags_to_keep_with_content=None,
        tags_to_remove_with_content=None,
        tags_to_convert_to_html=None,
        remove_xref=True
    ):

    if node is None:
        return

    node = deepcopy(node)

    std_to_keep = ["sup", "sub"]
    std_to_keep_with_content = [
        "mml:math",
        "{http://www.w3.org/1998/Math/MathML}math",
        "math",
    ]
    std_to_remove_content = ["xref"] if remove_xref else []
    std_to_convert = {"italic": "i"}

    # garante que as tags em std_to_keep serão mantidas
    if tags_to_keep is None:
        tags_to_keep = std_to_keep
    else:
        tags_to_keep = list(set(tags_to_keep + std_to_keep))

    # garante que as tags em std_to_keep_with_content serão mantidas
    if tags_to_keep_with_content is None:
        tags_to_keep_with_content = std_to_keep_with_content
    else:
        tags_to_keep_with_content = list(
            set(tags_to_keep_with_content + std_to_keep_with_content)
        )

    # verifica se é o caso de manutenção da tag e seu conteúdo
    tag = node.tag
    if tag in tags_to_keep_with_content:
        return tostring(node)

    # garante que as tags em std_to_remove_content serão removidas
    tags_to_remove_with_content = std_to_remove_content + (
        tags_to_remove_with_content or []
    )
    tags_to_remove_with_content = list(set(tags_to_remove_with_content))

    # garante que as tags em std_to_convert serão convertidas em html
    std_to_convert.update(tags_to_convert_to_html or {})

    text = remove_subtags(
        node,
        tags_to_keep=tags_to_keep,
        tags_to_keep_with_content=tags_to_keep_with_content,
        tags_to_remove_with_content=tags_to_remove_with_content,
        tags_to_convert_to_html=std_to_convert,
        # namespace_map=std_namespace_map
    )

    for xml_tag, html_tag in std_to_convert.items():
        text = text.replace(f"<{xml_tag} ", f"<{html_tag} ")
        text = text.replace(f"<{xml_tag}>", f"<{html_tag}>")
        text = text.replace(f"</{xml_tag}>", f"</{html_tag}>")

    return text


def get_parent_context(xmltree):
    main = xmltree.xpath(".")[0]
    main_lang = main.get("{http://www.w3.org/XML/1998/namespace}lang")
    main_article_type = main.get("article-type")
    for node in xmltree.xpath("./front | ./body | ./back | ./sub-article"):
        parent = "sub-article" if node.tag == "sub-article" else "article"
        parent_id = node.get("id")
        lang = node.get("{http://www.w3.org/XML/1998/namespace}lang") or main_lang
        article_type = node.get("article-type") or main_article_type
        yield node, lang, article_type, parent, parent_id


def put_parent_context(data, lang, article_type, parent, parent_id):
    data.update(
        {
            "parent": parent,
            "parent_id": parent_id,
            "parent_lang": lang,
            "parent_article_type": article_type,
        }
    )
    return data


def get_parent_data(node):
    return {
        "parent": node.tag,
        "parent_id": node.get("id"),
        "parent_lang": node.get("{http://www.w3.org/XML/1998/namespace}lang"),
        "parent_article_type": node.get("article-type"),
        "xpath": "sub-article" if node.tag == "sub-article" else "front | body | back"
    }


def get_parents(xmltree):
    main = xmltree.xpath(".")[0]
    yield get_parent_data(main)
    for node in xmltree.xpath("./sub-article"):
        yield get_parent_data(node)
        for sub_node in node.xpath("./sub-article"):
            yield get_parent_data(sub_node)
