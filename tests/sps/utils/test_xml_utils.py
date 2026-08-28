# coding: utf-8
import os
import tempfile
import unittest

from lxml import etree

from packtools.sps import exceptions
from packtools.sps.utils import xml_utils


class XMLUtilsTest(unittest.TestCase):

    def test_node_plain_text(self):
        xml = etree.fromstring(
            "<root>"
            "<title>Texto 1    <italic>italico</italic> TExto 2"
            "<xref><sup><bold>1</bold></sup></xref> "
            "         "
            "Texto 3</title></root>"
        )
        expected = "Texto 1 italico TExto 2 Texto 3"
        result = xml_utils.node_plain_text(xml.find(".//title"))
        self.assertEqual(expected, result)

    def test_node_text_without_xref(self):
        xml = etree.fromstring(
            "<root>"
            "<title>Texto 1    <italic>italico</italic> TExto 2"
            "<xref><sup><bold>1</bold></sup></xref> Texto 3</title></root>"
        )
        expected = "Texto 1    <italic>italico</italic> TExto 2 Texto 3"
        node = xml.find(".//title")
        result = xml_utils.node_text_without_fn_xref(node)
        self.assertEqual(expected, result)


class ProcessXrefTailPreservationTest(unittest.TestCase):
    """
    A partir do lxml 5.x, Element.addnext() deixou de mover automaticamente
    o `.tail` do elemento original para o elemento inserido (comportamento
    presente no lxml 4.9.3, usado até então). O workaround em process_xref()
    (marcador EMPTYTAGTOKEEPXREFTAIL) depende de preservar esse tail antes de
    `parent.remove(xref)` descartá-lo junto com o xref. Estes testes travam
    esse comportamento contra qualquer versão do lxml.
    """

    def test_tail_preserved_when_numeric_fn_xref_removed(self):
        node = etree.fromstring(
            '<p>a <xref ref-type="fn">1</xref> b</p>'
        )
        result = xml_utils.process_xref(node)
        self.assertEqual("a  b", "".join(result.xpath(".//text()")))
        self.assertIsNone(result.find(".//xref"))

    def test_tail_preserved_when_punctuation_marker_xref_removed(self):
        node = etree.fromstring(
            '<p>a <xref ref-type="fn">*</xref> b</p>'
        )
        result = xml_utils.process_xref(node, footnote_markers=["*"])
        self.assertEqual("a  b", "".join(result.xpath(".//text()")))
        self.assertIsNone(result.find(".//xref"))

    def test_no_tail_when_xref_is_last_child(self):
        node = etree.fromstring(
            '<p>a <xref ref-type="fn">1</xref></p>'
        )
        result = xml_utils.process_xref(node)
        self.assertEqual("a ", "".join(result.xpath(".//text()")))
        self.assertIsNone(result.find(".//EMPTYTAGTOKEEPXREFTAIL"))

    def test_xref_not_removed_when_not_fn_nor_marker_nor_numeric(self):
        node = etree.fromstring(
            '<p>see <xref ref-type="bibr">Silva 2020</xref> for details</p>'
        )
        result = xml_utils.process_xref(node)
        self.assertEqual(
            "see Silva 2020 for details",
            "".join(result.xpath(".//text()")),
        )

    def test_tail_preserved_for_fn_xrefs_in_different_parents(self):
        # xrefs em <p> distintos: cada um é o único filho do seu parent, sem
        # irmão xref, então cai no caminho "cria marcador" (getnext() is None)
        # em vez do caminho "pula marcador porque o próximo irmão é um xref"
        # (ver test_sibling_fn_xrefs_lose_intervening_text_known_bug abaixo).
        node = etree.fromstring(
            '<body><p>a <xref ref-type="fn">1</xref> b</p>'
            '<p>c <xref ref-type="fn">2</xref> d</p></body>'
        )
        result = xml_utils.process_xref(node)
        self.assertEqual("a  bc  d", "".join(result.xpath(".//text()")))
        self.assertIsNone(result.find(".//xref"))

    def test_sibling_fn_xrefs_lose_intervening_text_known_bug(self):
        # Bug pré-existente (não introduzido por esta PR, replicado aqui só
        # para documentar/travar o comportamento atual): quando dois <xref>
        # são irmãos diretos sob o mesmo parent, xref.getnext() aponta pro
        # próximo xref independente de haver texto (tail) entre eles, então
        # o código deliberadamente NÃO cria o marcador de preservação pro
        # primeiro xref. Se esse primeiro xref for removido, seu tail (o
        # texto entre os dois xrefs) é descartado junto. Ver issue aberta
        # para acompanhamento; process_xref segue com esse comportamento.
        node = etree.fromstring(
            '<p>a <xref ref-type="fn">1</xref> b '
            '<xref ref-type="fn">2</xref> c</p>'
        )
        result = xml_utils.process_xref(node)
        self.assertEqual("a  c", "".join(result.xpath(".//text()")))

    def test_addnext_no_longer_moves_tail_automatically(self):
        # Canário: isola só o addnext() da lxml, sem passar pelo restante da
        # lógica de process_xref(). Documenta a premissa por trás do fix
        # acima (e da revisão em code review, PR #1283): em lxml 4.9.3,
        # addnext() movia o .tail do elemento original para o elemento
        # inserido como efeito colateral automático; a partir do lxml 5.x
        # (validado também na 6.1.1, versão-alvo desta PR) isso não acontece
        # mais — o tail permanece no elemento original. Se a lxml reverter
        # esse comportamento no futuro, este teste é o primeiro a acusar, e
        # o fix manual em process_xref() (e.tail = xref.tail; xref.tail =
        # None) pode então ser reavaliado.
        original = etree.SubElement(etree.Element("root"), "xref")
        original.tail = " after"
        inserted = etree.Element("MARKER")

        original.addnext(inserted)

        self.assertEqual(" after", original.tail)
        self.assertIsNone(inserted.tail)

    def test_no_marker_tag_leaks_into_final_result(self):
        node = etree.fromstring(
            '<p>a <xref ref-type="fn">1</xref> b</p>'
        )
        result = xml_utils.process_xref(node)
        self.assertNotIn(
            "EMPTYTAGTOKEEPXREFTAIL", etree.tostring(result, encoding="unicode")
        )


