from lxml import etree
from packtools.sps.validation.utils import build_response
from packtools.sps.validation.accessibility_data import AccessibilityDataValidation


class MediaValidation:
    """Class for validating <media> and <inline-media> elements in XML."""

    def __init__(self, media_data, xml_tree, params):
        """
        Initializes the media validation.

        Args:
            media_data (dict): Extracted media data
            xml_tree (etree.ElementTree): XML tree of the article
            params (dict): Validation parameters
        """
        self.media_data = media_data
        self.xml_tree = xml_tree
        self.params = params

    def validate(self):
        """Executes all defined validations."""
        yield self.validate_id()
        yield self.validate_mime_type()
        yield self.validate_mime_subtype()
        yield self.validate_xlink_href()
        yield from AccessibilityDataValidation(self.media_data, self.xml_tree, self.params).validate()

    def validate_id(self):
        """Checks if the @id attribute is present."""
        valid = bool(self.media_data.get("id"))
        return build_response(
            title="@id attribute validation",
            parent=self.media_data,
            item="media",
            sub_item=None,
            is_valid=valid,
            validation_type="exist",
            expected="Present",
            obtained="Missing" if not valid else "Present",
            advice="Ensure @id is included.",
            error_level=self.params["media_attributes_error_level"],
            data=self.media_data
        )

    def validate_mime_type(self):
        """Ensures @mime-type has a valid value."""
        valid_mime_types = {"application", "video", "audio"}
        mime_type = self.media_data.get("mimetype")
        valid = mime_type in valid_mime_types

        return build_response(
            title="@mime-type validation",
            parent=self.media_data,
            item="mimetype",
            sub_item=None,
            is_valid=valid,
            validation_type="match",
            expected=f"One of {valid_mime_types}",
            obtained=mime_type,
            advice="Use a valid @mime-type (application, video, audio).",
            error_level=self.params["mime_type_error_level"],
            data=self.media_data
        )

    def validate_mime_subtype(self):
        """Validates that @mime-subtype matches the correct extensions for specific formats."""
        required_subtypes = {"video": "mp4", "audio": "mp3", "application": "zip"}
        mime_type = self.media_data.get("mimetype")
        mime_subtype = self.media_data.get("mime_subtype")
        valid = mime_type not in required_subtypes or required_subtypes[mime_type] == mime_subtype

        return build_response(
            title="@mime-subtype validation",
            parent=self.media_data,
            item="mime_subtype",
            sub_item=None,
            is_valid=valid,
            validation_type="match",
            expected=required_subtypes.get(mime_type, "Valid subtype"),
            obtained=mime_subtype,
            advice=f"For {mime_type}, use {required_subtypes.get(mime_type)} as @mime-subtype.",
            error_level=self.params["mime_subtype_error_level"],
            data=self.media_data
        )

    def validate_xlink_href(self):
        """Ensures @xlink:href contains a valid file reference."""
        xlink_href = self.media_data.get("xlink_href")
        valid = bool(xlink_href and "." in xlink_href and len(xlink_href.split(".")) == 2)

        return build_response(
            title="@xlink:href validation",
            parent=self.media_data,
            item="xlink_href",
            sub_item=None,
            is_valid=valid,
            validation_type="format",
            expected="File name with extension",
            obtained=xlink_href,
            advice="Provide a valid file name with its extension in @xlink:href.",
            error_level=self.params["xlink_href_error_level"],
            data=self.media_data
        )
