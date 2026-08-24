import unittest
from unittest.mock import patch

from packtools.sps.formats.pdf.pipeline import docx as docx_pipe


class TestPipelineDocx(unittest.TestCase):
    # TODO
    ...


class TestJournalTitlePipe(unittest.TestLoader):
    # TODO
    ...


class TestDocxDoiPipe(unittest.TestCase):
    # TODO
    ...


class TestDocxArticleTypeAndCategoryPipe(unittest.TestCase):
    # TODO
    ...


class TestDocxArticleTitlePipe(unittest.TestCase):
    # TODO
    ...


class TestDocxAuthorsPipe(unittest.TestCase):
    # TODO
    ...


class TestDocxAffiliationPipe(unittest.TestCase):
    # TODO
    ...


class TestDocxCorrespondingPipe(unittest.TestCase):
    # TODO
    ...


class TestDocxAbstractPipe(unittest.TestCase):
    # TODO
    ...


class TestDocxKeyworksPipe(unittest.TestCase):
    # TODO
    ...


class TestDocxCiteAsPipe(unittest.TestCase):
    # TODO
    ...


class TestDocxSecondHeaderPipe(unittest.TestCase):
    # TODO
    ...


class TestDocxSecondFooterPipe(unittest.TestCase):
    # TODO
    ...


class TestDocxPageVolIssueYearPipe(unittest.TestCase):
    # TODO
    ...


class TestDocxBodyPipe(unittest.TestCase):
    # TODO
    ...


class TestDocxReferencesPipe(unittest.TestCase):
    # TODO
    ...


class TestDocxAcknowledgmentsPipe(unittest.TestCase):
    # TODO
    ...


class TestDocxSupplementaryMaterialPipe(unittest.TestCase):
    # TODO
    ...


class TestFlagDpiOutliers(unittest.TestCase):
    """Tests for _flag_dpi_outliers: flags a figure's DPI as untrustworthy
    when it diverges from its sibling figures' median DPI, in the same
    batch, by more than outlier_ratio."""

    def test_flags_dpi_outlier_against_siblings(self):
        figures = [{'href': 'graph1.tif'}, {'href': 'graph2.tif'}, {'href': 'graph3.tif'}]
        probes = {'graph1.tif': (612, 72.0), 'graph2.tif': (800, 300.0), 'graph3.tif': (700, 300.0)}
        with patch(
            'packtools.sps.formats.pdf.renderer.docx.figure.probe_image_dpi',
            side_effect=lambda docx, fig: probes[fig['href']],
        ):
            docx_pipe._flag_dpi_outliers(docx=None, figures=figures)

        self.assertEqual(figures[0]['layout_dpi_override'], 300.0)
        self.assertNotIn('layout_dpi_override', figures[1])
        self.assertNotIn('layout_dpi_override', figures[2])

    def test_does_not_flag_similar_dpis(self):
        figures = [{'href': 'a.tif'}, {'href': 'b.tif'}]
        probes = {'a.tif': (700, 280.0), 'b.tif': (700, 300.0)}
        with patch(
            'packtools.sps.formats.pdf.renderer.docx.figure.probe_image_dpi',
            side_effect=lambda docx, fig: probes[fig['href']],
        ):
            docx_pipe._flag_dpi_outliers(docx=None, figures=figures)

        self.assertNotIn('layout_dpi_override', figures[0])
        self.assertNotIn('layout_dpi_override', figures[1])

    def test_skips_figures_with_explicit_layout(self):
        # 'a.tif' already has a resolved layout and must not be probed; only
        # 'b.tif' should be. With a single figure left to probe there aren't
        # enough siblings to compare against, so no override is set either.
        figures = [{'href': 'a.tif', 'layout': 'single-column-layout'}, {'href': 'b.tif'}]
        with patch(
            'packtools.sps.formats.pdf.renderer.docx.figure.probe_image_dpi',
            return_value=(700, 300.0),
        ) as mock_probe:
            docx_pipe._flag_dpi_outliers(docx=None, figures=figures)
        mock_probe.assert_called_once_with(None, figures[1])
        self.assertNotIn('layout_dpi_override', figures[0])
        self.assertNotIn('layout_dpi_override', figures[1])

    def test_single_figure_is_never_flagged(self):
        figures = [{'href': 'a.tif'}]
        with patch(
            'packtools.sps.formats.pdf.renderer.docx.figure.probe_image_dpi',
            return_value=(612, 72.0),
        ):
            docx_pipe._flag_dpi_outliers(docx=None, figures=figures)
        self.assertNotIn('layout_dpi_override', figures[0])
