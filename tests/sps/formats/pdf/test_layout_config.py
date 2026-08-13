import json
import os
import tempfile
import unittest

from packtools.sps.formats.pdf.layout_config import (
    DecisionSource,
    LayoutConfig,
    LayoutDecision,
    PageProfile,
    WidthClass,
    load_profile,
)


class TestPageProfile(unittest.TestCase):

    def test_defaults_match_a4_two_columns(self):
        profile = PageProfile()
        self.assertAlmostEqual(profile.page_width_pt, 595.28, places=1)
        self.assertAlmostEqual(profile.page_height_pt, 841.89, places=1)
        self.assertEqual(profile.default_column_count, 2)

    def test_content_width_subtracts_margins(self):
        profile = PageProfile(page_width_pt=600.0, margin_left_pt=50.0, margin_right_pt=50.0)
        self.assertAlmostEqual(profile.content_width_pt, 500.0)

    def test_column_width_single_column_equals_content_width(self):
        profile = PageProfile(page_width_pt=600.0, margin_left_pt=50.0, margin_right_pt=50.0)
        self.assertAlmostEqual(profile.column_width_pt(1), profile.content_width_pt)

    def test_column_width_two_columns_subtracts_gap_and_divides(self):
        profile = PageProfile(
            page_width_pt=620.0, margin_left_pt=50.0, margin_right_pt=50.0, column_gap_pt=20.0
        )
        # content_width = 520; two columns => (520 - 20) / 2 = 250
        self.assertAlmostEqual(profile.column_width_pt(2), 250.0)

    def test_to_dict_from_dict_roundtrip(self):
        profile = PageProfile(page_height_pt=793.7, default_column_count=1)
        restored = PageProfile.from_dict(profile.to_dict())
        self.assertEqual(profile, restored)

    def test_from_dict_partial_falls_back_to_defaults(self):
        profile = PageProfile.from_dict({"page_height_pt": 793.7})
        self.assertAlmostEqual(profile.page_height_pt, 793.7)
        self.assertEqual(profile.default_column_count, 2)  # untouched, default

    def test_to_page_attributes_overrides_only_page_size(self):
        base = {"page_width": 999, "page_height": 999, "top_margin": 123}
        profile = PageProfile(page_width_pt=595.28, page_height_pt=793.7)
        result = profile.to_page_attributes(base)
        self.assertAlmostEqual(result["page_width"].pt, 595.28, places=1)
        self.assertAlmostEqual(result["page_height"].pt, 793.7, places=1)
        self.assertEqual(result["top_margin"], 123)  # untouched


class TestLayoutDecision(unittest.TestCase):

    def test_label_matches_legacy_string_for_within_column(self):
        decision = LayoutDecision(
            element_class=WidthClass.WITHIN_COLUMN,
            width_pt=100.0,
            justification="fits",
            source=DecisionSource.MEASURED,
        )
        self.assertEqual(decision.label, "double-column-layout")

    def test_label_matches_legacy_string_for_full_page_width(self):
        decision = LayoutDecision(
            element_class=WidthClass.FULL_PAGE_WIDTH,
            width_pt=500.0,
            justification="too wide",
            source=DecisionSource.HEURISTIC,
        )
        self.assertEqual(decision.label, "single-column-layout")


class TestLayoutConfigColumns(unittest.TestCase):

    def test_default_column_count_comes_from_profile(self):
        cfg = LayoutConfig(profile=PageProfile(default_column_count=1))
        self.assertEqual(cfg.column_count, 1)

    def test_explicit_column_count_overrides_profile_default(self):
        cfg = LayoutConfig(profile=PageProfile(default_column_count=2), column_count=1)
        self.assertEqual(cfg.column_count, 1)

    def test_full_width_switches_to_one_column_and_restores(self):
        cfg = LayoutConfig(profile=PageProfile(default_column_count=2))
        self.assertEqual(cfg.column_count, 2)
        with cfg.full_width():
            self.assertEqual(cfg.column_count, 1)
        self.assertEqual(cfg.column_count, 2)

    def test_full_width_restores_correctly_when_nested(self):
        cfg = LayoutConfig(profile=PageProfile(default_column_count=2))
        with cfg.full_width():
            self.assertEqual(cfg.column_count, 1)
            with cfg.full_width():
                self.assertEqual(cfg.column_count, 1)
            self.assertEqual(cfg.column_count, 1)
        self.assertEqual(cfg.column_count, 2)

    def test_full_width_restores_even_when_body_raises(self):
        cfg = LayoutConfig(profile=PageProfile(default_column_count=2))
        with self.assertRaises(ValueError):
            with cfg.full_width():
                raise ValueError("boom")
        self.assertEqual(cfg.column_count, 2)

    def test_column_width_reflects_one_column_journal(self):
        profile = PageProfile(page_width_pt=600.0, margin_left_pt=50.0, margin_right_pt=50.0, default_column_count=1)
        cfg = LayoutConfig(profile=profile)
        self.assertAlmostEqual(cfg.column_width_pt, 500.0)


