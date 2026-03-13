from lxml import etree
from packtools.sps.models.supplementary_material import XmlSupplementaryMaterials
from packtools.sps.validation.graphic import GraphicValidation
from packtools.sps.validation.media import MediaValidation
from packtools.sps.validation.utils import build_response


class SupplementaryMaterialValidation:
    def __init__(self, data, params):
        """
        Inicializa a validação de um material suplementar.

        Args:
            data (dict): Dados do material suplementar extraídos do modelo
            params (dict): Parâmetros de configuração de validação
        """
        self.data = data
        self.params = params

    def validate(self):
        """
        Executa todas as validações definidas.
        """
        yield from MediaValidation(self.data, self.params).validate()
        yield from GraphicValidation(self.data, self.params).validate()
        yield self.validate_id()
        yield self.validate_sec_type()
        yield self.validate_label()
        yield self.validate_not_in_app_group()
        yield self.validate_content()

    def validate_id(self):
        """
        Verifica a presença obrigatória de @id em <supplementary-material>.
        """
        suppl_id = self.data.get("id")
        valid = bool(suppl_id)
        return build_response(
            title="supplementary-material @id",
            parent=self.data,
            item="supplementary-material",
            sub_item="@id",
            is_valid=valid,
            validation_type="exist",
            expected="@id in <supplementary-material>",
            obtained=suppl_id,
            advice='Add @id to <supplementary-material>: <supplementary-material id="...">. Consult SPS documentation for more detail.',
            error_level=self.params["id_error_level"],
            data=self.data,
        )

    def validate_sec_type(self):
        """
        Verifica se <supplementary-material> está inserido em <sec>, caso esteja, valida @sec-type="supplementary-material"
        """
        if self.data.get("parent_suppl_mat") == "sec":
            sec_type = self.data.get("sec_type")
            valid = sec_type == "supplementary-material"
            return build_response(
                title="@sec-type",
                parent=self.data,
                item="sec",
                sub_item="supplementary-material",
                is_valid=valid,
                validation_type="match",
                expected="<sec sec-type='supplementary-material'>",
                obtained=self.data.get("parent_tag"),
                advice=f'In <sec sec-type="{sec_type}"><supplementary-material> replace "{sec_type}" with "supplementary-material".',
                error_level=self.params["sec_type_error_level"],
                data=self.data,
            )

    def validate_label(self):
        """
        Verifica a presença obrigatória de <label> em <supplementary-material>.
        Uses suppl_label which preserves the supplementary-material's own label
        even when media/graphic data is merged.
        """
        label = self.data.get("suppl_label") or self.data.get("label")
        valid = bool(label)
        return build_response(
            title="label",
            parent=self.data,
            item="supplementary-material",
            sub_item="label",
            is_valid=valid,
            validation_type="exist",
            expected="<label> in <supplementary-material>",
            obtained=label,
            advice="Add label in <supplementary-material>: <supplementary-material><label>. Consult SPS documentation for more detail.",
            error_level=self.params["label_error_level"],
            data=self.data,
        )

    def validate_not_in_app_group(self):
        """
        Ensures that <supplementary-material> does not occur inside <app-group> and <app>.
        """
        valid = self.data.get("parent_suppl_mat") not in self.params["parent_suppl_mat_expected"]
        return build_response(
            title="Prohibition of <supplementary-material> inside <app-group> and <app>",
            parent=self.data,
            item="supplementary-material",
            sub_item="parent",
            is_valid=valid,
            validation_type="forbidden",
            expected="Outside <app-group> and <app>",
            obtained=self.data.get("parent_tag"),
            advice="Do not use <supplementary-material> inside <app-group> or <app>.",
            error_level=self.params["app_group_error_level"],
            data=self.data,
        )

    def validate_content(self):
        """
        Verifica a presença de <graphic> ou <media> dentro de <supplementary-material>.
        """
        has_content = self.data.get("has_content", False)
        valid = bool(has_content)
        return build_response(
            title="supplementary-material content",
            parent=self.data,
            item="supplementary-material",
            sub_item="graphic or media",
            is_valid=valid,
            validation_type="exist",
            expected="<graphic> or <media> in <supplementary-material>",
            obtained=self.data.get("visual_elem") if has_content else None,
            advice="Add <graphic> (for figures) or <media> (for other types) inside <supplementary-material>.",
            error_level=self.params["content_error_level"],
            data=self.data,
        )


