import os
from packtools.sps.validation.visual_resource_base import VisualResourceBaseValidation
from packtools.sps.validation.utils import build_response


class GraphicValidation(VisualResourceBaseValidation):
    """
    Validation class for <graphic> and <inline-graphic> elements according to SPS 1.10.
    
    Validates:
    - @id attribute (required for both <graphic> and <inline-graphic>)
    - @xlink:href attribute (required)
    - File extensions (.jpg, .jpeg, .png, .tif, .tiff, .svg)
    - .svg only allowed inside <alternatives>
    - Accessibility elements (<alt-text>, <long-desc>)
    """
    
    def validate(self):
        """Execute all validations for graphic/inline-graphic elements."""
        yield self.validate_id()
        yield self.validate_xlink_href()
        yield from self.validate_svg_in_alternatives()
        yield from self.accessibility_validation.validate()
    
    def validate_id(self):
        """
        Validate @id attribute is present in <graphic> and <inline-graphic>.
        
        Per SPS 1.10 specification, @id is required for both <graphic> and <inline-graphic> elements.
        This overrides the base class behavior which exempts inline-* elements.
        """
        xml = self.data.get("xml")
        tag = self.data.get("tag")
        id_value = self.data.get("id")
        
        valid = bool(id_value)
        elem = xml[:xml.find(">")+1] if xml else None
        expected = f"id for {elem}" if not valid else None
        
        return build_response(
            title="@id",
            parent=self.data,
            item=tag,
            sub_item=None,
            is_valid=valid,
            validation_type="exist",
            expected=expected,
            obtained=id_value,
            advice=f'Add id="" to {xml}' if not valid else None,
            error_level=self.params["media_attributes_error_level"],
            data=self.data,
        )
    
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
        
        # Get file extension
        _, ext = os.path.splitext(xlink_href)
        ext = ext.lower()
        
        # Check if it's an SVG file
        if ext == ".svg":
            # SVG is only valid inside <alternatives>
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
                    f"Either move this <graphic> inside <alternatives> or use a different format (.jpg, .png, .tif)."
                ) if not is_valid else None,
                error_level=self.params.get("svg_error_level", "ERROR"),
                data=self.data,
            )
