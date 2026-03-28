from unittest import TestCase

from lxml import etree
from packtools.sps.validation.article_xref import ArticleXrefValidation


def filter_results(results):
    """Remove None values from validation results."""
    return [r for r in results if r is not None]


class TestValidateRidPresence(TestCase):
    """Tests for validate_rid_presence: @rid is mandatory in <xref>."""

    def test_rid_present(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="bibr" rid="B1">1</xref></p>'
            "</body>"
            "</article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_rid_presence())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")

    def test_rid_missing(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="fig">Figure 1</xref></p>'
            "</body>"
            "</article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_rid_presence())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "CRITICAL")

    def test_rid_empty(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="fig" rid="">Figure 1</xref></p>'
            "</body>"
            "</article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_rid_presence())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "CRITICAL")

    def test_rid_whitespace_only(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="fig" rid="   ">Figure 1</xref></p>'
            "</body>"
            "</article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_rid_presence())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "CRITICAL")

    def test_multiple_xrefs_one_missing_rid(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="bibr" rid="B1">1</xref></p>'
            '<p><xref ref-type="fig">Figure 1</xref></p>'
            "</body>"
            "</article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_rid_presence())
        self.assertEqual(len(results), 2)
        responses = [r["response"] for r in results]
        self.assertIn("OK", responses)
        self.assertIn("CRITICAL", responses)


class TestValidateRefTypePresence(TestCase):
    """Tests for validate_ref_type_presence: @ref-type is mandatory in <xref>."""

    def test_ref_type_present(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="bibr" rid="B1">1</xref></p>'
            "</body>"
            "</article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_ref_type_presence())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")

    def test_ref_type_missing(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref rid="f1">Figure 1</xref></p>'
            "</body>"
            "</article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_ref_type_presence())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "CRITICAL")

    def test_ref_type_empty(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="" rid="f1">Figure 1</xref></p>'
            "</body>"
            "</article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_ref_type_presence())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "CRITICAL")

    def test_both_attributes_empty(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="" rid="">reference</xref></p>'
            "</body>"
            "</article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        ref_type_results = list(validator.validate_ref_type_presence())
        rid_results = list(validator.validate_rid_presence())
        self.assertEqual(ref_type_results[0]["response"], "CRITICAL")
        self.assertEqual(rid_results[0]["response"], "CRITICAL")


class TestValidateRefTypeValue(TestCase):
    """Tests for validate_ref_type_value: @ref-type must be a valid value."""

    def test_valid_aff(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="aff" rid="aff1">1</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_ref_type_value())
        self.assertEqual(results[0]["response"], "OK")

    def test_valid_app(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="app" rid="app1">Appendix</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_ref_type_value())
        self.assertEqual(results[0]["response"], "OK")

    def test_valid_author_notes(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="author-notes" rid="an1">*</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_ref_type_value())
        self.assertEqual(results[0]["response"], "OK")

    def test_valid_bibr(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="bibr" rid="B1">1</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_ref_type_value())
        self.assertEqual(results[0]["response"], "OK")

    def test_valid_bio(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="bio" rid="bio1">Bio</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_ref_type_value())
        self.assertEqual(results[0]["response"], "OK")

    def test_valid_boxed_text(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="boxed-text" rid="bx1">Box 1</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_ref_type_value())
        self.assertEqual(results[0]["response"], "OK")

    def test_valid_contrib(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="contrib" rid="c1">Author</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_ref_type_value())
        self.assertEqual(results[0]["response"], "OK")

    def test_valid_corresp(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="corresp" rid="cor1">*</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_ref_type_value())
        self.assertEqual(results[0]["response"], "OK")

    def test_valid_disp_formula(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="disp-formula" rid="e1">Eq. 1</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_ref_type_value())
        self.assertEqual(results[0]["response"], "OK")

    def test_valid_fig(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="fig" rid="f1">Figure 1</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_ref_type_value())
        self.assertEqual(results[0]["response"], "OK")

    def test_valid_fn(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="fn" rid="fn1">*</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_ref_type_value())
        self.assertEqual(results[0]["response"], "OK")

    def test_valid_list(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="list" rid="l1">List 1</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_ref_type_value())
        self.assertEqual(results[0]["response"], "OK")

    def test_valid_sec(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="sec" rid="s1">Section 1</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_ref_type_value())
        self.assertEqual(results[0]["response"], "OK")

    def test_valid_supplementary_material(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="supplementary-material" rid="suppl1">Suppl 1</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_ref_type_value())
        self.assertEqual(results[0]["response"], "OK")

    def test_valid_table(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="table" rid="t1">Table 1</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_ref_type_value())
        self.assertEqual(results[0]["response"], "OK")

    def test_valid_table_fn(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="table-fn" rid="tfn1">*</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_ref_type_value())
        self.assertEqual(results[0]["response"], "OK")

    def test_invalid_image(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="image" rid="f1">Figure 1</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_ref_type_value())
        self.assertEqual(results[0]["response"], "ERROR")

    def test_invalid_reference(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="reference" rid="B1">1</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_ref_type_value())
        self.assertEqual(results[0]["response"], "ERROR")

    def test_invalid_uppercase_fig(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="Fig" rid="f1">Figure 1</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_ref_type_value())
        self.assertEqual(results[0]["response"], "ERROR")

    def test_invalid_underscore_author_notes(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="author_notes" rid="fn1">*</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_ref_type_value())
        self.assertEqual(results[0]["response"], "ERROR")

    def test_skips_empty_ref_type(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="" rid="f1">Figure 1</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_ref_type_value())
        self.assertEqual(len(results), 0)


class TestValidateBibrPresence(TestCase):
    """Tests for validate_bibr_presence: at least one xref with ref-type='bibr' required."""

    def test_has_bibr(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="bibr" rid="B1">1</xref></p>'
            "</body>"
            "<back>"
            '<ref-list><ref id="B1"><mixed-citation>Citation</mixed-citation></ref></ref-list>'
            "</back></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_bibr_presence())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")

    def test_no_bibr(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="fig" rid="f1">Figure 1</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_bibr_presence())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "ERROR")

    def test_multiple_bibr(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="bibr" rid="B1">1</xref>, '
            '<xref ref-type="bibr" rid="B2">2</xref>, '
            '<xref ref-type="bibr" rid="B3">3</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_bibr_presence())
        self.assertEqual(results[0]["response"], "OK")

    def test_no_xref_at_all(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body><p>No cross-references.</p></body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_bibr_presence())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "ERROR")

    def test_editorial_without_bibr(self):
        xml_tree = etree.fromstring(
            '<article article-type="editorial" xml:lang="pt">'
            "<body><p>Editorial.</p></body>"
            "<back>"
            '<ref-list><ref id="B1"><mixed-citation>Ref</mixed-citation></ref></ref-list>'
            "</back></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_bibr_presence())
        self.assertEqual(results[0]["response"], "ERROR")

    def test_has_other_xref_but_no_bibr(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="fig" rid="f1">Figure 1</xref></p>'
            '<p><xref ref-type="table" rid="t1">Table 1</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_bibr_presence())
        self.assertEqual(results[0]["response"], "ERROR")


class TestValidateRidHasCorrespondingId(TestCase):
    """Tests for validate_rid_has_corresponding_id: @rid must point to existing @id."""

    def test_rid_matches_id(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="fig" rid="f1">Figure 1</xref></p>'
            '<fig id="f1"><label>Figure 1</label></fig>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_rid_has_corresponding_id())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")

    def test_rid_no_matching_id(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="fig" rid="f999">Figure 999</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_rid_has_corresponding_id())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "ERROR")

    def test_multiple_rids_all_match(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="bibr" rid="B1">1</xref>, '
            '<xref ref-type="bibr" rid="B2">2</xref></p>'
            "</body>"
            "<back><ref-list>"
            '<ref id="B1"><mixed-citation>R1</mixed-citation></ref>'
            '<ref id="B2"><mixed-citation>R2</mixed-citation></ref>'
            "</ref-list></back></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_rid_has_corresponding_id())
        for r in results:
            self.assertEqual(r["response"], "OK")

    def test_multiple_rids_some_no_match(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="fig" rid="f1">Fig 1</xref> and '
            '<xref ref-type="table" rid="t999">Table 999</xref></p>'
            '<fig id="f1"><label>Figure 1</label></fig>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_rid_has_corresponding_id())
        responses = [r["response"] for r in results]
        self.assertIn("OK", responses)
        self.assertIn("ERROR", responses)

    def test_rid_to_ref(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="bibr" rid="B1">1</xref></p>'
            "</body>"
            "<back><ref-list>"
            '<ref id="B1"><mixed-citation>Citation</mixed-citation></ref>'
            "</ref-list></back></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_rid_has_corresponding_id())
        self.assertEqual(results[0]["response"], "OK")

    def test_rid_to_aff(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<front><article-meta>"
            '<contrib-group><contrib contrib-type="author">'
            '<xref ref-type="aff" rid="aff1">1</xref>'
            "</contrib></contrib-group>"
            '<aff id="aff1"><institution>University</institution></aff>'
            "</article-meta></front></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_rid_has_corresponding_id())
        self.assertEqual(results[0]["response"], "OK")

    def test_rid_to_table(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="table" rid="t1">Table 1</xref></p>'
            '<table-wrap id="t1"><label>Table 1</label></table-wrap>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_rid_has_corresponding_id())
        self.assertEqual(results[0]["response"], "OK")

    def test_rid_to_sec(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="sec" rid="s1">Section 1</xref></p>'
            '<sec id="s1"><title>Section 1</title></sec>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_rid_has_corresponding_id())
        self.assertEqual(results[0]["response"], "OK")

    def test_skips_empty_rid(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="fig" rid="">Figure</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_rid_has_corresponding_id())
        self.assertEqual(len(results), 0)

    def test_multiple_rids_all_missing(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="bibr" rid="B1">1</xref>, '
            '<xref ref-type="bibr" rid="B2">2</xref>, '
            '<xref ref-type="bibr" rid="B3">3</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_rid_has_corresponding_id())
        self.assertEqual(len(results), 3)
        for r in results:
            self.assertEqual(r["response"], "ERROR")

    def test_bibr_rid_without_ref_list(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="bibr" rid="B1">1</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_rid_has_corresponding_id())
        self.assertEqual(results[0]["response"], "ERROR")


class TestValidateTranscriptXref(TestCase):
    """Tests for validate_transcript_xref: transcript sections need xref."""

    def test_no_transcript_section(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            "<sec><title>Introduction</title><p>Content</p></sec>"
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = filter_results(list(validator.validate_transcript_xref()))
        self.assertEqual(len(results), 0)

    def test_transcript_with_xref(self):
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" xml:lang="pt">'
            "<body>"
            '<media mimetype="video" mime-subtype="mp4" xlink:href="video.mp4">'
            "<label>Interview</label>"
            '<xref ref-type="sec" rid="TR1"/>'
            "</media>"
            '<sec sec-type="transcript" id="TR1">'
            "<title>Transcript</title><p>Content</p>"
            "</sec></body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = filter_results(list(validator.validate_transcript_xref()))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")

    def test_transcript_without_xref(self):
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" xml:lang="pt">'
            "<body>"
            '<media mimetype="video" mime-subtype="mp4" xlink:href="video.mp4">'
            "<label>Interview</label>"
            "</media>"
            '<sec sec-type="transcript" id="TR1">'
            "<title>Transcript</title><p>Content</p>"
            "</sec></body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = filter_results(list(validator.validate_transcript_xref()))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "WARNING")


class TestValidateAffSelfClosing(TestCase):
    """Tests for validate_aff_self_closing: aff xref without text should be self-closing."""

    def test_aff_with_text(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<front><article-meta>"
            '<contrib-group><contrib contrib-type="author">'
            '<xref ref-type="aff" rid="aff1">1</xref>'
            "</contrib></contrib-group>"
            '<aff id="aff1"><institution>University</institution></aff>'
            "</article-meta></front></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_aff_self_closing())
        self.assertEqual(len(results), 0)

    def test_aff_self_closing(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<front><article-meta>"
            '<contrib-group><contrib contrib-type="author">'
            '<xref ref-type="aff" rid="aff1"/>'
            "</contrib></contrib-group>"
            '<aff id="aff1"><institution>University</institution></aff>'
            "</article-meta></front></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_aff_self_closing())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "INFO")

    def test_aff_empty_not_self_closing(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<front><article-meta>"
            '<contrib-group><contrib contrib-type="author">'
            '<xref ref-type="aff" rid="aff1"></xref>'
            "</contrib></contrib-group>"
            '<aff id="aff1"><institution>University</institution></aff>'
            "</article-meta></front></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_aff_self_closing())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "INFO")

    def test_non_aff_not_validated(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="bibr" rid="B1">1</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_aff_self_closing())
        self.assertEqual(len(results), 0)


class TestValidateXrefRidHasCorrespondingElementId(TestCase):
    """Tests for the existing validate_xref_rid_has_corresponding_element_id method."""

    def test_all_rids_match(self):
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" xml:lang="pt">'
            "<front><article-meta>"
            '<p><xref ref-type="aff" rid="aff1">1</xref></p>'
            '<aff id="aff1"><p>affiliation</p></aff>'
            '<p><xref ref-type="fig" rid="fig1">1</xref></p>'
            '<fig id="fig1"><p>figure</p></fig>'
            "</article-meta></front></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_xref_rid_has_corresponding_element_id())
        for r in results:
            self.assertEqual(r["response"], "OK")

    def test_rid_no_match(self):
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" xml:lang="pt">'
            "<front><article-meta>"
            '<p><xref ref-type="table" rid="table1">1</xref></p>'
            "</article-meta></front></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_xref_rid_has_corresponding_element_id())
        error_results = [r for r in results if r["response"] == "ERROR"]
        self.assertTrue(len(error_results) > 0)


class TestValidateElementIdHasCorrespondingXrefRid(TestCase):
    """Tests for the existing validate_element_id_has_corresponding_xref_rid method."""

    def test_all_ids_have_xref(self):
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" xml:lang="pt">'
            "<front><article-meta>"
            '<p><xref ref-type="aff" rid="aff1">1</xref></p>'
            '<aff id="aff1"><p>affiliation</p></aff>'
            '<p><xref ref-type="fig" rid="fig1">1</xref></p>'
            '<fig id="fig1"><p>figure</p></fig>'
            '<p><xref ref-type="table" rid="table1">1</xref></p>'
            '<table-wrap id="table1"><p>table</p></table-wrap>'
            "</article-meta></front></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_element_id_has_corresponding_xref_rid())
        for r in results:
            self.assertEqual(r["response"], "OK")

    def test_id_without_xref(self):
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" xml:lang="pt">'
            "<front><article-meta>"
            '<table-wrap id="table1"><p>table</p></table-wrap>'
            "</article-meta></front></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_element_id_has_corresponding_xref_rid())
        error_results = [r for r in results if r["response"] == "ERROR"]
        self.assertTrue(len(error_results) > 0)


class TestValidateAttribNameAndValueHasCorrespondingXref(TestCase):
    """Tests for validate_attrib_name_and_value_has_corresponding_xref."""

    def test_transcript_with_xref(self):
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" xml:lang="pt">'
            "<body>"
            '<xref ref-type="sec" rid="TR1"/>'
            '<sec sec-type="transcript" id="TR1">'
            "<title>Transcript</title><p>Content</p>"
            "</sec></body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_attrib_name_and_value_has_corresponding_xref())
        ok_results = [r for r in results if r["response"] == "OK"]
        self.assertTrue(len(ok_results) > 0)

    def test_transcript_without_xref(self):
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" xml:lang="pt">'
            "<body>"
            '<sec sec-type="transcript" id="TR1">'
            "<title>Transcript</title><p>Content</p>"
            "</sec></body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_attrib_name_and_value_has_corresponding_xref())
        error_results = [r for r in results if r["response"] != "OK"]
        self.assertTrue(len(error_results) > 0)


class TestMultipleXrefs(TestCase):
    """Tests for documents with multiple xrefs."""

    def test_no_xref(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body><p>No xrefs here.</p></body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        rid_results = list(validator.validate_rid_presence())
        self.assertEqual(len(rid_results), 0)

    def test_single_bibr_xref(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="bibr" rid="B1">1</xref></p>'
            "</body>"
            "<back>"
            '<ref-list><ref id="B1"><mixed-citation>Ref</mixed-citation></ref></ref-list>'
            "</back></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        bibr_results = list(validator.validate_bibr_presence())
        self.assertEqual(bibr_results[0]["response"], "OK")

    def test_multiple_different_xrefs(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="bibr" rid="B1">1</xref></p>'
            '<p><xref ref-type="fig" rid="f1">Figure 1</xref></p>'
            '<p><xref ref-type="table" rid="t1">Table 1</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_ref_type_value())
        self.assertEqual(len(results), 3)
        for r in results:
            self.assertEqual(r["response"], "OK")


class TestXrefInDifferentContexts(TestCase):
    """Tests for xref in different parent elements."""

    def test_xref_in_p(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="bibr" rid="B1">1</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_rid_presence())
        self.assertEqual(results[0]["response"], "OK")

    def test_xref_in_td(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<table-wrap id="t1"><table><tbody><tr>'
            '<td><xref ref-type="bibr" rid="B1">1</xref></td>'
            "</tr></tbody></table></table-wrap>"
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_rid_presence())
        self.assertEqual(results[0]["response"], "OK")

    def test_xref_in_th(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<table-wrap id="t1"><table><thead><tr>'
            '<th><xref ref-type="fn" rid="fn1">*</xref></th>'
            "</tr></thead></table></table-wrap>"
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_rid_presence())
        self.assertEqual(results[0]["response"], "OK")

    def test_xref_in_contrib(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<front><article-meta>"
            '<contrib-group><contrib contrib-type="author">'
            '<name><surname>Silva</surname><given-names>J</given-names></name>'
            '<xref ref-type="aff" rid="aff1">1</xref>'
            "</contrib></contrib-group>"
            '<aff id="aff1"><institution>Univ</institution></aff>'
            "</article-meta></front></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_rid_presence())
        self.assertEqual(results[0]["response"], "OK")

    def test_xref_in_article_title(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<front><article-meta>"
            "<title-group>"
            '<article-title>Title <xref ref-type="fn" rid="fn1">*</xref></article-title>'
            "</title-group>"
            "</article-meta></front>"
            "<body><p>Content</p></body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_rid_presence())
        self.assertEqual(results[0]["response"], "OK")


class TestEdgeCases(TestCase):
    """Tests for edge cases."""

    def test_xref_with_complex_content(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="bibr" rid="B1"><sup>1</sup></xref></p>'
            "</body>"
            "<back>"
            '<ref-list><ref id="B1"><mixed-citation>Ref</mixed-citation></ref></ref-list>'
            "</back></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        rid_results = list(validator.validate_rid_presence())
        self.assertEqual(rid_results[0]["response"], "OK")
        bibr_results = list(validator.validate_bibr_presence())
        self.assertEqual(bibr_results[0]["response"], "OK")

    def test_xref_with_sup_inside(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p>Text<xref ref-type="bibr" rid="B1"><sup>1</sup></xref></p>'
            "</body>"
            "<back>"
            '<ref-list><ref id="B1"><mixed-citation>Smith. 2020.</mixed-citation></ref></ref-list>'
            "</back></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_ref_type_value())
        self.assertEqual(results[0]["response"], "OK")

    def test_citation_range(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p>Studies <xref ref-type="bibr" rid="B1">1</xref>-'
            '<xref ref-type="bibr" rid="B5">5</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_ref_type_value())
        self.assertEqual(len(results), 2)
        for r in results:
            self.assertEqual(r["response"], "OK")


class TestResponseFormat(TestCase):
    """Tests for the response format structure."""

    def test_response_has_required_keys(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="bibr" rid="B1">1</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_rid_presence())
        self.assertTrue(len(results) > 0)
        expected_keys = {
            "title", "parent", "parent_id", "parent_article_type",
            "parent_lang", "item", "sub_item", "validation_type",
            "response", "expected_value", "got_value", "message",
            "msg_text", "msg_params", "advice", "adv_text",
            "adv_params", "data",
        }
        self.assertEqual(set(results[0].keys()), expected_keys)

    def test_i18n_fields_present(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="fig">Figure 1</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_rid_presence())
        result = results[0]
        self.assertIn("msg_text", result)
        self.assertIn("msg_params", result)
        self.assertIn("adv_text", result)
        self.assertIn("adv_params", result)
        self.assertEqual(result["response"], "CRITICAL")
        self.assertIsNotNone(result["adv_text"])

    def test_ok_response_has_null_advice(self):
        xml_tree = etree.fromstring(
            '<article article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p><xref ref-type="bibr" rid="B1">1</xref></p>'
            "</body></article>"
        )
        validator = ArticleXrefValidation(xml_tree)
        results = list(validator.validate_rid_presence())
        result = results[0]
        self.assertEqual(result["response"], "OK")
        self.assertIsNone(result["advice"])
        self.assertIsNone(result["adv_text"])
        self.assertIsNone(result["adv_params"])
