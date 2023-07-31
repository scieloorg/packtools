import logging
import re

from copy import deepcopy
from lxml import etree
from packtools import validations
from packtools.sps import exceptions
from packtools import file_utils


logger = logging.getLogger(__name__)


def get_nodes_with_lang(xmltree, lang_xpath, node_xpath=None):
    _items = []
    for node in xmltree.xpath(lang_xpath):
        _item = {}
        if node_xpath:
            _item["node"] = node.find(node_xpath)
        else:
            _item["node"] = node
        _item["lang"] = node.get('{http://www.w3.org/XML/1998/namespace}lang')
        _items.append(_item)
    return _items


def node_plain_text(node):
    """
    Função que retorna texto de nó, sem subtags e com espaços padronizados

    Entrada:
    ```xml
    <node>
        <italic>Duguetia leucotricha</italic> (Annonaceae)<xref>1</xref>
    </node>
    ```

    Saída:
    Duguetia leucotricha (Annonaceae)
    """
    if node is None:
        return
    for xref in node.findall(".//xref"):
        for child in xref.findall(".//*"):
            child.text = ""
        xref.text = ""
    text = "".join([text for text in node.xpath(".//text()") if text.strip()])
    return " ".join(text.split())


def node_text_without_xref(node):
    """
    Retorna text com subtags, exceto `xref`
    """
    if node is None:
        return

    node = deepcopy(node)

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


def tostring(node, doctype=None, pretty_print=False):
    return etree.tostring(
        node,
        doctype=doctype,
        xml_declaration=True,
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
        items.append(
            etree.tostring(child, encoding="utf-8").decode("utf-8")
        )
    return "".join(items)


def get_node_without_subtag(node, remove_extra_spaces=False):
    """
        Função que retorna nó sem subtags. 
    """
    if remove_extra_spaces:
        return " ".join([text.strip()for text in node.xpath(".//text()") if text.strip()])
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
            [(node.findtext(item) or "").zfill(2)
             for item in ["year", "month", "day"]]
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


def is_allowed_to_update(xml_sps, attr_name, attr_new_value):
    """
    Se há uma função de validação associada com o atributo,
    verificar se é permitido atualizar o atributo, dados seus valores
    atual e/ou novo
    """
    validate_function = validations.VALIDATE_FUNCTIONS.get(attr_name)
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
            "because current is valid" %
            (attr_name, curr_value, attr_new_value))

    try:
        # valida o valor novo para o atributo
        validate_function(attr_new_value)

    except (ValueError, exceptions.InvalidValueForOrderError):
        # o valor novo é inválido, então não permitir atualização
        raise exceptions.InvalidAttributeValueError(
            "Not allowed to update %s (%s) with %s, "
            "because new value is invalid" %
            (attr_name, curr_value, attr_new_value))

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
