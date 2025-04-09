from packtools.sps.models.accessibility_data import AccessibilityData
from sympy.physics.vector.printing import params

from packtools.sps.validation.utils import build_response


class AccessibilityDataValidation:
    def __init__(self, node, params):
        self.accessibility_data = AccessibilityData(node).data
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

    def validate_alt_text(self):
        """Validates that <alt-text> has a maximum of 120 characters and contains only allowed characters."""
        alt_text = self.accessibility_data.get("alt_text")
        if not alt_text:
            error_level = self.params["alt_text_exist_error_level"]
            valid = False
        elif len(alt_text) > 120:
            error_level = self.params["alt_text_content_error_level"]
            valid = False
        else:
            error_level = None
            valid = True

        return build_response(
            title="<alt-text> validation",
            parent=self.accessibility_data,
            item="alt-text",
            sub_item=None,
            is_valid=valid,
            validation_type="format",
            expected="Up to 120 characters",
            obtained=alt_text,
            advice="Ensure <alt-text> is provided and does not exceed 120 characters to support accessibility.",
            error_level=error_level,
            data=self.accessibility_data,
        )

    def validate_long_desc(self):
        """Validates that <long-desc> is present and has more than 120 characters."""
        long_desc = self.accessibility_data.get("long_desc")

        if not long_desc:
            error_level = self.params["long_desc_exist_error_level"]
            valid = False
        elif len(long_desc) <= 120:
            error_level = self.params["long_desc_content_error_level"]
            valid = False
        else:
            error_level = None
            valid = True

        return build_response(
            title="<long-desc> validation",
            parent=self.accessibility_data,
            item="long-desc",
            sub_item=None,
            is_valid=valid,
            validation_type="format",
            expected="More than 120 characters",
            obtained=long_desc,
            advice="Ensure <long-desc> is provided and contains more than 120 characters to support accessibility.",
            error_level=error_level,
            data=self.accessibility_data,
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
            data=self.accessibility_data,
        )

    def validate_content_type(self):
        """Validates the @content-type attribute for machine-generated content when applicable."""
        content_type = self.accessibility_data.get("content_type")
        valid = content_type in self.params["content_types"]
        return build_response(
            title="@content-type validation",
            parent=self.accessibility_data,
            item="content-type",
            sub_item=None,
            is_valid=valid,
            validation_type="match",
            expected=self.params["content_types"],
            obtained=content_type,
            advice=f'In <long-desc> or <alt-text> replace @content-type by one of {self.params["content_types"]}',
            error_level=self.params["content_type_error_level"],
            data=self.accessibility_data,
        )

    def validate_speaker_and_speech(self):
        """Validates that <speaker> and <speech> elements are present when required in transcript sections."""
        speakers = self.accessibility_data.get("speakers", [])

        if not speakers:
            valid = False
            obtained = "Missing"
            advice = (
                "Use <speaker> and <speech> inside <sec sec-type=\"transcript\"> to mark dialogues. "
                "Refer to SPS 1.10 docs for details."
            )
        else:
            valid = True
            obtained = "Present"
            advice = "Dialogue is properly marked with <speaker> and <speech> elements."

        return build_response(
            title="<speaker> and <speech> validation",
            parent=self.accessibility_data,
            item="speakers",
            sub_item=None,
            is_valid=valid,
            validation_type="exist",
            expected="Present in dialogue transcripts",
            obtained=obtained,
            advice=advice,
            error_level=self.params["speaker_speech_error_level"],
            data=self.accessibility_data,
        )

    def validate_media_structure(self):  # corrigir o nome do método
        """Checks if accessibility elements are correctly structured within media."""
        valid_tags = {"graphic", "inline-graphic", "media", "inline-media"}  # parâmetro
        valid = self.accessibility_data.get("tag") in valid_tags
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
            data=self.accessibility_data,
        )
