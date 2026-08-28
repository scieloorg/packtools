import os
import tempfile
import unittest

from packtools.sps.pid_provider.xml_loader import xml_parser_ent2char


class XmlParserEnt2CharXXEProtectionTest(unittest.TestCase):
    """
    lxml < 6.1.0 resolve entidades externas por padrão, permitindo que um XML
    malicioso leia arquivos locais via `<!ENTITY xxe SYSTEM "file://...">`.
    xml_parser_ent2char() usa recover=True, então uma entidade externa
    bloqueada não levanta exceção: o parser recupera e descarta o conteúdo
    não resolvido. O que importa é que o conteúdo do arquivo nunca apareça
    no resultado.
    """

    def setUp(self):
        self.secret_content = "conteudo-secreto-que-nao-pode-vazar"
        fd, self.secret_path = tempfile.mkstemp(suffix=".txt")
        with os.fdopen(fd, "w") as f:
            f.write(self.secret_content)

    def tearDown(self):
        os.unlink(self.secret_path)

    def test_external_entity_file_content_never_leaks(self):
        xml = (
            '<?xml version="1.0"?>'
            '<!DOCTYPE article [ <!ENTITY xxe SYSTEM "file://{}"> ]>'
            "<article><body>&xxe;</body></article>"
        ).format(self.secret_path)

        result = xml_parser_ent2char(xml)

        self.assertIsNotNone(result)
        self.assertNotIn(self.secret_content, result)

    def test_internal_character_entity_still_resolved(self):
        xml = (
            '<?xml version="1.0"?>'
            '<!DOCTYPE article [ <!ENTITY ok "texto interno"> ]>'
            "<article><body>&ok;</body></article>"
        )
        result = xml_parser_ent2char(xml)
        self.assertIn("texto interno", result)
