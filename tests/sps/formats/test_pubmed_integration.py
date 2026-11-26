import glob
import os
import unittest

from lxml import etree as ET

from packtools.sps.formats import pubmed

HERE = os.path.dirname(os.path.abspath(__file__))
DTD_PATH = os.path.join(HERE, "..", "..", "fixtures", "pubmed", "PubMed.dtd")
SAMPLES_DIR = os.path.join(HERE, "..", "..", "samples")

# Samples that don't produce DTD-valid PubMed XML yet on this branch because
# the fix lives in an independent, not-yet-merged sub-issue PR of #1226.
# When one of these unexpectedly starts passing, `assertRaises` below will
# fail loudly -- that's the signal to remove the corresponding entry.
KNOWN_FAILURES = {
    "example.xml": (
        "Author sem <surname> (só <given-names>) produz Author sem "
        "LastName -- corrigido em #1236/PR #1245, ainda não mesclado aqui."
    ),
    "0034-8910-rsp-48-2-0249.xml": (
        "contrib sem xref de afiliação faz get_affiliations quebrar com "
        "TypeError -- corrigido com `or []` em #1236/PR #1245, ainda não "
        "mesclado aqui."
    ),
}


def _sample_paths():
    return sorted(glob.glob(os.path.join(SAMPLES_DIR, "*.xml")))


def _build_article_set_xml(path):
    xml_tree = ET.parse(path).getroot()
    article = pubmed.build_pubmed_article(xml_tree)
    return pubmed.build_article_set_xml([article])


class PubmedRealSamplesEndToEndTest(unittest.TestCase):
    """
    Testes de integração fim-a-fim: cada amostra real em tests/samples/
    passa pelo pipeline completo (build_pubmed_article + build_article_set_xml)
    e o resultado é validado contra a DTD real do PubMed (vendorizada em
    tests/fixtures/pubmed/PubMed.dtd, para não depender de rede). Diferente
    de test_pubmed.py, que testa cada pipe isoladamente com XML sintético
    mínimo, aqui o objetivo é pegar regressões que só aparecem com artigos
    reais e completos (datas, paginação, referências, etc. combinados).
    """

    @classmethod
    def setUpClass(cls):
        cls.dtd = ET.DTD(DTD_PATH)

    def _assert_produces_valid_pubmed_xml(self, path):
        xml_set = _build_article_set_xml(path)
        doc = ET.fromstring(xml_set.encode("utf-8"))
        valid = self.dtd.validate(doc)
        if not valid:
            self.fail(str(self.dtd.error_log.filter_from_errors()))

    def test_real_samples_produce_dtd_valid_pubmed_xml(self):
        paths = _sample_paths()
        self.assertTrue(paths, "nenhuma amostra encontrada em tests/samples/*.xml")

        for path in paths:
            name = os.path.basename(path)
            with self.subTest(sample=name):
                if name in KNOWN_FAILURES:
                    with self.assertRaises(
                        (AssertionError, TypeError),
                        msg=(
                            f"{name} passou a gerar XML válido -- remova a "
                            f"entrada em KNOWN_FAILURES ({KNOWN_FAILURES[name]})"
                        ),
                    ):
                        self._assert_produces_valid_pubmed_xml(path)
                else:
                    self._assert_produces_valid_pubmed_xml(path)

    def test_no_stale_known_failures(self):
        """Garante que KNOWN_FAILURES só referencia amostras que existem."""
        existing = {os.path.basename(p) for p in _sample_paths()}
        stale = set(KNOWN_FAILURES) - existing
        self.assertFalse(
            stale, f"KNOWN_FAILURES referencia amostras inexistentes: {stale}"
        )


if __name__ == "__main__":
    unittest.main()