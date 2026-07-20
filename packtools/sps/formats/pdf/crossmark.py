"""
crossmark.py - Add Crossmark button to PDF files.

This module provides functionality to insert the Crossmark logo and hyperlink
into PDF files, along with relevant XMP metadata, as required by Crossref.

Reference: https://www.crossref.org/documentation/crossmark/
"""

import argparse
import csv
import io
import os
from xml.etree import ElementTree

from pypdf import PdfReader, PdfWriter, generic
from reportlab.pdfgen import canvas as rl_canvas

try:
    from PIL import Image as PILImage
    _PIL_AVAILABLE = True
except ImportError:
    _PIL_AVAILABLE = False


# Default logo bundled with the package
_ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
_DEFAULT_LOGO = os.path.join(_ASSETS_DIR, "CROSSMARK_Color_horizontal.png")

# Crossmark dialog URL template
_CROSSMARK_URL = (
    "https://crossmark.crossref.org/dialog"
    "?doi={doi}&domain=pdf&date_stamp={date_stamp}"
)

# XMP namespaces used for Crossmark metadata
_XMP_NAMESPACES = {
    "dc": "http://purl.org/dc/elements/1.1/",
    "prism": "http://prismstandard.org/namespaces/basic/2.0/",
    "crossmark": "http://crossref.org/crossmark/1.0/",
    "pdfx": "http://ns.adobe.com/pdfx/1.3/",
}

# Mapping: XMP field -> value template key
_XMP_FIELDS = {
    "dc:identifier": "doi:{doi}",
    "prism:doi": "{doi}",
    "prism:url": "https://doi.org/{doi}",
    "crossmark:MajorVersionDate": "{date_stamp}",
    "crossmark:DOI": "{doi}",
    "pdfx:doi": "{doi}",
    "pdfx:CrossmarkMajorVersionDate": "{date_stamp}",
}


def _compute_logo_rect(page_width, page_height, position, logo_width, logo_height,
                       margin=20):
    """
    Compute the (x, y) lower-left position for the logo given position name.

    PDF coordinate system has origin at bottom-left.

    Args:
        page_width (float): Width of the page in points.
        page_height (float): Height of the page in points.
        position (str): One of 'top-right', 'top-left', 'bottom-right', 'bottom-left'.
        logo_width (float): Width of the logo in points.
        logo_height (float): Height of the logo in points.
        margin (int): Margin from page edge in points.

    Returns:
        tuple: (x, y) lower-left coordinates for the logo.
    """
    if position == "top-right":
        x = page_width - logo_width - margin
        y = page_height - logo_height - margin
    elif position == "top-left":
        x = margin
        y = page_height - logo_height - margin
    elif position == "bottom-right":
        x = page_width - logo_width - margin
        y = margin
    elif position == "bottom-left":
        x = margin
        y = margin
    else:
        # Default to top-right
        x = page_width - logo_width - margin
        y = page_height - logo_height - margin
    return x, y


def _get_logo_height(logo_path, logo_width):
    """
    Calculate logo height maintaining aspect ratio.

    Args:
        logo_path (str): Path to the logo image file.
        logo_width (int): Desired width in points.

    Returns:
        float: Calculated height in points.
    """
    if _PIL_AVAILABLE:
        try:
            with PILImage.open(logo_path) as img:
                orig_w, orig_h = img.size
            return logo_width * orig_h / orig_w
        except Exception:
            pass
    # Fallback: assume typical horizontal logo aspect ratio ~4:1
    return logo_width / 4.0


def _build_xmp_packet(doi, date_stamp):
    """
    Build an XMP metadata packet string for Crossmark.

    Args:
        doi (str): DOI of the article (e.g., '10.1590/s0100-12345').
        date_stamp (str): Date of the major version (e.g., '2026-01-15').

    Returns:
        bytes: UTF-8 encoded XMP packet.
    """
    fields_xml = "\n".join(
        f"      <{field}>{value.format(doi=doi, date_stamp=date_stamp)}</{field}>"
        for field, value in _XMP_FIELDS.items()
    )

    ns_attrs = "\n        ".join(
        f'xmlns:{prefix}="{uri}"'
        for prefix, uri in _XMP_NAMESPACES.items()
    )

    xmp = (
        "<?xpacket begin='\ufeff' id='W5M0MpCehiHzreSzNTczkc9d'?>\n"
        "<x:xmpmeta xmlns:x=\"adobe:ns:meta/\">\n"
        "  <rdf:RDF xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\">\n"
        "    <rdf:Description rdf:about=\"\"\n"
        f"        {ns_attrs}>\n"
        f"{fields_xml}\n"
        "    </rdf:Description>\n"
        "  </rdf:RDF>\n"
        "</x:xmpmeta>\n"
        "<?xpacket end='w'?>"
    )
    return xmp.encode("utf-8")


