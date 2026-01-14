import gettext
from packtools.sps.models.accessibility_data import XMLAccessibilityData
from packtools.sps.validation.utils import build_response

_ = gettext.gettext


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
        yield from self.validate_alt_text_media_restriction()  # NOVA
        yield from self.validate_alt_text_not_duplicate_label_caption()  # NOVA
        yield from self.validate_decorative_figure_alt_text()  # NOVA
        yield from self.validate_long_desc()
        yield self.validate_transcript()
        yield self.validate_speaker_and_speech()
        yield self.validate_accessibility_data_structure()

    def validate_alt_text(self):
        """Validates that <alt-text> has a maximum of 120 characters and contains only allowed characters."""
        alt_text = self.data.get("alt_text")
        xml = self.data.get("alt_text_xml")

        if not alt_text:
            error_level = self.params["alt_text_exist_error_level"]
            valid = False
            validation_type = "exist"
            advice = "Missing <alt-text>. Provide a concise textual description of the visual element content."
            advice_text = _("Missing <alt-text>. Provide a concise textual description of the visual element content.")
            advice_params = {}
        elif len(alt_text) > 120:
            error_level = self.params["alt_text_content_error_level"]
            valid = False
            validation_type = "format"
            advice = f"alt-text has {len(alt_text)} characters in {xml}. Provide text with up to 120 characters."
            advice_text = _("alt-text has {length} characters in {xml}. Provide text with up to {max_length} characters.")
            advice_params = {"length": len(alt_text), "xml": xml, "max_length": 120}
        else:
            error_level = None
            valid = True
            validation_type = "exist"
            advice = None
            advice_text = None
            advice_params = None

        yield build_response(
            title="<alt-text>",
            parent=self.data,
            item="alt-text",
            sub_item=None,
            is_valid=valid,
            validation_type=validation_type,
            expected="Up to 120 characters",
            obtained=alt_text,
            advice=advice,
            error_level=error_level,
            data=self.data,
            advice_text=advice_text,
            advice_params=advice_params,
        )

        # CORREÇÃO: Só valida @content-type se o atributo estiver presente
        # @content-type é OPCIONAL, só obrigatório quando conteúdo é gerado por máquina
        alt_text_content_type = self.data.get("alt_text_content_type")
        if alt_text_content_type:  # Valida apenas quando atributo existe
            valid = alt_text_content_type in self.params["content_types"]

            if not valid:
                advice = (f'The value \'{alt_text_content_type}\' is invalid in {self.data.get("alt_text_xml")}. '
                         f'Replace it with one of the accepted values: {self.params["content_types"]}.')
                advice_text = _('The value {value} is invalid in {xml}. Replace it with one of the accepted values: {accepted_values}.')
                advice_params = {
                    "value": alt_text_content_type,
                    "xml": self.data.get("alt_text_xml"),
                    "accepted_values": str(self.params["content_types"])
                }
            else:
                advice = None
                advice_text = None
                advice_params = None

            yield build_response(
                title="@content-type",
                parent=self.data,
                item="alt-text",
                sub_item="@content-type",
                is_valid=valid,
                validation_type="value in list",
                expected=self.params["content_types"],
                obtained=alt_text_content_type,
                advice=advice,
                error_level=self.params["content_type_error_level"],
                data=self.data,
                advice_text=advice_text,
                advice_params=advice_params,
            )

    def validate_alt_text_media_restriction(self):
        """
        NOVA VALIDAÇÃO: Valida que <alt-text> em <media> e <inline-media> só ocorre para vídeo/áudio.

        Regra SPS 1.10:
        "Em <media> e <inline-media> o elemento <alt-text> só deverá ocorrer quando
        o formato do objeto for vídeo ou áudio, tendo os seguintes atributos para
        @mime-type e @mime-subtype: video/mp4, audio/mp3"
        """
        tag = self.data.get("tag")

        # Só valida para elementos <media> e <inline-media>
        if tag not in ("media", "inline-media"):
            return

        alt_text = self.data.get("alt_text")
        mimetype = self.data.get("mimetype")
        mime_subtype = self.data.get("mime_subtype")

        # Se não há alt-text, não precisa validar esta regra
        if not alt_text:
            return

        # alt-text só deve estar presente para video/mp4 ou audio/mp3
        valid_combinations = [
            ("video", "mp4"),
            ("audio", "mp3"),
        ]

        current = (mimetype, mime_subtype)
        valid = current in valid_combinations

        if not valid:
            advice = (
                f"In <{tag}>, <alt-text> should only be used for video (mp4) or audio (mp3) files. "
                f"Current mime-type is '{mimetype}' with mime-subtype '{mime_subtype}'. "
                f"For other file types (PDF, ZIP, XLSX), remove <alt-text> or consider using <long-desc> instead. "
                f"Refer to SPS 1.10 documentation for details."
            )
            advice_text = _(
                "In <{tag}>, <alt-text> should only be used for video (mp4) or audio (mp3) files. "
                "Current mime-type is {mimetype} with mime-subtype {mime_subtype}. "
                "For other file types (PDF, ZIP, XLSX), remove <alt-text> or consider using <long-desc> instead. "
                "Refer to SPS 1.10 documentation for details."
            )
            advice_params = {
                "tag": tag,
                "mimetype": mimetype or "undefined",
                "mime_subtype": mime_subtype or "undefined"
            }
        else:
            advice = None
            advice_text = None
            advice_params = None

        yield build_response(
            title="<alt-text> restriction for media",
            parent=self.data,
            item="alt-text",
            sub_item="media restriction",
            is_valid=valid,
            validation_type="value in list",
            expected=f"mime-type/mime-subtype combinations: {valid_combinations}",
            obtained=f"{mimetype}/{mime_subtype}",
            advice=advice,
            error_level=self.params.get("alt_text_media_restriction_error_level", "ERROR"),
            data=self.data,
            advice_text=advice_text,
            advice_params=advice_params,
        )

    def validate_alt_text_not_duplicate_label_caption(self):
        """
        NOVA VALIDAÇÃO: Valida que <alt-text> não copia o conteúdo de <label> ou <caption>.

        Regra SPS 1.10:
        "O conteúdo de <alt-text> não deve ser usado para substituir ou copiar
        a informação descrita em <label> ou <caption>"
        """
        alt_text = self.data.get("alt_text")

        # Se não há alt-text, não há o que validar
        if not alt_text:
            return

        label = self.data.get("parent_label")
        caption_title = self.data.get("parent_caption_title")

        # Normaliza strings para comparação (lowercase, sem espaços extras)
        alt_text_normalized = " ".join(alt_text.lower().split())

        duplicates_label = False
        duplicates_caption = False
        duplicated_element = None
        duplicated_content = None

        if label:
            label_normalized = " ".join(label.lower().split())
            duplicates_label = alt_text_normalized == label_normalized
            if duplicates_label:
                duplicated_element = "<label>"
                duplicated_content = label

        if caption_title and not duplicates_label:  # Só verifica caption se não duplicou label
            caption_normalized = " ".join(caption_title.lower().split())
            duplicates_caption = alt_text_normalized == caption_normalized
            if duplicates_caption:
                duplicated_element = "<caption><title>"
                duplicated_content = caption_title

        valid = not (duplicates_label or duplicates_caption)

        if not valid:
            advice = (
                f"<alt-text> content duplicates {duplicated_element}: '{duplicated_content}'. "
                f"The alt-text should provide unique descriptive information about the visual element, "
                f"not copy the label or caption. Provide a brief description of what the image shows. "
                f"Refer to SPS 1.10 documentation for examples."
            )
            advice_text = _(
                "<alt-text> content duplicates {element}: {content}. "
                "The alt-text should provide unique descriptive information about the visual element, "
                "not copy the label or caption. Provide a brief description of what the image shows. "
                "Refer to SPS 1.10 documentation for examples."
            )
            advice_params = {
                "element": duplicated_element,
                "content": duplicated_content
            }
        else:
            advice = None
            advice_text = None
            advice_params = None

        # Só reporta se houver problema
        if not valid:
            yield build_response(
                title="<alt-text> content uniqueness",
                parent=self.data,
                item="alt-text",
                sub_item="duplication check",
                is_valid=valid,
                validation_type="format",
                expected="Unique content (not copying label or caption)",
                obtained=alt_text,
                advice=advice,
                error_level=self.params.get("alt_text_duplication_error_level", "WARNING"),
                data=self.data,
                advice_text=advice_text,
                advice_params=advice_params,
            )

    def validate_decorative_figure_alt_text(self):
        """
        NOVA VALIDAÇÃO: Valida que figuras decorativas têm <alt-text>null</alt-text>.

        Regra SPS 1.10:
        "Figuras decorativas devem ter <alt-text>null</alt-text>"

        Nota: Esta validação identifica figuras potencialmente decorativas baseado em:
        - Ausência de <label>
        - Ausência de <caption> ou <title>
        - Elemento é <graphic> ou <inline-graphic> (não <media>)

        Se uma figura aparenta ser decorativa mas tem alt-text diferente de "null",
        um aviso é emitido.
        """
        alt_text = self.data.get("alt_text")
        tag = self.data.get("tag")

        # Não precisa validar se não há alt-text
        if not alt_text:
            return

        # Critério para identificar figura potencialmente decorativa:
        # - Não tem label
        # - Não tem caption/title
        # - É um graphic/inline-graphic (não media)
        label = self.data.get("parent_label")
        caption_title = self.data.get("parent_caption_title")

        is_graphic = tag in ("graphic", "inline-graphic")
        has_no_label = not label
        has_no_caption = not caption_title

        is_potentially_decorative = is_graphic and has_no_label and has_no_caption

        # Se parece ser decorativa e tem alt-text diferente de "null"
        if is_potentially_decorative and alt_text.lower().strip() != "null":
            valid = False
            advice = (
                f"This appears to be a decorative figure (no <label> or <caption>). "
                f"Decorative figures should have <alt-text>null</alt-text>. "
                f"Current alt-text: '{alt_text}'. "
                f"If this figure is informative and not decorative, add a proper <caption> and <label>. "
                f"Refer to SPS 1.10 documentation for examples."
            )
            advice_text = _(
                "This appears to be a decorative figure (no <label> or <caption>). "
                "Decorative figures should have <alt-text>null</alt-text>. "
                "Current alt-text: {current}. "
                "If this figure is informative and not decorative, add a proper <caption> and <label>. "
                "Refer to SPS 1.10 documentation for examples."
            )
            advice_params = {"current": alt_text}
        else:
            valid = True
            advice = None
            advice_text = None
            advice_params = None

        # Só reporta se houver problema
        if not valid:
            yield build_response(
                title="Decorative figure alt-text",
                parent=self.data,
                item="alt-text",
                sub_item="decorative",
                is_valid=valid,
                validation_type="format",
                expected="null (for decorative figures without label/caption)",
                obtained=alt_text,
                advice=advice,
                error_level=self.params.get("decorative_alt_text_error_level", "WARNING"),
                data=self.data,
                advice_text=advice_text,
                advice_params=advice_params,
            )

    def validate_long_desc(self):
        """Validates that <long-desc> is present and has more than 120 characters."""
        long_desc = self.data.get("long_desc")
        long_desc_xml = self.data.get("long_desc_xml")

        if not long_desc:
            error_level = self.params["long_desc_exist_error_level"]
            valid = False
            validation_type = "exist"
            advice = "Missing <long-desc>. Provide a detailed textual description of the visual element content."
            advice_text = _("Missing <long-desc>. Provide a detailed textual description of the visual element content.")
            advice_params = {}
        elif len(long_desc) <= 120:
            error_level = self.params["long_desc_content_error_level"]
            valid = False
            validation_type = "format"
            advice = f"long-desc has {len(long_desc)} characters in {long_desc_xml}. Provide text with more than to 120 characters."
            advice_text = _("long-desc has {length} characters in {xml}. Provide text with more than {min_length} characters.")
            advice_params = {"length": len(long_desc), "xml": long_desc_xml, "min_length": 120}
        else:
            error_level = None
            valid = True
            validation_type = "exist"
            advice = None
            advice_text = None
            advice_params = None

        yield build_response(
            title="<long-desc>",
            parent=self.data,
            item="long-desc",
            sub_item=None,
            is_valid=valid,
            validation_type=validation_type,
            expected="More than 120 characters",
            obtained=long_desc,
            advice=advice,
            error_level=error_level,
            data=self.data,
            advice_text=advice_text,
            advice_params=advice_params,
        )

        # Valida @content-type apenas se presente (mesma lógica do alt-text)
        long_desc_content_type = self.data.get("long_desc_content_type")
        if long_desc_content_type:
            valid = long_desc_content_type in self.params["content_types"]

            if not valid:
                advice = (f"The value '{long_desc_content_type}' is invalid in {long_desc_xml}. "
                         f"Replace it with one of the accepted values: {self.params['content_types']}.")
                advice_text = _("The value {value} is invalid in {xml}. Replace it with one of the accepted values: {accepted_values}.")
                advice_params = {
                    "value": long_desc_content_type,
                    "xml": long_desc_xml,
                    "accepted_values": str(self.params["content_types"])
                }
            else:
                advice = None
                advice_text = None
                advice_params = None

            yield build_response(
                title="@content-type",
                parent=self.data,
                item="long-desc",
                sub_item="@content-type",
                is_valid=valid,
                validation_type="value in list",
                expected=self.params["content_types"],
                obtained=long_desc_content_type,
                advice=advice,
                error_level=self.params["content_type_error_level"],
                data=self.data,
                advice_text=advice_text,
                advice_params=advice_params,
            )

    def validate_transcript(self):
        """Checks for the presence of a transcript (<sec sec-type='transcript'>) for media."""
        transcript = self.data.get("transcript")
        valid = bool(transcript)

        if not valid:
            advice = (f'The transcript is missing in the {self.data["tag"]} element. '
                     'Add a <sec sec-type="transcript"> section to provide accessible text alternatives. Refer to SPS 1.10 docs for details.')
            advice_text = _('The transcript is missing in the {tag} element. Add a <sec sec-type="transcript"> section to provide accessible text alternatives. Refer to SPS 1.10 docs for details.')
            advice_params = {"tag": self.data["tag"]}
        else:
            advice = None
            advice_text = None
            advice_params = None

        return build_response(
            title="Transcript validation",
            parent=self.data,
            item="transcript",
            sub_item=None,
            is_valid=valid,
            validation_type="exist",
            expected="Present",
            obtained="Missing" if not transcript else "Present",
            advice=advice,
            error_level=self.params["transcript_error_level"],
            data=self.data,
            advice_text=advice_text,
            advice_params=advice_params,
        )

    def validate_speaker_and_speech(self):
        """Validates that <speaker> and <speech> elements are present when required in transcript sections."""
        speakers = self.data.get("speakers", [])

        if not speakers:
            valid = False
            obtained = "Missing"
            advice = ("Dialog elements are missing in the <sec sec-type='transcript'> section. "
                     "Use <speaker> and <speech> to represent the dialogue. Refer to SPS 1.10 docs for details.")
            advice_text = _("Dialog elements are missing in the <sec sec-type='transcript'> section. Use <speaker> and <speech> to represent the dialogue. Refer to SPS 1.10 docs for details.")
            advice_params = {}
        else:
            valid = True
            obtained = "Present"
            advice = None
            advice_text = None
            advice_params = None

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
            advice_text=advice_text,
            advice_params=advice_params,
        )

    def validate_accessibility_data_structure(self):
        """Checks if accessibility elements are correctly structured within a valid tag."""
        valid_tags = ("graphic", "inline-graphic", "media", "inline-media")
        tag = self.data.get("tag")
        valid = tag in valid_tags

        if not valid:
            advice = (f"Accessibility data is located in an invalid element: <{tag}>. "
                     f"Use one of the valid elements: {valid_tags}. Refer to SPS 1.10 docs for details.")
            advice_text = _("Accessibility data is located in an invalid element: <{tag}>. Use one of the valid elements: {valid_elements}. Refer to SPS 1.10 docs for details.")
            advice_params = {"tag": tag, "valid_elements": str(valid_tags)}
        else:
            advice = None
            advice_text = None
            advice_params = None

        return build_response(
            title="structure",
            parent=self.data,
            item=tag,
            sub_item=None,
            is_valid=valid,
            validation_type="value in list",
            expected=valid_tags,
            obtained=tag,
            advice=advice,
            error_level=self.params["structure_error_level"],
            data=self.data,
            advice_text=advice_text,
            advice_params=advice_params,
        )
