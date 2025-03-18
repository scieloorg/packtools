from packtools.sps.validation.utils import build_response
from packtools.sps.validation.visual_resource_base import VisualResourceBaseValidation


class MediaValidation(VisualResourceBaseValidation):
    def validate(self):
        """Executes all defined validations."""
        yield self.validate_mime_type()
        yield self.validate_mime_subtype()
        yield from super().validate()

    def validate_mime_type(self):
        """Ensures @mime-type has a valid value."""
        valid_mime_types = {"application", "video", "audio"}
        mime_type = self.data.get("mimetype")
        valid = mime_type in valid_mime_types

        return build_response(
            title="@mime-type validation",
            parent=self.data,
            item="mimetype",
            sub_item=None,
            is_valid=valid,
            validation_type="match",
            expected=f"One of {valid_mime_types}",
            obtained=mime_type,
            advice="Use a valid @mime-type (application, video, audio).",
            error_level=self.params["mime_type_error_level"],
            data=self.data,
        )

    def validate_mime_subtype(self):
        """Validates that @mime-subtype matches the correct extensions for specific formats."""
        required_subtypes = {"video": "mp4", "audio": "mp3", "application": "zip"}
        mime_type = self.data.get("mimetype")
        mime_subtype = self.data.get("mime_subtype")
        valid = (
            mime_type not in required_subtypes
            or required_subtypes[mime_type] == mime_subtype
        )

        return build_response(
            title="@mime-subtype validation",
            parent=self.data,
            item="mime_subtype",
            sub_item=None,
            is_valid=valid,
            validation_type="match",
            expected=required_subtypes.get(mime_type, "Valid subtype"),
            obtained=mime_subtype,
            advice=f"For {mime_type}, use {required_subtypes.get(mime_type)} as @mime-subtype.",
            error_level=self.params["mime_subtype_error_level"],
            data=self.data,
        )