class XmlSupplementaryMaterialValidation:
    def __init__(self, xml_tree, params):
        self.article_supp = list(XmlSupplementaryMaterials(xml_tree).items)
        self.xml_tree = xml_tree
        self.params = params

    def validate_prohibited_inline(self):
        """
        Ensures that <inline-supplementary-material> is not used.
        """
        nodes = self.xml_tree.xpath(".//inline-supplementary-material")
        obtained = etree.tostring(nodes[0]) if nodes else "None"
        valid = not bool(nodes)

        return build_response(
            title="Prohibition of inline-supplementary-material",
            parent={},
            item="inline-supplementary-material",
            sub_item=None,
            is_valid=valid,
            validation_type="forbidden",
            expected="No <inline-supplementary-material>",
            obtained=obtained,
            advice="The use of <inline-supplementary-material> is prohibited.",
            error_level=self.params["inline_error_level"],
            data={},
        )

    def validate_position(self):
        """
        Verifies if the supplementary materials section is in the last position of <body> or inside <back>.
        """
        sections = self.xml_tree.xpath('.//sec[@sec-type="supplementary-material"]')
        if not sections:
            return

        article_body = self.xml_tree.find("body")
        article_back = self.xml_tree.find("back")

        is_last_in_body = False
        is_in_back = False

        if article_body is not None:
            sections = article_body.findall("sec")
            if sections and sections[-1].get("sec-type") == "supplementary-material":
                is_last_in_body = True

        if article_back is not None:
            sections = article_back.findall("sec")
            is_in_back = any(
                sec.get("sec-type") == "supplementary-material" for sec in sections
            )

        valid = is_last_in_body or is_in_back

        if is_last_in_body:
            parent_tag = "body (last section)"
        elif is_in_back:
            parent_tag = "back"
        else:
            parent_tag = None

        return build_response(
            title="Position of supplementary materials",
            parent={},
            item="supplementary-material",
            sub_item=None,
            is_valid=valid,
            validation_type="position",
            expected="Last section of <body> or inside <back>",
            obtained=parent_tag,
            advice="The supplementary materials section must be at the end of <body> or inside <back>.",
            error_level=self.params["position_error_level"],
            data={},
        )

    def validate_sec_title(self):
        """
        Validates that <sec sec-type="supplementary-material"> contains a <title> element.
        """
        sections = self.xml_tree.xpath('.//sec[@sec-type="supplementary-material"]')
        for sec in sections:
            title_elem = sec.find("title")
            title_text = title_elem.text if title_elem is not None else None
            valid = bool(title_text)
            yield build_response(
                title="sec supplementary-material title",
                parent={},
                item="sec",
                sub_item="title",
                is_valid=valid,
                validation_type="exist",
                expected='<title> in <sec sec-type="supplementary-material">',
                obtained=title_text,
                advice='Add <title> to <sec sec-type="supplementary-material">: <sec sec-type="supplementary-material"><title>...</title></sec>.',
                error_level=self.params["sec_title_error_level"],
                data={},
            )

    def validate_id_uniqueness(self):
        """
        Validates that each <supplementary-material> has a unique @id.
        """
        seen_ids = {}
        for supp in self.article_supp:
            suppl_id = supp.get("id")
            if not suppl_id:
                continue
            if suppl_id in seen_ids:
                yield build_response(
                    title="supplementary-material @id uniqueness",
                    parent=supp,
                    item="supplementary-material",
                    sub_item="@id",
                    is_valid=False,
                    validation_type="unique",
                    expected="Unique @id for each <supplementary-material>",
                    obtained=f'Duplicate @id="{suppl_id}"',
                    advice=f'Replace duplicate @id="{suppl_id}" with a unique value in <supplementary-material>.',
                    error_level=self.params["id_uniqueness_error_level"],
                    data=supp,
                )
            seen_ids[suppl_id] = True

    def validate(self):
        for supp in self.article_supp:
            yield from SupplementaryMaterialValidation(
                supp, self.params
            ).validate()

        yield self.validate_prohibited_inline()
        yield self.validate_position()
        yield from self.validate_sec_title()
        yield from self.validate_id_uniqueness()
