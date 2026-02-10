import gettext
from packtools.sps.models.accessibility_data import XMLAccessibilityData
from packtools.sps.validation.utils import build_response

_ = gettext.gettext


class XMLAccessibilityDataValidation:
    """
    Validador principal para dados de acessibilidade em documentos XML SPS.

    Processa todos os elementos com dados de acessibilidade (<graphic>, <inline-graphic>,
    <media>, <inline-media>) e aplica as validações conforme SPS 1.9/1.10.
    """

    def __init__(self, xmltree, params):
        self.params = params
        self.xml_accessibility_data = XMLAccessibilityData(xmltree).data

    def validate(self):
        """
        Executa validações em todos os elementos de acessibilidade encontrados.

        Retorna:
            Generator de resultados de validação para cada elemento
        """
        for item in self.xml_accessibility_data:
            validator = AccessibilityDataValidation(item, self.params)
            yield from validator.validate()


class AccessibilityDataValidation:
    """
    Classe que implementa todas as validações de acessibilidade para um elemento específico.

    Valida elementos conforme especificação SPS 1.9/1.10 incluindo:
    - <alt-text>: descrições curtas (até 120 caracteres)
    - <long-desc>: descrições longas (mais de 120 caracteres)
    - <sec sec-type="transcript">: transcrições para áudio/vídeo
    - <speaker> e <speech>: elementos de diálogo em transcrições
    """

    def __init__(self, data, params):
        self.data = data
        self.params = params

    def validate(self):
        """
        Executa todas as validações definidas na ordem apropriada.

        Ordem de validação:
        1. Localização estrutural dos elementos
        2. Validações de conteúdo
        3. Validações de restrições específicas
        4. Validações de uso combinado
        """
        yield from self.validate_alt_text_location()
        yield from self.validate_alt_text()
        yield from self.validate_alt_text_media_restriction()
        yield from self.validate_alt_text_not_duplicate_label_caption()
        yield from self.validate_decorative_figure_alt_text()
        yield from self.validate_long_desc()
        yield from self.validate_long_desc_minimum_length()
        yield from self.validate_long_desc_media_restriction()
        yield from self.validate_long_desc_not_duplicate_label_caption()
        yield from self.validate_long_desc_occurrence()
        yield from self.validate_long_desc_incompatible_with_null_alt()
        yield from self.validate_media_xref_to_transcript()
        yield self.validate_transcript()
        yield self.validate_speaker_and_speech()
        yield self.validate_accessibility_data_structure()

    def validate_alt_text_location(self):
        """
        Valida se <alt-text> está dentro de um elemento válido.

        Regra SPS 1.9/1.10:
        "<alt-text> deve estar dentro de <graphic>, <inline-graphic>, <media> ou <inline-media>"

        Detalhes:
        - Detecta <alt-text> mal posicionado (ex: dentro de <fig>)
        - Sugere correção movendo para elemento apropriado

        Retorna:
            Generator de build_response apenas se elemento estiver mal posicionado
        """
        current_location = self.data.get("current_location")

        if not current_location:
            return

        parent_tag = self.data.get("parent_tag")
        parent_id = self.data.get("parent_id")
        expected = self.data.get("expected_location")

        advice = (
            f"<alt-text> is incorrectly located inside <{parent_tag}>. "
            f"According to SPS 1.9/1.10, <alt-text> must be inside one of these elements: "
            f"{', '.join(f'<{tag}>' for tag in expected)}. "
            f"Move the <alt-text> element inside the appropriate <graphic> or <media> element."
        )

        if parent_id:
            advice += f" (Found in <{parent_tag} id=\"{parent_id}\">)"

        advice_text = _(
            "<alt-text> is incorrectly located inside <{parent_tag}>. "
            "According to SPS 1.9/1.10, <alt-text> must be inside one of these elements: "
            "{expected_elements}. "
            "Move the <alt-text> element inside the appropriate <graphic> or <media> element."
        )

        advice_params = {
            "parent_tag": parent_tag,
            "expected_elements": ', '.join(f'<{tag}>' for tag in expected)
        }

        yield build_response(
            title="<alt-text> location",
            parent=self.data,
            item="alt-text",
            sub_item="location",
            is_valid=False,
            validation_type="structure",
            expected=f"Inside {expected}",
            obtained=f"Inside <{parent_tag}>",
            advice=advice,
            error_level="ERROR",
            data=self.data,
            advice_text=advice_text,
            advice_params=advice_params,
        )

    def validate_alt_text(self):
        """
        Valida existência, tamanho e atributos de <alt-text>.

        Regra SPS 1.9/1.10:
        "<alt-text> deve ter até 120 caracteres. Para descrições maiores, use <long-desc>.
        Quando gerado por máquina, deve ter @content-type='machine-generated'."

        Detalhes:
        - Verifica presença de <alt-text>
        - Valida tamanho máximo de 120 caracteres
        - Valida valores permitidos para @content-type quando presente

        Retorna:
            Generator com 1-2 build_response (existência/tamanho + content-type se aplicável)
        """
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

        # Valida @content-type quando presente
        alt_text_content_type = self.data.get("alt_text_content_type")
        if alt_text_content_type:
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
        Valida que <alt-text> em <media> e <inline-media> só ocorre para vídeo/áudio.

        Regra SPS 1.9/1.10:
        "Em <media> e <inline-media>, <alt-text> só deve ocorrer quando o formato do objeto
        for vídeo ou áudio, com @mime-type='video' @mime-subtype='mp4' ou
        @mime-type='audio' @mime-subtype='mp3'"

        Detalhes:
        - Só valida para elementos <media> e <inline-media>
        - Para outros tipos de arquivo (PDF, ZIP, XLSX), <alt-text> não deve ser usado
        - Sugere <long-desc> como alternativa

        Retorna:
            Generator de build_response apenas para <media>/<inline-media>
        """
        tag = self.data.get("tag")

        if tag not in ("media", "inline-media"):
            return

        alt_text = self.data.get("alt_text")
        mimetype = self.data.get("mimetype")
        mime_subtype = self.data.get("mime_subtype")

        if not alt_text:
            return

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
        Valida que <alt-text> não duplica conteúdo de <label> ou <caption>.

        Regra SPS 1.9/1.10:
        "O conteúdo de <alt-text> não deve ser usado para substituir ou copiar
        a informação descrita em <label> ou <caption>."

        Detalhes:
        - Compara texto de <alt-text> com <label> e <caption/title>
        - Texto deve ser descritivo, não redundante
        - Normaliza espaços para comparação

        Retorna:
            Generator de build_response quando há duplicação
        """
        alt_text = self.data.get("alt_text")
        if not alt_text:
            return

        parent_label = self.data.get("parent_label")
        parent_caption_title = self.data.get("parent_caption_title")

        alt_text_normalized = " ".join(alt_text.split())

        is_duplicate_label = False
        is_duplicate_caption = False

        if parent_label:
            label_normalized = " ".join(parent_label.split())
            is_duplicate_label = alt_text_normalized == label_normalized

        if parent_caption_title:
            caption_normalized = " ".join(parent_caption_title.split())
            is_duplicate_caption = alt_text_normalized == caption_normalized

        if is_duplicate_label or is_duplicate_caption:
            duplicated_element = "<label>" if is_duplicate_label else "<caption/title>"
            advice = (
                f"<alt-text> content duplicates {duplicated_element}. "
                f"According to SPS 1.9/1.10, <alt-text> should not copy content from <label> or <caption>. "
                f"Provide a unique, descriptive text for the visual element instead."
            )
            advice_text = _(
                "<alt-text> content duplicates {duplicated_element}. "
                "According to SPS 1.9/1.10, <alt-text> should not copy content from <label> or <caption>. "
                "Provide a unique, descriptive text for the visual element instead."
            )
            advice_params = {"duplicated_element": duplicated_element}
        else:
            advice = None
            advice_text = None
            advice_params = None

        if is_duplicate_label or is_duplicate_caption:
            yield build_response(
                title="<alt-text> duplication",
                parent=self.data,
                item="alt-text",
                sub_item="duplication check",
                is_valid=False,
                validation_type="match",
                expected="Unique descriptive text",
                obtained=f"Duplicates {duplicated_element}",
                advice=advice,
                error_level=self.params.get("alt_text_duplication_error_level", "WARNING"),
                data=self.data,
                advice_text=advice_text,
                advice_params=advice_params,
            )

    def validate_decorative_figure_alt_text(self):
        """
        Valida uso de <alt-text>null</alt-text> para figuras decorativas.

        Regra SPS 1.9/1.10:
        "Se uma imagem for apenas decorativa (decisão editorial), use <alt-text>null</alt-text>.
        Este uso permitirá que leitores de tela pulem imagens incluídas apenas por razões
        estéticas ou que são ilustrações do texto já fornecido."

        Detalhes:
        - Valida se <alt-text>null</alt-text> está sendo usado corretamente
        - Figuras decorativas devem ter exatamente o texto "null"
        - Não deve ter outros conteúdos quando marcada como decorativa

        Retorna:
            Generator de build_response quando há uso incorreto de "null"
        """
        alt_text = self.data.get("alt_text")
        if not alt_text:
            return

        alt_text_normalized = alt_text.strip().lower()

        if alt_text_normalized == "null":
            advice = (
                "<alt-text>null</alt-text> indicates a decorative figure. "
                "Ensure this is an editorial decision and the image is truly decorative "
                "(not essential for understanding the content). "
                "Refer to SPS 1.10 documentation for decorative images guidance."
            )
            advice_text = _(
                "<alt-text>null</alt-text> indicates a decorative figure. "
                "Ensure this is an editorial decision and the image is truly decorative "
                "(not essential for understanding the content). "
                "Refer to SPS 1.10 documentation for decorative images guidance."
            )
            advice_params = {}

            yield build_response(
                title="Decorative figure",
                parent=self.data,
                item="alt-text",
                sub_item="decorative",
                is_valid=True,
                validation_type="format",
                expected="null (for decorative images)",
                obtained="null",
                advice=advice,
                error_level="INFO",
                data=self.data,
                advice_text=advice_text,
                advice_params=advice_params,
            )

    def validate_long_desc(self):
        """
        Valida existência e atributos de <long-desc>.

        Regra SPS 1.9/1.10:
        "<long-desc> deve ter mais de 120 caracteres. Para descrições curtas, use <alt-text>.
        Quando gerado por máquina, deve ter @content-type='machine-generated'."

        Detalhes:
        - Verifica presença de <long-desc> para elementos complexos
        - Valida valores permitidos para @content-type quando presente
        - Descrições longas são recomendadas para gráficos, diagramas complexos

        Retorna:
            Generator com 0-2 build_response (existência + content-type se aplicável)
        """
        long_desc = self.data.get("long_desc")

        # Validação de content-type quando presente
        long_desc_content_type = self.data.get("long_desc_content_type")
        if long_desc_content_type:
            valid = long_desc_content_type in self.params["content_types"]

            if not valid:
                advice = (
                    f'The value \'{long_desc_content_type}\' is invalid in {self.data.get("long_desc_xml")}. '
                    f'Replace it with one of the accepted values: {self.params["content_types"]}.'
                )
                advice_text = _(
                    'The value {value} is invalid in {xml}. '
                    'Replace it with one of the accepted values: {accepted_values}.'
                )
                advice_params = {
                    "value": long_desc_content_type,
                    "xml": self.data.get("long_desc_xml"),
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

    def validate_long_desc_minimum_length(self):
        """
        Valida que <long-desc> tem MAIS de 120 caracteres.

        Regra SPS 1.9/1.10:
        "<long-desc> obrigatoriamente deve possuir conteúdo textual acima de 120 caracteres.
        Para descrições de até 120 caracteres use <alt-text>."

        Detalhes:
        - Tamanho mínimo: 121 caracteres
        - Se tiver ≤120 caracteres, deve usar <alt-text> ao invés
        - Descrições longas devem ser detalhadas e informativas

        Retorna:
            Generator de build_response quando tamanho é inválido
        """
        long_desc = self.data.get("long_desc")

        if not long_desc:
            return

        length = len(long_desc)
        valid = length > 120

        if not valid:
            advice = (
                f"<long-desc> has only {length} characters. "
                f"According to SPS 1.9/1.10, <long-desc> must have MORE than 120 characters. "
                f"Use <alt-text> for descriptions up to 120 characters, or expand this <long-desc> to provide more detail."
            )
            advice_text = _(
                "<long-desc> has only {length} characters. "
                "According to SPS 1.9/1.10, <long-desc> must have MORE than 120 characters. "
                "Use <alt-text> for descriptions up to 120 characters, or expand this <long-desc> to provide more detail."
            )
            advice_params = {"length": length}
        else:
            advice = None
            advice_text = None
            advice_params = None

        yield build_response(
            title="<long-desc> minimum length",
            parent=self.data,
            item="long-desc",
            sub_item="minimum length",
            is_valid=valid,
            validation_type="format",
            expected="More than 120 characters",
            obtained=f"{length} characters",
            advice=advice,
            error_level=self.params.get("long_desc_minimum_length_error_level", "ERROR"),
            data=self.data,
            advice_text=advice_text,
            advice_params=advice_params,
        )

    def validate_long_desc_media_restriction(self):
        """
        Valida que <long-desc> em <media> e <inline-media> só ocorre para vídeo/áudio.

        Regra SPS 1.9/1.10:
        "Em <media> e <inline-media>, <long-desc> só deve ocorrer quando o formato do objeto
        for vídeo ou áudio, com @mime-type='video' @mime-subtype='mp4' ou
        @mime-type='audio' @mime-subtype='mp3'"

        Detalhes:
        - Só valida para elementos <media> e <inline-media>
        - Para outros tipos de arquivo, <long-desc> não deve ser usado
        - Vídeo e áudio são os únicos formatos que justificam descrições longas

        Retorna:
            Generator de build_response apenas para <media>/<inline-media>
        """
        tag = self.data.get("tag")

        if tag not in ("media", "inline-media"):
            return

        long_desc = self.data.get("long_desc")
        mimetype = self.data.get("mimetype")
        mime_subtype = self.data.get("mime_subtype")

        if not long_desc:
            return

        valid_combinations = [
            ("video", "mp4"),
            ("audio", "mp3"),
        ]

        current = (mimetype, mime_subtype)
        valid = current in valid_combinations

        if not valid:
            advice = (
                f"In <{tag}>, <long-desc> should only be used for video (mp4) or audio (mp3) files. "
                f"Current mime-type is '{mimetype}' with mime-subtype '{mime_subtype}'. "
                f"For other file types, <long-desc> is not appropriate. "
                f"Refer to SPS 1.10 documentation for details."
            )
            advice_text = _(
                "In <{tag}>, <long-desc> should only be used for video (mp4) or audio (mp3) files. "
                "Current mime-type is {mimetype} with mime-subtype {mime_subtype}. "
                "For other file types, <long-desc> is not appropriate. "
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
            title="<long-desc> restriction for media",
            parent=self.data,
            item="long-desc",
            sub_item="media restriction",
            is_valid=valid,
            validation_type="value in list",
            expected=f"mime-type/mime-subtype combinations: {valid_combinations}",
            obtained=f"{mimetype}/{mime_subtype}",
            advice=advice,
            error_level=self.params.get("long_desc_media_restriction_error_level", "ERROR"),
            data=self.data,
            advice_text=advice_text,
            advice_params=advice_params,
        )

    def validate_long_desc_not_duplicate_label_caption(self):
        """
        Valida que <long-desc> não duplica conteúdo de <label> ou <caption>.

        Regra SPS 1.9/1.10:
        "O conteúdo de <long-desc> não deve ser usado para substituir ou copiar
        a informação descrita em <label> ou <caption>."

        Detalhes:
        - Compara texto de <long-desc> com <label> e <caption/title>
        - Descrição longa deve adicionar informação, não duplicar
        - Normaliza espaços para comparação

        Retorna:
            Generator de build_response quando há duplicação
        """
        long_desc = self.data.get("long_desc")
        if not long_desc:
            return

        parent_label = self.data.get("parent_label")
        parent_caption_title = self.data.get("parent_caption_title")

        long_desc_normalized = " ".join(long_desc.split())

        is_duplicate_label = False
        is_duplicate_caption = False

        if parent_label:
            label_normalized = " ".join(parent_label.split())
            is_duplicate_label = long_desc_normalized == label_normalized

        if parent_caption_title:
            caption_normalized = " ".join(parent_caption_title.split())
            is_duplicate_caption = long_desc_normalized == caption_normalized

        if is_duplicate_label or is_duplicate_caption:
            duplicated_element = "<label>" if is_duplicate_label else "<caption/title>"
            advice = (
                f"<long-desc> content duplicates {duplicated_element}. "
                f"According to SPS 1.9/1.10, <long-desc> should not copy content from <label> or <caption>. "
                f"Provide a detailed, unique description that adds value beyond the label or caption."
            )
            advice_text = _(
                "<long-desc> content duplicates {duplicated_element}. "
                "According to SPS 1.9/1.10, <long-desc> should not copy content from <label> or <caption>. "
                "Provide a detailed, unique description that adds value beyond the label or caption."
            )
            advice_params = {"duplicated_element": duplicated_element}
        else:
            advice = None
            advice_text = None
            advice_params = None

        if is_duplicate_label or is_duplicate_caption:
            yield build_response(
                title="<long-desc> duplication",
                parent=self.data,
                item="long-desc",
                sub_item="duplication check",
                is_valid=False,
                validation_type="match",
                expected="Unique detailed description",
                obtained=f"Duplicates {duplicated_element}",
                advice=advice,
                error_level=self.params.get("long_desc_duplication_error_level", "WARNING"),
                data=self.data,
                advice_text=advice_text,
                advice_params=advice_params,
            )

    def validate_long_desc_occurrence(self):
        """
        Valida que há no máximo um <long-desc> por elemento gráfico/media.

        Regra SPS 1.9/1.10:
        "<long-desc> deve ocorrer uma única vez por elemento. Múltiplas ocorrências
        não são permitidas."

        Detalhes:
        - Apenas 0 ou 1 <long-desc> permitido
        - Múltiplas descrições longas causam ambiguidade
        - Se necessário múltiplas descrições, consolidar em uma única

        Retorna:
            Generator de build_response sempre (válido ou inválido)
        """
        long_desc_count = self.data.get("long_desc_count", 0)

        valid = long_desc_count <= 1

        if not valid:
            advice = (
                f"Found {long_desc_count} <long-desc> elements. "
                f"Only one <long-desc> is allowed per graphic/media element. "
                f"Remove duplicate <long-desc> elements. "
                f"Refer to SPS 1.10 documentation for details."
            )
            advice_text = _(
                "Found {count} <long-desc> elements. "
                "Only one <long-desc> is allowed per graphic/media element. "
                "Remove duplicate <long-desc> elements. "
                "Refer to SPS 1.10 documentation for details."
            )
            advice_params = {
                "count": long_desc_count
            }
        else:
            advice = None
            advice_text = None
            advice_params = None

        yield build_response(
            title="<long-desc> occurrence",
            parent=self.data,
            item="long-desc",
            sub_item="occurrence",
            is_valid=valid,
            validation_type="format",
            expected="0 or 1 occurrence",
            obtained=f"{long_desc_count} occurrence(s)",
            advice=advice,
            error_level=self.params.get("long_desc_occurrence_error_level", "ERROR"),
            data=self.data,
            advice_text=advice_text,
            advice_params=advice_params,
        )

    def validate_long_desc_incompatible_with_null_alt(self):
        """
        Valida incompatibilidade entre <long-desc> e <alt-text>null</alt-text>.

        Regra SPS 1.9/1.10:
        "Quando houver uso combinado <alt-text> não pode ter conteúdo null.
        Quando usar marcação combinada, <alt-text> não pode ter conteúdo nulo;
        neste caso, não use <alt-text>."

        Detalhes:
        - <long-desc> indica conteúdo importante que requer descrição detalhada
        - <alt-text>null</alt-text> indica figura decorativa
        - Estes dois usos são mutuamente exclusivos e contraditórios

        Retorna:
            Generator de build_response quando ambos estão presentes
        """
        long_desc = self.data.get("long_desc")
        alt_text = self.data.get("alt_text")

        if not long_desc or not alt_text:
            return

        alt_text_normalized = alt_text.strip().lower()
        valid = alt_text_normalized != "null"

        if not valid:
            advice = (
                f"Found <alt-text>null</alt-text> combined with <long-desc>. "
                f"When using <long-desc>, do not use <alt-text>null</alt-text>. "
                f"Either remove <alt-text> or provide meaningful content instead of 'null'. "
                f"Refer to SPS 1.10 documentation for combined markup guidance."
            )
            advice_text = _(
                "Found <alt-text>null</alt-text> combined with <long-desc>. "
                "When using <long-desc>, do not use <alt-text>null</alt-text>. "
                "Either remove <alt-text> or provide meaningful content instead of 'null'. "
                "Refer to SPS 1.10 documentation for combined markup guidance."
            )
            advice_params = {}
        else:
            advice = None
            advice_text = None
            advice_params = None

        yield build_response(
            title="<long-desc> incompatibility with null alt-text",
            parent=self.data,
            item="long-desc",
            sub_item="null alt-text incompatibility",
            is_valid=valid,
            validation_type="format",
            expected="<alt-text> not 'null' when <long-desc> is present",
            obtained=f"alt-text='{alt_text}'",
            advice=advice,
            error_level=self.params.get("long_desc_null_incompatibility_error_level", "WARNING"),
            data=self.data,
            advice_text=advice_text,
            advice_params=advice_params,
        )

    def validate_media_xref_to_transcript(self):
        """
        Valida que <media>/<inline-media> com áudio/vídeo tem <xref ref-type="sec"> para transcrição.

        Regra SPS 1.9/1.10:
        "<media> e <inline-media> devem incluir uma referência cruzada <xref ref-type='sec'>,
        que vincula a transcrição com a seção de transcrição <sec sec-type='transcript'>."

        Detalhes:
        - Só valida para <media> e <inline-media> com áudio ou vídeo
        - <xref> deve ter @ref-type="sec" e @rid apontando para a transcrição
        - Transcrições são recomendadas para acessibilidade de conteúdo multimídia

        Retorna:
            Generator de build_response apenas para media com áudio/vídeo
        """
        tag = self.data.get("tag")

        if tag not in ("media", "inline-media"):
            return

        mimetype = self.data.get("mimetype")
        if mimetype not in ("audio", "video"):
            return

        xref_sec_rid = self.data.get("xref_sec_rid")
        valid = bool(xref_sec_rid)

        if not valid:
            advice = (
                f"<{tag}> with {mimetype} is missing <xref ref-type=\"sec\"> linking to transcript section. "
                f"According to SPS 1.9/1.10, audio and video elements should include a reference to their transcript section. "
                f"Add: <xref ref-type=\"sec\" rid=\"TRANSCRIPT_ID\"/> inside <{tag}>. "
                f"Refer to SPS 1.10 documentation for details."
            )
            advice_text = _(
                "<{tag}> with {mimetype} is missing <xref ref-type=\"sec\"> linking to transcript section. "
                "According to SPS 1.9/1.10, audio and video elements should include a reference to their transcript section. "
                "Add: <xref ref-type=\"sec\" rid=\"TRANSCRIPT_ID\"/> inside <{tag}>. "
                "Refer to SPS 1.10 documentation for details."
            )
            advice_params = {"tag": tag, "mimetype": mimetype}
        else:
            advice = None
            advice_text = None
            advice_params = None

        yield build_response(
            title="<xref> to transcript section",
            parent=self.data,
            item="xref",
            sub_item="transcript reference",
            is_valid=valid,
            validation_type="exist",
            expected="<xref ref-type=\"sec\" rid=\"...\">",
            obtained=xref_sec_rid or "Missing",
            advice=advice,
            error_level=self.params.get("xref_transcript_error_level", "WARNING"),
            data=self.data,
            advice_text=advice_text,
            advice_params=advice_params,
        )

    def validate_transcript(self):
        """
        Valida presença de transcrição para elementos de áudio e vídeo.

        Regra SPS 1.9/1.10:
        "Recomenda-se que vídeos e áudios sempre venham acompanhados de seções de transcrição
        <sec sec-type='transcript'> e não apenas <alt-text> e/ou <long-desc>."

        Detalhes:
        - Só valida para <media> e <inline-media>
        - Só valida para @mime-type="audio" ou @mime-type="video"
        - Transcrições fornecem texto completo do conteúdo falado e sons
        - Não aplicável a imagens estáticas (<graphic>, <inline-graphic>)

        Retorna:
            build_response apenas para media com áudio/vídeo
        """
        tag = self.data.get("tag")

        # CORREÇÃO: Só valida para <media> e <inline-media>
        if tag not in ("media", "inline-media"):
            return

        # CORREÇÃO: Só valida para áudio/vídeo
        mimetype = self.data.get("mimetype")
        if mimetype not in ("audio", "video"):
            return

        transcript = self.data.get("transcript")
        valid = bool(transcript)

        if not valid:
            advice = (f'The transcript is missing in the {tag} element. '
                     'Add a <sec sec-type="transcript"> section to provide accessible text alternatives. Refer to SPS 1.10 docs for details.')
            advice_text = _('The transcript is missing in the {tag} element. Add a <sec sec-type="transcript"> section to provide accessible text alternatives. Refer to SPS 1.10 docs for details.')
            advice_params = {"tag": tag}
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
        """
        Valida presença de <speaker> e <speech> em transcrições de diálogos.

        Regra SPS 1.9/1.10:
        "Quando o diálogo/discussão ocorrer entre duas ou mais entidades, deverão ser
        utilizados os elementos <speaker> (orador) e <speech> (texto proferido)."

        Detalhes:
        - Só valida para <media> e <inline-media>
        - Só valida para @mime-type="audio" ou @mime-type="video"
        - Só valida quando há transcrição presente
        - Diálogos devem ter estrutura clara de quem fala e o que fala
        - Não aplicável a imagens ou media sem transcrição

        Retorna:
            build_response apenas para media com áudio/vídeo e transcrição
        """
        tag = self.data.get("tag")

        # CORREÇÃO: Só valida para <media> e <inline-media>
        if tag not in ("media", "inline-media"):
            return

        # CORREÇÃO: Só valida para áudio/vídeo
        mimetype = self.data.get("mimetype")
        if mimetype not in ("audio", "video"):
            return

        # CORREÇÃO: Só valida se há transcrição
        transcript = self.data.get("transcript")
        if not transcript:
            return

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
        """
        Valida que elementos de acessibilidade estão dentro de tags válidas.

        Regra SPS 1.9/1.10:
        "Elementos de acessibilidade (<alt-text>, <long-desc>) devem estar contidos
        dentro de <graphic>, <inline-graphic>, <media> ou <inline-media>."

        Detalhes:
        - Valida estrutura hierárquica correta do XML
        - Garante que dados de acessibilidade estão nos elementos apropriados
        - Tags válidas: graphic, inline-graphic, media, inline-media

        Retorna:
            build_response sempre (válido ou inválido)
        """
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
