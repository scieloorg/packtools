from unittest import TestCase

from lxml import etree

from packtools.sps.utils import xml_utils


class TestXMLUtils(TestCase):

    def test_node_text_diacritics(self):
        xmltree = xml_utils.get_xml_tree("<root><city>São Paulo</city></root>")
        expected = "São Paulo"
        result = xml_utils.node_text(xmltree.find(".//city"))
        self.assertEqual(expected, result)

    def test_tostring_diacritics_from_root(self):
        xmltree = xml_utils.get_xml_tree("<root><city>São Paulo</city></root>")
        expected = (
            "<?xml version='1.0' encoding='utf-8'?>\n"
            "<root><city>São Paulo</city></root>"
        )
        result = xml_utils.tostring(xmltree)
        self.assertEqual(expected, result)

    def test_tostring_entity_from_root(self):
        xmltree = xml_utils.get_xml_tree(
            "<root><city>S&#227;o Paulo</city></root>")
        expected = (
            "<?xml version='1.0' encoding='utf-8'?>\n"
            "<root><city>São Paulo</city></root>"
        )
        result = xml_utils.tostring(xmltree)
        self.assertEqual(expected, result)


class NodeTextTest(TestCase):

    def test_node_text_with_sublevels(self):
        xmltree = etree.fromstring(
            """
            <root>
            <city><bold><italic>São</italic> Paulo</bold> <i>Paulo</i></city>
            </root>
            """
        )
        expected = "<bold><italic>São</italic> Paulo</bold> <i>Paulo</i>"
        result = xml_utils.node_text(xmltree.find(".//city"))
        self.assertEqual(expected, result)

    def test_generate_tag_list(self):
        expected = ['sup', 'sub', 'italic', 'bold']
        obtained = xml_utils._generate_tag_list(
            ['sup', 'sub'],
            {
                'italic': 'i',
                'bold': 'b'
            }
        )
        self.assertEqual(expected, obtained)

    def test_process_subtags_keeps_i(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <root>
            <city><bold><italic>São</italic> Paulo</bold> <i>Paulo</i></city>
            </root>
            """
        )
        expected = "<i>São</i> Paulo <i>Paulo</i>"
        obtained = xml_utils.process_subtags(xmltree.find(".//city"), ['i'])
        self.assertEqual(expected, obtained)

    def test_process_subtags_keeps_bold(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <root>
            <city><bold><italic>São</italic> Paulo</bold> <i>Paulo</i></city>
            </root>
            """
        )
        expected = "<bold><i>São</i> Paulo</bold> Paulo"
        obtained = xml_utils.process_subtags(xmltree.find(".//city"), ['bold'])
        self.assertEqual(expected, obtained)

    def test_process_subtags_keeps_italic(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <root>
            <city><bold><italic>São</italic> Paulo</bold> <i>Paulo</i></city>
            </root>
            """
        )
        expected = "<i>São</i> Paulo Paulo"
        obtained = xml_utils.process_subtags(xmltree.find(".//city"), ['italic'])
        self.assertEqual(expected, obtained)

    def test_process_subtags_keeps_bold_and_italic(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <root>
            <city><bold><italic>São</italic> Paulo</bold> <i>Paulo</i></city>
            </root>
            """
        )
        expected = "<bold><i>São</i> Paulo</bold> Paulo"
        obtained = xml_utils.process_subtags(xmltree.find(".//city"), ['bold', 'italic'])
        self.assertEqual(expected, obtained)

    def test_process_subtags_keeps_bold_and_i(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <root>
            <city><bold><italic>São</italic> Paulo</bold> <i>Paulo</i></city>
            </root>
            """
        )
        expected = "<bold><i>São</i> Paulo</bold> <i>Paulo</i>"
        obtained = xml_utils.process_subtags(xmltree.find(".//city"), ['bold', 'i'])
        self.assertEqual(expected, obtained)

    def test_process_subtags_keeps_italic_and_i(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <root>
            <city><bold><italic>São</italic> Paulo</bold> <i>Paulo</i></city>
            </root>
            """
        )
        expected = "<i>São</i> Paulo <i>Paulo</i>"
        obtained = xml_utils.process_subtags(xmltree.find(".//city"), ['italic', 'i'])
        self.assertEqual(expected, obtained)

    def test_process_subtags_keeps_all(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <root>
            <city><bold><italic>São</italic> Paulo</bold> <i>Paulo</i></city>
            </root>
            """
        )
        expected = "<bold><i>São</i> Paulo</bold> <i>Paulo</i>"
        obtained = xml_utils.process_subtags(xmltree.find(".//city"), ['bold', 'italic', 'i'])
        self.assertEqual(expected, obtained)

    def test_process_subtags_keeps_math(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML">'
            '<article-title xmlns:mml="http://www.w3.org/1998/Math/MathML">'
            'Uma Reflexão de Professores sobre Demonstrações Relativas à Irracionalidade de ' 
            '<inline-formula><mml:math display="inline" id="m1"><mml:mrow><mml:msqrt><mml:mn>2</mml:mn></mml:msqrt>'
            '</mml:mrow></mml:math></inline-formula> </article-title>'
            '</article>'
        )
        expected = ('Uma Reflexão de Professores sobre Demonstrações Relativas à Irracionalidade de '
                    '<mml:math xmlns:mml="http://www.w3.org/1998/Math/MathML" display="inline" '
                    'id="m1"><mml:mrow><mml:msqrt><mml:mn>2</mml:mn></mml:msqrt></mml:mrow></mml:math>')

        obtained = xml_utils.process_subtags(xmltree.find(".//article-title"))
        self.assertEqual(expected, obtained)

    def test_process_subtags_keeps_math_tex_math(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            '<p>... Selected as described for Acc-29'
            '<disp-formula>'
            '<tex-math id="M1"><![CDATA[xxxxxxxxxx]]></tex-math>'
            '</disp-formula> TER1/ter1-Acc: Acc-29 crossed with ...</p>'
        )
        expected = ('... Selected as described for Acc-29xxxxxxxxxx TER1/ter1-Acc: Acc-29 crossed with ...')

        obtained = xml_utils.process_subtags(xmltree.find("."))
        self.assertEqual(expected, obtained)

    def test_process_subtags_remove_italic_content(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <root>
            <city><bold><italic>São</italic> Paulo</bold> <i>Paulo</i></city>
            </root>
            """
        )
        expected = "Paulo Paulo"
        obtained = xml_utils.process_subtags(
            xmltree.find(".//city"),
            tags_to_keep=None,
            tags_to_remove_with_content=['italic'],
            tags_to_convert_to_html=None
        )
        self.assertEqual(expected, obtained)

    def test_process_subtags_keep_bold_remove_with_content_i_convert_italic(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <root>
            <city><bold><italic>São</italic> Paulo</bold> <i>Paulo</i></city>
            </root>
            """
        )
        expected = "<bold><i>São</i> Paulo</bold>"
        obtained = xml_utils.process_subtags(
            xmltree.find(".//city"),
            tags_to_keep=['bold'],
            tags_to_remove_with_content=['i'],
            tags_to_convert_to_html={'italic': 'i'}
        )
        self.assertEqual(expected, obtained)

    def test_process_subtags_standard_remove(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <article>
                <article-meta>
                    <p><xref ref-type="aff" rid="aff1">1</xref></p>     
                    <aff id="aff1">
                        <p>affiliation</p>
                    </aff>

                    <p><xref ref-type="fig" rid="fig1">1</xref></p>     
                    <fig id="fig1">
                        <p>figure</p>
                    </fig>

                    <p><xref ref-type="table" rid="table1">1</xref></p>     
                    <table id="table1">
                        <p>table</p>
                    </table>
                </article-meta>
            </article>
            """
        )
        expected = "affiliation figure table"
        obtained = xml_utils.process_subtags(xmltree.find(".//article-meta"))
        self.assertEqual(expected, obtained)

    def test_convert_xml_to_html(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <root>
            <city><bold><italic>São</italic> Paulo</bold> <i>Paulo</i></city>
            </root>
            """
        )
        expected = "<b><i>São</i> Paulo</b> Paulo"
        obtained = xml_utils.process_subtags(
            xmltree.find(".//city"),
            tags_to_keep=None,
            tags_to_remove_with_content=None,
            tags_to_convert_to_html={'italic': 'i', 'bold': 'b'}
        )
        self.assertEqual(expected, obtained)

    def test_convert_xml_to_html_without_dict(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <root>
            <city><bold><italic>São</italic> Paulo</bold> <i>Paulo</i></city>
            </root>
            """
        )
        expected = "<bold><i>São</i> Paulo</bold> Paulo"
        obtained = xml_utils.process_subtags(
            xmltree.find(".//city"),
            ['italic', 'bold']
        )
        self.assertEqual(expected, obtained)

    def test_convert_xml_to_html_with_attribs(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <article>
                <front>
                <journal-meta>
                    <journal-id journal-id-type="nlm-ta">Rev Saude Publica</journal-id>
                    <journal-title-group>
                        <journal-title>Revista de Saúde Pública</journal-title>
                        <abbrev-journal-title abbrev-type="publisher">Rev. Saúde Pública</abbrev-journal-title>
                    </journal-title-group>
                    <issn pub-type="ppub">0034-8910</issn>
                    <issn pub-type="epub">1518-8787</issn>
                    <publisher>
                        <publisher-name>Faculdade de Saúde Pública da Universidade de São Paulo</publisher-name>
                    </publisher>
                </journal-meta>
                </front>
            </article>
            """
        )

        expected = (
            '<journal-id journal-id-type="nlm-ta">Rev Saude Publica</journal-id> '
            'Revista de Saúde Pública '
            '<abbrev-journal-title abbrev-type="publisher">Rev. Saúde Pública</abbrev-journal-title> '
            '<issn pub-type="ppub">0034-8910</issn> '
            '<issn pub-type="epub">1518-8787</issn> '
            'Faculdade de Saúde Pública da Universidade de São Paulo'
        )

        obtained = xml_utils.process_subtags(
            xmltree.find(".//front"),
            tags_to_keep=['journal-id', 'abbrev-journal-title', 'issn']
        )
        self.assertEqual(expected, obtained)


class NodeTextWithoutXrefTest(TestCase):

    def test_node_text_without_xref_with_sublevels(self):
        xmltree = etree.fromstring(
            """
            <root>
            <city><bold><italic>São</italic> Paulo</bold> <i>Paulo</i><xref rid="fn1">1</xref>, <xref rid="fn2">2</xref></city>
            </root>
            """
        )
        expected = "<bold><italic>São</italic> Paulo</bold> <i>Paulo</i>"
        result = xml_utils.node_text_without_xref(xmltree.find(".//city"))
        self.assertEqual(expected, result)

    def test_node_text_without_xref_with_sublevels_keeps_xref_tail(self):
        xmltree = etree.fromstring(
            """
            <root>
            <city><bold><italic>São</italic> Paulo</bold> <i>Paulo</i><xref rid="fn1">*</xref> texto para manter</city>
            </root>
            """
        )
        expected = "<bold><italic>São</italic> Paulo</bold> <i>Paulo</i> texto para manter"
        result = xml_utils.node_text_without_xref(xmltree.find(".//city"))
        self.assertEqual(expected, result)


class XrefRefTypeFn(TestCase):


    def test_node_plain_text_xref_ref_type_bibr_preserved(self):
        """Testa se <xref> com ref-type='bibr' mantém seu conteúdo."""
        xmltree = etree.fromstring(
            """
            <title-group>
            <article-title>
            De espaços abandonados, de <xref ref-type="bibr" rid="B8">Luísa Geisler (2018)</xref>: o dialogismo e a narração multipessoal
            </article-title>
            </title-group>
            """
        )
        expected = "De espaços abandonados, de Luísa Geisler (2018): o dialogismo e a narração multipessoal"
        result = xml_utils.node_plain_text(xmltree.find(".//article-title"))
        self.assertEqual(expected, result)

    def test_node_plain_text_xref_ref_type_bibr_with_italic_preserved(self):
        """Testa se <xref> com ref-type='bibr' e <italic> mantém o conteúdo formatado."""
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <title-group>
            <trans-title>
            De espaços abandonados, <italic>de</italic> <xref ref-type="bibr" rid="B8"><italic>Luísa Geisler (2018)</italic></xref>: <italic>el dialogismo y la narración multipersonal</italic> 
            </trans-title>
            </title-group>
            """
        )
        expected = "De espaços abandonados, de Luísa Geisler (2018): el dialogismo y la narración multipersonal"
        result = xml_utils.node_plain_text(xmltree.find(".//trans-title"))
        self.assertEqual(expected, result)

    def test_node_text_without_xref_xref_ref_type_bibr_preserved(self):
        """Testa se <xref> com ref-type='bibr' mantém seu conteúdo."""
        xmltree = etree.fromstring(
            """
            <title-group>
            <article-title>De espaços abandonados, de <xref ref-type="bibr" rid="B8">Luísa Geisler (2018)</xref>: o dialogismo e a narração multipessoal</article-title>
            </title-group>
            """
        )
        expected = 'De espaços abandonados, de <xref ref-type="bibr" rid="B8">Luísa Geisler (2018)</xref>: o dialogismo e a narração multipessoal'
        result = xml_utils.node_text_without_xref(xmltree.find(".//article-title"))
        self.assertEqual(expected, result)

    def test_node_text_without_xref_xref_ref_type_bibr_with_italic_preserved(self):
        """Testa se <xref> com ref-type='bibr' e <italic> mantém o conteúdo formatado."""
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <title-group>
            <trans-title>De espaços abandonados, <italic>de</italic> <xref ref-type="bibr" rid="B8"><italic>Luísa Geisler (2018)</italic></xref>: <italic>el dialogismo y la narración multipersonal</italic></trans-title>
            </title-group>
            """
        )
        expected = 'De espaços abandonados, <italic>de</italic> <xref ref-type="bibr" rid="B8"><italic>Luísa Geisler (2018)</italic></xref>: <italic>el dialogismo y la narración multipersonal</italic>'
        result = xml_utils.node_text_without_xref(xmltree.find(".//trans-title"))
        self.assertEqual(expected, result)

    def test_process_subtags_xref_ref_type_bibr_preserved(self):
        """Testa se <xref> com ref-type='bibr' mantém seu conteúdo."""
        xmltree = etree.fromstring(
            """
            <title-group>
            <article-title>De espaços abandonados, de <xref ref-type="bibr" rid="B8">Luísa Geisler (2018)</xref>: o dialogismo e a narração multipessoal</article-title>
            </title-group>
            """
        )
        expected = 'De espaços abandonados, de Luísa Geisler (2018): o dialogismo e a narração multipessoal'
        result = xml_utils.process_subtags(xmltree.find(".//article-title"))
        self.assertEqual(expected, result)

    def test_process_subtags_xref_ref_type_bibr_with_italic_preserved(self):
        """Testa se <xref> com ref-type='bibr' e <italic> mantém o conteúdo formatado."""
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <title-group>
            <trans-title>De espaços abandonados, <italic>de</italic> <xref ref-type="bibr" rid="B8"><italic>Luísa Geisler (2018)</italic></xref>: <italic>el dialogismo y la narración multipersonal</italic></trans-title>
            </title-group>
            """
        )
        expected = 'De espaços abandonados, <i>de</i> <i>Luísa Geisler (2018)</i>: <i>el dialogismo y la narración multipersonal</i>'
        result = xml_utils.process_subtags(xmltree.find(".//trans-title"))
        self.assertEqual(expected, result)