class GetXmlTreeXXEProtectionTest(unittest.TestCase):
    """
    lxml < 6.1.0 resolve entidades externas por padrão (resolve_entities=True),
    permitindo que um XML malicioso leia arquivos locais via
    `<!ENTITY xxe SYSTEM "file://...">`. get_xml_tree() precisa continuar
    bloqueando isso mesmo após o bump para lxml 6.1.1 (PYSEC-2026-87).
    """

    def setUp(self):
        self.secret_content = "conteudo-secreto-que-nao-pode-vazar"
        fd, self.secret_path = tempfile.mkstemp(suffix=".txt")
        with os.fdopen(fd, "w") as f:
            f.write(self.secret_content)

    def tearDown(self):
        os.unlink(self.secret_path)

    def test_external_entity_file_read_is_blocked(self):
        xml = (
            '<?xml version="1.0"?>'
            '<!DOCTYPE article [ <!ENTITY xxe SYSTEM "file://{}"> ]>'
            "<article><body>&xxe;</body></article>"
        ).format(self.secret_path)

        with self.assertRaises(exceptions.SPSLoadToXMLError) as ctx:
            xml_utils.get_xml_tree(xml)

        self.assertNotIn(self.secret_content, str(ctx.exception))

    def test_internal_character_entity_still_resolved(self):
        xml = (
            '<?xml version="1.0"?>'
            '<!DOCTYPE article [ <!ENTITY ok "texto interno"> ]>'
            "<article><body>&ok;</body></article>"
        )
        result = xml_utils.get_xml_tree(xml)
        self.assertEqual(
            "texto interno", "".join(result.xpath(".//text()"))
        )

