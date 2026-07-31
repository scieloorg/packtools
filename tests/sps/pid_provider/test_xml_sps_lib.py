from unittest import TestCase
from unittest.mock import patch
from packtools.sps.pid_provider.xml_sps_lib import XMLWithPre

from packtools.sps.pid_provider.xml_sps_lib import (
    XMLWithPre,
    XMLWithPreArticlePublicationDateError,
)

class XMLWithPreTestMixin:
    """Mixin com helper para criar XML de artigo SciELO."""

    def _make_xml(
        self,
        issn_epub=None,
        issn_ppub=None,
        acron="abc",
        vol=None,
        num=None,
        suppl=None,
        elocation=None,
        fpage=None,
        fpage_seq=None,
        lpage=None,
        doi=None,
        order=None,
        v2=None,
        v2_items=None,
    ):
        """
        v2_items : list of tuple(assigning_authority, value), optional
            Permite gerar múltiplos <article-id specific-use="scielo-v2">
            com atributo `assigning-authority`, simulando um artigo
            publicado em mais de uma coleção SciELO. Ex.:
            [("scielo-scl", "S0103-65642009000300003"),
             ("scielo-psi", "S1678-51772009000300003")]
        """
        issn_parts = []
        if issn_epub:
            issn_parts.append(f'<issn pub-type="epub">{issn_epub}</issn>')
        if issn_ppub:
            issn_parts.append(f'<issn pub-type="ppub">{issn_ppub}</issn>')
        issns = "".join(issn_parts) or '<issn pub-type="epub">0000-0000</issn>'

        vol_tag = f"<volume>{vol}</volume>" if vol else ""
        num_tag = f"<issue>{num}</issue>" if num else ""
        suppl_tag = f"<supplement>{suppl}</supplement>" if suppl else ""
        eloc_tag = f"<elocation-id>{elocation}</elocation-id>" if elocation else ""

        fpage_attr = f' seq="{fpage_seq}"' if fpage_seq else ""
        fpage_tag = f"<fpage{fpage_attr}>{fpage}</fpage>" if fpage else ""
        lpage_tag = f"<lpage>{lpage}</lpage>" if lpage else ""

        doi_tag = f'<article-id pub-id-type="doi">{doi}</article-id>' if doi else ""
        order_tag = f'<article-id pub-id-type="other">{order}</article-id>' if order else ""
        v2_tag = f'<article-id specific-use="scielo-v2" pub-id-type="publisher-id">{v2}</article-id>' if v2 else ""

        v2_items_tags = ""
        if v2_items:
            v2_items_tags = "".join(
                f'<article-id pub-id-type="publisher-id" specific-use="scielo-v2" '
                f'assigning-authority="{assigning_authority}">{value}</article-id>'
                for assigning_authority, value in v2_items
            )

        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.1 20151215//EN" "JATS-journalpublishing1.dtd">
<article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
  <front>
    <journal-meta>
      <journal-id journal-id-type="publisher-id">{acron}</journal-id>
      {issns}
    </journal-meta>
    <article-meta>
      {doi_tag}
      {v2_tag}
      {v2_items_tags}
      {order_tag}
      {vol_tag}
      {num_tag}
      {suppl_tag}
      {eloc_tag}
      {fpage_tag}
      {lpage_tag}
    </article-meta>
  </front>
