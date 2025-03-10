from lxml import etree
from packtools.sps.validation.utils import build_response


class AccessibilityDataValidation:
    def __init__(self, accessibility_data, xml_tree, params):
        """
        Initializes accessibility validation for multimedia elements.

        Args:
            accessibility_data (dict): Accessibility data extracted from the model
            xml_tree (etree.ElementTree): XML tree of the article
            params (dict): Validation configuration parameters
        """
        self.accessibility_data = accessibility_data
        self.xml_tree = xml_tree
        self.params = params

    def validate(self):
        """
        Executes all defined validations.
        """
        yield self.validate_alt_text()
        yield self.validate_long_desc()
        yield self.validate_transcript()
        yield self.validate_content_type()
        yield self.validate_speaker_and_speech()
        yield self.validate_media_structure()
        yield self.validate_cross_references()

    def validate_alt_text(self):
        """Validates that <alt-text> has a maximum of 120 characters and contains only allowed characters."""
        alt_text = self.accessibility_data.get("alt_text")
        valid = bool(alt_text) and len(alt_text) <= 120
        return build_response(
            title="<alt-text> validation",
            parent=self.accessibility_data,
            item="alt-text",
            sub_item=None,
            is_valid=valid,
            validation_type="length",
            expected="Up to 120 characters",
            obtained=len(alt_text) if alt_text else "Missing",
            advice="Provide an alternative text with a maximum of 120 characters.",
            error_level=self.params["alt_text_error_level"],
            data=self.accessibility_data
        )

    def validate_long_desc(self):
        """Validates that <long-desc> has more than 120 characters."""
        long_desc = self.accessibility_data.get("long_desc")
        valid = bool(long_desc) and len(long_desc) > 120
        return build_response(
            title="<long-desc> validation",
            parent=self.accessibility_data,
            item="long-desc",
            sub_item=None,
            is_valid=valid,
            validation_type="length",
            expected="More than 120 characters",
            obtained=len(long_desc) if long_desc else "Missing",
            advice="Provide a long description with more than 120 characters.",
            error_level=self.params["long_desc_error_level"],
            data=self.accessibility_data
        )

    def validate_transcript(self):
        """Checks for the presence of a transcript (<sec sec-type='transcript'>) for media."""
        transcript = self.accessibility_data.get("transcript")
        valid = bool(transcript)
        return build_response(
            title="Transcript validation",
            parent=self.accessibility_data,
            item="transcript",
            sub_item=None,
            is_valid=valid,
            validation_type="exist",
            expected="Present",
            obtained="Missing" if not transcript else "Present",
            advice="Provide a transcript for videos and audio files.",
            error_level=self.params["transcript_error_level"],
            data=self.accessibility_data
        )

    def validate_content_type(self):
        """Validates the @content-type attribute for machine-generated content when applicable."""
        content_type = self.accessibility_data.get("content_type")
        valid = content_type == "machine-generated"
        return build_response(
            title="@content-type validation",
            parent=self.accessibility_data,
            item="content-type",
            sub_item=None,
            is_valid=valid,
            validation_type="match",
            expected="machine-generated",
            obtained=content_type,
            advice="If applicable, use 'machine-generated' as the content-type.",
            error_level=self.params["content_type_error_level"],
            data=self.accessibility_data
        )

    def validate_speaker_and_speech(self):
        """Ensures that <speaker> and <speech> are used correctly in transcripts."""
        speakers = self.accessibility_data.get("speakers", [])
        valid = bool(speakers)
        return build_response(
            title="<speaker> and <speech> validation",
            parent=self.accessibility_data,
            item="speakers",
            sub_item=None,
            is_valid=valid,
            validation_type="exist",
            expected="Present",
            obtained="Missing" if not speakers else "Present",
            advice="Ensure proper markup for dialogues.",
            error_level=self.params["speaker_speech_error_level"],
            data=self.accessibility_data
        )

    def validate_media_structure(self):
        """Checks if accessibility elements are correctly structured within media."""
        valid_tags = {"graphic", "inline-graphic", "media", "inline-media"}
        valid = self.accessibility_data.get("media_type") in valid_tags
        return build_response(
            title="Media structure validation",
            parent=self.accessibility_data,
            item="media",
            sub_item=None,
            is_valid=valid,
            validation_type="structure",
            expected=f"One of the allowed types: {valid_tags}",
            obtained=self.accessibility_data.get("media_type"),
            advice="Ensure that accessibility elements are placed within appropriate media types.",
            error_level=self.params["media_structure_error_level"],
            data=self.accessibility_data
        )

    def validate_cross_references(self):
        """Checks cross-references between media and transcripts."""
        media_refs = self.accessibility_data.get("xref_refs", [])
        valid = bool(media_refs)
        return build_response(
            title="Cross-references validation",
            parent=self.accessibility_data,
            item="xref",
            sub_item=None,
            is_valid=valid,
            validation_type="exist",
            expected="Reference present",
            obtained="Missing" if not media_refs else "Present",
            advice="Ensure that media references a transcript.",
            error_level=self.params["cross_references_error_level"],
            data=self.accessibility_data
        )
