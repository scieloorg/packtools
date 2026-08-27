import os
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch
from zipfile import ZipFile, ZIP_DEFLATED

from packtools.sps.pid_provider.xml_sps_lib import (
    XMLWithPre,
    XMLWithPreArticlePublicationDateError,
    XMLWithPreMissingISSNError,
    GetXmlWithPreError,
    get_xml_with_pre_from_xml_file,
    get_xml_with_pre_from_zip_file,
    generate_finger_print,
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

    def _make_base_xml(self):
        """
        Configuração canônica usada nos testes de dicionário: ISSN eletrônico
        único, sem suplemento/fpage/lpage/order/submitted_filename — produz
        valores 100% determinísticos para sps_pkg_name, pkg_name_variations,
        get_pmc_pkg_name etc.
        """
        return self._make_xml(
            issn_epub="1234-5678",
            acron="abc",
            vol="10",
            num="2",
            elocation="e12345",
        )
 

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

    def test_incorrect_sps_pkg_name_suppl_none(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        self.assertIsNone(xml_with_pre.incorrect_sps_pkg_name_suppl)

    def test_incorrect_sps_pkg_name_suppl_zero(self):
        xml_with_pre = self._make_xml(vol="10", num="2", suppl="0")
        self.assertEqual(xml_with_pre.incorrect_sps_pkg_name_suppl, "suppl")

    def test_incorrect_sps_pkg_name_suppl_numeric(self):
        xml_with_pre = self._make_xml(vol="10", num="2", suppl="1")
        self.assertEqual(xml_with_pre.incorrect_sps_pkg_name_suppl, "1")

    def test_incorrect_sps_pkg_name_suppl_text(self):
        xml_with_pre = self._make_xml(vol="10", num="2", suppl="A")
        self.assertEqual(xml_with_pre.incorrect_sps_pkg_name_suppl, "A")


class TestSPSPkgNameFpage(XMLWithPreTestMixin, TestCase):
    """Testes para sps_pkg_name_fpage e deprecated_sps_pkg_name_fpage"""

    def test_sps_pkg_name_fpage_none(self):
        xml_with_pre = self._make_xml(vol="10", num="2", elocation="e123")
        self.assertIsNone(xml_with_pre.fpage)
        self.assertIsNone(xml_with_pre.legacy_sps_pkg_name_fpage)

    def test_sps_pkg_name_fpage_zero(self):
        xml_with_pre = self._make_xml(vol="10", num="2", fpage="0", lpage="0")
        self.assertIsNone(xml_with_pre.fpage)
        self.assertIsNone(xml_with_pre.legacy_sps_pkg_name_fpage)

    def test_sps_pkg_name_fpage_simple(self):
        xml_with_pre = self._make_xml(vol="10", num="2", fpage="123", lpage="130")
        self.assertEqual(xml_with_pre.fpage, "123")
        self.assertEqual(xml_with_pre.legacy_sps_pkg_name_fpage, "123")

    def test_sps_pkg_name_fpage_with_seq(self):
        xml_with_pre = self._make_xml(vol="10", num="2", fpage="123", fpage_seq="a", lpage="130")
        self.assertEqual(xml_with_pre.fpage, "123")
        self.assertEqual(xml_with_pre.fpage_seq, "a")
        self.assertEqual(xml_with_pre.legacy_sps_pkg_name_fpage, "123_a")

    def test_sps_pkg_name_fpage_same_fpage_lpage_with_v2(self):
        xml_with_pre = self._make_xml(
            vol="10", num="2", fpage="123", lpage="123",
            v2="S0101-01011999000100123"
        )
        self.assertEqual(xml_with_pre.fpage, "123")
        self.assertEqual(xml_with_pre.lpage, "123")
        self.assertEqual(xml_with_pre.legacy_sps_pkg_name_fpage, "123_00123")

    def test_sps_pkg_name_fpage_same_fpage_lpage_without_v2(self):
        xml_with_pre = self._make_xml(vol="10", num="2", fpage="123", lpage="123")
        self.assertEqual(xml_with_pre.fpage, "123")
        self.assertEqual(xml_with_pre.lpage, "123")
        self.assertEqual(xml_with_pre.legacy_sps_pkg_name_fpage, "123")

    def test_sps_pkg_name_fpage_alphanumeric(self):
        xml_with_pre = self._make_xml(vol="10", num="2", fpage="e123", lpage="e130")
        self.assertEqual(xml_with_pre.fpage, "e123")
        self.assertEqual(xml_with_pre.legacy_sps_pkg_name_fpage, "e123")

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
        self.assertEqual(xml_with_pre.sps_pkg_name, "1234-5678-abc-10-02-s1-100")

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
                "1234-5678-abc-10-02-s1-100_110",                              
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
            xml_with_pre.sps_pkg_name, "1234-5678-abc-10-02-100"
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
            xml_with_pre.sps_pkg_name, "1234-5678-abc-10-02-s1-100"
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
            xml_with_pre.sps_pkg_name, "1234-5678-abc-10-02-e100"
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
            xml_with_pre.sps_pkg_name, "1234-5678-abc-10-02-e100"
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
            xml_with_pre.sps_pkg_name, "1234-5678-abc-10-02-e100"
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
            xml_with_pre.sps_pkg_name, "1234-5678-abc-10-02-e100"
        )


class TestLegacySPSPkgName(XMLWithPreTestMixin, TestCase):
    """Testes para sps_pkg_name e deprecated_sps_pkg_name"""

    def test_deprecated_v3_sps_pkg_name_complete(self):
        xml_with_pre = self._make_xml(
            issn_epub="1234-5678",
            issn_ppub="8765-4321",
            acron="abc",
            vol="10",
            num="2",
            elocation="e12345",
        )
        self.assertEqual(xml_with_pre.deprecated_sps_pkg_name_version_3, "1234-5678-abc-10-02-e12345")

    def test_deprecated_v3_sps_pkg_name_with_suppl(self):
        xml_with_pre = self._make_xml(
            issn_epub="1234-5678",
            acron="abc",
            vol="10",
            num="2",
            suppl="1",
            fpage="100",
            lpage="110",
        )
        self.assertEqual(xml_with_pre.deprecated_sps_pkg_name_version_3, "1234-5678-abc-10-02-s1-100_110")

    def test_deprecated_v3_sps_pkg_name_ppub_fallback(self):
        xml_with_pre = self._make_xml(
            issn_ppub="8765-4321",
            acron="xyz",
            vol="5",
            elocation="e001",
        )
        self.assertEqual(xml_with_pre.deprecated_sps_pkg_name_version_3, "8765-4321-xyz-5-e001")

    def test_deprecated_v3_sps_pkg_name_no_volume_no_number(self):
        xml_with_pre = self._make_xml(
            issn_epub="1111-2222",
            acron="rev",
            elocation="e999",
        )
        self.assertEqual(xml_with_pre.deprecated_sps_pkg_name_version_3, "1111-2222-rev-e999")

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
                "1234-5678-abc-10-02-s1-100_110"
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

    def test_deprecated_v3_sps_pkg_name_with_xml_source_filename_bypasses_computation(self):
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
        self.assertEqual(xml_with_pre.deprecated_sps_pkg_name_version_3, "1234-5678-abc-10-02-s1-100")

    def test_deprecated_v3_sps_pkg_name_with_xml_source_filename_bypasses_even_without_metadata(self):
        # mesmo sem volume/numero/issn, com extensão .xml o nome do
        # pacote é o próprio source_filename (sem extensão)
        xml_with_pre = self._make_xml()
        xml_with_pre.add_pkg_name_components("1234-5678-abc-10-02-s1-100.xml")
        self.assertEqual(xml_with_pre.deprecated_sps_pkg_name_version_3, "1234-5678-abc-10-02-s1-100")

    def test_deprecated_v3_sps_pkg_name_with_htm_source_filename_appends_as_suffix(self):
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
            xml_with_pre.deprecated_sps_pkg_name_version_3, "1234-5678-abc-10-02-100_110_1989"
        )

    def test_deprecated_v3_sps_pkg_name_with_htm_source_filename_and_suppl(self):
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
            xml_with_pre.deprecated_sps_pkg_name_version_3, "1234-5678-abc-10-02-s1-100_110_1989"
        )

    # -------- sps_pkg_name com order e/ou v2 --------
    # get_pkg_name_suffix inclui `self.order or self.v2 and self.v2[-5:]`
    # como parte do sufixo: order tem precedência sobre os 5 últimos
    # dígitos do v2 quando ambos estão presentes.

    def test_deprecated_v3_sps_pkg_name_without_order_and_without_v2(self):
        xml_with_pre = self._make_xml(
            issn_epub="1234-5678",
            acron="abc",
            vol="10",
            num="2",
            elocation="e100",
        )
        self.assertEqual(xml_with_pre.deprecated_sps_pkg_name_version_3, "1234-5678-abc-10-02-e100")

    def test_deprecated_v3_sps_pkg_name_with_order_only(self):
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
            xml_with_pre.deprecated_sps_pkg_name_version_3, "1234-5678-abc-10-02-e100_00001"
        )

    def test_deprecated_v3_sps_pkg_name_with_v2_only(self):
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
            xml_with_pre.deprecated_sps_pkg_name_version_3, "1234-5678-abc-10-02-e100_00123"
        )

    def test_deprecated_v3_sps_pkg_name_with_order_and_v2_order_takes_precedence(self):
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
            xml_with_pre.deprecated_sps_pkg_name_version_3, "1234-5678-abc-10-02-e100_00001"
        )

    def test_deprecated_v3_sps_pkg_name_with_order_v2_and_htm_source_filename(self):
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
            xml_with_pre.deprecated_sps_pkg_name_version_3, "1234-5678-abc-10-02-e100_00001_1989"
        )


