import os
from packtools.sps.validation.visual_resource_base import VisualResourceBaseValidation
from packtools.sps.validation.utils import build_response
from packtools.sps.models.graphic import XmlGraphic


class GraphicValidation(VisualResourceBaseValidation):
    """
    Validation class for <graphic> and <inline-graphic> elements according to SPS 1.10.

    Validates:
    - @id attribute (required for both <graphic> and <inline-graphic>)
    - @xlink:href attribute (required, with valid file extension)
    - File extensions (.jpg, .jpeg, .png, .tif, .tiff, .svg)
    - .svg only allowed inside <alternatives>

    Note: Accessibility validation (<alt-text>, <long-desc>) is handled separately
    by XMLAccessibilityDataValidation in the validation pipeline to avoid duplicates.
    """

    def validate(self):
        """Execute all validations for graphic/inline-graphic elements."""
        yield self.validate_id()
        yield self.validate_xlink_href()
        yield from self.validate_svg_in_alternatives()
        # Note: Accessibility validation is handled by the dedicated XMLAccessibilityDataValidation
        # in the pipeline to avoid duplicate validation entries in reports

    def validate_id(self):
        """
        Validate @id attribute is present in <graphic> and <inline-graphic>.

        Per SPS 1.10 specification, @id is required for both <graphic> and
        <inline-graphic> elements. This overrides the base class behavior which
        exempts inline-* elements.
        """
        xml = self.data.get("xml")
        tag = self.data.get("tag")
        id_value = self.data.get("id")

        valid = bool(id_value)
        elem = xml[:xml.find(">")+1] if xml else tag

        return build_response(
            title="@id",
            parent=self.data,
            item=tag,
            sub_item=None,
            is_valid=valid,
            validation_type="exist",
            expected="@id attribute",
            obtained=id_value,
            advice=f'Add id="" to {elem}' if not valid else None,
            error_level=self.params["media_attributes_error_level"],
            data=self.data,
        )

    def validate_xlink_href(self):
        """
        Override to validate @xlink:href presence before delegating to the base
        class extension check.

        The inherited method calls os.path.splitext(xlink_href) unconditionally,
        which raises TypeError when the attribute is absent. This override:
        1. Returns an ERROR response when @xlink:href is missing.
        2. Delegates to the base implementation when the attribute is present,
           so extension validation runs normally.
        """
        xlink_href = self.data.get("xlink_href")
        if not xlink_href:
            return build_response(
                title="@xlink:href",
                parent=self.data,
                item=self.data.get("tag"),
                sub_item=None,
                is_valid=False,
                validation_type="exist",
                expected="@xlink:href attribute with valid file extension",
                obtained=None,
                advice=(
                    f'Add xlink:href="filename.ext" to '
                    f'<{self.data.get("tag")}> '
                    f'(valid extensions: jpg, jpeg, png, tif, tiff, svg)'
                ),
                error_level=self.params["xlink_href_error_level"],
                data=self.data,
            )
        return super().validate_xlink_href()

    def validate_svg_in_alternatives(self):
        """
        Validate that .svg extension is only used when <graphic> is inside <alternatives>.

        Per SPS 1.10 specification:
        - .svg files are only allowed when the graphic is inside <alternatives>
        - Other formats (.jpg, .jpeg, .png, .tif, .tiff) can be used anywhere

        Yields:
            dict: Validation response
        """
        xlink_href = self.data.get("xlink_href")
        parent_tag = self.data.get("parent_tag")

        if not xlink_href:
            return

        _, ext = os.path.splitext(xlink_href)
        ext = ext.lower()

        if ext == ".svg":
            is_valid = parent_tag == "alternatives"

            yield build_response(
                title="SVG in alternatives",
                parent=self.data,
                item=self.data.get("tag"),
                sub_item="xlink_href",
                is_valid=is_valid,
                validation_type="format",
                expected="<graphic> with .svg extension inside <alternatives>",
                obtained=f"{self.data.get('tag')} with .svg inside <{parent_tag}>",
                advice=(
                    f"SVG files are only allowed inside <alternatives>. "
                    f"The file '{xlink_href}' is currently in <{parent_tag}>. "
                    f"Either move this <graphic> inside <alternatives> or use a "
                    f"different format (.jpg, .png, .tif)."
                ) if not is_valid else None,
                error_level=self.params.get("svg_error_level", "ERROR"),
                data=self.data,
            )


class XMLGraphicValidation:
    """
    Validates all <graphic> and <inline-graphic> elements in an XML document.

    This class follows the same pattern as XMLMediaValidation and
    XMLAccessibilityDataValidation. It iterates through all graphic elements
    found in the document and validates each one.
    """

    def __init__(self, xmltree, params):
        self.params = params
        self.xml_graphic = XmlGraphic(xmltree)

    def validate(self):
        """
        Validate all graphic and inline-graphic elements in the document.

        Yields validation results for each graphic element found.
        """
        for data in self.xml_graphic.data:
            validator = GraphicValidation(data, self.params)
            yield from validator.validate()
