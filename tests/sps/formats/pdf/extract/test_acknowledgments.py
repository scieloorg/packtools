import unittest

from lxml import etree

from packtools.sps.formats.pdf.extract import acknowledgments


class TestExtractAcknowledgmentData(unittest.TestCase):

    def test_extract_acknowledgment_data_empty_xml(self):
        xml_tree = etree.fromstring("<article></article>")
        expected = {"paragraphs": [], 'title': ''}
        result = acknowledgments.extract_acknowledgment_data(xml_tree)
        self.assertEqual(expected, result)

    def test_extract_acknowledgment_data_with_title_no_paragraphs(self):
        xml_tree = etree.fromstring(
            """
            <article>
                <ack>
                    <title>Acknowledgments</title>
                </ack>
            </article>
            """
        )
        expected = {
            "title": "Acknowledgments",
            "paragraphs": []
        }
        result = acknowledgments.extract_acknowledgment_data(xml_tree)
        self.assertEqual(expected, result)

    def test_extract_acknowledgment_data_with_paragraphs_no_title(self):
        xml_tree = etree.fromstring(
            """
            <article>
                <ack>
                    <p>First acknowledgment paragraph</p>
                    <p>Second acknowledgment paragraph</p>
                </ack>
            </article>
            """
        )
        result = acknowledgments.extract_acknowledgment_data(xml_tree)
        self.assertEqual(result["title"], '')
        self.assertEqual(
            _paragraph_texts(result),
            ["First acknowledgment paragraph", "Second acknowledgment paragraph"],
        )

    def test_extract_acknowledgment_data_complete(self):
        xml_tree = etree.fromstring(
            """
            <article>
                <ack>
                    <title>Acknowledgements Section</title>
                    <p>Thank you to all contributors</p>
                    <p>Special thanks to funding agencies</p>
                    <p>Additional acknowledgments</p>
                </ack>
            </article>
            """
        )
        result = acknowledgments.extract_acknowledgment_data(xml_tree)
        self.assertEqual(result["title"], "Acknowledgements Section")
        self.assertEqual(
            _paragraph_texts(result),
            [
                "Thank you to all contributors",
                "Special thanks to funding agencies",
                "Additional acknowledgments",
            ],
        )

    def test_extract_acknowledgment_data_nested_paragraphs(self):
        xml_tree = etree.fromstring(
            """
            <article>
                <ack>
                    <title>Acknowledgments</title>
                    <sec>
                        <p>Nested paragraph 1</p>
                        <p>Nested paragraph 2</p>
                    </sec>
                </ack>
            </article>
            """
        )
        result = acknowledgments.extract_acknowledgment_data(xml_tree)
        self.assertEqual(result["title"], "Acknowledgments")
        self.assertEqual(_paragraph_texts(result), ["Nested paragraph 1", "Nested paragraph 2"])

    def test_extract_acknowledgment_data_keeps_text_after_inline_markup(self):
        # sant/v16n2/2238-3875-sant-16-02-e250090 (#1374): o texto era cortado no 1o <italic>
        xml_tree = etree.fromstring(
            """
            <article>
                <ack>
                    <p>aos pareceristas ad hoc da <italic>Sociologia &amp; Antropologia</italic>, pela avaliação cuidadosa; ao comitê editorial da <italic>Sociologia &amp; Antropologia</italic>, pela acolhida do manuscrito.</p>
                </ack>
            </article>
            """
        )
        result = acknowledgments.extract_acknowledgment_data(xml_tree)
        self.assertEqual(
            _paragraph_texts(result),
            [
                "aos pareceristas ad hoc da Sociologia & Antropologia, pela avaliação cuidadosa; "
                "ao comitê editorial da Sociologia & Antropologia, pela acolhida do manuscrito."
            ],
        )
        italic = [seg["text"] for seg in result["paragraphs"][0] if seg["italic"]]
        self.assertEqual(italic, ["Sociologia & Antropologia", "Sociologia & Antropologia"])

    def test_extract_acknowledgment_data_paragraph_starting_with_markup(self):
        # antes, paragraph.text era None quando o <p> começava por um elemento
        xml_tree = etree.fromstring(
            "<article><ack><p><bold>CNPq</bold> e CAPES.</p></ack></article>"
        )
        result = acknowledgments.extract_acknowledgment_data(xml_tree)
        self.assertEqual(_paragraph_texts(result), ["CNPq e CAPES."])

    def test_extract_acknowledgment_data_title_with_markup(self):
        xml_tree = etree.fromstring(
            "<article><ack><title>Agradecimentos à <italic>FAPESP</italic> e ao CNPq</title></ack></article>"
        )
        result = acknowledgments.extract_acknowledgment_data(xml_tree)
        self.assertEqual(result["title"], "Agradecimentos à FAPESP e ao CNPq")


def _paragraph_texts(ack_data):
    return ["".join(seg["text"] for seg in segments) for segments in ack_data["paragraphs"]]
