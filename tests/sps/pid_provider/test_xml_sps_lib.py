from unittest import TestCase
from unittest.mock import MagicMock, PropertyMock, patch
from lxml import etree
from packtools.sps.pid_provider.xml_sps_lib import XMLWithPre


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
    ):
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


if __name__ == "__main__":
    import unittest
    unittest.main()