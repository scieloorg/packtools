import os

from packtools.sps.validation.accessibility_data import \
    AccessibilityDataValidation
from packtools.sps.validation.utils import build_response


class VisualResourceBaseValidation:
    def __init__(self, data, params):
        self.data = data
        self.params = params
        self.accessibility_validation = AccessibilityDataValidation(
            data, self.params
        )

    def validate(self):
        yield self.validate_id()
        yield self.validate_xlink_href()
        yield from self.accessibility_validation.validate()

    def validate_id(self):
        xml = self.data.get("xml")
        tag = self.data.get("tag")
        if tag.startswith("inline-"):
            valid = True
            expected = None
        else:
            valid = bool(self.data.get("id"))
            elem = xml[:xml.find(">")+1]
            expected = f"id for {elem}"
        return build_response(
            title="@id",
            parent=self.data,
            item=tag,
            sub_item=None,
            is_valid=valid,
            validation_type="exist",
            expected=expected,
            obtained=self.data.get("id"),
            advice=f'Add id="" to {xml}',
            error_level=self.params["media_attributes_error_level"],
            data=self.data,
        )

    def validate_xlink_href(self):
        xlink_href = self.data.get("xlink_href")
        name, ext = os.path.splitext(xlink_href)
        valid = ext[1:] in self.params["valid_extension"]

        return build_response(
            title="@xlink:href validation",
            parent=self.data,
            item="xlink_href",
            sub_item=None,
            is_valid=valid,
            validation_type="format",
            expected="File name with extension",
            obtained=xlink_href,
            advice=f'In @xlink:href, provide a valid file name with its extension in {self.params["valid_extension"]}.',
            error_level=self.params["xlink_href_error_level"],
            data=self.data,
        )

    def validate_accessibility(self):
        yield from self.accessibility_validation.validate()