class TestDecideTableLayout(unittest.TestCase):

    def setUp(self):
        self.profile = PageProfile(page_width_pt=620.0, margin_left_pt=50.0, margin_right_pt=50.0, column_gap_pt=20.0)
        self.cfg = LayoutConfig(profile=self.profile)  # column_width_pt == 250.0

    def test_heuristic_fallback_uses_column_count_threshold(self):
        decision = self.cfg.decide_table_layout(n_columns=5)
        self.assertEqual(decision.element_class, WidthClass.FULL_PAGE_WIDTH)
        self.assertEqual(decision.source, DecisionSource.HEURISTIC)

    def test_heuristic_fallback_fits_at_or_below_threshold(self):
        decision = self.cfg.decide_table_layout(n_columns=4)
        self.assertEqual(decision.element_class, WidthClass.WITHIN_COLUMN)
        self.assertEqual(decision.source, DecisionSource.HEURISTIC)

    def test_measured_widths_used_when_given(self):
        # sum = 260 > 250 available -> must break to full width, even though
        # n_columns=2 would pass the (irrelevant, unused) heuristic threshold
        decision = self.cfg.decide_table_layout(n_columns=2, column_min_widths_pt=[130.0, 130.0])
        self.assertEqual(decision.element_class, WidthClass.FULL_PAGE_WIDTH)
        self.assertEqual(decision.source, DecisionSource.MEASURED)

    def test_measured_widths_fit_within_column(self):
        decision = self.cfg.decide_table_layout(n_columns=2, column_min_widths_pt=[100.0, 100.0])
        self.assertEqual(decision.element_class, WidthClass.WITHIN_COLUMN)
        self.assertEqual(decision.source, DecisionSource.MEASURED)
        self.assertAlmostEqual(decision.width_pt, 200.0)

    def test_full_page_width_resolves_to_single_column_width(self):
        decision = self.cfg.decide_table_layout(n_columns=8)
        self.assertAlmostEqual(decision.width_pt, self.profile.column_width_pt(1))

    def test_justification_is_non_empty(self):
        decision = self.cfg.decide_table_layout(n_columns=8)
        self.assertTrue(decision.justification)


class TestDecideFigureLayout(unittest.TestCase):

    def setUp(self):
        self.profile = PageProfile(page_width_pt=620.0, margin_left_pt=50.0, margin_right_pt=50.0, column_gap_pt=20.0)
        self.cfg = LayoutConfig(profile=self.profile)  # column_width_pt == 250.0

    def test_narrow_figure_fits_within_column(self):
        decision = self.cfg.decide_figure_layout(natural_width_pt=100.0)
        self.assertEqual(decision.element_class, WidthClass.WITHIN_COLUMN)
        self.assertAlmostEqual(decision.width_pt, 100.0)

    def test_wide_figure_breaks_to_full_width(self):
        decision = self.cfg.decide_figure_layout(natural_width_pt=240.0)
        self.assertEqual(decision.element_class, WidthClass.FULL_PAGE_WIDTH)

    def test_threshold_is_configurable(self):
        # 200pt is 80% of the 250pt column - fits under the default 0.9
        # threshold, but not under a stricter 0.75 threshold.
        self.assertEqual(
            self.cfg.decide_figure_layout(natural_width_pt=200.0, threshold=0.9).element_class,
            WidthClass.WITHIN_COLUMN,
        )
        self.assertEqual(
            self.cfg.decide_figure_layout(natural_width_pt=200.0, threshold=0.75).element_class,
            WidthClass.FULL_PAGE_WIDTH,
        )

    def test_source_is_always_measured(self):
        decision = self.cfg.decide_figure_layout(natural_width_pt=100.0)
        self.assertEqual(decision.source, DecisionSource.MEASURED)


class TestLoadProfile(unittest.TestCase):

    def test_missing_profile_falls_back_to_default(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            profile = load_profile("0000-0000", profiles_dir=tmpdir)
            self.assertEqual(profile, PageProfile())

    def test_existing_profile_is_loaded(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            data = {
                "schema_version": 1,
                "issn_epub": "1809-4392",
                "page": {"page_height_pt": 793.7, "default_column_count": 2},
            }
            with open(os.path.join(tmpdir, "1809-4392.json"), "w", encoding="utf-8") as f:
                json.dump(data, f)
            profile = load_profile("1809-4392", profiles_dir=tmpdir)
            self.assertAlmostEqual(profile.page_height_pt, 793.7)
            self.assertEqual(profile.default_column_count, 2)

    def test_bundled_profiles_load_without_error(self):
        # Sanity check against the real, calibrated profiles shipped with
        # packtools (packtools/sps/formats/pdf/profiles/*.json).
        for issn_epub, expected_height, expected_columns in [
            ("1809-4392", 793.7, 2),   # Acta Amazonica
            ("1677-941X", 793.7, 2),   # Acta Botanica Brasilica
            ("2357-738X", 841.89, 1),  # Anuário Antropológico
        ]:
            profile = load_profile(issn_epub)
            self.assertAlmostEqual(profile.page_height_pt, expected_height, places=1)
            self.assertEqual(profile.default_column_count, expected_columns)


if __name__ == "__main__":
    unittest.main()
