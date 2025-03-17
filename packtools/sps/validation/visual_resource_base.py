from packtools.sps.validation.utils import build_response
from packtools.sps.validation.accessibility_data import AccessibilityDataValidation


class VisualResourceBaseValidation:
    def __init__(self, node, data, params):
        self.node = node
        self.data = data
        self.params = params
        self.accessibility_validation = AccessibilityDataValidation(self.node, self.params)

    def validate(self):
        yield self.validate_id
        yield self.validate_xlink_href
        yield from self.accessibility_validation.validate()

    def validate_id(self):
        valid = bool(self.data.get("id"))
        return build_response(
            title="@id attribute validation",
            parent=self.data,
            item="media",
            sub_item=None,
            is_valid=valid,
            validation_type="exist",
            expected="Present",
            obtained="Missing" if not valid else "Present",
            advice="Ensure @id is included.",
            error_level=self.params["media_attributes_error_level"],
            data=self.data
        )

    def validate_xlink_href(self):
        xlink_href = self.data.get("xlink_href")
        valid = bool(xlink_href and "." in xlink_href and len(xlink_href.split(".")) == 2)
        return build_response(
            title="@xlink:href validation",
            parent=self.data,
            item="xlink_href",
            sub_item=None,
            is_valid=valid,
            validation_type="format",
            expected="File name with extension",
            obtained=xlink_href,
            advice="Provide a valid file name with its extension in @xlink:href.",#citar o contexto
            error_level=self.params["xlink_href_error_level"],
            data=self.data
        )

    def validate_accessibility(self):
        yield from self.accessibility_validation.validate()