def _merge_xmp_packet(existing_xmp_bytes, doi, date_stamp):
    """
    Merge Crossmark fields into an existing XMP packet, or create a new one.

    When existing XMP is present, the Crossmark fields are added to the
    existing rdf:Description block.  If a field already exists it is updated.

    Args:
        existing_xmp_bytes (bytes | None): Existing XMP packet bytes, or None.
        doi (str): DOI of the article.
        date_stamp (str): Date stamp string.

    Returns:
        bytes: Updated XMP packet bytes.
    """
    if not existing_xmp_bytes:
        return _build_xmp_packet(doi, date_stamp)

    # Register namespaces to avoid ns0 mangling
    for prefix, uri in _XMP_NAMESPACES.items():
        ElementTree.register_namespace(prefix, uri)
    ElementTree.register_namespace("x", "adobe:ns:meta/")
    ElementTree.register_namespace(
        "rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    )

    try:
        root = ElementTree.fromstring(existing_xmp_bytes)
    except ElementTree.ParseError:
        return _build_xmp_packet(doi, date_stamp)

    rdf_ns = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    desc_tag = f"{{{rdf_ns}}}Description"
    desc = root.find(f".//{desc_tag}")
    if desc is None:
        return _build_xmp_packet(doi, date_stamp)

    new_values = {
        field: value.format(doi=doi, date_stamp=date_stamp)
        for field, value in _XMP_FIELDS.items()
    }

    for prefixed_field, text in new_values.items():
        prefix, local = prefixed_field.split(":", 1)
        ns_uri = _XMP_NAMESPACES[prefix]
        clark = f"{{{ns_uri}}}{local}"
        elem = desc.find(clark)
        if elem is None:
            elem = ElementTree.SubElement(desc, clark)
        elem.text = text

    xmp_str = ElementTree.tostring(root, encoding="unicode", xml_declaration=False)
    return (
        "<?xpacket begin='\ufeff' id='W5M0MpCehiHzreSzNTczkc9d'?>\n"
        + xmp_str
        + "\n<?xpacket end='w'?>"
    ).encode("utf-8")


def _create_logo_overlay(page_width, page_height, x, y, logo_width, logo_height,
                         logo_path):
    """
    Create a single-page PDF overlay containing the Crossmark logo.

    Args:
        page_width (float): Width of the page in points.
        page_height (float): Height of the page in points.
        x (float): Left coordinate of the logo.
        y (float): Bottom coordinate of the logo.
        logo_width (float): Width of the logo in points.
        logo_height (float): Height of the logo in points.
        logo_path (str): Path to the logo image file.

    Returns:
        io.BytesIO: Buffer containing the overlay PDF.
    """
    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=(page_width, page_height))
    c.drawImage(
        logo_path,
        x, y,
        width=logo_width,
        height=logo_height,
        mask="auto",
        preserveAspectRatio=True,
    )
    c.save()
    buf.seek(0)
    return buf


def add_crossmark(
    input_pdf,
    output_pdf,
    doi,
    date_stamp,
    logo_path=None,
    position="top-right",
    width=150,
):
    """
    Insert the Crossmark logo with hyperlink and XMP metadata into a PDF.

    The logo is placed on the first page only.  All other pages are left
    unchanged.  Existing content is preserved.

    Args:
        input_pdf (str): Path to the input PDF file.
        output_pdf (str): Path for the output PDF file.
        doi (str): DOI of the article (e.g., '10.1590/s0100-12345').
        date_stamp (str): Date of the major version in YYYY-MM-DD format.
        logo_path (str | None): Path to the Crossmark logo PNG/JPEG image.
            Defaults to the bundled ``CROSSMARK_Color_horizontal.png``.
        position (str): Logo position on the first page.  One of
            ``'top-right'``, ``'top-left'``, ``'bottom-right'``,
            ``'bottom-left'``.  Defaults to ``'top-right'``.
        width (int): Desired logo width in points (1 pt ≈ 1/72 inch).
            Height is calculated automatically to preserve aspect ratio.
            Defaults to 150.

    Returns:
        None

    Raises:
        FileNotFoundError: If ``input_pdf`` or ``logo_path`` does not exist.
        ValueError: If ``doi`` or ``date_stamp`` is empty.
    """
    if not doi:
        raise ValueError("doi must not be empty")
    if not date_stamp:
        raise ValueError("date_stamp must not be empty")

    if logo_path is None:
        logo_path = _DEFAULT_LOGO

    if not os.path.exists(input_pdf):
        raise FileNotFoundError(f"Input PDF not found: {input_pdf}")
    if not os.path.exists(logo_path):
        raise FileNotFoundError(f"Logo file not found: {logo_path}")

    reader = PdfReader(input_pdf)
    writer = PdfWriter(clone_from=reader)

    # --- Process first page: add logo overlay ---
    first_page = writer.pages[0]
    page_width = float(first_page.mediabox.width)
    page_height = float(first_page.mediabox.height)

    logo_height = _get_logo_height(logo_path, width)
    x, y = _compute_logo_rect(page_width, page_height, position, width, logo_height)

    overlay_buf = _create_logo_overlay(
        page_width, page_height, x, y, width, logo_height, logo_path
    )
    overlay_page = PdfReader(overlay_buf).pages[0]
    first_page.merge_page(overlay_page)

    # --- Add URI annotation (clickable hyperlink) on first page ---
    crossmark_url = _CROSSMARK_URL.format(doi=doi, date_stamp=date_stamp)
    annotation_rect = [x, y, x + width, y + logo_height]
    writer.add_uri(0, crossmark_url, annotation_rect)

    # --- Update XMP metadata ---
    existing_xmp = None
    meta_ref = reader.root_object.get("/Metadata")
    if meta_ref is not None:
        try:
            existing_xmp = meta_ref.get_object().get_data()
        except Exception:
            pass

    xmp_bytes = _merge_xmp_packet(existing_xmp, doi, date_stamp)
    xmp_stream = generic.DecodedStreamObject()
    xmp_stream.set_data(xmp_bytes)
    xmp_stream.update({
        generic.NameObject("/Type"): generic.NameObject("/Metadata"),
        generic.NameObject("/Subtype"): generic.NameObject("/XML"),
    })
    xmp_ref = writer._add_object(xmp_stream)
    writer.root_object[generic.NameObject("/Metadata")] = xmp_ref

    # --- Write output ---
    output_dir = os.path.dirname(output_pdf)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(output_pdf, "wb") as f:
        writer.write(f)


