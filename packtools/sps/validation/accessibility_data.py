from packtools.sps.models.accessibility_data import XMLAccessibilityData
from packtools.sps.validation.utils import build_response


class XMLAccessibilityDataValidation:
    def __init__(self, xmltree, params):
        self.params = params
        self.xml_accessibility_data = XMLAccessibilityData(xmltree).data

    def validate(self):
        for item in self.xml_accessibility_data:
            validator = AccessibilityDataValidation(item, self.params)
            yield from validator.validate()


class AccessibilityDataValidation:
    def __init__(self, data, params):
        self.data = data
        self.params = params

    def validate(self):
        """
        Executes all defined validations.
        """
        yield from self.validate_alt_text()
        yield from self.validate_long_desc()
        yield self.validate_transcript()
        yield self.validate_speaker_and_speech()
        yield self.validate_structure()

    def validate_alt_text(self):
        """Validates that <alt-text> has a maximum of 120 characters and contains only allowed characters."""
        alt_text = self.data.get("alt_text")
        xml = self.data.get("alt_text_xml")
        if not alt_text:
            error_level = self.params["alt_text_exist_error_level"]
            valid = False
            validation_type = "exist"
            advice = "alt-text is missing. Provide a descriptive value."
        elif len(alt_text) > 120:
            error_level = self.params["alt_text_content_error_level"]
            valid = False
            validation_type = "format"
            advice = f"alt-text has {len(alt_text)} characters in {xml}. Provide text with up to 120 characters."
        else:
            error_level = None
            valid = True
            validation_type = "exist"
            advice = None

        yield build_response(
            title="<alt-text>",
            parent=self.data,
            item="alt-text",
            sub_item=None,
            is_valid=valid,
            validation_type=validation_type,
            expected="Up to 120 characters",
            obtained=alt_text,
            advice="The content is missing or exceeds 120 characters in the <alt-text> element. "
                   "Provide text with up to 120 characters to meet accessibility standards.",
            error_level=error_level,
            data=self.data,
        )

        alt_text_content_type = self.data.get("alt_text_content_type")
        if alt_text or alt_text_content_type:
            valid = alt_text_content_type in self.params["content_types"]
            yield build_response(
                title="@content-type",
                parent=self.data,
                item="alt-text",
                sub_item="@content-type",
                is_valid=valid,
                validation_type="exist",
                expected=self.params["content_types"],
                obtained=alt_text_content_type,
                advice=f"The value '{alt_text_content_type}' is invalid in <alt-text>/@content-type. "
                       f"Replace it with one of the accepted values: {self.params['content_types']}.",
                error_level=self.params["content_type_error_level"],
                data=self.data,
            )

    def validate_long_desc(self):
        """Validates that <long-desc> is present and has more than 120 characters."""
        long_desc = self.data.get("long_desc")
        long_desc_xml = self.data.get("long_desc_xml")
        if not long_desc:
            error_level = self.params["long_desc_exist_error_level"]
            valid = False
            validation_type = "exist"
            advice = "long-desc is missing. Provide a descriptive value."
        elif len(long_desc) <= 120:
            error_level = self.params["long_desc_content_error_level"]
            valid = False
            validation_type = "format"
            advice = f"long-desc has {len(long_desc)} characters in {long_desc_xml}. Provide text with more than to 120 characters."
        else:
            error_level = None
            valid = True
            validation_type = "exist"
            advice = None

        yield build_response(
            title="<long-desc>",
            parent=self.data,
            item="long-desc",
            sub_item=None,
            is_valid=valid,
            validation_type=validation_type,
            expected="More than 120 characters",
            obtained=long_desc,
            advice="The content is missing or too short in the <long-desc> element. "
                   "Provide text with more than 120 characters to support accessibility.",
            error_level=error_level,
            data=self.data,
        )

        long_desc_content_type = self.data.get("long_desc_content_type")
        if long_desc or long_desc_content_type:
            valid = long_desc_content_type in self.params["content_types"]
            yield build_response(
                title="@content-type",
                parent=self.data,
                item="long-desc",
                sub_item="@content-type",
                is_valid=valid,
                validation_type="exist",
                expected=self.params["content_types"],
                obtained=long_desc_content_type,
                advice=f"The value '{long_desc_content_type}' is invalid in <long-desc>/@content-type. "
                       f"Replace it with one of the accepted values: {self.params['content_types']}.",
                error_level=self.params["content_type_error_level"],
                data=self.data,
            )

    def validate_transcript(self):
        """Checks for the presence of a transcript (<sec sec-type='transcript'>) for media."""
        transcript = self.data.get("transcript")
        valid = bool(transcript)
        return build_response(
            title="Transcript validation",
            parent=self.data,
            item="transcript",
            sub_item=None,
            is_valid=valid,
            validation_type="exist",
            expected="Present",
            obtained="Missing" if not transcript else "Present",
            advice="The transcript is missing in the media element. "
                   "Add a <sec sec-type='transcript'> section to provide accessible text alternatives. Refer to SPS 1.10 docs for details.",
            error_level=self.params["transcript_error_level"],
            data=self.data,
        )

    def validate_speaker_and_speech(self):
        """Validates that <speaker> and <speech> elements are present when required in transcript sections."""
        speakers = self.data.get("speakers", [])

        if not speakers:
            valid = False
            obtained = "Missing"
            advice=("Dialog elements are missing in the <sec sec-type='transcript'> section. "
                    "Use <speaker> and <speech> to represent the dialogue. Refer to SPS 1.10 docs for details.")
        else:
            valid = True
            obtained = "Present"
            advice = None

        return build_response(
            title="<speaker> and <speech> validation",
            parent=self.data,
            item="speakers",
            sub_item=None,
            is_valid=valid,
            validation_type="exist",
            expected="Present in dialogue transcripts",
            obtained=obtained,
            advice=advice,
            error_level=self.params["speaker_speech_error_level"],
            data=self.data,
        )

    def validate_structure(self):  # corrigir o nome do método
        """Checks if accessibility elements are correctly structured within media."""
        valid_tags = {"graphic", "inline-graphic", "media", "inline-media"}  # parâmetro
        tag = self.data.get("tag")
        valid = tag in valid_tags
        return build_response(
            title="structure",
            parent=self.data,
            item=tag,
            sub_item=None,
            is_valid=valid,
            validation_type="value in list",
            expected=valid_tags,
            obtained=tag,
            advice=f"Accessibility data is located in an invalid element: <{tag}>. "
                   f"Use one of the valid elements: {valid_tags}. Refer to SPS 1.10 docs for details.",
            error_level=self.params["structure_error_level"],
            data=self.data,
        )
