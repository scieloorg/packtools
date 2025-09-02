import html
import logging
from lxml import etree
from bs4 import BeautifulSoup
from packtools.sps.pid_provider.name2number import NAME_TO_NUMBER_ENTITIES


def fix_entities(xml):
    return format_output(html_parser_ent2char(xml))


def discover_entities_to_fix_in_output(bkp):
    bkp = bkp.replace("&amp;", "<ISOLAENTIDADEXML>&")
    bkp = bkp.replace(";", ";<ISOLAENTIDADEXML>")

    for item in bkp.split("<ISOLAENTIDADEXML>"):
        if not item.strip():
            continue
        if " " in item:
            continue
        if item[0] == "&" and item[-1] == ";":
            yield item.replace("&", "&amp;")


def format_output(xml):
    if "&" not in xml:
        return xml

    entities = set(discover_entities_to_fix_in_output(xml))
    if not entities:
        return xml

    for ent in entities:
        xml = xml.replace(ent, NAME_TO_NUMBER_ENTITIES.get(ent) or ent)
    return xml


def xml_parser_ent2char(xml):
    try:
        parser = etree.XMLParser(recover=True, encoding="utf-8")
        root = etree.fromstring(xml, parser)
        return etree.tostring(root, method="xml", encoding="utf-8").decode("utf-8")
    except Exception as e:
        logging.info("opção 1")
        logging.exception(e)


def html_unescape_ent2char(xml):
    try:
        xml = html.unescape(xml)
        root = etree.fromstring(xml)
        return etree.tostring(root, method="xml", encoding="utf-8").decode("utf-8")
    except Exception as e:
        logging.info("opção 2")
        logging.exception(e)


def html_parser_ent2char(xml):
    try:
        parser = etree.HTMLParser()
        root = etree.fromstring(xml, parser)
        return etree.tostring(root.find(".").find("body").find("*"), method="xml", encoding="utf-8").decode("utf-8")
    except Exception as e:
        logging.info("opção 3")
        logging.exception(e)


def bs_ent2char_(xml):
    parsers = [
        ("xml", "Alias para lxml-xml"),
        ("lxml", "Parser HTML com lxml, rápido"),
        ("html.parser", "Parser HTML built-in do Python"),
        ("html5lib", "Parser HTML5 mais compatível"),  # Precisa instalar
    ]
    for parser, description in parsers:
        print(f"\n---\n{parser}")
        soup_xml = BeautifulSoup(xml, parser)
        yield str(soup_xml)


def bs_ent2char(xml):
    soup_xml = BeautifulSoup(xml, "lxml")
    return str(soup_xml)


def main():
    xml = """<document>
	    <title>Exemplo com Entidades</title>
	    <content>&rsquo;&iacute;
	        <paragraph>&ldquo;Quotes&rdquo; e &lquo;apostrophes&rquo;</paragraph>
	        <special>&mdash; travessão &nbsp; espaço &copy;2024</special>
	        <price>&euro;100 ou &pound;80</price>
	        <math>&frac12; &times; 2 = 1</math>
	        <nested>
	            <item id="1">Primeiro &rquo;item&lquo;</item>
	            <item id="2">Segundo &mdash; item</item>
	        </nested>
	        <p>mdash : &mdash;</p>
			<p>180 : &#180;</p>
			<p>rquo : &rquo;<break/>191 : &#191; | &#x02019;</p>
			<p>187 : &#187;</p>
	    </content>
	</document>"""

    print("\n---\nEntrada")
    print(xml)

    print("\n---\nxml_parser_ent2char")
    print(xml_parser_ent2char(xml))

    print("\n---\nhtml_unescape_ent2char")
    print(html_unescape_ent2char(xml))

    print("\n---\nhtml_parser_ent2char")
    print(html_parser_ent2char(xml))

    print("\n---\nbs_ent2char")
    print(bs_ent2char(xml))

    for item in bs_ent2char_(xml):
        print("")
        print(item)

    print("\n---\nfix_entities")
    print(fix_entities(xml))


if __name__ == "__main__":
    main()