def main():
    """CLI entry point for adding Crossmark to PDF files."""
    parser = argparse.ArgumentParser(
        description=(
            "Insert the Crossmark logo and metadata into a PDF file. "
            "Supports single-file and batch (CSV) modes."
        )
    )

    # Single-file mode arguments
    parser.add_argument(
        "--input",
        help="Path to the input PDF file.",
    )
    parser.add_argument(
        "--output",
        help="Path for the output PDF file.",
    )
    parser.add_argument(
        "--doi",
        help="DOI of the article (e.g., 10.1590/s0100-12345).",
    )
    parser.add_argument(
        "--date-stamp",
        dest="date_stamp",
        help="Date of the last major version in YYYY-MM-DD format.",
    )

    # Batch mode
    parser.add_argument(
        "--csv",
        dest="csv_file",
        help=(
            "CSV file for batch processing. "
            "Expected columns: doi, input_pdf, output_pdf, date_stamp. "
            "(output_pdf is optional; if omitted, a suffix '_cm' is added.)"
        ),
    )

    # Common options
    parser.add_argument(
        "--logo",
        dest="logo_path",
        default=None,
        help=(
            "Path to the Crossmark logo image. "
            "Defaults to the bundled CROSSMARK_Color_horizontal.png."
        ),
    )
    parser.add_argument(
        "--position",
        default="top-right",
        choices=["top-right", "top-left", "bottom-right", "bottom-left"],
        help="Position of the logo on the first page (default: top-right).",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=150,
        help="Logo width in points (default: 150).",
    )

    args = parser.parse_args()

    if args.csv_file:
        # Batch mode
        if not os.path.exists(args.csv_file):
            parser.error(f"CSV file not found: {args.csv_file}")

        with open(args.csv_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        for i, row in enumerate(rows, start=1):
            doi = row.get("doi", "").strip()
            input_pdf = row.get("input_pdf", "").strip()
            date_stamp = row.get("date_stamp", "").strip()
            output_pdf = row.get("output_pdf", "").strip()

            if not doi or not input_pdf or not date_stamp:
                print(
                    f"[Row {i}] Skipping: missing required fields "
                    f"(doi, input_pdf, date_stamp)."
                )
                continue

            if not output_pdf:
                base, ext = os.path.splitext(input_pdf)
                output_pdf = f"{base}_cm{ext}"

            try:
                add_crossmark(
                    input_pdf=input_pdf,
                    output_pdf=output_pdf,
                    doi=doi,
                    date_stamp=date_stamp,
                    logo_path=args.logo_path,
                    position=args.position,
                    width=args.width,
                )
                print(f"[Row {i}] Created: {output_pdf}")
            except Exception as exc:
                print(f"[Row {i}] Error processing {input_pdf}: {exc}")

    else:
        # Single-file mode
        missing = []
        if not args.input:
            missing.append("--input")
        if not args.doi:
            missing.append("--doi")
        if not args.date_stamp:
            missing.append("--date-stamp")
        if missing:
            parser.error(
                f"The following arguments are required in single-file mode: "
                + ", ".join(missing)
            )

        output_pdf = args.output
        if not output_pdf:
            base, ext = os.path.splitext(args.input)
            output_pdf = f"{base}_cm{ext}"

        add_crossmark(
            input_pdf=args.input,
            output_pdf=output_pdf,
            doi=args.doi,
            date_stamp=args.date_stamp,
            logo_path=args.logo_path,
            position=args.position,
            width=args.width,
        )
        print(f"Created: {output_pdf}")


if __name__ == "__main__":
    main()
