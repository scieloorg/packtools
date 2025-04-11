from packtools.sps.validation.utils import build_response
from packtools.sps.validation.visual_resource_base import VisualResourceBaseValidation
from packtools.sps.models.media import XmlMedias


class MediaValidation(VisualResourceBaseValidation):
    def validate(self):
        """Executes all defined validations."""
        yield self.validate_mime_type_and_subtype()
        yield from super().validate()

    def validate_mime_type_and_subtype(self):
        """Validates that @mime-subtype matches the correct extensions for specific formats."""
        mime_types_and_subtypes = self.params["mime_types_and_subtypes"]
        mime_type = self.data.get("mimetype")
        mime_subtype = self.data.get("mime_subtype")

        got = {"mimetype": mime_type, "mime-subtype": mime_subtype}
        valid = got in mime_types_and_subtypes

        return build_response(
            title="mime type and subtype",
            parent=self.data,
            item="mime type and subtype",
            sub_item=None,
            is_valid=valid,
            validation_type="value in lis",
            expected=mime_types_and_subtypes,
            obtained=got,
            advice=f"Use expected values: {mime_types_and_subtypes}",
            error_level=self.params["mime_type_error_level"],
            data=self.data,
        )


class XMLMediaValidation:
    def __init__(self, xmltree, params):
        self.params = params
        self.xml_media = XmlMedias(xmltree)

    def validate(self):
        for data in self.xml_media.data:
            validator = MediaValidation(data, self.params)
            yield from validator.validate()
