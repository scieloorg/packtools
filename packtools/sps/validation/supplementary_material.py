from lxml import etree
from langdetect import detect
from packtools.sps.models.supplementary_material import ArticleSupplementaryMaterials
from packtools.sps.validation.utils import build_response


class SupplementaryMaterialValidation:
    def __init__(self, supp, xml_tree, params):
        """
        Inicializa a validação de um material suplementar.

        Args:
            supp (dict): Dados do material suplementar extraídos do modelo
        """
        self.supp = supp
        self.article_lang = supp.get("parent_lang")
        self.xml_tree = xml_tree
        self.params = params

    def validate(self):
        """
        Executa todas as validações definidas.
        """
        yield self.validate_supplementary_material_structure()
        yield self.validate_supplementary_material_id()
        yield self.validate_supplementary_material_language()
        yield self.validate_supplementary_material_position()
        yield self.validate_supplementary_material_format()
        yield self.validate_supplementary_material_not_in_app_group()
        yield self.validate_sec_type_supplementary_material()
        yield self.validate_media_attributes()
        yield self.validate_accessibility_requirements()

    def validate_supplementary_material_structure(self):
        """
        Ensures that supplementary materials are inside <sec sec-type="supplementary-material">.
        """
        valid = self.supp.get("parent_tag") == "sec" and self.supp.get("parent_attrib_type") == "supplementary-material"
        return build_response(
            title="Supplementary material structure",
            parent=self.supp,
            item="supplementary-material",
            sub_item="parent sec-type",
            is_valid=valid,
            validation_type="structure",
            expected="Inside <sec sec-type='supplementary-material'>",
            obtained=self.supp.get("parent_tag"),
            advice="Supplementary materials must be inside <sec sec-type='supplementary-material'>.",
            error_level=self.params["supplementary_material_structure_error_level"],
            data=self.supp
        )

    def validate_supplementary_material_id(self):
        """
        Verifies the presence of required attribute id in supplementary materials.
        """
        valid = bool(self.supp.get("id"))
        return build_response(
            title="ID",
            parent=self.supp,
            item="supplementary-material",
            sub_item="@id",
            is_valid=valid,
            validation_type="exist",
            expected='<supplementary-material id="">',
            obtained=f'<supplementary-material id="{self.supp.get('id')}">',
            advice='Add supplementary material with id="" in <supplementary-material>: <supplementary-material id="">. Consult SPS documentation for more detail.',
            error_level=self.params["supplementary_material_attributes_error_level"],
            data=self.supp
        )

    def validate_supplementary_material_language(self):
        """
        Verifies if the language of the supplementary material is consistent with the article's language.
        """
        label_text = self.supp.get("label", "")
        detected_lang = detect(label_text) if label_text else "unknown"
        valid = detected_lang == self.article_lang
        return build_response(
            title="Consistency of language between article and supplementary material",
            parent=self.supp,
            item="supplementary-material",
            sub_item="language",
            is_valid=valid,
            validation_type="match",
            expected=self.article_lang,
            obtained=detected_lang,
            advice=f"The language of the supplementary material ({detected_lang}) differs from the language of the article ({self.article_lang}).",
            error_level=self.params["supplementary_material_language_error_level"],
            data=self.supp
        )

    def validate_supplementary_material_position(self):
        """
        Verifies if the supplementary materials section is in the last position of <body> or inside <back>.
        """
        article_body = self.xml_tree.find("body")
        article_back = self.xml_tree.find("back")
        parent_tag = self.supp.get("parent_tag")

        is_last_in_body = False
        is_in_back = False

        if article_body is not None:
            sections = article_body.findall("sec")
            if sections and sections[-1].get("sec-type") == "supplementary-material":
                is_last_in_body = True

        if article_back is not None:
            sections = article_back.findall("sec")
            is_in_back = any(sec.get("sec-type") == "supplementary-material" for sec in sections)

        valid = is_last_in_body or is_in_back

        return build_response(
            title="Position of supplementary materials",
            parent=self.supp,
            item="supplementary-material",
            sub_item="position",
            is_valid=valid,
            validation_type="position",
            expected="Last section of <body> or inside <back>",
            obtained=parent_tag,
            advice="The supplementary materials section must be at the end of <body> or inside <back>.",
            error_level=self.params["supplementary_material_position_error_level"],
            data=self.supp
        )

    def validate_supplementary_material_format(self):
        """
        Ensures that the supplementary material type matches the correct markup.
        """
        expected_format = {
            "application/pdf": "media",
            "image/jpeg": "graphic",
            "video/mp4": "media",
            "audio/mp3": "media",
            "application/zip": "media",
        }
        valid = expected_format.get(self.supp.get("mimetype")) == self.supp.get("media_type")
        return build_response(
            title="Correct format of supplementary material",
            parent=self.supp,
            item="supplementary-material",
            sub_item="format",
            is_valid=valid,
            validation_type="match",
            expected=expected_format.get(self.supp.get("mimetype")),
            obtained=self.supp.get("media_type"),
            advice=f"Incorrect format. Expected: {expected_format.get(self.supp.get('mimetype'))} for {self.supp.get('mimetype')}.",
            error_level=self.params["supplementary_material_format_error_level"],
            data=self.supp
        )

    def validate_supplementary_material_not_in_app_group(self):
        """
        Ensures that <supplementary-material> does not occur inside <app-group> and <app>.
        """
        valid = self.supp.get("parent_tag") not in ["app-group", "app"]
        return build_response(
            title="Prohibition of <supplementary-material> inside <app-group> and <app>",
            parent=self.supp,
            item="supplementary-material",
            sub_item="parent",
            is_valid=valid,
            validation_type="forbidden",
            expected="Outside <app-group> and <app>",
            obtained=self.supp.get("parent_tag"),
            advice="Do not use <supplementary-material> inside <app-group> or <app>.",
            error_level=self.params["supplementary_material_in_app_group_error_level"],
            data=self.supp
        )

    def validate_prohibited_inline_supplementary_material(self):
        """
        Ensures that <inline-supplementary-material> is not used.
        """

        obtained = etree.tostring(self.xml_tree.xpath(".//inline-supplementary-material")[0])
        valid = not bool(obtained)
        return build_response(
            title="Prohibition of inline-supplementary-material",
            parent=self.supp,
            item="inline-supplementary-material",
            sub_item=None,
            is_valid=valid,
            validation_type="forbidden",
            expected="No <inline-supplementary-material>",
            obtained=obtained,
            advice="The use of <inline-supplementary-material> is prohibited.",
            error_level=self.params["inline_supplementary_material_error_level"],
            data=self.supp
        )

    def validate_sec_type_supplementary_material(self):
        """Checks if all <sec> elements containing <supplementary-material> have @sec-type='supplementary-material'."""
        valid = self.supp.get("parent_tag") == "sec" and self.supp.get("parent_type") == "supplementary-material"
        return build_response(
            title="Mandatory attribute in <sec>",
            parent=self.supp,
            item="sec",
            sub_item="sec-type",
            is_valid=valid,
            validation_type="exist",
            expected="sec-type='supplementary-material'",
            obtained=self.supp.get("parent_type"),
            advice="Every section containing <supplementary-material> must have sec-type='supplementary-material'.",
            error_level=self.params["supplementary_material_sec_attributes_error_level"],
            data=self.supp
        )

    def validate_media_attributes(self):
        """Checks if <media> contains the mandatory attributes @id, @mime-type, @mime-subtype, @xlink:href."""
        media_node = self.supp.get("media_node")
        valid = media_node and all([
            media_node.get("id"),
            media_node.get("mimetype"),
            media_node.get("mime-subtype"),
            media_node.get("{http://www.w3.org/1999/xlink}href")
        ])
        return build_response(
            title="Mandatory attributes in <media>",
            parent=self.supp,
            item="media",
            sub_item="attributes",
            is_valid=valid,
            validation_type="exist",
            expected="id, mime-type, mime-subtype, xlink:href",
            obtained=None if not valid else "Present",
            advice="Each <media> must contain the attributes id, mime-type, mime-subtype, and xlink:href.",
            error_level=self.params["supplementary_material_midia_attributes_error_level"],
            data=self.supp
        )

    def validate_accessibility_requirements(self):
        """Checks if images and media contain a description in <alt-text> or <long-desc>."""
        media_node = self.supp.get("media_node")
        valid = media_node is not None and (media_node.find("alt-text") is not None or media_node.find("long-desc") is not None)
        return build_response(
            title="Accessibility requirements",
            parent=self.supp,
            item="supplementary-material",
            sub_item="accessibility",
            is_valid=valid,
            validation_type="exist",
            expected="alt-text or long-desc",
            obtained="Missing" if not valid else "Present",
            advice="Images, figures, videos, and audio files must contain <alt-text> or <long-desc> for accessibility.",
            error_level=self.params["supplementary_material_midia_accessibility_requirements_error_level"],
            data=self.supp
        )


class ArticleSupplementaryMaterialValidation:
    def __init__(self, xml_tree, params):
        self.article_supp = list(ArticleSupplementaryMaterials(xml_tree).data())
        self.xml_tree = xml_tree
        self.params = params

    def validate(self):
        for supp in self.article_supp:
            yield from SupplementaryMaterialValidation(supp, self.xml_tree, self.params).validate()

        SupplementaryMaterialValidation({}, self.xml_tree, self.params).validate_prohibited_inline_supplementary_material()
