"""
LayoutConfig: the layout "modelo intermediário" (decision + width + justification).

Centralizes the layout context that table/figure rendering consult, replacing:
- packtools/sps/formats/pdf/enum.py::PAGE_ATTRIBUTES (fixed dict, no per-journal override)
- packtools/sps/formats/pdf/pipeline/xml.py::determine_table_layout (isolated ">4 columns" heuristic)
- packtools/sps/formats/pdf/renderer/docx/figure.py::decide_figure_layout (isolated DPI heuristic)

What changes relative to the previous behavior:
- A single source of page/column/margin geometry per document (PageProfile),
  optionally calibrated per journal, instead of a hardcoded A4/2-column constant.
- Table and figure layout decisions consult the same context instead of each
  inventing its own notion of "available width".
- Every decision is a structured object (LayoutDecision), never just a label string:
  it carries the resolved width, a human-readable justification, and where the
  judgment came from (measured / heuristic / override / default).
- An explicit primitive for "temporarily break to full page width, then restore"
  (LayoutConfig.full_width), instead of each caller re-implementing the same
  section break/restore mechanics.

All of this is additive and opt-in: every touched function keeps working exactly
as before when no LayoutConfig is passed in.
"""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class WidthClass(str, Enum):
    """
    Width class of a table/figure, relative to the current column layout.

    The string values intentionally match the legacy labels in
    packtools.sps.formats.pdf.enum (SINGLE_COLUMN_PAGE_LABEL / DOUBLE_COLUMN_PAGE_LABEL)
    for drop-in compatibility with existing callers. Note that those legacy names
    describe the *page's* state while rendering the element (a "single-column-layout"
    page is one that broke out to full width), not the element's own width - the
    members below are named from the element's point of view instead, which is
    less ambiguous to read at a call site.
    """

    WITHIN_COLUMN = "double-column-layout"
    FULL_PAGE_WIDTH = "single-column-layout"


class DecisionSource(str, Enum):
    """Where a LayoutDecision's judgment came from."""

    MEASURED = "measured"
    HEURISTIC = "heuristic"
    OVERRIDE = "override"
    DEFAULT = "default"


@dataclass(frozen=True)
class LayoutDecision:
    """
    A single layout decision: never just a label, always width + why.

    Args:
        element_class (WidthClass): Whether the element fits within the current
            column or needs to break out to the full page width.
        width_pt (float): The resolved width, in points.
        justification (str): Human-readable explanation of the decision, meant to
            be shown to a reviewer (human or, in the future, surfaced to an app UI).
        source (DecisionSource): Where the judgment came from.
        confidence (float, optional): Reserved for future LLM-assisted suggestions.
            None means "not applicable" (the default, deterministic path).
    """

    element_class: WidthClass
    width_pt: float
    justification: str
    source: DecisionSource
    confidence: Optional[float] = None

    @property
    def label(self) -> str:
        """
        Compatibility shim for existing code that only expects the legacy string
        label (packtools.sps.formats.pdf.enum.SINGLE_COLUMN_PAGE_LABEL /
        DOUBLE_COLUMN_PAGE_LABEL).

        Returns:
            str: The legacy label string for this decision's width class.
        """
        return self.element_class.value


