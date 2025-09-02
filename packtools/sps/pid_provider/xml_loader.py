import html
import logging
from lxml import etree
from bs4 import BeautifulSoup
from packtools.sps.pid_provider.amp_name2number import AMP_NAME_TO_NUMBER_ENTITIES
from packtools.sps.pid_provider.name2number import NAME_TO_NUMBER_ENTITIES


def load_xml(xml):
    return etree.tostring(
        etree.fromstring(fix_input(xml)),
        method="xml", encoding="utf-8").decode("utf-8")


def fix_input(xml):
    if "&" not in xml:
        return xml

    entities = set(find_entities_to_fix_in_input(xml))
    if not entities:
        return xml

    for ent in entities:
        xml = xml.replace(ent, NAME_TO_NUMBER_ENTITIES.get(ent) or f"&amp;{ent}")

    print(xml)
    return xml


def find_entities_to_fix_in_input(bkp):
    bkp = bkp.replace("&", "<ISOLAENTIDADEXML>&")
    bkp = bkp.replace(";", ";<ISOLAENTIDADEXML>")

    for item in bkp.split("<ISOLAENTIDADEXML>"):
        print(item)
        if not item.strip():
            continue
        if " " in item:
            continue
        if not item[0] == "&" and not item[-1] == ";":
            continue
        if item[1] == "#":
            continue
        if item in ("&amp;", "&gt;", "&apos;", "&quot;", "&lt;"):
            continue
        if item[0] == "&" and item[-1] == ";":
            yield item


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
        xml = xml.replace(ent, AMP_NAME_TO_NUMBER_ENTITIES.get(ent) or ent)
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
    xml = """<article>
    <body>
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
    </body>
	</article>"""

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


    print("\n---\nload_xml")
    print(load_xml(xml))

    
if __name__ == "__main__":
    main()


"""
---
Entrada
<article>
        <body>
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
        </body>
    </article>

---
"""
# PERDE OS CARACTERES
"""
xml_parser_ent2char
<article>
        <body>
        <title>Exemplo com Entidades</title>
        <content>
            <paragraph>Quotes e apostrophes</paragraph>
            <special> travessão  espaço 2024</special>
            <price>100 ou 80</price>
            <math>  2 = 1</math>
            <nested>
                <item id="1">Primeiro item</item>
                <item id="2">Segundo  item</item>
            </nested>
            <p>mdash : </p>
            <p>180 : ´</p>
            <p>rquo : <break/>191 : ¿ | ’</p>
            <p>187 : »</p>
        </content>
        </body>
    </article>

---
"""
# NAO CONSEGUE LER O XML
"""
html_unescape_ent2char
ERROR:root:Entity 'lquo' not defined, line 5, column 38 (<string>, line 5)
Traceback (most recent call last):
  File "/Users/roberta.takenaka/github.com/scieloorg/packtools/packtools/packtools/sps/pid_provider/ent2char.py", line 51, in html_unescape_ent2char
    root = etree.fromstring(xml)
  File "src/lxml/etree.pyx", line 3257, in lxml.etree.fromstring
  File "src/lxml/parser.pxi", line 1916, in lxml.etree._parseMemoryDocument
  File "src/lxml/parser.pxi", line 1796, in lxml.etree._parseDoc
  File "src/lxml/parser.pxi", line 1085, in lxml.etree._BaseParser._parseUnicodeDoc
  File "src/lxml/parser.pxi", line 618, in lxml.etree._ParserContext._handleParseResultDoc
  File "src/lxml/parser.pxi", line 728, in lxml.etree._handleParseResult
  File "src/lxml/parser.pxi", line 657, in lxml.etree._raiseParseError
  File "<string>", line 5
lxml.etree.XMLSyntaxError: Entity 'lquo' not defined, line 5, column 38
None

---
"""
# PERDE O ARTICLE/BODY, MAS PERDE O ; APÓS LQUO E RQUO
"""
html_parser_ent2char
<article>

        <title>Exemplo com Entidades</title>
        <content>’í
            <paragraph>“Quotes” e &amp;lquo;apostrophes&amp;rquo;</paragraph>
            <special>— travessão   espaço ©2024</special>
            <price>€100 ou £80</price>
            <math>½ × 2 = 1</math>
            <nested>
                <item id="1">Primeiro &amp;rquo;item&amp;lquo;</item>
                <item id="2">Segundo — item</item>
            </nested>
            <p>mdash : —</p>
            <p>180 : ´</p>
            <p>rquo : &amp;rquo;<break/>191 : ¿ | ’</p>
            <p>187 : »</p>
        </content>

    </article>

---
"""
# MANTÉM O ARTICLE/BODY, MAS PERDE O ; APÓS LQUO E RQUO
"""
bs_ent2char LXML
<article>
<body>
<title>Exemplo com Entidades</title>
<content>’í
            <paragraph>“Quotes” e &amp;lquoapostrophes&amp;rquo</paragraph>
<special>— travessão   espaço ©2024</special>
<price>€100 ou £80</price>
<math>½ × 2 = 1</math>
<nested>
<item id="1">Primeiro &amp;rquoitem&amp;lquo</item>
<item id="2">Segundo — item</item>
</nested>
<p>mdash : —</p>
<p>180 : ´</p>
<p>rquo : &amp;rquo<break></break>191 : ¿ | ’</p>
<p>187 : »</p>
</content>
</body>
</article>

---
"""