class TestSPSPkgNameSuffix(XMLWithPreTestMixin, TestCase):
    """Testes para sps_pkg_name_suffix e legacy_alternative_sps_pkg_name_suffix"""

    def test_sps_pkg_name_suffix_elocation_id(self):
        xml_with_pre = self._make_xml(
            vol="10", num="2",
            elocation="e12345",
            fpage="100", lpage="110",
            doi="10.1590/1234",
        )
        self.assertEqual(xml_with_pre.legacy_sps_pkg_name_suffix, "e12345")

    def test_sps_pkg_name_suffix_fpage(self):
        xml_with_pre = self._make_xml(
            vol="10", num="2",
            fpage="100", lpage="110",
            doi="10.1590/1234",
        )
        self.assertEqual(xml_with_pre.legacy_sps_pkg_name_suffix, "100")

    def test_sps_pkg_name_suffix_doi(self):
        xml_with_pre = self._make_xml(
            vol="10", num="2",
            doi="10.1590/0001-3714.2020.v1.n2.1234",
        )
        self.assertEqual(xml_with_pre.legacy_sps_pkg_name_suffix, "0001-3714-2020-v1-n2-1234")

    def test_sps_pkg_name_suffix_doi_simple(self):
        xml_with_pre = self._make_xml(
            vol="10", num="2",
            doi="10.1590/abc123",
        )
        self.assertEqual(xml_with_pre.legacy_sps_pkg_name_suffix, "abc123")

    def test_sps_pkg_name_suffix_none(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        self.assertIsNone(xml_with_pre.legacy_sps_pkg_name_suffix)

    def test_legacy_alternative_sps_pkg_name_suffix_order(self):
        xml_with_pre = self._make_xml(vol="10", num="2", order="00001")
        self.assertEqual(xml_with_pre.legacy_alternative_sps_pkg_name_suffix, "00001")

    def test_legacy_alternative_sps_pkg_name_suffix_filename(self):
        # legacy_alternative_sps_pkg_name_suffix cai para `filename` quando
        # não há `order`. `filename` NÃO tem setter: é sempre derivado de
        # xml_name (via add_xml_info) — aqui, sem zip_file_path, filename ==
        # f"{xml_name}.xml".
        xml_with_pre = self._make_xml(vol="10", num="2")
        xml_with_pre.add_xml_info("article")
        self.assertIsNone(xml_with_pre.order)
        self.assertEqual(xml_with_pre.xml_name, "article")
        self.assertEqual(xml_with_pre.filename, "article.xml")
        self.assertEqual(xml_with_pre.legacy_alternative_sps_pkg_name_suffix, "article.xml")


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
    """Testes para aliases (files, filenames), data e manipulação de DOCTYPE.

    `filename` (singular) NÃO possui setter — é sempre derivado de
    xml_name/xml_file_path/zip_file_path, atribuídos via add_xml_info /
    add_zip_info. Já `files`/`filenames` (plural) SÃO aliases graváveis
    para zip_namelist/zip_basenames.
    """

    def test_files_and_filenames_getters_and_setters(self):
        xml_with_pre = self._make_xml(vol="10", num="2")

        # Atribuição via setters (aliases de zip_namelist/zip_basenames)
        xml_with_pre.files = ["artigo.xml", "imagem.jpg"]
        xml_with_pre.filenames = ["artigo.xml", "imagem.jpg"]

        self.assertEqual(xml_with_pre.files, ["artigo.xml", "imagem.jpg"])
        self.assertEqual(xml_with_pre.zip_namelist, ["artigo.xml", "imagem.jpg"])

        self.assertEqual(xml_with_pre.filenames, ["artigo.xml", "imagem.jpg"])
        self.assertEqual(xml_with_pre.zip_basenames, ["artigo.xml", "imagem.jpg"])

    def test_filename_singular_has_no_setter(self):
        # `filename` é somente leitura; tentar atribuí-lo diretamente
        # deve falhar (não existe filename.setter no código-fonte).
        xml_with_pre = self._make_xml(vol="10", num="2")
        with self.assertRaises(AttributeError):
            xml_with_pre.filename = "artigo.xml"

    def test_filename_getter_uses_xml_name_when_set_via_add_xml_info(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        xml_with_pre.add_xml_info("artigo", "/tmp/uploads/artigo.xml")
        self.assertEqual(xml_with_pre.xml_name, "artigo")
        # sem zip_file_path, filename ignora o path completo do arquivo e
        # usa somente xml_name + ".xml"
        self.assertEqual(xml_with_pre.filename, "artigo.xml")

    def test_data_property(self):
        xml_with_pre = self._make_xml(
            vol="10",
            num="2",
            v2="S0101-01011999000100123",
            issn_epub="1234-5678",
            acron="abc",
            elocation="e100",
        )
        xml_with_pre.add_xml_info("artigo")
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


# ==============================================================================
# submitted_filename / source_filename / source_ext
# ==============================================================================
class TestSubmittedFilename(XMLWithPreTestMixin, TestCase):

    def test_submitted_filename_setter_splits_name_and_lowercases_extension(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        xml_with_pre.submitted_filename = "artigo.XML"
        self.assertEqual(xml_with_pre._submitted_filename, "artigo")
        self.assertEqual(xml_with_pre._submitted_ext, ".xml")
        self.assertEqual(xml_with_pre.submitted_filename, "artigo.xml")

    def test_submitted_filename_getter_none_when_not_set(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        self.assertIsNone(xml_with_pre.submitted_filename)
        self.assertIsNone(xml_with_pre.submitted_ext)

    def test_submitted_filename_setter_none_clears_name_and_ext(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        xml_with_pre.submitted_filename = "artigo.xml"
        xml_with_pre.submitted_filename = None
        self.assertIsNone(xml_with_pre._submitted_filename)
        self.assertIsNone(xml_with_pre._submitted_ext)
        self.assertIsNone(xml_with_pre.submitted_filename)

    def test_submitted_filename_setter_empty_string_clears_name_and_ext(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        xml_with_pre.submitted_filename = "artigo.xml"
        xml_with_pre.submitted_filename = ""
        self.assertIsNone(xml_with_pre._submitted_filename)
        self.assertIsNone(xml_with_pre.submitted_filename)

    def test_submitted_filename_without_extension_keeps_previous_extension(self):
        # Comportamento sutil: se o novo valor não tem extensão, a extensão
        # anterior é mantida (o setter só atualiza _submitted_ext quando
        # `ext` é verdadeiro).
        xml_with_pre = self._make_xml(vol="10", num="2")
        xml_with_pre.submitted_filename = "artigo.xml"
        xml_with_pre.submitted_filename = "outro_nome_sem_extensao"
        self.assertEqual(xml_with_pre._submitted_filename, "outro_nome_sem_extensao")
        self.assertEqual(xml_with_pre._submitted_ext, ".xml")
        self.assertEqual(xml_with_pre.submitted_filename, "outro_nome_sem_extensao.xml")

    def test_source_filename_and_source_ext_aliases(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        xml_with_pre.source_filename = "documento.pdf"
        self.assertEqual(xml_with_pre.source_filename, "documento")
        self.assertEqual(xml_with_pre.source_ext, ".pdf")
        # o getter "cheio" (submitted_filename) reconstrói nome + extensão
        self.assertEqual(xml_with_pre.submitted_filename, "documento.pdf")

    def test_source_ext_setter_direct(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        xml_with_pre.source_filename = "documento.pdf"
        xml_with_pre.source_ext = ".xml"
        self.assertEqual(xml_with_pre.source_ext, ".xml")
        self.assertEqual(xml_with_pre.submitted_filename, "documento.xml")

    def test_is_html_source_true_for_html_and_htm(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        xml_with_pre.submitted_filename = "pagina.html"
        self.assertTrue(xml_with_pre.is_html_source)

        xml_with_pre.submitted_filename = "outra.htm"
        self.assertTrue(xml_with_pre.is_html_source)

    def test_is_html_source_false_for_xml(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        xml_with_pre.submitted_filename = "artigo.xml"
        self.assertFalse(xml_with_pre.is_html_source)

    def test_is_html_source_false_when_no_extension_set(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        self.assertFalse(xml_with_pre.is_html_source)


# ==============================================================================
# add_pkg_name_components
# ==============================================================================
class TestAddPkgNameComponentsExtended(XMLWithPreTestMixin, TestCase):

    def test_add_pkg_name_components_with_xml_sets_provided_sps_pkg_name(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        xml_with_pre.add_pkg_name_components("1234-5678-abc-10-02-e100.xml")
        self.assertEqual(xml_with_pre.provided_sps_pkg_name, "1234-5678-abc-10-02-e100")
        # sps_pkg_name deve retornar diretamente o valor "provided", sem
        # nenhum cálculo adicional baseado em issn/acron/volume/etc.
        self.assertEqual(xml_with_pre.sps_pkg_name, "1234-5678-abc-10-02-e100")

    def test_add_pkg_name_components_with_non_xml_extension_does_not_set_provided_name(self):
        xml_with_pre = self._make_xml(
            issn_epub="1234-5678", acron="abc", vol="10", num="2", elocation="e100"
        )
        xml_with_pre.add_pkg_name_components("1989.htm")
        self.assertIsNone(xml_with_pre.provided_sps_pkg_name)
        self.assertEqual(xml_with_pre.source_filename, "1989")
        self.assertEqual(xml_with_pre.source_ext, ".htm")
        # sem provided/built, cai no fallback deprecated_sps_pkg_name_version_2
        self.assertEqual(xml_with_pre.sps_pkg_name, xml_with_pre.deprecated_sps_pkg_name_version_2)

    def test_add_pkg_name_components_with_underscore_in_xml_name_keeps_legacy_name(self):
        # "_" não segue o padrão SPS (sanitize_sps_name trocaria por "-"),
        # mas por ser um nome legado o valor original é preservado em vez
        # de lançar ValueError.
        xml_with_pre = self._make_xml(vol="10", num="2")
        xml_with_pre.add_pkg_name_components("1234_5678_abc.xml")
        self.assertEqual(xml_with_pre.provided_sps_pkg_name, "1234_5678_abc")
        self.assertEqual(xml_with_pre.sps_pkg_name, "1234_5678_abc")

    def test_add_pkg_name_components_with_extra_dot_before_xml_ext_keeps_legacy_name(self):
        # "1234-5678.v2.xml" -> remove apenas os últimos 4 caracteres (".xml"),
        # sobrando "1234-5678.v2", que contém "." e seria alterado por
        # sanitize_sps_name ("1234-5678-v2"); como é legado, o valor original
        # com ponto é mantido.
        xml_with_pre = self._make_xml(vol="10", num="2")
        xml_with_pre.add_pkg_name_components("1234-5678.v2.xml")
        self.assertEqual(xml_with_pre.provided_sps_pkg_name, "1234-5678.v2")
        self.assertEqual(xml_with_pre.sps_pkg_name, "1234-5678.v2")

    def test_add_pkg_name_components_with_extra_dot_and_non_xml_ext_is_allowed(self):
        # Mesmo nome com pontos, mas extensão diferente de ".xml": não passa
        # pela validação de provided_sps_pkg_name, então não há erro.
        xml_with_pre = self._make_xml(vol="10", num="2")
        xml_with_pre.add_pkg_name_components("1234-5678.v2.htm")
        self.assertIsNone(xml_with_pre.provided_sps_pkg_name)
        self.assertEqual(xml_with_pre.source_filename, "1234-5678.v2")
        self.assertEqual(xml_with_pre.source_ext, ".htm")

    def test_add_pkg_name_components_overwrites_previous_call(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        xml_with_pre.add_pkg_name_components("primeiro-nome.xml")
        self.assertEqual(xml_with_pre.provided_sps_pkg_name, "primeiro-nome")

        xml_with_pre.add_pkg_name_components("segundo-nome.xml")
        self.assertEqual(xml_with_pre.provided_sps_pkg_name, "segundo-nome")
        self.assertEqual(xml_with_pre.submitted_filename, "segundo-nome.xml")

    def test_add_pkg_name_components_sets_pkg_name_version_attribute(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        self.assertIsNone(xml_with_pre.pkg_name_version)
        xml_with_pre.add_pkg_name_components("artigo.xml", pkg_name_version=2)
        self.assertEqual(xml_with_pre.pkg_name_version, 2)


# ==============================================================================
# sps_pkg_name (precedência provided > built > deprecated_v2)
# ==============================================================================
class TestSpsPkgNamePriority(XMLWithPreTestMixin, TestCase):

    def test_sps_pkg_name_falls_back_to_deprecated_version_2_by_default(self):
        xml_with_pre = self._make_xml(
            issn_epub="1234-5678", acron="abc", vol="10", num="2", fpage="100", lpage="110"
        )
        self.assertIsNone(xml_with_pre.provided_sps_pkg_name)
        self.assertIsNone(xml_with_pre.built_sps_pkg_name)
        self.assertEqual(xml_with_pre.sps_pkg_name, xml_with_pre.deprecated_sps_pkg_name_version_2)

    def test_sps_pkg_name_prefers_provided_over_built(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        xml_with_pre._built_sps_pkg_name = "built-name"
        xml_with_pre.provided_sps_pkg_name = "provided-name"
        self.assertEqual(xml_with_pre.sps_pkg_name, "provided-name")

    def test_sps_pkg_name_uses_built_when_no_provided(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        xml_with_pre._built_sps_pkg_name = "built-name"
        self.assertIsNone(xml_with_pre.provided_sps_pkg_name)
        self.assertEqual(xml_with_pre.sps_pkg_name, "built-name")

    def test_sps_pkg_name_setter_sets_provided_name(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        xml_with_pre.provided_sps_pkg_name = "meu-pacote-1"
        self.assertEqual(xml_with_pre.provided_sps_pkg_name, "meu-pacote-1")
        self.assertEqual(xml_with_pre.sps_pkg_name, "meu-pacote-1")

    def test_provided_sps_pkg_name_setter_keeps_legacy_name_when_sanitize_differs(self):
        # Nome fora do padrão SPS (contém "_" e "."), mas tratado como
        # legado: o valor original é preservado em vez de lançar ValueError.
        xml_with_pre = self._make_xml(vol="10", num="2")
        xml_with_pre.provided_sps_pkg_name = "nome_invalido.com"
        self.assertEqual(xml_with_pre.provided_sps_pkg_name, "nome_invalido.com")

    def test_provided_sps_pkg_name_setter_keeps_sanitized_value_when_already_valid(self):
        # Quando o valor já está no padrão SPS, sanitize_sps_name não altera
        # nada e o valor é aceito normalmente (sem passar pelo caminho de
        # "nome legado").
        xml_with_pre = self._make_xml(vol="10", num="2")
        xml_with_pre.provided_sps_pkg_name = "nome-valido-123"
        self.assertEqual(xml_with_pre.provided_sps_pkg_name, "nome-valido-123")

    def test_provided_sps_pkg_name_setter_none_clears_value(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        xml_with_pre.provided_sps_pkg_name = "nome-valido"
        xml_with_pre.provided_sps_pkg_name = None
        self.assertIsNone(xml_with_pre.provided_sps_pkg_name)


# ==============================================================================
# build_sps_pkg_name
# ==============================================================================
class TestBuildSpsPkgName(XMLWithPreTestMixin, TestCase):

    def test_build_sps_pkg_name_using_elocation_id(self):
        xml_with_pre = self._make_xml(
            issn_epub="1234-5678", acron="abc", vol="10", num="2", elocation="e100"
        )
        self.assertEqual(xml_with_pre.build_sps_pkg_name(), "1234-5678-abc-10-02-e100")

    def test_build_sps_pkg_name_uses_order_when_no_elocation(self):
        xml_with_pre = self._make_xml(
            issn_epub="1234-5678", acron="abc", vol="10", num="2", order="00007"
        )
        self.assertEqual(xml_with_pre.build_sps_pkg_name(), "1234-5678-abc-10-02-00007")

    def test_build_sps_pkg_name_uses_submitted_filename_when_no_elocation_or_order(self):
        xml_with_pre = self._make_xml(
            issn_epub="1234-5678", acron="abc", vol="10", num="2"
        )
        xml_with_pre.submitted_filename = "MeuArquivo.xml"
        self.assertEqual(xml_with_pre.build_sps_pkg_name(), "1234-5678-abc-10-02-meuarquivo")

    def test_build_sps_pkg_name_elocation_takes_precedence_over_order(self):
        xml_with_pre = self._make_xml(
            issn_epub="1234-5678", acron="abc", vol="10", num="2",
            elocation="e100", order="00007",
        )
        self.assertEqual(xml_with_pre.build_sps_pkg_name(), "1234-5678-abc-10-02-e100")

    def test_build_sps_pkg_name_order_takes_precedence_over_submitted_filename(self):
        xml_with_pre = self._make_xml(
            issn_epub="1234-5678", acron="abc", vol="10", num="2", order="00007"
        )
        xml_with_pre.submitted_filename = "MeuArquivo.xml"
        self.assertEqual(xml_with_pre.build_sps_pkg_name(), "1234-5678-abc-10-02-00007")

    def test_build_sps_pkg_name_with_custom_issn(self):
        xml_with_pre = self._make_xml(
            issn_epub="1234-5678", issn_ppub="8765-4321",
            acron="abc", vol="10", num="2", elocation="e100",
        )
        self.assertEqual(
            xml_with_pre.build_sps_pkg_name(issn="8765-4321"),
            "8765-4321-abc-10-02-e100",
        )

    def test_build_sps_pkg_name_with_lang_suffix_when_different_from_main_lang(self):
        # o XML gerado pelo mixin de testes usa xml:lang="en"
        xml_with_pre = self._make_xml(
            issn_epub="1234-5678", acron="abc", vol="10", num="2", elocation="e100"
        )
        self.assertEqual(
            xml_with_pre.build_sps_pkg_name(lang="pt"), "1234-5678-abc-10-02-e100-pt"
        )

    def test_build_sps_pkg_name_no_lang_suffix_when_same_as_main_lang(self):
        xml_with_pre = self._make_xml(
            issn_epub="1234-5678", acron="abc", vol="10", num="2", elocation="e100"
        )
        self.assertEqual(
            xml_with_pre.build_sps_pkg_name(lang="en"), "1234-5678-abc-10-02-e100"
        )

    def test_build_sps_pkg_name_missing_issn_raises(self):
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<article article-type="research-article" xml:lang="en">
  <front>
    <journal-meta>
      <journal-id journal-id-type="publisher-id">abc</journal-id>
    </journal-meta>
    <article-meta>
      <volume>10</volume>
      <issue>2</issue>
      <elocation-id>e100</elocation-id>
    </article-meta>
  </front>
</article>"""
        for xml_with_pre in XMLWithPre.create(xml_content=xml_content):
            with self.assertRaises(XMLWithPreMissingISSNError):
                xml_with_pre.build_sps_pkg_name()

    def test_build_sps_pkg_name_missing_suffix_raises_value_error(self):
        # sem elocation_id, order ou submitted_filename disponíveis, nenhuma
        # das estratégias padrão de build_sps_pkg_name produz um sufixo válido
        xml_with_pre = self._make_xml(
            issn_epub="1234-5678", acron="abc", vol="10", num="2"
        )
        with self.assertRaises(ValueError):
            xml_with_pre.build_sps_pkg_name()

"""
Testes complementares para packtools.sps.pid_provider.xml_sps_lib.XMLWithPre

Foco:
    - sps_pkg_name_origin
    - provided_sps_pkg_name (setter sem sanitização — nomes legados)
    - get_pmc_pkg_name (com e sem revision_number)
    - pkg_names_dict / sps_pkg_names_dict / input_files_dict / data
    - get_data (composição condicional dos dicionários acima)
    - xml_name vs filename conforme a origem (arquivo .xml avulso x .zip)

Arquivo independente (contém sua própria mixin de fabricação de XML).
"""
# ==============================================================================
# sps_pkg_name_origin
# ==============================================================================
class TestSpsPkgNameOrigin(XMLWithPreTestMixin, TestCase):

    def test_origin_is_deprecated_version_2_by_default(self):
        xml_with_pre = self._make_base_xml()
        self.assertIsNone(xml_with_pre.provided_sps_pkg_name)
        self.assertIsNone(xml_with_pre.built_sps_pkg_name)
        self.assertIsNone(xml_with_pre.xml_name)                
        self.assertEqual(xml_with_pre.sps_pkg_name_origin, "deprecated_sps_pkg_name_version_2")

    def test_origin_is_built_when_built_name_is_set(self):
        xml_with_pre = self._make_base_xml()
        xml_with_pre.built_sps_pkg_name = "built-name"
        self.assertEqual(xml_with_pre.sps_pkg_name_origin, "built_sps_pkg_name")

    def test_origin_is_provided_when_provided_name_is_set(self):
        xml_with_pre = self._make_base_xml()
        xml_with_pre.provided_sps_pkg_name = "provided-name"
        self.assertEqual(xml_with_pre.sps_pkg_name_origin, "provided_sps_pkg_name")

    def test_origin_provided_takes_precedence_over_built(self):
        xml_with_pre = self._make_base_xml()
        xml_with_pre._built_sps_pkg_name = "built-name"
        xml_with_pre.provided_sps_pkg_name = "provided-name"
        self.assertEqual(xml_with_pre.sps_pkg_name_origin, "provided_sps_pkg_name")
        # sps_pkg_name e sps_pkg_name_origin devem ser sempre consistentes
        self.assertEqual(xml_with_pre.sps_pkg_name, "provided-name")

    def test_origin_is_xml_name_when_only_xml_name_is_set(self):
        # xml_name é atribuído via add_xml_info (não confundir com
        # provided_sps_pkg_name / built_sps_pkg_name)
        xml_with_pre = self._make_base_xml()
        xml_with_pre.add_xml_info("nome-do-arquivo")
        self.assertIsNone(xml_with_pre.provided_sps_pkg_name)
        self.assertIsNone(xml_with_pre.built_sps_pkg_name)
        self.assertEqual(xml_with_pre.xml_name, "nome-do-arquivo")
        self.assertEqual(xml_with_pre.sps_pkg_name_origin, "xml_name")
        self.assertEqual(xml_with_pre.sps_pkg_name, "nome-do-arquivo")


# ==============================================================================
# provided_sps_pkg_name: setter não sanitiza mais (nomes legados)
# ==============================================================================
class TestProvidedSpsPkgNameLegacyBehavior(XMLWithPreTestMixin, TestCase):

    def test_setter_keeps_value_as_is_even_with_characters_invalid_for_sps(self):
        # "_" e "." não são permitidos pelo padrão SPS estrito (ver
        # sanitize_sps_name), mas o setter atual não valida/sanitiza mais,
        # justamente para preservar nomes legados de pacotes antigos.
        xml_with_pre = self._make_base_xml()
        xml_with_pre.provided_sps_pkg_name = "nome_legado.v2"
        self.assertEqual(xml_with_pre.provided_sps_pkg_name, "nome_legado.v2")
        self.assertEqual(xml_with_pre.sps_pkg_name, "nome_legado.v2")

    def test_setter_none_clears_value(self):
        xml_with_pre = self._make_base_xml()
        xml_with_pre.provided_sps_pkg_name = "nome-valido"
        xml_with_pre.provided_sps_pkg_name = None
        self.assertIsNone(xml_with_pre.provided_sps_pkg_name)

    def test_setter_empty_string_clears_value(self):
        xml_with_pre = self._make_base_xml()
        xml_with_pre.provided_sps_pkg_name = "nome-valido"
        xml_with_pre.provided_sps_pkg_name = ""
        self.assertIsNone(xml_with_pre.provided_sps_pkg_name)


# ==============================================================================
# get_pmc_pkg_name
# ==============================================================================
class TestGetPmcPkgName(XMLWithPreTestMixin, TestCase):

    def test_get_pmc_pkg_name_without_revision(self):
        xml_with_pre = self._make_base_xml()
        # acron-vol-iss-uid ; iss NÃO é zero-padded aqui (diferente do prefixo SPS)
        self.assertEqual(xml_with_pre.get_pmc_pkg_name(), "abc-10-2-e12345")

    def test_get_pmc_pkg_name_with_revision_number(self):
        # ATENÇÃO: sanitize_name remove o "." do sufixo ".r{n}" (ele não é um
        # caractere permitido), então o resultado final NÃO preserva o ponto
        # entre o uid e o "r{n}" — comportamento atual, possivelmente não
        # intencional, documentado aqui.
        xml_with_pre = self._make_base_xml()
        self.assertEqual(xml_with_pre.get_pmc_pkg_name(revision_number=2), "abc-10-2-e12345r2")

    def test_get_pmc_pkg_name_with_revision_number_falsy_is_ignored(self):
        xml_with_pre = self._make_base_xml()
        self.assertEqual(xml_with_pre.get_pmc_pkg_name(revision_number=0), "abc-10-2-e12345")


# ==============================================================================
# data / input_files_dict / pkg_names_dict / sps_pkg_names_dict
# ==============================================================================
class TestDictProperties(XMLWithPreTestMixin, TestCase):

    def test_data_contains_only_expected_keys(self):
        xml_with_pre = self._make_base_xml()
        data = xml_with_pre.data
        self.assertEqual(
            set(data.keys()),
            {
                "sps_pkg_name",
                "pid_v3",
                "pid_v2",
                "aop_pid",
                "filename",
                "files",
                "filenames",
                "pkg_names",
            },
        )

    def test_data_values_for_base_xml(self):
        xml_with_pre = self._make_base_xml()
        data = xml_with_pre.data
        self.assertEqual(data["sps_pkg_name"], "1234-5678-abc-10-02-e12345")
        self.assertIsNone(data["pid_v3"])
        self.assertIsNone(data["pid_v2"])
        self.assertIsNone(data["aop_pid"])
        self.assertIsNone(data["filename"])
        self.assertIsNone(data["files"])
        self.assertIsNone(data["filenames"])
        # sem fpage/lpage/suppl, as 3 variações deprecated coincidem
        self.assertEqual(
            data["pkg_names"],
            [
                "1234-5678-abc-10-02-e12345",
                "1234-5678-abc-10-02-e12345",
                "1234-5678-abc-10-02-e12345",
            ],
        )

    def test_data_no_longer_contains_submitted_filename_or_xml_name(self):
        # Esses campos migraram para input_files_dict; garantir que não
        # "vazam" de volta para `data` por engano em uma futura refatoração.
        xml_with_pre = self._make_base_xml()
        xml_with_pre.submitted_filename = "artigo.xml"
        xml_with_pre.add_xml_info("artigo")
        data = xml_with_pre.data
        self.assertNotIn("submitted_filename", data)
        self.assertNotIn("submitted_ext", data)
        self.assertNotIn("xml_name", data)
        self.assertNotIn("zip_namelist", data)
        self.assertNotIn("zip_basenames", data)

    def test_input_files_dict_keys_and_values(self):
        xml_with_pre = self._make_base_xml()
        xml_with_pre.add_xml_info("artigo", "/tmp/artigo.xml")
        xml_with_pre.add_zip_info("/tmp/pacote.zip", ["artigo.xml"], ["artigo.xml"])
        xml_with_pre.submitted_filename = "Artigo.HTM"

        expected = {
            "xml_name": "artigo",
            "zip_namelist": ["artigo.xml"],
            "zip_basenames": ["artigo.xml"],
            "zip_file_path": "/tmp/pacote.zip",
            "xml_file_path": "/tmp/artigo.xml",
            "submitted_filename": "Artigo.htm",
            "submitted_ext": ".htm",
            "is_html": True,
            "provided_sps_pkg_name": None,
        }
        self.assertEqual(xml_with_pre.input_files_dict, expected)

    def test_input_files_dict_defaults_when_nothing_set(self):
        xml_with_pre = self._make_base_xml()
        expected = {
            "xml_name": None,
            "zip_namelist": None,
            "zip_basenames": None,
            "zip_file_path": None,
            "xml_file_path": None,
            "submitted_filename": None,
            "submitted_ext": None,
            "is_html": None,
            "provided_sps_pkg_name": None,
        }
        self.assertEqual(xml_with_pre.input_files_dict, expected)

    def test_pkg_names_dict_keys(self):
        xml_with_pre = self._make_base_xml()
        self.assertEqual(
            set(xml_with_pre.pkg_names_dict.keys()),
            {
                "pmc_pkg_name",
                "built_sps_pkg_name",
                "provided_sps_pkg_name",
                "sps_pkg_name",
                "sps_pkg_name_origin",
                "pkg_name_list",
            },
        )

    def test_pkg_names_dict_values_for_base_xml(self):
        xml_with_pre = self._make_base_xml()
        pkg_names = xml_with_pre.pkg_names_dict
        self.assertEqual(pkg_names["pmc_pkg_name"], "abc-10-2-e12345")
        self.assertIsNone(pkg_names["built_sps_pkg_name"])
        self.assertIsNone(pkg_names["provided_sps_pkg_name"])
        self.assertEqual(pkg_names["sps_pkg_name"], "1234-5678-abc-10-02-e12345")
        self.assertEqual(pkg_names["sps_pkg_name_origin"], "deprecated_sps_pkg_name_version_2")
        # ATENÇÃO: pkg_name_variations sempre inclui `None` quando
        # built_sps_pkg_name não foi definido, pois o try/except em
        # pkg_name_variations não captura nenhuma exceção real (a property
        # built_sps_pkg_name nunca lança ValueError, apenas retorna None).
        self.assertEqual(
            pkg_names["pkg_name_list"],
            {"1234-5678-abc-10-02-e12345", None},
        )

    def test_pkg_names_dict_reflects_provided_name_when_set(self):
        xml_with_pre = self._make_base_xml()
        xml_with_pre.provided_sps_pkg_name = "meu-pacote"
        pkg_names = xml_with_pre.pkg_names_dict
        self.assertEqual(pkg_names["sps_pkg_name"], "meu-pacote")
        self.assertEqual(pkg_names["sps_pkg_name_origin"], "provided_sps_pkg_name")
        self.assertIn("meu-pacote", pkg_names["pkg_name_list"])

    def test_sps_pkg_names_dict_keys(self):
        xml_with_pre = self._make_base_xml()
        self.assertEqual(
            set(xml_with_pre.sps_pkg_names_dict.keys()),
            {
                "sps_pkg_name",
                "sps_pkg_name_origin",
                "pkg_name_list",
                "built_sps_pkg_name",
                "built_sps_pkg_name_now",
                "provided_sps_pkg_name",
            },
        )

    def test_sps_pkg_names_dict_values_for_base_xml(self):
        xml_with_pre = self._make_base_xml()
        sps_pkg_names = xml_with_pre.sps_pkg_names_dict
        self.assertEqual(sps_pkg_names["sps_pkg_name"], "1234-5678-abc-10-02-e12345")
        self.assertEqual(sps_pkg_names["sps_pkg_name_origin"], "deprecated_sps_pkg_name_version_2")
        self.assertIsNone(sps_pkg_names["built_sps_pkg_name"])
        self.assertIsNone(sps_pkg_names["provided_sps_pkg_name"])
        # built_sps_pkg_name_now é calculado na hora (build_sps_pkg_name()),
        # e não depende de `built_sps_pkg_name` ter sido definido antes
        self.assertEqual(sps_pkg_names["built_sps_pkg_name_now"], "1234-5678-abc-10-02-e12345")

    def test_sps_pkg_names_dict_raises_when_no_suffix_strategy_matches(self):
        # build_sps_pkg_name() (chamado dentro de sps_pkg_names_dict) usa
        # apenas as estratégias elocation_id/order/submitted_filename; sem
        # nenhuma delas, uma ValueError se propaga ao acessar o dicionário.
        xml_with_pre = self._make_xml(issn_epub="1234-5678", acron="abc", vol="10", num="2")
        with self.assertRaises(ValueError):
            xml_with_pre.sps_pkg_names_dict


# ==============================================================================
# get_data
# ==============================================================================
class TestGetData(XMLWithPreTestMixin, TestCase):

    def test_get_data_default_equals_data_property(self):
        xml_with_pre = self._make_base_xml()
        self.assertEqual(xml_with_pre.get_data(), xml_with_pre.data)

    def test_get_data_with_input_files_true_adds_input_files_dict_keys(self):
        xml_with_pre = self._make_base_xml()
        xml_with_pre.submitted_filename = "artigo.xml"
        result = xml_with_pre.get_data(input_files=True)
        for key in xml_with_pre.input_files_dict:
            self.assertIn(key, result)
        self.assertEqual(result["submitted_filename"], "artigo.xml")
        # chaves originais de `data` continuam presentes
        self.assertIn("sps_pkg_name", result)

    def test_get_data_with_pkg_names_true_adds_pkg_names_dict_keys(self):
        xml_with_pre = self._make_base_xml()
        result = xml_with_pre.get_data(pkg_names=True)
        for key in xml_with_pre.pkg_names_dict:
            self.assertIn(key, result)
        self.assertEqual(result["pmc_pkg_name"], "abc-10-2-e12345")
        self.assertEqual(result["sps_pkg_name_origin"], "deprecated_sps_pkg_name_version_2")

    def test_get_data_with_sps_pkg_names_true_adds_sps_pkg_names_dict_keys(self):
        xml_with_pre = self._make_base_xml()
        result = xml_with_pre.get_data(sps_pkg_names=True)
        for key in xml_with_pre.sps_pkg_names_dict:
            self.assertIn(key, result)
        self.assertEqual(result["built_sps_pkg_name_now"], "1234-5678-abc-10-02-e12345")

    def test_get_data_with_article_true_adds_article_data_keys(self):
        xml_with_pre = self._make_base_xml()
        result = xml_with_pre.get_data(article=True)
        for key in ("surnames", "collab", "links", "article_titles", "body_fragment"):
            self.assertIn(key, result)
        self.assertNotIn("partial_body", result)
        # XML de teste não tem corpo, autores nem títulos
        self.assertEqual(result["surnames"], [])
        self.assertIsNone(result["collab"])
        self.assertEqual(result["body_fragment"], "")

    def test_get_data_default_flags_do_not_add_extra_dict_keys(self):
        # input_files, sps_pkg_names e pkg_names/article são opt-in;
        # por padrão nenhum deles deve aparecer no resultado.
        xml_with_pre = self._make_base_xml()
        result = xml_with_pre.get_data()
        self.assertNotIn("pmc_pkg_name", result)
        self.assertNotIn("built_sps_pkg_name_now", result)
        self.assertNotIn("submitted_filename", result)
        self.assertNotIn("surnames", result)

    def test_get_data_combining_multiple_flags(self):
        xml_with_pre = self._make_base_xml()
        xml_with_pre.submitted_filename = "artigo.xml"
        result = xml_with_pre.get_data(input_files=True, pkg_names=True, article=True)
        for key in xml_with_pre.input_files_dict:
            self.assertIn(key, result)
        for key in xml_with_pre.pkg_names_dict:
            self.assertIn(key, result)
        for key in ("surnames", "collab", "links", "article_titles", "body_fragment"):
            self.assertIn(key, result)
        self.assertNotIn("partial_body", result)


# ==============================================================================
# xml_name vs filename: comportamento conforme a origem (arquivo .xml
# avulso versus item dentro de um .zip)
# ==============================================================================
class TestXmlNameVsFilenameOrigin(XMLWithPreTestMixin, TestCase):
    """
    `xml_name` e `filename` NÃO são a mesma coisa:

    - `xml_name`: nome "lógico" do XML, sem extensão. É atribuído
      explicitamente via `add_xml_info(xml_name, xml_file_path=None)` — seja
      manualmente, seja internamente por `get_xml_with_pre_from_xml_file`
      (nome do arquivo, sem ".xml") ou por `get_xml_with_pre_from_zip_file`
      (nome-base do item do zip, sem ".xml").

    - `filename` (propriedade só de leitura, sem setter): nome "físico"
      calculado a partir de `zip_file_path`/`xml_file_path`/`xml_name`:
        * SEM zip (zip_file_path vazio): filename = f"{xml_name}.xml"
          (o path completo em xml_file_path é ignorado).
        * COM zip (zip_file_path setado): filename = xml_file_path, ou
          seja, o caminho do XML *dentro do zip* — que pode incluir
          subpastas e diferir de f"{xml_name}.xml".

    Ou seja: a mesma instância pode ter xml_name="artigo" e filename
    "artigo.xml" (origem: arquivo avulso) ou filename
    "subpasta/artigo.xml" (origem: zip com o XML dentro de uma subpasta).
    """

    def test_filename_from_plain_xml_equals_xml_name_plus_extension(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        xml_with_pre.add_xml_info("artigo", "/tmp/uploads/artigo.xml")

        self.assertEqual(xml_with_pre.xml_name, "artigo")
        self.assertIsNone(xml_with_pre.zip_file_path)
        # sem zip, filename ignora o path completo e usa apenas
        # xml_name + ".xml"
        self.assertEqual(xml_with_pre.filename, "artigo.xml")

    def test_filename_from_zip_uses_xml_file_path_not_xml_name(self):
        xml_with_pre = self._make_xml(vol="10", num="2")
        # xml_name é o nome lógico (sem extensão); xml_file_path é o
        # caminho do item dentro do zip, que pode ter subpastas e diferir
        # do valor de xml_name
        xml_with_pre.add_xml_info("artigo", "pasta/artigo.xml")
        xml_with_pre.add_zip_info("/tmp/pacote.zip", ["pasta/artigo.xml"], ["artigo.xml"])

        self.assertEqual(xml_with_pre.xml_name, "artigo")
        self.assertEqual(xml_with_pre.zip_file_path, "/tmp/pacote.zip")
        # com zip, filename é o path do XML dentro do zip (xml_file_path),
        # não xml_name + ".xml"
        self.assertEqual(xml_with_pre.filename, "pasta/artigo.xml")
        self.assertNotEqual(xml_with_pre.filename, f"{xml_with_pre.xml_name}.xml")

    def test_filename_from_zip_when_xml_file_path_matches_xml_name(self):
        # Caso comum: sem subpastas, xml_file_path coincide com
        # xml_name + ".xml", mas ainda assim é xml_file_path (não xml_name)
        # quem determina o valor de filename.
        xml_with_pre = self._make_xml(vol="10", num="2")
        xml_with_pre.add_xml_info("artigo", "artigo.xml")
        xml_with_pre.add_zip_info("/tmp/pacote.zip", ["artigo.xml"], ["artigo.xml"])

        self.assertEqual(xml_with_pre.filename, "artigo.xml")
        self.assertEqual(xml_with_pre.filename, f"{xml_with_pre.xml_name}.xml")

    def test_xml_name_is_not_changed_by_add_zip_info(self):
        # add_zip_info altera zip_file_path/zip_namelist/zip_basenames, mas
        # nunca xml_name — só add_xml_info define/altera xml_name.
        xml_with_pre = self._make_xml(vol="10", num="2")
        xml_with_pre.add_xml_info("artigo", "artigo.xml")
        self.assertEqual(xml_with_pre.xml_name, "artigo")

        xml_with_pre.add_zip_info(
            "/tmp/pacote.zip", ["artigo.xml", "artigo.pdf"], ["artigo.xml", "artigo.pdf"]
        )
        self.assertEqual(xml_with_pre.xml_name, "artigo")  # inalterado

    def test_get_xml_with_pre_from_xml_file_sets_xml_name_from_basename_without_extension(self):
        xml_content = self._make_base_xml().tostring()
        with TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "meu-artigo-123.xml")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(xml_content)

            result = get_xml_with_pre_from_xml_file(file_path)
            xml_with_pre = result["xml_with_pre"]

            self.assertEqual(xml_with_pre.xml_name, "meu-artigo-123")
            self.assertIsNone(xml_with_pre.zip_file_path)
            # sem zip, filename = xml_name + ".xml"
            self.assertEqual(xml_with_pre.filename, "meu-artigo-123.xml")

    def test_get_xml_with_pre_from_zip_file_sets_xml_name_and_filename_from_zip_item(self):
        xml_content = self._make_base_xml().tostring()
        with TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, "pacote.zip")
            with ZipFile(zip_path, "w", compression=ZIP_DEFLATED) as zf:
                zf.writestr("subpasta/meu-artigo-123.xml", xml_content)

            items = get_xml_with_pre_from_zip_file(zip_path)
            self.assertEqual(len(items), 1)
            xml_with_pre = items[0]["xml_with_pre"]

            # xml_name vem apenas do nome-base do item, sem extensão e sem
            # subpasta
            self.assertEqual(xml_with_pre.xml_name, "meu-artigo-123")
            self.assertEqual(xml_with_pre.zip_file_path, zip_path)
            # filename, por outro lado, é o path COMPLETO do XML dentro do
            # zip (inclui a subpasta) — diferente de f"{xml_name}.xml"
            self.assertEqual(xml_with_pre.filename, "subpasta/meu-artigo-123.xml")
            self.assertNotEqual(xml_with_pre.filename, f"{xml_with_pre.xml_name}.xml")


# ==============================================================================
# 1. TESTES PARA XMLWithPre.create
# ==============================================================================
class TestXMLWithPreCreate(XMLWithPreTestMixin, TestCase):
    """Testes para o método construtor alternativo e gerador XMLWithPre.create."""

    def test_create_from_xml_content_string(self):
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
        <article article-type="research-article" xml:lang="en">
            <front><journal-meta><journal-id journal-id-type="publisher-id">abc</journal-id></journal-meta></front>
        </article>"""
        instances = list(XMLWithPre.create(xml_content=xml_content))
        self.assertEqual(len(instances), 1)
        self.assertIsInstance(instances[0], XMLWithPre)
        self.assertEqual(instances[0].journal_acron, "abc")

    def test_create_from_path_single_xml_file(self):
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
        <article article-type="research-article" xml:lang="en">
            <front><journal-meta><journal-id journal-id-type="publisher-id">xyz</journal-id></journal-meta></front>
        </article>"""
        with TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test_doc.xml")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(xml_content)

            instances = list(XMLWithPre.create(path=file_path))
            self.assertEqual(len(instances), 1)
            self.assertIsInstance(instances[0], XMLWithPre)
            self.assertEqual(instances[0].journal_acron, "xyz")
            self.assertEqual(instances[0].xml_name, "test_doc")
            # origem: arquivo .xml avulso -> filename = xml_name + ".xml"
            self.assertIsNone(instances[0].zip_file_path)
            self.assertEqual(instances[0].filename, "test_doc.xml")

    def test_create_from_path_with_custom_names(self):
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
        <article article-type="research-article" xml:lang="en">
            <front><journal-meta><journal-id journal-id-type="publisher-id">abc</journal-id></journal-meta></front>
        </article>"""
        with TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "doc.xml")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(xml_content)

            instances = list(
                XMLWithPre.create(
                    path=file_path,
                    xml_native_name="custom_native",
                    built_name="custom_built",
                )
            )
            self.assertEqual(len(instances), 1)
            self.assertEqual(instances[0].provided_sps_pkg_name, "custom_native")
            self.assertEqual(instances[0].built_sps_pkg_name, "custom_built")
            self.assertEqual(instances[0].submitted_filename, "custom_native.xml")
            # xml_name continua vindo do nome físico do arquivo lido (doc),
            # independente de xml_native_name/built_name, que afetam apenas
            # provided/built_sps_pkg_name e submitted_filename
            self.assertEqual(instances[0].xml_name, "doc")

    @patch("packtools.sps.pid_provider.xml_sps_lib.get_xml_with_pre_from_uri")
    def test_create_from_uri(self, mock_get_from_uri):
        mock_instance = self._make_base_xml()
        mock_get_from_uri.return_value = mock_instance

        instances = list(XMLWithPre.create(uri="https://scielo.org/sample.xml"))
        self.assertEqual(len(instances), 1)
        self.assertEqual(instances[0], mock_instance)
        mock_get_from_uri.assert_called_once_with("https://scielo.org/sample.xml", 30)

    def test_create_from_path_invalid_file_raises_get_xml_with_pre_error(self):
        with TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "invalid.xml")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("CONTEUDO_XML_INVALIDO_SEM_TAGS")

            with self.assertRaises(GetXmlWithPreError):
                list(XMLWithPre.create(path=file_path))


# ==============================================================================
# 2. TESTES PARA XMLWithPre.add_pkg_name
# ==============================================================================
class TestAddPkgName(XMLWithPreTestMixin, TestCase):
    """Testes de atribuição explícita de nomes via add_pkg_name."""

    def test_add_pkg_name_with_xml_native_name(self):
        xml_with_pre = self._make_base_xml()
        xml_with_pre.add_pkg_name(xml_native_name="native-pkg-name")
        self.assertEqual(xml_with_pre.provided_sps_pkg_name, "native-pkg-name")
        self.assertEqual(xml_with_pre.submitted_filename, "native-pkg-name.xml")
        self.assertEqual(xml_with_pre.source_filename, "native-pkg-name")
        self.assertEqual(xml_with_pre.source_ext, ".xml")

    def test_add_pkg_name_with_html_name(self):
        xml_with_pre = self._make_base_xml()
        xml_with_pre.add_pkg_name(html_name="legacy_page")
        self.assertIsNone(xml_with_pre.provided_sps_pkg_name)
        self.assertEqual(xml_with_pre.submitted_filename, "legacy_page.html")
        self.assertEqual(xml_with_pre.source_filename, "legacy_page")
        self.assertEqual(xml_with_pre.source_ext, ".html")
        self.assertTrue(xml_with_pre.is_html_source)

    def test_add_pkg_name_with_built_name(self):
        xml_with_pre = self._make_base_xml()
        xml_with_pre.add_pkg_name(built_name="constructed-name-v1")
        self.assertEqual(xml_with_pre.built_sps_pkg_name, "constructed-name-v1")

    def test_add_pkg_name_xml_native_precedes_html_name(self):
        xml_with_pre = self._make_base_xml()
        xml_with_pre.add_pkg_name(xml_native_name="native_win", html_name="html_lose")
        self.assertEqual(xml_with_pre.provided_sps_pkg_name, "native_win")
        self.assertEqual(xml_with_pre.submitted_filename, "native_win.xml")

    def test_add_pkg_name_combining_native_and_built(self):
        xml_with_pre = self._make_base_xml()
        xml_with_pre.add_pkg_name(xml_native_name="pkg-123", built_name="built-123")
        self.assertEqual(xml_with_pre.provided_sps_pkg_name, "pkg-123")
        self.assertEqual(xml_with_pre.built_sps_pkg_name, "built-123")
        self.assertEqual(xml_with_pre.sps_pkg_name, "pkg-123")


# ==============================================================================
# 3. TESTES PARA XMLWithPre.pkg_name_variations
# ==============================================================================
class TestPkgNameVariations(XMLWithPreTestMixin, TestCase):
    """Testes para geração de variações de nomes utilizadas em buscas/queries do Django ORM."""

    def test_pkg_name_variations_includes_multi_issn(self):
        xml_with_pre = self._make_xml(
            issn_epub="1234-5678",
            issn_ppub="8765-4321",
            acron="abc",
            vol="10",
            num="2",
            elocation="e100",
        )
        variations = xml_with_pre.pkg_name_variations
        self.assertIn("1234-5678-abc-10-02-e100", variations)
        self.assertIn("8765-4321-abc-10-02-e100", variations)

    def test_pkg_name_variations_includes_submitted_filename(self):
        xml_with_pre = self._make_base_xml()
        xml_with_pre.submitted_filename = "artigo_original.xml"
        variations = xml_with_pre.pkg_name_variations
        self.assertIn("artigo_original.xml", variations)

    def test_pkg_name_variations_includes_provided_and_built_names(self):
        xml_with_pre = self._make_base_xml()
        xml_with_pre.provided_sps_pkg_name = "provided-name"
        xml_with_pre._built_sps_pkg_name = "built-name"
        variations = xml_with_pre.pkg_name_variations
        self.assertIn("provided-name", variations)
        self.assertIn("built-name", variations)

    def test_pkg_name_variations_includes_xml_name(self):
        xml_with_pre = self._make_base_xml()
        xml_with_pre.add_xml_info("artigo_parsed")
        variations = xml_with_pre.pkg_name_variations
        self.assertIn("artigo_parsed", variations)

    def test_pkg_name_variations_includes_deprecated_list(self):
        xml_with_pre = self._make_xml(
            issn_epub="1234-5678",
            acron="abc",
            vol="10",
            num="2",
            suppl="1",
            fpage="100",
            lpage="110",
        )
        variations = xml_with_pre.pkg_name_variations
        for dep_name in xml_with_pre.deprecated_sps_pkg_name_list:
            self.assertIn(dep_name, variations)

    def test_pkg_name_variations_returns_set(self):
        xml_with_pre = self._make_base_xml()
        variations = xml_with_pre.pkg_name_variations
        self.assertIsInstance(variations, set)


# ==============================================================================
# 4. TESTES PARA XMLWithPre.sps_pkg_name (Regras Globais de Precedência e Fallback)
# ==============================================================================
class TestSpsPkgNameComprehensive(XMLWithPreTestMixin, TestCase):
    """Testes de alta cobertura cobrindo a hierarquia completa de sps_pkg_name."""

    def test_sps_pkg_name_hierarchy_1_provided_has_top_priority(self):
        xml_with_pre = self._make_base_xml()
        xml_with_pre.provided_sps_pkg_name = "1-provided"
        xml_with_pre._built_sps_pkg_name = "2-built"
        xml_with_pre.add_xml_info("3-xml-name")

        self.assertEqual(xml_with_pre.sps_pkg_name, "1-provided")
        self.assertEqual(xml_with_pre.sps_pkg_name_origin, "provided_sps_pkg_name")

    def test_sps_pkg_name_hierarchy_2_built_has_second_priority(self):
        xml_with_pre = self._make_base_xml()
        xml_with_pre.provided_sps_pkg_name = None
        xml_with_pre._built_sps_pkg_name = "2-built"
        xml_with_pre.add_xml_info("3-xml-name")

        self.assertEqual(xml_with_pre.sps_pkg_name, "2-built")
        self.assertEqual(xml_with_pre.sps_pkg_name_origin, "built_sps_pkg_name")

    def test_sps_pkg_name_hierarchy_3_xml_name_has_third_priority(self):
        xml_with_pre = self._make_base_xml()
        xml_with_pre.provided_sps_pkg_name = None
        xml_with_pre._built_sps_pkg_name = None
        xml_with_pre.add_xml_info("3-xml-name")

        self.assertEqual(xml_with_pre.sps_pkg_name, "3-xml-name")
        self.assertEqual(xml_with_pre.sps_pkg_name_origin, "xml_name")

    def test_sps_pkg_name_hierarchy_4_deprecated_v2_as_final_fallback(self):
        xml_with_pre = self._make_base_xml()
        xml_with_pre.provided_sps_pkg_name = None
        xml_with_pre._built_sps_pkg_name = None
        self.assertIsNone(xml_with_pre.xml_name)

        self.assertEqual(xml_with_pre.sps_pkg_name, xml_with_pre.deprecated_sps_pkg_name_version_2)
        self.assertEqual(xml_with_pre.sps_pkg_name_origin, "deprecated_sps_pkg_name_version_2")

    def test_sps_pkg_name_setter_is_rejected(self):
        xml_with_pre = self._make_base_xml()
        with self.assertRaises(AttributeError):
            xml_with_pre.sps_pkg_name = "new-set-name"

"""
Testes complementares para packtools.sps.pid_provider.xml_sps_lib.XMLWithPre.renditions

Última versão de `renditions`:
    1. O "portão" agora verifica `self.zip_namelist` (não mais
       `zip_basenames`) — se falsy, retorna [] imediatamente.
    2. Constrói um mapa {basename: caminho_completo} a partir de
       `self.zip_namelist` usando os.path.basename, permitindo localizar um
       arquivo mesmo que esteja dentro de subpastas no zip.
    3. Troca o campo booleano "in_zip" por "path_in_zip": o CAMINHO COMPLETO
       (conforme está no zip) do arquivo cujo basename bate com "name", ou
       None se não houver correspondência.
    4. "sps_pkg_name" continua sendo montado por f-string direta.

`ArticleRenditions` é mockado para isolar a lógica própria da property.
"""
from types import SimpleNamespace


def _patch_article_renditions(items):
    """Mocka ArticleRenditions(...).article_renditions com `items`."""
    patcher = patch("packtools.sps.pid_provider.xml_sps_lib.ArticleRenditions")
    mock_class = patcher.start()
    mock_class.return_value.article_renditions = items
    return mock_class


class TestRenditionsGating(XMLWithPreTestMixin, TestCase):
    """Testa o "portão" baseado em zip_namelist (não mais zip_basenames)."""

    def tearDown(self):
        patch.stopall()

    def test_returns_empty_list_when_zip_namelist_is_none(self):
        xml_with_pre = self._make_base_xml()
        xml_with_pre.xml_name = "artigo"
        self.assertIsNone(xml_with_pre.zip_namelist)

        mock_class = _patch_article_renditions(
            [SimpleNamespace(is_main_language=True, language="en")]
        )
        self.assertEqual(xml_with_pre.renditions, [])
        mock_class.assert_not_called()

    def test_returns_empty_list_when_zip_namelist_is_empty_list(self):
        xml_with_pre = self._make_base_xml()
        xml_with_pre.xml_name = "artigo"
        xml_with_pre.zip_namelist = []

        mock_class = _patch_article_renditions(
            [SimpleNamespace(is_main_language=True, language="en")]
        )
        self.assertEqual(xml_with_pre.renditions, [])
        mock_class.assert_not_called()

    def test_zip_basenames_no_longer_gates_anything(self):
        # zip_basenames (usado em versões anteriores) deixou de importar:
        # com zip_namelist preenchido e zip_basenames vazio/None, a property
        # deve funcionar normalmente.
        xml_with_pre = self._make_base_xml()
        xml_with_pre.xml_name = "artigo"
        xml_with_pre.zip_namelist = ["artigo.pdf"]
        xml_with_pre.zip_basenames = None
        _patch_article_renditions([SimpleNamespace(is_main_language=True, language="en")])

        result = xml_with_pre.renditions
        self.assertEqual(len(result), 1)

        # e o inverso: zip_basenames preenchido mas zip_namelist vazio ->
        # continua retornando []
        xml_with_pre2 = self._make_base_xml()
        xml_with_pre2.xml_name = "artigo"
        xml_with_pre2.zip_namelist = []
        xml_with_pre2.zip_basenames = ["artigo.pdf"]
        _patch_article_renditions([SimpleNamespace(is_main_language=True, language="en")])
        self.assertEqual(xml_with_pre2.renditions, [])

    def test_raises_value_error_immediately_on_property_access(self):
        xml_with_pre = self._make_base_xml()
        xml_with_pre.zip_namelist = ["artigo.xml"]
        # xml_name nunca foi atribuído (permanece None)
        _patch_article_renditions([SimpleNamespace(is_main_language=True, language="en")])

        with self.assertRaises(ValueError):
            xml_with_pre.renditions

    def test_no_error_when_xml_name_missing_but_zip_namelist_falsy(self):
        xml_with_pre = self._make_base_xml()
        # nem xml_name nem zip_namelist foram definidos
        mock_class = _patch_article_renditions(
            [SimpleNamespace(is_main_language=True, language="en")]
        )
        self.assertEqual(xml_with_pre.renditions, [])
        mock_class.assert_not_called()


class TestRenditionsPathInZip(XMLWithPreTestMixin, TestCase):
    """Testa o mapeamento basename -> caminho completo e o campo path_in_zip."""

    def tearDown(self):
        patch.stopall()

    def _setup(self, xml_name="artigo", zip_namelist=None, provided_name="1234-5678-abc-10-02-e100"):
        xml_with_pre = self._make_base_xml()
        xml_with_pre.xml_name = xml_name
        xml_with_pre.zip_namelist = zip_namelist if zip_namelist is not None else []
        if provided_name is not None:
            xml_with_pre.provided_sps_pkg_name = provided_name
        return xml_with_pre

    def test_path_in_zip_equals_full_path_when_file_is_at_zip_root(self):
        xml_with_pre = self._setup(zip_namelist=["artigo.pdf"])
        _patch_article_renditions([SimpleNamespace(is_main_language=True, language="en")])

        result = xml_with_pre.renditions
        self.assertEqual(result[0]["path_in_zip"], "artigo.pdf")

    def test_path_in_zip_resolves_via_basename_when_file_is_in_subfolder(self):
        # zip_namelist guarda o caminho completo dentro do zip; o match é
        # feito pelo basename, mas o valor retornado é o caminho ORIGINAL.
        xml_with_pre = self._setup(zip_namelist=["pkg/subpasta/artigo.pdf"])
        _patch_article_renditions([SimpleNamespace(is_main_language=True, language="en")])

        result = xml_with_pre.renditions
        self.assertEqual(result[0]["name"], "artigo.pdf")
        self.assertEqual(result[0]["path_in_zip"], "pkg/subpasta/artigo.pdf")

    def test_path_in_zip_is_none_when_no_matching_basename(self):
        xml_with_pre = self._setup(zip_namelist=["outro-arquivo.pdf"])
        _patch_article_renditions([SimpleNamespace(is_main_language=True, language="en")])

        result = xml_with_pre.renditions
        self.assertIsNone(result[0]["path_in_zip"])

    def test_duplicate_basenames_last_entry_in_zip_namelist_wins(self):
        # Se dois caminhos no zip tiverem o MESMO basename (situação
        # incomum, mas possível), o dict `namelist` é sobrescrito em ordem —
        # o último item de zip_namelist "vence".
        xml_with_pre = self._setup(
            zip_namelist=["dir1/artigo.pdf", "dir2/artigo.pdf"]
        )
        _patch_article_renditions([SimpleNamespace(is_main_language=True, language="en")])

        result = xml_with_pre.renditions
        self.assertEqual(result[0]["path_in_zip"], "dir2/artigo.pdf")

    def test_multiple_renditions_with_mixed_path_in_zip(self):
        xml_with_pre = self._setup(
            zip_namelist=["artigo.pdf", "pkg/artigo-pt.pdf"]
        )
        fake_items = [
            SimpleNamespace(is_main_language=True, language="en"),
            SimpleNamespace(is_main_language=False, language="pt"),
            SimpleNamespace(is_main_language=False, language="es"),
        ]
        _patch_article_renditions(fake_items)

        result = xml_with_pre.renditions

        self.assertEqual(
            [item["name"] for item in result],
            ["artigo.pdf", "artigo-pt.pdf", "artigo-es.pdf"],
        )
        self.assertEqual(
            [item["path_in_zip"] for item in result],
            ["artigo.pdf", "pkg/artigo-pt.pdf", None],
        )


class TestRenditionsContent(XMLWithPreTestMixin, TestCase):
    """Testa as demais chaves do dicionário retornado."""

    def tearDown(self):
        patch.stopall()

    def _setup(self, xml_name="artigo", zip_namelist=None, provided_name="1234-5678-abc-10-02-e100"):
        xml_with_pre = self._make_base_xml()
        xml_with_pre.xml_name = xml_name
        xml_with_pre.zip_namelist = zip_namelist if zip_namelist is not None else []
        if provided_name is not None:
            xml_with_pre.provided_sps_pkg_name = provided_name
        return xml_with_pre

    def test_return_type_is_a_plain_list(self):
        xml_with_pre = self._setup(zip_namelist=["artigo.pdf"])
        _patch_article_renditions([SimpleNamespace(is_main_language=True, language="en")])
        self.assertIsInstance(xml_with_pre.renditions, list)

    def test_main_language_dict_shape_and_values(self):
        xml_with_pre = self._setup(zip_namelist=["artigo.pdf"])
        _patch_article_renditions([SimpleNamespace(is_main_language=True, language="en")])

        result = xml_with_pre.renditions

        self.assertEqual(len(result), 1)
        item = result[0]
        self.assertEqual(
            set(item.keys()),
            {"name", "lang", "component_type", "main", "sps_pkg_name", "path_in_zip"},
        )
        self.assertEqual(item["name"], "artigo.pdf")
        self.assertEqual(item["lang"], "en")
        self.assertEqual(item["component_type"], "rendition")
        self.assertTrue(item["main"])
        self.assertEqual(item["sps_pkg_name"], "1234-5678-abc-10-02-e100.pdf")
        self.assertEqual(item["path_in_zip"], "artigo.pdf")

    def test_translation_dict_shape_and_values(self):
        xml_with_pre = self._setup(zip_namelist=["artigo-pt.pdf"])
        _patch_article_renditions([SimpleNamespace(is_main_language=False, language="pt")])

        result = xml_with_pre.renditions

        item = result[0]
        self.assertEqual(item["name"], "artigo-pt.pdf")
        self.assertEqual(item["lang"], "pt")
        self.assertFalse(item["main"])
        self.assertEqual(item["sps_pkg_name"], "1234-5678-abc-10-02-e100-pt.pdf")

    def test_sps_pkg_name_uses_direct_fstring_not_replace(self):
        xml_with_pre = self._setup(
            xml_name="xmlname", zip_namelist=["xmlname-pt.pdf"], provided_name="provided"
        )
        _patch_article_renditions([SimpleNamespace(is_main_language=False, language="pt")])

        result = xml_with_pre.renditions

        self.assertEqual(result[0]["name"], "xmlname-pt.pdf")
        self.assertEqual(result[0]["sps_pkg_name"], "provided-pt.pdf")

    def test_uses_deprecated_fallback_sps_pkg_name_when_nothing_provided(self):
        xml_with_pre = self._setup(zip_namelist=["artigo.pdf"], provided_name=None)
        _patch_article_renditions([SimpleNamespace(is_main_language=True, language="en")])

        result = xml_with_pre.renditions

        self.assertEqual(result[0]["name"], "artigo.pdf")
        self.assertEqual(result[0]["sps_pkg_name"], "artigo.pdf")

    def test_empty_result_when_article_renditions_has_no_items(self):
        xml_with_pre = self._setup(zip_namelist=["artigo.pdf"])
        _patch_article_renditions([])

        self.assertEqual(xml_with_pre.renditions, [])

    def test_article_renditions_called_with_xmltree_only_after_gate_passes(self):
        xml_with_pre = self._setup(zip_namelist=["artigo.pdf"])
        mock_class = _patch_article_renditions([])

        xml_with_pre.renditions

        mock_class.assert_called_once_with(xml_with_pre.xmltree)


class TestMaxBodyFragmentLength(XMLWithPreTestMixin, TestCase):

    def test_default_is_300(self):
        xml_with_pre = self._make_base_xml()
        self.assertEqual(xml_with_pre.max_body_fragment_length, 300)

    def test_setter_overrides_default(self):
        xml_with_pre = self._make_base_xml()
        xml_with_pre.max_body_fragment_length = 50
        self.assertEqual(xml_with_pre.max_body_fragment_length, 50)

    def test_setter_none_falls_back_to_default(self):
        # o getter usa `self._max_body_fragment_length or default`
        xml_with_pre = self._make_base_xml()
        xml_with_pre.max_body_fragment_length = 50
        xml_with_pre.max_body_fragment_length = None
        self.assertEqual(xml_with_pre.max_body_fragment_length, 300)

    def test_setter_zero_falls_back_to_default_due_to_falsy_check(self):
        # comportamento sutil: 0 é falsy, então "or default" faz o getter
        # ignorar 0 e retornar 300 — documentando esse edge case
        xml_with_pre = self._make_base_xml()
        xml_with_pre.max_body_fragment_length = 0
        self.assertEqual(xml_with_pre.max_body_fragment_length, 300)


class TestBodyTextAndFragment(XMLWithPreTestMixin, TestCase):
    """Cobre body_text (cached_property), body_fragment, body_fingerprint
    e body_fragment_fingerprint, e a integração com max_body_fragment_length."""

    def _xml_with_body(self, text):
        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<article article-type="research-article" xml:lang="en">
  <front><article-meta></article-meta></front>
  <body><p>{text}</p></body>
</article>"""
        for xml_with_pre in XMLWithPre.create(xml_content=xml_content):
            return xml_with_pre

    def test_body_text_returns_raw_joined_text(self):
        xml_with_pre = self._xml_with_body("Texto de   Teste")
        # normaliza espaços múltiplos, preserva capitalização
        self.assertEqual(xml_with_pre.body_text, "Texto de Teste")

    def test_body_text_empty_when_no_body(self):
        xml_with_pre = self._make_base_xml()
        self.assertEqual(xml_with_pre.body_text, "")

    def test_body_text_is_cached(self):
        # cached_property: valor computado é armazenado em __dict__;
        # não é possível espionar xmltree.xpath diretamente porque
        # lxml.etree._Element é um tipo C-extension com atributos
        # read-only (não suporta patch.object).
        xml_with_pre = self._xml_with_body("abc")
        first = xml_with_pre.body_text
        self.assertIn("body_text", xml_with_pre.__dict__)
        second = xml_with_pre.body_text
        self.assertIs(first, second)

    def test_body_fragment_uses_default_max_length_300(self):
        xml_with_pre = self._xml_with_body("Texto de Teste Longo")
        self.assertEqual(xml_with_pre.body_fragment, "texto de teste longo")

    def test_body_fragment_respects_custom_max_body_fragment_length(self):
        xml_with_pre = self._xml_with_body("Texto de Teste Longo")
        xml_with_pre.max_body_fragment_length = 5
        self.assertEqual(xml_with_pre.body_fragment, "texto")

    def test_body_fragment_is_lowercased(self):
        xml_with_pre = self._xml_with_body("TEXTO MAIÚSCULO")
        self.assertIn("texto", xml_with_pre.body_fragment)

    def test_body_fingerprint_uses_full_body_text_not_truncated_fragment(self):
        xml_with_pre = self._xml_with_body("abc")
        xml_with_pre.max_body_fragment_length = 1  # não deve afetar body_fingerprint
        expected = generate_finger_print(xml_with_pre.body_text)
        self.assertEqual(xml_with_pre.body_fingerprint, expected)

    def test_body_fragment_fingerprint_uses_body_fragment(self):
        xml_with_pre = self._xml_with_body("abc")
        expected = generate_finger_print(xml_with_pre.body_fragment)
        self.assertEqual(xml_with_pre.body_fragment_fingerprint, expected)

    def test_body_fragment_fingerprint_changes_with_max_body_fragment_length(self):
        xml_with_pre = self._xml_with_body("abcdefgh")
        xml_with_pre.max_body_fragment_length = 3
        truncated_fp = xml_with_pre.body_fragment_fingerprint
        # instância separada para simular o valor "cheio" (default 300)
        xml_with_pre2 = self._xml_with_body("abcdefgh")
        full_fp = xml_with_pre2.body_fragment_fingerprint
        self.assertNotEqual(truncated_fp, full_fp)

    def test_body_fragment_reflects_max_length_change_after_first_access(self):
        # body_fragment agora é @property (não mais cached_property), então
        # mudar max_body_fragment_length DEPOIS de acessar body_fragment uma
        # vez deve refletir no próximo acesso — sem cache obsoleto.
        xml_with_pre = self._xml_with_body("abcdefgh")
        first = xml_with_pre.body_fragment  # default 300 -> "abcdefgh"
        xml_with_pre.max_body_fragment_length = 3
        second = xml_with_pre.body_fragment
        self.assertNotEqual(first, second)
        self.assertEqual(second, "abc")


class TestGetArticleDataCacheReuse(XMLWithPreTestMixin, TestCase):
    """get_article_data reaproveita body_fragment cacheado quando o
    max_body_fragment_length pedido bate com o já configurado."""

    def _xml_with_body(self, text):
        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<article article-type="research-article" xml:lang="en">
  <front><article-meta></article-meta></front>
  <body><p>{text}</p></body>
</article>"""
        for xml_with_pre in XMLWithPre.create(xml_content=xml_content):
            return xml_with_pre

    def test_reuses_cached_body_fragment_when_length_matches_current_setting(self):
        xml_with_pre = self._xml_with_body("abcdef")
        cached = xml_with_pre.body_fragment  # popula body_text com default (300)
        data = xml_with_pre.get_article_data(max_body_fragment_length=300)
        self.assertEqual(data["body_fragment"], cached)

    def test_bypasses_cache_when_length_differs_from_current_setting(self):
        xml_with_pre = self._xml_with_body("abcdef")
        data = xml_with_pre.get_article_data(max_body_fragment_length=3)
        self.assertEqual(data["body_fragment"], "abc")
        # max_body_fragment_length (default 300) não deve ter mudado
        self.assertEqual(xml_with_pre.body_fragment, "abcdef")

    def test_get_article_data_still_returns_partial_body_key(self):
        xml_with_pre = self._xml_with_body("abc")
        data = xml_with_pre.get_article_data()
        self.assertIn("partial_body", data)


class TestSurnamesCachedProperty(XMLWithPreTestMixin, TestCase):

    def test_surnames_empty_list_on_exception_or_absence(self):
        xml_with_pre = self._make_base_xml()
        self.assertEqual(xml_with_pre.surnames, [])

    def test_surnames_matches_get_article_data_surnames(self):
        xml_with_pre = self._make_base_xml()
        self.assertEqual(xml_with_pre.surnames, xml_with_pre.get_article_data()["surnames"])


class TestReadableData(XMLWithPreTestMixin, TestCase):

    def test_readable_data_has_no_partial_body_key(self):
        xml_with_pre = self._make_base_xml()
        result = xml_with_pre.readable_data
        self.assertNotIn("partial_body", result)
        self.assertEqual(
            set(result.keys()),
            {"surnames", "collab", "links", "article_titles", "body_fragment"},
        )

    def test_readable_data_body_fragment_matches_cached_body_fragment_property(self):
        xml_with_pre = self._make_base_xml()
        self.assertEqual(xml_with_pre.readable_data["body_fragment"], xml_with_pre.body_fragment)


if __name__ == "__main__":
    import unittest
    unittest.main()