@dataclass
class PageProfile:
    """
    Page/column geometry for a document or journal. Replaces the PAGE_ATTRIBUTES dict.

    Field defaults match today's packtools behavior (A4, 2 columns) and serve as
    the fallback for a journal that hasn't been calibrated yet - they are not meant
    to be read as "the universally correct value". Every field here is something
    confirmed, by measuring real published PDFs from more than one journal, to
    actually vary between journals (it is not derivable from the XML or from an
    image file alone) - that is why it is explicit per-journal configuration
    instead of an automatic heuristic.

    Args:
        page_width_pt (float): Page width, in points. Default matches A4 (21cm).
        page_height_pt (float): Page height, in points. Default matches A4 (29.7cm).
        margin_top_pt (float): Top margin, in points.
        margin_bottom_pt (float): Bottom margin, in points.
        margin_left_pt (float): Left margin, in points.
        margin_right_pt (float): Right margin, in points.
        default_column_count (int): Number of columns the document body uses by
            default (1 or 2, today).
        column_gap_pt (float): Spacing between columns, in points, when
            default_column_count > 1.
        figure_width_scale_override (float, optional): Escape hatch for the figure
            sizing problem confirmed in 2026-08 to not be a deterministic function
            of image DPI. When set, scales the ceiling width used for a figure's
            layout class (see renderer/docx/figure.py::add_figure) by this
            factor, so a journal can be calibrated to render narrower (or wider)
            than its raw column/content width would otherwise produce. None
            means "use the ceiling as computed, no adjustment". Only apply this
            when it has been calibrated against a real published PDF for that
            journal - see profiles/1809-4392.json for a calibrated example and
            profiles/1677-941X.json's known_limitations for a case where a
            single per-journal scalar was tried and found NOT to fit (the
            journal's own Figure 1 needs to be *larger*, not smaller, than its
            trustworthy natural size - the opposite direction), so it was left
            unset there rather than guessed.
    """

    page_width_pt: float = 595.28
    page_height_pt: float = 841.89
    margin_top_pt: float = 99.21
    margin_bottom_pt: float = 56.69
    margin_left_pt: float = 56.69
    margin_right_pt: float = 56.69
    default_column_count: int = 2
    column_gap_pt: float = 15.0
    figure_width_scale_override: Optional[float] = None

    @property
    def content_width_pt(self) -> float:
        """float: Page width minus left and right margins, in points."""
        return self.page_width_pt - self.margin_left_pt - self.margin_right_pt

    def column_width_pt(self, column_count: int) -> float:
        """
        Compute the width available to a single column, in points.

        Args:
            column_count (int): Number of columns the body is currently using.
                1 means the full content width (no column gap to subtract).

        Returns:
            float: The width, in points, available to one column.
        """
        if column_count <= 1:
            return self.content_width_pt
        return (self.content_width_pt - self.column_gap_pt * (column_count - 1)) / column_count

    def to_dict(self) -> dict:
        """
        Returns:
            dict: This profile's fields, suitable for JSON serialization.
        """
        return {
            "page_width_pt": self.page_width_pt,
            "page_height_pt": self.page_height_pt,
            "margin_top_pt": self.margin_top_pt,
            "margin_bottom_pt": self.margin_bottom_pt,
            "margin_left_pt": self.margin_left_pt,
            "margin_right_pt": self.margin_right_pt,
            "default_column_count": self.default_column_count,
            "column_gap_pt": self.column_gap_pt,
            "figure_width_scale_override": self.figure_width_scale_override,
        }

    def to_page_attributes(self, base: dict) -> dict:
        """
        Build a page_attributes-shaped dict (as consumed by
        packtools.sps.formats.pdf.renderer.docx.section.docx_setup_sections and
        related legacy code) by overriding base's page size with this profile's
        values. Margins are not overridden yet - no journal calibrated so far
        has needed a margin different from the packtools default.

        Args:
            base (dict): The starting page_attributes dict, typically
                packtools.sps.formats.pdf.enum.PAGE_ATTRIBUTES.

        Returns:
            dict: A new dict, base with page_width/page_height overridden.
        """
        from docx.shared import Pt

        merged = dict(base)
        merged["page_width"] = Pt(self.page_width_pt)
        merged["page_height"] = Pt(self.page_height_pt)
        return merged

    @classmethod
    def from_dict(cls, data: dict) -> "PageProfile":
        """
        Build a PageProfile from a (possibly partial) dict, e.g. loaded from
        profiles/{issn_epub}.json. Only overrides the fields that are present -
        anything missing falls back to the default (A4, 2 columns).

        Args:
            data (dict): Field values to override, matching PageProfile.to_dict()'s
                keys. May be a subset of the fields.

        Returns:
            PageProfile: A profile with the given fields overridden.
        """
        defaults = cls()
        merged = {**defaults.to_dict(), **{k: v for k, v in data.items() if v is not None}}
        return cls(**merged)


def load_profile(issn_epub: str, profiles_dir: Optional[str] = None) -> PageProfile:
    """
    Load a journal's calibrated page profile from profiles/{issn_epub}.json.

    The electronic ISSN is used as the lookup key because it is already what
    SciELO's own asset storage uses (minio.scielo.br/documentstore/{issn_epub}/...),
    so it can be read directly from the XML being processed (<issn pub-type="epub">)
    without needing a separate, manually-supplied journal identifier.

    Profiles are stored one file per journal, rather than in a single registry
    file, so that calibrating one journal doesn't produce merge conflicts with
    another and the registry doesn't turn into a single ever-growing file as more
    of SciELO's ~330 active journals get calibrated.

    Args:
        issn_epub (str): The journal's electronic ISSN, e.g. "1809-4392".
        profiles_dir (str, optional): Directory containing the profile JSON files.
            Defaults to the profiles/ directory shipped alongside this module.

    Returns:
        PageProfile: The calibrated profile, or the default (A4, 2 columns) when
        the journal hasn't been calibrated yet - this function never raises for a
        missing profile, matching item 02's requirement to always have a default
        when no explicit configuration is given.
    """
    import json
    import os

    if profiles_dir is None:
        profiles_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "profiles")

    path = os.path.join(profiles_dir, f"{issn_epub}.json")
    try:
        with open(path, encoding="utf-8") as f:
            entry = json.load(f)
    except (FileNotFoundError, TypeError):
        return PageProfile()

    page_data = entry.get("page", {})
    return PageProfile.from_dict(page_data)