# PERDE OS CARACTERES 
"""
xml

<?xml version="1.0" encoding="utf-8"?>
<article>
<body>
<title>Exemplo com Entidades</title>
<content>
<paragraph>Quotes e apostrophes</paragraph>
<special> travessão  espaço 2024</special>
<price>100 ou 80</price>
<math>  2 = 1</math>
<nested>
<item id="1">Primeiro item</item>
<item id="2">Segundo  item</item>
</nested>
<p>mdash : </p>
<p>180 : ´</p>
<p>rquo : <break/>191 : ¿ | ’</p>
<p>187 : »</p>
</content>
</body>
</article>

---
"""

# PERDE O ARTICLE/BODY
"""
lxml

<html><body><article>
<title>Exemplo com Entidades</title>
<content>’í
            <paragraph>“Quotes” e &amp;lquo;apostrophes&amp;rquo;</paragraph>
<special>— travessão   espaço ©2024</special>
<price>€100 ou £80</price>
<math>½ × 2 = 1</math>
<nested>
<item id="1">Primeiro &amp;rquo;item&amp;lquo;</item>
<item id="2">Segundo — item</item>
</nested>
<p>mdash : —</p>
<p>180 : ´</p>
<p>rquo : &amp;rquo;<break></break>191 : ¿ | ’</p>
<p>187 : »</p>
</content>
</article></body></html>

---
"""

# MANTÉM O ARTICLE/BODY, MAS PERDE O ; APÓS LQUO E RQUO
"""
html.parser

<article>
<body>
<title>Exemplo com Entidades</title>
<content>’í
            <paragraph>“Quotes” e &amp;lquoapostrophes&amp;rquo</paragraph>
<special>— travessão   espaço ©2024</special>
<price>€100 ou £80</price>
<math>½ × 2 = 1</math>
<nested>
<item id="1">Primeiro &amp;rquoitem&amp;lquo</item>
<item id="2">Segundo — item</item>
</nested>
<p>mdash : —</p>
<p>180 : ´</p>
<p>rquo : &amp;rquo<break></break>191 : ¿ | ’</p>
<p>187 : »</p>
</content>
</body>
</article>

---
"""

# SOME O ARTICLE/BODY
"""
html5lib

<html><head></head><body><article>

        <title>Exemplo com Entidades</title>
        <content>’í
            <paragraph>“Quotes” e &amp;lquo;apostrophes&amp;rquo;</paragraph>
            <special>— travessão   espaço ©2024</special>
            <price>€100 ou £80</price>
            <math>½ × 2 = 1</math>
            <nested>
                <item id="1">Primeiro &amp;rquo;item&amp;lquo;</item>
                <item id="2">Segundo — item</item>
            </nested>
            <p>mdash : —</p>
            <p>180 : ´</p>
            <p>rquo : &amp;rquo;<break>191 : ¿ | ’</break></p>
            <p>187 : »</p>
        </content>

    </article></body></html>


"""