</article>"""
        for item in XMLWithPre.create(xml_content=xml_content):
            return item


class TestSPSPkgNameSuppl(XMLWithPreTestMixin, TestCase):
    """Testes para sps_pkg_name_suppl e deprecated_sps_pkg_name_suppl"""

    def test_sps_pkg_name_suppl_none(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        self.assertIsNone(xml_with_pre.suppl)
        self.assertIsNone(xml_with_pre.sps_pkg_name_suppl)

    def test_sps_pkg_name_suppl_zero(self):
        xml_with_pre = self._make_xml(vol="10", num="2", suppl="0")
        self.assertEqual(xml_with_pre.suppl, "0")
        self.assertEqual(xml_with_pre.sps_pkg_name_suppl, "suppl")

    def test_sps_pkg_name_suppl_numeric(self):
        xml_with_pre = self._make_xml(vol="10", num="2", suppl="1")
        self.assertEqual(xml_with_pre.suppl, "1")
        self.assertEqual(xml_with_pre.sps_pkg_name_suppl, "s1")

    def test_sps_pkg_name_suppl_numeric_two_digits(self):
        xml_with_pre = self._make_xml(vol="10", num="2", suppl="12")
        self.assertEqual(xml_with_pre.suppl, "12")
        self.assertEqual(xml_with_pre.sps_pkg_name_suppl, "s12")

    def test_sps_pkg_name_suppl_text(self):
        xml_with_pre = self._make_xml(vol="10", num="2", suppl="A")
        self.assertEqual(xml_with_pre.suppl, "A")
        self.assertEqual(xml_with_pre.sps_pkg_name_suppl, "sA")

    def test_deprecated_sps_pkg_name_suppl_none(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        self.assertIsNone(xml_with_pre.deprecated_sps_pkg_name_suppl)

    def test_deprecated_sps_pkg_name_suppl_zero(self):
        xml_with_pre = self._make_xml(vol="10", num="2", suppl="0")
        self.assertEqual(xml_with_pre.deprecated_sps_pkg_name_suppl, "suppl")

    def test_deprecated_sps_pkg_name_suppl_numeric(self):
        xml_with_pre = self._make_xml(vol="10", num="2", suppl="1")
        self.assertEqual(xml_with_pre.deprecated_sps_pkg_name_suppl, "1")

    def test_deprecated_sps_pkg_name_suppl_text(self):
        xml_with_pre = self._make_xml(vol="10", num="2", suppl="A")
        self.assertEqual(xml_with_pre.deprecated_sps_pkg_name_suppl, "A")


class TestSPSPkgNameFpage(XMLWithPreTestMixin, TestCase):
    """Testes para sps_pkg_name_fpage e deprecated_sps_pkg_name_fpage"""

    def test_sps_pkg_name_fpage_none(self):
        xml_with_pre = self._make_xml(vol="10", num="2", elocation="e123")
        self.assertIsNone(xml_with_pre.fpage)
        self.assertIsNone(xml_with_pre.sps_pkg_name_fpage)

    def test_sps_pkg_name_fpage_zero(self):
        xml_with_pre = self._make_xml(vol="10", num="2", fpage="0", lpage="0")
        self.assertIsNone(xml_with_pre.fpage)
        self.assertIsNone(xml_with_pre.sps_pkg_name_fpage)

    def test_sps_pkg_name_fpage_simple(self):
        xml_with_pre = self._make_xml(vol="10", num="2", fpage="123", lpage="130")
        self.assertEqual(xml_with_pre.fpage, "123")
        self.assertEqual(xml_with_pre.sps_pkg_name_fpage, "123")

    def test_sps_pkg_name_fpage_with_seq(self):
        xml_with_pre = self._make_xml(vol="10", num="2", fpage="123", fpage_seq="a", lpage="130")
        self.assertEqual(xml_with_pre.fpage, "123")
        self.assertEqual(xml_with_pre.fpage_seq, "a")
        self.assertEqual(xml_with_pre.sps_pkg_name_fpage, "123_a")

    def test_sps_pkg_name_fpage_same_fpage_lpage_with_v2(self):
        xml_with_pre = self._make_xml(
            vol="10", num="2", fpage="123", lpage="123",
            v2="S0101-01011999000100123"
        )
        self.assertEqual(xml_with_pre.fpage, "123")
        self.assertEqual(xml_with_pre.lpage, "123")
        self.assertEqual(xml_with_pre.sps_pkg_name_fpage, "123_00123")

    def test_sps_pkg_name_fpage_same_fpage_lpage_without_v2(self):
        xml_with_pre = self._make_xml(vol="10", num="2", fpage="123", lpage="123")
        self.assertEqual(xml_with_pre.fpage, "123")
        self.assertEqual(xml_with_pre.lpage, "123")
        self.assertEqual(xml_with_pre.sps_pkg_name_fpage, "123")

    def test_sps_pkg_name_fpage_alphanumeric(self):
        xml_with_pre = self._make_xml(vol="10", num="2", fpage="e123", lpage="e130")
        self.assertEqual(xml_with_pre.fpage, "e123")
        self.assertEqual(xml_with_pre.sps_pkg_name_fpage, "e123")

    def test_deprecated_sps_pkg_name_fpage_none(self):
        xml_with_pre = self._make_xml(vol="10", num="2", elocation="e123")
        self.assertIsNone(xml_with_pre.deprecated_sps_pkg_name_fpage)

    def test_deprecated_sps_pkg_name_fpage_zero(self):
        xml_with_pre = self._make_xml(vol="10", num="2", fpage="0", lpage="0")
        self.assertIsNone(xml_with_pre.deprecated_sps_pkg_name_fpage)

    def test_deprecated_sps_pkg_name_fpage_simple(self):
        xml_with_pre = self._make_xml(vol="10", num="2", fpage="123", lpage="130")
        self.assertEqual(xml_with_pre.deprecated_sps_pkg_name_fpage, "123")

    def test_deprecated_sps_pkg_name_fpage_with_seq(self):
        xml_with_pre = self._make_xml(vol="10", num="2", fpage="123", fpage_seq="a", lpage="130")
        self.assertEqual(xml_with_pre.deprecated_sps_pkg_name_fpage, "123a")


class TestSPSPkgName(XMLWithPreTestMixin, TestCase):
    """Testes para sps_pkg_name e deprecated_sps_pkg_name"""

    def test_sps_pkg_name_complete(self):
        xml_with_pre = self._make_xml(
            issn_epub="1234-5678",
            issn_ppub="8765-4321",
            acron="abc",
            vol="10",
            num="2",
            elocation="e12345",
        )
        self.assertEqual(xml_with_pre.sps_pkg_name, "1234-5678-abc-10-02-e12345")

    def test_sps_pkg_name_with_suppl(self):
        xml_with_pre = self._make_xml(
            issn_epub="1234-5678",
            acron="abc",
            vol="10",
            num="2",
            suppl="1",
            fpage="100",
            lpage="110",
        )
        self.assertEqual(xml_with_pre.sps_pkg_name, "1234-5678-abc-10-02-s1-100_110")

    def test_sps_pkg_name_ppub_fallback(self):
        xml_with_pre = self._make_xml(
            issn_ppub="8765-4321",
            acron="xyz",
            vol="5",
            elocation="e001",
        )
        self.assertEqual(xml_with_pre.sps_pkg_name, "8765-4321-xyz-5-e001")

    def test_sps_pkg_name_no_volume_no_number(self):
        xml_with_pre = self._make_xml(
            issn_epub="1111-2222",
            acron="rev",
            elocation="e999",
        )
        self.assertEqual(xml_with_pre.sps_pkg_name, "1111-2222-rev-e999")

    def test_deprecated_sps_pkg_name_with_suppl(self):
        xml_with_pre = self._make_xml(
            issn_epub="1234-5678",
            acron="abc",
            vol="10",
            num="2",
            suppl="1",
            fpage="100",
            lpage="110",
        )
        self.assertEqual(xml_with_pre.deprecated_sps_pkg_name, "1234-5678-abc-10-02-1-100")

    def test_deprecated_sps_pkg_name_suppl_zero(self):
        xml_with_pre = self._make_xml(
            issn_epub="1234-5678",
            acron="abc",
            vol="10",
            num="2",
            suppl="0",
            fpage="100",
            lpage="110",
        )
        self.assertEqual(xml_with_pre.deprecated_sps_pkg_name, "1234-5678-abc-10-02-suppl-100")

    def test_deprecated_sps_pkg_name_version_2_with_suppl(self):
        xml_with_pre = self._make_xml(
            issn_epub="1234-5678",
            acron="abc",
            vol="10",
            num="2",
            suppl="1",
            fpage="100",
            lpage="110",
        )
        # version_2 usa o mesmo suppl de sps_pkg_name (com "s"), mas o
        # sufixo de sps_pkg_name_suffix (não o antigo get_pkg_name_suffix)
        self.assertEqual(
            xml_with_pre.deprecated_sps_pkg_name_version_2,
            "1234-5678-abc-10-02-s1-100",
        )

    def test_deprecated_sps_pkg_name_version_2_no_suppl(self):
        xml_with_pre = self._make_xml(
            issn_epub="1234-5678",
            acron="abc",
            vol="10",
            num="2",
            fpage="123",
            lpage="123",
        )
        self.assertEqual(
            xml_with_pre.deprecated_sps_pkg_name_version_2,
            "1234-5678-abc-10-02-123",
        )

    def test_deprecated_sps_pkg_name_list(self):
        xml_with_pre = self._make_xml(
            issn_epub="1234-5678",
            acron="abc",
            vol="10",
            num="2",
            suppl="1",
            fpage="100",
            lpage="110",
        )
        self.assertEqual(
            xml_with_pre.deprecated_sps_pkg_name_list,
            [
                "1234-5678-abc-10-02-1-100",
                "1234-5678-abc-10-02-s1-100",
            ],
        )

    # -------- add_pkg_name_components --------

    def test_add_pkg_name_components_stores_source_filename_and_ext(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        xml_with_pre.add_pkg_name_components("1234-5678-abc-10-02-s1-100.xml")
        self.assertEqual(xml_with_pre.source_filename, "1234-5678-abc-10-02-s1-100")
        self.assertEqual(xml_with_pre.source_ext, ".xml")

    def test_add_pkg_name_components_default_pkg_name_version(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        xml_with_pre.add_pkg_name_components("1989.htm")
        self.assertEqual(xml_with_pre.pkg_name_version, 3)

    def test_add_pkg_name_components_custom_pkg_name_version(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        xml_with_pre.add_pkg_name_components("1989.htm", pkg_name_version=2)
        self.assertEqual(xml_with_pre.pkg_name_version, 2)

    def test_sps_pkg_name_with_xml_source_filename_bypasses_computation(self):
        # source_filename já é o próprio sps_pkg_name (extensão .xml):
        # sps_pkg_name deve retorná-lo tal como está, ignorando
        # issn/acron/volume/numero/suppl/fpage/etc.
        xml_with_pre = self._make_xml(
            issn_epub="1234-5678",
            acron="abc",
            vol="10",
            num="2",
            suppl="1",
            fpage="100",
            lpage="110",
        )
        xml_with_pre.add_pkg_name_components("1234-5678-abc-10-02-s1-100.xml")
        self.assertEqual(xml_with_pre.sps_pkg_name, "1234-5678-abc-10-02-s1-100")

    def test_sps_pkg_name_with_xml_source_filename_bypasses_even_without_metadata(self):
        # mesmo sem volume/numero/issn, com extensão .xml o nome do
        # pacote é o próprio source_filename (sem extensão)
        xml_with_pre = self._make_xml()
        xml_with_pre.add_pkg_name_components("1234-5678-abc-10-02-s1-100.xml")
        self.assertEqual(xml_with_pre.sps_pkg_name, "1234-5678-abc-10-02-s1-100")

    def test_sps_pkg_name_with_htm_source_filename_appends_as_suffix(self):
        # com extensão diferente de .xml (ex.: .htm, conversão do site
        # clássico), o source_filename ("1989") é incorporado ao
        # sufixo calculado (get_pkg_name_suffix), não substitui o nome
        xml_with_pre = self._make_xml(
            issn_epub="1234-5678",
            acron="abc",
            vol="10",
            num="2",
            fpage="100",
            lpage="110",
        )
        xml_with_pre.add_pkg_name_components("1989.htm")
        self.assertEqual(xml_with_pre.source_filename, "1989")
        self.assertEqual(xml_with_pre.source_ext, ".htm")
        self.assertEqual(
            xml_with_pre.sps_pkg_name, "1234-5678-abc-10-02-100_110_1989"
        )

    def test_sps_pkg_name_with_htm_source_filename_and_suppl(self):
        xml_with_pre = self._make_xml(
            issn_epub="1234-5678",
            acron="abc",
            vol="10",
            num="2",
            suppl="1",
            fpage="100",
            lpage="110",
        )
        xml_with_pre.add_pkg_name_components("1989.htm")
        self.assertEqual(
            xml_with_pre.sps_pkg_name, "1234-5678-abc-10-02-s1-100_110_1989"
        )

    # -------- sps_pkg_name com order e/ou v2 --------
    # get_pkg_name_suffix inclui `self.order or self.v2 and self.v2[-5:]`
    # como parte do sufixo: order tem precedência sobre os 5 últimos
    # dígitos do v2 quando ambos estão presentes.

    def test_sps_pkg_name_without_order_and_without_v2(self):
        xml_with_pre = self._make_xml(
            issn_epub="1234-5678",
            acron="abc",
            vol="10",
            num="2",
            elocation="e100",
        )
        self.assertEqual(xml_with_pre.sps_pkg_name, "1234-5678-abc-10-02-e100")

    def test_sps_pkg_name_with_order_only(self):
        xml_with_pre = self._make_xml(
            issn_epub="1234-5678",
            acron="abc",
            vol="10",
            num="2",
            elocation="e100",
            order="00001",
        )
        self.assertEqual(xml_with_pre.order, "00001")
        self.assertIsNone(xml_with_pre.v2)
        self.assertEqual(
            xml_with_pre.sps_pkg_name, "1234-5678-abc-10-02-e100_00001"
        )

    def test_sps_pkg_name_with_v2_only(self):
        xml_with_pre = self._make_xml(
            issn_epub="1234-5678",
            acron="abc",
            vol="10",
            num="2",
            elocation="e100",
            v2="S0101-01011999000100123",
        )
        self.assertIsNone(xml_with_pre.order)
        self.assertEqual(xml_with_pre.v2, "S0101-01011999000100123")
        self.assertEqual(
            xml_with_pre.sps_pkg_name, "1234-5678-abc-10-02-e100_00123"
        )

    def test_sps_pkg_name_with_order_and_v2_order_takes_precedence(self):
        xml_with_pre = self._make_xml(
            issn_epub="1234-5678",
            acron="abc",
            vol="10",
            num="2",
            elocation="e100",
            order="00001",
            v2="S0101-01011999000100123",
        )
        # order ("00001") prevalece sobre v2[-5:] ("00123")
        self.assertEqual(
            xml_with_pre.sps_pkg_name, "1234-5678-abc-10-02-e100_00001"
        )

    def test_sps_pkg_name_with_order_v2_and_htm_source_filename(self):
        xml_with_pre = self._make_xml(
            issn_epub="1234-5678",
            acron="abc",
            vol="10",
            num="2",
            elocation="e100",
            order="00001",
            v2="S0101-01011999000100123",
        )
        xml_with_pre.add_pkg_name_components("1989.htm")
        self.assertEqual(
            xml_with_pre.sps_pkg_name, "1234-5678-abc-10-02-e100_00001_1989"
        )


class TestSPSPkgNameSuffix(XMLWithPreTestMixin, TestCase):
    """Testes para sps_pkg_name_suffix e alternative_sps_pkg_name_suffix"""

    def test_sps_pkg_name_suffix_elocation_id(self):
        xml_with_pre = self._make_xml(
            vol="10", num="2",
            elocation="e12345",
            fpage="100", lpage="110",
            doi="10.1590/1234",
        )
        self.assertEqual(xml_with_pre.sps_pkg_name_suffix, "e12345")

    def test_sps_pkg_name_suffix_fpage(self):
        xml_with_pre = self._make_xml(
            vol="10", num="2",
            fpage="100", lpage="110",
            doi="10.1590/1234",
        )
        self.assertEqual(xml_with_pre.sps_pkg_name_suffix, "100")

    def test_sps_pkg_name_suffix_doi(self):
        xml_with_pre = self._make_xml(
            vol="10", num="2",
            doi="10.1590/0001-3714.2020.v1.n2.1234",
        )
        self.assertEqual(xml_with_pre.sps_pkg_name_suffix, "0001-3714-2020-v1-n2-1234")

    def test_sps_pkg_name_suffix_doi_simple(self):
        xml_with_pre = self._make_xml(
            vol="10", num="2",
            doi="10.1590/abc123",
        )
        self.assertEqual(xml_with_pre.sps_pkg_name_suffix, "abc123")

    def test_sps_pkg_name_suffix_none(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        self.assertIsNone(xml_with_pre.sps_pkg_name_suffix)

    def test_alternative_sps_pkg_name_suffix_order(self):
        xml_with_pre = self._make_xml(vol="10", num="2", order="00001")
        self.assertEqual(xml_with_pre.alternative_sps_pkg_name_suffix, "00001")

    def test_alternative_sps_pkg_name_suffix_filename(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        xml_with_pre.filename = "article.xml"
        self.assertEqual(xml_with_pre.alternative_sps_pkg_name_suffix, "article.xml")


class TestV2List(XMLWithPreTestMixin, TestCase):
    """
    Testes para a nova property `v2_list`, que resolve o cenário de
    múltiplos PID v2 (article-id specific-use="scielo-v2") quando o
    artigo é publicado em mais de uma coleção SciELO, cada uma
    identificada pelo atributo `assigning-authority`:

    <article-id pub-id-type="publisher-id" specific-use="scielo-v2"
                assigning-authority="scielo-scl">S0103-65642009000300003</article-id>
    <article-id pub-id-type="publisher-id" specific-use="scielo-v2"
                assigning-authority="scielo-psi">S1678-51772009000300003</article-id>

    Mantém compatibilidade retroativa com o formato clássico (1 único
    scielo-v2, sem assigning-authority), representado na lista com
    "assigning-authority": None.
    """

    # -------- getter --------

    def test_v2_list_empty_when_absent(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        self.assertEqual(xml_with_pre.v2_list, [])

    def test_v2_list_classic_single_v2_backward_compatible(self):
        xml_with_pre = self._make_xml(
            vol="10", num="2",
            v2="S0101-01011999000100123",
        )
        self.assertEqual(
            xml_with_pre.v2_list,
            [{"assigning-authority": None, "pid": "S0101-01011999000100123"}],
        )
        # getter simples continua funcionando normalmente
        self.assertEqual(xml_with_pre.v2, "S0101-01011999000100123")

    def test_v2_list_multiple_collections(self):
        xml_with_pre = self._make_xml(
            vol="10", num="2",
            v2_items=[
                ("scielo-scl", "S0103-65642009000300003"),
                ("scielo-psi", "S1678-51772009000300003"),
            ],
        )
        self.assertEqual(
            xml_with_pre.v2_list,
            [
                {"assigning-authority": "scielo-scl", "pid": "S0103-65642009000300003"},
                {"assigning-authority": "scielo-psi", "pid": "S1678-51772009000300003"},
            ],
        )

    def test_v2_list_mixes_classic_and_collections(self):
        # cenário de transição: v2 clássico + v2 com assigning-authority
        xml_with_pre = self._make_xml(
            vol="10", num="2",
            v2="S0101-01011999000100123",
            v2_items=[("scielo-scl", "S0103-65642009000300003")],
        )
        self.assertEqual(
            xml_with_pre.v2_list,
            [
                {"assigning-authority": None, "pid": "S0101-01011999000100123"},
                {"assigning-authority": "scielo-scl", "pid": "S0103-65642009000300003"},
            ],
        )

    # -------- setter --------

    def test_v2_list_setter_creates_new_nodes(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        xml_with_pre.v2_list = [
            {"assigning-authority": "scielo-scl", "pid": "S0103-65642009000300003"},
            {"assigning-authority": "scielo-psi", "pid": "S1678-51772009000300003"},
        ]
        self.assertEqual(
            xml_with_pre.v2_list,
            [
                {"assigning-authority": "scielo-scl", "pid": "S0103-65642009000300003"},
                {"assigning-authority": "scielo-psi", "pid": "S1678-51772009000300003"},
            ],
        )

    def test_v2_list_setter_updates_existing_node_without_duplicating(self):
        xml_with_pre = self._make_xml(
            vol="10", num="2",
            v2_items=[("scielo-scl", "S0103-65642009000300003")],
        )
        xml_with_pre.v2_list = [
            {"assigning-authority": "scielo-scl", "pid": "S0103-65642009000300099"},
        ]
        self.assertEqual(
            xml_with_pre.v2_list,
            [{"assigning-authority": "scielo-scl", "pid": "S0103-65642009000300099"}],
        )
        nodes = xml_with_pre.xmltree.xpath(
            './/article-id[@specific-use="scielo-v2" and @assigning-authority="scielo-scl"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_v2_list_setter_updates_only_matching_authority(self):
        xml_with_pre = self._make_xml(
            vol="10", num="2",
            v2_items=[
                ("scielo-scl", "S0103-65642009000300003"),
                ("scielo-psi", "S1678-51772009000300003"),
            ],
        )
        xml_with_pre.v2_list = [
            {"assigning-authority": "scielo-scl", "pid": "S0103-65642009000300099"},
        ]
        self.assertEqual(
            xml_with_pre.v2_list,
            [
                {"assigning-authority": "scielo-scl", "pid": "S0103-65642009000300099"},
                {"assigning-authority": "scielo-psi", "pid": "S1678-51772009000300003"},
            ],
        )

    def test_v2_list_setter_backward_compatible_with_classic_v2(self):
        # atualizar via v2_list um XML clássico (sem assigning-authority)
        xml_with_pre = self._make_xml(
            vol="10", num="2",
            v2="S0101-01011999000100123",
        )
        xml_with_pre.v2_list = [
            {"assigning-authority": None, "pid": "S0101-01011999000199999"},
        ]
        self.assertEqual(xml_with_pre.v2, "S0101-01011999000199999")
        self.assertEqual(
            xml_with_pre.v2_list,
            [{"assigning-authority": None, "pid": "S0101-01011999000199999"}],
        )

    def test_v2_list_setter_adds_collection_to_classic_v2(self):
        # XML clássico recebendo um novo PID de outra coleção
        xml_with_pre = self._make_xml(
            vol="10", num="2",
            v2="S0101-01011999000100123",
        )
        xml_with_pre.v2_list = [
            {"assigning-authority": "scielo-scl", "pid": "S0103-65642009000300003"},
        ]
        self.assertEqual(
            xml_with_pre.v2_list,
            [
                {"assigning-authority": None, "pid": "S0101-01011999000100123"},
                {"assigning-authority": "scielo-scl", "pid": "S0103-65642009000300003"},
            ],
        )

    def test_v2_list_setter_empty_list_does_nothing(self):
        xml_with_pre = self._make_xml(
            vol="10", num="2",
            v2="S0101-01011999000100123",
        )
        xml_with_pre.v2_list = []
        self.assertEqual(
            xml_with_pre.v2_list,
            [{"assigning-authority": None, "pid": "S0101-01011999000100123"}],
        )

    def test_v2_list_setter_invalid_pid_length_raises(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        with self.assertRaises(ValueError):
            xml_with_pre.v2_list = [
                {"assigning-authority": "scielo-scl", "pid": "short"}
            ]

    def test_v2_list_setter_missing_pid_raises(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        with self.assertRaises(ValueError):
            xml_with_pre.v2_list = [{"assigning-authority": "scielo-scl"}]

    def test_v2_list_round_trip(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        original = [
            {"assigning-authority": "scielo-scl", "pid": "S0103-65642009000300003"},
            {"assigning-authority": "scielo-psi", "pid": "S1678-51772009000300003"},
        ]
        xml_with_pre.v2_list = original
        self.assertEqual(xml_with_pre.v2_list, original)


class TestXMLWithPrePropertiesAndMetadata(XMLWithPreTestMixin, TestCase):
    """Testes para aliases (filename, files, filenames), data e manipulação de DOCTYPE."""

    def test_filename_files_filenames_getters_and_setters(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        
        # Atribuição via setters
        xml_with_pre.filename = "artigo.xml"
        xml_with_pre.files = ["artigo.xml", "imagem.jpg"]
        xml_with_pre.filenames = ["artigo.xml", "imagem.jpg"]

        # Verificação via getters e propriedades de suporte
        self.assertEqual(xml_with_pre.filename, "artigo.xml")
        self.assertEqual(xml_with_pre.xml_name, "artigo.xml")

        self.assertEqual(xml_with_pre.files, ["artigo.xml", "imagem.jpg"])
        self.assertEqual(xml_with_pre.zip_namelist, ["artigo.xml", "imagem.jpg"])

        self.assertEqual(xml_with_pre.filenames, ["artigo.xml", "imagem.jpg"])
        self.assertEqual(xml_with_pre.zip_basenames, ["artigo.xml", "imagem.jpg"])

    def test_data_property(self):
        xml_with_pre = self._make_xml(
            vol="10",
            num="2",
            v2="S0101-01011999000100123",
            issn_epub="1234-5678",
            acron="abc",
            elocation="e100",
        )
        xml_with_pre.filename = "artigo.xml"
        xml_with_pre.files = ["artigo.xml"]
        xml_with_pre.filenames = ["artigo.xml"]

        data = xml_with_pre.data

        self.assertEqual(data["filename"], "artigo.xml")
        self.assertEqual(data["files"], ["artigo.xml"])
        self.assertEqual(data["filenames"], ["artigo.xml"])
        self.assertEqual(data["pid_v2"], "S0101-01011999000100123")
        self.assertIn("pkg_names", data)

    def test_parse_doctype_public_and_system_ids(self):
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.1 20151215//EN" "https://jats.nlm.nih.gov/publishing/1.1/JATS-journalpublishing1.dtd">
<article article-type="research-article" xml:lang="en">
  <front><journal-meta><journal-id journal-id-type="publisher-id">abc</journal-id></journal-meta></front>
</article>"""
        for xml_with_pre in XMLWithPre.create(xml_content=xml_content):
            self.assertIsNotNone(xml_with_pre.DOCTYPE)
            self.assertEqual(
                xml_with_pre.public_id,
                "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.1 20151215//EN",
            )
            self.assertEqual(
                xml_with_pre.system_id,
                "https://jats.nlm.nih.gov/publishing/1.1/JATS-journalpublishing1.dtd",
            )