class LayoutConfig:
    """
    Central layout context that an XML-to-PDF generation run consults.

    One instance per document (a journal's PageProfile can be reused across
    documents from the same journal). Table and figure rendering call
    decide_table_layout / decide_figure_layout instead of each computing their
    own notion of available width, and use full_width() instead of duplicating
    section break/restore logic when an element needs to span the full page.

    Args:
        profile (PageProfile, optional): The page geometry to use. Defaults to a
            new PageProfile() (A4, 2 columns).
        column_count (int, optional): The body's starting column count. Defaults
            to profile.default_column_count.
    """

    def __init__(self, profile: Optional[PageProfile] = None, column_count: Optional[int] = None):
        self.profile = profile or PageProfile()
        self._column_count = column_count if column_count is not None else self.profile.default_column_count
        self._stack: List[int] = []

    @property
    def column_count(self) -> int:
        """int: The body's current column count (changes temporarily inside full_width())."""
        return self._column_count

    @property
    def column_width_pt(self) -> float:
        """float: Width available to the current column, in points."""
        return self.profile.column_width_pt(self._column_count)

    @contextmanager
    def full_width(self):
        """
        Temporarily switch to a single, full-width column (for a table/figure
        too wide for the current column layout) and restore the previous column
        count on exit - including nested calls, via an internal stack.

        Replaces the section break/restore mechanics duplicated across the
        table/figure rendering code for wide elements.

        Yields:
            LayoutConfig: self, with column_count temporarily set to 1.
        """
        self._stack.append(self._column_count)
        self._column_count = 1
        try:
            yield self
        finally:
            self._column_count = self._stack.pop()

    def decide_table_layout(
        self, n_columns: int, column_min_widths_pt: Optional[List[float]] = None
    ) -> LayoutDecision:
        """
        Decide whether a table fits within the current column or needs the full
        page width, given either its real per-column minimum widths (preferred)
        or just its column count (fallback heuristic, matching today's ">4
        columns" rule but explicitly labeled as a heuristic rather than a
        measurement).

        Args:
            n_columns (int): Number of columns in the table.
            column_min_widths_pt (list of float, optional): Minimum width, in
                points, required by each column. When given, the decision is
                based on measured geometry instead of the column-count heuristic.

        Returns:
            LayoutDecision: The width class, resolved width, and justification.
        """
        available = self.column_width_pt
        if column_min_widths_pt:
            required = sum(column_min_widths_pt)
            fits = required <= available
            source = DecisionSource.MEASURED
            basis = (
                f"sum of minimum column widths ({required:.1f}pt) vs. "
                f"available column width ({available:.1f}pt)"
            )
            width_if_fits = required
        else:
            fits = n_columns <= 4
            source = DecisionSource.HEURISTIC
            basis = f"column count ({n_columns}) vs. heuristic threshold (4) - no real width measured"
            width_if_fits = available

        if fits:
            return LayoutDecision(
                element_class=WidthClass.WITHIN_COLUMN,
                width_pt=width_if_fits,
                justification=f"fits within the available column - {basis}",
                source=source,
            )
        return LayoutDecision(
            element_class=WidthClass.FULL_PAGE_WIDTH,
            width_pt=self.profile.column_width_pt(1),
            justification=f"exceeds the available column width - {basis}",
            source=source,
        )

    def decide_figure_layout(self, natural_width_pt: float, threshold: float = 0.9) -> LayoutDecision:
        """
        Decide whether a figure fits within the current column or needs the full
        page width, given its natural (intrinsic) width.

        Args:
            natural_width_pt (float): The figure's natural width, in points
                (typically derived from its pixel width and a trustworthy DPI).
            threshold (float): Fraction of the available column width above
                which a figure is considered too wide to stay within the column.
                Defaults to 0.9.

        Returns:
            LayoutDecision: The width class, resolved width, and justification.
        """
        available = self.column_width_pt
        if natural_width_pt >= available * threshold:
            return LayoutDecision(
                element_class=WidthClass.FULL_PAGE_WIDTH,
                width_pt=self.profile.column_width_pt(1),
                justification=(
                    f"natural image width ({natural_width_pt:.1f}pt) >= "
                    f"{threshold:.0%} of the available column width ({available:.1f}pt)"
                ),
                source=DecisionSource.MEASURED,
            )
        return LayoutDecision(
            element_class=WidthClass.WITHIN_COLUMN,
            width_pt=natural_width_pt,
            justification=(
                f"natural image width ({natural_width_pt:.1f}pt) is below "
                f"{threshold:.0%} of the available column width ({available:.1f}pt)"
            ),
            source=DecisionSource.MEASURED,
        )