class TestXMLWithPreArticleDataAndBody(XMLWithPreTestMixin, TestCase):
    """Testes para fragmento de corpo e resumo de dados do artigo."""

    def test_get_article_data(self):
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<article article-type="research-article" xml:lang="en">
  <front>
    <article-meta>
      <title-group>
        <article-title>Título do Artigo</article-title>
      </title-group>
      <contrib-group>
        <contrib contrib-type="author">
          <name><surname>Silva</surname><given-names>João</given-names></name>
        </contrib>
      </contrib-group>
    </article-meta>
  </front>
  <body>
    <p>Este é o texto do corpo do artigo para testes unitários.</p>
  </body>
</article>"""
        for xml_with_pre in XMLWithPre.create(xml_content=xml_content):
            article_data = xml_with_pre.get_article_data(max_body_fragment_length=20)
            
            self.assertEqual(article_data["surnames"], ["Silva"])
            self.assertIn("Título do Artigo", article_data["article_titles"])
            self.assertEqual(article_data["body_fragment"], "este é o texto do co")


class TestXMLWithPreSettersAndIDs(XMLWithPreTestMixin, TestCase):
    """Testes para alteração de order, v2, v3, aop_pid e update_ids."""

    def test_order_setter_success(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        xml_with_pre.order = "1"  # Deve formatar para '00001'
        self.assertEqual(xml_with_pre.order, "00001")

    def test_order_setter_invalid_raises_value_error(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        with self.assertRaises(ValueError):
            xml_with_pre.order = "123456"  # Mais que 5 caracteres

    def test_v2_v3_aop_pid_setters_and_update_ids(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        
        v2_val = "S0101-01011999000100123"
        v3_val = "12345678901234567890123"
        aop_val = "98765432109876543210987"

        xml_with_pre.update_ids(v3=v3_val, v2=v2_val, aop_pid=aop_val)

        self.assertEqual(xml_with_pre.v2, v2_val)
        self.assertEqual(xml_with_pre.v3, v3_val)
        self.assertEqual(xml_with_pre.aop_pid, aop_val)

    def test_invalid_pid_length_raises_value_error(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        with self.assertRaises(ValueError):
            xml_with_pre.v2 = "PID_CURTO"


class TestXMLWithPrePublicationDates(XMLWithPreTestMixin, TestCase):
    """Testes para consulta e modificação da data de publicação."""

    def test_set_article_publication_date_from_dict(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        nova_data = {"year": "2023", "month": "05", "day": "20"}
        
        xml_with_pre.article_publication_date = nova_data
        self.assertIn("2023", xml_with_pre.article_publication_date)

    def test_set_article_publication_date_from_string(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        xml_with_pre.article_publication_date = "2023-05-20"
        # self.assertIn("2023", xml_with_pre.article_publication_date)

    def test_set_invalid_article_publication_date_raises(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        with self.assertRaises(XMLWithPreArticlePublicationDateError):
            xml_with_pre.article_publication_date = "data-invalida"


class TestXMLWithPrePIDV2Generation(XMLWithPreTestMixin, TestCase):
    """Testes para geração dinâmica de PID v2."""

    def test_generated_pid_v2_sucesso(self):
        xml_with_pre = self._make_xml(
            issn_epub="1234-5678",
            vol="10",
            num="2",
            fpage="100",
        )

        with patch.object(xml_with_pre, "pub_year", "2023"):
            pid_v2 = xml_with_pre.generated_pid_v2()
            self.assertTrue(pid_v2.startswith("S1234-56782023"))
            self.assertEqual(len(pid_v2), 23)

    def test_generated_pid_v2_sem_issn_raises_value_error(self):
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<article article-type="research-article" xml:lang="en">
  <front><journal-meta></journal-meta></front>
</article>"""
        for xml_with_pre in XMLWithPre.create(xml_content=xml_content):
            with self.assertRaises(ValueError):
                xml_with_pre.generated_pid_v2()


if __name__ == "__main__":
    import unittest
    unittest.main()